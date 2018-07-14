# -*- coding: utf-8 -*-

import os,sys,re,time
import yaml
import tornado.ioloop
import queue

from multiprocessing import Manager
from multiprocessing.managers import BaseManager

#from tornado.queues import Queue

parent_path = os.path.dirname(sys.path[0])
if parent_path not in sys.path:
  sys.path.append(parent_path)

from automation.common.elasticsearch import ESHandler
from automation.common.logging import Logger
from automation.common.application import Configure
from automation.scheduler.orchestrate import ParellelSchedule
from automation.scheduler.orchestrate import CrawlerRegister
from automation.scheduler.orchestrate import CrawlerPicker
from automation.scheduler.orchestrate import JobSync
from automation.common.asyncqueue import ThreadSafeQueue

class Main(object):    
  es_client=None
  parellelSchedule = None
  crawlerRegister = None
  jobSync = None
  
  @staticmethod
  def fuckup(p_command=None):
    Main.rootdir = os.path.abspath('.')
    manager = Manager()
    #BaseManager.register('CrawlerPicker', CrawlerPicker)
    #manager = BaseManager()
    
    #Initialize application configure
    filename = "application-config.yml"
    Configure.load(p_dir=Main.rootdir+"/"+filename, p_command=p_command)
        
    #Initialize log    
    Logger()

    #Initialize elasticsearch client
    ESHandler.ini()
    
    #Initialize job schedule
    #main_jod_queue = queue.Queue(Configure.configure().value("scheduler.messageQueueSize", p_default=1000))
    main_jod_queue = ThreadSafeQueue(size=Configure.configure().value("scheduler.messageQueueSize", p_default=1000))

    crawler_picker = CrawlerPicker()
    Main.crawlerRegister = CrawlerRegister(p_crawler_picker=crawler_picker, p_main_jod_queue=main_jod_queue)
    Main.crawlerRegister.start()

    #main_jod_queue = manager.Queue(Configure.configure().value("scheduler.messageQueueSize", p_default=1000))
    #main_jod_queue = Queue(maxsize=Configure.configure().value("scheduler.messageQueueSize", p_default=1000))
    
    Main.parellelSchedule=ParellelSchedule(p_main_jod_queue=main_jod_queue)
    Main.parellelSchedule.start()
    #Main.parellelSchedule.run()
    
    #Main.crawlerRegister.daemon = True
    #Main.crawlerRegister.run()
    
    #registerserver = Configure.configure().value("server.crawler.healthServer.host")
    #registerport = Configure.configure().value("server.crawler.healthServer.port")
    #Main.jobSync = JobSync(p_queue=main_jod_queue, p_register={"host":registerserver, "port":registerport}, p_crawler_picker=crawler_picker)
    #Main.jobSync.start()
    #Start main thread loop
    #tornado.ioloop.IOLoop.current().start()
    
    #After start all sub process, we need invode join function to make shared object available
    #Main.jobSync.join()
    Main.crawlerRegister.join()
    
    #Initialize server
    try:
        # This is here to simulate application activity (which keeps the main thread alive).
        while True:
            time.sleep(2)
    except (KeyboardInterrupt, SystemExit):
      pass    
        # Not strictly necessary if daemonic mode is enabled but should be done if possible
#         parellelSchedule.shutdown()
            
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