# *****************************************************
# File name: http.py
# *****************************************************

current_http_version = "HTTP/1.1"

status_code_map = {
	101: "Switching Protocols",
	200: "OK",
	400: "Bad Request",
	401: "Unauthorized",
	404: "Not Found",
	405: "Method Not Allowed"
}

class HttpObject(object):
	def __init__(self):
		self.headers = dict()
		self.http_version = current_http_version

	def add_header(self, name, value):
		self.headers[name] = value

	def encode_headers(self):
		sheaders = ""
		for name in self.headers:
			sheaders = sheaders + name + ": " + self.headers[name] + "\r\n"
		return sheaders

	def decode_headers(self, lines):
		self.headers = dict()
		for line in lines:
			pair = line.split(": ", 1)
			if len(pair) != 2:
				return False
			self.headers[pair[0]] = pair[1]
		return True


class HttpRequest(HttpObject):
	def __init__(self, path = ""):
		super(self.__class__, self).__init__()
		self.method = "GET"
		self.path = "*" if not path else path

	def encode(self):
		srequest = "{} {} {}\r\n"\
			.format(self.method, self.path, self.http_version)
		srequest += self.encode_headers()
		srequest += "\r\n"
		return srequest

	def decode(self, srequest):
		lines = srequest.split("\r\n")
		if len(lines) < 3:
			return False

		line = lines[0].split(" ")
		if len(line) != 3:
			return False

		self.method = line[0]
		self.path = line[1]
		self.http_version = line[2]

		# Decode headers
		if not self.decode_headers(lines[1:-2]):
			return False
		return True


class HttpResponse(HttpObject):
	def __init__(self, status_code = 200):
		super(self.__class__, self).__init__()
		self.status_code = status_code
		self.reason_phrase = status_code_map[self.status_code]

	def encode(self):
		sresp = "{} {} {}\r\n".format(self.http_version, self.status_code, self.reason_phrase)
		sresp += self.encode_headers()
		sresp += "\r\n"
		return sresp

	def decode(self, sresp):
		lines = sresp.split("\r\n")
		if len(lines) < 3:
			return False

		line = lines[0].split(" ", 2)
		if len(line) != 3:
			return False

		self.http_version = line[0]
		self.status_code = int(line[1])
		self.reason_phrase = line[2]

		# Decode headers
		if not self.decode_headers(lines[1:-2]):
			return False
		return True
