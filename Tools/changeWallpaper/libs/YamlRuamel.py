#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (C) 2019 Stefan Hagmann
import ruamel.yaml

class YamlRuamel():
  """
  wrapper for ruamel - Keeping Comments in YAML FIles
  """
  undefined = object()


  def my_pop(self, key, default=undefined):
    if key not in self:
        if default is self.undefined:
            raise KeyError(key)
        return default
    keys = list(self.keys())
    idx = keys.index(key)
    if key in self.ca.items:
        if idx == 0:
            raise NotImplementedError('cannot handle moving comment when popping the first key', key)
        prev = keys[idx-1]
        # print('prev', prev, self.ca)
        comment = self.ca.items.pop(key)[2]
        if prev in self.ca.items:
            self.ca.items[prev][2].value += comment.value
        else:
            self.ca.items[prev] = self.ca.items.pop(key)
    res = self.__getitem__(key)
    self.__delitem__(key)
    return res
  
  def load(self, yaml_str):
    """
    load Yaml File
    :param yaml_str: can be a string, filepointer
    """
    ruamel.yaml.comments.CommentedMap.pop = self.my_pop
    yaml = ruamel.yaml.YAML()
    data = yaml.load(yaml_str)
    return data


