# -*- coding: utf-8 -*-

import os
import datetime
import json
import random
import threading
import time

from scrapy.selector import Selector 

from automation.scenario.entity import Scenario
from automation.cast.recording import PageCrawl
from automation.performance.util import Util
from automation.scenario.selector import PageElementFinder
from automationsys import Configure

class ImagePicker(Actor):

  def __init__( self, p_scenario, p_parameters, p_sceneno, p_pageno, p_imgselector, p_imglinkselector, p_pageid=None ):
    self._scenario = p_scenario
    self._pageid = p_pageid
    self._imgselector = p_imgselector
    self._imglinkselector = p_imglinkselector
    self.setProperties(p_parameters)
    
    self._sceneno = p_sceneno
    self._pageno = p_pageno

  def do(self, p_selector, p_location=None):
    imgs = PageElementFinder.getCompInstance(p_selector=p_selector, p_element=self._imgselector)
    imglinks = PageElementFinder.getCompInstance(p_selector=p_selector, p_element=self._imglinkselector)
    
  def setProperties(self, p_parameters):  
    self._saveimg =   p_parameters["saveimg"] if "saveimg" in p_parameters else None
    self._attachlink =   p_parameters["attachlink"] if "attachlink" in p_parameters else None
