# -*- coding: utf-8 -*-
  
import os,sys,time
import queue
import json

from pytz import utc

from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
from apscheduler.schedulers.background import BackgroundScheduler

import tornado.gen
  
from automation.common.application import Configure
  
from automation.common.logging import Logger
from automation.common.network import ServerWrapper
from automation.common.network import SimpleTcpclient
from automation.common.constants import StatusCode
from automation.common.asyncqueue import ThreadSafeQueue

class Communicator(object):
    
  def __init__(self, p_schedule_server, p_leader):
    self._schedule_server = p_schedule_server
    self._leader = p_leader
    #self._scheduler = self.getSchedule()
#     reg = Configure.configure().value(p_key="scheduler.worknodes.register.interval")
#     hea = Configure.configure().value(p_key="scheduler.worknodes.health.interval")
    self._register_instance = None
    self._register_task = self.generateRegisterTask(p_interval=Configure.configure().value(p_key="worknode.registerInterval"))
    #self._health_task = self.generateHealthInfo(p_interval=7)
    #self._scheduler.start()
    
  def getSchedule(self):
    executors = {
                'default': ThreadPoolExecutor(3),
                'processpool': ProcessPoolExecutor(1)
                 }
    job_defaults = {
                'coalesce': True,
                'max_instances': 1
                 }
    scheduler = BackgroundScheduler(executors=executors, job_defaults=job_defaults, timezone=utc)    
    return scheduler
  
  def getRegister(self):
    return self._register_instance
      
#   def getHealth(self):
#     return self._health_instance

  def generateRegisterTask1(self, p_interval):
    host = self._leader.getHost()
    port = self._leader.getPort()
    data = {"host": host, "port": port, "id":self._leader.getId()}
    self._register_instance = Register(p_server=self._schedule_server, p_node=data)
    return self._scheduler.add_job(self._register_instance,'interval',seconds=p_interval)
  
  def generateRegisterTask(self, p_interval):
    host = self._leader.getHost()
    port = self._leader.getPort()
    data = {"host": host, "port": port, "id":self._leader.getId()}
    self._register_instance = Register(p_server=self._schedule_server, p_node=data, p_interval=p_interval)
    self._register_instance.start()
    #return self._scheduler.add_job(self._register_instance,'interval',seconds=p_interval)

class Register(object):

  def __init__(self, p_server, p_node, p_interval):
    self._isRegistered = False 
     
    self._node = p_node
    self._mp = ThreadSafeQueue(size=10)#queue.Queue(10)
    self._server = p_server
    self._interval = p_interval
    
    self._client = SimpleTcpclient(p_mq=self._mp, p_server_map=p_server, p_callback=self.handle)
    self._client.start()
    print ("communicator client starts...")
    
  def __call__(self):
    if self._isRegistered == False: 
      self._node["event"]="register"  
      self._mp.put(self._node, block=False)
      print ("register self to server", self._node)
      Logger.getLogger().info('Start register self to server: %s_%s:%d', self._node["id"], self._node["host"], int(self._node["port"]))

    else:
      pass
      #print ("send health info...")
      
  @tornado.gen.coroutine
  def start(self): 
    print ("register worker starts...", self._interval)     
    while True:
      try:
        if self._isRegistered == False: 
          self._node["event"]="register"  
          yield self._mp.put(self._node)
          print ("register self to server", self._node)
          Logger.getLogger().info('Start register self to server: %s_%s:%d', self._node["id"], self._node["host"], int(self._node["port"]))

        else:
          pass    
      except:
        pass
      finally:
        yield tornado.gen.sleep(self._interval)
        
  def handle(self, data):
    done=False
    jsonret = json.loads(data.decode())
    Logger.getLogger().info('Register returned from server: %d', jsonret["status"])

    if jsonret["status"] == StatusCode.OK:
      self._isRegistered = True
    else:
      pass
                      
class Health(object):
    
  def __init__(self, p_server, p_node):
    self._comm = p_communicator

  def __call__(self):
    print ("start send health info...")
    if self._comm.isRegistered() == True:
      pass    
  
  def handle(self, data):
    print ('health handle recived from the server: ', data)