#2020 programming nerd



import socket
import threading # module used for useing threads
import time # module used for delay
import sys # module for connection with exturnal program
import os # mudule for finding server ip
import random # module for finding valid port

data = "<b>--begining of chat--</b>%Eg%v7%8" # temperary veriable for parseing the data from the server

timeBetwenRefresh = 0.2 # Time in second between each time the client asks for data from server

startServerOutput = True

serverRunning = False

HEADER_LEN = 64

MSG_HEADER_LEN = 10

DISSCONECT_MESSAGE = "!DISSCONECT"

dataTemp = ""

hdr = ""

clients = []

def serverInit(ip,port):
	global conn
	s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	s.bind((ip,int(port)))


	s.listen()
	while serverRunning:
		conn,addr = s.accept()
		thread = threading.Thread(target=handle_client,args=(conn,addr))
		thread.start()	

		print(f"[ACTIVE CONNECTIONS] {threading.activeCount()-1}")
	try:
		conn.close()
	except:
		pass

def handle_client(conn,addr):
	global hdr,data,dataTemp
	print(f"[NEW CONNECTION]: {addr}")
	#clients.append({"socket":conn,"ipv4":addr})
	while serverRunning:
		msg_length = conn.recv(HEADER_LEN).decode("utf-8")
		if msg_length:
			#print(conn.recv(2048))
			msg_length = int(msg_length)

			msg = conn.recv(msg_length).decode("utf-8")
			if(msg == DISSCONECT_MESSAGE):
				#client.remove({socket:conn,ipv4:addr})
				break
			elif(msg == "!GET"):
				conn.send(data.encode("utf-8"))

			else:
				dataTemp = ""
				data += msg+"%Eg%v7%8"
				if(len(data.split("%Eg%v7%8"))>12):
					replace = data.split("%Eg%v7%8")[0]+"%Eg%v7%8"
					if(replace!="%Eg%v7%8"):
						print(replace)
						data = data.replace(replace,"")
					
				print(data)
			# for i in range(len(clients)):
			# 	clients[i].get("socket").send(conn.recv(msg_length+HEADER_LEN))
			print(f"[{addr}] {msg}")

class server:
	def __init__(self,ip,port):
		self.ip = ip
		self.port = port
	def startServer(self):
		global serverRunning
		serverRunning = True
		threading.Thread(target=serverInit,args=(self.ip,self.port)).start()
		
	def stopServer(self):
		global serverRunning
		serverRunning = False # shutdown server




class client:
	def __init__(self,url):
		self.ip,self.port = url.split(":")[0],int(url.split(":")[1])
		self.s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		self.s.connect((self.ip,self.port))
	def sendMessage(self,msg):
		message = msg.encode("utf-8")
		msg_length = len(message)
		send_length = str(msg_length).encode("utf-8")
		send_length += b' '*(HEADER_LEN-len(send_length)) 
		self.s.send(send_length)
		self.s.send(message)
		#self.dissconect()
		#print(self.s.recv(2048))
		
	def dissconect(self):
		self.sendMessage(DISSCONECT_MESSAGE)

	def getMessages(self):
		self.sendMessage("!GET")
		self.sendMessage(DISSCONECT_MESSAGE)
		return self.s.recv(2048).decode("utf-8")
		

		
		
if(sys.argv[1] == "-startServ"):
	server = server(sys.argv[2],int(sys.argv[3])) #(sys.argv[2]) = ip) (sys.argv[3]) = port)
	server.startServer()


if(sys.argv[1] == "-getData"):
	client = client(sys.argv[2]) # (sys.argv[2]) = ip)
	print(client.getMessages()) 
	client.dissconect()

if(sys.argv[1] == "-sendData"):
	client = client(sys.argv[2]) #(sys.argv[2]) = ip)
	client.sendMessage(sys.argv[3].replace("%E2%96%88"," ")) #(sys.argv[3]) = message)
	client.dissconect()

if(sys.argv[1] == "-findServIp"):
	ip,port ="",""
	for a in os.popen("ipconfig").read().split("\n"):
		if(a.split(":")[0] == "   IPv4 Address. . . . . . . . . . . "):
			ip = a.split(":")[1].replace(" ","")
			break
	
	while True:
		guessPort = random.randint(1000,9999)
		try:
			startServerOutput = False
			server = server(ip,guessPort) #(sys.argv[2]) = ip) (sys.argv[3]) = port)
			server.startServer()
			server.stopServer()
			print(ip+":"+str(guessPort))
			break
		except:
		 pass
