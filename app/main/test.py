#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-07-14 10:20:40
# @Author  : Wangmengcn (eclipse_sv@163.com)
# @Link    : https://eclipsesv.com
# @Version : $0.1$
# test.py用以测试新增功能
from getmsg import valuebyHour, sortbyDay
from datetime import datetime
day = datetime.today()
(a, b, c, d) = valuebyHour(day)
print a
print b
print type(c)
print type(d)
