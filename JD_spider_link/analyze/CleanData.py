import re

import jieba
import pandas as pd
from zhon.hanzi import non_stops
from zhon.hanzi import punctuation
from zhon.hanzi import stops

from JD_spider_link.utils.MongoUtil import *

original_collection_name = 'original_data'
clean_collection_name = 'clean_data_'


def clean_data(good_id):
    data = pd.DataFrame(get_original_data(good_id))

    # 去除某些固定词
    words_to_remove = ['京东', '您没有填写评价内容']
    for word in words_to_remove:
        data['comment_content'] = data['comment_content'].str.replace(word, '')
    # 需要去除的关键词列表
    keywords_to_remove = []
    with open("analyze/file/keywords_to_remove.txt", "r", encoding="utf-8") as file:
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
    # 分词
    data = segmented(data)
    insert_data = []
    create_time = datetime.datetime.now()
    for i in range(len(data['comment_content'])):
        insert_data.append({
            'good_id': good_id,
            'create_time': create_time,
            'comment_data': {
                'comment_content': data['comment_content'][i],
                'comment_star': int(data['comment_star'][i]),
                'segmented_text': data['segmented_text'][i]
            }
        })

    mongo_insert(insert_data, clean_collection_name+good_id)

    data = data.to_dict(orient='list')

    return data


def get_original_data(good_id):
    # 取出原始数据
    query = {"good_id": str(good_id)}
    original_data = mongo_query_original(original_collection_name, query=query)
    data = original_data['comment_data']
    if 'segmented_text' in data:
        data.pop('segmented_text')
    return data


# 分词
def segmented(data):
    # 使用中文停用词表去除停用词
    stop_words = set()
    with open('analyze/file/stopwords.zh.cn.txt', 'r', encoding='utf-8') as f:
        for line in f:
            stop_words.add(line.strip())
    data['segmented_text'] = data['comment_content'].apply(
        lambda x: ' '.join([word for word in jieba.cut(x) if word not in stop_words]))

    # 文本标准化
    data['segmented_text'] = data['segmented_text'].apply(lambda x: x.lower())

    return data
