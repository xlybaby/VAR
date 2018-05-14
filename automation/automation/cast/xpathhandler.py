# -*- coding: utf-8 -*-

import os
import re

from automation.performance.actor import Actor

class XPathExtractor(Actor): 
    
  def __init__(self, p_selector,p_type, p_id, p_class, p_xpath, p_name, p_tag, p_configure_file, p_path):
    Actor.__init__(self, p_selector,p_type, p_id, p_class, p_xpath, p_name, p_tag)
    self._selector=p_selector
    self._act_time = None
    self._configure_file =  p_configure_file
    self._p_path = p_path
    
    self.init()

  def init(self):
    pass