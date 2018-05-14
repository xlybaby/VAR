#-*-coding:utf-8-*-

from automation.cast.assistant import Locator
from automation.cast.input import InputComponent
from automation.cast.click import ClickEvent
from automation.cast.screen import PageCapture
from automation.cast.switch import Changer
from automation.cast.custom import UserScript
from automation.cast.download import FileSave
from automation.performance.loop import Foreach
from automation.cast.recording import PageCrawl

class ActorFactory(object):

  @staticmethod
  def find(p_selector, p_type, p_id, p_class, p_xpath, p_name,p_tag,p_parameters,p_data_model=None):
    if p_type == "input":
      return InputComponent(p_data_model=p_data_model, p_selector=p_selector, p_type=p_type, p_id=p_id, p_class=p_class, p_xpath=p_xpath, p_name=p_name, p_tag=p_tag, p_parameters=p_parameters)

    elif p_type == "click":
      return ClickEvent(p_data_model=p_data_model, p_selector=p_selector,p_type=p_type, p_id=p_id, p_class=p_class, p_xpath=p_xpath, p_name=p_name, p_tag=p_tag, p_parameters=p_parameters)

    elif p_type == "screen":                       
      return PageCapture(p_data_model=p_data_model, p_selector=p_selector,p_type=p_type, p_id=p_id, p_class=p_class, p_xpath=p_xpath, p_name=p_name, p_tag=p_tag, p_parameters=p_parameters)

    elif p_type == "switch":
      return Changer(p_data_model=p_data_model, p_selector=p_selector,p_type=p_type, p_id=p_id, p_class=p_class, p_xpath=p_xpath, p_name=p_name, p_tag=p_tag, p_parameters=p_parameters)
        
    elif p_type == "custom":
      return UserScript(p_data_model=p_data_model, p_selector=p_selector,p_type=p_type, p_id=p_id, p_class=p_class, p_xpath=p_xpath, p_name=p_name, p_tag=p_tag, p_parameters=p_parameters)

    elif p_type == "download":
      return FileSave(p_data_model=p_data_model, p_selector=p_selector,p_type=p_type, p_id=p_id, p_class=p_class, p_xpath=p_xpath, p_name=p_name, p_tag=p_tag, p_parameters=p_parameters)

    elif p_type == "foreach":
      return Foreach(p_data_model=p_data_model, p_selector=p_selector,p_type=p_type, p_id=p_id, p_class=p_class, p_xpath=p_xpath, p_name=p_name, p_tag=p_tag, p_parameters=p_parameters)

    elif p_type == "recording":
      return PageCrawl(p_data_model=p_data_model, p_selector=p_selector,p_type=p_type, p_id=p_id, p_class=p_class, p_xpath=p_xpath, p_name=p_name, p_tag=p_tag, p_parameters=p_parameters)

    else:
      return None