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

result = sorted(c.iteritems(), key=lambda d: d[1], reverse=True)
rresult = sorted(d.iteritems(), key=lambda d: d[1], reverse=True)

for item in result:
    print item[0], ' sends ', item[1], 'gifts!'
for item in rresult:
	print item[0],' gets ',item[1],'gifts!'