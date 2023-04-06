import socket
import time
import json
from datetime import datetime
from threading import Timer

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("localhost", 8051))

test_json_string = "{\"time\":\"2023-04-05 16:29:30\",\"sendby\":\"giraffe0928\", \"content\":\"hello\"}"

def sendMsg(msg):
    s.sendall(str(msg).encode())

def auto_update():
    while (True):
        print("timer is working")
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        struct_time = time.strptime(now, '%Y-%m-%d %H:%M:%S')
        tstamp = int(time.mktime(struct_time))
        sendMsg(f"latest,{tstamp}")
        #recv = s.recv(1024)
        #print(recv)

#nick_name = str(input("輸入暱稱"))
#Timer(2, auto_update).start()
''''''
while True:
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    #test_json_string = "{\"time\":\"{}\",\"sendby\":\"giraffe0928\", \"content\":\"hello\"}".format(now)
    test_json_string = {
        "time":f"{now}", 
        "sendby":"giraffe0928", 
        "content":"hello"
        }
    
    #print(datetime.now().strftime('%H:%M:%S'))
    #test = input("輸入訊息")
    sendMsg(f"new,{json.dumps(test_json_string)}")
    recv = s.recv(1024)
    print(recv)
    time.sleep(10)