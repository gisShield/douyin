#! /user/bin/env python
# -*- coding:utf-8 -*-
from apscheduler.schedulers.background import BackgroundScheduler
import subprocess
import os
from datetime import datetime
import time


def tick_list():
    print('启动爬虫! The time is: %s' % datetime.now())
    subprocess.Popen("scrapy crawl categorySpider")


def tick_challenge():
    print('启动 热门挑战 爬虫! The time is: %s' % datetime.now())
    subprocess.Popen("scrapy crawl categoryVideoSpider")


def tick_music():
    print('启动 热门音乐 爬虫! The time is: %s' % datetime.now())
    subprocess.Popen("scrapy crawl douyinSpider")


if __name__ == '__main__':
    scheduler = BackgroundScheduler()
    scheduler.add_job(tick_list, 'cron', day='*', hour=0, minute=0)  # 每天凌晨执行

    scheduler.add_job(tick_challenge, 'cron', day='*', hour=1, minute=0)
    scheduler.add_job(tick_music, 'cron', day='*', hour=1, minute=30)
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
        print('Exit The Job!')
