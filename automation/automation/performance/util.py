# -*- coding: utf-8 -*-

import os
import hashlib
import json
import urllib3

from automationsys import Configure        

class Util(object):
  
  @staticmethod
  def deletedoc(p_indice, p_type, p_id):
    response = Configure.get_es_client().request( "DELETE", 
                                                           "http://test-mhis-service.pingan.com.cn/elasticsearch/"+p_indice+"/"+p_type+"/"+p_id)    
    print (response.status)  
    return response.status

  @staticmethod
  def getoneextracttask(p_indice, p_type):
    data = {
                     "from" : 0, "size" : 1,
                    "query": {
                        "match_all": {}
                    }
                }  
    encoded_data = json.dumps(data).encode('utf-8')
    print ("http://test-mhis-service.pingan.com.cn/elasticsearch/"+p_indice+"/"+p_type+"/_search")
    response = Configure.get_es_client().request( "GET", 
                                                           "http://test-mhis-service.pingan.com.cn/elasticsearch/"+p_indice+"/"+p_type+"/_search",
                                                           body=encoded_data,
                                                           headers={"Content-Type":"application/json"})
    if response.status == 200:
      hits = json.loads(response.data.decode('utf-8'))["hits"]
      total = hits["total"]
      if total > 0:
        docs = hits["hits"]
        id = docs[0]["_id"]
        doc = docs[0]["_source"]
        return (id, doc)
    return (None, None)
#         for idx, doc in enumerate(docs):
#           scenario = doc["_source"]
#           print (scenario)    
          
                
  @staticmethod
  def writeextracttask(p_indice, p_type, p_scenarioid, p_sceneno, p_pageno, p_uri):
    id = Util.hash(p_uri)  
    
    data = {  "scenarioId": p_scenarioid, "sceneno":p_sceneno, "pageno": p_pageno, "href": p_uri}  
    #print (data) 
    #print ("http://test-mhis-service.pingan.com.cn/elasticsearch/"+p_indice+"/"+p_type+"/"+id)
    encoded_data = json.dumps(data).encode('utf-8')
    response = Configure.get_es_client().request( "PUT", 
                                                           "http://test-mhis-service.pingan.com.cn/elasticsearch/"+p_indice+"/"+p_type+"/"+id,
                                                           body=encoded_data,
                                                           headers={"Content-Type":"application/json"})
    print ("write extract: "+str(response.status))
    
  @staticmethod
  def getabsurl(p_location, p_uri):
    if not p_location:
      return p_uri
      
    if not p_uri.startswith("http://"):
        if not p_uri.startswith("/"):
          if p_uri.startswith("./"):
            lidx = p_location.rfind("/")
            return p_location[:lidx]+"/"+p_uri[2:]        
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