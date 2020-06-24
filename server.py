import zmq
from threading import Thread
list1 = []
dic = {}

def binding(list1):
	context1 = zmq.Context()
	sock1 = context1.socket(zmq.REP)
	sock1.bind("tcp://127.0.0.1:5678")
	context = zmq.Context()
	sock = context.socket(zmq.PUB)
	sock.bind("tcp://127.0.0.1:5680")
	while True:
		username , message = sock1.recv().decode().split()

		data = "[ALL] :" + "["+username+"]>" + message
		sock1.send(data.encode())
		sock.send(data.encode())
		#list1.append(binding_message)
		print(data)

binding_start = (Thread(target=binding,args=(list1, )))
binding_start.start()
