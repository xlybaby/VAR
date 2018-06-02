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

  def __init__(self, p_scenario, p_parameters, p_sceneno, p_pageno, p_pageid=None):
    #Actor.__init__(self, p_selector,p_type, p_id, p_class, p_xpath, p_name, p_tag)
    self._scenario = p_scenario
    self._pageid = p_pageid
    self.setProperties(p_parameters)
    self._item_id = 0
    
    self._sceneno = p_sceneno
    self._pageno = p_pageno
    
  def do(self, p_selector=None, p_pageid=None):
    #self._pageComponents.collect(p_document=get_phantomjs_webdriver().page_source)
    writebuffer=[]
    components = self._pageComponents
    for idx, component in enumerate(components):
      self.crawlcon(p_containers=component["containers"], p_selector=p_selector)    
  
  def docollect(self, item, p_link=False, p_netpagelink=None, p_img=False, p_extract=False, p_label=None, p_labelattr=None, p_valueattr=None):
    item_map = {}
    self._item_id += 1
    item_map["item_id"] = self._pageid + "_item" + str(self._item_id)

    if p_label:
      key = p_label
    elif p_labelattr:
      key = item.xpath("@"+p_labelattr).extract_first()
    else:
      key = "value"

    if p_valueattr:
      value = item.xpath("@"+p_valueattr).extract_first()
    else:
      value = item.xpath("string()").extract_first()
    
    try:  
      #print key+": "+value
      #item_map[key.encode("utf-8")] = value.encode("utf-8")
      #item_map[key] = value
      item_map["label"] = key
      item_map["value"] = value
        
      href=""
      if p_link == 1:
        href= item.xpath("@href").extract_first()
        if p_netpagelink:
          item_map["next"] = p_netpagelink
        else:
          item_map["next"] = href
        if p_extract  == 1:
          print ("need submit extract link")
          taskfile = open(Configure.get_ouput_dir()+"/extract/"+Util.hash(p_content=item_map["next"]), "ab")
          taskfile.write(bytes(item_map["next"]+"\n"+self._scenario.getId()+"\n"+str(self._sceneno)+"\n"+str(self._pageno+1), encoding = "utf8"))                
          taskfile.close() 
          #self.submit(item_map["next"], item_map["item_id"], self._nextpagetemp, p_tid)
      
      return item_map
    except Exception as e:
      print("Unexpected Error: {}".format(e))
    
  def collect(self, p_sel_items, p_link=False, p_netpagelink=None, p_img=False, p_extract=False, p_label=None, p_labelattr=None, p_valueattr=None ):
    #print (p_sel_items)
    item_collect = []
    
    if None == p_sel_items:
      return item_collect
    
    if not hasattr(p_sel_items, '__iter__') :
      item_collect.append(self.docollect(p_sel_items, p_link=p_link, p_img=p_img, p_extract=p_extract, p_labelattr=p_labelattr, p_valueattr=p_valueattr))      
    else:
      for idx, item in enumerate(p_sel_items):
        item_collect.append(self.docollect(item, p_link=p_link, p_img=p_img, p_extract=p_extract, p_labelattr=p_labelattr, p_valueattr=p_valueattr))
    return item_collect    
  
  def crawlitem(self, p_sel_iters, p_items, p_selector):
    if not p_items:
      return
    item_collect = []
    
    for itemidx, item in enumerate(p_items) :
      selector = item["selector"] if "selector" in item else None
      index = item["index"] if "index" in item else None  
      isimg =  item["img"] if "img" in item else None
      islink = item["link"] if "link" in item else None   
      needextract = item["extract"] if "extract" in item else None   
      labelattr = item["labelattr"] if "labelattr" in item else None  
      valueattr = item["valueattr"] if "valueattr" in item else None  
      
      if not selector :
        continue
    
      if index:
        for idx, sel_iter in enumerate(p_sel_iters):
          #print (sel_iter)  
          sel_items=PageElementFinder.getCompInstance(p_selector=sel_iter, p_element=selector, p_relative=True)
          #print (sel_items[index])
          item_collect += self.collect(p_sel_items=sel_items[index-1], p_link=islink, p_img=isimg, p_extract=needextract, p_labelattr=labelattr, p_valueattr=valueattr)
      else:
        sel_items=PageElementFinder.getCompInstance(p_selector=p_sel_iters, p_element=selector, p_relative=True)
        item_collect = self.collect(p_sel_items=sel_items, p_link=islink, p_img=isimg, p_extract=needextract, p_labelattr=labelattr, p_valueattr=valueattr)   
    Storage.write_map_result(p_dir = Configure.get_ouput_dir(), p_file_name=self._pageid, p_contents = item_collect)
        
  def crawliter(self, p_sel_cons, p_iterators, p_selector):  
    for iteridx, iter in enumerate(p_iterators) :
      selector = iter["selector"]  if "selector" in iter else None
      items = iter["items"]  if "items" in iter else None  
      index = iter["index"] if "pageComponent" in iter else None   
      
      if not selector:
        continue 

      if index:
        for idx, sel_con in enumerate(p_sel_cons):
          sel_iters=PageElementFinder.getCompInstance(p_selector=sel_con, p_element=selector, p_relative=True)
          self.crawlitem(p_sel_iters=sel_iters[index], p_items=items, p_selector=p_selector)
      else:
        sel_iters=PageElementFinder.getCompInstance(p_selector=p_sel_cons, p_element=selector, p_relative=True)
        #print (sel_iters)
        self.crawlitem(p_sel_iters=sel_iters, p_items=items, p_selector=p_selector)
        
  def crawlcon(self, p_containers, p_selector):
    for conidx, con in enumerate(p_containers):
      selector = con["selector"] if "selector" in con else None
      iterators = con["iterators"] if "iterators" in con else None   
      index = con["index"] if "index" in con else None  
      
      if not selector:
        continue 
      sel_cons=PageElementFinder.getCompInstance(p_selector=p_selector, p_element=selector)
      #print (sel_cons)
      if not iterators:
        continue
        
      if index :
        ary = []
        ary.append(sel_cons[index])  
        self.crawliter(p_sel_cons=sel_cons[index], p_iterators=iterators, p_selector=p_selector)     
      else :
        self.crawliter(p_sel_cons=sel_cons, p_iterators=iterators, p_selector=p_selector)     
  
  def getContent(self, p_selector):
    pass
            
  def duration(self):
    return self._act_time

  def getProperty(self, p_name):  
    pass

  def setProperties(self, p_parameters):  
    self._pageComponents =   p_parameters["pageComponent"] if "pageComponent" in p_parameters else None
         
  def getData(self):
    pass