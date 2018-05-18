# -*- coding: utf-8 -*-

from automationsys import Configure
from automation.performance.actor import Actor

class UserScript(Actor):

  def __init__(self, p_selector, p_type, p_id, p_class, p_xpath, p_name, p_tag, p_parameters, p_data_mode=None):
    Actor.__init__(self,p_selector, p_type, p_id, p_class, p_xpath, p_name, p_tag)
    self._selector=p_selector
    self._act_time = None
    self._script = None
    self._async = False
    self.setProperties(p_parameters)
    
  def do(self, p_location=None):
    driver = Configure.get_chrome_webdriver()
    if self._script:
      if not self._async:
        driver.execute_script(script=self._script)
      else:
        driver.execute_async_script(script=self._script)

  def duration(self):
    return self._act_time

  def getProperty(self, p_name):  
    pass

  def getData(self):
    pass

  def setProperties(self, p_parameters):  
    duration = p_parameters["duration"] if p_parameters.has_key("duration") else None
    script = p_parameters["script"]
    async = p_parameters["async"]
    self._script = script
    if duration:
      self._act_time = int(duration)
    if async == "True":
      self._async = True