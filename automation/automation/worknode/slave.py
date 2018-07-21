# -*- coding: utf-8 -*-

import datetime, json, queue, time, uuid, traceback
from multiprocessing import Process
from multiprocessing import Manager

from automation.common.logging import Logger
from automation.common.application import Configure
from automation.common.constants import StatusCode

class Leader(object):

  def __init__(self, p_addr, p_node_name, p_monitor):
    self._node_id = p_node_name
    self._host = p_addr
    self._port = Configure.configure().value("server.nodeServer.port")
    
    self._max_working_proc_num = Configure.configure().value("worknode.maxWorkerNum")
    self._work_queue = Manager().Queue( Configure.configure().value("worknode.mainWorkQueueSize") )#queue.Queue(Configure.configure().value("worknode.mainWorkQueueSize"))
    self._monitor = p_monitor  
    
    #self._processing_sid_ary = []  
    self._events = {
      "work": self.accept
    }
    
    for i in range(self._max_working_proc_num):
      mate = Mate(p_leader=self, p_queue= self._work_queue)
#       mate.daemon = True
      mate.start()
      self._monitor.newProc(p_proc=mate)
    
  def getId(self):
    return self._node_id

  def getHost(self):
    return self._host

  def getPort(self):
    return self._port
  
  def setMonitor(self, p_monitor):
    self._monitor = p_monitor
    
  def accept(self, p_job_context):
    utc_time = datetime.datetime.utcfromtimestamp(time.time())
    accepttime = utc_time.strftime( '%Y-%m-%dT%H:%M:%S.%fZ' )
    p_job_context["accepttime"] = accepttime
    try:
      self._work_queue.put(p_job_context, block=False)
      return {"status": StatusCode.OK, "message": "Task accepted!"} 
 
    except queue.Full:
      return {"status": StatusCode.ERROR, "message": "No more available work node"} 
                
  def callback(self, p_message):
    body = json.loads(p_message)  
    event = body["event"] if "event" in body else None
    if event == None:
      return json.dumps({"status": StatusCode.ERROR, "message": "Unknown event type"})    
    
    res = self._events[event](body)
    return json.dumps(res)

class Mate(Process):

  def __init__(self, p_leader, p_queue):
    Process.__init__(self)
    self._leader = p_leader
    self._task_queue = p_queue
  
  def execute(self, p_job, p_exectime):
    scenario = p_job["scenario"]
    sid = scenario["scenarioId"]
    outputdir = Configure.configure().value("application.outputdir")
    
    rootdir = Configure.configure().value("application.rootdir")
    workdir = rootdir+"/"+"s"+"_"+ sid+"_"+p_exectime
    tmpdir = rootdir+"/"+"s"+"_"+ sid+"_"+p_exectime+"/tmp"
    print ("task dir: %s, %s"%(workdir, tmpdir))

  def run(self):
      sid=None  
      while True:
        try:
          print ("work node process[%s] waiting for scenario..."%(self.pid) )
          job_context = self._task_queue.get(block=True);
          print ("work node process[%s] got message: ", job_context)
          job = job_context["job"]
          
          utc_time = datetime.datetime.utcfromtimestamp(time.time())
          exectime = utc_time.strftime( '%Y-%m-%dT%H:%M:%S.%fZ' )
          Logger.getLogger().info("work node process[%s] got work, schedule time=>%s, accept time =>%s, execute time => %s"%(self.pid, job_context["scheduletime"], job_context["accepttime"], exectime))
          
          self.execute(p_job=job, p_exectime=exectime)
        except:
          traceback.print_exc()