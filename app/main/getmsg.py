#-*- coding:UTF-8-*-
# this is for getting message from redis subscribe and send it to socketio
# server
from pymongo import MongoClient
import redis


# 从数据库中获取关于直播间更为详细信息
client = MongoClient(host="123.206.211.77")
db = client["Douyu"]
roomcol = db["Roominfo"]


def RocketRoom(roomid):
    if roomid:
        room = roomcol.find_one({"roomid": roomid},{"_id":0,"date":0})
        if room:
            return room
        else:
            return None


# 用于获取弹幕信息和火箭信息的redis 订阅频道
redis = redis.StrictRedis(host='123.206.211.77',
                          port='6379', db=0, password='abc@123')
chatcast = redis.pubsub()
chatcast.subscribe('chatinfo')

rocketcast = redis.pubsub()
rocketcast.subscribe('rocketinfo')
