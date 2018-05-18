# -*- coding: utf-8 -*-

import os
from scrapy.selector import Selector 

from automationsys import Configure
from automation.cast.cookie import CookieHandler
from automation.performance.factory import ActorFactory
from automation.performance.script import Sence

class Executor(object):

  def __init__(self, p_scenario_id):
    self._scenario_id = p_scenario_id
    self._scenario = Scenario(p_scenario_id)

  def action(self, template=None):
    scene_queue = self._scenario.load(template=template)
    print (scene_queue)
    driver = Configure.get_chrome_webdriver()
    for scene in scene_queue:
      addr = scene.address()
      print ("get addr: "+addr)
      driver.get(addr)
      #driver.implicitly_wait(5)
      driver.set_window_size(1280, 700)
      scene.start()
      scene.join()
      #CookieHandler.populate_cookies()
      
class Scenario(object):

  def __init__(self, p_scenario_id):
    self._scenario_id = p_scenario_id

  def load(self, template=None):
    #script="<scenario><scene href='http://account.autohome.com.cn/'><actor name='' id='UserName' type='text'><lines>d_drive_you_down</lines></actor><actor name='' id='PassWord' type='text'><lines>llcooljb1999</lines></actor><actor name='' id='SubmitLogin' type='click' duration='15'><lines></lines></actor><actor name='' id='' xpath='//*[@id=\"auto-header-login-text\"]/a[1]' type='click' duration='15'><lines></lines></actor><actor name='' id='' type='switch' tourl='i.autohome.com.cn' window='' switch_to='window'><lines></lines></actor><actor name='' id='' xpath='//*[@id=\"usersignInfo\"]/div[@class=\"handle\"]' type='click' duration='15'><lines></lines></actor><actor name='' id='' type='screen'><lines></lines></actor></scene></scenario>"
    #script=u"<scenario><scene href='http://account.autohome.com.cn/'><actor name='' id='UserName' type='text'><lines>d_drive_you_down</lines></actor><actor name='' id='PassWord' type='text'><lines>llcooljb1999</lines></actor><actor name='' id='SubmitLogin' type='click' duration='15'><lines></lines></actor></scene><scene href='http://club.autohome.com.cn/bbs/thread-a-100024-63237851-1.html'><actor type='custom' async='false'><lines>$($('.ke-edit-iframe')[0].contentWindow.document).find('.ke-content')[0].innerHTML='&lt;strong&gt;退一步海阔天空，进一步命根不保&lt;/strong&gt;'</lines></actor><actor name='' id='btnSendKS' type='click' duration='15'><lines></lines></actor></scene></scenario>"
    #script="<scenario><scene href='http://account.autohome.com.cn/'><actor name='' id='UserName' type='text'><lines>d_drive_you_down</lines></actor><actor name='' id='PassWord' type='text'><lines>llcooljb1999</lines></actor><actor name='' id='SubmitLogin' type='click' duration='15'><lines></lines></actor></scene><scene href='http://club.autohome.com.cn/bbs/thread-a-100024-63237851-1.html'><actor name='' id='' type='switch' tourl='' frame_class='ke-edit-iframe' window='' switch_to='frame'><lines></lines></actor></scene></scenario>"
    if not template:
      raise Exception("Template is none!")
    
    script=template
    
    '''
    <scenario>
           <scene href='http://www.medsci.cn/sci/icd-10.asp'>
           <actor type='recording'>
           <selector>
           <id value=''/>
           <name value=''/>
           <tag value='a'/>
           <class value=''/>
           <xpath value=''/>
           </selector>
           <properties>
           <property>
           <name>configure</name>
           <value>COMP_1011.xml</value>
           </property>
           <property>
           <name>duration</name>
           <value>0</value>
           </property>
           </properties>
           </actor>
           </scene>
           </scenario>
    '''

    '''
    <scenario>
           <scene href='http://3a.paic.com.cn/3A-2017-zt.html'>
           <actor type='download'>
           <selector>
           <id value=''/>
           <name value=''/>
           <tag value='a'/>
           <class value='download'/>
           <xpath value=''/>
           </selector>
           <properties>
           <property>
           <name>src_prop</name>
           <value>href</value>
           </property>
           <property>
           <name>duration</name>
           <value>0</value>
           </property>
           </properties>
           </actor>
           </scene>
           </scenario>
    '''
    '''
    script="<scenario>"
           "<scene href='http://3a.paic.com.cn/3A-2017-zt.html'>"
           "<foreach>"
           "<data type='automation.lines.filereader'>"
           "<properties>"
           "<property>"
           "<name>file</name>"
           "<value>ICD-10.csv</value>"
           "</property>"
           "</properties>"
           "<map>"
           "<column>"
           "<name></name>"
           "<ref>DISEASE_NAME</ref>"
           "</column>"
           "</map>"
           "</data>"
           "<actor type='text'>"
           "<selector>"
           "<id value=''/>"
           "<name value='q'/>"
           "<tag value='input'/>"
           "<class value='ipt_text'/>"
           "<xpath value=''/>"
           "</selector>"
           "<properties>"
           "<property>"
           "<name>type</name>"
           "<value>text</value>"
           "</property>"
           "<property>"
           "<name>contents</name>"
           "<value>{{DISEASE_NAME}}</value>"
           "</property>"
           "</properties>"
           "</actor>"
           "<actor type='click'>"
           "<selector>"
           "<id value=''/>"
           "<name value=''/>"
           "<tag value='button'/>"
           "<class value='ipt_sub'/>"
           "<xpath value=''/>"
           "</selector>"
           "<properties>"
           "<property>"
           "<name>duration</name>"
           "<value>10</value>"
           "</property>"
           "</properties>"
           "</actor>"
           "<actor type='collect'>"
           "<selector></selector>"
           "<properties>"
           "<property>"
           "<name>component_id</name>"
           "<value>COMP_1011</value>"
           "</property>"
           "</properties>"
           "</actor>"
           "</foreach>"
           "</scene>"
           "</scenario>"
    '''
    '''
    script=u"""
    <scenario>
            <scene href='http://www.medsci.cn/sci/icd-10.asp'>
            <actor type='foreach'>
            <data type='automation.lines.filereader'>
            <properties>
            <property>
            <name>file</name>
            <value>disease_index_test.csv</value>
            </property>
            </properties>
            <map>
            <column>
            <name></name>
            <ref>DISEASE_NAME</ref>
            </column>
            </map>
            </data>
            <actor type='input'>
            <selector>
            <id value=''/>
            <name value='q'/>
            <tag value='input'/>
            <class value='ipt_text'/>
            <xpath value=''/>
            </selector>
            <properties>
            <property>
            <name>duration</name>
            <value>0</value>
            </property>
            <property>
            <name>type</name>
            <value>text</value>
            </property>
            <property>
            <name>contents</name>
            <value>{{DISEASE_NAME}}</value>
            </property>
            </properties>
            </actor>
            <actor type='input'>
            <selector>
            <id value=''/>
            <name value='classtype'/>
            <tag value='select'/>
            <class value=''/>
            <xpath value=''/>
            </selector>
            <properties>
            <property>
            <name>duration</name>
            <value>0</value>
            </property>
            <property>
            <name>type</name>
            <value>select</value>
            </property>
            <property>
            <name>contents</name>
            <value>ICD-10疾病编码</value>
            </property>
            </properties>
            </actor>
            <actor type='click'>
            <selector>
            <id value=''/>
            <name value=''/>
            <tag value='button'/>
            <class value='ipt_sub'/>
            <xpath value=''/>
            </selector>
            <properties>
            <property>
            <name>duration</name>
            <value>10</value>
            </property>
            </properties>
            </actor>
            <actor type='screen'>
            </actor>
            </actor>
            </scene>
            </scenario>
    """
    '''
    sence_queue = Translator.populate(script)
    return sence_queue

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
