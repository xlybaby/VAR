# -*- coding: utf-8 -*-
import json

class JSONParser(object):

  def __init__(self, p_content=None):
    self._content = p_content
    self._sence_ary = []
    self.parse()
    
  def parse(self):
    for idx, sence in enumerate(self._content):
      addr = sence["href"]
      pages = sence["pages"]
        
      thesence = Sence(threadname="Sence", p_addr=addr, p_act_time=None, p_director=None, p_actor_queue=actor_ary)
      self._sence_ary.append(thesence)
      
  def getScenes(self):
    return self._sence_ary