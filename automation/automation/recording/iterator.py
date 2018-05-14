# -*- coding: utf-8 -*-

class ListComponentIterator(object):

  def __init__(self, p_component=None):
    self._component = p_component
    self._items = []
  '''
  def colloct(self):
    iters = self._component.select_elements_relatively(self._parent)
    iterator_value=[]
    for it in iters:
      item_value=[]
      for item in self._items:
        list_item = ListComponentDisplayItem( item["label"], item["labelattr"], item["valueattr"], p_parent=it, p_islink=item["linkextract"],p_nextpagelink=item["nextpagelink"] )
        if item["type"] == "tag":
          item_content=list_item.items_from_tag(p_tag=item["tag"], index=item["index"])
        elif item["type"] == "xpath":
          item_content=list_item.items_from_xpath(p_xpath=item["path"])
        elif item["type"] == "label":
          item_content=list_item.items_behind_label(p_label=item["label"])

        item_value.append(item_content)
      iterator_value.append(item_value)

    return iterator_value
  '''
  def getxpath(self):
    return self._component.xpath()

  def getInstance(self, p_selector) :
    return self._component.select_elements_relatively(p_selector=p_selector)

  def addItem(self, p_item):
    self._items.append(p_item)

  def getItems(self):
    return self._items