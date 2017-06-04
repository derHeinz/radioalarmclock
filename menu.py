#!/usr/bin/python
# -*- coding: utf-8 -*-

class MenuItem(object):
	def __init__(self, name):
		self._name = name
		
	def get_text(self):
		return self._name

class FunctionItem(MenuItem):
	def __init__(self, name, func, use_display):
		super(FunctionItem, self).__init__(name)
		self._function = func
		self._use_display = use_display
		
	def execute(self):
		self._function()
		
class SubItem(MenuItem):
	def __init__(self, name, sub):
		super(SubItem, self).__init__(name)
		self._sub = sub
		
	def return_sub(self):
		return self._sub
		
class GroupItem(MenuItem):
	def __init__(self, name, subitems):
		super(GroupItem, self).__init__(name + ">")
		self._subitems = subitems
		
	def get_menu(self):
		return self._subitems
		
class BackItem(MenuItem):
	def __init__(self):
		super(BackItem, self).__init__("<")


class Menu(object):

	def __init__(self, display, menu):
		
		self._display = display
	
		# when cascading into submenu: store
		self._menustack = []
		self._menuitemstack = []
		
		# prepare variables
		self._menuitems = None
		self._state = None
		
		# initial menu
		self._new_menu(menu)

	
	def _new_menu(self, menu):
		self._menuitems = menu
		self._state = self._menuitems[0] # currently selected object
		self.display()
		
	def _back_menu(self, menu, menuitem):
		self._menuitems = menu
		self._state = menuitem # currently selected object
		self.display()
			
	def display(self):
		self._display.show_text(self._state.get_text())
		
	def next(self):
		self._move(1)
	
	def prev(self):
		self._move(-1)
		
	def select(self):
		if type(self._state) == FunctionItem:
			self._state.execute()
			if (not self._state._use_display):
				self._display.show_text_blinking(self._state.get_text())
				self.display()
			
		if type(self._state) == GroupItem:
			# store old menu and item (stack-like in a list)
			self._menustack.append(self._menuitems)
			self._menuitemstack.append(self._state)
			# replace with new one
			self._new_menu(self._state.get_menu())
		
		if type(self._state) == BackItem:
			last_menu = self._menustack.pop()
			last_menu_item = self._menuitemstack.pop()
			# old menu again
			self._back_menu(last_menu, last_menu_item)
			
		if type(self._state) == SubItem:
			return self._state.return_sub()
		
	def _move(self, steps):
		current_menu = self._menuitems
		current_index = current_menu.index(self._state)
		
		if (current_index < len(current_menu) - steps and (current_index + steps) >= 0):
			self._state = current_menu[current_index + steps]
			self.display()
