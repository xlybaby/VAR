#-*-coding:utf-8-*-

import os
import time
import uuid

from selenium import webdriver

from automationsys import get_phantomjs_webdriver
from automationsys import get_ouput_dir
from automation.performance.actor import Actor

class PageCapture(Actor):

  def __init__(self, p_selector, p_type, p_id, p_class, p_xpath, p_name, p_tag, p_parameters,p_data_model=None):
    Actor.__init__(self, p_selector,p_type, p_id, p_class, p_xpath, p_name, p_tag)
    self._act_time = None
    self._file = None
    self._time_format = '%Y-%m-%d.%X'
    self.setProperties(p_parameters)

  def do(self):
    self.capture_whole(self._file)

  def duration(self):
    return self._act_time

  def capture_whole(self, p_file=None, p_url=None):
    #get_phantomjs_webdriver().get(p_url)
    os.chdir(get_ouput_dir())
    file_path = get_ouput_dir()+"/snapshot"
    if not os.path.exists(file_path):
      os.mkdir("snapshot")

    if p_file == None:
      p_file = "snapshot_"+str(uuid.uuid1())+".png"
    print (file_path+"/"+p_file)
    
    stored = get_phantomjs_webdriver().get_screenshot_as_file(file_path+"/"+p_file)
    return stored

  def getProperty(self, p_name):  
    pass

  def setProperties(self, p_parameters):  
    duration = p_parameters["duration"] if p_parameters.has_key("duration") else None
    tfile = p_parameters["file"] if p_parameters.has_key("file") else None
    if duration:
      self._act_time = int(duration)
    if tfile:
      self._file = tfile

  def getData(self):
    pass