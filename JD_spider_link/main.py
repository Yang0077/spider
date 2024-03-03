import threading
from tkinter import *
from tkinter.ttk import *

from JD_spider_link.JdSpider import start


# 运行爬虫按钮点击事件
def runSpiderHandler(*args):
    try:
        # 获取需要爬取的商品名
        GoodName = searchGoodName.get()
        # 判断商品名是否为空
        if GoodName.strip() == '':
            print('商品名为空')
            return
        else:
            # 赋值
            lable_value.set('运行状态：运行中')
            print(f'爬取商品关键词：{GoodName}')
        start(GoodName)

    except ValueError as e:
        # 打印错误
        print("错误信息---" + str(e))
        lable_value.set('运行状态：爬取失败')
        pass


def thread_it(func, *args):
    # 打包函数进线程
    t = threading.Thread(target=func, args=args)
    # 守护线程
    t.daemon = True
    # 启动
    t.start()

# 初始化图形界面函数
def init_GUI():
    global root_window
    # 调用Tk()创建主窗口
    root_window = Tk()
    # 设置窗体居中显示
    SW = root_window.winfo_screenwidth()
    SH = root_window.winfo_screenheight()
    DW = 600
    DH = 400
    root_window.geometry("%dx%d+%d+%d" % (DW, DH, (SW - DW) / 2, (SH - DH) / 2))
    # 窗口标题
    root_window.title("京东爬虫")
    # 关闭窗口拉伸
    root_window.resizable(False, False)
    # 商品名输入框
    global searchGoodName, goodNameInput
    Label(root_window, text="请输入要爬取的商品名：", font=('微软雅黑', 12)).grid(row=0, column=0)
    searchGoodName = StringVar()
    goodNameInput = Entry(root_window, width=45, textvariable=searchGoodName).grid(row=0, column=1)
    # 爬虫按钮
    Button(root_window, width=10, text="爬取数据", command=lambda: thread_it(runSpiderHandler)).grid(row=0, column=2,sticky=E)

    # 处理状态
    global lable_value
    lable_value = StringVar()
    lable_value.set('运行状态：未启动')
    Label(root_window, textvariable=lable_value, font=('微软雅黑', 12)).grid(row=1, column=0, sticky=W)

    # 使窗口处于显示状态
    root_window.mainloop()


# 主函数
if __name__ == "__main__":
    init_GUI()
