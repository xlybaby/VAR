# -*- coding: utf-8 -*-

import os
import uuid

from automationsys import Configure

class Storage(object):

  @staticmethod
  def write_file(p_file_name=None, p_contents=None):
    next_urls=[]
    for contents in p_contents:
      for items in contents:
        for item in items:
          for key in item.keys():
            if key == "next":
              next_urls.append({"parent_item_id":item["@item_id@"],"url":item["next"]})
            else:
              open(p_file_name,'ab').write(key + " " + item[key] + "\n")
      open(p_file_name,'ab').write("\n")
    return next_urls

  @staticmethod
  def write_db(p_contents=None):
    pass

  @staticmethod
  def write_array_result(p_dir=None, p_file_name=None, p_contents=None, p_prefix=None, p_suffix=None, p_seperator=None, p_linenum=False):
    if p_dir : 
      file_path = p_dir
    else:
      file_path = Configure.get_ouput_dir()
    if not os.path.exists(file_path):
      os.makedirs(file_path)
      
    if p_file_name == None:
      p_file_name = "crawl_"+str(uuid.uuid1())+".data"
    print (file_path+"/"+p_file_name)  
        
    ofile = open(file_path+"/"+p_file_name,'w', encoding="utf-8")
    if p_contents:
      for idx, content in enumerate(p_contents) :
        if p_linenum :
              ofile.write(str(idx) + "  ")
                
        if p_prefix:
          ofile.write(p_prefix)      
             
        if type(content) == list:  
          for i, item in enumerate(content):  
            if i>0 and p_seperator :
              ofile.write(p_seperator) 
            else:
              ofile.write(" ")    
            ofile.write(item)   
        else :    
          ofile.write(content)   
          
        if p_suffix:
          ofile.write(p_suffix)     
        ofile.write("\n") 
    
    ofile.close()
        
  @staticmethod
  def write_map_result(p_dir=None, p_file_name=None, p_contents=None):
    if p_dir : 
      file_path = p_dir
    else:
      file_path = Configure.get_ouput_dir()
            
    if not os.path.exists(file_path):
      os.mkdir(file_path)

    if p_file_name == None:
      p_file_name = "crawl_"+str(uuid.uuid1())+".data"
    print (file_path+"/"+p_file_name)

    ofile = open(file_path+"/"+p_file_name,'w', encoding="utf-8")

    if p_contents:
      for lines in p_contents:
        #ofile.write("\n")
        ofile.write('{ "items": {')  
        for lidx, item in enumerate(lines):
          if lidx > 0:
            ofile.write( ', ' )  
          id=item["item_id"]
          ofile.write('"'+id+'": {' )
          val=None
          for idx, key in enumerate(item.keys()) :
            if key == "item_id":
              continue  
            if val == None:  
              val = '"' + key+'": "'+item[key]+'"'   
            else:
              val += ', "' + key+'": "'+item[key]+'"' 
          ofile.write(val)
          ofile.write('}')    
        ofile.write(" } }\n") 
      ofile.close()
