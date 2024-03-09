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
        comment_content.append(result['comment_data']['comment_content'])
        comment_star.append(result['comment_data']['comment_star'])
        segmented_text.append(result['comment_data']['segmented_text'])

    out = {
        '_id': _ids,
        'comment_data': {
            'comment_content': comment_content,
            'comment_star': comment_star,
            'segmented_text': segmented_text
        }}
    return out


# 更新MongoDB数据的方法
def mongo_update_batch(collection_name, update_data):
    db = client[db_name]
    collection = db[collection_name]

    batch_size = 1000
    for i in range(0, len(update_data), batch_size):
        batch = update_data[i:i + batch_size]
        bulk_operations = [pymongo.UpdateOne({"_id": doc["_id"]},
                                             {"$set": {"comment_data": doc["comment_data"]}}) for doc in batch]
        result = collection.bulk_write(bulk_operations)
        print("Updated", result.modified_count, "documents in batch", i // batch_size)
