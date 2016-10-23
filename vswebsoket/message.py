# *****************************************************
# File name: message.py
# *****************************************************

import frame
from exceptions import WebSocketError

TEXT_MESSAGE = 0x1
BINARY_MESSAGE = 0x2
CLOSE_MESSAGE = 0x8
PING_MESSAGE = 0x9
PONG_MESSAGE = 0xA

MAX_FRAME_COUNT = 10


class Message:
	def __init__(self, type, data):
		self.type = type
		self.data = data

class MessageProcessor:
	def __init__(self, connection, application):
		self.application = application
		self.frame_processor = frame.FrameProcessor(connection)

	def receive_message (self):
		frame_count = 0
		frame_type = 0
		fin = 0

		fm = self.frame_processor.wait_for_frame()
		frame_type = fm.header.opcode
		#if frame_type == CONTINUATION_FRAME:
		#	raise WebSocketError("Wrong frame operation code.")

		if fm.header.fin == 1:
			return Message(fm.header.opcode, fm.body)
		else:
			frame_count += 1
			data = fm.body
			while True:
				fm = self.frame_processor.wait_for_frame()
				data = data + fm.body
				if fm.header.fin:
					return Message(fm.header.opcode, data)
				self.frame_count += 1
				#if self.frame_count > MAX_FRAME_COUNT:
				#	raise WebSocketError("Too many frames")

	def send_message (self, msg):
		fm = frame.build_frame(
			frame.TEXT_FRAME, msg, 1, self.application == "client")
		self.frame_processor.send_frame(fm)

	def send_close (self):
		fm = frame.build_frame(
			frame.CLOSE_FRAME, "", 1, self.application == "client")
		self.frame_processor.send_frame(fm)
