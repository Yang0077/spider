import re

import pandas as pd

from JD_spider_link.utils.MongoUtil import *

original_collection_name = 'original_data'
clean_collection_name = 'clean_data'


def clean_data(good_id):
    data = get_original_data(good_id)
    comments = data['comment_content']
    comments_pd = pd.DataFrame(comments, columns=['comment_content'])
    # 去重
    comments_pd = comments_pd.drop_duplicates()
    #
    # info = re.compile('[0-9a-zA-Z]')
    # comments_pd = comments_pd.apply(lambda x: info.sub('', x))  # 替换所有匹配项

    return comments_pd


def get_original_data(good_id):
    # 取出原始数据
    query = {"good_id": str(good_id)}
    projection = {
        '_id': 0
    }
    original_data = mongo_query(original_collection_name, query=query, projection=projection)

    #
    data_dict = {'good_id': original_data['good_id'], 'comment_content': original_data['comment_content']}
    return data_dict
