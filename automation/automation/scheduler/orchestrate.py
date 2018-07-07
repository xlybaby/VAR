# -*- coding: utf-8 -*-

import asyncio
import json,os,sys,time,random,threading,datetime,traceback
import queue
import concurrent.futures
from pytz import utc

import apscheduler.executors.pool
from apscheduler.schedulers.background import BackgroundScheduler

import tornado.ioloop
from tornado.tcpclient import TCPClient

from automation.common.logging import Logger
from automation.common.application import Configure
from automation.common.elasticsearch import ESHandler
from automation.common.network import SimpleTcpclient
from automation.common.constants import StatusCode

class ParellelSchedule(object):
    
  def trigger(self):
    print ("job running")
        
  def __init__(self, p_crawler_maps=None):
    self._scheduler = None
    #self._crawler_maps = None
    self._crawlerPicker = CrawlerPicker()
    self._inijoblock = threading.Lock()
    self._master_job_queue = queue.Queue(1000) 
#     if p_crawler_maps:
#       self._crawler_maps = p_crawler_maps  
#       self.initJobs()
  
#   def getCrawlerMaps(self):
#     return self._crawler_maps

  def initJobs(self):
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
          job = Job(p_name=jobkey, p_queue=self._master_job_queue, p_interval=jobitem["interval"], p_threads=jobitem["threadsNum"], p_batchnum=jobitem["batchnum"], p_indice=jobitem["indice"], p_type=jobitem["type"], p_crawler_picker=self._crawlerPicker)
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
                
  def start(self):
    if self._scheduler != None:
      self._scheduler.start()
        
  def shutdown(self):
    if self._scheduler != None:  
      self._scheduler.shutdown()
  
  def registerCrawler(self, p_crawler):
    print ("register crawler...")
    try:  
#       if self._crawler_maps == None:
#         self._crawler_maps = {}
      c = self.Sync(p_queue=self._master_job_queue, p_crawler=p_crawler)      
      self._crawlerPicker.addItem(p_item = c)
      c.start()
       
    except:
      traceback.print_exc()
      return False
   
    if self._scheduler == None:
        self.initJobs()
        
    return True

  def callback(self, p_message=None):
    res = self.registerCrawler(p_crawler=p_message)   
    if res:
      status = StatusCode.OK
    else :
      status = StatusCode.ERROR  
    ret = {"status": status, "message": "Register done"}
    return json.dumps(ret)

  class Sync(threading.Thread):
    
    def __init__(self, p_queue, p_crawler, p_clientnum=1):
      threading.Thread.__init__(self)
      self._main_queue= p_queue
      self._crawler = json.loads(p_crawler)
      self._crawler["weight"] = 50
      self._crawler["last_communication_time"] = datetime.datetime.now()
      self._num = p_clientnum
      
    def setProp(self, p_prop, p_val):
      self._crawler[p_prop] = p_val 
    
    def getProp(self, p_prop):
      return self._crawler[p_prop]
       
    def run(self):
      asyncio.set_event_loop(asyncio.new_event_loop())
      for idx in range(self._num) : 
        m={"host":self._crawler["host"],"port":self._crawler["port"]}
        client = SimpleTcpclient(p_mq=self._main_queue, p_server_map=m)
        client.start()
        print (idx, "new crawler listen starts...")  
       
class CrawlerPicker(object):
  
  def __init__(self):
    self._item_array = []
    
  def addItem(self, p_item):
    self._item_array.append(p_item)
  
  def removeItem(self, p_item):
    self._item_array.remove(p_item)
      
  def adjuct(self, p_item):
    pass

  def getItem(self):
    if len(self._item_array) <= 0:
      return None
  
    items = self._item_array[0:]
    sum = 0
    for item in items:
      sum = sum + item.getProp(p_prop="weight")
    randomidx = random.randint(1,sum)
    end=0
    for item in items:
      end = end+item.getProp(p_prop="weight") 
      if randomidx<=end:
        return item
                      
class Job(object):

  def __init__(self, p_name, p_queue, p_interval, p_threads, p_batchnum, p_indice, p_type, p_crawler_picker):
    self._name=p_name
    self._main_job_queue=p_queue
    self._interval=p_interval
    
    self._threadnum=p_threads
    self._batchnum=p_batchnum
    
    self._indice = p_indice 
    self._type = p_type
    self._crawler_picker = p_crawler_picker
    
    self._job_fetch_pool = concurrent.futures.ThreadPoolExecutor(max_workers=self._threadnum)
    self._last_exec_time=None
    self._last_exec_duration=None
          
  def __call__(self):
    print ("job %s running...", self._name)  
    self._last_exec_time = datetime.datetime.now()
    futures = []  
    for i in range(self._threadnum):
      future = self._job_fetch_pool.submit(self.sync, self._name, i, self._threadnum, self._batchnum, self._indice, self._type, self._crawler_picker)
      futures.append(future)
      
    for fu in futures:
      res = fu.result()
      
    self._last_exec_duration = (datetime.datetime.now()-self._last_exec_time).seconds 
  
  def handle(self, data):
    pass
    
  def sync(self, p_name, p_tindex, p_threadnum, p_batchnum, p_indice, p_type, p_crawler_picker):
    size = p_batchnum  
    loop=0
    node = p_crawler_picker.getItem()
    if node == None:
      raise Exception("") ;
  
    while True:
      start = p_threadnum * size * loop
      ifrom = p_tindex * size + start
      loop = loop + 1
      data = ESHandler.ESClient.precise_search(p_indice=p_indice, p_type=p_type, p_qry_map={"groupName": p_name}, p_size=size, p_from=ifrom) 
      if data == None:
        break;
      for rec in data:
        scenario = rec["scenario"]
        try:
          data = {"event": "work", "scenario": scenario}  
          self._main_job_queue.put(scenario, block=False)    
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