# -*- coding: utf-8 -*-

class ListComponentPagination(object):

  def __init__(self, p_component, p_parent=None):
    self._component = p_component
    self._parent = p_parent
    
  def getxpath(self):
    return self._component.xpath()

  def getInstance(self, p_selector) :
    if self._parent:
      selp = self._parent.select_elements_absolutly(p_selector=p_selector)
      return self._component.select_elements_absolutly(p_selector=selp)

    else:      
      return self._component.select_elements_absolutly(p_selector=p_selector)

  def setParent(self, p_parent):
    self._parent = p_parent