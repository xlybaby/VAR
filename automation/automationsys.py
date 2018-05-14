# -*- coding: utf-8 -*-

import sys
import os

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

class Configure(object):
  ouput_dir = None
  root_dir = None
  phantomjs_webdriver = None
  application = "automation"

def get_ouput_dir():
  return Configure.ouput_dir

def get_application_root_dir():
  return Configure.root_dir

def get_phantomjs_webdriver():
  return Configure.phantomjs_webdriver

# instantiate a chrome options object so you can set the size and headless preference
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--window-size=1024x768")
chrome_driver = "/usr/local/python/library/chromedriver"
Configure.phantomjs_webdriver = webdriver.Chrome(chrome_options=chrome_options, executable_path=chrome_driver)

#Configure.phantomjs_webdriver = webdriver.PhantomJS()

parent_path = os.path.dirname(sys.path[0])
Configure.ouput_dir = parent_path + "/" + Configure.application + "/outputs"
Configure.root_dir = parent_path + "/" + Configure.application