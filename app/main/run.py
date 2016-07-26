#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-07-14 10:20:40
# @Author  : Wangmengcn (eclipse_sv@163.com)
# @Link    : https://eclipsesv.com
# @Version : $0.1$
from flask import Flask, jsonify
from flask import render_template
from getmsg import HotRoom, GetUserinfo

app = Flask(__name__)

# this part is for normal requests


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/chatmsg')
def chatmsg():
    rooms = HotRoom()
    return render_template('gift.html', hotroom=rooms, flag=0)


@app.route('/history')
def history():
    return render_template('history.html')


@app.route('/tv/<int:roomid>')
def tvstream(roomid):
    if roomid:
        return render_template('tv.html', roomid=roomid)


# this part is for restful requests

@app.route('/api/v1.0/user/<string:username>')
def getUserinfo(username):
    if username is not None:
    	print username
        userinfo = GetUserinfo(username)
        return jsonify({'userinfo': userinfo})
    else:
        return "There is no data aviliable!", 404

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=4000)
