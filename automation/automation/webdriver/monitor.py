# -*- coding: utf-8 -*-

import datetime, threading
from multiprocessing import Process
from pytz import utc

import apscheduler.executors.pool
from apscheduler.schedulers.background import BackgroundScheduler

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from automation.common.logging import Logger
from automation.common.application import Configure
from automation.webdriver.driver import DriverProcess

class PooledWebDriverManager(threading.Thread):

  def __init__(self, p_queue, p_request_queue):
    #Process.__init__(self)  
    threading.Thread.__init__(self) 
    self._interval = Configure.configure().value("headless.webdriver.browserIdleTimeMonitorInterval")
    self._max_idle_time = Configure.configure().value("headless.webdriver.maxBrowserIdleTime")
    
    self._alertMinAvailableNum = Configure.configure().value("headless.webdriver.alertMinAvailableNum")
    self._alertMaxAvailableNum = Configure.configure().value("headless.webdriver.alertMaxAvailableNum")
    self._monitorMinAvailableNum = Configure.configure().value("headless.webdriver.monitorMinAvailableNum")
    self._monitorMaxAvailableNum = Configure.configure().value("headless.webdriver.monitorMaxAvailableNum")
    
    self._iniBrowserNum = Configure.configure().value("headless.webdriver.iniBrowserNum")
    self._iniWinHeight = Configure.configure().value("headless.webdriver.iniBrowserWinHeight")
    self._iniWinWidth = Configure.configure().value("headless.webdriver.iniBrowserWinWidth")
    self._driver_path = Configure.configure().value("headless.webdriver.path")

    self._alert_used_rate = 0.5
    #self._alert_job_interval = 5
    self._driver_queue = p_queue
    self._request_queue = p_request_queue
    
  def run(self):
    executors = {
                'default': apscheduler.executors.pool.ThreadPoolExecutor(2),
                'processpool': apscheduler.executors.pool.ProcessPoolExecutor(2)
                 }
    job_defaults = {
                'coalesce': True,
                'max_instances': 1
                 }
    self._scheduler = BackgroundScheduler(executors=executors, job_defaults=job_defaults, timezone=utc)  
    #self._scheduler.add_job(self.checkLess,'interval',seconds=self._monitorMinAvailableNum)
    #self._scheduler.add_job(self.checkOverload,'interval',seconds=self._monitorMaxAvailableNum)
    self._scheduler.add_job(self.check,'interval',seconds=self._monitorMinAvailableNum)
    Logger.getLogger().info("Web driver pool manager starts")
    self._scheduler.start()
  
  def check(self):
    drivernum = self._driver_queue.qsize()
    requestnum = self._request_queue.qsize() 
    print ("current driver num is %d, waiting request num is %d"%(drivernum, requestnum))
    if round(requestnum/drivernum, 4) >= 0.5:
      print ("waiting request num is half of driver num")  
      for i in range(self._iniBrowserNum):
        try:  
          timeout = int(Configure.configure().value("headless.webdriver.addedNewDriverProcessAliveTimeout")) + i  
          proc = DriverProcess(p_request_queue=self._request_queue, p_alive_timeout=timeout)
          self._driver_queue.put(proc, block=False)
          proc.start()    
        except:
          pass   
      
  def checkOverload(self):
    cursize = self._driver_queue.qsize()
    Logger.getLogger().info ("*** check idle driver count, current queue size: %d"%(cursize))
    if cursize >= self._alertMaxAvailableNum:
      Logger.getLogger().info ("Current queue size is great than alert idle value: %d >= %d"%(cursize, self._alertMaxAvailableNum) )
      num = self._alertMaxAvailableNum - cursize
      for i in range(num):
        try:
          proc = self._driver_queue.get(block=False)
          proc.raiseExc(SystemExit)
          #proc.getInputQueue.put("Over")
#           driverwrapper = proc.getDriverwrapper()
#           driver = driverwrapper["driver"]
#           driver.quit()
#           driver = None
#           driverwrapper = None
        except:
          pass
      
  def checkLess(self):
    cursize = self._driver_queue.qsize()
    Logger.getLogger().info ("*** check minimum driver count, current queue size: %d"%(cursize))
    if cursize <= self._alertMinAvailableNum:
      Logger.getLogger().info ("Current queue size is less than alert minimum value: %d <= %d"%(cursize, self._alertMinAvailableNum) )
      for i in range(self._iniBrowserNum):
        try:  
          proc = DriverProcess()
          self._driver_queue.put(proc, block=False)
          proc.start()    
#           chrome_options = Options()
#           chrome_options.add_argument("--headless")
#           chrome_options.add_argument("--window-size="+str(self._iniWinWidth)+"x"+str(self._iniWinHeight))
#           driver = webdriver.Chrome(chrome_options=chrome_options, executable_path=self._driver_path)
#           driverwrapper = {"driver": driver, "instancetime": datetime.datetime.now(), "lastactivetime": datetime.datetime.now(), "usetimes": 0 }
#           self._queue.put(driverwrapper, block=False)
        except:
          pass
    