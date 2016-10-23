# *****************************************************
# File name: client.py
# *****************************************************

import socket
from connection import *
from urlparse import urlparse

class WSClient:
	def __init__ (self):
		pass

	def connect(self, url):
		purl = urlparse(url)
		self.hostname = purl.hostname
		self.path = purl.path
		self.port = 80 if not purl.port else purl.port
		self.scheme = purl.scheme

		# Create a TCP/IP socket
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.sock.connect((self.hostname, self.port))

		origin = self.scheme + "://" + self.hostname + ":" + str(self.port)
		connection = Connection (self.sock)
		connection.make_handshake(origin, self.path)
		return connection
