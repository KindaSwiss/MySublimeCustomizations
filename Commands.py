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




# Used to trim off trailing whitespace in a selection 
class TrimTrailingWhiteSpaceInSelectionCommand(sublime_plugin.TextCommand):
	""" Trim whitespace off the end of each line in a selection """
	def run(self, edit):
		view = self.view
		view_settings = view.settings()
		sels = [sel for sel in view.sel() if not sel.empty()]

		# Get all whitespace regions
		trailing_white_space_regions = self.view.find_all("[\t ]+$")

		# The regions to trim
		to_trim = []

		# Check if any of the trailing whitespace is in any selection region
		for sel in sels:
			for region in trailing_white_space_regions:
				# Get the regions intersecting the selector region
				if sel.intersects(region):
					to_trim.append(region)
					
		# Erase the regions starting from the last!!1
		to_trim.reverse()

		# This command will trim lines that are just whitespace. 
		# By setting trim_empty_lines to false, lines that are just whitespace will not be trimmed
		trim_empty_lines = user_settings.get('trim_empty_lines') or view_settings.get('trim_empty_lines')
		
		for region in to_trim:

			if not trim_empty_lines:
				line = view.substr(view.line(region.begin())).strip()
				if not line:
					continue
			view.erase(edit, region)




# Naive Sass Convert command to convert SCSS to Sass
class SassConvertCommand(sublime_plugin.TextCommand):
	""" Get rid of all semicolons and opening and closing curly brackets """
	def run(self, edit):
		view = self.view
		view_settings = view.settings()
		sels = [sel for sel in view.sel() if not sel.empty()]

		# Get all whitespace regions
		regions_to_erase = view.find_all("\{|\}|\;")

		# Erase the regions starting from the last!!1
		regions_to_erase.reverse()
		
		for region in regions_to_erase:
			view.erase(edit, region)
		
		view.run_command("trim_trailing_white_space")





