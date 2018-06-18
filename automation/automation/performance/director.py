# -*- coding: utf-8 -*-

import os
from scrapy.selector import Selector 
from apscheduler.schedulers.background import BackgroundScheduler

from automationsys import Configure
from automation.cast.cookie import CookieHandler
from automation.performance.factory import ActorFactory
from automation.scenario.factory import ScenarioFactory

from automation.performance.script import Sence

class Executor(object):

  def __init__(self, p_scenario):
    self._scenario = ScenarioFactory.build(p_scenario=p_scenario)
    print ("build scenario: ")
    print (self._scenario)
    
  def action(self):
    print ("Action!")  
    schedule =  self._scenario.getSchedule()
    print (schedule)
    if schedule :
      unit = schedule["unit"]
      interval = schedule["interval"]
      
      scheduler = BackgroundScheduler()
      scheduler.add_job(self._scenario.perform, 'interval', seconds=interval)
      scheduler.start()
      try:
        while True:
            time.sleep(2)
      except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
        
    else :
      #Perform once    
      self._scenario.perform()
    
#   def action(self, p_scenelist=None):
#     scene_queue = self._scenario.load(scenelist=p_scenelist)
#     print (scene_queue)
#     driver = Configure.get_chrome_webdriver()
#     for scene in scene_queue:
#       addr = scene.address()
#       print ("get addr: "+addr)
#       driver.get(addr)
#       #driver.implicitly_wait(5)
#       driver.set_window_size(1280, 700)
#       scene.start()
#       scene.join()
#       #CookieHandler.populate_cookies()
      

class Translator(object):

  def __init__(self):
    pass

  @staticmethod
  def populate(p_xml):
    sences = Selector(text=p_xml).xpath("//scene")
    sence_ary = []
    for sence in sences:
      addr = sence.xpath("@href").extract_first()
      actors = sence.xpath("child::actor")
      actor_ary=[]
      for actor in actors:
        selector = actor.xpath(".//selector")
        properties = actor.xpath(".//properties")
        properties_map = {}
        type=actor.xpath("@type").extract_first()
        print ("################")
        print ("Populate scene's actor:")
        print (actor)
        print (type)
        print ("################")
        id=cls=xpath=name=tag=None

        if selector:
          name=selector.xpath(".//name").xpath("@value").extract_first()
          cls=selector.xpath(".//class").xpath("@value").extract_first()
          id=selector.xpath(".//id").xpath("@value").extract_first()
          xpath=selector.xpath(".//xpath").xpath("@value").extract_first()
          tag=selector.xpath(".//tag").xpath("@value").extract_first()
        
        if properties:
          property_items = properties.xpath(".//property")
          for item in property_items:
            pname=item.xpath(".//name//text()").extract_first()
            pvalue=item.xpath(".//value//text()").extract_first()
            properties_map[pname]=pvalue

        actor_ary.append( ActorFactory.find(actor, type, id, cls, xpath, name, tag, properties_map) )
        print (actor_ary)
      thesence = Sence(threadname="Sence", p_addr=addr, p_act_time=None, p_director=None, p_actor_queue=actor_ary)
      sence_ary.append(thesence)
    return sence_ary
