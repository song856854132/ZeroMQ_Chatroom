import zmq
import sys
import time
import threading
from tkinter import *
from threading import Thread


HEIGHT = 700
WIDTH = 1000

root=Tk()
root.title("ZeroMQ Chatroom")
root.geometry(f"{WIDTH}x{HEIGHT}")

#set up the console window
textbox = Text(root, bg='#EEEEEE', fg='#00BF20', width = 80, height = 37)
textbox.place(x = 10, y = 10, anchor = NW)

#set up the input field

input_label = Frame(root)
input_label.place(x = 10, y = 660)
Label(input_label, font = ("Arial, 15"), text = "輸入欲傳送的訊息").pack()
inputbox = Entry(root, width = 56)
inputbox.place(x = 200, y = 660)
inputbox.bind("<Key-Return>", lambda x : sendmess(sock1, sys.argv[1], inputbox.get()))
inputbox.focus_set()

#傳給server訊息的socket
context1 = zmq.Context()
sock1 = context1.socket(zmq.REQ)
sock1.connect("tcp://127.0.0.1:5678")
name = str(sys.argv[1])
num = 0

#接收server訊息的socket
context = zmq.Context()

# Define the socket using the "Context"
sock = context.socket(zmq.SUB)

# Define subscription and messages with prefix to accept.
#sock.setsockopt_string(zmq.SUBSCRIBE, "")
sock.connect("tcp://127.0.0.1:5680")


def sendmess(socket , username, text):
	global inputbox
	try:
		command , mess = text.split(" ",1)
		objectname , mess2 = mess.split(" ",1)
		if command == "dm": #私人訊息
			print ("You talked to ["+objectname+"]>"+mess2)
		data = username+" "+text
		socket.send(data.encode())
		message= socket.recv().decode()
		inputbox.delete(0, END)
	except ValueError:
		data = username+" "+text
		socket.send(data.encode())
		message= socket.recv().decode()
		inputbox.delete(0, END)
	

def recvthread(socket , username):
	option1 = "[ALL]"
	socket.setsockopt_string(zmq.SUBSCRIBE,option1)
	option2 = "["+username+"]"
	socket.setsockopt_string(zmq.SUBSCRIBE,option2)
	while True:
		message = socket.recv().decode()
		try:
			_ , mess = message.split(":",1)
			blockcheck , mess2 = mess.split(" ",1)
			if blockcheck == "bl":
				blockwho , mess3 = mess2.split(" ",1)
				if blockwho == username:
					continue
				else:
					print(mess3)
					
			else:
				print(message)
			
		except:
			print(message)

#ensure that the last entry in client is shown
textbox.see("end")
#clear the input field
inputbox.delete(0, END)
        
#makes it so data is sent on pressing of Send buttom
#root.bind("<Return>", send)

#any print statements are printed to the textbox
def redirector(inputStr):
        textbox.insert(INSERT, inputStr)

#print 
sys.stdout.write = redirector

print("User["+str(sys.argv[1])+"] Connected to the chat server.")
#用來接收pub
#running = threading.Event() #用來停止thread
#running.set()
subthread = threading.Thread(target=recvthread, args = (sock, str(sys.argv[1])))
subthread.start()
#start the GUI chatroom
root.mainloop()
#subthread.join()
#context1.term()
#context.term()
