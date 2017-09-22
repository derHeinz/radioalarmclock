#!/usr/bin/python
# -*- coding: utf-8 -*-

import unittest
from menu import Menu, MenuItem, FunctionItem, GroupItem, BackItem, SubItem

class BooleanSetter:
	
	def __init__(self, val):
		self._value = val
		
	def get_value(self):
		return self._value
		
	def set_value(self, val):
		self._value = val
		
	def set_true(self):
		self._value = True
		
	def set_false(self):
		self._value = False
	

class TestFunctionItem(unittest.TestCase):

	def test_set_true_false(self):
		# set setting true 
		setter = BooleanSetter(False)
		fi = FunctionItem("test", False, setter.set_true)
		fi.execute()
		self.assertEquals(True, setter.get_value())
		
		# check setting false
		setter = BooleanSetter(True)
		fi = FunctionItem("test", False, setter.set_false)
		fi.execute()
		self.assertEquals(False, setter.get_value())
		
	def test_set_value(self):
		# cehck setting true
		setter = BooleanSetter(False)
		fi = FunctionItem("test", False, setter.set_value, True)
		fi.execute()
		self.assertEquals(True, setter.get_value())
		
		# cehck setting false
		setter = BooleanSetter(True)
		fi = FunctionItem("test", False, setter.set_value, False)
		fi.execute()
		self.assertEquals(False, setter.get_value())
		