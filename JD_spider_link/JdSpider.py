import csv
import time

from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By


def start_jd_spider(driver):
    link = driver.current_url

    # 发送请求并检索网页内容
    driver.get(link)

    # 初始化变量
    data = []

    # 切换到新标签页
    windows = driver.window_handles
    driver.switch_to.window(windows[-1])

    time.sleep(3)
    good_name = driver.find_element(By.CLASS_NAME, "sku-name").text

    # 点击“商品评价”按钮
    shop_button = driver.find_elements(By.XPATH, "//*[@id='detail']/div[1]/ul/li[5]")[0]
    shop_button.click()
    time.sleep(2)  # 爬取并输出评价信息（评论数 好评、中评、差评数目）
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

    # 将数据添加到列表中
    info = {
        "商品名": good_name,
        "评论数": comments_count,
        "好评": good_comments_count,
        "中评": medium_comments_count,
        "差评": bad_comments_count
    }
    data.append(info)

    # 打印书籍信息
    print(info)

    # 将数据保存到CSV文件中
    filename = "book_info.csv"
    fields = ["商品名", "价格", "评论数", "出版社", "出版年份", "好评", "中评", "差评"]

    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fields)
        writer.writeheader()
        writer.writerows(data)

    print("数据已保存到", filename)

    return data