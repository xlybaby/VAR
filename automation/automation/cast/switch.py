#-*-coding:utf-8-*-
import os
from selenium import webdriver

from automationsys import get_phantomjs_webdriver
from automationsys import get_ouput_dir
from automation.performance.actor import Actor
from automation.cast.assistant import Locator

class Changer(Actor):
  
  def __init__(self, p_selector, p_type, p_id, p_class, p_xpath, p_name, p_tag, p_parameters,p_data_model=None):
    Actor.__init__(self, p_selector,p_type, p_id, p_class, p_xpath, p_name, p_tag)
    self._act_time = None
    self._type = None
    self._window = None
    self._url = None
    self._frame_name = None
    self._frame_id = None
    self._frame_class = None
    self._frame_index = None
    self.setProperties(p_parameters)

  def do(self):
    if self._type == "window":
      self.switch_window()

    elif self._type == "frame":
      self.switch_frame()

    elif self._type == "parent_frame":
      self.switch_parent_frame()

  def duration(self):
    return self._act_time

  def switch_parent_frame(self):
    get_phantomjs_webdriver().switch_to.parent_frame()

  def switch_frame(self):
    driver = get_phantomjs_webdriver()
    xpath=None
    if self._frame_index:
      xpath = "//iframe["+str(self._frame_index)+"]"
    frame = Locator.find(self._frame_id, self._frame_class, xpath, self._frame_name)
    driver.switch_to.frame(frame)
    print (driver.page_source)

  def switch_window(self):
    driver = get_phantomjs_webdriver()
    handles = driver.window_handles

    print ("switch window: "+self._window)
    if self._window:
      driver.switch_to.window(self._window)
      driver.implicitly_wait(30)
      driver.set_window_size(1920, 1080)
      return

    print ("switch url: "+self._url)
    if self._url:
      for handle in handles:
        print ("switch to window: " + handle)
        driver.switch_to.window(handle)
        driver.implicitly_wait(30)
        driver.set_window_size(1920, 1080)
        cur_url = driver.current_url
        print ("window url: " +cur_url)
        if cur_url.find(self._url) >= 0 :
          break

  def getProperty(self, p_name):  
    pass

  def setProperties(self, p_parameters):  
    duration = p_parameters["duration"] if p_parameters.has_key("duration") else None
    type = p_parameters["type"]
    window_name = p_parameters["window_name"]
    url = p_parameters["url"]
    frame_name = p_parameters["frame_name"]
    frame_id = p_parameters["frame_id"]
    frame_class = p_parameters["frame_class"]
    frame_index = p_parameters["frame_index"]

    self._type = type
    self._window = window_name
    self._url = url
    self._frame_name = frame_name
    self._frame_id = frame_id
    self._frame_class = frame_class
    self._frame_index = frame_index

    if duration:
      self._act_time = int(duration)

  def getData(self):
    pass