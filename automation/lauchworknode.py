# -*- coding: utf-8 -*-

import os,sys,re,time,threading
import queue
from pytz import utc
import yaml,socket

from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
from apscheduler.schedulers.background import BackgroundScheduler

import tornado.ioloop

parent_path = os.path.dirname(sys.path[0])
if parent_path not in sys.path:
  sys.path.append(parent_path)

from automation.common.elasticsearch import ESHandler
from automation.common.logging import Logger
from automation.common.network import ServerWrapper
from automation.common.network import Client

from automation.common.application import Configure
from automation.worknode.notify import Communicator
from automation.worknode.slave import Leader
from automation.worknode.monitor import MultiProcessJobWatcher

class Main(object):    
  es_client=None
  communicator=None
  ApplicationContext = {}
  ipAddr=None
  
  @staticmethod
  def fuckup(p_command=None):
    Main.rootdir = os.path.abspath('.')
    
    #Initialize application configure
    filename = "application-config.yml"
    Configure.load(p_dir=Main.rootdir+"/"+filename, p_command=p_command)
        
    nodename = Configure.configure().value("worknode.name")
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        Main.ipAddr = s.getsockname()[0]
    finally:
        s.close() 
    
    #Initialize log    
    Logger()

    #Initialize elasticsearch client
    Main.es_client = ESHandler() 
    
    #Initialize worker monitor
    monitor = MultiProcessJobWatcher()
    executors = {
                'default': ThreadPoolExecutor(1),
                'processpool': ProcessPoolExecutor(1)
                 }
    job_defaults = {
                'coalesce': True,
                'max_instances': 1
                 }
    mosche = BackgroundScheduler(executors=executors, job_defaults=job_defaults, timezone=utc)  
    mosche.add_job(monitor,'interval',seconds=10)
      
    #Initialize worker leader
    leader=Leader(p_node_name=nodename, p_monitor=monitor)
      
    #Initialize node register and health info report schedule
    scheduleserveraddr = Configure.configure().value("server.crawler.healthServer.host")
    scheduleserverport = Configure.configure().value("server.crawler.healthServer.port")
    scheduleserver={"host":scheduleserveraddr,"port":scheduleserverport}
    Main.communicator=Communicator(p_schedule_server=scheduleserver, p_leader=leader)
      
    #Initialize node job accept service
    ServerWrapper.listen(p_name=nodename, p_prefix="server.crawler.nodeServer", p_handler=leader)
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

# mq = queue.Queue(100)
# communicator=Communicator(p_mq=mq)
# register = communicator.getRegister()
# health = communicator.getHealth()
# 
# m={"host":"localhost","port":8036}
# client = SimpleTcpclient(p_mq=mq, p_server_map=m, p_callback=register)
# #client.start()
# print ("client initial done!")