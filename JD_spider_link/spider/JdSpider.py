import datetime
import re
import time

from bs4 import BeautifulSoup
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By


def start_jd_spider(driver,link):
    # 切换到新标签页
    windows = driver.window_handles
    driver.switch_to.window(windows[-1])
    # 获取当前窗口的句柄（即当前标签页的句柄）
    # current_window_handle = driver.current_window_handle
    # # 获取所有窗口的句柄
    # all_window_handles = driver.window_handles
    # # 遍历所有窗口的句柄，判断哪个窗口句柄不等于当前窗口句柄，即为新打开的标签页
    # for window_handle in all_window_handles:
    #     if window_handle != current_window_handle:
    #         # 切换到新标签页
    #         driver.switch_to.window(window_handle)
    #         break
    # link = driver.current_url

    if is_jd_url_format(str(link)) is False:
        print(f'链接 {link} 错误')
        # 抛出一个自定义异常
        raise ValueError(f'链接 {link} 错误')

    print(f'link {link}')
    # 发送请求并检索网页内容
    driver.get(link)
    print(f'driver.current_url {driver.current_url}')

    # 初始化变量
    data = []

    time.sleep(2)
    good_name = driver.find_element(By.CLASS_NAME, "sku-name").text
    # 商品id
    class_name = driver.find_elements(By.XPATH, '//div[@class="comment-count item fl"]/a')[0].get_attribute("class")
    global good_id
    good_id = str(class_name).split()[-1].split('-')[-1]

    # 点击“商品评价”按钮
    shop_button = driver.find_elements(By.XPATH, "//*[@id='detail']/div[1]/ul/li")
    for shop in shop_button:
        if '商品评价' in shop.text:
            shop.click()
            break

    time.sleep(2.5)
    # 爬取并输出评价信息（评论数 好评、中评、差评数目）
    # comments = driver.find_elements(By.XPATH, "//*[@id='comment']/div[2]/div[2]/div[1]/ul/li[1]/a/em")
    # for comment in comments:
    #     comment_text = comment.text.strip("()+")
    #     if "万" in comment_text:
    #         comment_text = str(int(float(comment_text.strip("万")) * 10000))
    #     comments_count = int(comment_text)
    #
    # good_comments = driver.find_elements(By.XPATH, "//*[@id='comment']/div[2]/div[2]/div[1]/ul/li[5]/a/em")
    # for comment in good_comments:
    #     comment_text = comment.text.strip("()+")
    #     if "万" in comment_text:
    #         comment_text = str(int(float(comment_text.strip("万")) * 10000))
    #     good_comments_count = int(comment_text)
    #
    # medium_comments = driver.find_elements(By.XPATH, "//*[@id='comment']/div[2]/div[2]/div[1]/ul/li[6]/a/em")
    # for comment in medium_comments:
    #     comment_text = comment.text.strip("()+")
    #     if "万" in comment_text:
    #         comment_text = str(int(float(comment_text.strip("万")) * 10000))
    #     medium_comments_count = int(comment_text)
    #
    # bad_comments = driver.find_elements(By.XPATH, "//*[@id='comment']/div[2]/div[2]/div[1]/ul/li[7]/a/em")
    # for comment in bad_comments:
    #     comment_text = comment.text.strip("()+")
    #     if "万" in comment_text:
    #         comment_text = str(int(float(comment_text.strip("万")) * 10000))
    #     bad_comments_count = int(comment_text)

    # 评论内容
    comment_content = []
    # 评论星级
    comment_star = []

    # 分别爬取好评 中评 差评
    driver.find_elements(By.XPATH, "//*[@id='comment']/div[2]/div[2]/div[1]/ul/li[5]/a")[0].click()
    driver, comment_content, comment_star = get_comments(driver, comment_content, comment_star, 'comment-4')
    driver.find_elements(By.XPATH, "//*[@id='comment']/div[2]/div[2]/div[1]/ul/li[6]/a")[0].click()
    driver, comment_content, comment_star = get_comments(driver, comment_content, comment_star, 'comment-5')
    driver.find_elements(By.XPATH, "//*[@id='comment']/div[2]/div[2]/div[1]/ul/li[7]/a")[0].click()
    driver, comment_content, comment_star = get_comments(driver, comment_content, comment_star, 'comment-6')

    create_time = datetime.datetime.now()

    # 将数据添加到列表中
    info = {
        "good_name": good_name,  # 商品名
        "good_id": good_id,  # 商品id
        # "comments_count": comments_count,  # 评论数
        # "good_comments_count": good_comments_count,  # 好评数
        # "medium_comments_count": medium_comments_count,  # 中评数
        # "bad_comments_count": bad_comments_count,  # 差评数
        'create_time': create_time,
        "comment_content": comment_content,
        "comment_star": comment_star
    }
    data.append(info)
    # 打印书籍信息
    # print(data)

    return data, good_id


def get_comments(driver, comment_content, comment_star, id_str):
    page = 1
    time.sleep(2)
    while True:
        print(f'爬取 {good_id} {choose(id_str)} 第{page}页 ')

        comment_texts = driver.find_elements(By.XPATH, '//div[@class="comment-column J-comment-column"]/p')
        comment_stars = driver.find_elements(By.XPATH, '//div[@class="comment-column J-comment-column"]/div[1]')

        for i in range(len(comment_texts)):
            comment = str(comment_texts[i].text).replace("\n", " ").strip()
            sentiment = str(comment_stars[i].get_attribute("class")[-1])[-1]

            if comment == '':
                continue

            comment_content.append(comment)
            comment_star.append(int(sentiment))

        try:
            next_page_button = driver.find_element(By.XPATH,
                                                   '//div[@id="' + id_str + '"]/div[@class="com-table-footer"]/div/div/a[text()="下一页"]')  # 定位下一页
            next_page_button.click()
            page += 1
            time.sleep(1)
        except Exception as e:
            # print(f'ERROR: {e}')
            time.sleep(0.5)
            break

    return driver, comment_content, comment_star


def choose(str_id):
    if str_id == 'comment-4':
        return '好评'
    elif str_id == 'comment-5':
        return '中评'
    elif str_id == 'comment-6':
        return '差评'


def is_jd_url_format(url):
    # 定义正则表达式模式
    # pattern = r"https://item\.jd\.com/\w+\.html"
    # 只匹配数字
    pattern = r"https://item\.jd\.com/\d+\.html"
    # 使用正则表达式进行匹配
    if re.match(pattern, url):
        return True
    else:
        return False
