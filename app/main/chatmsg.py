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
# broadcast.run_in_thread(sleep_time=0.001)


def info():
    broadcast = redis.pubsub()
    broadcast.subscribe('rocketinfo')
    for message in broadcast.listen():
        if message:
            socketio.emit('chat msg', str(message))
            print message


def convertData(data):
	if data:
		try:
			result = eval(data)
			print type(result)
			print result
		except Exception, e:
			raise e



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


@socketio.on('connect')
def clientconnected():
    socketio.emit('broad cast', "msg")
    # info()
    print 'connected'


@socketio.on('broad cast')
def castinfo(data):
    emit('broad cast', data, broadcast=True)




if __name__ == '__main__':
    socketio.run(app,host='0.0.0.0', port=3000)
