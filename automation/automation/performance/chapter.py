# -*- coding: utf-8 -*-

import threading
from time import sleep

class Page(object):

  def __init__(self, threadname, p_addr, p_act_time, p_director, p_actor_queue):
    threading.Thread.__init__(self, name=threadname)
    self._act_time = None
    if p_act_time:
      self._act_time = int(p_act_time)
    self._actor_queue = p_actor_queue

  def crawl(self):
    if self._act_time:
      sleep(self._act_time)

    for actor in self._actor_queue:
      print ("Actor perform: ")
      print (actor)  
      time = actor.duration()
      actor.do(p_location=self._addr)
      if time:
        print ("Actor perform last " + str(time) + " seconds...")
        sleep(time)
      #print "handler:"
      #print get_phantomjs_webdriver().window_handles
    #sleep(self._act_time)
