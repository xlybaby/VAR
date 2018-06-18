# -*- coding: utf-8 -*-

import datetime

from selenium import webdriver

from automationsys import Configure
from automation.performance.actor import Actor
from automation.scenario.selector import PageElementFinder

class Iterator(Actor):

  def __init__( self, p_scenario, p_parameters, p_sceneno, p_pageno, p_pageid=None ):
    self._scenario = p_scenario
    self._pageid = p_pageid
    self._item_id = 0
    self._kvmappings = None
    self._sceneno = p_sceneno
    self._pageno = p_pageno
    self.setProperties(p_parameters)

  def do(self, p_selector, p_pageid=None):
    if self._kvmappings == None :
      return
    kvcollection = []
    for idx, mapping in enumerate(self._kvmappings):
      item = {}  
      timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
      
      keypath = mapping["mapping"]["fieldsel"]    
      valpath = mapping["mapping"]["datasel"]
      keysel = keypath["selector"]
      valsel = valpath["selector"]
      
      sel_key=PageElementFinder.getCompInstance(p_selector=p_selector, p_element=keysel)
      sel_val=PageElementFinder.getCompInstance(p_selector=p_selector, p_element=valsel)
      print (sel_key)
      print (sel_val)
      key_valueattr = keypath["valueattr"] if "valueattr" in keypath else None
      val_valueattr = valpath["valueattr"] if "valueattr" in valpath else None
      if key_valueattr:
        keyvalue = sel_key.xpath("@"+key_valueattr).extract_first()
      else:
        keyvalue = sel_key.xpath("string()").extract_first()
      
      if val_valueattr:
        valvalue = sel_val.xpath("@"+val_valueattr).extract_first()
      else:
        valvalue = sel_val.xpath("string()").extract_first()
      
      item["key"] =  keyvalue
      item["value"] =  valvalue
      item["timestamp"] = timestamp
      kvcollection.append(item) 
    return kvcollection
  
  def setProperties(self, p_parameters):
    self._kvmappings = p_parameters["kv-mappings"]  if "kv-mappings" in p_parameters else None