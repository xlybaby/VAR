#-*-coding:utf-8-*-
import os
import threading
from time import ctime,sleep

from selenium import webdriver

from automationsys import get_phantomjs_webdriver
from automationsys import get_ouput_dir
from automation.performance.actor import Actor
from automation.performance.loophelper import ForeachHelper
from automation.cast.assistant import Locator

class Foreach(Actor):

  def __init__(self, p_selector, p_type, p_id, p_class, p_xpath, p_name, p_tag, p_parameters, p_data_model=None):
    self._act_time = None
    self._act_list = []
    self._data_list = []
    self._data_record_model = {}
    self._data_record_cursor = 0
    self._selector = p_selector
    self.init(p_selector)

  def do(self):  
    res=self.nextRecord()
    while res:
      for actor in self._act_list:
        time = actor.duration()
        print ("Foreach actor perform: ")
        print (actor)
        actor.do()
        if time:
          sleep(time)
      res = self.nextRecord()

  def duration(self):
    return self._act_time

  def getProperty(self, p_name):  
    pass

  def setProperties(self, p_parameters):  
    pass
  
  def getData():
    pass

  def init(self, p_selector):
    self._data_list = ForeachHelper.loadData(p_selector)
    self._act_list = ForeachHelper.initActors(p_selector,p_data_model=self._data_record_model)

  def nextRecord(self):
    if self._data_record_cursor >= len(self._data_list):
      return None
    rec = self._data_list[self._data_record_cursor]
    for idx, key in enumerate(rec.keys()):
      val = rec[key]
      self._data_record_model[key]=val
    self._data_record_cursor+=1
    return 1