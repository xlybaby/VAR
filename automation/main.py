# -*- coding: utf-8 -*-
import sys,os,getopt

import schedule
import time
import threading
import fcntl

from scrapy.selector import Selector 
#from selenium import webdriver
parent_path = os.path.dirname(sys.path[0])
if parent_path not in sys.path:
  sys.path.append(parent_path)
    
from automationsys import Configure        
from automation.performance.director import Executor

def init(p_config, p_out):
  setinprocess(False)
  setmaxprocesstasknum(1)
  
  schedule.every(2).seconds.do(tlook)
  schedule.every(2).seconds.do(tsendheartbeat)
  
  Configure.setconfig(p_dir = p_config)
  Configure.setoutput(p_dir = p_out)
  
global main_in_process
global main_max_process_task_num

def setinprocess(value):
  global main_in_process
  main_in_process = value

def inprocess():
  global main_in_process
  return main_in_process
    
def setmaxprocesstasknum(value):
  global main_max_process_task_num
  main_max_process_task_num = value

def maxprocesstasknum():
  global main_max_process_task_num
  return main_max_process_task_num

def look2(p_url):
  script = """
                        <scenario>
                           <scene href='%s'>
                             <actor type='screen'>
                             </actor>
                           </scene>
                        </scenario>
                       """ % (p_url)
  print (script)                       
  exe = Executor(p_scenario_id=None)
  exe.action(template=script) 
  
def look():
  if not inprocess():
    setinprocess(True)
    """
    Create a scheduler which looking for 'one' new task periodically
    """
    tasks = os.listdir(Configure.get_application_root_dir()+"/task")
    for file in tasks:
      if not file.startswith("task_") :
        continue
    
      fp = os.path.join(Configure.get_application_root_dir()+"/task", file)
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
        
          script =  """
               <scenario>
         <scene href='%s'>
         <actor type='recordingkv'>
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
    
def main(argv):
  try:
      opts, args = getopt.getopt(argv,"hc:o:",["config=","output="])
      print (opts)
      print (args)
      if not opts:
        print ('Missing required parameters: main.py -c <configfile> -o <outputfile>')
        sys.exit(2)
        
  except getopt.GetoptError:
    print ('main.py -c <configfile> -o <outputfile>')
    sys.exit(2)
  
  configdir=None
  outputdir=None
     
  for opt, arg in opts:
      if opt == '-h':
         print ('usage: main.py -c <configfile> -o <outputfile>')
         sys.exit()
      elif opt in ("-c", "--config"):
         configdir = arg
      elif opt in ("-o", "--output"):
         outputdir = arg   
            
  init(p_config=configdir, p_out=outputdir)
  try:     
    # while True:
    #schedule.run_pending()
    #    time.sleep(1)   
    look2("http://drugs.dxy.cn/index.htm")      
  finally:   
    Configure.get_chrome_webdriver().quit()  
      
if __name__ == "__main__":
   main(sys.argv[1:])