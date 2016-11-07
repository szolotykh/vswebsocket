# *****************************************************
# File name: server.py
# *****************************************************

import sys
import socket
from connection import *

class WSServer(object):
	def __init__ (self, address, port):
		self.address = address
		self.port = port
		# Create a TCP/IP socket
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		# Bind the socket to the port
		self.sock.bind((self.address, self.port))
		# Listen for incoming connections
		self.sock.listen(3)

		self.stop = False

	def accept (self):
		# Wait for a connection
		socket, client_address = self.sock.accept()
		if self.stop:
			socket.close()
			return None
		connection = Connection (socket, "server")
		connection.wait_for_handshake()
		return connection

	def interrupt_accept(self):
		self.stop = True
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.connect((self.address, self.port))
		sock.close()
