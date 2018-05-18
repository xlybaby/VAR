# -*- coding: utf-8 -*-

import os
import re

from automationsys import Configure
from automation.performance.actor import Actor
from automation.cast.assistant import Locator

class InputComponent(Actor):

  def __init__(self, p_selector,p_type, p_id, p_class, p_xpath, p_name, p_tag, p_parameters, p_data_model=None):
    Actor.__init__(self, p_selector,p_type, p_id, p_class, p_xpath, p_name, p_tag)
    print ("init input comp, name -> " + p_name)
    self._selector = p_selector
    self._act_time = None
    self._type = None
    self._value = None
    self._comp = None
    self._data_model = p_data_model
    self._dataBinding = False
    self._databinding_pattern = re.compile(r'\{\{[\w\d]+\}\}')
    self._databinding_key = None
    self.setProperties(p_parameters)
    
  class Text(object):

    def __init__(self, p_comp):
      self._component = p_comp

    def input(self, p_value):
      if self._component:
        print ("Input send key: " + p_value)
        for com in self._component:
          com.clear()
          com.send_keys(p_value)

  class RichText(object):

    def __init__(self, p_comp):
      pass

  class Select(object):

    def __init__(self, p_name,p_tag,p_class,p_id):
      self._name = "'"+p_name+"'" if p_name else "null"
      self._tag = "'"+p_tag+"'" if p_tag else "null"
      self._class = "'"+p_class+"'" if p_class else "null"
      self._id = "'"+p_id+"'" if p_id else "null"

      self._find_script = open(Configure.get_application_root_dir()+"/js/findelements_min.js")
      self._select_script = open(Configure.get_application_root_dir()+"/js/select_min.js")
      self._find_scripts = None
      self._select_scripts = None
      if self._find_script:
        self._find_scripts = self._find_script.readline()
      if self._select_script:
        self._select_scripts = self._select_script.readline()

    def input(self, p_value):
      func = u"select('"+p_value+"',"+self._name+","+self._tag+","+self._class+","+self._id+");"
      print (func)
      Configure.get_chrome_webdriver().execute_script(self._find_scripts.decode("utf-8")+" "+self._select_scripts.decode("utf-8")+" "+func);

  def do(self, p_location=None):  
    lines = self.getData()
    print ("Input get data: "+lines)

    if self._type == "text":
      comp = self.getComponent()
      text = self.Text(comp)
      text.input(lines)
      return

    if self._type == "select":
      select = self.Select(p_name=self.getName(),p_tag=self.getTag(),p_class=self.getClass(),p_id=self.getID())
      select.input(lines)
      return

  def duration(self):
    return self._act_time

  def getProperty(self, p_name):  
    pass

  def getData(self):
    if self._dataBinding:
      return self._data_model[self._databinding_key]
    else:
      return self._value

  def setProperties(self, p_parameters):  
    duration = p_parameters["duration"] if p_parameters.has_key("duration") else None
    type = p_parameters["type"] if p_parameters.has_key("type") else None
    contents = p_parameters["contents"] if p_parameters.has_key("contents") else ""

    m = self._databinding_pattern.match(contents)
    if m:
      self._dataBinding = True
      self._databinding_key = contents[2:-2]
    else:
      self._value=contents

    if duration:
      self._act_time = int(duration)
    self._type = type
     