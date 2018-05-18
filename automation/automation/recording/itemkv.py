# -*- coding: utf-8 -*-

class ListComponentDisplayItemKV(object):
    
  def __init__(self):
    self._key = None
    self._value = None
    
  def setkey(self, p_key):
    self._key = p_key
        
  def setvalue(self, p_value):
    self._value = p_value
    
  def getkey(self):
    return self._key
        
  def getvalue(self):
    return self._value  