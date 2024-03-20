import threading
import time
from tkinter import *
from tkinter.ttk import *
from PIL import ImageTk, Image

from JD_spider_link.analyze.Analyze import *
from JD_spider_link.analyze.CleanData import *
from JD_spider_link.analyze.CreateWordCloud import *
from JD_spider_link.spider.JdSpider import start_jd_spider
from JD_spider_link.spider.LoginAndGetCookie import login_and_cookies

global_driver = None


def on_login_button_click():
    global global_driver
    lable_value.set('运行状态：登录商城')
    global_driver = login_and_cookies()
    lable_value.set('运行状态：登录成功')


# 运行爬虫按钮点击事件
def run_spider_handler(*args):
    ks = time.time()
    try:
        lable_value.set('运行状态：开始爬取')
        # 爬取数据
        global good_id
        ret_data, good_id = start_jd_spider(global_driver, None)

        lable_value.set('运行状态：爬取成功')

        # 保存数据->mongo 原始数据
        collection_name = 'original_data'
        mongo_insert(ret_data, collection_name)

        # 清洗数据
        lable_value.set('运行状态：数据清洗')
        global cl_data
        cl_data = clean_data(good_id)
        lable_value.set('运行状态：数据清洗完成')

    except Exception as e:
        # 打印错误
        print("错误信息---" + str(e))
        lable_value.set('运行状态：爬取失败')
        pass

    print("运行时间：{:.2f}s".format((time.time() - ks)))


def thread_it(func, *args):
    # 打包函数进线程
    t = threading.Thread(target=func, args=args)
    # 守护线程
    t.daemon = True
    # 启动
    t.start()


def generate_image():
    try:
        # 画词云图
        lable_value.set('运行状态：画词云图')
        time.sleep(3)

        img_name = create_wordCloud(cl_data, good_id)

        # 打开生成的图像文件
        image = Image.open(img_name)

        # 调整图像大小，如果需要的话
        image = image.resize((300, 300))

        # 创建ImageTk对象，用于在Tkinter中显示图像
        image_tk = ImageTk.PhotoImage(image)

        # 创建标签，并将图像显示在标签上
        img_label.configure(image=image_tk)
        img_label.image = image_tk
        lable_value.set('运行状态：词云图生成')

    except Exception as e:
        print("错误信息---" + str(e))
        lable_value.set('运行状态：错误')


def prediction():
    try:
        # 情感分析 预测
        model_prediction(good_id)
        lable_value.set('运行状态：情感预测完成')
    except Exception as e:
        print("错误信息---" + str(e))
        lable_value.set('运行状态：错误')


# 初始化图形界面函数
def init_GUI():
    global root_window
    # 调用Tk()创建主窗口
    root_window = Tk()
    # 设置窗体居中显示
    SW = root_window.winfo_screenwidth()
    SH = root_window.winfo_screenheight()
    DW = 800
    DH = 400
    # root_window.geometry("%dx%d+%d+%d" % (DW, DH, (SW - DW) / 2, (SH - DH) / 2))
    root_window.geometry("%dx%d+%d+%d" % (DW, DH, SW - DW, 0))
    # 窗口标题
    root_window.title("爬虫")
    # 关闭窗口拉伸
    root_window.resizable(False, False)
    # 处理状态
    global lable_value
    lable_value = StringVar()
    lable_value.set('运行状态：未启动')
    Label(root_window, textvariable=lable_value, font=('微软雅黑', 15)).grid(row=0, column=0, padx=10, pady=5)

    # 京东登录按钮
    button = Button(root_window, width=16, text="进入商城", command=lambda: thread_it(on_login_button_click))
    button.grid(row=0, column=1, padx=10, pady=5)

    # 爬虫按钮
    button = Button(root_window, width=16, text="爬取数据", command=lambda: thread_it(run_spider_handler))
    button.grid(row=0, column=2, padx=10, pady=5)
    # 画图
    global img_label
    img_label = Label(root_window)
    img_label.grid(row=1, column=0, columnspan=5, pady=6)
    button = Button(root_window, width=16, text="画词云图", command=lambda: thread_it(generate_image))
    button.grid(row=0, column=3, padx=10, pady=5)

    # 预测
    button = Button(root_window, width=16, text="情感预测", command=lambda: thread_it(prediction))
    button.grid(row=0, column=4, padx=10, pady=5)

    # 设置窗口总是显示在其他程序之前
    root_window.attributes('-topmost', True)

    # 使窗口处于显示状态
    root_window.mainloop()


# 主函数
if __name__ == "__main__":
    init_GUI()
