# -*- coding: utf-8 -*-

class Component(object):

  def __init__(self, p_xpath=None, p_class=None, p_id=None, p_tag=None, p_name=None, p_index=None, p_attrs=None):
    self._index = p_index
    
    if p_xpath:
      self._xpath = p_xpath

    else:
      xpath="//";
      express="";
      if p_tag :
        xpath += p_tag
      else:
        xpath += "*"
  
      if p_id :
        express += "contains(@id, '"+p_id+"')"

      if p_name :
        if len(express)>0 :
          express += " and "
        express += "contains(@name, '"+p_name+"')"
    
      if p_class:
        if len(express) > 0 :
          express+=" and "
        express+="contains(@class, '"+p_class+"')"
 
      if p_attrs:
        kvs = p_attrs.split(",")
        for kv in kvs:
          kvpair = kv.split("=")
          if len(express) > 0 :
            express+=" and "
          express+="contains(@"+kvpair[0]+", '"+kvpair[1]+"')"
          
      if len(express) > 0 :
        express="["+express+"]"
          
      xpath+=express

      if p_index:
        xpath += "["+p_index+"]"
        
      self._xpath = xpath

  def xpath(self):
    return self._xpath;

  def select_elements_relatively(self, p_selector):
    if self._xpath:
      xpath = self._xpath
    else :
      return None

    if not xpath.startswith(".//"):
      if xpath.startswith("."):
        xpath = ".//"+xpath[1:]
      elif xpath.startswith("//"):
        xpath = "."+xpath
      else:
        xpath = ".//"+xpath
    
    print (xpath)  
    return p_selector.xpath(xpath)

  def select_elements_absolutly(self, p_selector):
    if self._xpath:
      xpath = self._xpath
    else :
      return None

    if not xpath.startswith("//"):
      xpath = "//"+xpath

    return p_selector.xpath(xpath)

  def getindex(self):
    return self._index