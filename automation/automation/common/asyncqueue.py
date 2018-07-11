# -*- coding: utf-8 -*-

from tornado.queues import Queue

class ThreadSafeQueue(Queue):
    
  def __init__(self, size):
    Queue.__init__(self, maxsize=size)    

  def get(self, timeout=None):
    return Queue.get(self, timeout)