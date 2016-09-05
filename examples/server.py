from vswebsoket.server import *
from time import sleep
from utils import VSThread

class KeepAlive(VSThread):
	def __init__(self, client):
		super(KeepAlive, self).__init__()
		self.client = client

	def run (self):
		while not self.stopped():
			client.send_message("Keep alive.")
			sleep(1)

# Main
if __name__ == "__main__":
	server = CWsServer("localhost", 8080)
	client = server.WaitForClient ()
	keep_alive = KeepAlive(client)
	keep_alive.start()
	try:
		while True:
			message = client.wait_message()
			print message.data
			if message.type == CLOSE_MESSAGE:
				raise Exception()
	except:
		keep_alive.stop()
		client.close()