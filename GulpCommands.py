import sys, inspect
from Customizations.Utils import ignore, all_views, get_command_name




IS_FAILURE = 0
IS_SUCCESS = 1




class Command(object):
	def name(self):
		return get_command_name(self.__class__.__name__)




class UpdateStatusCommand(Command):
	def run(self, status_id, status):
		for view in all_views():
			view.set_status(status_id, status)




class EraseStatusCommand(Command):
	def run(self, status_id):
		for view in all_views():
			view.erase_status(status_id)




def run_command(command_name, args):
	if not command_name in commands:
		raise Exception('Command not found for command name {0}'.format(command_name))

	command_class = commands[command_name]
	command = command_class()
	command.run(**args)




def handle_received(command):
	with ignore(Exception, origin="handle_received"):
		# print(command)
		command_name = command['command_name']
		data = command['data']

		run_command(command_name, data)




def get_commands():
	""" Get the commands in the current module """
	cmds = {}
	
	for class_name, obj in inspect.getmembers(sys.modules[__name__], inspect.isclass):
		if obj != Command and issubclass(obj, Command):
			cmds[get_command_name(class_name)] = obj
			
	return cmds




commands = get_commands()




def plugin_loaded():
	from Customizations.Server import on_received
	on_received(handle_received)
	





