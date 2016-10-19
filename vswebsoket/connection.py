import hashlib
import base64
import random
import string
import socket
from urlparse import urlparse

from message import *

class HttpRequest():
	def __init__(self, path):
		self.methrod = "GET"
		self.path = path
		self.headers = dict()

	def add_header(self, name, value):
		self.headers[name] = value

	def encode(self):
		hstr = self.methrod + " " + self.path + " HTTP/1.1\r\n"
		for name in self.headers:
			hstr = hstr + name + ": " + self.headers[name] + "\r\n"
		hstr += "\r\n"
		return hstr

class Connection:
	def __init__(self, socket):
		self.socket = socket
		self.data = ""
		self.message_pocessor = MessageProcessor(self.socket)
		self.wait_message = self.message_pocessor.receive_message
		self.send_message = self.message_pocessor.send_message

	# Handshake
	def get_parameter(self, hstr, pstr):
		big = hstr.find(pstr)
		big = hstr.find(":", big + len(pstr))
		end = hstr.find("\r\n", big + 1)
		value = hstr[big + 1:end]
		value = value.strip()
		return value

	def parse_http_header(self, hstr):
		params = dict()
		params["host"] = self.get_parameter (hstr, "Host")
		params["connection"] = self.get_parameter (hstr, "Connection")
		params["upgrade"] = self.get_parameter (hstr, "Upgrade")
		params["sec-webSocket-version"] = self.get_parameter (hstr, "Sec-WebSocket-Version")
		params["sec-websocket-key"] = self.get_parameter (hstr, "Sec-WebSocket-Key")
		return params

	def send_client_handshake(self, origin, path):
		h = HttpRequest(path)
		h.add_header("Origin", origin)
		#WebSocket version
		h.add_header("Sec-WebSocket-Version","13")
		# WebSocket key
		key = ''.join(random.choice(string.printable) for ch in range(16))
		h.add_header("Sec-WebSocket-Key", base64.b64encode(key))
		print h.encode()
		self.socket.sendall(h.encode())

	def receive_server_handshake(self):
		response = self.receive_http_header()
		print response
		return response


	def receive_http_header(self):
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

	def handshake_response (self, key):
		header = "HTTP/1.1 101 Switching Protocols\r\n"
		header += "Upgrade: websocket\r\n"
		header += "Connection: Upgrade\r\n"
		header += "Sec-WebSocket-Accept: " + self.generate_accept(key) + "\r\n"
		header += "\r\n"
		return header

	def send_handshake_response(self, key):
		header = self.handshake_response (key)
		self.socket.sendall(header)

	def handshake(self):
		header = self.receive_http_header()
		print header
		parameters = self.parse_http_header(header)
		self.send_handshake_response(parameters["sec-websocket-key"])

	def close(self):
		self.message_pocessor.send_close()
		self.socket.close()

	def __del__(self):
		self.socket.close()
