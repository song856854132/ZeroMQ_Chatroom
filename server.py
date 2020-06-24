import zmq
from threading import Thread
list1 = []
check_first = []

def binding(list1):
	context1 = zmq.Context()
	sock1 = context1.socket(zmq.REP)
	sock1.bind("tcp://127.0.0.1:5678")
	context = zmq.Context()
	sock = context.socket(zmq.PUB)
	sock.bind("tcp://127.0.0.1:5680")
	while True:
		username , message = sock1.recv().decode().split(" ",1)
		if username not in check_first:   #確認是否第一次進chatting room
			check_first.append(username)
			hello = username + " has joined the chatting room! Welcome~"
			sock.send(hello.encode())
		elif str.lower(message) == "bye": #離開chatting room
			check_first.remove(username)
			bye = username + " has left the chatting room."
			sock.send(bye.encode())
			sock1.send(message.encode())
			continue 
		try:
			command , message2 = message.split(" ",1)
			if command == "dm":  #私訊
				objectname , message3 = message2.split(" ",1)
				data = "["+objectname+"] :"+"["+username+"]>"+message3
				sock1.send(data.encode())
				sock.send(data.encode())
				print(data)
				continue
			elif command == "bl":
				objectname , message3 = message2.split(" ",1)
				data = "[ALL] :"+command+" "+objectname+" "+\
					"["+username+"]>"+message3
				sock1.send(data.encode())
				sock.send(data.encode())
				print(data)
				continue
				
		except:
			data = "[ALL] :" + "["+username+"]>" + message
			sock1.send(data.encode())
			sock.send(data.encode())
			#list1.append(binding_message)
			print(data)

binding_start = (Thread(target=binding,args=(list1, )))
binding_start.start()
