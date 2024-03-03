import time


def login_and_cookies(driver):
    print('需要登录')
    # 导航到登录页面
    driver.get("https://passport.jd.com/new/login.aspx?/")
    # 等待用户登录
    time.sleep(20)  # 第一次使用需要用户手动登录获取cookie, 可根据网络状况修改
    if driver.get_cookies() is None:
        print('登录成功')
    else:
        print('登录失败')
