#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-07-22 23:53:40
# @Author  : Wangmengcn (eclipse_sv@163.com)
# @Link    : https://eclipsesv.com
# @Version : $0.1$

from bs4 import BeautifulSoup
import re
import requests
from datetime import datetime
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


def get_roominfo(data):
    if data:
        firstpage = BeautifulSoup(data)
        roomlist = firstpage.select('li')
        print len(roomlist)
        if roomlist:
            for room in roomlist:
                try:
                    roomid = room["data-rid"]
                    roomtitle = room.a["title"]
                    roomtitle = roomtitle.encode('utf-8')
                    roomowner = room.select("p > span")
                    roomtag = room.select("div > span")
                    roomimg = room.a
                    roomtag = roomtag[0].string
                    date = datetime.now()
                    # now = datetime.datetime(
                    # date.year, date.month, date.day, date.hour, date.minute)
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
                except Exception, e:
                    pass


def aggregateData():
    '''
    通过mongodb自带的aggregation()将关于主播和分类的数据装载到两个不同的表中，以供后用
    '''
    sortbyKind = [{"$project": {'audience': 1, 'tag': 1, 'date': 1}}, {
        "$group": {"_id": '$tag', "sum": {"$sum": '$audience'}}}]
    sortbyAnchor = [{"$project": {'date': 1, 'audience': 1, 'roomid': 1,
                                  'anchor': 1, 'tag': 1, '_id': 0}}, {"$out": 'anchorRecord'}]
    col.aggregate(sortbyAnchor)
    tagsinfo = col.aggregate(sortbyKind)
    kindRecord = db['kindRecord']
    for item in tagsinfo:
        kindinfo = {
            "date": datetime.now(),
            "audience": item['sum'],
            "tag": item['_id']
        }
        kindRecord.insert_one(kindinfo)


def insert_info():
    session = requests.session()
    pagecontent = session.get(Directory_url).text
    pagesoup = BeautifulSoup(pagecontent)
    games = pagesoup.select('a')
    col.drop()
    for game in games:
        links = game["href"]
        pagecount = 1
        initdata = None
        originURL = HOST + links + "/?page=1&isAjax=1"
        while True:
            Qurystr = "/?page=" + str(pagecount) + "&isAjax=1"
            gameurl = HOST + links + Qurystr
            print gameurl
            if pagecount == 1:
                gamedata = session.get(gameurl).text
                initdata = gamedata
            else:
                gamedata = session.get(gameurl).text
                origindata = session.get(originURL).text
                if initdata == origindata:
                    break
            get_roominfo(gamedata)
            pagecount = pagecount + 1
            print pagecount
    aggregateData()

insert_info()
