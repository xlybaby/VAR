# -*- coding: utf-8 -*-
import os
import urllib 

from automationsys import Configure
from automation.performance.actor import Actor

class FileSave(Actor):

  def __init__(self, p_selector,p_type, p_id, p_class, p_xpath, p_name, p_tag, p_parameters,p_data_model=None):
    Actor.__init__(self, p_selector,p_type, p_id, p_class, p_xpath, p_name, p_tag)
    self._selector=p_selector
    self._act_time = None
    self._url_property = None
    self.setProperties(p_parameters)
    
  def download_file(self):
    elements = self.getComponent()
    file_path = Configure.get_ouput_dir()+"/download"
    if not os.path.exists(file_path):
      os.mkdir(file_path)
    print (elements)
    for elmt in elements:
      if self._url_property:
        url = elmt.xpath("@"+self._url_property).extract_first()
      else:
        url = elmt.xpath("text()").extract_first()

      file_name = url.split("/")[-1]
      print ("Download file to path: " + file_path+"/"+file_name)
      urllib.urlretrieve(url, file_path+"/"+file_name)

  def do(self, p_location=None):
    self.download_file()

  def duration(self):
    return self._act_time

  def getProperty(self, p_name):  
    pass

  def setProperties(self, p_parameters):  
    duration = p_parameters["duration"] if p_parameters.has_key("duration") else None
    src_prop = p_parameters["src_prop"] if p_parameters.has_key("src_prop") else None
    if duration:
      self._act_time = int(duration)
    if src_prop:
      self._url_property = src_prop

  def getData(self):
    pass