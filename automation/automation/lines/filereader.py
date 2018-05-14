#-*-coding:utf-8-*-
import sys
import os

from automationsys import get_ouput_dir
from automationsys import get_application_root_dir

class LineReader(object):

  def __init__(self):
    pass   

  def fetch(self, p_props, p_cols):
    data_list = []
    file_name = p_props["file"]
    #os.chdir("data")
    fileHandle = open(get_application_root_dir()+"/data/"+file_name)

    line = fileHandle.readline()
    while (line != ''):
      record = {}
      cols = line.split(",")
      if len(cols) != len(p_cols):
        raise Exception("Defined column-mapping length not equal data cols' number")
      for idx, key in enumerate(p_cols.keys()):
        ref = p_cols[key]
        if ref:
          record[ref] = cols[idx]
        else :
          record[idx] = cols[idx]
      data_list.append(record)
      line = fileHandle.readline()

    fileHandle.close()
    print "*********************"
    print "Data list: "
    print data_list
    print "*********************"

    return data_list

