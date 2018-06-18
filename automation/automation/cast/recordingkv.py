# -*- coding: utf-8 -*-

import os
import re

from selenium import webdriver
from scrapy.selector import Selector 

from automationsys import Configure
from automation.performance.actor import Actor
from automation.cast.assistant import Locator
from automation.recording.pagecomponent import PageComponent
from automation.cast.persistent import Storage
from automation.performance.util import Util
from automation.cast.recording import PageCrawl

class PageKVCrawl(Actor):

  def __init__(self, p_scenario, p_parameters, p_sceneno, p_pageno, p_pageid=None):
    #Actor.__init__(self, p_selector,p_type, p_id, p_class, p_xpath, p_name, p_tag)
    self._scenario = p_scenario
    self._pageid = p_pageid
    self.setProperties(p_parameters)
    self._item_id = 0
    
    self._sceneno = p_sceneno
    self._pageno = p_pageno

  def do(self, p_selector=None, p_pageid=None):
    data = {}  
    data["keylabel"] = self._key_label
    if self._key_components:
      crawler = PageCrawl(p_scenario=self._scenario, p_parameters=None, p_sceneno=0, p_pageno=0, p_pageid=p_pageid)
      kitem_collect = crawler.crawlcon(p_containers=self._key_components, p_selector=p_selector)   
      print (kitem_collect)
      data["keydata"] = kitem_collect
    else:
      data["keyvalue"] = self._key_value
          
    if self._value_ary:
      data["values"] = {}  
      for idx, value in enumerate(self._value_ary) :
        label = value["label"]
        #print (label)
        containers = value["components"]
        crawler = PageCrawl(p_scenario=self._scenario, p_parameters=None, p_sceneno=0, p_pageno=0, p_pageid=p_pageid)
        item_collect = crawler.crawlcon(p_containers=containers, p_selector=p_selector)   
        #print (item_collect)
        data["values"][label] = item_collect
        
    return data
        
  def duration(self):
    return self._act_time

  def getProperty(self, p_name):  
    pass

  #   kvv-mapping
#        key
#          label
#          value
#          components[optional]
#        values
#          value1
#            label
#            components
#          value2
#            label
#            components
#            ...
#          valuen
#            label
#            components
           
  def setProperties(self, p_parameters):  
    pageComponent =   p_parameters["pageComponent"] if "pageComponent" in p_parameters else None
    if pageComponent: 
      kvvmapping = pageComponent["kvv-mapping"] if "kvv-mapping" in pageComponent else None
      if kvvmapping:
        keyobj = kvvmapping["key"] if "key" in kvvmapping else None
        
        self._key_label = keyobj["label"] if "label" in keyobj else None
        self._key_value = keyobj["value"] if "value" in keyobj else None
        self._key_components = keyobj["components"] if "components" in keyobj else None
        
        values = kvvmapping["values"] if "values" in kvvmapping else None  
        
        self._value_ary = []
        for value in values.values():
          self._value_ary.append(value)        
          
        