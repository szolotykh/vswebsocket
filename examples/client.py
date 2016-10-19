from vswebsoket.client import *
from time import sleep


# Main
if __name__ == "__main__":
    client = CWsClient()
    connection = client.connect("ws://localhost:8080")
    print "Client connected"
    #try:
    i = 1
    while True:
        connection.send_message(str(i))
        print "Send: " + str(i)
        i = i + 1
        sleep(1)
    #except:
    #    connection.close()
    #    print "Done"
