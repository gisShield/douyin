#! /user/bin/env python
# -*- coding:utf-8 -*-
import pymongo
import json
import random
import time
from scrapy.conf import settings


class DBTools:
    '''
        数据库链接类
    '''
    host = settings['MONGODB_HOST']  # settings 赋值piplines
    port = settings['MONGODB_PORT']
    dbName = settings['MONGODB_DBNAME']  # 数据库名字
    client = pymongo.MongoClient(host=host, port=port)  # 链接数据库
    tdb = client[dbName]

    def __init__(self, name):
        print('name:',name)
        self.post = self.tdb[name]

    def get_db_con(self):
        return self.post


class MyTools:
    '''
        基础工具类
    '''
    def init_device_id():
        value = random.randint(1000000000, 9999999999)
        return str(value)

    def transform_time(u_time):
        timeArray = time.localtime(u_time)
        otherStyleTime = time.strftime("%Y/%m/%d %H:%M:%S", timeArray)
        return otherStyleTime
