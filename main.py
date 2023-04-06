import socketserver
import socket
import sys
import threading
import time
import json
from pprint import pprint
from pymongo import MongoClient
from datetime import datetime


client = MongoClient('mongodb://root:mongo0928@localhost:27017')
'''db_user = client.chat_user
collection_user_info = db_user.user_info'''

db_chat = client.chat_room
collection_chat_room = db_chat.chat_record


def first_use():
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    struct_time = time.strptime(now, '%Y-%m-%d %H:%M:%S')
    tstamp = int(time.mktime(struct_time))
    result = list(
        collection_chat_room.aggregate([
        {"$match":{"chatroom.record.time":{"$lt":tstamp}}},
        {"$unwind":"$chatroom.record"},     
        {"$sort":{"chatroom.record.time":-1}},  
        {"$limit":15}
        ])
    )
    result_list = list()
    for i in range(0, len(result)):
        result_list.append(result[i]['chatroom']['record'])
    js_str = json.dumps(result_list).encode("utf-8")
    return js_str

def update_chat(latest_time:str):
    struct_time = time.strptime(latest_time, '%Y-%m-%d %H:%M:%S')
    tstamp = int(time.mktime(struct_time))
    result = list(
        collection_chat_room.aggregate([
        {"$match":{"chatroom.record.time":{"$lt":tstamp}}}
    ]))
    js_str = json.dumps(result[0]['chatroom']['record']).encode("utf-8")
    return js_str

def new_msg(msg_content:str, ip:str):
    msg = json.loads(msg_content)
    latest_time = msg['time']
    content = msg['content']
    sendby = msg['sendby']
    struct_time = time.strptime(latest_time, '%Y-%m-%d %H:%M:%S')
    tstamp = int(time.mktime(struct_time))
    collection_chat_room.update_many(
        {}, 
        {
            "$push":{
                "chatroom.record":{
                    "time":tstamp, 
                    "sendby":f"{sendby}", 
                    "content":f"{content}", 
                    "ip":f"{ip}"
                }
            }
        }, upsert=True
    )

class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):

    def handle(self):
        connection = self.request
        ip, port = connection.getpeername()
        cur_thread = threading.current_thread()
        print(cur_thread)
        print(ip)
        connect_detail = f"{ip}:{port}"
        while True:
            data = str(connection.recv(1024).decode("utf-8"))
            print(f"receive from user {ip}:{data}".encode("utf-8"))
            response = ""

            if data == "quit":
                break

            elif data.startswith("latest"):
                latest_time = str(data.split("latest,")[1]).strip()
                response = update_chat(latest_time)
                response = bytes(response)
                self.request.sendall(response)
            
            elif data.startswith("new"):
                msg_content = str(data.split("new,")[1]).strip()
                new_msg(msg_content, connect_detail)
                self.request.sendall(b"receive new msg \n")
                print("send success")

            elif data.startswith("first"):
                response = first_use()
                self.request.sendall(response)

            self.request.sendall(b"\n")

    
    
class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    daemon_threads = True

if __name__ == "__main__":
    try:
        '''server_thread = threading.Thread(target=server.serve_forever)

        server_thread.start()
        print("Server loop running in thread:", server_thread.name)'''
        binding = ("0.0.0.0", 8051)
        server = ThreadedTCPServer(binding, ThreadedTCPRequestHandler)
        server.serve_forever()
    
    except KeyboardInterrupt:
        server.shutdown()
        sys.exit(0)