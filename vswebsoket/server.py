
import sys
import socket
from connection import *

class CWsServer:
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

	def WaitForClient (self):
		# Wait for a connection
		# print ("Waiting for client...")
		socket, client_address = self.sock.accept()
		if self.stop:
			socket.close()
			return None
		connection = Connection (socket)
		# print ("Client connected.")
		connection.wait_for_handshake()
		# print ("Http handshake complete.")
		return connection

	def StopWaiting(self):
		self.stop = True
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.connect((self.address, self.port))
		sock.close()
