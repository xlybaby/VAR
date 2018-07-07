# -*- coding: utf-8 -*-

import os,datetime,time

from scrapy.selector import Selector 

from automation.scenario.entity import Scenario
from automation.cast.recording import PageCrawl
from automation.cast.screen import PageCapture
from automation.cast.persistent import Storage
from automation.performance.util import Util
from automation.scenario.selector import PageElementFinder
from automationsys import Configure
# <properties>
#     <pageComponent></pageComponent>
#     <list>
#         <size></size>default:10
#     </list>
#     <filter>
#         <key-words></key-words>
#         <reg-exp></reg-exp>
#     </filter>
# </properties>

# {
#     list: [ {hashcode: '', title: '', extractlink: '', timestamp: ''},
#             {hashcode: '', title: '', extractlink: '', timestamp: ''} ]
# }
class RefreshBlock(Scenario):
    
  def __init__(self,p_scenario):
    Scenario.__init__(self, p_scenario=p_scenario)  
    if self.getAutomation() :
      print ("this scene need automation driver!")
      self._driver = Configure.get_chrome_webdriver()
    else:
      self._driver = Configure.get_http_lowlevel_webdriver()
  
  def perform(self, p_pageno=0):
    print ("RefreshBlock starts perfomance!")
    try:
      scenes = self.getScenes()
      if scenes:
        for idx, scene in enumerate(scenes):
          startaddr = scene["href"]         
          startpage = scene["pages"][p_pageno]
          delay = scene["delay"] if "delay" in scene else None
          self.collect(p_href=startaddr, p_page=startpage, p_sceneno=idx, p_pageno=p_pageno, p_delay=delay)
    finally:  
      self._driver.quit()
      print ("Performance done!")      
      
  def collect(self, p_href, p_page, p_sceneno, p_pageno, p_delay=None):
    #startaddr = p_scene["href"]
    print ("get page: "+p_href)
    #print (startpage)
    pagebody = self._driver.get(p_href)
    if p_delay :
      print ("after get page ,we need sleep for a while: " + str(p_delay))
      time.sleep(p_delay)
      
    selector = Selector(text=pagebody)
    actors = p_page["actors"]
    for actidx, actor in enumerate(actors):
      acttype = actor["type"]
      properties = actor["properties"]
      recorder = None
      if acttype == 2: #Recording
        recorder = PageCrawl(p_scenario=self, p_parameters=properties, p_sceneno=p_sceneno, p_pageno=p_pageno, p_location=p_href)    
    
      else:
        raise Exception("Unsupported actor type")    
      data = recorder.do(p_selector=selector)
      if data and "data" in data:
        dir = Configure.get_ouput_dir() + "/" + self.getId()
        filename = self.getTypename() + datetime.datetime.now().strftime('%Y%m%d%H%M%S') + ".json"     
        pageComponentsData = data["data"]
        for data in pageComponentsData :
          print (data)  
          Storage.write_map_result( p_dir = dir, p_file_name = filename, p_contents = data )

 