#! /user/bin/env python
# -*- coding:utf-8 -*-
from apscheduler.schedulers.background import BackgroundScheduler
import subprocess
import os
from datetime import datetime
import time
import logging

logging.basicConfig(level=logging.DEBUG)


def tick_list():
    logging.debug('启动爬虫! The time is: %s' % datetime.now())
    app_path = os.path.dirname(os.path.realpath(__file__))
    subprocess.Popen("scrapy crawl categorySpider", shell=True, cwd=app_path)


def tick_challenge():
    logging.debug('启动 热门挑战 爬虫! The time is: %s' % datetime.now())
    subprocess.Popen("scrapy crawl categoryVideoSpider")


def tick_music():
    logging.debug('启动 热门音乐 爬虫! The time is: %s' % datetime.now())
    subprocess.Popen("scrapy crawl douyinSpider")


if __name__ == '__main__':
    logging.debug(
        '======================程序启动！The time is: %s =======================' %
        datetime.now())
    tick_list()
