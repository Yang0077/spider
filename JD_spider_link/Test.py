import concurrent.futures
import threading
import time

from selenium.webdriver.common.by import By

from JD_spider_link.spider.JdSpider import start_jd_spider
from JD_spider_link.spider.LoginAndGetCookie import login_and_cookies
from JD_spider_link.analyze.AnalyzeSentiment import *
from JD_spider_link.analyze.CleanData import *
from JD_spider_link.utils.MongoUtil import *
from bs4 import BeautifulSoup


def start(key):
    global_driver = login_and_cookies()
    ids = get_good_id()
    url = f"https://search.jd.com/Search?keyword={key}"
    global_driver.get(url)
    page_number = 1
    max_pages = 10
    while page_number <= max_pages:
        print("正在爬取第", page_number, "页 搜索")

        # 检索页面完全加载后的html内容
        html_content = global_driver.page_source

        # 使用BeautifulSoup解析html内容
        soup = BeautifulSoup(html_content, "html.parser")

        # 查找所有包含产品信息的class为“gl-i-wrap”的div
        div_list = soup.find_all("div", class_="gl-i-wrap")
        # 从每个div中提取文本信息
        for div in div_list:
            commit = div.find("div", class_="p-commit").get_text().strip()
            commit = commit.replace('条评价', '').replace('+', '')
            if '万' in commit:
                commit = float(commit.replace('万', '')) * 10000
            if int(commit) < 50000:
                continue

            # 模拟点击书名，获取新页面中的信息
            link = div.find("div", class_="p-name").find("a").get("href")
            if "http" not in link:
                link = "https:" + link
            print(extract_good_id(link))
            if extract_good_id(link) is None or extract_good_id(link) in ids:
                continue
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
                # create_wordCloud(cl_data, good_id)
                # 情感分析
                analyze_sentiment(good_id)

            except Exception as e:
                # 打印错误
                print("错误信息---" + str(e))
                pass

            print("运行时间：{:.2f}s".format((time.time() - ks)))
        # 点击下一页按钮（如果可用）
        next_page_button = global_driver.find_element(By.CLASS_NAME, "pn-next")
        if next_page_button:
            next_page_button.click()
            time.sleep(3)  # 延迟以完全加载下一页
        else:
            break

        page_number += 1


def extract_good_id(link):
    # 使用正则表达式提取数字部分
    match = re.search(r'(\d+)', link)

    if match:
        good_id = match.group(1)
        return str(good_id)
    else:
        return None


if __name__ == '__main__':
    # links = ['https://item.jd.com/100017568399.html',
    #          'https://item.jd.com/100031192620.html',
    #          'https://item.jd.com/100014352501.html', 'https://item.jd.com/100041239034.html']
    # links = ['https://item.jd.com/100023070523.html', 'https://item.jd.com/100057334060.html',
    # #          'https://item.jd.com/100066896392.html']
    # links = ['https://item.jd.com/100066896214.html', 'https://item.jd.com/100066896396.html',
    #          'https://item.jd.com/100066896468.html', 'https://item.jd.com/100066896220.html',
    #          'https://item.jd.com/100046043036.html', 'https://item.jd.com/100066896262.html']
    start('荣耀手机')
