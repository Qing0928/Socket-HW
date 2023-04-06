from pymongo import MongoClient
from pprint import pprint
from datetime import datetime
import time


client = MongoClient('mongodb://root:mongo0928@localhost:27017')
db_chat = client.chat_room
collection_chat_room = db_chat.chat_record

now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
struct_time = time.strptime(now, '%Y-%m-%d %H:%M:%S')
tstamp = int(time.mktime(struct_time))
latest_time = 1679817632
result = list(collection_chat_room.aggregate([
    {"$match":{"chatroom.record.time":{"$lt":tstamp}}},
    {"$unwind":"$chatroom.record"},     
    {"$sort":{"chatroom.record.time":-1}},  
    {"$limit":5}
        ]))
result_list = list()
for i in range(0, len(result)):
    result_list.append(result[i]['chatroom']['record'])
#pprint(result[0]['chatroom']['record'])
pprint(result_list)

'''now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
print(now)
struct_time = time.strptime(now, '%Y-%m-%d %H:%M:%S')
print(struct_time)'''
