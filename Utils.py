import sublime
from contextlib import contextmanager




@contextmanager
def ignore(*exceptions, origin="", message="", print_exception=True):
	try:
		yield exceptions
	except exceptions as exs:
		if print_exception:
			print(exs, '- in', origin, 'with message' if message else '', message)




# Return whether all items passed are of a single type 
def all_of_type(items, t):
	""" Check if all items are of a single type """
	a = all([isinstance(item, t) for item in items])
	# print('all_of_type', a, items, t)
	return a




# Return a list of every view from every window 
def all_views():
	""" Get all views from every window """
	views = []
	for window in sublime.windows():
		for view in window.views():
			views.append(view)
	return views




def get_command_name(clsname):
	name = clsname[0].lower()
	last_upper = False
	for c in clsname[1:]:
		if c.isupper() and not last_upper:
			name += '_'
			name += c.lower()
		else:
			name += c
		last_upper = c.isupper()
	if name.endswith("_command"):
		name = name[0:-8]
	return name




def get_views_by_id(ids):
	return [view for view in all_views() if view.id() in (ids if isinstance(ids, list) else [ids])]



