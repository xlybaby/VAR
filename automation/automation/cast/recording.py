# -*- coding: utf-8 -*-

import os
import re

from scrapy.selector import Selector 
from automationsys import Configure
from automation.performance.actor import Actor
from automation.cast.assistant import Locator
from automation.recording.pagecomponent import PageComponent
from automation.cast.persistent import Storage
from automation.performance.util import Util
from automation.scenario.selector import PageElementFinder

class PageCrawl(Actor):

  def __init__(self, p_scenario, p_parameters, p_sceneno, p_pageno, p_pageid=None, p_location=None):
    #Actor.__init__(self, p_selector,p_type, p_id, p_class, p_xpath, p_name, p_tag)
    self._scenario = p_scenario
    self._pageid = p_pageid
    self.setProperties(p_parameters)
    self._item_id = 0
    
    self._sceneno = p_sceneno
    self._pageno = p_pageno
    self._location = p_location
    
  def do(self, p_selector=None, p_pageid=None):
    #self._pageComponents.collect(p_document=get_phantomjs_webdriver().page_source)
    writebuffer=[]
    data = {}
    components = self._pageComponents
    for idx, component in enumerate(components):
      item_collect = self.crawlcon(p_containers=component["containers"], p_selector=p_selector)   
      writebuffer.append(item_collect) 
      
    data["data"] = writebuffer
    return data
    
  def docollect(self, item, p_link=False, p_netpagelink=None, p_img=False, p_extract=False, p_label=None, p_labelattr=None, p_valueattr=None):
    item_map = {}
    self._item_id += 1
    item_map["item_id"] = "scenario["+self._scenario.getId() + "]_scene["+str(self._sceneno)+"]_page["+str(self._pageno)+"]_item[" + str(self._item_id) + "]"

    if p_label:
      key = p_label
    elif p_labelattr:
      key = item.xpath("@"+p_labelattr).extract_first()
    else:
      key = "value"

    if p_valueattr:
      value = item.xpath("@"+p_valueattr).extract_first()
    else:
      if p_link == 1:  
        value = item.xpath("@href").extract_first()
        value = Util.getabsurl(self._location, value)
      else:      
        value = item.xpath("string()").extract_first()
    
    try:  
      #print key+": "+value
      #item_map[key.encode("utf-8")] = value.encode("utf-8")
      #item_map[key] = value
      #item_map["label"] = key
      #item_map["value"] = value
      item_map[key] = value
        
      if p_link == 1 and p_extract  == 1:
        href= item.xpath("@href").extract_first()
        if p_netpagelink:
          item_map["next"] = p_netpagelink
        else:
          item_map["next"] = href
        #print ("need submit extract link")
        #print ("u"+str(self._scenario.getUser()["userId"])+"_indice_extract")
        Util.writeextracttask(p_indice="u"+str(self._scenario.getUser()["userId"])+"_"+"corpuscollect-crawler"+str(self._scenario.getCrawler())+"_extract", p_type="process_task",p_scenarioid=self._scenario.getId(), p_sceneno=self._sceneno, p_pageno=(self._pageno+1), p_uri= Util.getabsurl(item_map["next"]))
        #self.submit(item_map["next"], item_map["item_id"], self._nextpagetemp, p_tid)
      
      if p_img:
        pass      
      return item_map
    except Exception as e:
      print("Unexpected Error: {}".format(e))
  
  def crawlitem(self, p_sel_iters, p_items, p_selector):
    if not p_items:
      return
    item_collect = []
    
    for itemidx, item in enumerate(p_items) :
      #try: # if one item meets error, just skip  
        selector = item["selector"] if "selector" in item else None
        index = item["index"] if "index" in item else None  
        isimg =  item["img"] if "img" in item else None
        islink = item["link"] if "link" in item else None   
        needextract = item["extract"] if "extract" in item else None   
        label = item["label"] if "label" in item else None  
        labelattr = item["labelattr"] if "labelattr" in item else None  
        valueattr = item["valueattr"] if "valueattr" in item else None  
      
        if not selector :
          continue

        if index:
          sel_items=PageElementFinder.getCompInstance(p_selector=p_sel_iters, p_element=selector, p_relative=True)
          #print (sel_items[index])
          item_collect.append(self.docollect(item=sel_items[index], p_link=islink, p_img=isimg, p_extract=needextract, p_label=label, p_labelattr=labelattr, p_valueattr=valueattr))
        else:
          sel_items=PageElementFinder.getCompInstance(p_selector=p_sel_iters, p_element=selector, p_relative=True)
          #print (sel_items)
          for sidx, sel_item in enumerate(sel_items) :
            item_collect.append(self.docollect(item=sel_item, p_link=islink, p_img=isimg, p_extract=needextract, p_label=label, p_labelattr=labelattr, p_valueattr=valueattr)   )
      #except:
        #print ("Item collect met error, skipped!")  
        
    return item_collect
    
  def crawliter(self, p_sel_cons, p_iterators, p_selector):  
    item_collect = []
    for iteridx, iter in enumerate(p_iterators) :
      #try: # if one iterator meets error, just skip  
            
        selector = iter["selector"]  if "selector" in iter else None
        items = iter["items"]  if "items" in iter else None  
        index = iter["index"] if "pageComponent" in iter else None   
      
        if not selector:
          continue 

        if index:
          iter_item_collect = []  
          sel_iters=PageElementFinder.getCompInstance(p_selector=p_sel_cons, p_element=selector, p_relative=True)
          iter_item_collect += self.crawlitem(p_sel_iters=sel_iters[index], p_items=items, p_selector=p_selector)
          item_collect.append( iter_item_collect )
        else:
          sel_iters=PageElementFinder.getCompInstance(p_selector=p_sel_cons, p_element=selector, p_relative=True)
          print (len(sel_iters))
          print (sel_iters)
          for sidx, sel_iter in enumerate(sel_iters) :
            iter_item_collect = []  
            iter_item_collect += self.crawlitem(p_sel_iters=sel_iter, p_items=items, p_selector=p_selector)
            item_collect.append( iter_item_collect )
            print (iter_item_collect)    
            
      #except:
        #print ("Iterator collect met error, skipped!")    
            
    return item_collect
    
  def crawlcon(self, p_containers, p_selector):
    item_collect = []
    for conidx, con in enumerate(p_containers):
      #try: # if one container meets error, just skip  
        selector = con["selector"] if "selector" in con else None
        iterators = con["iterators"] if "iterators" in con else None   
        index = con["index"] if "index" in con else None  
      
        if not selector:
          continue 
        sel_cons=PageElementFinder.getCompInstance(p_selector=p_selector, p_element=selector)
        print (sel_cons)
        if not iterators:
          continue
        
            
        if index :
          item_collect += self.crawliter(p_sel_cons=sel_cons[index], p_iterators=iterators, p_selector=p_selector)     
        else :
          for sidx, sel_con in enumerate(sel_cons) :  
            item_collect += self.crawliter(p_sel_cons=sel_con, p_iterators=iterators, p_selector=p_selector)     
      #except:
        #print ("Container collect met error, skipped!")    
    return item_collect
  
  def getContent(self, p_selector):
    pass
            
  def duration(self):
    return self._act_time

  def getProperty(self, p_name):  
    pass

  def setProperties(self, p_parameters):  
    if p_parameters:  
      self._pageComponents =   p_parameters["pageComponent"] if "pageComponent" in p_parameters else None
         
  def getData(self):
    pass