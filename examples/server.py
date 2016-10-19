from vswebsoket.server import *
from time import sleep
from utils import VSThread

class KeepAlive(VSThread):
	def __init__(self, connection):
		super(KeepAlive, self).__init__()
		self.connection = connection

	def run (self):
		while not self.stopped():
			connection.send_message("Keep alive.")
			sleep(1)

# Main
if __name__ == "__main__":
	server = CWsServer("localhost", 8080)
	connection = server.WaitForClient ()
	print "Client connected"
	#keep_alive = KeepAlive(connection)
	#keep_alive.start()
	#try:
	while True:
		message = connection.wait_message()
		print "Receive: " + message.data
		if message.type == CLOSE_MESSAGE:
			raise Exception()
	#except:
		#keep_alive.stop()
		#connection.close()
