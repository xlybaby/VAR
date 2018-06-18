# -*- coding: utf-8 -*-

from scrapy.selector import Selector 

from automation.scenario.entity import Scenario
from automationsys import Configure

'''
动画大师！
'''
class AnimationMaster(Scenario):

  def __init__(self, p_scenario):
    Scenario.__init__(self, p_scenario=p_scenario)
    self._driver = Configure.get_chrome_webdriver()
    
  def perform(self, p_pageno=0):
    print ("Banner starts perfomance!")
    try:
      pass
    finally:  
      self._driver.close()
      print ("Performance done!")    