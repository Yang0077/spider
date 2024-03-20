import time

import joblib
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.tree import DecisionTreeClassifier
from sklearn.tree import export_text

from JD_spider_link.analyze.CleanData import *
from JD_spider_link.utils.MongoUtil import *


def analyze():
    # 加载爬取的中文评论数据，假设数据包含两列：'segmented_text'为评论文本，sentiment为情感标签或客户满意度评分
    ks = time.time()
    # data = pd.DataFrame(clean_data(good_id))
    data = get_train_data()
    # 分割特征和标签
    X = data['segmented_text']
    y = data['comment_content_score']
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
    print(f"模型准确率：{accuracy}")

    # 打印分类报告
    print("分类报告: ")
    print(classification_report(y_test, y_pred))
    cross_verification(X, y)

    # 保存模型到文件
    model_filename = 'analyze/decision_tree_model.joblib'
    joblib.dump(dt_classifier, model_filename)
    print(f"\nModel saved to {model_filename}")

    # 导出决策树结构文本
    tree_text = export_text(dt_classifier, feature_names=tfidf_vectorizer.get_feature_names())

    # 绘制决策树文本
    custom_font = FontProperties(fname='C:/Windows/Fonts/simkai.ttf')

    plt.figure(figsize=(10, 10))
    plt.text(0.1, 0.5, tree_text, fontsize=10, fontfamily="monospace", fontproperties=custom_font)
    plt.axis("off")
    # 保存决策树为图片文件
    img_filename = "img/decision_tree.png"  # 指定图片文件名
    plt.savefig(img_filename, dpi=300, bbox_inches="tight")

    print(f"决策树已保存为图片文件：{img_filename}")

    print("模型训练耗时: ", time.time() - ks)


def cross_verification(X, y):
    # 定义决策树分类器
    dt_classifier = DecisionTreeClassifier()

    # 使用TF-IDF向量化的全部数据
    tfidf_vectorizer = TfidfVectorizer(max_features=1000)
    X_tfidf = tfidf_vectorizer.fit_transform(X)

    # 进行交叉验证
    cv_scores = cross_val_score(dt_classifier, X_tfidf, y, cv=5)  # 5折交叉验证

    # 打印交叉验证得分
    print("交叉验证得分:", cv_scores)
    print("平均交叉验证得分:", cv_scores.mean())


def model_prediction(good_id_):
    ks = time.time()
    global good_id
    good_id = good_id_
    comment_data = mongo_query_clean('clean_data_' + good_id, query={'good_id': str(good_id)})
    _ids = comment_data['_id']

    comment_data = comment_data['segmented_text']

    while len(comment_data) < 1000:
        comment_data.append("空" + str(len(comment_data)))

    loaded_model = joblib.load('analyze/decision_tree_model.joblib')
    # 使用TF-IDF向量化文本特征
    tfidf_vectorizer = TfidfVectorizer(max_features=1000)  # 可以根据需要调整特征数量

    # 对评论数据进行转换
    X_new = tfidf_vectorizer.fit_transform(comment_data)
    # 进行预测
    y_pred_new = loaded_model.predict(X_new)
    result_pred = []
    for i in range(len(_ids)):
        mongo_update(clean_collection_name + good_id, _ids[i], 'predict_result', int(y_pred_new[i]))
        result_pred.append(y_pred_new[i])

    img_names = [export_importances(loaded_model), export_label(result_pred)]

    print("情感预测耗时:", time.time() - ks)
    return img_names


def export_importances(loaded_model):
    # 获取特征重要性
    feature_importance = loaded_model.feature_importances_

    # 可视化特征重要性
    plt.bar(range(len(feature_importance)), feature_importance)
    plt.xlabel('Feature Index')
    plt.ylabel('Feature Importance')
    plt.title('Feature Importance')
    img_name = 'img/' + good_id + '_feature_importance.png'
    plt.savefig(img_name)  # 保存特征重要性图表为图片文件

    return img_name


def export_label(y_pred_new):
    # 统计每个类别的数量
    y = [y_pred_new.count(1), y_pred_new.count(0)]
    unique_labels = ["1", "0"]

    fig, ax = plt.subplots()

    # 设置柱状图的宽度
    width = 0.5

    # 创建柱状图
    ax.bar(unique_labels, y, width, align="center", color=["r", "g"])

    # 设置坐标轴范围
    ax.set_ylim([0, max(y) * 1.2])

    ax.set_xlabel('Labels')
    ax.set_ylabel('Counts')
    ax.set_title('Prediction Distribution')
    img_name = 'img/' + good_id + '_prediction_distribution.png'

    plt.savefig(img_name)
    plt.show()

    return img_name
