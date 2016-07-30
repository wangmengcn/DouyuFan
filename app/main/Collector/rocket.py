#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-07-14 10:20:40
# @Author  : Wangmengcn (eclipse_sv@163.com)
# @Link    : https://eclipsesv.com
# @Version : $0.1$
# 获取实时火箭数量
import socket
import time
import re
from pymongo import MongoClient
import pymongo
from datetime import datetime
from broadcast import castRocket
from broadcast import castChat


'''这里要注意几个变量： host port roomid gid '''

HOST = 'openbarrage.douyutv.com'
PORT = 8601
RID = 97376
LOGIN_INFO = "type@=loginreq/username@=qq_aPSMdfM5" + \
    "/password@=1234567890123456/roomid@=" + str(RID) + "/"
JION_GROUP = "type@=joingroup/rid@=" + str(RID) + "/gid@=-9999" + "/"
ROOM_ID = "type@=qrl/rid@=" + str(RID) + "/"
KEEP_ALIVE = "type@=keeplive/tick@=" + \
    str(int(time.time())) + "/vbw@=0/k@=19beba41da8ac2b4c7895a66cab81e23/"
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def tranMsg(content):
    length = bytearray([len(content) + 9, 0x00, 0x00, 0x00])
    code = length
    magic = bytearray([0xb1, 0x02, 0x00, 0x00])
    end = bytearray([0x00])
    trscont = bytes(content.encode('utf-8'))
    return bytes(length + code + magic + trscont + end)


# 获取全频道播放的火箭信息
def get_rocket(data):
    try:
        sender_id = re.search('\/sn@=(.+?)\/', data).group(1)
        recver_id = re.search('\/dn@=(.+?)\/', data).group(1)
        recver_room = re.search('\/drid@=(.+?)\/', data).group(1)
        gift = re.search('\/gn@=(.+?)\/', data).group(1)
        rocketmsg = {}
        rocketmsg["sender_id"] = sender_id
        rocketmsg["recver_id"] = recver_id
        rocketmsg["recver_room"] = recver_room
        rocketmsg["gift"] = gift
        rocketmsg["date"] = datetime.now()
        col.insert_one(rocketmsg, bypass_document_validation=False)
        if gift == u"火箭":
            publishvalue = {}
            publishvalue["sender_id"] = sender_id
            publishvalue["recver_id"] = recver_id
            publishvalue["recver_room"] = recver_room
            publishvalue["gift"] = gift
            castRocket(publishvalue)
            print sender_id, "送给房间号为:", recver_room, "的", recver_id, "一个",\
                gift, "<", datetime.now(), ">"
    except Exception, e:
        print "error occur:", repr(data)
    finally:
        pass

# 获取聊天信息


def get_chatmsg(data):
    try:
        sender_id = re.search('\/nn@=(.+?)\/', data).group(1)
        sender_content = re.search('\/txt@=(.+?)\/', data).group(1)
        chatmsg = {}
        chatmsg["sender_id"] = sender_id
        chatmsg["content"] = sender_content
        chatmsg["date"] = datetime.now()
        publishvalue = {}
        publishvalue["sender_id"] = sender_id
        publishvalue["content"] = sender_content
        chatcol.insert_one(chatmsg, bypass_document_validation=False)
        castChat(publishvalue)
        print sender_id, "said:", sender_content, "at:<", datetime.now(), ">"
    except Exception, e:
        print "error occur:", repr(data)
    finally:
        pass


def insert_msg(sock):
    sendtime = 0
    while True:
        if sendtime % 20 == 0:
            print "----------Keep Alive---------"
            try:
                sock.sendall(tranMsg(KEEP_ALIVE))
            except socket.error:
                print "alive error"
                sock = create_Conn()
                insert_msg(sock)
        sendtime += 1
        print sendtime
        try:
            data = sock.recv(4000)
            if data:
                strdata = repr(data)
                if "type@=spbc" in strdata:
                    get_rocket(data)
                if "type@=chatmsg" in strdata:
                    get_chatmsg(data)
        except socket.error:
            print "chat error"
            sock = create_Conn()
            insert_msg(sock)
        time.sleep(1)


def create_Conn():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    RID = get_Hotroom()
    if RID:
        print "当前最热房间:", RID
        LOGIN_INFO = "type@=loginreq/username@=qq_aPSMdfM5" + \
            "/password@=1234567890123456/roomid@=" + str(RID) + "/"
        print LOGIN_INFO
        JION_GROUP = "type@=joingroup/rid@=" + str(RID) + "/gid@=-9999" + "/"
        print JION_GROUP
        s.sendall(tranMsg(LOGIN_INFO))
        s.sendall(tranMsg(JION_GROUP))
        return s
    else:
        time.sleep(300)
        create_Conn()


def false_Conn():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((HOST, PORT))
        RID = 110
        print "当前最热房间:", RID
        LOGIN_INFO = "type@=loginreq/username@=qq_aPSMdfM5" + \
            "/password@=1234567890123456/roomid@=" + str(RID) + "/"
        print LOGIN_INFO
        JION_GROUP = "type@=joingroup/rid@=" + str(RID) + "/gid@=-9999" + "/"
        print JION_GROUP
        s.sendall(tranMsg(LOGIN_INFO))
        s.sendall(tranMsg(JION_GROUP))
    except:
        pass
    return s


def get_Hotroom():
    hotroom = roomcol.find().sort("audience", pymongo.DESCENDING).limit(1)
    for item in hotroom:
        return item["roomid"]

client = MongoClient()
db = client["Douyu"]
col = db["rocket"]
chatcol = db["chatmsg"]
roomcol = db["Roominfo"]
print "已连接至数据库"

s = create_Conn()
insert_msg(s)
