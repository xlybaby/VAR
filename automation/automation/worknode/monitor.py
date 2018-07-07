# -*- coding: utf-8 -*-

from automation.common.application import Configure

class MultiProcessJobWatcher(object):

  def __init__(self):
    self._max_working_time_per_worker = Configure.configure().value("worknode.maxWorkerNum")
    self._proc_pool = {}
    
  def newProc(self, p_proc):
    self._proc_pool[p_proc.pid] = {"proc":p_proc, "starttime": datetime.datetime.now()}
  
  def __call__(self):
    print ("MultiProcessJobWatcher running...")
    
  def monitorWorkingProc(self):
    procs=self._proc_pool.keys()
    if procs == None or len(procs)==0:
      return
    for pid in procs:
      pmap = procs[pid]
      p = pmap["proc"]
      starttime = pmap["starttime"]
      last = datetime.datetime.now() - starttime
      if last.seconds > self._max_working_time_per_worker:
        p.terminate()
      if not p.is_alive():
        pass

  def monitorWorkingEffect(self):
    procs = len(self._proc_pool)
