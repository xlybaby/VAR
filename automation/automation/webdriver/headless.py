# -*- coding: utf-8 -*-

import asyncio, datetime, json, queue, uuid, time, threading, traceback
from multiprocessing import Process,Manager

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import tornado.ioloop

from automation.common.logging import Logger
from automation.common.network import ServerWrapper
from automation.common.application import Configure
from automation.webdriver.monitor import PooledWebDriverManager
from automation.webdriver.driver import DriverProcess
 
class WebDriverContainer(threading.Thread):
  
  def __init__(self, p_queue, p_request_queue):
    #Process.__init__(self)  
    threading.Thread.__init__(self)
    self._ini_driver_num = Configure.configure().value("headless.webdriver.iniBrowserNum")
    self._request_queue = p_request_queue
    #self._driver_index_map = {}
    #self._driver_queue = p_queue
    self._driver_process_queue = p_queue

  async def callback(self, p_message=None):
    ret = None
    proc = None
    print ("Request coming: ", p_message)
    try:
      proc = await asyncio.wait_for(self._driver_process_queue.get(), Configure.configure().value("headless.webdriver.freeDriverWaittingTimeout"))
      Logger.getLogger().info("Got a web driver")
      proc.getInputQueue().put(p_message, block=False)
      print ("put message: ", p_message)
      #await proc.execute(p_message)
      outq = proc.getOutputQueue()
      print ("Waiting for response: ")
      ret = await asyncio.wait_for(outq.get(),timeout=None)
      print ("Got response: ", ret)
      return ret
  
    except asyncio.TimeoutError:
      Logger.getLogger().error("Can't get free web driver")
      return "None"
    finally:
      if proc != None:
        self._driver_process_queue.put_nowait(proc)
  
  def run(self):
    Logger.getLogger().info("Initial web driver")
    for i in range(self._ini_driver_num):
      proc = DriverProcess(p_request_queue=self._request_queue)
      proc.start() 
      self._driver_process_queue.put(proc, block=True)
      Logger.getLogger().info("Add one web driver...")
      
    self.pooledWebDriverManager = PooledWebDriverManager(p_queue = self._driver_process_queue, p_request_queue = self._request_queue)
    self.pooledWebDriverManager.start()
      