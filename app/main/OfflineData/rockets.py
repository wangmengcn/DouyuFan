#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-07-14 10:20:40
# @Author  : Wangmengcn (eclipse_sv@163.com)
# @Link    : https://eclipsesv.com
# @Version : $0.1$

import pymongo
from pymongo import MongoClient

client = MongoClient()
db = client['Douyu']
col = db['rocket']

