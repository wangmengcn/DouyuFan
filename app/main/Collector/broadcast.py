#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-07-14 10:20:40
# @Author  : Wangmengcn (eclipse_sv@163.com)
# @Link    : https://eclipsesv.com
# @Version : $0.1$
import redis
redis = redis.StrictRedis(password='abc@123')

# 将获取到的弹幕信息通过redis publish出去


def castChat(data):
    if data:
        redis.publish('chatinfo', data)

# 将获取到的火箭信息通过redis publish出去


def castRocket(data):
    if data:
        redis.publish('rocketinfo', data)
