import sublime_plugin, sublime, sys, os
from sublime import Region
from functools import partial
from Customizations.Settings import Settings




# User settings from User/Customizations.sublime-settings
user_settings = None




def plugin_loaded():
	global user_settings
	user_settings = Settings()
	user_settings.load()




# For use after split_selection_into_lines to remove selection lines that are just whitespace
class RemoveWhiteSpaceSelectionLinesCommand(sublime_plugin.TextCommand):
	""" Remove selection lines that are only whitespace """
	def run(self, edit, **kwargs):
		view = self.view
		sels = view.sel()
		new_sels = []

		for sel in sels:
			substr = view.substr(view.line(sel.begin())).strip()
			if substr:
				new_sels.append(sel)

		sels.clear()
		sels.add_all(new_sels)




# A keybinding to side_bar_rename
class CRename(sublime_plugin.ApplicationCommand):
	def run(self):
		window = sublime.active_window()
		view = window.active_view()
		file_name = view.file_name()

		if file_name and os.path.exists(file_name):
			args = { 'paths': [file_name] }
			window.run_command('side_bar_rename', args)