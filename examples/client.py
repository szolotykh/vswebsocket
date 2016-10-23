from vswebsoket.client import *
from time import sleep

# Main
if __name__ == "__main__":
	client = WSClient()
	connection = client.connect("ws://localhost:8080")
	print "Connected"
	try:
		i = 1
		while True:
			connection.send_message(str(i))
			print "Send: " + str(i)

			message = connection.receive_message()
			if message.type == CLOSE_MESSAGE:
				raise Exception()
			print "Receive: " + message.data
			i = i + 1
			sleep(1)
	except:
		connection.close()
		print "Disconnected"
