#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-07-14 10:20:40
# @Author  : Wangmengcn (eclipse_sv@163.com)
# @Link    : https://eclipsesv.com
# @Version : $0.1$
from flask import Flask, jsonify
from flask import render_template
from getmsg import HotRoom, GetUserinfo, getAllTags
import getmsg

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


@app.route('/api/v1.0/tags')
def getTags():
    tags = getAllTags()
    if tags:
        return jsonify(boradCast=tags)
    else:
        return "There is no data aviliable!", 404


@app.route('/api/v1.0/online')
def getOnline():
    onlineinfo = getmsg.getOnline()
    return jsonify(onlinedata=onlineinfo) if onlineinfo else None


@app.route('/api/v1.0/online/<string:tag>')
def getTaginfo(tag):
    if tag:
        taginfo, anchorinfo = getmsg.getTaginfo(tag)
        return jsonify(anchorinfo=anchorinfo, tag=taginfo['tag'], audience=taginfo['audience']) \
            if taginfo else "There is no data aviliable!"


@app.route('/api/v1.0/anchors')
def getAnchors():
    anchors = getmsg.getAnchors()
    return jsonify(anchors=anchors) if anchors \
        else "There is no data aviliable!"


@app.route('/api/v1.0/anchor/<string:anchor>')
def getAnchorInfo(anchor):
    if anchor:
        anchorinfo = getmsg.getAnchorinfo(anchor)
        return jsonify(anchorinfo=anchorinfo) if anchorinfo else "There is no data aviliable!"
    else:
        return "There is no data aviliable!"

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=4000)
