#! /user/bin/env python
# -*- coding:utf-8 -*-
'''
    爬取列表信息
'''
import json

from scrapy.http import Request
from scrapy.spiders import CrawlSpider

from douyin.items import DouyinCategoryItem


class categorySpider(CrawlSpider):
    name = 'categorySpider'
    redis_key = 'categorySpider'
    cursor_num = 0
    count_size = 10
    url = "https://aweme.snssdk.com/aweme/v1/category/list/?version_code=181&count=10&cursor="
    start_urls = [url + str(cursor_num)]

    def parse(self, response):
        jsonresp = json.loads(response.body_as_unicode())
        if jsonresp['status_code'] == 0:
            if jsonresp['has_more'] == 1:
                aweme_list = list(jsonresp['category_list'])
                for jsonobj in aweme_list:
                    item = self.init_item(jsonobj)
                    yield item
                self.cursor_num += self.count_size
                nexturl = self.url + str(self.cursor_num)
                yield Request(nexturl, callback=self.parse)
            else:
                aweme_list = list(jsonresp['category_list'])
                for jsonobj in aweme_list:
                    item = self.init_item(jsonobj)
                    yield item

    def init_item(self, jsonobj):
        item = DouyinCategoryItem()
        if str(jsonobj['desc']) == "热门挑战":
            item['category_type'] = jsonobj['desc']
            item['category_id'] = jsonobj['challenge_info']['cid']
            item['category_desc'] = jsonobj['challenge_info']['desc']
            item['category_title'] = jsonobj['challenge_info']['cha_name']
            item['category_url'] = jsonobj['challenge_info']['schema']
            item['category_user_count'] = jsonobj['challenge_info']['user_count']
        else:
            # print("执行热门音乐赋值")
            item['category_type'] = jsonobj['desc']
            item['category_title'] = jsonobj['music_info']['title']
            item['category_id'] = jsonobj['music_info']['mid']
            item['category_url'] = 'https://api.amemv.com/aweme/v1/music/aweme/?music_id=' + \
                str(jsonobj['music_info']['mid'])
            item['category_desc'] = jsonobj['music_info']['offline_desc']
            item['category_user_count'] = jsonobj['music_info']['user_count']
        return item
