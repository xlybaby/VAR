# -*- coding: utf-8 -*-

import os,sys,re,time
import yaml

class Configure(object):
  conf=None
  
  def __init__(self, p_dir, p_command=None):
    cf = open(p_dir,'r',encoding='utf-8')
    self._configure = yaml.load(cf.read())
    self._command = p_command
    
  @staticmethod
  def load(p_dir, p_command=None):
    Configure.conf=Configure(p_dir=p_dir, p_command=p_command) 
  
  @staticmethod
  def configure():
    return Configure.conf
             
  def value(self, p_key, p_default=None):
    if p_key == None or len(p_key.strip()) == 0 :
      return p_default
    
    if self._command != None and len(self._command) > 0:
      value = self._command[p_key] if p_key in self._command else None
      if value != None:
        return value
    
    keys=p_key.split(".")
    if len(keys) == 0:
      return p_default
    
    if not (keys[0] in self._configure) :
      return p_default
        
    val=self._configure[keys[0]]
    for k in range(1,len(keys)):  
      if not (keys[k] in val) :
        return p_default
      val=val[keys[k]]
      
    return val