# -*- coding: utf-8 -*-
import sys,os
import json

from pip._vendor.requests.models import PreparedRequest

parent_path = os.path.dirname(sys.path[0])
if parent_path not in sys.path:
  sys.path.append(parent_path)
    
from automationsys import Configure        
from automation.performance.director import Executor

class Main(object):
  
  @staticmethod
  def _init(p_usrid, p_udir, p_uout, p_ex, p_driver):
    if not os.path.exists(p_udir):
      os.makedirs(p_udir)
    if not os.path.exists(p_uout):
      os.makedirs(p_uout)
    if not os.path.exists(p_ex):
      os.makedirs(p_ex)
            
    Configure.setconfig(p_dir=p_udir)
    Configure.setoutput(p_dir=p_uout)
    Configure.setextractdir(p_dir=p_ex)
    Configure.setdriver(p_dir=p_driver)
    Configure.set_es_client()
    
  @staticmethod
  def init(p_usrid, p_driver):
    usrbasedir = "/usr/local/var/base/u"+str(p_usrid)
    usroutputdir = usrbasedir+"/output"
    usrextractdir = usroutputdir+"/extract"
    Main._init(p_usrid=p_usrid, p_udir=usrbasedir, p_uout=usroutputdir, p_ex=usrextractdir, p_driver=p_driver)
    
  @staticmethod
  def submit_user_specified_task_immediately( p_userid, p_scenarioid, p_href=None ):
    data = {  "query": {
                              "match":{
                                  "scenarioId": p_scenarioid
                               }
                   }
                }  
    encoded_data = json.dumps(data).encode('utf-8')
    response = Configure.get_es_client().request( "GET", 
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
  
Main.init( p_usrid=10000, p_driver="/usr/local/python/webdriver/chromedriver" )                                                                           
Main.submit_user_specified_task_immediately( 10000, "eab9c721-1c40-4520-b3c5-fe610d82b653" )