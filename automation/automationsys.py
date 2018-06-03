# -*- coding: utf-8 -*-

import sys,os

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from automation.performance.connection import HttpConnectionManager

class Configure(object):
  ouput_dir = None
  root_dir = None
  extract_dir = None
  driver_dir = None
  
  phantomjs_webdriver = None
  chrome_webdriver = None
  native_webdriver = None
  application = "automation"
  
  @staticmethod
  def setextractdir(p_dir):
    Configure.extract_dir = p_dir
        
  @staticmethod
  def get_extract_dir():
    return Configure.extract_dir
    
  @staticmethod
  def setconfig(p_dir):
    if p_dir.endswith("/"):
       p_dir = p_dir[0:len(p_dir)-1]     
    Configure.root_dir = p_dir
  
  @staticmethod
  def setdriver(p_dir):
    if p_dir.endswith("/"):
       p_dir = p_dir[0:len(p_dir)-1]     
    Configure.driver_dir = p_dir
              
  @staticmethod
  def setoutput(p_dir):
    if p_dir.endswith("/"):
       p_dir = p_dir[0:len(p_dir)-1]    
    Configure.ouput_dir = p_dir
  
  @staticmethod              
  def get_ouput_dir():
    return Configure.ouput_dir

  @staticmethod 
  def get_application_root_dir():
    return Configure.root_dir
  
  @staticmethod
  def get_chrome_webdriver():
    if not Configure.chrome_webdriver:
      chrome_options = Options()
      chrome_options.add_argument("--headless")
      chrome_options.add_argument("--window-size=1280x700")
      chrome_driver = Configure.driver_dir
      Configure.chrome_webdriver = webdriver.Chrome(chrome_options=chrome_options, executable_path=chrome_driver)
  
    return Configure.chrome_webdriver
  
  @staticmethod
  def get_http_lowlevel_webdriver():
    return HttpConnectionManager.getConnection()

  @staticmethod
  def get_phantomjs_webdriver():
    if not Configure.phantomjs_webdriver:
      Configure.phantomjs_webdriver = webdriver.PhantomJS()   
    return Configure.phantomjs_webdriver

#parent_path = os.path.dirname(sys.path[0])
#Configure.ouput_dir = output_file
#Configure.root_dir = config_file