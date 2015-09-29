import sublime_plugin




class SideBarListener(sublime_plugin.EventListener):

	def on_window_command(self, window, command_name, args):
		# Close a file when it is deleted from the sidebar
		if command_name == 'side_bar_delete':
			files = args['paths']

			for view in all_views():
				if view.file_name() in files:
					view.set_scratch(True)
					window.focus_view(view)
					window.run_command('close_file')