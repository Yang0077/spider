import csv
import time

from bs4 import BeautifulSoup
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By


def start_jd_spider(driver):
    comments_count = 0
    good_comments_count = 0
    medium_comments_count = 0
    bad_comments_count = 0

    # 切换到新标签页
    windows = driver.window_handles
    driver.switch_to.window(windows[-1])

    link = driver.current_url
    print(f'link {link}')
    # 发送请求并检索网页内容
    driver.get(link)
    print(f'driver.current_url {driver.current_url}')

    # 初始化变量
    data = []

    time.sleep(3)
    good_name = driver.find_element(By.CLASS_NAME, "sku-name").text

    # 点击“商品评价”按钮
    shop_button = driver.find_elements(By.XPATH, "//*[@id='detail']/div[1]/ul/li[5]")[0]
    shop_button.click()
    time.sleep(3)  # 爬取并输出评价信息（评论数 好评、中评、差评数目）
    comments = driver.find_elements(By.XPATH, "//*[@id='comment']/div[2]/div[2]/div[1]/ul/li[1]/a/em")
    for comment in comments:
        comment_text = comment.text.strip("()+")
        if "万" in comment_text:
            comment_text = str(int(float(comment_text.strip("万")) * 10000))
        comments_count = int(comment_text)

    good_comments = driver.find_elements(By.XPATH, "//*[@id='comment']/div[2]/div[2]/div[1]/ul/li[5]/a/em")
    for comment in good_comments:
        comment_text = comment.text.strip("()+")
        if "万" in comment_text:
            comment_text = str(int(float(comment_text.strip("万")) * 10000))
        good_comments_count = int(comment_text)

    medium_comments = driver.find_elements(By.XPATH, "//*[@id='comment']/div[2]/div[2]/div[1]/ul/li[6]/a/em")
    for comment in medium_comments:
        comment_text = comment.text.strip("()+")
        if "万" in comment_text:
            comment_text = str(int(float(comment_text.strip("万")) * 10000))
        medium_comments_count = int(comment_text)

    bad_comments = driver.find_elements(By.XPATH, "//*[@id='comment']/div[2]/div[2]/div[1]/ul/li[7]/a/em")
    for comment in bad_comments:
        comment_text = comment.text.strip("()+")
        if "万" in comment_text:
            comment_text = str(int(float(comment_text.strip("万")) * 10000))
        bad_comments_count = int(comment_text)

    # 评论内容
    comment_content = []
    # 评论星级
    sentiments = []

    # 分别爬取好评 中评 差评
    driver.find_elements(By.XPATH, "//*[@id='comment']/div[2]/div[2]/div[1]/ul/li[5]/a")[0].click()
    driver, comment_content, sentiments = get_comments(driver, comment_content, sentiments, 'comment-4')
    driver.find_elements(By.XPATH, "//*[@id='comment']/div[2]/div[2]/div[1]/ul/li[6]/a")[0].click()
    driver, comment_content, sentiments = get_comments(driver, comment_content, sentiments, 'comment-5')
    driver.find_elements(By.XPATH, "//*[@id='comment']/div[2]/div[2]/div[1]/ul/li[7]/a")[0].click()
    driver, comment_content, sentiments = get_comments(driver, comment_content, sentiments, 'comment-6')

    # 商品id
    class_name = driver.find_elements(By.XPATH, '//div[@class="comment-count item fl"]/a')[0].get_attribute("class")
    good_id = str(class_name).split()[-1].split('-')[-1]
    # 将数据添加到列表中
    info = {
        "good_name": good_name,  # 商品名
        "good_id": good_id,  # 商品id
        "comments_count": comments_count,  # 评论数
        "good_comments_count": good_comments_count,  # 好评数
        "medium_comments_count": medium_comments_count,  # 中评数
        "bad_comments_count": bad_comments_count,  # 差评数
        "comment_content": comment_content,
        "sentiment": sentiments
    }
    data.append(info)

    # 打印书籍信息
    print(data)

    return data, good_id


def get_comments(driver, comment_content, sentiments, id_str):
    time.sleep(2)
    while True:
        comment_texts = driver.find_elements(By.XPATH, '//div[@class="comment-column J-comment-column"]/p')
        for comment in comment_texts:
            comment_content.append(str(comment.text).replace("\n", " ").strip())
        sentiment_stars = driver.find_elements(By.XPATH, '//div[@class="comment-column J-comment-column"]/div[1]')
        for sentiment in sentiment_stars:
            star = str(sentiment.get_attribute("class")[-1])[-1]
            sentiments.append(int(star))
        try:
            next_page_button = driver.find_element(By.XPATH,
                '//div[@id="'+id_str+'"]/div[@class="com-table-footer"]/div/div/a[text()="下一页"]')  # 定位下一页
            next_page_button.click()
            time.sleep(2)
        except Exception as e:
            print(f'ERROR: {e}')
            break

    return driver, comment_content, sentiments

