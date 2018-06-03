# -*- coding: utf-8 -*-

import os
import hashlib

class Util(object):

  @staticmethod
  def writeextracttask(p_scenarioid, p_sceneno, p_pageno, p_uri):
    id = Util.hash(p_uri)  
    
    data = {  "scenarioId": p_scenarioid, "sceneno":p_sceneno, "pageno": p_pageno, "href": p_uri}  
    encoded_data = json.dumps(data).encode('utf-8')
    response = Main.esclient.request( "PUT", 
                                                           "http://test-mhis-service.pingan.com.cn/elasticsearch/u"+str(p_userid)+"_indice_extract/process_task/"+id,
                                                           body=encoded_data,
                                                           headers={"Content-Type":"application/json"})
    
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