import pandas as pd
from bson.objectid import ObjectId
from JD_spider_link.utils.MongoUtil import *
from JD_spider_link.analyze.judge_polarity import *


def analyze_sentiment(good_id):
    data = mongo_query_clean('clean_data_'+good_id, query={'good_id': str(good_id)})
    _ids = data['_id']

    comment_data = data['comment_data']

    pos_comment = load_file('analyze/file/正面评价词语（中文）.txt')
    pos_emotion = load_file('analyze/file/正面情感词语（中文）.txt')

    neg_comment = load_file('analyze/file/负面评价词语（中文）.txt')
    neg_emotion = load_file('analyze/file/负面情感词语（中文）.txt')

    # 正面
    pos = pos_comment.union(pos_emotion)
    # 负面
    neg = neg_comment.union(neg_emotion)
    sentiment_score = []

    for words in comment_data['segmented_text']:
        words = str(words).split()
        positive_count = 0
        negative_count = 0
        for word in words:
            if word in pos:
                positive_count += 1
            elif word in neg:
                negative_count += 1
            else:
                continue
        if positive_count - negative_count > 0:
            # 正面
            score = 1
        elif positive_count - negative_count < 0:
            # 负面
            score = 0
        else:
            # 中性
            score = -1
        sentiment_score.append(score)

    comment_data['sentiment_score'] = sentiment_score

    documents_to_update = []

    sentence_score = []
    for sentence in comment_data['comment_content']:
        sentence_score.append(DictClassifier().analyse_sentence(sentence, runout_filepath='log.txt'))
    comment_data['sentence_score'] = sentence_score

    for i in range(len(_ids)):
        documents_to_update.append({
            '_id': ObjectId(_ids[i]),
            'comment_data': {
                'comment_content': comment_data['comment_content'][i],
                'comment_star': int(comment_data['comment_star'][i]),
                'segmented_text': comment_data['segmented_text'][i],
                'sentiment_score': comment_data['sentiment_score'][i],
                'sentence_score': int(comment_data['sentence_score'][i])
            }
        })

    mongo_update_batch('clean_data_'+good_id, documents_to_update)

    # print(data)


def load_file(path):
    data = set()
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            data.add(line.strip())
    data = set(filter(lambda x: x != '', data))
    return data
