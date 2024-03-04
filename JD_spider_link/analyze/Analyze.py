from JD_spider_link.analyze.CleanData import *
from JD_spider_link.analyze.AnalyzeSentiment import *
from JD_spider_link.analyze.CreateWordCloud import *


def analyze(good_id):

    comments = clean_data(good_id)
    create(comments)


if __name__ == '__main__':
    print(analyze("100080153863"))
