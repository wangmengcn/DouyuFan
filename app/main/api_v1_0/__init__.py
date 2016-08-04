#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-08-04 21:43:34
# @Author  : Wangmengcn (eclipse_sv@163.com)
# @Link    : https://eclipsesv.com
# @Version : $Id$

from flask import Blueprint
api = Blueprint("api", __name__)

from . import restful