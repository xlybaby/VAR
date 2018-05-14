# -*- coding: utf-8 -*-

import os
from selenium import webdriver

from automationsys import get_phantomjs_webdriver
from automationsys import get_ouput_dir
from automation.cast.cookie import CookieHandler
from automation.performance.script import Scenario

class Executor(object):

  def __init__(self, p_scenario_id):
    self._scenario_id = p_scenario_id
    self._scenario = Scenario(p_scenario_id)

  def action(self, template=None):
    scene_queue = self._scenario.load(template=template)
    driver = get_phantomjs_webdriver()
    for scene in scene_queue:
      addr = scene.address()
      print ("get addr: "+addr)
      driver.get(addr)
      #driver.implicitly_wait(5)
      #driver.set_window_size(1024, 768)
      scene.start()
      scene.join()
      #CookieHandler.populate_cookies()