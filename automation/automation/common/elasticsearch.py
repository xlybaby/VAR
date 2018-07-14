# -*- coding: utf-8 -*-

import json
import re
import urllib3

from automation.common.application import Configure

class ESHandler(object):
  
  ESClient=None
  
  @staticmethod
  def ini():  
    ESHandler.ESClient = ESHandler()
        
  def __init__(self):
    esurl = Configure.configure().value("elasticsearch.url")
    poolsize = Configure.configure().value("elasticsearch.pool.maxsize")

    self._es_url = esurl
    self._pool_maxsize = poolsize
    self._es_domain = None
    
    if esurl.startswith("http://") :
       self._es_domain = esurl[7:]   
    elif esurl.startswith("https://") : 
       self._es_domain = esurl[8:]
    
    idx = self._es_domain.find("/")
    self._es_domain = self._es_domain[:idx]    
#     httpexp = re.compile(r'^https?://')
#     httpma = httpexp.search(self._es_url)
#     print (httpma.span())
#     s,e=httpma.span()
#     domain = p_es_url[e:]
#     i = domain.find("/") 
#     if i >= 0:
#       domain=domain[:i]
#     print (domain)
    print ("extract domain",self._es_domain)
    self._es_client = urllib3.HTTPConnectionPool(self._es_domain, maxsize=self._pool_maxsize)
    
  def precise_search(self, p_indice, p_type, p_qry_map=None, p_size=10, p_from=0):
    sizeexp = p_size
    fromexp = p_from
    queryexp = {}
    
    if p_qry_map==None :
      queryexp["match_all"] = {}
      data = {  
               "from" : p_from,
               "size": sizeexp,
               "query": queryexp
                }
    else:
      queryexp = []
      for item in p_qry_map:
        queryexp.append({"match":item})
      data = {
              "from" : p_from,
              "size": sizeexp,
              "query": { 
                "bool": { 
                  "must": queryexp
                 }
                }
              }
    encoded_data = json.dumps(data).encode('utf-8')
    print ("elasticsearch start search", encoded_data)
    response = self._es_client.request( "GET", 
                                            self._es_url+"/"+p_indice+"/"+p_type+"/_search?pretty",
                                            body=encoded_data,
                                            headers={"Content-Type":"application/json"})
    print ("elasticsearch response: ", response.status, response.data)
    if response.status == 200:
      hits = json.loads(response.data.decode('utf-8'))["hits"]
      total = hits["total"]
      if total > 0:
        docs = hits["hits"]
        return docs
    
    return None