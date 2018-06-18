# -*- coding: utf-8 -*-

import os
import time
import datetime

import numpy as np
from scrapy.selector import Selector 

from automation.cast.recordingkv import PageKVCrawl
from automation.scenario.entity import Scenario
from automation.cast.element import Iterator
from automation.cast.persistent import Storage
from automationsys import Configure

class Timeseries(Scenario):
    #Actor type: element (5)
    #find element
    #get element's attribute's value or text value
    #insert into es
    #Document format: (scenarioId, title, field1,field2...fieldn, value1,value2...valuen, max, min, timepoint)
    
    #timepoint format: 年-月-日 时:分:秒
    #                            时:分:秒  
    
    #Example 1. properties:
    #<kv-mappings>
#         <mapping>
#             <key>/html/body/div[5]/div[1]/div[1]/div[3]/table/thead/tr/th[1]</key>
#             <val>/html/body/div[5]/div[1]/div[1]/div[3]/table/tbody/tr/td[1]</val>
#         </mapping>
#         <mapping>
#             <key>/html/body/div[5]/div[1]/div[1]/div[3]/table/thead/tr/th[2]</key>
#             <val>/html/body/div[5]/div[1]/div[1]/div[3]/table/tbody/tr/td[2]</val>
#         </mapping>
#         <mapping>
#             <key>/html/body/div[5]/div[1]/div[1]/div[3]/table/thead/tr/th[3]</key>
#             <val>/html/body/div[5]/div[1]/div[1]/div[3]/table/tbody/tr/td[3]</val>
#         </mapping>
#         <mapping>
#             <key>/html/body/div[5]/div[1]/div[1]/div[3]/table/thead/tr/th[4]</key>
#             <val>/html/body/div[5]/div[1]/div[1]/div[3]/table/tbody/tr/td[4]</val>
#         </mapping>
#    </kv-mappings>

#    Example 2. properties:
#    <pageComponents>
#         <scene>
#           <field>
#                 <label></label>
#                 <components>
#                     pagelist
#                 </components>
#           </field>
#           <timepoint>
#                 <systime>
#                     true
#                 </systime>
#                 <components>
#                     pagelist
#                 </components>
#           </timepoint>
#           <value>
#                 <components>
#                     pagelist
#                 </components>
#           </value>
#           </scene>
#         </pageComponents>

  def __init__(self,p_scenario):
    Scenario.__init__(self, p_scenario=p_scenario)
    if self.getAutomation() :
      print ("this scene need automation driver!")
      self._driver = Configure.get_chrome_webdriver()
    else:
      self._driver = Configure.get_http_lowlevel_webdriver()

  def perform(self, p_pageno=0):
    print ("Timeseries starts perfomance!")
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
    self._driver.get(p_href)
    if p_delay :
      print ("after get page ,we need sleep for a while: " + str(p_delay))
      time.sleep(p_delay)
      
    selector = Selector(text=self._driver.page_source)
    ofile = open("/usr/local/var/source1.htm",'w', encoding="utf-8")
    ofile.write(self._driver.page_source)
    ofile.close()
    self._driver.save_screenshot("/usr/local/var/capture1.png")
    actors = p_page["actors"]
    for actidx, actor in enumerate(actors):
      acttype = actor["type"]
      properties = actor["properties"]
      if "indexname" in properties :
        indexname = properties["indexname"]   
      else :
        indexname = "indice"
        
      recorder = None
      if acttype == 5: #element
        recorder = Iterator(p_scenario=self, p_parameters=properties, p_sceneno=p_sceneno, p_pageno=p_pageno)    
      elif acttype == 10: #Recordingkv
        recorder = PageKVCrawl(p_scenario=self, p_parameters=properties, p_sceneno=p_sceneno, p_pageno=p_pageno)     
             
      else:
        raise Exception("Unsupported actor type")    
      data = recorder.do(p_selector=selector, p_pageid=self.getId()+"_page0")
      
      resultary = []
      prevalary = None
      iniprevalary = False
      
      keydata = data["keydata"] if "keydata" in data else None
      keylabel = data["keylabel"]
      if not keydata:
        keyvalue = data["keyvalue"] if "keyvalue" in data else "unknown key value"    
      else:
        for ikey in keydata:
          ikeyval = ikey["value"]
          kvpair = '"'+keylabel+'":"'+ikeyval+'"'
          valary.append(kvpair)
        npvalary = np.array(valary).reshape((len(valary),1))  
        if iniprevalary:
          prevalary = np.hstack((prevalary,npvalary))  
        else:
          prevalary = npvalary    
          iniprevalary = True
                
      values = data["values"]
      for valkey in values.keys():
        valcollect = values[valkey]
        valary = []
        for item in valcollect:
          itemval = item["value"]
          itemtype = properties["pageComponent"]["kvv-mapping"]["values"][valkey]["type"]
          if valkey == "timepoint":
            format = properties["timepoint"]["format"]
            if format == "yyyy-mm-dd HH:mi:ss" :
              itemval = itemval[0:10] +"T"+  itemval[11:]+".000Z"    
            elif format == "HH:mi:ss" :     
              itemval = datetime.datetime.now().strftime('%Y-%m-%dT') +  itemval +".000Z"
                  
          if itemtype == "number" or itemtype == "boolean" :
            kvpair = '"'+valkey+'":'+itemval  
          else:
            kvpair = '"'+valkey+'":"'+itemval+'"'
          valary.append(kvpair)
        npvalary = np.array(valary).reshape((len(valary),1))  
        if iniprevalary :
          prevalary = np.hstack((prevalary,npvalary))  
        else :
          prevalary = npvalary
          iniprevalary = True
      
      if not keydata:
        rows, cols = prevalary.shape
        print ("rows, cols, "+str(rows)+str(cols))
        keysary = []
        for ii in range(rows):
          keysary.append('"'+keylabel+'":"'+keyvalue+'"')     
        npkeysary = np.array(keysary).reshape((len(keysary),1))    
        prevalary = np.hstack((prevalary,npkeysary))  
        
      dir = Configure.get_ouput_dir() + "/" + self.getId()
      filename = self.getTypename()+datetime.datetime.now().strftime('%Y%m%d%H%M%S')+".json"   
      Storage.write_array_result(p_dir=dir, p_file_name=filename, p_contents=prevalary.tolist(), p_prefix="{", p_suffix="}", p_seperator=",")