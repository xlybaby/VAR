# -*- coding: utf-8 -*-

import os
import datetime
import threading
import time

from scrapy.selector import Selector 

from automation.scenario.entity import Scenario
from automation.cast.recording import PageCrawl
from automation.performance.util import Util
from automationsys import Configure

class CorpusCollect(Scenario):
    
  def __init__(self,p_scenario):
    Scenario.__init__(self, p_scenario=p_scenario)
    self._starttime = None
    self._driver = Configure.get_http_lowlevel_webdriver()
    
  def generateCrawler(self):
    threadnum = self.getThreadnum()
    duration = self.getDuration()
    lock = threading.Lock()
    for i in range(threadnum):
      crawler =  SubCrawler("CorpusCollect-crawler-"+str(i), p_scenario=self, p_lock=lock, p_duration=duration)     
      crawler.start()
      
  def collect(self, p_scene, p_page, p_sceneno, p_pageno):
    startaddr = p_scene["href"]
    print ("get page: "+startaddr)
    #print (startpage)
    pagebody = self._driver.get(startaddr)
    selector = Selector(text=pagebody)

    actors = p_page["actors"]
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
        self.goNext( p_location=startaddr, p_pagination = pagination, p_selector=selector )
              
  def performSpecified(self, p_sceneno, p_pageno):
    try:  
      scenes = self.getScenes()  
      self.collect(p_scene=scenes[p_sceneno], p_page=scenes[p_sceneno]["pages"][p_pageno], p_sceneno=p_sceneno, p_pageno=p_pageno)
    finally:  
      self._driver.close()  
      print ("Performance done!")  
               
  def perform(self, p_pageno=0):
    print ("CorpusCollect starts perfomance!")
    file_path=Configure.get_ouput_dir() + "/extract"  
    if not os.path.exists(file_path):
      os.mkdir(file_path)
    self._starttime = datetime.datetime.now()
    
    try:
      #self.generateCrawler()  
      scenes = self.getScenes()
      #print (scenes)
      if scenes:
        for idx, scene in enumerate(scenes):
          startpage = scene["pages"][p_pageno]
          self.collect(p_scene=scene, p_page=startpage, p_sceneno=idx, p_pageno=p_pageno)
    #except Exception as err:
      #print (err)  
    finally:  
      self._driver.close()
      print ("Performance done!")      
 
  def goNext( self, p_location,p_pagination,p_selector ):
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
        print (selpagination)      
        nxtlocation = selpagination.xpath("@href").extract_first()
        print ( "next location: " + Util.getabsurl(p_location=p_location, p_uri=nxtlocation) )
#         if nxtlocation.rfind("/") >=0:
#           uri = nxtlocation[nxtlocation.rfind("/")+1:]
#         else:
#           uri = nxtlocation
#         taskfile = open(Configure.get_application_root_dir()+"/task_"+self._tid+"_"+uri+".xml", "ab")
#         content = """
#                         <crawl>
#                             <task>
#                                 <pid>%s</pid>
#                                 <uri>%s</uri>
#                                 <template>%s</template>
#                                 <id>%s</id>
#                             </task>
#                         </crawl>
#                         """ % (self._pid, Util.getabsurl(p_location, nxtlocation), self._pageComponents.getTemplate(), self._tid)
#         taskfile.write(bytes(content, encoding = "utf8"))                
#         taskfile.close()    

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
      path = Configure.get_ouput_dir() + "/extract"   
      files= os.listdir(path)  
      if files:
        if self._rlock.acquire(blocking=False) :
          try:
            file = files[0]
            print (file)  
          finally:
            self._rlock.release()     
                             
      time.sleep(2)
      interval = datetime.datetime.now() - starttime
      lasts = interval.seconds
      print ("SubCrawler has been working for " + str(lasts) + " seconds.")
    print (self._tname + " is stop...")  
              