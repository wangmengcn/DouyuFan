#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-07-29 17:04:24
# @Author  : Wangmengcn (eclipse_sv@163.com)
# @Link    : https://eclipsesv.com
# @Version : $Id$chromedriver

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
import time


fp = webdriver.FirefoxProfile(
    r'/Users/eclipse/Library/Application Support/Firefox/Profiles/tmsbsjpg.default')
browser = webdriver.Firefox(fp)
browser.implicitly_wait(15)  # seconds
browser.get("http://www.douyu.com/56229")
indexvideo = browser.find_element_by_class_name('cs-textarea')
print type(indexvideo)
indexvideo.send_keys('2333333333333')
print indexvideo
time.sleep(7)
sendbut = browser.find_element_by_class_name('b-btn')
ActionChains(browser).move_to_element(indexvideo).click(sendbut).perform()
gift = browser.find_element_by_class_name('peck-cdn')
while True:
	ActionChains(browser).move_to_element(gift).click(gift).perform()
	time.sleep(2)

