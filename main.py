import socketserver
import socket
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


def update(latest_time):
    struct_time = time.strptime(latest_time, '%Y-%m-%d %H:%M:%S')
    tstamp = int(time.mktime(struct_time))
    result = list(collection_chat_room.aggregate([
        {
            "$match":{"chatroom.record.time":{"$lt":tstamp}}
        }
    ]))
    js_str = json.dumps(result[0]['chatroom']['record'])
    print(js_str)
    return js_str.encode("utf-8")

class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):

    def handle(self):
        connection = self.request
        who = connection.getpeername()
        cur_thread = threading.current_thread()
        print(cur_thread)
        print(who)
        while True:
            data = str(connection.recv(1024).decode("utf-8"))
            print(f"receive from user {who}:{data}".encode("utf-8"))
            response = ""
            if data == "quit":
                print("client quit")
                break
            if data.startswith("latest"):
                latest_time = str(data.split(",")[1]).strip()
                response = update(latest_time)
                response = bytes(response)
                self.request.sendall(response)
            
            self.request.sendall(f"get you {data}".encode("utf-8"))

    
    
class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    daemon_threads = True

if __name__ == "__main__":
    try:
        binding = ("0.0.0.0", 8051)
        server = ThreadedTCPServer(binding, ThreadedTCPRequestHandler)
        server_thread = threading.Thread(target=server.serve_forever)

        server_thread.start()
        print("Server loop running in thread:", server_thread.name)
    
    except KeyboardInterrupt:
        server.shutdown()
    
    '''while True:
        for i in threading.enumerate():
            print(i)
        time.sleep(5)'''

    #server.shutdown()