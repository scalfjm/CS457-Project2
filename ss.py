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
    data = clientConn.recv(1024)
    url = data.splitlines()[0]
    chain: List = data[len(url):]
    if(len(chain) > 0):
        try:
            nextIP, nextPort = chain[random.randint(0, len(chain)-1)]
            chain.remove((nextIP, nextPort))
            nextSS = socket.create_connection((nextIP, nextPort))
        except:
            print("Failed to connect to next stepping stone")
            exit(1)
        clientConn.send(data.encode())
    else:
        encoding, text = requests.get(url, verify=False)
        content = str(encoding) + "\n" + text
        clientConn.send(content.encode())
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

    print("ss: {}, {}".format(hostname, portNumber))

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