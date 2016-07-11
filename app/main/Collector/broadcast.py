#-*- coding: UTF-8 -*-
import redis
redis = redis.StrictRedis(host='123.206.211.77',
                          port='6379', db=0, password='abc@123')

# 将获取到的弹幕信息通过redis publish出去


def castChat(data):
    if data:
        redis.publish('chatinfo', data)

# 将获取到的火箭信息通过redis publish出去


def castRocket(data):
    if data:
        redis.publish('rocketinfo', data)
