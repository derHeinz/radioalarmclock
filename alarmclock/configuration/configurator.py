#!/usr/bin/python
# -*- coding: utf-8 -*-

class Configurator(object):
	'''
	Configuration to generically access configuration properties.
	'''
	
	def __init__(self, with_api=True):
		self._data = {} # empty dict
		
	def register_component(self, component, component_name):
		'''Save a configurable component.'''
		self._data[component_name] = component
		
	def get_component(self, component_name):
		'''Only for special purpose - retrieve the component again.'''
		return self._data[component_name]
		
	def get(self, component_name, component_property):
		'''Get the configured value of the given property for the component name given.'''
		comp = self._data[component_name]
		return getattr(comp, "get_" + component_property)()
	
	def set(self, component_name, component_property, value):
		'''Save a configuration value to a given component'S property.'''
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
	