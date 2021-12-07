###############################################
# Group Name  : SAP

# Member1 Name: Ben Combs
# Member1 SIS ID: 831850566
# Member1 Login ID: bcombs18

# Member2 Name: Max Scalf
# Member2 SIS ID: 832005539
# Member2 Login ID: scalfjm
###############################################

import sys
import getopt
import socket
import threading
import os
import random
from typing import List

def parseChain(chainStr):
    chain = []
    for line in chainStr.splitlines():
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
    chain = data.splitlines()

    tmpfile = createTmpfile()

    print("Request: {}".format(url))

    if(len(chain) > 1):
        print("chainlist is")
        for ss in chain[1:]:
            print("{}".format(ss))
        try:
            rand = random.randint(1, len(chain)-1)

            nextIP, nextPort = chain[rand].split(" ")
            print("next ss is (\'{}\', {})".format(nextIP, nextPort))
            chain.pop(rand)
            print((nextIP.replace("'", "")))
            nextSS = socket.create_connection((nextIP, nextPort))

            data = ""
            for c in chain:
                data += c + "\n"
            nextSS.sendall(data.encode())

            print("waiting for file...")
            receiveFromSS(nextSS, tmpfile)
            print("Relaying file...")
            relayToClient(clientConn, tmpfile)

            
        except:
            print("Failed to connect to next stepping stone")

    else:
        print("chainlist is empty\nissuing wget for file", url)
        os.system("wget -q -O " + tmpfile + " " + url)
        print("File received\nRelaying file...")
        relayToClient(clientConn, tmpfile)

    print("Goodbye!")
    clientConn.close()
    os.system("rm -f " + tmpfile)

def receiveFromSS(nextSS, tmpfile):
    o = open(tmpfile, 'wb')

    while True:
        chunk = nextSS.recv(1024)
        if not chunk:
            break

        o.write(chunk)

def relayToClient(clientConn, tmpfile):
    f = open(tmpfile, 'rb')

    while True:
        chunk = f.read(1024)

        while(chunk):
            clientConn.sendall(chunk)
            chunk = f.read(1024)

        f.close()
        clientConn.close()
        break

def createTmpfile():
    tmpnum = str(random.randint(0,999999999))
    tmpfile = "tmp"+tmpnum
    while os.path.exists("./" +tmpfile):
        tmpnum = str(random.randint(0,999999999))
        tmpfile = "tmp"+tmpnum
    return tmpfile
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
