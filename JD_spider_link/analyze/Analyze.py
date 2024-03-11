from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier

from JD_spider_link.analyze.CleanData import *
from JD_spider_link.utils.MongoUtil import *


def analyze(arg1, agr2):
    # 加载爬取的中文评论数据，假设数据包含两列：'segmented_text'为评论文本，sentiment为情感标签或客户满意度评分

    # data = pd.DataFrame(clean_data(good_id))
    data = get_train_data()

    # 分割特征和标签
    X = data[arg1]
    y = data[agr2]
    # 划分训练集和测试集
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # 使用TF-IDF向量化文本特征
    tfidf_vectorizer = TfidfVectorizer(max_features=1000)  # 可以根据需要调整特征数量
    X_train_tfidf = tfidf_vectorizer.fit_transform(X_train)
    X_test_tfidf = tfidf_vectorizer.transform(X_test)

    # 构建决策树分类器模型
    dt_classifier = DecisionTreeClassifier()
    dt_classifier.fit(X_train_tfidf, y_train)

    # 在测试集上进行预测
    y_pred = dt_classifier.predict(X_test_tfidf)

    # 评估模型性能
    accuracy = accuracy_score(y_test, y_pred)
    print("模型准确率：", accuracy)

    # 打印分类报告
    print(classification_report(y_test, y_pred))


if __name__ == '__main__':
    analyze("comment_content", "comment_content_score")
    analyze("segmented_text", "segmented_text_score")
