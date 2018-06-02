# -*- coding: utf-8 -*-
import sys,os
import json
import urllib3

from pip._vendor.requests.models import PreparedRequest

parent_path = os.path.dirname(sys.path[0])
if parent_path not in sys.path:
  sys.path.append(parent_path)
    
from automationsys import Configure        
from automation.performance.director import Executor

class Main(object):
  esclient = None
  
  @staticmethod
  def init(p_udir, p_uout, p_driver):
    Configure.setconfig(p_dir=p_udir)
    Configure.setoutput(p_dir=p_uout)
    Configure.setdriver(p_dir=p_driver)
    Main.esclient = urllib3.HTTPConnectionPool('test-mhis-service.pingan.com.cn', maxsize=10)
    
  @staticmethod
  def submit_user_specified_task_immediately( p_userid, p_scenarioid, p_href=None ):
    data = {  "query": {
                              "match":{
                                  "scenarioId": p_scenarioid
                               }
                   }
                }  
    encoded_data = json.dumps(data).encode('utf-8')
    response = Main.esclient.request( "GET", 
                                                           "http://test-mhis-service.pingan.com.cn/elasticsearch/u"+str(p_userid)+"_indice_base/custom_task/_search?pretty",
                                                           body=encoded_data,
                                                           headers={"Content-Type":"application/json"})
    if response.status == 200:
      hits = json.loads(response.data.decode('utf-8'))["hits"]
      total = hits["total"]
      if total > 0:
        docs = hits["hits"]
        for idx, doc in enumerate(docs):
          scenario = doc["_source"]
          print (scenario)    
          executor = Executor(p_scenario=scenario)
          executor.action()
 
            
  @staticmethod
  def submit_user_specified_task( p_indice, p_type, p_scenarioid, p_scene_index, p_page_index, p_href=None ):
    pass
  
Main.init( p_udir="/usr/local/var/u10000", p_uout="/usr/local/var/base/u10000/output", p_driver="/usr/local/python/webdriver/chromedriver" )                                                                           
Main.submit_user_specified_task_immediately( 10000, "9ead8e44-ac52-40ae-a9d0-39eb68839417" )