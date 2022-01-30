from base64 import decode
import socket
import select
import threading
import sys
from datetime import datetime
from requests import get
import os


# Connection Data
ip = get('https://api.ipify.org').content.decode('utf8')
print('My public IP address is: {}'.format(ip))
host = socket.gethostbyname(ip)
port = 1131

# Starting Server
#This is the global server allowing for exchange of information between clients
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((host, port))
server.listen()

qservers = []
qthreads = []
#Each user requires a personal server
def generateAdditonalServer():
    global port
    qservers.append(socket.socket(socket.AF_INET, socket.SOCK_STREAM))
    qservers[-1].setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    port +=1
    print("binding qserver to port %c", port)
    qservers[-1].bind((host, port))
    qservers[-1].listen(1)

qserver =socket.socket(socket.AF_INET, socket.SOCK_STREAM)
qserver.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
qserver.bind((host, port+6846))
qserver.listen()

# Lists For Clients and Their roles
clientsA = []
clientsB = []
nicknames = []
quantumInstructions = []
qifiles = []

# Sending Messages To All Connected Clients
def broadcast(message):
    
    for client in clientsA:
        #if(nicknames[clientsA.index(client)]) == 'interface':
        client.send(message)
# Handling Messages From Clients
def handle(client):
    while True:
        try:
            # Broadcasting Messages
            msg = message = client.recv(1024)
            #this is how we check whether or not we actually want to broadcast
            #instead of broadcasting circuits, we send them encoded to the interface
            #which decode them and send them to qiskit
            if msg.decode('ascii').startswith('EXIT'):
                name_to_kick = msg.decode('ascii')[5:]
                print(name_to_kick)
                kick_user(name_to_kick)
            else:
                broadcast(message)
        except:
            # Removing And Closing Clients
            if client in clientsA:
                index = clientsA.index(client)
                clientsA.remove(client)
                client.close()
                nickname = nicknames[index]
                broadcast('{} left!'.format(nickname).encode('ascii'))
                nicknames.remove(nickname)
                break
def qhandle(client):
    while True:
        try:
            # Broadcasting Messages
            msg = message = client.recv(1024)
            #this is how we check whether or not we actually want to broadcast
            #instead of broadcasting circuits, we send them encoded to the interface
            #which decode them and send them to qiskit
            if msg.decode('ascii').startswith('INTERFACE'):
                #if nicknames[clientsA.index(client)] == 'admin':
                qCommand = msg.decode('ascii')[msg.decode('ascii').find('|'):]
                filename =  msg.decode('ascii')[9:msg.decode('ascii').find('|')]#+str(datetime.now())[:-7]+".txt"
                qifiles.append(filename)
                with open("_in/"+filename, 'x') as f:
                    f.write(f'{qCommand}\n')
                print('Command Recieved')
                #else:
                #   client.send('Command Refused'.encode('ascii'))
            if msg.decode('ascii').startswith('KEY'):
                #if nicknames[clientsA.index(client)] == 'admin':
                qCommand = msg.decode('ascii')[msg.decode('ascii').find('|')+1:]
                filename =  "BOB"#+str(datetime.now())[:-7]+".txt"
                qifiles.append(filename)
                with open("_in/"+filename, 'x') as f:
                    f.write(f'{qCommand}\n')
                print('Command Recieved')
            if msg.decode('ascii').startswith('BASIS'):
                #if nicknames[clientsA.index(client)] == 'admin':
                qCommand = msg.decode('ascii')[msg.decode('ascii').find('|')+1:]              
                print(qCommand)
                #filename =  msg.decode('ascii')[:msg.decode('ascii').find('bitstring')+len("bitstring")]+str(datetime.now())[:-7]+".txt"
                filename = "ALICE"#+str(datetime.now())[:-7]+".txt"
                qifiles.append(filename)
                with open("_in/"+filename, 'x') as f:
                    f.write(f'{qCommand}\n')
                print('Command Recieved')
            #else:
            #    broadcast(message)
           # if(os.system('ls ALICE*') != '' and os.system("ls BOB*")!=''):
            #    os.system('qinterfeace.py')
        except:
            # Removing And Closing Clients
            if client in clientsB:
                index = clientsB.index(client)
                clientsB.remove(client)
                client.close()
                nickname = nicknames[index]
                broadcast('{} left!'.format(nickname).encode('ascii'))
                nicknames.remove(nickname)
                closeQ(qservers[index])
                qservers.remove(index)
                break
        #except KeyboardInterrupt:
        #   print("[!] Keyboard Interrupted!")
        #    close()
        #    break

# Receiving / Listening Function
def receive():
    generateAdditonalServer()
    while True:
        # Accept Connection
        clientA, addressA = server.accept()


        #clientB, addressB = qserver.accept()
        print("Connected with {}".format(str(addressA)))

        # Request And Store Nickname
        clientA.send('NICK'.encode('ascii'))
        clientsA.append(clientA)
        if(len(clientsA) > len(qservers)):
            generateAdditonalServer()
        clientA.send(str(port).encode('ascii'))
        nickname = clientA.recv(1024).decode('ascii')
  
       # if nickname == 'admin':
       #     #send a specific request
       #     clientA.send('PASS'.encode('ascii'))
       #     #password is a string that is taken as the next 1024 bytes recieved as ASCII or until \n
       #     password = clientA.recv(1024).decode('ascii')

       #     if(password != "password"):
       #        clientA.send('REFUSE'.encode('ascii'))
       #         clientA.close()
       #         continue 

        nicknames.append(nickname)

        currServ = qservers[-1]
        clientB, addressB = currServ.accept()
        clientB.send('NICK'.encode('ascii'))
        clientsB.append(clientB)


        # Print And Broadcast Nickname
        print("Nickname is {}".format(nickname))
        broadcast("{} joined!".format(nickname).encode('ascii'))
        clientA.send('Connected to serverA!'.encode('ascii'))
        clientB.send('Connected to Personal Server!'.encode('ascii'))

        #breaks here
        # Start Handling Thread For Client
        thread = threading.Thread(target=handle, args=(clientA,))
        thread.start()
        
        #qthread = threading.Thread(target= qhandle,args=(clientB,))
        #qthread.start()
        qthreads.append(threading.Thread(target=qhandle, args=(clientB,)))
        qthreads[-1].start()
            
def kick_user(name):
    if name in nicknames:
        name_index = nicknames.index(name)
        client_to_kick = clientsA[name_index]
        # remove client from list
        clientsA.remove(client_to_kick)
        client_to_kick.send('You were kicked'.encode('ascii'))
        client_to_kick.close()
        nicknames.remove(name)
        broadcast(f'{name} was kicked'.encode('ascii'))

def close():
    server.shutdown(socket.SHUT_RDWR)
    server.close()
    print ("closed")

#closes a quantum server once it's user has disconnected
def closeQ(qserver):
    qserver.shutdown(socket.SHUT_RDWR)
    qserver.close()





#def alice():
    #2 jobs

 #   pass

#def bob():
#    #1 job
#    pass


print("Server is listening")
receive()