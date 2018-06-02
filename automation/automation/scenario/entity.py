# -*- coding: utf-8 -*-
from automation.performance.taskparser import JSONParser

class Scenario(object):

  def __init__(self, p_scenario):
    self._type = None
    self._id = None
    self._title = None
    self._schedule = None
    self._user = None
    self._scenes = None
    self._maxduration = 5*60#seconds
    self._maxthreads = None
    self._ini_(p_scenario = p_scenario)

  def perform(self, p_pageno=0):
    pass

  def load(self, scenelist=None):
    if not scenelist:
      raise Exception("Scene list is none!")
  
    self._parser = JSONParser(scenelist)
    #sence_queue = Translator.populate(script)

  def getSchedule(self):
    return self._schedule    

  def getScenes(self):
    #return self._parser.getScenes()
    return self._scenes

  def getId(self):
    return self._id

  def getType(self):
    return self._type

  def getUser(self):
    return self._user
  
  def getDuration(self):
    return self._maxduration

  def getThreadnum(self):
    return self._maxthreads

  def _ini_(self, p_scenario):
    if "scenarioType" in p_scenario :
      self._type = p_scenario["scenarioType"] 
      
    if "scenarioId" in p_scenario :  
      self._id = p_scenario["scenarioId"] 
      
    if "title" in p_scenario :
      self._title = p_scenario["title"]
      
    if "schedule" in p_scenario :
      self._schedule = p_scenario["schedule"]
      
    if "user" in p_scenario :
      self._user = p_scenario["user"]
      
    if "scenelist" in p_scenario :
      self._scenes = p_scenario["scenelist"]
      
    if "maxDuration" in p_scenario :
      self._maxduration = p_scenario["maxDuration"]
      print (self._maxduration)
      
    if "maxThreadNum" in p_scenario :
      self._maxthreads = p_scenario["maxThreadNum"]
      print (self._maxthreads)