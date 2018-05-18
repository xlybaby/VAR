# -*- coding: utf-8 -*-

import os
import time
import uuid

from automationsys import Configure
from automation.performance.actor import Actor

class PageCapture(Actor):

  def __init__(self, p_selector, p_type, p_id, p_class, p_xpath, p_name, p_tag, p_parameters,p_data_model=None):
    Actor.__init__(self, p_selector,p_type, p_id, p_class, p_xpath, p_name, p_tag)
    self._act_time = None
    self._file = None
    self._time_format = '%Y-%m-%d.%X'
    self.setProperties(p_parameters)

  def do(self, p_location=None):
    self.capture_whole(self._file)

  def duration(self):
    return self._act_time

  def capture_whole(self, p_file=None, p_url=None):
    #get_phantomjs_webdriver().get(p_url)
    os.chdir(Configure.get_ouput_dir())
    file_path = Configure.get_ouput_dir()+"/snapshot"
    if not os.path.exists(file_path):
      os.mkdir("snapshot")

    if p_file == None:
      p_file = "snapshot_"+str(uuid.uuid1())+".png"
    print (file_path+"/"+p_file)
    print (Configure.get_chrome_webdriver().get_window_size())
    
    #Get web page's actual height
    clientHeight = Configure.get_chrome_webdriver().execute_script("return document.body.clientHeight;")
    print (clientHeight)
    #Adjuest window's height to fit web page's height
    cursize = Configure.get_chrome_webdriver().get_window_size()
    Configure.get_chrome_webdriver().set_window_size(cursize["width"], clientHeight)
    
    stored = Configure.get_chrome_webdriver().get_screenshot_as_file(file_path+"/"+p_file)
    return stored

  def getProperty(self, p_name):  
    pass

  def setProperties(self, p_parameters):  
    duration = p_parameters["duration"] if "duration" in p_parameters else None
    tfile = p_parameters["file"] if "file" in p_parameters else None
    if duration:
      self._act_time = int(duration)
    if tfile:
      self._file = tfile

  def getData(self):
    pass