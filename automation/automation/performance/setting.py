# -*- coding: utf-8 -*-

class UILayout(object):

  def __init__(self, p_scenarioid, p_layoutobj):
    self._scenarioid = p_scenarioid
    self.init(p_layoutobj)
    
  def init(self, p_scheduleobj):
    self._offsetParentLeft= p_scheduleobj["offsetParentLeft"]
    self._offsetParentTop=  p_scheduleobj["offsetParentTop"]
    self._zindex=           p_scheduleobj["zindex"]
    
    self._contentWidth=     p_scheduleobj["contentWidth"]
    self._contentHeight=    p_scheduleobj["contentHeight"]
    
    self._paddingTop=       p_scheduleobj["paddingTop"]
    self._paddingRight=     p_scheduleobj["paddingRight"]
    self._paddingBottom=    p_scheduleobj["paddingBottom"]
    self._paddingLeft=      p_scheduleobj["paddingLeft"]
    
    self._marginTop=        p_scheduleobj["marginTop"]
    self._marginRight=      p_scheduleobj["marginRight"]
    self._marginBottom=     p_scheduleobj["marginBottom"]
    self._marginLeft=       p_scheduleobj["marginLeft"]
    
    self._backgroundColor=  p_scheduleobj["backgroundColor"]
    self._opacity=          p_scheduleobj["opacity"]
    
    self._shadow=           p_scheduleobj["shadow"]
    self._border=           p_scheduleobj["border"]
    self._borderColor=      p_scheduleobj["borderColor"]
    self._borderRound=      p_scheduleobj["borderRound"]
