#!/usr/bin/python
# -*- coding: utf-8 -*-

import unittest
from configurator import Configurator

class TestComponent(object):
	
	def __init__(self):
		self._bla = None # simple value
		self._foo = [] # list
		self._bar = {} # dict
	
	def set_bla(self, value):
		self._bla = value
		
	def get_bla(self):
		return self._bla
	
	def get_foo(self):
		return self._foo
	
	def get_bar(self):
		return self._bar
		

class TestConfigurator(unittest.TestCase):
	
	def test_set_and_get(self):
		t = TestComponent()
		c = Configurator()
		c.register_component(t, "test")
		va = 42
		c.set("test", "bla", va)
		v = c.get("test", "bla")
		self.assertEquals(va, t.get_bla())
		self.assertEquals(va, v)
		
	def test_append1(self):
		t = TestComponent()
		c = Configurator()
		c.register_component(t, "test")
		va = "blubb"
		c.append("test", "foo", va)
		foo = c.get("test", "foo")
		self.assertEquals(va, foo[0])
		
	def test_append2(self):
		t = TestComponent()
		c = Configurator()
		c.register_component(t, "test")
		va = "blubb"
		c.append("test", "foo", va)
		vb = "quak"
		c.append("test", "foo", vb)
		foo = c.get("test", "foo")
		self.assertEquals(va, foo[0])
		self.assertEquals(vb, foo[1])
		
	def test_add1(self):
		t = TestComponent()
		c = Configurator()
		c.register_component(t, "test")
		
		bar = c.get("test", "bar")
		self.assertEquals({}, bar)
		
		vk = "key"
		vv = "val"
		c.add("test", "bar", vk, vv)
		
		bar = c.get("test", "bar")
		self.assertEquals(vv, bar[vk])
		
	def test_add2(self):
		t = TestComponent()
		c = Configurator()
		c.register_component(t, "test")
		
		bar = c.get("test", "bar")
		self.assertEquals({}, bar)
		
		vk1 = "key"
		vv1 = "val"
		c.add("test", "bar", vk1, vv1)
		
		bar = c.get("test", "bar")
		self.assertEquals(vv1, bar[vk1])
		
		vk2 = "foo"
		vv2 = "bar"
		c.add("test", "bar", vk2, vv2)
		
		bar = c.get("test", "bar")
		self.assertEquals(vv2, bar[vk2])

if __name__ == '__main__':
	unittest.main()