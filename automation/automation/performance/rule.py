# -*- coding: utf-8 -*-

import urllib3
from urllib.robotparser import RobotFileParser

class CrawlController(object):
    
  def __init__(self):
    self._rp=RobotFileParser()
    
  def allow(self, p_robots_uri, p_target_uri):
    http = urllib3.PoolManager()    
    r=http.request('GET', p_robots_uri)
    if r.data:
      self._rp.parse(r.data.decode('utf-8').splitlines())
      return rp.can_fetch('*', p_target_uri)
    return True