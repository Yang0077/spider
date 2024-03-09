import jieba
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from wordcloud import WordCloud


def create_wordCloud(data, good_id):
    text = ' '.join(data['segmented_text'])

    # 读取形状图片
    mask = np.array(Image.open("img/shape_image.png"))

    # 创建词云对象
    wordcloud = (WordCloud(font_path='simhei.ttf', width=800, height=400, background_color='white',mask=mask)
                 .generate(text))

    # 保存词云图像到本地
    wordcloud.to_file("img/"+good_id+"_wordcloud.png")

