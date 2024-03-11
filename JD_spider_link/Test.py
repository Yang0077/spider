import concurrent.futures
import threading
import time

from JD_spider_link.spider.JdSpider import start_jd_spider
from JD_spider_link.spider.LoginAndGetCookie import login_and_cookies
from JD_spider_link.analyze.AnalyzeSentiment import *
from JD_spider_link.analyze.CleanData import *
from JD_spider_link.analyze.CreateWordCloud import *


def start(link):
    global_driver = login_and_cookies()
    ks = time.time()
    try:
        # 爬取数据
        ret_data, good_id = start_jd_spider(global_driver)

        # 保存数据->mongo 原始数据
        collection_name = 'original_data'
        mongo_insert(ret_data, collection_name)

        # 清洗数据
        cl_data = clean_data(good_id)
        # 画词云图
        # create_wordCloud(cl_data, good_id)
        # 情感分析
        analyze_sentiment(good_id)

    except Exception as e:
        # 打印错误
        print("错误信息---" + str(e))
        pass

    print("运行时间：{:.2f}s".format((time.time() - ks)))


def start_in_thread(link):
    thread = threading.Thread(target=start, args=(link,))
    thread.start()


if __name__ == '__main__':
    # links = ['https://item.jd.com/100017568399.html',
    #          'https://item.jd.com/100031192620.html',
    #          'https://item.jd.com/100014352501.html', 'https://item.jd.com/100041239034.html']
    # links = ['https://item.jd.com/100023070523.html', 'https://item.jd.com/100057334060.html',
    #          'https://item.jd.com/100066896392.html']
    links = ['https://item.jd.com/100066896214.html', 'https://item.jd.com/100066896396.html',
             'https://item.jd.com/100066896468.html', 'https://item.jd.com/100066896220.html',
             'https://item.jd.com/100046043036.html', 'https://item.jd.com/100066896262.html']
    start('https://item.jd.com/100066896396.html')

    for link in links:
        time.sleep(1)
