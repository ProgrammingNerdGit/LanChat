#2020 programming nerd


import requests # module for geting / sending data from server
from bs4 import BeautifulSoup # module for parseing data from server
from http.server import HTTPServer, BaseHTTPRequestHandler # module for creating / managing server
import threading # module used for useing threads
import time # module used for delay
import sys # module for connection with exturnal program

data = '' # temperary veriable for parseing the data from the server

timeBetwenRefresh = 0.2 # Time in second between each time the client asks for data from server

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
		try:
			page = requests.get(str(self.url+"/?text="+message)) # "/?text=" used int url to send data to the server (used before the message)
		except:
			print("not valid ip/port")

	def getMessages(self):
			page = requests.get(self.url+"/?get",stream=True,timeout=1) # "/?get" used in url to get data without sending data
			return BeautifulSoup(page.content,'lxml').find("div").text.replace("%E2%96%88"," ").replace("\n","%G2%12%99") # return data parsed and in a list (%E2%96%88 is space keycode)

		
		
if(sys.argv[1] == "-startServ"): # checks for exturnal program asking to create a server
	server = server(sys.argv[2],int(sys.argv[3])) # gets data from exturnal program and makes server (sys.argv[2]) = ip) (sys.argv[3]) = port)
	server.startServer()


if(sys.argv[1] == "-getData"): # checks for exturnal program asking to get data from a server
	#print(sys.argv)
	client = client(sys.argv[2]) #create client connection with data from ext. program (sys.argv[2]) = ip)
	print(client.getMessages()) #get data from server

if(sys.argv[1] == "-sendData"): # checks for exturnal program asking to send data from a server
	client = client(sys.argv[2]) #create client connection with data from ext. program (sys.argv[2]) = ip)
	client.sendMessage(sys.argv[3]) # sends data to server (sys.argv[3]) = message)
	






