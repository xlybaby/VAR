# -*- coding: utf-8 -*-

import os
import urllib3

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

class HeadlessWebDriverManager(object):
    
  def __init__(self, p_driver):
    self._chrome = p_driver
        
  @staticmethod
  def getConnection(p_width=1280, p_height=700):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size="+str(p_width)+"x"+str(p_height))
    driver = webdriver.Chrome(chrome_options=chrome_options, executable_path="/usr/local/python/webdriver/chromedriver")
  
    return HeadlessWebDriverManager(p_driver=driver)

  def get(self, p_uri):
   self._chrome.get( p_uri )  
   return self._chrome.page_source 
    
  def get_screenshot_as_file(self, p_dir):
    return self._chrome.get_screenshot_as_file(p_dir)

  def quit(self):
    self._chrome.quit()

  def getDriver(self):
    return self._chrome
    
class HttpConnectionManager(object):
  
  def __init__(self, p_http):
    self._http = p_http
        
  @staticmethod
  def getConnection():
    http = urllib3.PoolManager()
    con = HttpConnectionManager(p_http=http)    
    return con

  def get(self, p_uri):
    r = self._http.request( 'GET', p_uri )  
    data = None
    if r:
      data = r.data  
      r.release_conn()
      
    return data    
    
  def quit(self):
    pass
#     self._http.clear()  
#     self._http = None