import socket
import time

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("localhost", 9999))

def sendMsg(msg):
    s.sendall(str(msg).encode())

while True:
    test = input()
    if(test != "quit"):
        sendMsg(test)
    else:
        sendMsg(test)
        break
    #recv = s.recv(1024)
    '''if recv == "":
        s.close()
        print("connection close")
        break'''
    
    #print(f"recv:{recv}")