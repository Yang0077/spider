import pandas as pd
from bson.objectid import ObjectId
from tqdm import tqdm

from JD_spider_link.utils.MongoUtil import *
from JD_spider_link.analyze.judge_polarity import *


def analyze_sentiment(good_id):
    comment_data = mongo_query_clean('clean_data_' + good_id, query={'good_id': str(good_id)})
    _ids = comment_data['_id']

    pos_comment = load_file('analyze/file/正面评价词语（中文）.txt')
    pos_emotion = load_file('analyze/file/正面情感词语（中文）.txt')

    neg_comment = load_file('analyze/file/负面评价词语（中文）.txt')
    neg_emotion = load_file('analyze/file/负面情感词语（中文）.txt')

    # 正面
    pos = pos_comment.union(pos_emotion)
    # 负面
    neg = neg_comment.union(neg_emotion)
    segmented_text_score = []

    # for words in comment_data['segmented_text']:
    for words in tqdm(comment_data['segmented_text'], desc="Processing Comments"):
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
        segmented_text_score.append(score)

    comment_data['segmented_text_score'] = segmented_text_score

    documents_to_insert = []

    comment_content_score = []
    # for sentence in comment_data['comment_content']:
    for sentence in tqdm(comment_data['comment_content'], desc="Analyzing Sentences"):
        comment_content_score.append(DictClassifier().analyse_sentence(sentence,
                                                                       runout_filepath='analyze/log/log_' + good_id + '.txt'))
    comment_data['comment_content_score'] = comment_content_score

    for i in range(len(_ids)):
        documents_to_insert.append({
            'comment_content': comment_data['comment_content'][i],
            'comment_star': int(comment_data['comment_star'][i]),
            'segmented_text': comment_data['segmented_text'][i],
            'comment_content_score': comment_data['comment_content_score'][i],
            'segmented_text_score': int(comment_data['segmented_text_score'][i])
        })

    mongo_insert(documents_to_insert, 'train_data')

    # print(data)


def load_file(path):
    data = set()
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            data.add(line.strip())
    data = set(filter(lambda x: x != '', data))
    return data
