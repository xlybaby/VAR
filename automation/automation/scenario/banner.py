# -*- coding: utf-8 -*-

from scrapy.selector import Selector 

from automation.scenario.entity import Scenario
from automation.cast.recording import PageCrawl
from automation.cast.screen import PageCapture
from automation.performance.util import Util
from automation.scenario.selector import PageElementFinder
from automationsys import Configure

class Banner(Scenario):
    
  def __init__(self, p_scenario):
    Scenario.__init__(self, p_scenario=p_scenario)
    if self.getAutomation() :
      print ("this scene need automation driver!")
      self._driver = Configure.get_chrome_webdriver()
    else:
      self._driver = Configure.get_http_lowlevel_webdriver()
    
  def perform(self, p_pageno=0):
    print ("Banner starts perfomance!")
    try:
       scenes = self.getScenes()
       if scenes:
         for idx, scene in enumerate(scenes):
           startaddr = scene["href"]         
           startpage = scene["pages"][p_pageno]
           self.collect(p_href=startaddr, p_page=startpage, p_sceneno=idx, p_pageno=p_pageno)
    finally:  
      self._driver.quit()
      print ("Performance done!")      
      
  def collect(self, p_href, p_page, p_sceneno, p_pageno):
    #startaddr = p_scene["href"]
    print ("get page: "+p_href)
    #print (startpage)
    pagebody = self._driver.get(p_href)
    selector = Selector(text=pagebody)

    actors = p_page["actors"]
    print (actors)
    for actidx, actor in enumerate(actors):
      acttype = actor["type"]
      properties = actor["properties"]
      recorder = None
      if acttype == 2: #Recording
        recorder = PageCrawl(p_scenario=self, p_parameters=properties, p_sceneno=p_sceneno, p_pageno=p_pageno, p_pageid=p_page["pageId"])    
      elif acttype == 6: #Screen
        recorder = PageCapture()     
      else:
        raise Exception("Unsupported actor type")    
      recorder.do(p_selector=selector)
            
      pagination = p_page["pagination"] if "pagination" in p_page else None
      if pagination:
        self.goNext( p_location=p_href, p_pagination = pagination, p_selector=selector,p_sceneno=p_sceneno, p_pageno=p_pageno )
              