#-*-coding:utf-8-*-

from selenium import webdriver

from automationsys import get_phantomjs_webdriver
from automationsys import get_ouput_dir
from automation.performance.actor import Actor
from automation.cast.assistant import Locator

class ClickEvent(Actor):

  def __init__(self, p_selector, p_type, p_id, p_class, p_xpath, p_name, p_tag, p_parameters,p_data_model=None):
    Actor.__init__(self, p_selector, p_type, p_id, p_class, p_xpath, p_name, p_tag)
    self._selector=p_selector
    self._act_time = None
    self.setProperties(p_parameters)

  def click(self):
    elements = self.getComponent()
    if elements:
      #if self._xpath and self._xpath.find("usersignInfo") >=0 :
        #print self._component 
        #return
      for e in  elements :
        e.click()

  def do(self):  
    self.click()

  def duration(self):
    return self._act_time

  def getProperty(self, p_name):  
    pass

  def setProperties(self, p_parameters):  
    duration = p_parameters["duration"] if p_parameters.has_key("duration") else None
    if duration:
      self._act_time = int(duration)

  def getData():
    pass