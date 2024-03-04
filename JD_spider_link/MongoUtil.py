from pymongo import MongoClient

db_name = 'jd_spider'
collection_name = 'jd_spider'
client = MongoClient('localhost', 27017)


# 插入数据到MongoDB的方法
def mongo_insert(data):
    db = client[db_name]
    collection = db[collection_name]
    result = collection.insert_many(data)
    return result


# 从MongoDB查询数据的方法
def mongo_query(query={}):
    db = client[db_name]
    collection = db[collection_name]
    results = collection.find(query)
    return list(results)
