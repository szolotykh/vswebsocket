import socket
from connection import *
from urlparse import urlparse

class CWsClient:
	#def __init__ (self, url):

	def connect(self, url):
		purl = urlparse(url)
		self.hostname = purl.hostname
		self.path = "*" if not purl.path else purl.path
		self.port = 80 if not purl.port else purl.port
		self.scheme = purl.scheme

		# Create a TCP/IP socket
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.sock.connect((self.hostname, self.port))

		origin = self.scheme + "://" + self.hostname + ":" + str(self.port)
		connection = Connection (self.sock)
		connection.send_client_handshake(origin, self.path)
		connection.receive_server_handshake()
		return connection
