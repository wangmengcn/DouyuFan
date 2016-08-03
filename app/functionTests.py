#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-07-29 17:04:24
# @Author  : Wangmengcn (eclipse_sv@163.com)
# @Link    : https://eclipsesv.com
# @Version : $Id$chromedriver

import unittest
from pymongo import MongoClient
import redis
from main import getmsg


class FlaskUnitTest(unittest.TestCase):
    """A Class built for testing"""

    def setUp(self):
        self.client = MongoClient()
        self.db = self.client['Douyu']
        self.redis = redis.StrictRedis(password='abc@123')

    def tearDown(self):
        self.client.close()

    def test_mongo_getTags(self):
        col = self.db['kindRecord']
        tags = col.distinct('tag')
        self.assertEqual(tags, getmsg.getAllTags())

    def test_mongo_getOnline(self):
        col = self.db['Roominfo']
        sortbyKind = [{"$project": {'audience': 1, 'tag': 1, 'date': 1}}, {
            "$group": {"_id": '$tag', "sum": {"$sum": '$audience'}}}]
        onlineinfo = col.aggregate(sortbyKind)
        result = [{'tag': item['_id'], 'online':item['sum']}
                  for item in onlineinfo]
        self.assertEqual(result, getmsg.getOnline())

    def test_mongo_hotroom(self):
        self.assertEqual(21, len(getmsg.HotRoom()))


if __name__ == '__main__':
    unittest.main()
