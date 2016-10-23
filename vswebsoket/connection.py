# *****************************************************
# File name: connection.py
# *****************************************************

import hashlib
import base64
import random
import string
import socket
from urlparse import urlparse

from message import *
from http import HttpRequest, HttpResponse


class Connection:
	def __init__(self, socket):
		self.socket = socket
		self.data = ""
		self.message_pocessor = MessageProcessor(self.socket)
		self.receive_message = self.message_pocessor.receive_message
		self.send_message = self.message_pocessor.send_message

	def receive_http(self):
		data = ""
		while True:
			data += self.socket.recv(1024)
			if "\r\n\r\n" in data:
				return data

	def generate_accept (self, key):
		GUID = "258EAFA5-E914-47DA-95CA-C5AB0DC85B11"
		sha = hashlib.sha1()
		sha.update(key+GUID)
		return base64.b64encode(sha.digest())

	# Handshake
	def send_handshake_request(self, origin, path = ""):
		request = HttpRequest(path)
		request.add_header("Origin", origin)
		#WebSocket version
		request.add_header("Sec-WebSocket-Version","13")
		# WebSocket key
		key = ''.join(random.choice(string.printable) for ch in range(16))
		request.add_header("Sec-WebSocket-Key", base64.b64encode(key))
		self.socket.sendall(request.encode())

	def receive_handshake_request(self):
		srequest = self.receive_http()
		request = HttpRequest()
		request.decode(srequest)
		return request

	def send_handshake_response(self, key):
		response = HttpResponse()
		response.add_header("Upgrade", "websocket")
		response.add_header("Connection", "Upgrade")
		response.add_header("Sec-WebSocket-Accept", self.generate_accept(key))
		self.socket.sendall(response.encode())

	def receive_handshake_response(self):
		sresponse = self.receive_http()
		response = HttpResponse()
		response.decode(sresponse)
		return response

	# Client side of handshake
	def make_handshake(self, origin, path = ""):
		self.send_handshake_request(origin, path)
		self.receive_handshake_response()
		return True

	# Server Side of handshake
	def wait_for_handshake(self):
		request = self.receive_handshake_request()
		print request.headers
		key = request.headers['Sec-WebSocket-Key']
		self.send_handshake_response(key)
		return True

	def close(self):
		self.message_pocessor.send_close()
		self.socket.close()

	def __del__(self):
		self.socket.close()
