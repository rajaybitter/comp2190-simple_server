# Client to implement simplified Diffie-Hellman protocol and demonstrate socket
# programming in the process.
# Author: fokumdt 2015-09-18

from socket import *
import math
import random

def IsValidGenerator(g, p):
    """Validation of generator and prime"""
    x = set()
    for i in range(1,p): #to iterate on the powers of the generator modulo p
        x.add((g**i)%p)
    #print ", ".join(str(e) for e in x)
    if (len(x) == (p-1)) and (g < p):
        return True
    else:
        return False

def serverHello():
    """Sends server hello message"""
    status = "100 Hello"
    return status
def sendGenerator(g):
    """Sends server generator"""
    status = "110 Generator " + str(g)
    return status

def sendPrime(p):
    """Sends server generator"""
    status = "120 Prime " + str(p)
    return status

def computeSecretKey(g, p):
	"""Computes this node's secret key"""
	secretKey = random.randint(int(g), int(p))
	return secretKey

def computePublicKey(g, p, s):
    """Computes a node's public key"""
    return (g**s)%p

def sendPublicKey(g, p):
	"""Sends node's public key"""
	status = "130 PubKey " + str(computePublicKey(g, p, computeSecretKey(g,p)))
	return status

# M   = message, an integer
# s   = sender's secret key, an integer
# Pub = receiver's public key, an integer
# p   = prime number, an integer
def encryptMsg(M, s, Pub, p):
	"""Encrypts a message M given parameters above"""
	return M*((Pub**s)% p)

# C   = ciphertext, an integer
# s   = receiver's secret key, an integer
# Pub = sender's public key, an integer
# p   = prime number, an integer
def decryptMsg(C, s, Pub, p):
	"""Encrypts a message M given parameters above"""
	return C/((Pub**s)% p)


def main():
    """Driver function for the project"""
    serverHost = '172.16.190.124'        # The remote host
    serverPort = 5115              # The same port as used by the server
    while (True):
    	prime = int(raw_input('Enter a valid prime between 7 and 101: '))
    	generator = int(raw_input('Enter a positive integer less than the prime just entered: '))
    	if (IsValidGenerator(int(generator), int(prime))): break
    # Create socket
    c_sock = socket(AF_INET,SOCK_STREAM)
    # Connect socket
    c_sock.connect((serverHost,serverPort))		
    # Send msg to server
    msg = serverHello() # make hello message
    c_sock.send(msg) # send hello message
    # Receive server's response to Hello message
    msg = c_sock.recv(1024) # get hello confirm
    # Handle case of invalid response to Hello message
    if msg != "100 Hello": 
    	c_sock.close()
    # Handle case of valid response to Hello message
    print msg
    msg = sendGenerator(generator) # make generator
    	# Send generator to server.
    c_sock.send(msg) 
    msg = c_sock.recv(1024) # get generator reply
    # Handle case of invalid response to generator message
    if " ".join(msg.split(" ")[0:-1]) != "111 Generator":
    	c_sock.close()
    # Handle valid response to generator message
    print msg
    msg= sendPrime(prime) # make prime
    # Send prime to server.
    c_sock.send(msg) # send prime
    msg = c_sock.recv(1024)#get prime response
    # Handle case of invalid response to prime message
    if " ".join(msg.split(" ")[0:-1]) != "121 Prime":
    	c_sock.close()
    print msg
    # Handle valid response to prime message
    # Compute secret key
    s_key = computeSecretKey(generator,prime)
    # Compute public key
    msg = sendPublicKey(generator, prime)#make public key
    pub_key = msg.split(" ")[-1]
    # Send public key to server
    c_sock.send(msg)#send pub key
    msg = c_sock.recv(1024)#get pub key
    # Handle invalid response to public key message
    if " ".join(msg.split(" ")[0:-1]) !="130 PubKey":
    	c_sock.close()
    # Handle valid response to public key message.
    print msg
    other_pub = msg.split(" ")[-1]
    # Print keys to standard output
    print "Other process public key: " + other_pub + "\nClient public key: " +str(pub_key) + "\nClient private key: " + str(s_key) 				
	# Close connection
    c_sock.close()

if __name__ == "__main__":
    main()
