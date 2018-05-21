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
    app_path = os.path.dirname(os.path.realpath(__file__))
    subprocess.Popen(
        "scrapy crawl categoryVideoSpider",
        shell=True,
        cwd=app_path)


def tick_music():
    logging.debug('启动 热门音乐 爬虫! The time is: %s' % datetime.now())
    app_path = os.path.dirname(os.path.realpath(__file__))
    subprocess.Popen("scrapy crawl douyinSpider", shell=True, cwd=app_path)


if __name__ == '__main__':
    logging.debug(
        '======================程序启动！The time is: %s =======================' %
        datetime.now())
    scheduler = BackgroundScheduler()
    scheduler.add_job(tick_list, 'cron', day='*', hour=0, minute=30)  # 每天凌晨更新

    scheduler.add_job(tick_challenge, 'cron', day='*', hour=2, minute=0)
    scheduler.add_job(tick_music, 'cron', day='*', hour=3, minute=0)
    scheduler.start()  # 这里的调度任务是独立的一个线程
    print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))

    try:
        # This is here to simulate application activity (which keeps the main
        # thread alive).
        while True:
            time.sleep(2)  # 其他任务是独立的线程执行
            print('sleep!')
    except (KeyboardInterrupt, SystemExit):
        # Not strictly necessary if daemonic mode is enabled but should be done
        # if possible
        scheduler.shutdown()
        logging.debug('Exit The Job!')
        print('Exit The Job!')
