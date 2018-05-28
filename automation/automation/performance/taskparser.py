# -*- coding: utf-8 -*-
import json

class JSONParser(object):

  def __init__(self, p_content=None):
    self._content = p_content.replace("'", '"')
    self._sence_ary = None
    
  def parse(self):
    self._sence_ary = json.loads(self._content)
    for idx, sence in enumerate(self._sence_ary):
      addr = sence["href"]
      
      thesence = Sence(threadname="Sence", p_addr=addr, p_act_time=None, p_director=None, p_actor_queue=actor_ary)
      
  def getScenes(self):
    return self._sence_ary