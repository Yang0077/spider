import datetime

import pymongo
from pymongo import MongoClient

db_name = 'E-commerce_review'
client = MongoClient('localhost', 27017)


# 插入数据到MongoDB的方法
def mongo_insert(data, collection_name):
    db = client[db_name]
    collection = db[collection_name]
    # data[0]['create_time'] = datetime.datetime.now()
    result = collection.insert_many(data)
    return result


# 从MongoDB查询数据的方法
def mongo_query_original(collection_name, query={}):
    out = {}
    db = client[db_name]
    collection = db[collection_name]
    latest_date_cursor = collection.find(query).sort('create_time', -1).limit(1)
    latest_date = latest_date_cursor[0]["create_time"]
    query['create_time'] = latest_date
    results = collection.find(query)[0]
    out['comment_data'] = {
        'comment_content': results['comment_content'],
        'comment_star': results['comment_star'],
    }
    return out


def mongo_query_clean(collection_name, query={}):
    db = client[db_name]
    collection = db[collection_name]
    latest_date_cursor = collection.find(query).sort('create_time', -1).limit(1)
    latest_date = latest_date_cursor[0]["create_time"]
    query['create_time'] = latest_date
    results = collection.find(query)

    _ids = []
    comment_content = []
    comment_star = []
    segmented_text = []

    for result in results:
        _ids.append(result['_id'])
        comment_content.append(result['comment_content'])
        comment_star.append(result['comment_star'])
        segmented_text.append(result['segmented_text'])

    out = {
        '_id': _ids,
        'comment_content': comment_content,
        'comment_star': comment_star,
        'segmented_text': segmented_text
    }
    return out


def get_train_data():
    db = client[db_name]

    collection = db['train_data']
    result = collection.find()

    comment_content = []
    sentiment_score_1 = []
    sentiment_score_2 = []
    segmented_text = []
    for doc in result:
        comment_content.append(doc['comment_content'])
        segmented_text.append(doc['segmented_text'])
        sentiment_score_1.append(doc['comment_content_score'])
        sentiment_score_2.append(doc['segmented_text_score'])
    data = {
        'comment_content': comment_content,
        'segmented_text': segmented_text,
        'comment_content_score': sentiment_score_1,
        'segmented_text_score': sentiment_score_2
    }
    return data


def get_good_id():
    db = client[db_name]
    collection = db['original_data']
    results = collection.find()
    good_id_list = []
    for result in results:
        good_id_list.append(result['good_id'])

    return good_id_list


# 更新MongoDB数据的方法
def mongo_update(collection_name, _id, column_name, update_data):
    db = client[db_name]
    collection = db[collection_name]
    collection.update_one({'_id': _id}, {'$set': {column_name: update_data}})

