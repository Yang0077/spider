import jieba


def analyze_sentiment(data):
    # 加载爬取的中文评论数据，假设数据包含两列：'segmented_text'为评论文本，'sentiment为情感标签或客户满意度评分
    # 使用中文停用词表去除停用词
    stop_words = set()
    with open('analyze/stopwords.zh.cn.txt', 'r', encoding='utf-8') as f:
        for line in f:
            stop_words.add(line.strip())
    data['segmented_text'] = data['comment_content'].apply(
        lambda x: ' '.join([word for word in jieba.cut(x) if word not in stop_words]))

    # 文本标准化
    data['segmented_text'] = data['segmented_text'].apply(lambda x: x.lower())

    return data
