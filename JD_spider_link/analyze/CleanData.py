import re

import pandas as pd
from zhon.hanzi import non_stops
from zhon.hanzi import punctuation
from zhon.hanzi import stops

from JD_spider_link.utils.MongoUtil import *

original_collection_name = 'original_data'
clean_collection_name = 'clean_data'


def clean_data(good_id):
    data = pd.DataFrame(get_original_data(good_id))

    # 去除某些固定词
    words_to_remove = ['京东']
    for word in words_to_remove:
        data['comment_content'] = data['comment_content'].str.replace(word, '')
    # 需要去除的关键词列表
    keywords_to_remove = []
    with open("analyze/keywords_to_remove.txt", "r", encoding="utf-8") as file:
        for line in file:
            keywords_to_remove.append(line.strip())

    # 使用正则表达式去除关键词
    for keyword in keywords_to_remove:
        data['comment_content'] = data['comment_content'].apply(lambda x: re.sub(keyword + r'[^：]*：', '', x))

    # 去除特殊字符和标点符号
    data['comment_content'] = data['comment_content'].apply(lambda x: re.sub(r'[%s]' % (punctuation + non_stops + stops), '', x))

    # 定义正则表达式模式，用于匹配英文字母
    pattern = re.compile(r'[a-zA-Z0-9]')
    # 去除评论中的英文字母
    data['comment_content'] = data['comment_content'].apply(lambda x: re.sub(pattern, '', x))
    temp_data = data.copy()
    temp_data['good_id'] = good_id
    insert_data = data.to_dict(orient='list')
    insert_data['good_id'] = good_id
    mongo_insert([insert_data], clean_collection_name)
    return data


def get_original_data(good_id):
    # 取出原始数据
    query = {"good_id": str(good_id)}
    projection = {
        '_id': 0
    }
    original_data = mongo_query(original_collection_name, query=query, projection=projection)

    #
    data_dict = {'comment_content': original_data['comment_content'],
                 'sentiment': original_data['sentiment']}
    return data_dict
