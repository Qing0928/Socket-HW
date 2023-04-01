import socket
import time
from datetime import datetime
from threading import Timer

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("localhost", 8051))

def sendMsg(msg):
    s.sendall(str(msg).encode())

def auto_update():
    while (True):
        print("timer is working")
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        struct_time = time.strptime(now, '%Y-%m-%d %H:%M:%S')
        tstamp = int(time.mktime(struct_time))
        sendMsg(f"latest,{tstamp}")
        recv = s.recv(1024)
        print(recv)

#nick_name = str(input("輸入暱稱"))
Timer(2, auto_update).start()
'''while True:
    #print(datetime.now().strftime('%H:%M:%S'))
    test = input("輸入訊息")
    sendMsg(test)
    recv = s.recv(1024)
    print(recv)
    #time.sleep(5)'''
