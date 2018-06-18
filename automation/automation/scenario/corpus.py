# -*- coding: utf-8 -*-

import os
import datetime
import json
import random
import threading
import time

from scrapy.selector import Selector 

from automation.scenario.entity import Scenario
from automation.cast.recording import PageCrawl
from automation.performance.util import Util
from automation.scenario.selector import PageElementFinder
from automationsys import Configure

class CorpusCollect(Scenario):
    
  def __init__(self,p_scenario):
    Scenario.__init__(self, p_scenario=p_scenario)
    self._starttime = None
    if self.getAutomation() :
      print ("this scene need automation driver!")
      self._driver = Configure.get_chrome_webdriver()
    else:
      self._driver = Configure.get_http_lowlevel_webdriver()
  
  def getCrawler(self):
    threadnum = self.getThreadnum()
    return random.randint(1, threadnum)    
 
  def generateCrawler(self):
    threadnum = self.getThreadnum()
    duration = self.getDuration()
    lock = threading.Lock()
    for i in range(threadnum):
      cname = "corpuscollect-crawler"+str(i+1)
       #create user extract index
      response = Configure.get_es_client().request( "GET", 
                                                           "http://test-mhis-service.pingan.com.cn/elasticsearch/u"+str(self.getUser()["userId"])+"_"+cname+"_extract/process_task/_mapping",
                                                           body=None,
                                                           headers={"Content-Type":"application/json"})
      
      if not (response.status == 200) :
        data = {  "settings": {
                              "index":{
                                  "number_of_shards": 3,
                                  "number_of_replicas":1
                               }
                   },
                   "mappings": {
                       "process_task": {
                           "properties": {
                                 "scenarioId": {
                                       "type":"keyword"
                                     },
                                  "href": {
                                       "type":"text"
                                     },
                                  "sceneno": {
                                       "type":"integer"
                                     },
                                  "gageno": {
                                       "type":"integer"
                                     },
                                  "configuration": {
                                      "type":"object"
                                      }
                               }
                        }
                   }
                }  
        encoded_data = json.dumps(data).encode('utf-8')
        response = Configure.get_es_client().request( "PUT", 
                                                           "http://test-mhis-service.pingan.com.cn/elasticsearch/u"+str(self.getUser()["userId"])+"_"+cname+"_extract",
                                                           body=encoded_data,
                                                           headers={"Content-Type":"application/json"})
        if not (response.status == 200) :
          print ("User extract task indice did not create.")
        print (response.data.decode('utf-8'))  
      crawler =  SubCrawler(cname, p_scenario=self, p_lock=lock, p_duration=duration)     
      crawler.start()
      
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
      elif acttype == 10: #Recordingkv
        recorder = PageKVCrawl()     
      else:
        raise Exception("Unsupported actor type")    
      recorder.do(p_selector=selector)
            
      pagination = p_page["pagination"] if "pagination" in p_page else None
      if pagination:
        self.goNext( p_location=p_href, p_pagination = pagination, p_selector=selector,p_sceneno=p_sceneno, p_pageno=p_pageno )
              
  def performSpecified(self, p_sceneno, p_pageno, p_href):
    try:  
      scenes = self.getScenes()  
      print (scenes[p_sceneno])
      print (scenes[p_sceneno]["pages"][p_pageno])
      self.collect(p_href=p_href, p_page=scenes[p_sceneno]["pages"][p_pageno], p_sceneno=p_sceneno, p_pageno=p_pageno)
    finally:  
      self._driver.close()  
      print ("Performance done!")  
               
  def perform(self, p_pageno=0):
    print ("CorpusCollect starts perfomance!")
    self._starttime = datetime.datetime.now()
    print (self.getUser()["userId"])
    try:
      self.generateCrawler()  
#       scenes = self.getScenes()
#       if scenes:
#         for idx, scene in enumerate(scenes):
#           startaddr = scene["href"]         
#           startpage = scene["pages"][p_pageno]
#           self.collect(p_href=startaddr, p_page=startpage, p_sceneno=idx, p_pageno=p_pageno)
    finally:  
      self._driver.quit()
      print ("Performance done!")      
 
  def goNext( self, p_location, p_pagination, p_selector, p_sceneno, p_pageno):
    if p_pagination:
      maxpageno = p_pagination["maxpageno"] if "maxpageno" in p_pagination else 10  
      paginationsel = p_pagination["selector"]
      if "parent" in p_pagination:
        parentsel = p_pagination["parent"]
        selp = PageElementFinder.getCompInstance(p_selector=p_selector, p_element=parentsel)
        selpagination = PageElementFinder.getCompInstance(p_selector=selp, p_element=paginationsel, p_relative=True)

      else:      
        selpagination = PageElementFinder.getCompInstance(p_selector=p_selector, p_element=paginationsel)
      
      print ("generate next page task")
      if selpagination:
        nxtlocation = selpagination.xpath("@href").extract_first()
        abslocation = Util.getabsurl(p_location=p_location, p_uri=nxtlocation)
        print ( "next location: " + abslocation )
        Util.writeextracttask(p_indice="u"+str(self.getUser()["userId"])+"_"+"corpuscollect-crawler"+str(self.getCrawler())+"_extract", p_type="process_task", p_scenarioid=self.getId(), p_sceneno=p_sceneno, p_pageno=p_pageno, p_uri=abslocation)

class  SubCrawler(threading.Thread):
    
  def __init__(self, threadname, p_scenario, p_lock, p_duration):
    threading.Thread.__init__(self, name=threadname)
    self._scenario = p_scenario
    self._rlock = p_lock
    self._duration = p_duration
    self._tname = threadname
    
  def run(self):  
    print (self._tname + " is running with " + str(self._duration) + " seconds.")  
    starttime = datetime.datetime.now()
    lasts = 0
    while lasts < self._duration :  
      if self._rlock.acquire(blocking=False) :
        try:
          sid, scenario = Util.getoneextracttask(p_indice="u"+str(self._scenario.getUser()["userId"])+"_"+self._tname+"_extract", p_type="process_task")    
          if sid:
            print (self._tname+" got one scenario: " + sid)
            print ( scenario )
            self._scenario.performSpecified( p_sceneno=scenario["sceneno"], p_pageno=scenario["pageno"], p_href=scenario["href"] )
            Util.deletedoc(p_indice="u"+str(self._scenario.getUser()["userId"])+"_"+self._tname+"_extract", p_type="process_task", p_id=sid)
            #time.sleep(2)
        finally:
          self._rlock.release()     
      else:
        print (self._tname + " not get lock")       
                        
      time.sleep(2)
      interval = datetime.datetime.now() - starttime
      lasts = interval.seconds
      print (self._tname + " has been working for " + str(lasts) + " seconds.")
    print (self._tname + " is stop...")  
              