# -*- coding: utf-8 -*-
import sys
import os
import schedule
import time
import threading
import fcntl

from scrapy.selector import Selector 
from automationsys import get_application_root_dir

parent_path = os.path.dirname(sys.path[0])
if parent_path not in sys.path:
  sys.path.append(parent_path)

#from selenium import webdriver
from automation.performance.director import Executor
from automationsys import get_phantomjs_webdriver

global main_in_process
global main_max_process_task_num

def setinprocess(value):
  global main_in_process
  main_in_process = value

setinprocess(False)

def inprocess():
  global main_in_process
  return main_in_process
    
def setmaxprocesstasknum(value):
  global main_max_process_task_num
  main_max_process_task_num = value

setmaxprocesstasknum(1)

def maxprocesstasknum():
  global main_max_process_task_num
  return main_max_process_task_num

def look():
  if not inprocess():
    setinprocess(True)
    """
    Create a scheduler which looking for 'one' new task periodically
    """
    tasks = os.listdir(get_application_root_dir()+"/data/task")
    for file in tasks:
      if not file.startswith("task_") :
        continue
    
      fp = os.path.join(get_application_root_dir()+"/data/task", file)
      if not os.path.isdir(fp) : 
        taskfile = open(fp, "r")
        try:
          fcntl.flock(taskfile, fcntl.LOCK_EX|fcntl.LOCK_NB)
        except:
          continue
        
        datafile = file[0:file.rfind(".")]
        print ( "Start task file: " + fp )
        content = "".join(taskfile.readlines())
        print (content)
        task = Selector(text=content).xpath("//crawl/task")
        print (task)
        if task:
          tid="".join(task.xpath("//id/text()").extract())
          pid="".join(task.xpath("//pid/text()").extract())
          uri="".join(task.xpath("//uri/text()").extract())
          template="".join(task.xpath("//template/text()").extract())
          print (pid+" : "+uri+" : "+template)
        
          script = """
                 <scenario>
           <scene href='%s'>
           <actor type='recording'>
           <selector>
           <id value=''/>
           <name value=''/>
           <tag value=''/>
           <class value=''/>
           <xpath value=''/>
           </selector>
           <properties>
           <property>
           <name>configure</name>
           <value>%s</value>
           </property>
           <property>
           <name>duration</name>
           <value>0</value>
           </property>
           </property>
           <property>
           <name>pid</name>
           <value>%s</value>
           </property>
           <property>
           <name>datafile</name>
           <value>%s</value>
           </property>
           <property>
           <name>taskid</name>
           <value>%s</value>
           </property>
           </properties>
           </actor>
           </scene>
           </scenario>
                 """ % (uri,template,pid,datafile,tid)

          exe = Executor(p_scenario_id=None)
          exe.action(template=script)
        
        taskfile.close()
        os.remove(fp)
      
    setinprocess(False)
    print ("job done!")
  else:
    print ("job is already in processing...")
    
def sendheartbeat():
  pass

def tlook():
  threading.Thread(target=look).start()
 
def tsendheartbeat():
  threading.Thread(target=sendheartbeat).start()
    
schedule.every(2).seconds.do(tlook)
schedule.every(2).seconds.do(tsendheartbeat)

# while True:
#    schedule.run_pending()
#    time.sleep(1)
look()        

get_phantomjs_webdriver().quit()