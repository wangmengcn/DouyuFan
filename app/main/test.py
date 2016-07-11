#-*- coding:UTF-8-*-
# test.py用以测试新增功能
from getmsg import RocketRoom

roominfo = RocketRoom(757104)
if roominfo:
	print type(roominfo)
	print roominfo