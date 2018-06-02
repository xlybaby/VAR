# -*- coding: utf-8 -*-

import os
import hashlib

class Util(object):

  @staticmethod
  def getabsurl(p_location, p_uri):
    if not p_location:
      return p_uri
      
    if not p_uri.startswith("http://"):
        if not p_uri.startswith("/"):
          if p_uri.startswith("./"):
            return p_location+"/"+p_uri[2:]         
          else:
            if p_uri.startswith("?"):
              return p_location+p_uri
            else:
              return p_location+"/"+p_uri
        else:
          if p_location.find("/", 8) >= 0:  
            return p_location[0:p_location.find("/", 8)] + p_uri     
          else:
            return p_location + p_uri     
    else:
      return p_uri
  
  @staticmethod
  def hash(p_content):  
    data=hashlib.sha224(p_content.encode(encoding='UTF-8'))
    return data.hexdigest()    