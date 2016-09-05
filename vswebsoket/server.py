
import sys
import socket
from client import *

class CWsServer:
	def __init__ (self, address, port):
		# Create a TCP/IP socket
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		# Bind the socket to the port
		self.sock.bind((address, port))
		# Listen for incoming connections
		self.sock.listen(1)

	def WaitForClient (self):
		# Wait for a connection
		print ("Waiting for client...")
		connection, client_address = self.sock.accept()
		client = Client (connection)
		print ("Client connected.")
		client.handshake()
		print ("Http handshake complete.")
		return client
	
	
	
	