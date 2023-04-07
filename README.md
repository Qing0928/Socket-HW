# Socket-HW-Server

網路最佳化作業

## 使用的套件

```
import socketserver >> 由python官方封裝好的socket，專門用來製作server
import sys
import threading >> 使用多threading來處理要求
import time
import json
from pymongo import MongoClient >> 連接MongoDB用
from datetime import datetime
```

## 連接資料庫

```
client = MongoClient('mongodb://root:mongo0928@localhost:27017')

db_chat = client.chat_room
collection_chat_room = db_chat.chat_record
```

## 處理首次使用的function
```
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
```
將訊息則數限制在最新的15則

## 更新聊天紀錄的function

```
def update_chat(latest_time:str):
    struct_time = time.strptime(latest_time, '%Y-%m-%d %H:%M:%S')
    tstamp = int(time.mktime(struct_time))
    result = list(
        collection_chat_room.aggregate([
        {"$match":{"chatroom.record.time":{"$lt":tstamp}}}
    ]))
    js_str = json.dumps(result[0]['chatroom']['record']).encode("utf-8")
    return js_str
```
其他人的發言會在這時一起回傳

## 發訊息的function

```
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
```

當使用者發來訊息時，會把資料存在MongoDB當中

紀錄在伺服器有以下資料:
  1. ip
  2. port
  3. time
  4. 訊息
 
 ## Handler
 
 ```
 class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):

    def handle(self):
        connection = self.request
        ip, port = connection.getpeername()
        cur_thread = threading.current_thread()
        connect_detail = f"{ip}:{port}"
        while True:
            data = str(connection.recv(1024).decode("utf-8"))
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

            elif data.startswith("first"):
                response = first_use()
                response = bytes(response)
                self.request.sendall(response)

            self.request.sendall(b"\n")
 ```
 
 ## Server
 ```
 class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    daemon_threads = True
 ```
 
 server會在背景中運作
 
 ## 啟動
 
 ```
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
 ```
 
 當有一個新的使用者進入，就會啟動新的threading來處理要求
