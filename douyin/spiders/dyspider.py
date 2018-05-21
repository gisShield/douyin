#! /user/bin/env python
# -*- coding:utf-8 -*-

import json

from douyin.items import DouyinItem
from scrapy.http import Request
from scrapy.spiders import CrawlSpider

from douyin.utils.tools import DBTools
from douyin.utils.tools import MyTools


class douyinSpider(CrawlSpider):
    name = 'douyinSpider'
    redis_key = 'douyinSpider'
    cursor_num = 0
    count_size = 20
    i = 0
    urls = 'https://api.amemv.com/aweme/v1/music/aweme/?count=20&cursor=%d&music_id=%s&device_id=%s'
    ids = []
    new_video_id = ''
    flag = False

    def __init__(self):
        # 查询满足的列表ids集合，组织urls
        super(douyinSpider, self).__init__()
        db_con = DBTools('category')
        self.post = db_con.get_db_con()

        db_video_con = DBTools('video')
        self.video_post = db_video_con.get_db_con()

        list = self.post.find({"category_type": "热门音乐"}).sort([{"category_user_count",-1}])
        for obj in list:
            self.ids.append(str(obj['category_id']))

        self.start_urls = [self.urls % (self.cursor_num, str(
            self.ids[self.i]), MyTools.init_device_id())]
        #self.new_video_id = self.getNewVideoId(str(self.ids[self.i]))

    def parse(self, response):
        print('抓取数据开始...')
        jsonresp = json.loads(response.body_as_unicode())
        if jsonresp['status_code'] == 0:
            if jsonresp['has_more'] == 1:
                aweme_list = list(jsonresp['aweme_list'])
                for jsonobj in aweme_list:
                    '''if self.notUpdate(self.ids[self.i],jsonobj):
                        break
                    else:'''
                    item = self.init_item(jsonobj, self.ids[self.i])
                    yield item
                self.cursor_num += self.count_size
                nexturl = self.urls % (self.cursor_num,
                                       self.ids[self.i],
                                       MyTools.init_device_id())
                yield Request(nexturl, callback=self.parse)
            else:
                aweme_list = list(jsonresp['aweme_list'])
                for jsonobj in aweme_list:
                    '''if self.notUpdate(self.ids[self.i], jsonobj):
                        break
                    else:'''
                    item = self.init_item(jsonobj, self.ids[self.i])
                    yield item
                self.i += 1
                self.cursor_num = 0
                if self.i < len(self.ids):
                    # self.getNewVideoId(str(self.ids[self.i]))
                    nexturl = self.urls % (
                        self.cursor_num, self.ids[self.i], MyTools.init_device_id())
                    yield Request(nexturl, callback=self.parse)

        else:
            self.i += 1
            self.cursor_num = 0
            if self.i < len(self.ids):
                # self.getNewVideoId(str(self.ids[self.i]))
                nexturl = self.urls % (self.cursor_num,
                                       self.ids[self.i],
                                       MyTools.init_device_id())
                yield Request(nexturl, callback=self.parse)
            else:
                pass

    def init_item(self, jsonobj, category_uid):
        item = DouyinItem()
        item['category_id'] = str(category_uid)
        item['user_uid'] = str(jsonobj['author']['uid'])
        item['user_sid'] = str(jsonobj['author']['short_id'])
        item['user_birthday'] = str(jsonobj['author']['birthday'])
        item['user_gender'] = jsonobj['author']['gender']

        item['video_id'] = str(jsonobj['aweme_id'])
        item['video_desc'] = str(jsonobj['desc'])
        item['video_play'] = jsonobj['statistics']['play_count']
        item['video_comment'] = jsonobj['statistics']['comment_count']
        item['video_share'] = jsonobj['statistics']['share_count']
        item['video_digg'] = jsonobj['statistics']['digg_count']
        item['video_durl'] = str(
            jsonobj['video']['download_addr']['url_list'][0])
        item['video_gurl'] = str(
            jsonobj['video']['dynamic_cover']['url_list'][0])
        item['video_time'] = MyTools.transform_time(jsonobj['create_time'])
        return item

    def notUpdate(self, categoryid, jsonobj):
        if str(categoryid) == str(jsonobj['aweme_id']):
            return True
        else:
            return False

    def getNewVideoId(self, categoryid):
        list = self.video_post.find(
            {"category_id": str(categoryid)}).sort([{"video_time", -1}])
        for obj in list:
            self.new_video_id = obj['video_id']
            break
