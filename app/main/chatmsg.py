#-*- coding:UTF-8-*-
from flask import Flask, render_template
from flask_socketio import SocketIO
from flask_socketio import send, emit
import redis
import time
import simplejson

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
socketio = SocketIO(app)

redis = redis.StrictRedis(host='123.206.211.77',
                          port='6379', db=0, password='abc@123')
broadcast = redis.pubsub()
broadcast.subscribe('rocketinfo')



def convertData(data):
    if data:
        try:
            result = eval(data)
            print type(result)
            print result
        except Exception, e:
            raise e

# ＝＝＝＝＝＝＝关于最新弹幕信息的触发和广播＝＝＝＝＝＝＝ #

# 客户端触发'chat msg'事件之后，向'broad cast'发送消息，从而触发广播事件
@socketio.on('chat msg')
def getmsg(message):
    print('received msg:' + str(message))
    msg = broadcast.get_message()
    if msg is not None and not isinstance(msg['data'], long):
        value = msg['data']
        mid = simplejson.dumps(value)
        jsondata = simplejson.loads(mid)
        result = eval(jsondata)
        sender = result['sender_id']
        content = result['content']
        chat = sender + " said: " + content
        print chat
        socketio.emit('broad cast', chat)


# 在客户端建立建立连接之后，通过触发此方法进行不同的操作，例如向'broad cast'时间发送消息
@socketio.on('connect')
def clientconnected():
    socketio.emit('broad cast', "msg")
    print 'connected'

# 通过'broad cast'向已经建立简介的客户端广播消息
@socketio.on('broad cast')
def castinfo(data):
    emit('broad cast', data, broadcast=True)



# ＝＝＝＝＝＝＝关于最新火箭信息的触发和广播＝＝＝＝＝＝＝ #


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=3000)
