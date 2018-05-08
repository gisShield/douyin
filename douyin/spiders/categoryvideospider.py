#! /user/bin/env python
# -*- coding:utf-8 -*-

import json
from scrapy.spiders import CrawlSpider
from scrapy.http import Request
from douyin.items import DouyinItem
from douyin.utils.tools import MyTools
from douyin.utils.tools import DBTools


class categoryVideoSpider(CrawlSpider):

    name = 'categoryVideoSpider'
    redis_key = 'categoryVideoSpider'
    cursor_num = 0
    count_size = 20
    i = 0
    urls = 'https://aweme.snssdk.com/aweme/v1/challenge/aweme/?query_type=0&count=20&aid=1128&cursor=%d&ch_id=%s&device_id=%s'
    ids = []

    def __init__(self):
        # 查询满足的列表ids集合，组织urls
        super(categoryVideoSpider, self).__init__()
        db_con = DBTools('category')
        self.post = db_con.get_db_con()
        list = self.post.find({"category_type": "热门挑战"}).sort([{"category_user_count",-1}]).limit(50)
        for obj in list:
            self.ids.append(str(obj['category_id']))

        self.start_urls = [self.urls % (self.cursor_num, str(
            self.ids[self.i]), MyTools.init_device_id())]

    def parse(self, response):
        print('抓取数据开始...')
        jsonresp = json.loads(response.body_as_unicode())
        if jsonresp['status_code'] == 0:
            if jsonresp['has_more'] == 1:
                aweme_list = list(jsonresp['aweme_list'])
                for jsonobj in aweme_list:
                    item = self.init_item(jsonobj)
                    yield item
                self.cursor_num += self.count_size
                nexturl = self.urls % (self.cursor_num,
                                       self.ids[self.i],
                                       MyTools.init_device_id())
                yield Request(nexturl, callback=self.parse)
            else:
                self.i += 1
                self.cursor_num = 0
                if self.i < len(self.ids):
                    nexturl = self.urls % (
                        self.cursor_num, self.ids[self.i], MyTools.init_device_id())
                    yield Request(nexturl, callback=self.parse)
                else:
                    pass

        else:
            self.i += 1
            self.cursor_num = 0
            if self.i < len(self.ids):
                nexturl = self.urls % (self.cursor_num,
                                       self.ids[self.i],
                                       MyTools.init_device_id())
                yield Request(nexturl, callback=self.parse)
            else:
                pass

    def init_item(self, jsonobj):
        item = DouyinItem()
        item['user_uid'] = jsonobj['author']['uid']
        item['user_sid'] = jsonobj['author']['short_id']
        item['user_birthday'] = jsonobj['author']['birthday']
        item['user_gender'] = jsonobj['author']['gender']

        item['video_id'] = jsonobj['aweme_id']
        item['video_desc'] = jsonobj['desc']
        item['video_play'] = jsonobj['statistics']['play_count']
        item['video_comment'] = jsonobj['statistics']['comment_count']
        item['video_share'] = jsonobj['statistics']['share_count']
        item['video_digg'] = jsonobj['statistics']['digg_count']
        item['video_durl'] = jsonobj['video']['download_addr']['url_list'][0]
        item['video_gurl'] = jsonobj['video']['dynamic_cover']['url_list'][0]
        item['video_time'] = MyTools.transform_time(jsonobj['create_time'])
        return item
