import zmq
import sys
from threading import Thread


def sendingMessage():
        context1 = zmq.Context()
        sock1 = context1.socket(zmq.REQ)
        sock1.connect("tcp://127.0.0.1:5678")
        name = str(sys.argv[1])
        num = 0
        while True:
        # Send a "message" using the socket
                sock1.send_string("["+str(sys.argv[1])+"]: " + input("["+str(sys.argv[1])+"]>"))
                sent_message = (sock1.recv().decode())
                num = num +1


def receivingmessage():
        context = zmq.Context()

        # Define the socket using the "Context"
        sock = context.socket(zmq.SUB)

        # Define subscription and messages with prefix to accept.
        sock.setsockopt_string(zmq.SUBSCRIBE, "")
        sock.connect("tcp://127.0.0.1:5680")
        while True:
            message= sock.recv().decode()
            if message.find("["+str(sys.argv[1])+"]: "):
                print("\n"+message+"\n["+str(sys.argv[1])+"] ")        


print("User["+str(sys.argv[1])+"] Connected to the chat server.")
sending_input = (Thread(target=receivingmessage,args=( )))
sending_input.start()

sending_message = (Thread(target=sendingMessage,args=( )))
sending_message.start()

