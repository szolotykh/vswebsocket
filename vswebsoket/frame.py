# *****************************************************
# File name: frame.py
# *****************************************************

# Import
import random

# Frame operation codes
CONTINUATION_FRAME = 0x0
TEXT_FRAME = 0x1
BINARY_FRAME = 0x2
CLOSE_FRAME = 0x8
PING_FRAME = 0x9
PONG_FRAME = 0xA

class Header:
	def decode(self, data):
		byte0 = ord(data[0])
		self.fin = byte0 >> 7
		self.opcode = byte0 & 0x0F

		byte1 = ord(data[1])
		self.maskbit = byte1 >> 7
		self.length = byte1 & 0x7F

	def decode_length(self, data):
			return 1

	def decode_mask(self, mask):
		self.mask = mask

	def encode(self):
		byte0 = self.fin << 7
		byte0 = byte0 | self.opcode
		byte1 = self.maskbit << 7

		length_bytes = []
		if self.length < 126:
			byte1 = byte1 | self.length
		elif self.length < 4095:
			byte1 = byte1 | 126
			length_bytes += [self.length >> 8 & 0xFF]
			length_bytes += [self.length & 0xFF]
		else:
			# frame data to large
			pass

		header_bytes = chr(byte0) + chr(byte1)

		for byte in length_bytes:
			header_bytes += chr(byte)

		if self.maskbit:
			for byte in self.mask:
				header_bytes += chr(byte)
		return header_bytes

# Build header
def build_header(opcode, length, fin = 1, maskbit = 1):
	header = Header()
	header.opcode = opcode
	header.length = length
	header.fin = fin
	header.maskbit = maskbit
	if header.maskbit:
		mask = random.randint(0, 65535)
		header.mask = [mask>>8*i & 0xFF for i in range(0,4)]
	return header

class Frame:
	def __init__(self, header, body):
		self.header = header
		self.body = body

	def encode(self):
		frame_bytes = self.header.encode()

		# Masking body of the frame
		if self.header.maskbit:
			body = ""
			for i in range(0, len(self.body)):
				body += chr(ord(self.body[i]) ^ self.header.mask[i % 4])
			frame_bytes += body
		else:
			frame_bytes += self.body

		return frame_bytes

 # Build frame
def build_frame(opcode, body = "", fin = 1, maskbit = 1):
	header = build_header(opcode, len(body), fin, maskbit)
	return Frame(header, body)


class FrameProcessor:
	def __init__(self, connection):
		self.connection = connection
		self.data = ""

	# Wait for message header
	def wait_for_header(self):
		# Wait for first two bytes of the header
		while len(self.data) < 2:
			self.data += self.connection.recv(1024)

		header = Header()
		header.decode(self.data[0:2])
		self.data = self.data[2:]

		len_bytes = 0
		if header.length == 126:
			len_bytes = 2
		elif header.length == 127:
			len_bytes = 8

		if len_bytes != 0:
			while len(self.data) < nbytes:
				self.data += self.connection.recv(1024)
			header.decode_length(self.data[0:len_bytes])
			self.data = self.data[len_bytes:]

		mask_bytes = 0
		if header.maskbit == 1:
			mask_bytes = 4
			while len(self.data) < mask_bytes:
				self.data += self.connection.recv(1024)
			header.decode_mask(self.data[0:mask_bytes])
			self.data = self.data[mask_bytes:]
		return header

	# Wait for body of the frame
	def wait_for_body(self, header):
		while len(self.data) < header.length:
			self.data += self.connection.recv(1024)

		body = ""
		if header.maskbit:
			for i in range(0, header.length):
				body += chr(ord(self.data[i]) ^ ord(header.mask[i % 4]))
		else:
			body = self.data[0:header.length]

		self.data = self.data[header.length:]
		return body

	# Wait for one frame
	def wait_for_frame(self):
		header = self.wait_for_header()
		body = self.wait_for_body(header)
		return Frame(header, body)

	# Send frame
	def send_frame(self, frame):
		self.connection.sendall(frame.encode ())
