# -*- coding: utf-8 -*-

import os,sys,re,time
import yaml
import tornado.ioloop

parent_path = os.path.dirname(sys.path[0])
if parent_path not in sys.path:
  sys.path.append(parent_path)

from automation.common.elasticsearch import ESHandler
from automation.common.logging import Logger
from automation.common.network import ServerWrapper
from automation.common.application import Configure
from automation.scheduler.orchestrate import ParellelSchedule

class Main(object):    
  es_client=None
  parellelSchedule=None
  
  @staticmethod
  def fuckup(p_command=None):
    Main.rootdir = os.path.abspath('.')
    
    #Initialize application configure
    filename = "application-config.yml"
    Configure.load(p_dir=Main.rootdir+"/"+filename, p_command=p_command)
        
    #Initialize log    
    Logger()

    #Initialize elasticsearch client
    ESHandler.ini()
    
    #Initialize job schedule
    Main.parellelSchedule=ParellelSchedule()
    if Main.parellelSchedule :
      Main.parellelSchedule.start()
    
    #Initialize server
    ServerWrapper.listen(p_name="Master-Scheduler", p_prefix="server.crawler.healthServer", p_handler=Main.parellelSchedule)
#     try:
#         # This is here to simulate application activity (which keeps the main thread alive).
#         while True:
#             time.sleep(2)
#     except (KeyboardInterrupt, SystemExit):
#         # Not strictly necessary if daemonic mode is enabled but should be done if possible
#         parellelSchedule.shutdown()
    tornado.ioloop.IOLoop.current().start()
            
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