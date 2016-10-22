import unittest
from  vswebsoket.http import HttpRequest, HttpResponse

http_request = "GET /chat HTTP/1.1\r\n" + \
	"Host: server.example.com\r\n" + \
	"Upgrade: websocket\r\n" + \
	"Connection: Upgrade\r\n" + \
	"Sec-WebSocket-Key: x3JJHMbDL1EzLkh9GBhXDw==\r\n" + \
	"Sec-WebSocket-Protocol: chat, superchat\r\n" + \
	"Sec-WebSocket-Version: 13\r\n" + \
	"Origin: http://example.com\r\n\r\n"

http_response = "HTTP/1.1 101 Switching Protocols\r\n" + \
	"Upgrade: websocket\r\n" + \
	"Connection: Upgrade\r\n" + \
	"Sec-WebSocket-Accept: HSmrc0sMlYUkAGmm5OPpG2HaGWk=\r\n" + \
	"Sec-WebSocket-Protocol: chat\r\n\r\n"

class HTTPTestCase(unittest.TestCase):

	def setUp(self):
		pass

	def tearDown(self):
		pass

	def test_encode_request(self):
		request = HttpRequest("/chat")
		request.add_header("Host", "server.example.com")
		request.add_header("Upgrade", "websocket")
		request.add_header("Connection", "Upgrade")
		request.add_header("Sec-WebSocket-Key", "x3JJHMbDL1EzLkh9GBhXDw==")
		request.add_header("Sec-WebSocket-Protocol", "chat, superchat")
		request.add_header("Sec-WebSocket-Version", "13")
		request.add_header("Origin", "http://example.com")
		srequest = request.encode()
		assert len(srequest) == len(http_request)

	def test_decode_request(self):
		request = HttpRequest()
		assert request.decode(http_request)
		assert request.method == "GET"
		assert request.path == "/chat"
		assert request.http_version == "HTTP/1.1"
		assert len(request.headers) == 7
		assert request.headers['Host'] == "server.example.com"
		assert request.headers['Upgrade'] == "websocket"
		assert request.headers['Connection'] == "Upgrade"
		assert request.headers['Sec-WebSocket-Key'] == "x3JJHMbDL1EzLkh9GBhXDw=="
		assert request.headers['Sec-WebSocket-Protocol'] == "chat, superchat"
		assert request.headers['Sec-WebSocket-Version'] == "13"
		assert request.headers['Origin'] == "http://example.com"

	def test_encode_response(self):
		response = HttpResponse(101)
		response.add_header("Upgrade", "websocket")
		response.add_header("Connection", "Upgrade")
		response.add_header("Sec-WebSocket-Accept", "HSmrc0sMlYUkAGmm5OPpG2HaGWk=")
		response.add_header("Sec-WebSocket-Protocol", "chat")
		sresponse = response.encode()
		assert len(sresponse) == len(http_response)

	def test_decode_response(self):
		response = HttpResponse()
		assert response.decode(http_response)
		assert response.http_version == "HTTP/1.1"
		assert response.status_code == 101
		assert response.reason_phrase == "Switching Protocols"
		assert len(response.headers) == 4
		assert response.headers['Upgrade'] == "websocket"
		assert response.headers['Connection'] == "Upgrade"
		assert response.headers['Sec-WebSocket-Accept'] == "HSmrc0sMlYUkAGmm5OPpG2HaGWk="
		assert response.headers['Sec-WebSocket-Protocol'] == "chat"

if __name__ == '__main__':
	unittest.main()
