import socket
import threading
import random


clientA = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientA.connect(("129.236.142.190", 1234))

clientB = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


stop_thread = False
methods = ['E91','BB84']

nickname = input("Choose a nickname: ")

if nickname == "admin":
    password = input("Enter paswword for admin: ")

#basis = input("#Please input your basis")

def receive():
    while True:
        global stop_thread
        if stop_thread:
            break
        try:
            msg = message = clientA.recv(1024).decode('ascii')
            if msg.startswith("NICK"):
                clientA.send(nickname.encode('ascii'))
               # port = int(clientA.recv(1024).decode('ascii'))
                port = int(msg[4:])
                #print(port)
                clientB.connect(("129.236.142.190", port))
                #clientB.send(nickname.encode('ascii'))
                #if next_message == 'PASS':
                #    clientA.send(password.encode('ascii'))
                #    if clientA.recv(1024).decode('ascii') == 'REFUSE':
                #        print("Connection was refused! Wrong passsword!")
                #        stop_thread = True
                #elif next_message == 'BAN':
                #   print("Connection refused because of ban")
                #   clientA.close()
                #   stop_thread = True
            if msg == "BASIS":
                pass
            else:
                print(message)

        except:
            print("An error occurred!")
            clientA.close()
            clientB.close()
            break

def write():
    while True:
        if stop_thread:
            break
        message = '<{}>: {}'.format(nickname, input(''))

        if message[len(nickname)+4:].startswith('/'):
            if message[len(nickname)+5:].startswith('EXIT'):
                clientA.send(f'EXIT {message[1:len(nickname)+1]}'.encode('ascii'))
            elif(nickname=='ALICE'):
                    method = methods[random.getrandbits(1)]
                    clientB.send(f'BASIS|ALICE\nMETHOD {method}\n{message[1:len(nickname)+1]} bitstring {rand_key(10)}\n{message[1:len(nickname)+1]} basis {rand_key(10)}'.encode('ascii'))
            elif(nickname=='BOB'):
                    clientB.send(f'KEY|{message[1:len(nickname)+1]}\nBOB basis {rand_key(10)}'.encode('ascii'))
            #else:
                #clientB.send(f'INTERFACE {nickname+"|"+message[len(nickname)+5:]}'.encode('ascii'))
        else:
            clientA.send(message.encode('ascii'))


def rand_key(p):
   
    # Variable to store the
    # string
    key1 = ""
 
    # Loop to find the string
    # of desired length
    for i in range(p):
         
        # randint function to generate
        # 0, 1 randomly and converting
        # the result into str
        temp = str(random.randint(0, 1))
 
        # Concatenation the random 0, 1
        # to the final result
        key1 += temp
         
    return(key1)
 
#n = 7
#str1 = rand_key(n)
#print("Desired length random binary string is: ", str1)

write_thread = threading.Thread(target = write)
write_thread.start()

receive_thread = threading.Thread(target = receive)
receive_thread.start()


