import time
import re
import csv
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

from LoginAndGetCookie import login_and_cookies

# 可使用Chrome浏览器驱动程序并将其设置为无头模式
chrome_options = Options()
driver = webdriver.Chrome(options=chrome_options)
chrome_options.add_argument("--disable-gpu")
# 可使用Chrome浏览器驱动程序并将其设置为无头模式
# chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# 登录操作获取到cookie
login_and_cookies(driver)
