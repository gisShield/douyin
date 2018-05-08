# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
import json
from scrapy.conf import settings
from douyin.items import DouyinCategoryItem
from douyin.utils.tools import MyTools
from douyin.utils.tools import DBTools
# 分类信息保存


class DouyinPipeline(object):
    def __init__(self):
        '''host = settings['MONGODB_HOST']  # settings 赋值piplines
        port = settings['MONGODB_PORT']
        dbName = settings['MONGODB_DBNAME']  # 数据库名字
        client = pymongo.MongoClient(host=host, port=port)  # 链接数据库
        tdb = client[dbName]'''
        db_con_video = DBTools('video')
        db_con_category = DBTools('category')
        self.post_video = db_con_video.get_db_con()
        self.post_category = db_con_category.get_db_con()

    def process_item(self, item, spider):
        if spider.name == 'categorySpider':
            result = self.post_category.find(
                {'category_id': item['category_id']})
            print("入库操作")
            if result.count() > 0:
                self.post_category.update(
                    {'category_id': item['category_id']}, dict(item))  # 更新操作
            else:
                self.post_category.insert(dict(item))  # 插入操作

            return item
        elif spider.name == 'categoryVideoSpider'or spider.name == 'douyinSpider':
            result = self.post_video.find({'video_id': item['video_id']})
            print("入库操作")
            if result.count() > 0:
                self.post_video.update(
                    {'category_id': item['video_id']}, dict(item))  # 更新操作
            else:
                self.post_video.insert(dict(item))  # 插入操作

            return item
