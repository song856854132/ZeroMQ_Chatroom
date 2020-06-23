import zmq
import sys
import time
from tkinter import *
from threading import Thread

class clientUI(): 

    def __init__(self):
    #set up base window
        HEIGHT = 700
        WIDTH = 1000
        
        self.root=Tk()
        self.root.title("ZeroMQ Chatroom")
        self.root.geometry(f"{WIDTH}x{HEIGHT}")

        self.frame = [Frame(),Frame(),Frame(),Frame()]

        #set up the textbox scroll
        self.textboxScrollBar = Scrollbar(self.frame[0])
        self.textboxScrollBar.pack(side = RIGHT, fill = Y)
        #textbox to show message
        self.textbox = Listbox(self.frame[0],width = 900, height = 500)
        self.textbox=Text(self.root, bg='#080808', fg='#00BF20')
        self.textbox['yscrollcommand'] = self.textboxScrollBar.set
        self.textbox.pack(fill=BOTH, expand=True)
        self.textboxScrollBar['command'] = self.textbox.yview()  
        self.frame[0].pack(expand=1,fill=BOTH)

        label = Label(self.frame[1],height=2)  
        label.pack(fill=BOTH)  
        self.frame[1].pack(expand=1,fill=BOTH)  
        #set up the inputbox scroll
        self.inputboxScrollBar = Scrollbar(self.frame[2])  
        self.inputboxScrollBar.pack(side=RIGHT,fill=Y) 
        #inputbox
        self.inputbox = Text(self.frame[2],width=900,height=100)  
        self.inputbox['yscrollcommand'] = self.inputboxScrollBar.set  
        self.inputbox.pack(expand=1,fill=BOTH)  
        self.inputboxScrollBar['command'] = self.inputbox.yview()  
        self.frame[2].pack(expand=1,fill=BOTH)  
            
        #Send message buttom
        self.sendButton=Button(self.frame[3],text=' Send ',width=10,command=self.sendingMessage)  
        self.sendButton.pack(expand=1,side=BOTTOM and RIGHT,padx=15,pady=8)  
            
        #Close program buttom
        self.closeButton=Button(self.frame[3],text=' Close ',width=10,command=self.close)  
        self.closeButton.pack(expand=1,side=RIGHT,padx=15,pady=8)  
        self.frame[3].pack(expand=1,fill=BOTH)  

    def sendingMessage(self):
        context1 = zmq.Context()
        sock1 = context1.socket(zmq.REQ)
        sock1.connect("tcp://127.0.0.1:5678")
        name = str(sys.argv[1])
        num = 0
        
        # Send a "message" using the socket
        sock1.send_string("["+str(sys.argv[1])+"]: " + input("["+str(sys.argv[1])+"]>"))
        sent_message = (sock1.recv().decode())
        num = num +1
        self.after(1000,sendingMessage)

    def receivingmessage(self):
        context = zmq.Context()

        # Define the socket using the "Context"
        sock = context.socket(zmq.SUB)

        # Define subscription and messages with prefix to accept.
        sock.setsockopt_string(zmq.SUBSCRIBE, "")
        sock.connect("tcp://127.0.0.1:5680")
        
        message= sock.recv().decode()
        if message.find("["+str(sys.argv[1])+"]: "):
            print("\n"+message+"\n["+str(sys.argv[1])+"] ") 
        self.after(1000,receivingMessage)


    def sendingThread(self):
        sending_input = Button(self.root, text='Send', command = Thread(target=self.receivingmessage,args=( )))
        sending_input.start()
    def receivingThread(self):
        sending_message = (Thread(target=self.sendingMessage,args=( )))
        sending_message.start()
    def close(self):
        sys.exit()
            


def main():
    client = clientUI()
    #print("User["+str(sys.argv[1])+"] Connected to the chat server.")
    client.sendingThread()
    client.receivingThread()
    client.root.mainloop()

if __name__ == '__main__':
    main()
