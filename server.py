# Server to implement simplified Diffie-Hellman protocol and demonstrate socket
# programming in the process.
# Author: fokumdt 2015-09-18

from socket import *
import random

def computePublicKey(g, p, s):
    """Computes a node's public key"""
    return (g**s)%p

def computeSecretKey(g, p):
	"""Computes this node's secret key"""
	secretKey = random.randint(int(g), int(p))
	return secretKey
	
def sendPublicKey(g, p):
	"""Sends node's public key"""
	status = "130 PubKey " + str(computePublicKey(g, p, computeSecretKey(g,p)))
	return status


HOST = 'localhost'          # Symbolic name meaning all available interfaces
PORT = 5115               # Arbitrary non-privileged port
STRHello = "100 Hello"
STRGenerator = "110 Generator"
STRGeneratorResp = "111 Generator Rcvd"
STRPrime = "120 Prime"
STRPrimeResp = "121 Prime Rcvd"
STRPubKey = "130 PubKey"

# Carry out necessary socket set up
serverPort = PORT
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
serverSocket.bind(("", serverPort))
serverSocket.listen(1)



while True:
    connectionSocket, addr = serverSocket.accept()
    print('Connected by', addr)
    # Receive Hello message
    msg = connectionSocket.recv(1024)#get hello
    # Receive server's response to Hello message
    	# Handle case of invalid message.
    if msg != STRHello: #check hello
    	print "Incorrect Hello message"
    	connectionSocket.close()
    # Handle case of valid Hello message
    print msg
    connectionSocket.send(STRHello) # send hello conformation
    msg= connectionSocket.recv(1024) #get generator
    if(" ".join(msg.split(" ")[0:-1]) == STRGenerator):
	    print msg
	    g = int(msg.split(" ")[-1]) #get generator int
	    # Handle case of valid generator message
	    connectionSocket.send(STRGeneratorResp) #send generator response
    msg = connectionSocket.recv(1024)#get prime
    if(" ".join(msg.split(" ")[0:-1]) == STRPrime):
	    print msg
	    p = int(msg.split(" ")[-1])#get prime int
	    # Handle case of valid prime message
	    connectionSocket.send(STRPrimeResp)#send prime response
    msg = connectionSocket.recv(1024)
    other_pub = msg.split(" ")[-1]# get pub key
    # Handle case of valid public key message
    if(" ".join(msg.split(" ")[0:-1]) == STRPubKey):
    	print msg
    	secret_key = int(computeSecretKey(g,p))
    	msg = sendPublicKey(g, p)#make public key
    	connectionSocket.send(msg) #send pub key
    	pub_key = msg.split(" ")[-1]
    print "\nOther process public key: " + other_pub + "\nServer public key: " +str(pub_key) + "\nServer private key: " + str(secret_key) 
	# Close connection.
    connectionSocket.close()
