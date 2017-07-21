#!/usr/bin/python
# -*- coding: utf-8 -*-

import unittest
from configurator import Configurator
from configuration_reader import ConfigurationReader

class TestComponent(object):
	
	def __init__(self):
		self._bla = None # simple value
		self._foo = [] # list
		self._bar = {} # dict
	
	def set_bla(self, value):
		self._bla = value
		
	def get_bla(self):
		return self._bla
	
	def set_foo(self, value):
		self._foo = value
	
	def get_foo(self):
		return self._foo
	
	def get_bar(self):
		return self._bar
		

class TestConfigurationReader(unittest.TestCase):
	
	def test_simple(self):
		test_bla_value = 12
		data = {"test": {"bla": test_bla_value}}
	
		t = TestComponent()
		c = Configurator()
		c.register_component(t, "test")
		
		cr = ConfigurationReader(c, data)
		cr.config_components()
		
		self.assertEquals(test_bla_value, t.get_bla())
		
	def test_list(self):
		test_foo_value = ["a", "b"]
		data = {"test": {"foo": test_foo_value}}
	
		t = TestComponent()
		c = Configurator()
		c.register_component(t, "test")
		
		cr = ConfigurationReader(c, data)
		cr.config_components()
		
		self.assertEquals(test_foo_value, t.get_foo())
		
	def test_two(self):
		test_bla_value = 12
		test_foo_value = ["a", "b"]
		data = {"test": {"foo": test_foo_value, "bla": test_bla_value}}
	
		t = TestComponent()
		c = Configurator()
		c.register_component(t, "test")
		
		cr = ConfigurationReader(c, data)
		cr.config_components()
		
		self.assertEquals(test_foo_value, t.get_foo())
		self.assertEquals(test_bla_value, t.get_bla())

if __name__ == '__main__':
	unittest.main()