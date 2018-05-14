#-*-coding:utf-8-*-

from selenium import webdriver

from automationsys import get_phantomjs_webdriver
from automationsys import get_ouput_dir
from automation.performance.actor import Actor
from assistant import Locator

class Iterator(Actor):

  def __init__( self, p_act_time, p_type, p_id, p_class, p_xpath, p_name, p_actor ):
    self._act_time = None
    if p_act_time:
      self._act_time = int(p_act_time)
    self._type=p_type
    self._id=p_id
    self._class=p_class
    self._xpath=p_xpath
    self._name=p_name
    self._actor=p_actor

  def do(self):
  	elements = None
    if self._id :
      elements = Locator.find_elements_with_id(self._id)
    if self._class :
      elements = Locator.find_elements_by_class_name(self._class)
    if self._xpath :
      elements = Locator.find_elements_by_xpath(self._xpath)
    if self._name :
      elements = Locator.find_elements_by_name(self._name)
    else :
      return None
    for el in elements:
      
  def duration(self):
    return self._act_time