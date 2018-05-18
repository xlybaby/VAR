# -*- coding: utf-8 -*-

import uuid

from automationsys import Configure

class ListComponentDisplayItem(object):
    
  def __init__(self, p_component, p_label, p_labelattr, p_valueattr, p_parent=None, p_islink=False, p_nextpagelink=None, p_linkextract=False, p_ignore=None,p_nextpagetemp=None ):
    self._parent = p_parent
    self._label = p_label
    self._labelattr = p_labelattr
    self._valueattr = p_valueattr
    self._islink = p_islink
    self._nextpagelink = p_nextpagelink
    self._linkextract = p_linkextract
    self._component = p_component
    self._ignore = p_ignore
    self._nextpagetemp = p_nextpagetemp
    '''
  def items_from_tag(self, p_tag, index=None):
    if index:
      items = self._parent.xpath(".//"+p_tag+"["+str(index)+"]")
    else: 
      items = self._parent.xpath(".//"+p_tag)

    return  self.collect(items)

  def items_from_xpath(self, p_xpath):
    items = self._parent.xpath(p_xpath)
    return  self.collect(items)


  def items_behind_label(self, p_label):
    pass
    '''
  def getxpath(self):
    return self._component.xpath()

  def getInstance(self, p_selector):
    return self._component.select_elements_relatively(p_selector=p_selector)

  def getindex(self):
    return self._component.getindex()

  def collect(self, p_items, p_tid=None):
    item_collect = []
    print ("item start collect......")
    
    if None == p_items:
      return item_collect
    uid = str(uuid.uuid1().int)

    for idx, item in enumerate(p_items):
      item_map = {}
      item_map["item_id"] = uid+"_"+str(idx)

      if self._label:
        key = self._label
      elif self._labelattr:
        key = item.xpath("@"+self._labelattr).extract_first()
      else:
        key = str(idx)

      if self._valueattr:
        value = item.xpath("@"+self._valueattr).extract_first()
      else:
        value = item.xpath("string()").extract_first()
      
      if self._ignore:
        #print (value)
        if cmp(value,self._ignore) == 0:
          continue

      if not value:
        continue
    
      try:  
        #print key+": "+value
        #item_map[key.encode("utf-8")] = value.encode("utf-8")
        #item_map[key] = value
        item_map["label"] = key
        item_map["value"] = value
        
        href=""
        if self._islink == "True":
          href= item.xpath("@href").extract_first()
          if self._nextpagelink:
            item_map["next"] = self._nextpagelink
          else:
            item_map["next"] = href
          if self._linkextract  == "True":
            #print ("need submit extract link")
            self.submit(item_map["next"], item_map["item_id"], self._nextpagetemp, p_tid)
      
        item_collect.append(item_map)
      except Exception as e:
        print("Unexpected Error: {}".format(e))
    return  item_collect

  def submit(self, uri, pid, template, tid):
    taskfile = open(Configure.get_application_root_dir()+"/task/task_"+pid+".xml", "ab")
    content = """
                    <crawl>
                        <task>
                            <pid>%s</pid>
                            <uri>%s</uri>
                            <template>%s</template>
                            <id>%s</id>
                        </task>
                    </crawl>
                    """ % (pid, uri, template, tid)
    taskfile.write(bytes(content, encoding = "utf8"))                
    taskfile.close()
           