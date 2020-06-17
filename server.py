import zmq
from threading import Thread
list1 = []


def binding(list1):
    context1 = zmq.Context()
    sock1 = context1.socket(zmq.REP)
    sock1.bind("tcp://127.0.0.1:5678")
    while True:
        binding_message = str(sock1.recv().decode())
        sock1.send_string("Echo: " + binding_message)
        list1.append(binding_message)
        print(list1)
        #q.put(binding_message)
def unbinding(list1):
    context = zmq.Context()
    sock = context.socket(zmq.PUB)
    sock.bind("tcp://127.0.0.1:5680")
    while True:
         while len(list1) != 0:
            message = list1.pop()
            sock.send_string(message)

unbinding_start = (Thread(target=unbinding,args=(list1, )))
unbinding_start.start()

binding_start = (Thread(target=binding,args=(list1, )))
binding_start.start()
