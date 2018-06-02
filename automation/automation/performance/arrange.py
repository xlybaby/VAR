# -*- coding: utf-8 -*-
import threading
import time
 
class Scheduler(object):

  def __init__(self, p_scenarioid, p_scheduleobj, p_director):
    self._scenarioid = p_scenarioid
    self._director=p_director
    self._end = False
    
    self.init(p_scheduleobj)
    
  def init(self, p_scheduleobj):
    self._interval = p_scheduleobj["interval"]
    self._unit = p_scheduleobj["unit"]
  
  def start(self):
    if not self._end:
      self._director.action()
      timer = threading.Timer( self._interval, self.start)
      timer.start()  
      
  def end(self, p_end):
    self._end = p_end      
    