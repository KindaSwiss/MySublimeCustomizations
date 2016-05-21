import sublime
from contextlib import contextmanager

@contextmanager
def ignore(*exceptions, origin="", message="", print_exception=True):
	try:
		yield exceptions
	except exceptions as exs:
		if print_exception:
			print(exs, '- in', origin, 'with message' if message else '', message)

# Return a list of every view from every window
def all_views():
	""" Get all views from every window """
	views = []
	for window in sublime.windows():
		for view in window.views():
			views.append(view)
	return views