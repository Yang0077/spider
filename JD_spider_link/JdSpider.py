import csv
import re
import time

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

from JD_spider_link.LoginAndGetCookie import login_and_cookies


def start(key):
    # 可使用Chrome浏览器驱动程序并将其设置为无头模式
    chrome_options = Options()
    driver = webdriver.Chrome(options=chrome_options)
    chrome_options.add_argument("--disable-gpu")
    # 可使用Chrome浏览器驱动程序并将其设置为无头模式
    # chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    login_and_cookies(driver)

    # 发送请求并检索网页内容
    # key = "人工智能"  # 搜索关键词
    url = (f"https://search.jd.com/Search?keyword={key}")
    driver.get(url)

    # 初始化变量
    page_number = 1
    max_pages = 10  # 设置要爬取的页面数，爬的页数太多会被反爬机制阻止，建议设置sleep
    count = 1
    max_count = 10
    data = []

    while page_number <= max_pages:
        print("正在爬取第", page_number, "页")

        # 检索页面完全加载后的html内容
        html_content = driver.page_source

        # 使用BeautifulSoup解析html内容
        soup = BeautifulSoup(html_content, "html.parser")

        # 查找所有包含产品信息的class为“gl-i-wrap”的div
        div_list = soup.find_all("div", class_="gl-i-wrap")

        # 从每个div中提取文本信息
        for div in div_list:
            if count > max_count:
                break
            name = div.find("div", class_="p-name").get_text().strip().replace("\n", "")
            price = div.find("div", class_="p-price").get_text().strip()
            commit = div.find("div", class_="p-commit").get_text().strip()
            commit = commit.replace('条评价', '').replace('+', '')
            if '万' in commit:
                commit = float(commit.replace('万', '')) * 10000

            # 模拟点击书名，获取新页面中的信息
            link = div.find("div", class_="p-name").find("a").get("href")
            if "http" not in link:
                link = "https:" + link

            # 打开新标签页
            driver.execute_script(f'''window.open("{link}","_blank");''')
            # 切换到新标签页
            windows = driver.window_handles
            driver.switch_to.window(windows[-1])
            time.sleep(2)
            soup_new = BeautifulSoup(driver.page_source, "html.parser")

            time.sleep(6)
            publisher = soup_new.find("li", title=True, clstag="shangpin|keycount|product|chubanshe_3")["title"] \
                if soup_new.find("li", title=True,
                                 clstag="shangpin|keycount|product|chubanshe_3") is not None else '未找到'
            publish_date_tag = soup_new.find("li", string=re.compile(r"出版时间："))
            publish_date = publish_date_tag.get_text().replace('出版时间：', '').strip() if publish_date_tag else '未找到'
            # 点击“商品评价”按钮
            shop_button = driver.find_elements(By.XPATH, "//*[@id='detail']/div[1]/ul/li[5]")[0]
            shop_button.click()
            time.sleep(2)  # 爬取并输出评价信息（好评、中评、差评数目）
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
            driver.close()
            driver.switch_to.window(windows[0])

            # 将数据添加到列表中
            info = {
                "书名": name,
                "价格": price,
                "评论数": commit,
                "出版社": publisher,
                "出版年份": publish_date,
                "好评": good_comments_count,
                "中评": medium_comments_count,
                "差评": bad_comments_count
            }
            data.append(info)

            # 打印书籍信息
            print(info)
            count += 1

        # 点击下一页按钮（如果可用）
        next_page_button = driver.find_element(By.CLASS_NAME, "pn-next")
        if next_page_button:
            next_page_button.click()
            time.sleep(3)  # 延迟以完全加载下一页
        else:
            break

        page_number += 1

    # 关闭浏览器驱动程序
    driver.quit()
    # 将数据保存到CSV文件中
    filename = "book_info.csv"
    fields = ["书名", "价格", "评论数", "出版社", "出版年份", "好评", "中评", "差评"]

    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fields)
        writer.writeheader()
        writer.writerows(data)

    print("数据已保存到", filename)
