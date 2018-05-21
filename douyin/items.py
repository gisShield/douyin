# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html
import scrapy


class DouyinItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    # 挑战唯一标识
    category_id = scrapy.Field()
    # 用户信息
    # 用户id
    user_uid = scrapy.Field()
    # 用户短ID
    user_sid = scrapy.Field()
    # 注册出生日期
    user_birthday = scrapy.Field()
    # 性别
    user_gender = scrapy.Field()

    # 视频信息
    # 视频ID
    video_id = scrapy.Field()
    # 视频描述
    video_desc = scrapy.Field()
    # 视频播放量
    video_play = scrapy.Field()
    # 评论量
    video_comment = scrapy.Field()
    # 分享量
    video_share = scrapy.Field()
    # 点赞量
    video_digg = scrapy.Field()
    # 视频下载地址
    video_durl = scrapy.Field()
    # 视频封面地址
    video_gurl = scrapy.Field()

    video_time = scrapy.Field()


class DouyinCategoryItem(scrapy.Item):
    # 类型：desc中的内容：热门音乐/热门挑战
    category_type = scrapy.Field()
    category_title = scrapy.Field()
    category_id = scrapy.Field()
    category_url = scrapy.Field()
    category_desc = scrapy.Field()
    category_user_count = scrapy.Field()
