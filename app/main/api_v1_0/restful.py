#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-08-04 22:04:16
# @Author  : Wangmengcn (eclipse_sv@163.com)
# @Link    : https://eclipsesv.com
# @Version : $Id$

import sys
sys.path.append('..')

from flask import jsonify
from . import api
import getmsg


# this part is for restful requests

@api.route('/user/<string:username>')
def getUserinfo(username):
    if username is not None:
        print username
        userinfo = getmsg.GetUserinfo(username)
        return jsonify({'userinfo': userinfo})
    else:
        return "There is no data aviliable!", 404


@api.route('/tags')
def getTags():
    tags = getmsg.getAllTags()
    if tags:
        return jsonify(boradCast=tags)
    else:
        return "There is no data aviliable!", 404


@api.route('/online')
def getOnline():
    onlineinfo = getmsg.getOnline()
    return jsonify(onlinedata=onlineinfo) if onlineinfo else None


@api.route('/online/<string:tag>')
def getTaginfo(tag):
    if tag:
        taginfo, anchorinfo = getmsg.getTaginfo(tag)
        return jsonify(anchorinfo=anchorinfo, tag=taginfo['tag'], audience=taginfo['audience']) \
            if taginfo else "There is no data aviliable!"


@api.route('/anchors')
def getAnchors():
    anchors = getmsg.getAnchors()
    return jsonify(anchors=anchors) if anchors \
        else "There is no data aviliable!"


@api.route('/anchor/<string:anchor>')
def getAnchorInfo(anchor):
    if anchor:
        anchorinfo = getmsg.getAnchorinfo(anchor)
        return jsonify(anchorinfo=anchorinfo) if anchorinfo else "There is no data aviliable!"
    else:
        return "There is no data aviliable!"
