# -*- coding: utf-8 -*-
from automation.scenario.banner import Banner
from automation.scenario.corpus import CorpusCollect
from automation.scenario.ranker import RankList
from automation.scenario.subscriber import RefreshBlock
from automation.scenario.timeseries import Timeseries

class ScenarioFactory(object):

  @staticmethod
  def build(p_scenario):
    scenario_type = p_scenario["scenarioType"]; 
    
    if scenario_type == 1:
      return Banner(p_scenario)
  
    elif scenario_type == 2:
      return RefreshBlock(p_scenario)

    elif scenario_type == 3:                       
      return RankList(p_scenario)

    elif scenario_type == 4:
      return Timeseries(p_scenario)
        
    elif scenario_type == 5:
      return CorpusCollect(p_scenario)

    else:
      return None
   
