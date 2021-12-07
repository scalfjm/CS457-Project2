###############################################
# Group Name  : SAP

# Member1 Name: Ben Combs
# Member1 SIS ID: 831850566
# Member1 Login ID: bcombs18

# Member2 Name: Max Scalf
# Member2 SIS ID: 832005539
# Member2 Login ID: scalfjm
###############################################


import socket
import argparse
import random

def formatMessage(url, chain):
    message = url + "\n"
    for ss in chain :
        message = message + '{} {}\n'.format(ss[0], ss[1])
    return message

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

def parseChainfile(chainfile):
    with open(chainfile, 'r') as file:
        #First line of chain file not needed so skip it
        file.readline()
        data = file.read()
    
    chain = parseChain(data)
    print("chainlist is")
    for ss in chain:
        print("{}".format(ss))
    return chain

def run_awget(args):
    print("awget:")
    url = args.url
    print("Request: {}".format(url))
    chainfile = args.chainfile
    chain = parseChainfile(chainfile)
    nextIP, nextPort = chain[random.randint(0, len(chain)-1)]
    print("next SS is (\'{}\', {})".format(nextIP, nextPort))
    chain.remove((nextIP, nextPort))

    nextSSConn = socket.create_connection((nextIP, nextPort))
    message = formatMessage(url, chain)
    nextSSConn.send(message.encode())

    print("waiting for file...")
    filename = url.split('/')[-1]
    if filename == '' or '/' not in url:
        filename = 'index.html'
    with open(filename, 'wb') as file:
        while True:
            content = nextSSConn.recv(1024)
            file.write(content)
            if not content:
                break
    print("Received file {}".format(filename))

    print("Goodbye!")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('url', type=str)
    parser.add_argument('-c', '--chainfile', type=str, default='chaingang.txt')
    args = parser.parse_args()
    run_awget(args)

if __name__ == "__main__":
    main()
