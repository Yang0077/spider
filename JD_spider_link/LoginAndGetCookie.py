import json
import os
import time


def login_and_cookies(driver):

    cookie_file = 'cookie.txt'
    """
    处理登录和cookie的逻辑。
    如果存在cookie文件，使用cookie登录；否则提示用户登录并保存cookie。
    """
    # 判断是否有 cookie.txt 文件
    driver.get("https://passport.jd.com/new/login.aspx?/")

    if os.path.exists(cookie_file):
        print('使用已保存的cookie登录')
        # 读取cookie文件中的内容
        with open(cookie_file, 'r') as file:
            # 读取文件中的 cookie
            cookies = json.load(file)
            # 加载cookie信息到浏览器
            for cookie in cookies:
                cookie['domain'] = '.jd.com'
                driver.add_cookie(cookie)
                # 跳转到目标页面
        # driver.get("https://www.jd.com/")
        # time.sleep(2)  # 等待页面加载
    else:
        print('需要登录')
        # 导航到登录页面
        # 等待用户登录
        time.sleep(20)  # 第一次使用需要用户手动登录获取cookie, 可根据网络状况修改
        # 获取登录后的cookie并保存到文件
        dictcookies = driver.get_cookies()
        jsoncookies = json.dumps(dictcookies)
        with open(cookie_file, 'w') as f:
            f.write(jsoncookies)
        print('cookies已保存')
        # 可以在这里继续后续操作，比如再次跳转到目标页面
        # driver.get("https://www.jd.com/")
        # driver.quit()
