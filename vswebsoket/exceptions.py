# *****************************************************
# File name: exceptions.py
# *****************************************************

class WebSocketError(RuntimeError):
	def __init__(self, arg):
		self.args = arg
