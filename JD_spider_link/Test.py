from JD_spider_link.spider.JdSpider import start_jd_spider
from JD_spider_link.spider.LoginAndGetCookie import login_and_cookies
from JD_spider_link.analyze.AnalyzeSentiment import *
from JD_spider_link.analyze.CleanData import *
from JD_spider_link.analyze.CreateWordCloud import *

if __name__ == '__main__':
    cl_data = clean_data('10071529115168')
    print(cl_data)
