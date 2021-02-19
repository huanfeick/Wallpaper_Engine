# -*- coding:utf-8 -*-

"""
时间:2021年02月19日
作者:幻非
"""

import os
import random
from tkinter import *
import tkinter.messagebox
import shutil

wallpaper_path = "E:\\Steam\\steamapps\\workshop\\content\\431960"  # wallpaper保存视频位置
video_list = []  # 全部视频地址列表
list_history = []  # 历史播放的视频名称列表
history_dict = {}  # 右侧历史记录字典
delete_path = 0  # 路径删除变量
delete_list = []  # 关闭窗口时删除的路径列表

player = tkinter.Tk()  # 窗口
player.title("wallpaper engine查找")
mw, mh = player.maxsize()
player.geometry('360x270+%d+%d' % ((mw - 500) / 2, (mh - 300) / 2))  # 窗口居中
player.resizable(0, 0)  # 锁定窗口大小
player.wm_attributes('-topmost', 1)  # 窗口置顶


# 打开视频
def video_play(path):
    class Video(object):
        def __init__(self, video_path):
            self.path = video_path

        def play(self):
            from os import startfile
            startfile(self.path)

    class Movie_MP4(Video):
        type = 'MP4'

    movie = Movie_MP4(path)
    movie.play()


# 获取路径下所有的视频路径
def search_file(path):
    # 首先先找到当前目录下的所有文件
    for file in os.listdir(path):  # os.listdir(path) 是当前这个path路径下的所有文件的列表
        this_path = os.path.join(path, file)
        if os.path.isfile(this_path):  # 判断这个路径对应的是目录还是文件，是文件就走下去
            if ".mp4" in file:
                video_list.append(this_path)
        else:  # 不是就再次执行这个函数，递归下去
            search_file(this_path)  # 递归下去
    return video_list


path_list = search_file(wallpaper_path)  # 全部视频地址列表
rand = random.sample(range(1, len(path_list)), len(path_list) - 1)  # 将全部视频地址序列打散
i = 1


# 开始随机播放视频
def random_video():
    global i
    global delete_path
    video_data_title = os.path.basename(os.path.splitext(path_list[rand[i]])[0])  # 随机播放视频的名称
    history_dict[video_data_title] = path_list[rand[i]]  # 字典
    # 打开视频
    video_play(path_list[rand[i]])
    list_history.append(video_data_title)
    listbox_history.delete(0, END)
    for item in list_history:
        listbox_history.insert(0, item)
    i = i + 1
    delete_path = os.path.dirname(path_list[rand[i - 1]]), path_list[rand[i - 1]]


def buttonList(event):
    global delete_path
    video_name = listbox_history.get(listbox_history.curselection())  # 获取点击的视频名称
    video_play(history_dict[video_name])  # 查找字典播放视频
    delete_path = os.path.dirname(history_dict[video_name]), history_dict[video_name]


# 删除按钮
def delete_video():
    if delete_path == 0:
        tkinter.messagebox.showinfo("提示", "请先观看一个视频")
    else:
        if tkinter.messagebox.askyesno('提示', '确定要删除?'):
            if delete_path[1].find("Xunlei") != -1:
                # print(delete_path[1])
                delete_list.append(delete_path[1])
            else:
                delete_list.append(delete_path[0])
                # print(delete_path[0])
        random_video()


# 即将关闭
def callbackClose():
    set_delete_list = list(set(delete_list))
    if len(set_delete_list) == 0:
        sys.exit(0)
    else:
        print(set_delete_list)
        close = tkinter.messagebox.askyesnocancel("提示", "将删除以上内容")
        if close:
            for a in range(0, len(set_delete_list)):
                # 检测是文件还是文件夹
                if set_delete_list[a].find("mp4") != -1:
                    os.remove(set_delete_list[a])
                    print("删除文件")
                else:
                    shutil.rmtree(set_delete_list[a])
                    print("删除文件夹")
            sys.exit(0)
        if close is None:
            pass
        else:
            print("删除取消")
            sys.exit(0)


btn_Random_video = tkinter.Button(player, text="随机视频", height=4, width=16, command=random_video)  # 随机视频
btn_Random_video.place(x=40, y=30)

btn_Random_video = tkinter.Button(player, text="删除路径", height=4, width=16, command=delete_video)  # 随机视频
btn_Random_video.place(x=40, y=140)

listbox_history = tkinter.Listbox(player, width=20, height=20, )
listbox_history.bind('<Double-Button-1>', buttonList)  # 双击事件
listbox_history.place(x=198, y=10)

# 让程序关闭之前执行删除指令
player.protocol("WM_DELETE_WINDOW", callbackClose)

player.mainloop()
