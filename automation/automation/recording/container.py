# -*- coding: utf-8 -*-

class ListComponentContainer(object):

  def __init__(self, p_component):
    self._component = p_component
    self._iterators = []
  '''
  def list_collect(self, p_selector=None):
    containers = self.getInstance(p_selector=p_selector)
    if containers:
      container_contents=[]
      for con in containers:
        if p_iterator:
          iterator = ListComponentIterator(con, p_iterator, p_items)
          container_contents.append(iterator.colloct())
        else:
          pass
      return container_contents
    return None
  '''
  def getxpath(self):
    return self._component.xpath()

  def getInstance(self, p_selector) :
    return self._component.select_elements_absolutly(p_selector=p_selector)

  def addIterator(self, p_iter):
    self._iterators.append(p_iter)

  def getIterators(self):
    return self._iterators