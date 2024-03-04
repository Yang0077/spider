import threading
from tkinter import *
from tkinter.ttk import *

from JD_spider_link.JdSpider import start_jd_spider
from JD_spider_link.LoginAndGetCookie import login_and_cookies
from JD_spider_link.MongoUtil import *

global_driver = None
page_num = 100  # 最大爬取页数

def on_login_button_click():
    global global_driver
    lable_value.set('运行状态：登录商城')
    global_driver = login_and_cookies()
    lable_value.set('运行状态：登录成功')


# 运行爬虫按钮点击事件
def run_spider_handler(*args):
    try:
        lable_value.set('运行状态：开始爬取')
        # 爬取数据
        ret_data = start_jd_spider(global_driver, page_num)

        lable_value.set('运行状态：爬取成功')

        # 保存数据->mongo
        mongo_insert(ret_data)

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
    DW = 200
    DH = 150
    # root_window.geometry("%dx%d+%d+%d" % (DW, DH, (SW - DW) / 2, (SH - DH) / 2))
    root_window.geometry("%dx%d+%d+%d" % (DW, DH, SW - DW*2, DH/2))
    # 窗口标题
    root_window.title("爬虫")
    # 关闭窗口拉伸
    root_window.resizable(False, False)

    # 京东登录按钮
    button = Button(root_window, width=20, text="进入京东商城", command=lambda: thread_it(on_login_button_click))
    button.grid(row=0, column=0, padx=24, pady=10)

    # 爬虫按钮
    button = Button(root_window, width=20, text="爬取数据", command=lambda: thread_it(run_spider_handler))
    button.grid(row=1, column=0, padx=24, pady=0)
    # 页数
    global page_num
    page_num = StringVar()
    entry = Entry(root_window, width=18, textvariable=page_num)  # 设置文本颜色为灰色以模仿占位符
    entry.insert(0, "输入爬取页数(默认100)")  # 在Entry中插入提示文本
    # 当Entry控件获取焦点时，清除提示文本
    entry.bind("<FocusIn>", lambda event: entry.delete(0, END) if entry.get() == "输入爬取页数(默认100)" else None)
    # 当Entry控件失去焦点且内容为空时，重新插入提示文本
    entry.bind("<FocusOut>", lambda event: entry.insert(0, "输入爬取页数(默认100)") if not entry.get() else None)
    # 使用grid布局管理器放置Entry控件
    entry.grid(row=2, column=0, padx=22, pady=5)
    # 处理状态
    global lable_value
    lable_value = StringVar()
    lable_value.set('运行状态：未启动')
    Label(root_window, textvariable=lable_value, font=('微软雅黑', 12)).grid(row=3, column=0, padx=22, pady=5)

    # 使窗口处于显示状态
    root_window.mainloop()


# 主函数
if __name__ == "__main__":
    init_GUI()