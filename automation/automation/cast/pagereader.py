# -*- coding: utf-8 -*-
import os

from scrapy.selector import Selector 
from automationsys import Configure
from automation.performance.actor import Actor

import urllib 

class Pagination(Actor):

  def __init__(self, p_type, p_id, p_class, p_xpath, p_name, p_tag, p_parameters):
    Actor.__init__(self, p_type, p_id, p_class, p_xpath, p_name, p_tag)
    self._act_time = None
    self._next_label = [u"下一页",u"next"]
    self._next = {}
    self._pre = {}
    self.setProperties(p_parameters)
    
  def do(self, p_location=None):
    pass

  def duration(self):
    return self._act_time

  def getProperty(self, p_name):  
    pass

  def setProperties(self, p_parameters):  
    duration = p_parameters["duration"]
    if duration:
      self._act_time = int(duration)
    self.findPagination()

  def findPagination(self):
  	driver = Configure.get_chrome_webdriver()
  	selector = Selector(text=driver.page_sources)
