# this is for getting message from redis subscribe and send it to socketio
# server


from flask import Flask, render_template
from flask_socketio import SocketIO
from flask_socketio import send, emit
import redis
import time

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
socketio = SocketIO(app)

redis = redis.StrictRedis(host='123.206.211.77',
                          port='6379', db=0, password='abc@123')
broadcast = redis.pubsub()
broadcast.subscribe('rocketinfo')


@socketio.on('chat msg')
def getmsg(message):
    print('received msg:' + str(message))
    while True:
        for i in range(1, 100):
            emit('chat msg', str(i), broadcast=True)
        emit('chat msg', "pause", broadcast=True)
        break
    # broadcast = redis.pubsub()
    # broadcast.subscribe('rocketinfo')
    # for message in broadcast.listen():
    #     if message:
    #         emit('chat msg', str(message))
    # emit('chat msg', str(message), broadcast=True)





if __name__ == '__main__':
    socketio.run(app, port=3000)
