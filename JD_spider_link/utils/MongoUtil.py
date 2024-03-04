from pymongo import MongoClient

db_name = 'E-commerce_review'
client = MongoClient('localhost', 27017)


# 插入数据到MongoDB的方法
def mongo_insert(data, collection_name):
    db = client[db_name]
    collection = db[collection_name]
    result = collection.insert_many(data)
    return result


# 从MongoDB查询数据的方法
def mongo_query(collection_name, query={},projection={}):
    db = client[db_name]
    collection = db[collection_name]

    results = collection.find(query, projection)
    return results[0]
