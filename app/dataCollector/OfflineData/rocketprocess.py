#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-07-14 23:20:46
# @Author  : Wangmengcn (eclipse_sv@163.com)
# @Link    : https://eclipsesv.com
# @Version : $Id$
# rocketprocess 用以在每天凌晨00:05的时候，处理前一整天的火箭数据

from pymongo import MongoClient
from datetime import datetime

client = MongoClient()
db = client['Douyu']
col = db['rocket']
byday = db['rocketbyDay']


# 声明枚举时间
hour = range(0, 24)


def sortbyDay():
    today = datetime.today()
    year = today.year
    m = today.month
    d = today.day
    singledate = datetime(year, m, d - 1)
    print singledate
    singledata = []
    count = 0
    for h in hour:
        data = []
        value = {}
        start = datetime(year, m, d - 1, h, 0, 0)
        end = datetime(year, m, d - 1, h, 59, 59)
        daydata = col.find(
            {'date': {'$gt': start, '$lt': end}}, {'_id': 0})
        if daydata is not None:
            for item in daydata:
                data.append(item)
                count = count + 1
        else:
            data = None
        value['hour'] = h
        value['rockets'] = data
        singledata.append(value)
    if count != 0:
        insertdata = {
            'date': singledate,
            'data': singledata,
            'count': count
        }
        byday.insert_one(insertdata)

sortbyDay()
