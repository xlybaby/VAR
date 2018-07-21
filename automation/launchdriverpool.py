# -*- coding: utf-8 -*-

import asyncio, datetime, os,sys,re,time
import yaml
import queue

from multiprocessing import Manager
import tornado.ioloop

parent_path = os.path.dirname(sys.path[0])
if parent_path not in sys.path:
  sys.path.append(parent_path)

from automation.common.logging import Logger
from automation.common.application import Configure
from automation.webdriver.headless import WebDriverContainer
from automation.webdriver.monitor import PooledWebDriverManager
from automation.common.network import ServerWrapper
from automation.webdriver.hub import StreamHandler

class Main(object):    
  
  webDriverContainer = None
  pooledWebDriverManager = None
  
  @staticmethod
  def fuckup(p_command=None):
    start = datetime.datetime.now()
    Main.rootdir = os.path.abspath('.')
    manager = Manager()
    
    #Initialize application configure
    filename = "application-config.yml"
    Configure.load(p_dir=Main.rootdir+"/"+filename, p_command=p_command)
        
    #Initialize log    
    Logger()
    Logger.getLogger().info("Web Driver Pool Launching......")
    
    #Initialize driver pool
    driver_queue = queue.Queue(Configure.configure().value("headless.webdriver.maxBrowserNum"))
    request_queue = queue.Queue(Configure.configure().value("headless.webdriver.maxRequestAcceptNum"))
    #Manager().Queue(Configure.configure().value("headless.webdriver.maxBrowserNum"))

    Main.webDriverContainer = WebDriverContainer( p_queue = driver_queue, p_request_queue = request_queue )
    Main.webDriverContainer.run()
    
    #Main.pooledWebDriverManager = PooledWebDriverManager(p_queue = queue)
    #Main.pooledWebDriverManager.start()
    end = datetime.datetime.now()
    duration = (start-end).seconds
    Logger.getLogger().info("Web Driver Pool Launched after %d seconds"%(duration))
    
    try:
      delimiter = Configure.configure().value("server.webdriverServer.delimiter")
      deary = delimiter.split('\\x')
      #print ("delimiter's array: ", deary)
      destr = ''
      for i in range(len(deary)):
        if deary[i] != '':
          de = chr(int(deary[i],16))
          destr = de + destr  
      StreamHandler.startlisten(p_name="Headless-Webdriver-Server", p_prefix="server.webdriverServer", p_queue=request_queue, p_delimiter=destr)
      #tornado.ioloop.IOLoop.current().start()
    except (KeyboardInterrupt, SystemExit):
      pass
#       Logger.getLogger().info ("***************** System exiting *****************") 
#       Logger.getLogger().info ("Clear driver queue - %d dirver remain in the queue"%(driver_queue.qsize())) 
#       try:
#         qsize = driver_queue.qsize()
#         for i in range(qsize):
#           proc = driver_queue.get() 
#           driverwrapper = proc.getDriverwrapper()
#           driver = driverwrapper["driver"]
#           driver.quit()
#           Logger.getLogger().info ("One driver quit.")              
#       except:
#         pass
               
if __name__ == '__main__':
  #print (sys.argv)
  props={}
  if len(sys.argv) > 1:
    for idx in range(1, len(sys.argv)):
      arg = sys.argv[idx]
      if arg.startswith("--") :
        prop = arg[2:]
        pair = prop.split("=")
        props[pair[0]]=pair[1]
    print ("command props", props)
    
  Main.fuckup(p_command=props)   