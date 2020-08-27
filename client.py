#2020 programming nerd


import requests # module for geting / sending data from server
from bs4 import BeautifulSoup # module for parseing data from server
from http.server import HTTPServer, BaseHTTPRequestHandler # module for creating / managing server
import threading # module used for useing threads
import time # module used for delay
import sys # module for connection with exturnal program
import os # mudule for finding server ip
import random # module for finding valid port

data = '' # temperary veriable for parseing the data from the server

timeBetwenRefresh = 0.2 # Time in second between each time the client asks for data from server

startServerOutput = True

class Serv(BaseHTTPRequestHandler):
	def do_GET(self):
		global data
		if(self.path[:7] == "/?text="): # checks for message post request
			data += "\n"+self.path.split("text=")[1] # adds sent data from client to global database of messages
			pageData = open("format.html").read().replace("//data//",data.replace("%20"," ")) # formatting data for clients computer  
			self.send_response(200) # sends validation response to server
		elif(self.path[:5] == "/?get"): # checks for message get request
			pageData = open("format.html").read().replace("//data//",data.replace("%20"," "))
			self.send_response(200)
		else:
			pageData = "::404::"
			self.send_response(404)# sends invalidation response to server

		self.end_headers() # required http functon
		self.wfile.write(bytes(pageData,'utf-8')) # sends data to client 
	def log_message(self, format, *args):
		return

def serverInit(httpd_,ip,port):
		httpd = httpd_
		if(startServerOutput):
			print("Server Started")
		httpd.serve_forever()

class server:
	def __init__(self,ip,port):
		self.httpd = HTTPServer((ip,int(port)),Serv) # var for HTTP server
		self.x = threading.Thread(target=serverInit,args=(self.httpd,ip,port)) # 'serverInit' thread
		self.ip = ip
		self.port = port
	def startServer(self):
		self.x.start() # start 'serverInit' thread
	def stopServer(self):
		self.httpd.shutdown() # shutdown server




class client:
	def __init__(self,url):
		self.url = url

	def sendMessage(self,message):

		page = requests.get(str(self.url+"/?text="+message),stream=True,timeout=1) # "/?text=" used int url to send data to the server (used before the message)


	def getMessages(self):
		page = requests.get(self.url+"/?get",stream=True,timeout=1) # "/?get" used in url to get data without sending data
		return BeautifulSoup(page.content,'lxml').find("div").text.replace("%E2%96%88"," ").replace("\n","%G2%12%99") # return data parsed and in a list (%E2%96%88 is space keycode)

		
		
if(sys.argv[1] == "-startServ"):
	server = server(sys.argv[2],int(sys.argv[3])) #(sys.argv[2]) = ip) (sys.argv[3]) = port)
	server.startServer()


if(sys.argv[1] == "-getData"):
	client = client(sys.argv[2]) # (sys.argv[2]) = ip)
	print(client.getMessages()) 

if(sys.argv[1] == "-sendData"):
	client = client(sys.argv[2]) #(sys.argv[2]) = ip)
	client.sendMessage(sys.argv[3]) #(sys.argv[3]) = message)

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
