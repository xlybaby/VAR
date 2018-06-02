# -*- coding: utf-8 -*-

import os
import urllib3

class HttpConnectionManager(object):

  def __init__(self, p_http):
    self._http = p_http
        
  @staticmethod
  def getConnection():
    http = urllib3.PoolManager()
    con = HttpConnectionManager(p_http=http)    
    return con

  def get(self, p_uri):
    r = self._http.request( 'GET', p_uri )  
    data = None
    if r:
      data = r.data  
      status = r.status
      r.release_conn()
      
    return data    
    
  def close(self):
    self._http.clear()  
    self._http = None