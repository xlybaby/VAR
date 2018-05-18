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
  def write_map_result(p_dir=None, p_file_name=None, p_contents=None):
    driver = Configure.get_chrome_webdriver()
    curl = driver.current_url
    file_path = Configure.get_ouput_dir()
    if p_dir : 
      file_path += "/" + p_dir
      
    if not os.path.exists(file_path):
      os.mkdir(file_path)

    if p_file_name == None:
      p_file_name = "crawl_"+str(uuid.uuid1())+".data"
    print (file_path+"/"+p_file_name)

    ofile = open(file_path+"/"+p_file_name,'ab')
    ofile.write(bytes(curl+"\n", encoding = "utf8"))

    if p_contents:
      for item in p_contents:
        #ofile.write("\n")
        for key in item.keys():
          val = key+": "+item[key]+"\n"
          ofile.write(bytes(val, encoding = "utf8"))

      ofile.close()
