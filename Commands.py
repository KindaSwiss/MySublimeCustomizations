import sublime_plugin
import sublime
import sys
import os
from sublime import Region
from functools import partial
from Customizations.Settings import Settings


# User settings from User/Customizations.sublime-settings
user_settings = None


def plugin_loaded():
	global user_settings
	user_settings = Settings()
	user_settings.load()


class SplitSelectionRemoveEmptyLines(sublime_plugin.TextCommand):
	"""
	Splits lines into selections and subsequent empty line selections
	"""
	def run(self, edit, **kwargs):
		view = self.view
		view.run_command('split_selection_into_lines')
		sels = view.sel()
		new_sels = []

		for sel in sels:
			substr = view.substr(view.line(sel.begin())).strip()
			if substr:
				new_sels.append(sel)

		sels.clear()
		sels.add_all(new_sels)


class CRename(sublime_plugin.ApplicationCommand):
	""" A keybinding to side_bar_rename """

	def run(self):
		window = sublime.active_window()
		view = window.active_view()
		file_name = view.file_name()

		if file_name and os.path.exists(file_name):
			args = { 'paths': [file_name] }
			window.run_command('side_bar_rename', args)
