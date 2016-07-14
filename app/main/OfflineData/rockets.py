#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-07-14 10:20:40
# @Author  : Wangmengcn (eclipse_sv@163.com)
# @Link    : https://eclipsesv.com
# @Version : $0.1$
# rockets 用以处理通过爬虫获取到的火箭信息，以天为单位，记录没天没个小时🚀发送的信息

from pymongo import MongoClient
from datetime import datetime

client = MongoClient(host='123.206.211.77', port=27017)
db = client['Douyu']
col = db['rocket']
byday = db['rocketbyDay']


# 声明枚举时间
year = 2016
bigmonth = [1, 3, 5, 7, 8, 10, 12]
month = [5, 6, 7]
bigday = range(1, 32)
smallday = range(1, 31)
hour = range(0, 24)


def sortbyDay():
    for m in month:
        if m in bigmonth:
            day = bigday
        else:
            day = smallday
        for d in day:
            singledate = datetime(year, m, d)
            print singledate
            singledata = []
            count = 0
            for h in hour:
                data = []
                value = {}
                start = datetime(year, m, d, h, 0, 0)
                end = datetime(year, m, d, h, 59, 59)
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
