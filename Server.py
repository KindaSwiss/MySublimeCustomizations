import sublime_plugin, sublime, sys, os, json, socketserver, socket
from sublime import Region

from functools import partial
from threading import Thread

from Customizations.Settings import Settings
from Customizations.Utils import ignore




IS_FAILURE = 0
IS_SUCCESS = 1

ACTION_UPDATE = 2
ACTION_REMOVE = 4
ACTION_RESET = 8

ON_STATUS_BAR = 1




HOST = '127.0.0.1'
PORT = 30048




on_received_callbacks = []





# Add a callback when data is received 
def on_received(callback):
	global on_received_callbacks
	on_received_callbacks.append(callback)




class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
	def __init__(self, server_address, RequestHandlerClass):
		socketserver.TCPServer.__init__(self, server_address, RequestHandlerClass)
		self.clients = []

	def add_client(self, client):
		server.clients.append(client)

	def remove_client(self, client):
		if client in self.clients:
			self.clients.remove(client)

	def send_all(self, data):
		""" Send data to all clients """
		for client in self.clients:
			client.send(data)

	def send(self, data, id_name):
		""" Send data to a specific client """
		for client in self.clients:
			if client.id == id_name:
				client.send(data)

	def close_requests(self):
		""" Close all requests of the server """
		for client in self.clients:
			client.finish()
		self.clients = []




class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):
	""" Server request handler """
	encoding = 'UTF-8'

	def handle(self):
		self.should_receieve = True
		self.closed = False

		with ignore(Exception, message="ThreadedTCPRequestHandler.handle"):
			handshake = json.loads(self.request.recv(2048).decode('UTF-8'))

			if handshake.get('id'):
				self.id = handshake['id']
				self.server.add_client(self)
				print('"{0}"'.format(self.id), 'connected', '- Total number connections:', len(self.server.clients))
			else:
				return self.finish()

			while self.should_receieve:
				data = self.request.recv(2048)
				if not data:
					break
				data = json.loads(data.decode('UTF-8'))

				for callback in on_received_callbacks:
					with ignore(Exception, message="on_received_callbacks"):
						callback(data)

		self.finish()

	def finish(self):
		""" Tie up any loose ends with the request """
		# If the client has not been closed for some reason, close it 
		if not self.closed:
			self.request.close()
		
		# Remove self from list of server clients 
		self.server.remove_client(self)
		self.closed = True
		if not hasattr(self, 'id'):
			return print('Disconnected', '- Total number of connections', len(self.server.clients))
		print('"{0}"'.format(self.id), 'disconnected', '- Total number of connections', len(self.server.clients))

	def send(self, data):
		# Send data to the client 
		with ignore(Exception, message='ThreadedTCPRequestHandler.send'):
			data = sublime.encode_value(data)
			self.request.sendall((data).encode(self.encoding))
			return
		self.finish()




server = None
server_thread = None

def start_server():
	""" Start the server """ 
	global server, server_thread
	if server != None:
		return print('Server is already running')
	server = ThreadedTCPServer((HOST, PORT), ThreadedTCPRequestHandler)
	server_thread = Thread(target=server.serve_forever, daemon=True)
	server_thread.start()
	print('Server started')


def stop_server():
	""" Stop the server """
	global server
	if server == None:
		return print('Server is already shutdown')
	
	server.close_requests()
	server.shutdown()
	server = None
	server_thread = None
	print('Server stopped')




class StartServerCommand(sublime_plugin.ApplicationCommand):
	""" Start the server """
	def run(self):
		sublime.set_timeout_async(start_server, 2000)

	def is_enabled(self):
		return server == None and server_thread != None and not server_thread.is_alive()


class StopServerCommand(sublime_plugin.ApplicationCommand):
	""" Stop the server """
	def run(self):
		stop_server()

	def is_enabled(self):
		return server != None and server_thread != None and server_thread.is_alive()




def plugin_loaded():
	# Setting a timeout will ensure the socket is clear for reuse 
	sublime.set_timeout_async(start_server, 2000)


def plugin_unloaded():
	stop_server()








