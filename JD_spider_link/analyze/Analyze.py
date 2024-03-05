from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier

from JD_spider_link.analyze.CleanData import *


def analyze(good_id):
    # 加载爬取的中文评论数据，假设数据包含两列：'segmented_text'为评论文本，'sentiment'为情感标签或客户满意度评分

    data = pd.DataFrame(clean_data(good_id))

    print(data)
    # 特征提取
    tfidf_vectorizer = TfidfVectorizer(max_features=1000)
    X = tfidf_vectorizer.fit_transform(data['segmented_text'])
    y = data['sentiment']  # 或者客户满意度评分

    # 划分训练集和测试集
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # 训练决策树模型
    decision_tree = DecisionTreeClassifier()
    decision_tree.fit(X_train, y_train)

    # 模型评估
    y_pred = decision_tree.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print("Accuracy:", accuracy)
    print("Classification Report:")
    print(classification_report(y_test, y_pred))

    # 新评论情感分析示例
    new_reviews = ["这个产品质量很好！", "客户服务太差了。"]
    X_new = tfidf_vectorizer.transform(new_reviews)
    predicted_sentiments = decision_tree.predict(X_new)
    print("Predicted Sentiments for new reviews:", predicted_sentiments)


# 分词函数
def chinese_word_segmentation(text):
    return ' '.join(jieba.cut(text))


if __name__ == '__main__':
    analyze("100060016468")
