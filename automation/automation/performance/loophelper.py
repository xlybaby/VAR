#-*-coding:utf-8-*-

import os
import importlib

import automation.performance.factory

class ForeachHelper(object):

  @staticmethod
  def loadData(p_selector):
    data = p_selector.xpath(".//data")
    properties = p_selector.xpath(".//properties")
    columns = p_selector.xpath(".//map")
    index=1

    properties_map = {}
    columns_map = {}
    if properties:
      property_items = properties.xpath(".//property")
      for item in property_items:
        name=item.xpath(".//name//text()").extract_first()
        value=item.xpath(".//value//text()").extract_first()
        properties_map[name]=value

    if columns:
      column_items = columns.xpath(".//column")
      for col in column_items:
        colname=col.xpath(".//name//text()").extract_first()
        colref=col.xpath(".//ref//text()").extract_first()
        if colname:
          columns_map[colname]=colref
        else :
          columns_map[index]=colref
          index=index+1;

    clstype = data.xpath("@type").extract_first()
    print ("class type: " + clstype)
    module = importlib.import_module(clstype)
    print (module)
    #cls = getattr(module,"LineReader")
    #print cls
    reader = module.LineReader()
    return reader.fetch(properties_map, columns_map)

  @staticmethod
  def initActors(p_selector,p_data_model=None):
    actor_ary = []
    actors = p_selector.xpath("child::actor")
    for actor in actors:
      selector = actor.xpath(".//selector")
      properties = actor.xpath(".//properties")
      properties_map = {}
      type=actor.xpath("@type").extract_first()
      act = None

      if selector:
        name=selector.xpath(".//name").xpath("@value").extract_first()
        print ("initActors' name: "+ name)
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

      actor_ary.append( factory.ActorFactory.find(actor, type, id, cls, xpath, name, tag, properties_map,p_data_model=p_data_model) )
    
    return actor_ary