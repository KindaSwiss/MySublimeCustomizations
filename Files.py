import os
import sys
import sublime
import sublime_plugin

from sublime import Region
from collections import defaultdict
from Customizations.Settings import Settings
from Customizations.Utils import all_views


# User settings from User/Customizations.sublime-settings
user_settings = None
view_sizes = defaultdict(int)


def plugin_loaded():
	global user_settings
	user_settings = Settings()
	user_settings.load()
	view = sublime.active_window().active_view()
	set_file_size_status(view)
	set_file_saved_status(view)


def set_file_size_status(view):
	""" Set the file size in the status bar """

	file_size = len(view.substr(Region(0, view.size())).encode('utf-8'))
	view.set_status(
			'file_size',
			'{0:.2F} KB'.format(file_size / 1000)
		)

def set_file_saved_status(view):
	"""
	Displays "Unsaved" in the status bar when file is unsaved
	or nothing if saved.
	"""

	view.set_status(
			'file_saved',
			'Unsaved' if view.is_dirty() else ''
		)


class EventListener(sublime_plugin.EventListener):

	def on_activated_async(self, view):
		view_id = view.id()
		view_size = view.size()
		view_sizes[view_id] = view_size

		set_file_size_status(view)
		set_file_saved_status(view)

	def on_modified_async(self, view):
		view_id = view.id()
		view_size = view.size()

		# Only update the file size status if more than n characters
		# have been added or deleted
		if abs(view_sizes[view_id] - view_size) > user_settings.get('character_count'):
			view_sizes[view_id] = view_size
			set_file_size_status(view)

		set_file_saved_status(view)

	def on_post_save_async(self, view):
		set_file_saved_status(view)

	def on_load_async(self, view):
		set_file_size_status(view)

		if view.file_name():
			# Set vagrant files to Ruby syntax
			basename = os.path.basename(view.file_name())

			if basename == 'Vagrantfile':
				view.set_syntax_file('Packages/Ruby/Ruby.tmLanguage')

	def on_window_command(self, window, command_name, args):
		# Close a file when it is deleted from the sidebar
		# using the SideBarEnhancements delete command
		if command_name == 'side_bar_delete':
			files = args['paths']

			for view in all_views():
				if view.file_name() in files:
					view.set_scratch(True)
					window.focus_view(view)
					window.run_command('close_file')
