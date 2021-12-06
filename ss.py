###############################################
# Group Name  : SAP

# Member1 Name: Ben Combs
# Member1 SIS ID: 831850566
# Member1 Login ID: bcombs18

# Member2 Name: XXXXXX
# Member2 SIS ID: XXXXXX
# Member2 Login ID: XXXXXX
###############################################

import sys
import getopt
import socket
import threading
import os
import random
import requests
from typing import List


def parseChain(chain):
    chain = []
    for line in chain.splitlines():
        line = line.strip()
        if line:
            parsed = line.split()
            ip = parsed[0]
            port = int(parsed[1])
            chain.append((ip, port))
    return chain

def runThread(clientConn):
    data = clientConn.recv(1024).decode()
    url = data.splitlines()[0]
    chain: List = data[len(url):]

    print("Request: {}".format(url))

    if(len(chain) > 1):
        print("chainlist is")
        for ss in chain.splitline():
            print("{}".format(ss))
        try:
            nextIP, nextPort = chain[random.randint(0, len(chain)-1)]
            print("next ss is (\'{}\', {})".format(nextIP, nextPort))
            chain.remove((nextIP, nextPort))
            nextSS = socket.create_connection((nextIP, nextPort))
        except:
            print("Failed to connect to next stepping stone")
            exit(1)
        print("Relaying file...")
        clientConn.send(data.encode())
    else:
        response = requests.get(url, verify=True)
        print("File received")
        print("Relaying file...")
        clientConn.send(response.text.encode())
    print("Goodbye!")
    clientConn.close()

        
def main():
    portNumber = 8000
    hostname = socket.gethostname()
    try:
        opts, args = getopt.getopt(sys.argv[1:], "p:", ["port"])
    except getopt.GetoptError as err:
        print(err)
        print("Usage: ss.py [-p] <port number>")
        exit(2)
    for o, a in opts:
        if o == "-p":
            portNumber = a

    print("ss {}, {}:".format(hostname, portNumber))

    ssSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ssSocket.bind(('', int(portNumber)))
    ssSocket.listen(5)
    connections = []
    while True:
        clientConnection, addr = ssSocket.accept()
        try:            
            currentThread = threading.Thread(target=runThread(clientConnection, ), daemon=True)
            connections.append(currentThread)
            currentThread.start()
        except IOError:
            exit(1)

if __name__ == "__main__":
    main()