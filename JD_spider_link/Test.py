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
        ret_data, good_id = start_jd_spider(global_driver, link)

        # 保存数据->mongo 原始数据
        collection_name = 'original_data'
        mongo_insert(ret_data, collection_name)

        # 清洗数据
        cl_data = clean_data(good_id)
        # 画词云图
        create_wordCloud(cl_data, good_id)
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
    links = ['https://item.jd.com/100014348458.html', 'https://item.jd.com/100017568399.html',
             'https://item.jd.com/100011493273.html', 'https://item.jd.com/100031192620.html',
             'https://item.jd.com/100014352501.html', 'https://item.jd.com/100041239034.html']
    # 启动多线程执行start函数
    # 为每个链接设置启动间隔
    for i, link in enumerate(links):
        if i != 0:
            time.sleep(60)  # 在启动每个线程之前等待十秒
        start_in_thread(link)



