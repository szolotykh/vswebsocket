from vswebsoket.server import *
from time import sleep

# Main
if __name__ == "__main__":
	server = WSServer("localhost", 8080)
	print "Waiting for client"
	connection = server.accept ()
	print "Client connected"
	try:
		while True:
			message = connection.receive_message()
			if message.type == CLOSE_MESSAGE:
				raise Exception()
			print "Receive: " + message.data
			response = str(int(message.data)*2)
			connection.send_message(response)
			print "Send: " + response
	except:
		connection.close()
		print "Client disconnected"
