#!/usr/bin/python
# -*- coding: utf-8 -*-

class Configurator(object):
	'''
	Configuration to generically access configuration properties.
	'''
	
	def __init__(self, with_api=True):
		self._data = {} # empty dict
		
	def register_component(self, component, component_name):
		self._data[component_name] = component
		
	def get(self, component_name, component_property):
		comp = self._data[component_name]
		return getattr(comp, "get_" + component_property)()
	
	def set(self, component_name, component_property, value):
		comp = self._data[component_name]
		setter = getattr(comp, "set_" + component_property)
		setter(value)
		
	def add(self, component_name, component_property, key, value):
		comp = self._data[component_name]
		getter = getattr(comp, "get_" + component_property)
		getter()[key] = value
		
	def append(self, component_name, component_property, value):
		comp = self._data[component_name]
		getter = getattr(comp, "get_" + component_property)
		getter().append(value)
		
	def clear(self, component_name, component_property):
		getter = getattr(comp, "get_" + component_property)
		getter().clear()
	