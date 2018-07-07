# -*- coding: utf-8 -*-

import datetime, queue, uuid
from multiprocessing import Process

from automation.common.logging import Logger
from automation.common.application import Configure
from automation.common.constants import StatusCode

class Leader(object):

  def __init__(self, p_node_name, p_monitor):
    self._max_working_proc_num = Configure.configure().value("worknode.maxWorkerNum")
    self._ini_working_proc_num = Configure.configure().value("worknode.iniWorkerNum")

    self._node_id = p_node_name#Configure.configure().value("worknode.name")
    self._host = Configure.configure().value("server.crawler.nodeServer.host")
    self._port = Configure.configure().value("server.crawler.nodeServer.port")
  
    self._worker_index_queue = queue.Queue(self._max_working_proc_num)
    self._worker_map = {}
    
    self._work_queue = queue.Queue(self._max_working_proc_num)
    self._monitor = p_monitor  
    
    self._processing_sid_ary = []  
    for i in range(self._ini_working_proc_num):
      mate = Mate(p_leader=self)
      self._worker_map[mate.getno()] = mate 
      self._worker_index_queue.put(mate.getno(), block=False)
#       mate.daemon = True
#       self._monitor.newProc(p_proc=mate)
#       mate.start()
          
  def getId(self):
    return self._node_id

  def getHost(self):
    return self._host

  def getPort(self):
    return self._port
  
  def setMonitor(self, p_monitor):
    self._monitor = p_monitor
    
  def accept(self, p_job_context):
    print ("accept scenario: ", p_job_context) 
    sid=p_job_context["scenarioId"]
    try:
      if self._processing_sid_ary.index(sid) >= 0 :
        return {"status": StatusCode.ERROR, "message": "Scenario is already in queue."}
    except:
      pass
    
    try:
      mate = self._worker_index_queue.get(block=False)
    except queue.Empty:
      workernum= len(self._worker_map)
      if workernum >= self._max_working_proc_num: 
        return {"status": StatusCode.ERROR, "message": "No more available work node"} 
      else:
        mate = Mate(p_leader=self)
        self._worker_map[mate.getno()] = mate 
        self._worker_index_queue.put(mate.getno(), block=False)
        
    mate.execute(p_message=p_job_context)
    return {"status": StatusCode.OK, "message": "Task accepted!"} 

#     if self._work_queue.put(p_job_context, block=False) == False:
#       return {"status": StatusCode.ERROR, "message": "Full in working queue."} 
# 
#     self._processing_sid_ary.append(sid) 
#     
#     sid = p_job_context["scenarioId"] 
#     mate = Mate(p_scenario=p_job_context)
#     if self._work_queue.put(1, block=False) == False:
#       return {"status": StatusCode.ERROR, "message": "No availabel worker in working queue."}  
#     
#     p = Process(target=mate)
#     p.daemon = True
#     self._monitor.newProc(p_proc=p)
#     p.start()
                
  def callback(self, p_message):
    return self.accept(p_job_context=p_message)

  def done(self, p_sid, p_no):
    try:
      self._worker_index_queue.put(p_no, block=False)
    except queue.Full:
      print ("worker queue is full, can't return mate.")
    finally:
      print ("job done, remove job sid: "+p_sid)
      self._processing_sid_ary.remove(p_sid)
        
class Mate(Process):

  def __init__(self, p_leader):
    Process.__init__(self)
    self._leader = p_leader
    
    self._no = str(uuid.uuid1().int)
    self._task_queue = queue.Queue(1)
    self._task_proc = self.Proc(p_task_queue=self._task_queue, p_callback=self.release)
  
  def getno(self):
    return self._no

  def release(self,p_sid):
    self._leader.done(p_sid=p_sid, p_no=self._no)
  
  def execute(self, p_message):
    self._task_queue.put(p_message, block=False) 
  
  class Proc(Process):
    def __init__(self, p_task_queue, p_callback):
      Process.__init__(self)  
      self._task_queue = p_task_queue
      self._callback = p_callback
           
    def run(self):
      sid=None  
      while true:
        try:
          print ("work node waiting for scenario...")
          scenario = self._task_queue.get(block=True);
          sid=scenario["scenarioId"] 
          print ("get scenario: ", scenario)
          print ("start execute...")
        except:
          pass
        finally:
          self._callback(sid)