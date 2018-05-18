# -*- coding: utf-8 -*-
from automationsys import Configure

class Locator(object):

  @staticmethod
  def find(p_id, p_class, p_xpath, p_name, p_tag):
    driver = Configure.get_chrome_webdriver()
    if p_xpath:
      return driver.find_elements_by_xpath(p_xpath)
    
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

    if len(express) > 0 :
      express="["+express+"]"

    xpath+=express
    return driver.find_elements_by_xpath(xpath)
    
    '''  
    if p_id:
      if p_tag:
        return driver.find_elements_by_xpath("//"+p_tag+"[contains(@id,'"+p_id+"')]")
      else:
        return driver.find_elements_by_id(p_id)
    elif p_class:
      if p_tag:
        return driver.find_elements_by_xpath("//"+p_tag+"[contains(@class,'"+p_class+"')]")
      else:
        return driver.find_elements_by_class_name(p_class)
    elif p_name:
      if p_tag:
        return driver.find_elements_by_xpath("//"+p_tag+"[contains(@name,'"+p_name+"')]")
      else:
        return driver.find_elements_by_name(p_name)
    elif p_tag:
      return driver.find_elements_by_tag_name("//"+p_tag)
    '''
  @staticmethod
  def find_elements_with_id(p_id):
    if p_id == None:
      return None
    driver = Configure.get_chrome_webdriver()
    return driver.find_elements_by_id(p_id)

  @staticmethod
  def find_elements_with_xpath(p_xpath):
    if p_xpath == None:
      return None
    driver = Configure.get_chrome_webdriver()
    return driver.find_elements_by_xpath(p_xpath)

  @staticmethod
  def find_elements_with_name(p_name):
    if p_name == None:
      return None
    driver = Configure.get_chrome_webdriver()
    return driver.find_elements_by_name(p_name)

  @staticmethod
  def find_elements_with_tagname(p_tag):
    if p_tag == None:
      return None
    driver = Configure.get_chrome_webdriver()
    return driver.find_elements_by_tag_name(p_tag)

  @staticmethod
  def find_elements_with_class(p_class):
    if p_class == None:
      return None
    driver = Configure.get_chrome_webdriver()
    return driver.find_elements_by_class_name(p_class)

  @staticmethod
  def find_path():
    return None