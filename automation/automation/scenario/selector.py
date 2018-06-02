# -*- coding: utf-8 -*-

class PageElementFinder(object):

  @staticmethod
  def getCompInstance(p_selector, p_element, p_relative=False):
      
    p_xpath = p_element["xpath"] if "xpath" in p_element else None
    p_tag = p_element["tag"] if "tag" in p_element else None
    p_class = p_element["clazz"] if "clazz" in p_element else None
    p_id = p_element["id"] if "id" in p_element else None
    p_name = p_element["name"] if "name" in p_element else None
    p_attrs = p_element["attributes"] if "attributes" in p_element else None
    p_index = p_element["index"] if "index" in p_element else None
    
    if p_xpath:
      xpath = p_xpath

    else:
      if p_relative:  
        xpath=".//";
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
        
    #print(xpath)    
    return p_selector.xpath(xpath)
        