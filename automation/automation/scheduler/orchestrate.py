# -*- coding: utf-8 -*-

import asyncio
import json,os,sys,time,random,threading,datetime,traceback
import queue
import concurrent.futures
from pytz import utc
from multiprocessing import Process

import apscheduler.executors.pool
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.schedulers.tornado import TornadoScheduler

import tornado.ioloop
import tornado.gen
import tornado.iostream
from tornado.tcpclient import TCPClient
from tornado.queues import Queue

from automation.common.network import ServerWrapper
from automation.common.logging import Logger
from automation.common.application import Configure
from automation.common.elasticsearch import ESHandler
from automation.common.network import SimpleTcpclient
from automation.common.constants import StatusCode

class ParellelSchedule(Process):
    
  def __init__(self, p_main_jod_queue=None):
    Process.__init__(self)  
    #threading.Thread.__init__(self)  
    self._scheduler = None
    #self._crawler_maps = None
    #self._crawlerPicker = p_crawler_picker
    self._inijoblock = threading.Lock()
    self._master_job_queue = p_main_jod_queue
#     if p_crawler_maps:
#       self._crawler_maps = p_crawler_maps  
#       self.initJobs()
  
#   def getCrawlerMaps(self):
#     return self._crawler_maps

  def initJobs1(self):
    try:
      if self._scheduler != None:
        return
  
      if self._inijoblock.acquire(blocking=False) == False:
        return  
      print ("############  Start initialize jobs  #############")  
      inijobs = Configure.configure().value("scheduler.threads")
      if len(inijobs) > 0:  
        executors = {
                'default': apscheduler.executors.pool.ThreadPoolExecutor(len(inijobs)),
                'processpool': apscheduler.executors.pool.ProcessPoolExecutor(1)
                 }
        job_defaults = {
                'coalesce': True,
                'max_instances': 1
                 }
        self._scheduler = BackgroundScheduler(executors=executors, job_defaults=job_defaults, timezone=utc)  
        self._jobs={}
        for jobkey in inijobs.keys():
          jobitem = inijobs[jobkey]
          job = Job(p_name=jobkey, p_queue=self._master_job_queue, p_interval=jobitem["interval"], p_threads=jobitem["threadsNum"], p_batchnum=jobitem["batchnum"], p_indice=jobitem["indice"], p_type=jobitem["type"] )
          print ("add job => ", jobkey,jobitem["interval"], jobitem["threadsNum"], jobitem["batchnum"], jobitem["indice"], jobitem["type"])
          added = self._scheduler.add_job(job,'interval',seconds=jobitem["interval"])
          self._jobs[jobkey] = added
          
        self._scheduler.start()
    except:
      self._scheduler = None
      traceback.print_exc()
      print ("Job initialize error")
    finally:
      self._inijoblock.release()
  
  #@tornado.gen.coroutine 
  def initJobs(self, p_jobSync):
    try:
      print ("start sync")
      if self._inijoblock.acquire(blocking=False) == False:
        return  
      print ("############  Start initialize sync coroutines  #############")  
      inijobs = Configure.configure().value("scheduler.threads")
      if len(inijobs) > 0:  
        for jobkey in inijobs.keys():
          jobitem = inijobs[jobkey]
          parallelnum = jobitem["threadsNum"]
          for idx in range(parallelnum):
            job = Job(p_name=jobkey, p_queue=self._master_job_queue, p_interval=jobitem["interval"], p_threads=jobitem["threadsNum"], p_batchnum=jobitem["batchnum"], p_indice=jobitem["indice"], p_type=jobitem["type"], p_index=idx, p_jobSync=self._jobSync )
            print ("Initial jod ", job)
            job.start()
    except:
      traceback.print_exc()
      print ("sync coroutines initialize error")
    finally:
      self._inijoblock.release()
                      
  def run(self):
    #self.initJobs()
    
    registerserver = Configure.configure().value("server.healthServer.host")
    registerport = Configure.configure().value("server.healthServer.port")
    self._jobSync = JobSync(p_queue=self._master_job_queue, p_register={"host":registerserver, "port":registerport} )
    self._jobSync.update()
    
    #asyncio.set_event_loop(asyncio.new_event_loop())
    self.initJobs(p_jobSync=self._jobSync)
    tornado.ioloop.IOLoop.current().start()

  def shutdown(self):
    if self._scheduler != None:  
      self._scheduler.shutdown()

class Job(object):

  def __init__(self, p_name, p_queue, p_interval, p_threads, p_batchnum, p_indice, p_type, p_index=None, p_jobSync=None):
    self._name=p_name
    self._main_job_queue=p_queue
    self._interval=p_interval
    
    self._threadnum=p_threads
    self._batchnum=p_batchnum
    
    self._indice = p_indice 
    self._type = p_type
    #self._crawler_picker = p_crawler_picker
    
    self._job_fetch_pool = concurrent.futures.ThreadPoolExecutor(max_workers=self._threadnum)
    self._last_exec_time=None
    self._last_exec_duration=None
    
    self._jobidx = p_index
    self._jobSync = p_jobSync
    
  def __call__(self):
    print ("job %s running...", self._name)  
    self._last_exec_time = datetime.datetime.now()
    futures = []  
    for i in range(self._threadnum):
      future = self._job_fetch_pool.submit(self.sync, self._name, i, self._threadnum, self._batchnum, self._indice, self._type )
      futures.append(future)
      
    for fu in futures:
      res = fu.result()
    self._last_exec_duration = (datetime.datetime.now()-self._last_exec_time).seconds 
  
  @tornado.gen.coroutine
  def start(self):
    print ("Job[%s] starts..."%(self._name))
    
    while True:
      loop=0  
      print (datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))  
      yield tornado.gen.sleep(self._interval) 
      print ( "Run once job after %d seconds"% (self._interval) ) 
      if self._jobSync.nsize() == 0:
        print ( "no available work node, skip this loop" )
        continue
    
      try:
        while True:  
          start = self._threadnum * self._batchnum * loop
          ifrom = self._jobidx * self._batchnum + start
          loop = loop + 1
          print ( "selelct job data from %d"% (ifrom) )
          docs = ESHandler.ESClient.precise_search(p_indice=self._indice, p_type=self._type, p_qry_map=[{"group": self._name}, {"status": 1}], p_size=self._batchnum, p_from=ifrom) 
          if docs == None or len(docs) == 0:
            break
          for rec in docs:
            scenario = rec["_source"]
            data = {"event": "work", "scenario": scenario} 
            print ("send job data to main queue") 
            yield self._main_job_queue.put(data)    
#           client = node["node_client"]
#           mq = node["mq"]
#           client.setHandler(p_callback=self)
#           
#           data = {"sendno": None, "message": scenario}  
#           mq.put(data, block=False)
    
      except:
        self.reportExcept()
   
  #@tornado.gen.coroutine 
  def sync1(self):
        print ("job start put message to queue")
        yield self._main_job_queue.put({"test":"message"})
        print ("after put message")
        
  def sync(self, p_name, p_tindex, p_threadnum, p_batchnum, p_indice, p_type ):
    size = p_batchnum  
    loop=0
  
    while True:
      start = p_threadnum * size * loop
      ifrom = p_tindex * size + start
      loop = loop + 1
      docs = ESHandler.ESClient.precise_search(p_indice=p_indice, p_type=p_type, p_qry_map=[{"group": self._name}, {"status": 1}], p_size=size, p_from=ifrom) 
      if docs == None:
        break;
      for rec in docs:
        scenario = rec["_source"]
        try:
          data = {"event": "work", "scenario": scenario} 
          print ("send job data to main queue") 
          self._main_job_queue.put(data)    
#           client = node["node_client"]
#           mq = node["mq"]
#           client.setHandler(p_callback=self)
#           
#           data = {"sendno": None, "message": scenario}  
#           mq.put(data, block=False)
    
        except:
          self.reportExcept()
          
  def reportExcept(self):
    pass 
  
class CrawlerRegister(Process):
    
  def __init__(self, p_crawler_picker=None, p_main_jod_queue=None): 
    Process.__init__(self)
    #self._crawlerPicker = p_crawler_picker
    #self._master_job_queue = p_main_jod_queue
    self._reg_node_list = {}
    self._events = {
      "register": self.registerCrawler,
      "heartbeat": self.sendHeartBeat,
      "activelist": self.getAvailableNodeList
    }
    
  def run(self):
    ServerWrapper.listen(p_name="Master-Scheduler", p_prefix="server.healthServer", p_handler=self)
    tornado.ioloop.IOLoop.current().start()

  def registerCrawler(self, p_request_body):
    print ("register crawler...", p_request_body)
    try:  
      crawler = p_request_body 
       
      if crawler["id"] in self._reg_node_list:
        print ("crawler already registered!")
        return { "status": StatusCode.ERROR, "message": "crawler already registered!" }
      self._reg_node_list[crawler["id"]] = { "host": crawler["host"], "port": crawler["port"], "registerTime": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "renewalTime": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
#       if self._crawler_maps == None:
#         self._crawler_maps = {}
      #c = self.Sync(p_queue=self._master_job_queue, p_crawler=crawler)      
      #self._crawlerPicker.addItem(p_id=crawler["id"], p_item = c)
      #c.start()
       
    except:
      traceback.print_exc()
      return { "status": StatusCode.ERROR, "message": "Register met error" }
        
    return { "status": StatusCode.OK, "message": "DONE" }
  
  def sendHeartBeat(self, p_request_body):
    pass

  def getAvailableNodeList(self, p_request_body):
    return { "status": StatusCode.OK, "message": "DONE", "reg_node_list": self._reg_node_list }
      
  def callback(self, p_message=None):
    body = json.loads(p_message)  
    event = body["event"] if "event" in body else None
    if event == None:
      return json.dumps({"status": StatusCode.ERROR, "message": "Unknown event type"})    
    
    res = self._events[event](body)
    #res = self.registerCrawler(p_crawler=p_message)   
#     if res:
#       status = StatusCode.OK
#     else :
#       status = StatusCode.ERROR  
#     ret = {"status": status, "message": "Register done"}
    return json.dumps(res)


class JobSync(threading.Thread):
    
    def __init__(self, p_queue, p_register, p_crawler_picker=None, p_clientnum=1):
      threading.Thread.__init__(self)
      #Process.__init__(self)
      self._crawlerPicker = p_crawler_picker
      self._main_queue = p_queue
      self._register = p_register
      
      self._node_list = {}
      self._num = p_clientnum
      
    def setProp(self, p_prop, p_val):
      self._crawler[p_prop] = p_val 
    
    def getProp(self, p_prop):
      return self._crawler[p_prop]
  
    def nsize(self):
      return len(self._node_list)
  
    @tornado.gen.coroutine
    def update(self):
      print ("Start connect to register server: ", self._register["host"], self._register["port"])  
      self.stream = yield TCPClient().connect(self._register["host"], self._register["port"])
      print ("Start update node list from register server...")
      count=0
      while True:
        try:
          message={"event":"activelist"}
          encode_json = json.dumps(message)  
          self.stream.write(encode_json.encode()+b"\n")
          rec=yield self.stream.read_until(b'\n')
          print ('recive from the server',rec)
          content = json.loads(rec) 
          nodelist = content["reg_node_list"] if "reg_node_list" in content else None
          if nodelist:
            for nodekey in nodelist.keys():
              if nodekey in self._node_list:
                continue
              m={ "host": nodelist[nodekey]["host"], "port": nodelist[nodekey]["port"] }
              client = SimpleTcpclient(p_mq=self._main_queue, p_server_map=m)
              client.start()
              self._node_list[nodekey] = nodelist[nodekey]
              print ("Add node", m)
          
        except tornado.iostream.StreamClosedError:
          print ("JobSync update met error")
        finally:
          yield tornado.gen.sleep(Configure.configure().value("register.crawler.updator.interval", 30))

    @tornado.gen.coroutine
    def sync(self):
      while True:
        print ("Start read message from sync queue")  
        future = yield self._main_queue.get()
        data = yield future.result()
        try:
          print ("JobSync got message: ",data)   
        finally:
          self._main_queue.task_done()
    
    @tornado.gen.coroutine
    def test(self): 
       while True:
          yield tornado.gen.sleep(10)    
          print ("start put message to queue")
          yield self._main_queue.put({"test":"message"})
          print ("after put message")      
                 
    def run(self):
      #asyncio.set_event_loop(asyncio.new_event_loop())  
      #self.sync()  
      #print ("Start job sync...")  
      self.update()
      print ("Start nodelist updator...")
      #self.test()
      
#       self._serverclient = SimpleTcpclient(p_mq=self._main_queue, p_server_map=m)
#       self._serverclient.start()  
#       #asyncio.set_event_loop(asyncio.new_event_loop())
#       for idx in range(self._num) : 
#         m={"host":self._crawler["host"],"port":8088}
#         client = SimpleTcpclient(p_mq=self._main_queue, p_server_map=m)
#         client.start()
#         print (idx, "new crawler::"+self._crawler["host"]+":"+str(self._crawler["port"])+" listen starts...")  
      #tornado.ioloop.IOLoop.current().start()
       
class CrawlerPicker(object):
  
  def __init__(self, p_list=None):
    if p_list == None:
      self._item_array = {}
    else:  
      self._item_array = p_list
    
  def addItem(self, p_id, p_item):
    self._item_array[p_id]=p_item
    print (len(self._item_array))
    
  def removeItem(self, p_id):
    try:  
      return self._item_array.pop(p_id)
    except:
      return None
    
  def adjust(self, p_id):
    pass

  def hasItem(self, p_id):
    val = self._item_array[p_id] if p_id in self._item_array else None
    if val == None:
      return False
    else:
      return True 
  
  def getItem(self):
    if len(self._item_array) <= 0:
      return None
  
    #items = self._item_array[0:]
    sum = 0
    for item in self._item_array.values():
      sum = sum + item.getProp(p_prop="weight")
    randomidx = random.randint(1,sum)
    end=0
    for item in self._item_array.values():
      end = end+item.getProp(p_prop="weight") 
      if randomidx<=end:
        return item
    
    return None

  def getWorkerSize(self):
    print (len(self._item_array)   )
    return len(self._item_array)
                            
     