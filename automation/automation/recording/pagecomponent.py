# -*- coding: utf-8 -*-
import os

from selenium import webdriver
from scrapy.selector import Selector 

from automationsys import get_phantomjs_webdriver
from automationsys import get_ouput_dir
from automationsys import get_application_root_dir

from automation.recording.container import ListComponentContainer
from automation.recording.item import ListComponentDisplayItem
from automation.recording.iterator import ListComponentIterator
from automation.recording.pagination import ListComponentPagination
from automation.recording.component import Component

class PageComponent(object):

  def __init__(self, p_configure_file=None, p_pid=None):
    self._configure_file =  p_configure_file
    self._pid = p_pid
    self._container_list = []
    self._pagination_comp = None
    self.init()

  def init(self):
    conf_file = open(get_application_root_dir()+"/data/template/"+self._configure_file)
    configures = "".join(conf_file.readlines())
    self.populate_page_components(p_configure=configures)
    self.populate_pagination(p_configure=configures)
    
  def collect(self, p_document):
    print ("PageComponent start collect......")
    self._container.set_selector(p_selector)
    list_content = self._container.list_collect(p_iterator=self._iterator, p_items=self._item)
    print ("PageComponent end collect......")
    return list_content
  
  def getTemplate(self):
    return self._configure_file

  def getContainers(self):
    return self._container_list
  
  def getPagination(self):
    return self._pagination_comp

  def populate_pagination(self,p_configure):
    sel = Selector(text=p_configure)
    pagination = sel.xpath("//pagination")
    #TODO
    if pagination:
      pclass = pagination.xpath("child::class/text()").extract_first()
      pid = pagination.xpath("child::id/text()").extract_first()
      pname = pagination.xpath("child::name/text()").extract_first()
      ptag = pagination.xpath("child::tag/text()").extract_first()
      pxpath = pagination.xpath("child::xpath/text()").extract_first()
      ptitle = pagination.xpath("child::title/text()").extract_first()
      pattrs = None
      if ptitle:
          pattrs = "title="+ptitle
          
      pcomponent = Component(p_xpath=pxpath, p_class=pclass, p_id=pid, p_tag=ptag, p_name=pname, p_attrs=pattrs)
      self._pagination_comp = ListComponentPagination(p_component=pcomponent)  
      
      pp = pagination.xpath(".//parent")
      if pp:
        ppclass = pp.xpath("child::class/text()").extract_first()
        ppid = pp.xpath("child::id/text()").extract_first()
        ppname = pp.xpath("child::name/text()").extract_first()
        pptag = pp.xpath("child::tag/text()").extract_first()
        ppxpath = pp.xpath("child::xpath/text()").extract_first()
        ppcomponent = Component(p_xpath=ppxpath, p_class=ppclass, p_id=ppid, p_tag=pptag, p_name=ppname)
        self._pagination_comp.setParent(p_parent=ppcomponent)
        
  def populate_page_components(self, p_configure):
    sel = Selector(text=p_configure)
    containers = sel.xpath("//container")
    
    for container in containers:
      con_class = container.xpath("child::class/text()").extract_first()
      con_id = container.xpath("child::id/text()").extract_first()
      con_name = container.xpath("child::name/text()").extract_first()
      con_tag = container.xpath("child::tag/text()").extract_first()
      con_xpath = container.xpath("child::xpath/text()").extract_first()

      ccomp = Component(p_xpath=con_xpath, p_class=con_class, p_id=con_id, p_tag=con_tag, p_name=con_name)
      oCon = ListComponentContainer(p_component=ccomp)
      iterators = container.xpath(".//iterator")
      for iterator in iterators:
        iter_class = iterator.xpath("child::class/text()").extract_first()
        iter_id = iterator.xpath("child::id/text()").extract_first()
        iter_name = iterator.xpath("child::name/text()").extract_first()
        iter_tag = iterator.xpath("child::tag/text()").extract_first()
        iter_xpath = iterator.xpath("child::xpath/text()").extract_first()

        icomp = Component(p_xpath=iter_xpath, p_class=iter_class, p_id=iter_id, p_tag=iter_tag, p_name=iter_name)
        oIter = ListComponentIterator(p_component=icomp)
        items = iterator.xpath(".//item")
        for item in items:
          item_class = item.xpath("child::class/text()").extract_first()
          item_id = item.xpath("child::id/text()").extract_first()
          item_name = item.xpath("child::name/text()").extract_first()
          item_tag = item.xpath("child::tag/text()").extract_first()
          item_xpath = item.xpath("child::xpath/text()").extract_first()

          index=item.xpath(".//index/text()").extract_first()
          label=item.xpath(".//label/text()").extract_first()
          labelattr=item.xpath(".//labelattr/text()").extract_first()
          valueattr=item.xpath(".//valueattr/text()").extract_first()
          linkextract=item.xpath(".//linkextract/text()").extract_first()
          islink=item.xpath(".//islink/text()").extract_first()
          nextpagelink=item.xpath(".//nextpagelink/text()").extract_first()
          ignore=item.xpath(".//ignore/text()").extract_first()
          nextpagetemp=item.xpath(".//nextpagetemp/text()").extract_first()
          
          itcomp = Component(p_xpath=item_xpath, p_class=item_class, p_id=item_id, p_tag=item_tag, p_name=item_name,p_index=index)
          oItem = ListComponentDisplayItem(p_component=itcomp, p_label=label, p_labelattr=labelattr, p_valueattr=valueattr, p_parent=self._pid, p_islink=islink, p_nextpagelink=nextpagelink,p_linkextract=linkextract, p_ignore=ignore, p_nextpagetemp=nextpagetemp)
          oIter.addItem(p_item=oItem)
        oCon.addIterator(p_iter=oIter)
      self._container_list.append(oCon)