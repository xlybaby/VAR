#-*-coding:utf-8-*-

from abc import ABCMeta,abstractmethod
from automation.cast.assistant import Locator

class Actor(object):

  __metaclass__ = ABCMeta

  def __init__(self, p_selector, p_type, p_id, p_class, p_xpath, p_name, p_tag, p_data_model=None):
    self._selector=p_selector
    self._type=p_type
    self._comp=None
    self._id=p_id
    self._class=p_class
    self._xpath=p_xpath
    self._name=p_name
    self._tag=p_tag

  def getComponent(self):
    return Locator.find(self._id, self._class, self._xpath, self._name, self._tag)

  def getName(self):
    return self._name

  def getClass(self):
    return self._class

  def getTag(self):
    return self._tag

  def getID(self):
    return self._id

  def getXPath(self):
    return self._xpath

  @abstractmethod
  def getData(self):
    pass

  @abstractmethod  
  def do(self,p_location):  
    pass

  @abstractmethod  
  def duration(self):  
    pass

  @abstractmethod  
  def getProperty(self, p_name):  
    pass

  @abstractmethod  
  def setProperties(self, p_parameters):  
    pass