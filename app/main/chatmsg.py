#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-07-14 10:20:40
# @Author  : Wangmengcn (eclipse_sv@163.com)
# @Link    : https://eclipsesv.com
# @Version : $0.1$
import time
import simplejson
from datetime import datetime
from flask import Flask, render_template
from flask_socketio import SocketIO
from flask_socketio import send, emit
from getmsg import chatcast, rocketcast, RocketRoom, valuebyHour


# flask 主程序
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
socketio = SocketIO(app)


def converData(data):
    if data is not None and not isinstance(data['data'], long):
        value = data['data']
        mid = simplejson.dumps(value)
        jsondata = simplejson.loads(mid)
        result = eval(jsondata)
        return result
    else:
        return None

# ＝＝＝＝＝＝＝关于最新弹幕信息的触发和广播＝＝＝＝＝＝＝ #
# 客户端触发'chat msg'事件之后，向'broad cast'发送消息，从而触发广播事件


@socketio.on('chat msg')
def getmsg(message):
    chatmsg = chatcast.get_message()
    rocketmsg = rocketcast.get_message()
    chatresult = converData(chatmsg)
    rocketreuslt = converData(rocketmsg)
    if chatresult is not None:
        sender = chatresult['sender_id']
        content = chatresult['content']
        chat = sender + " said: " + content
        socketio.emit('broad cast', chat)
    if rocketreuslt is not None:
        if rocketreuslt['recver_room'] is not None:
            roomid = int(rocketreuslt['recver_room'])
            print roomid
            if roomid:
                gitfroom = RocketRoom(roomid)
                socketio.emit('rocket cast', gitfroom)

# 经测试，直接讲dict类型发送给前端是无效的，但是转为list之后，前端可以直接接收数据


@socketio.on('index')
def getindex(message):
    today = datetime(2016, 7, 27)
    if valuebyHour(today) is not None:
        (a, b, c, d) = valuebyHour(today)
        if b is not None:
            socketio.emit('rocket by day', b)
        if c is not None:
            send = sorted(c.iteritems(), key=lambda d: d[1], reverse=True)
            socketio.emit('sender rank', send)
        if d is not None:
            recv = sorted(d.iteritems(), key=lambda d: d[1], reverse=True)
            socketio.emit('recver rank', recv)

# 在客户端建立建立连接之后，通过触发此方法进行不同的操作，例如向'broad cast'时间发送消息


@socketio.on('connect')
def clientconnected():
    socketio.emit('broad cast', "msg")
    print 'connected'

# 获取日历点击之后发回的日期


@socketio.on('historyDate')
def sendDate(date):
    if date:
        print date
        time = date.split('-')
        timevalue = [int(item) for item in time]
        y = timevalue[0]
        m = timevalue[1]
        d = timevalue[2]
        recordDate = datetime(y, m, d)
        returnValue = valuebyHour(recordDate)
        if returnValue:
            (a, b, c, d) = returnValue
            if b is not None:
                socketio.emit('historyRockets', b)
        else:
            socketio.emit('historyRockets', None)
# 通过'broad cast'向已经建立简介的客户端广播消息


@socketio.on('broad cast')
def castinfo(data):
    emit('broad cast', data, broadcast=True)


# ＝＝＝＝＝＝＝关于最新火箭信息的触发和广播＝＝＝＝＝＝＝ #

@socketio.on('rocket cast')
def castRocket(data):
    emit('rocket cast', data, broadcast=True)


# ＝＝＝＝＝＝＝每天按小时火箭分布情况＝＝＝＝＝＝＝ #
@socketio.on('rocket by day')
def rocketperhour(data):
    emit('rocket by day', data, broadcast=True)


@socketio.on('sender rank')
def sendrank(data):
    emit('sender rank', data, broadcast=True)


@socketio.on('recver rank')
def recvrank(data):
    emit('recver rank', data, broadcast=True)


@socketio.on('historyRockets')
def sendHistory(data):
    emit('historyRockets', data)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=3000)
