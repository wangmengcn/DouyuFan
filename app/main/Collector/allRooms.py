#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-07-22 23:53:40
# @Author  : Wangmengcn (eclipse_sv@163.com)
# @Link    : https://eclipsesv.com
# @Version : $0.1$


import re
from datetime import datetime
import time
from multiprocessing.dummy import Pool
import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient


HOST = "http://www.douyu.com"
Directory_url = "http://www.douyu.com/directory?isAjax=1"
Qurystr = "/?page=1&isAjax=1"

agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.86 Safari/537.36'
accept = "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
connection = "keep-alive"
CacheControl = "no-cache"
UpgradeInsecureRequests = 1
headers = {
    'User-Agent': agent,
    'Host': HOST,
    'Accept': accept,
    'Cache-Control': CacheControl,
    'Connection': connection,
    'Upgrade-InsecureRequests': UpgradeInsecureRequests
}

cli = MongoClient()
db = cli["Douyu"]
col = db["Roominfo"]

pool = Pool()


def get_roominfo(data):
    if data:
        firstpage = BeautifulSoup(data)
        roomlist = firstpage.select('li')
        if roomlist:
            for room in roomlist:
                try:
                    roomid = room["data-rid"]
                    print roomid
                    if col.find({'roomid': int(roomid)}).count() != 0:
                        return False
                    else:
                        roomtitle = room.a["title"]
                        roomtitle = roomtitle.encode('utf-8')
                        roomowner = room.select("p > span")
                        roomtag = room.select("div > span")
                        roomimg = room.a
                        roomtag = roomtag[0].string
                        date = datetime.now()
                        if len(roomowner) == 2:
                            zbname = roomowner[0].string
                            audience = roomowner[1].get_text()
                            audience = audience.encode('utf-8').decode('utf-8')
                            image = roomimg.span.img["data-original"]
                            word = u"万"
                            if word in audience:
                                r = re.compile(r'(\d+)(\.?)(\d*)')
                                data = r.match(audience).group(0)
                                audience = int(float(data) * 10000)
                            else:
                                audience = int(audience)
                            roominfo = {
                                "roomid": int(roomid),
                                "roomtitle": roomtitle,
                                "anchor": zbname,
                                "audience": audience,
                                "tag": roomtag,
                                "date": date,
                                "img": image
                            }
                            col.insert_one(roominfo)
                    # print roomid,":",roomtitle
                except Exception:
                    return False
            return True
        else:
            return False
    else:
        return False


def aggregateData():
    '''
    通过mongodb自带的aggregation()将关于主播和分类的数据装载到两个不同的表中，以供后用
    要注意的是：使用$out操作符会覆盖原有collection！
    '''
    sortbyKind = [{"$project": {'audience': 1, 'tag': 1, 'date': 1}}, {
        "$group": {"_id": '$tag', "sum": {"$sum": '$audience'}}}]

    sortbyAnchor = [{"$project": {'date': 1, 'audience': 1, 'roomid': 1,
                                  'anchor': 1, 'tag': 1, '_id': 0}}]
    anchors = col.aggregate(sortbyAnchor)
    tagsinfo = col.aggregate(sortbyKind)
    anchorinfo = db['anchorRecord']
    kindRecord = db['kindRecord']
    for item in tagsinfo:
        kindinfo = {
            "date": datetime.now(),
            "audience": item['sum'],
            "tag": item['_id']
        }
        kindRecord.insert_one(kindinfo)
    for item in anchors:
        anchordata = {
            "date": datetime.now(),
            "audience": item['audience'],
            "roomid": item['roomid'],
            "anchor": item['anchor'],
            "tag": item['tag']
        }
        anchorinfo.insert_one(anchordata)


def insert_info():
    '''
    通过遍历游戏分类页面获取所有直播间
    '''
    session = requests.session()
    pagecontent = session.get(Directory_url).text
    pagesoup = BeautifulSoup(pagecontent)
    games = pagesoup.select('a')
    gameurl = [HOST + url["href"] + "/?page=1&isAjax=1" for url in games]
    col.drop()
    g = lambda link: session.get(link).text
    gamedata = pool.map(g, gameurl)
    ginfo = lambda data: get_roominfo(data)
    pool.map(ginfo, gamedata)
    aggregateData()

insert_info()
