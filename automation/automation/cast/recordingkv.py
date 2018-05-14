# -*- coding: utf-8 -*-

import os
import re

from selenium import webdriver
from scrapy.selector import Selector 

from automationsys import get_application_root_dir
from automationsys import get_phantomjs_webdriver
from automationsys import get_ouput_dir
from automation.performance.actor import Actor
from automation.cast.assistant import Locator
from automation.recording.pagecomponent import PageComponent
from automation.cast.persistent import Storage
from automation.performance.util import Util

class PageKVCrawl(Actor):

  def __init__(self, p_selector,p_type, p_id, p_class, p_xpath, p_name, p_tag, p_parameters,p_data_model=None):
    Actor.__init__(self, p_selector,p_type, p_id, p_class, p_xpath, p_name, p_tag)
    self._selector=p_selector
    self._act_time = None
    self._configure_file =  None
    self._pageComponents = None
    self._pid = None
    self._datafile = None
    self._tid=None
    
    self.setProperties(p_parameters)
    self.init()

  def init(self):
    self._pageComponents = PageComponent( p_configure_file=self._configure_file, p_pid=self._pid )

  def do(self, p_location=None):
    #self._pageComponents.collect(p_document=get_phantomjs_webdriver().page_source)
    writebuffer=[]
    containers = self._pageComponents.getContainers()
    selector = Selector(text=get_phantomjs_webdriver().page_source)
    for conidx, con in enumerate(containers):
      iters = con.getIterators()
      sel_cons = con.getInstance(p_selector = selector)
      con_xpath = con.getxpath()
      for iteridx, iterator in enumerate(iters):
        items=iterator.getItems()
        sel_iters = iterator.getInstance(p_selector = sel_cons)
        iter_xpath = iterator.getxpath()
        for itidx, item in enumerate(items):
          sel_items = item.getInstance(p_selector = sel_iters)
          item_xpath = item.getxpath()
          
          filename = self._datafile + ".con" + str(conidx) +"_iter" + str(iteridx) +"_item" + str(itidx)
          collected = item.collect(p_items=sel_items, p_tid=self._tid)
          Storage.write_map_result(p_dir = self._pid, p_file_name=filename, p_contents = collected)
          #print (sel_items)
    pagination = self._pageComponents.getPagination()
    if pagination:
      print ("generate next page task")
      pagcomp = pagination.getInstance(p_selector=selector)
      if pagcomp:
        print (pagcomp)      
        nxtlocation = pagcomp.xpath("@href").extract_first()
        if nxtlocation.rfind("/") >=0:
          uri = nxtlocation[nxtlocation.rfind("/")+1:]
        else:
          uri = nxtlocation
        taskfile = open(get_application_root_dir()+"/data/task/task_"+self._tid+"_"+uri+".xml", "ab")
        content = """
                        <crawl>
                            <task>
                                <pid>%s</pid>
                                <uri>%s</uri>
                                <template>%s</template>
                                <id>%s</id>
                            </task>
                        </crawl>
                        """ % (self._pid, Util.getabsurl(p_location, nxtlocation), self._pageComponents.getTemplate(), self._tid)
        taskfile.write(bytes(content, encoding = "utf8"))                
        taskfile.close()
#     for conidx, con in enumerate(containers):
#       print(con)
#       sel_con = con.getInstance(p_selector=selector)
#       #print (sel_con)
#       iters = con.getIterators()
#       for iteridx, iterator in enumerate(iters):
#         sel_iter = iterator.getInstance(p_selector=sel_con)
#         for idx, iter in enumerate(sel_iter): 
#           #print (iterator.getItems())
#           for itemidx, item in enumerate(iterator.getItems()):
#             #print( item.getindex() )  
#             selitems =  item.getInstance(p_selector=iter)
#             if item.getindex():
#               tmp_items=[]
#               tmp_items.append(selitems[int(item.getindex())-1])
#               collected = item.collect(p_items=tmp_items)
#             else:
#               collected = item.collect(p_items=selitems)  
#             Storage.write_map_result(p_dir = self._pid, p_file_name=self._datafile, p_contents = collected)
#             #print(selitems[int(item.getindex())-1])
#           #print (iter)
#         #print (sel_iter)
        
#         items = iterator.getItems()
#         for itemidx, item in enumerate(items):
#           sel_item = item.getInstance(p_selector=sel_iter)
          #index = item.getindex()
#           if index:
#             tmp_items=[]
#             tmp_items.append(sel_item[int(index)])
#             collected = item.collect(p_items=tmp_items)
#           else:
#           collected = item.collect(p_items=sel_item)
#           #print (collected)
#           Storage.write_map_result(p_dir = self._pid, p_contents = collected)

  def duration(self):
    return self._act_time

  def getProperty(self, p_name):  
    pass

  def setProperties(self, p_parameters):  
    duration = p_parameters["duration"] if "duration" in p_parameters else None
    configure = p_parameters["configure"] if "configure" in p_parameters else None
    datafile = p_parameters["datafile"] if "datafile" in p_parameters else None
    taskid = p_parameters["taskid"] if "taskid" in p_parameters else None
    pid = p_parameters["pid"] if "pid" in p_parameters else None
    
    if duration:
      self._act_time = int(duration)
    if configure:
      self._configure_file = configure
    if pid:
      self._pid = pid
    else:
      self._pid = ""
    if datafile:
      self._datafile = datafile
    if taskid:
      self._tid = taskid
    else:
      self._tid =  ""
         
  def getData():
    pass