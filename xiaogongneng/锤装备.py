import sys
import os
import time
from pprint import pprint
import random

import win32api
import win32gui

from utils.xiayi import click_at

# 将项目根目录添加到 sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils import xiayi


def main():
    hwnd = xiayi.get_window_by_title_prefix("墨迹大侠")
    text = xiayi.capture_and_recognize_text(0, 0, 0, 0, hwnd, True)
    pprint(text)
    while True:
        # 1.点击锻铸
        # key = '锻铸'
        # xiayi.recognize_and_click(text, hwnd, key)
        time.sleep(10)
        # 2.对比属性
        text = xiayi.capture_and_recognize_text(0, 0, 0, 0, hwnd, True)
        pprint('================================================')
        pprint(text)
        result = str(text)
        index = result.find('评分')
        point1 = 0
        point2 = 0
        if index != -1:
            point1 = int(result[index + 3:index + 4])
        print('index:{}', index)
        print('point1:{}', point1)
        index = result.find('评分', index + 1)
        if index == -1:
            # xiayi.click_at(260, 512, hwnd)
            # window_left, window_top, window_right, window_bottom = win32gui.GetWindowRect(hwnd)
            # x = window_left + 271
            # y = window_top + 621
            # text = xiayi.capture_and_recognize_text(0, 0, 0, 0, hwnd, True,True)
            # key = '装备'
            # xiayi.recognize_and_click(text, hwnd, key)
            # """在指定坐标执行点击"""
            # win32api.SetCursorPos((x, y))
            # xiayi.click_at(271, 621, hwnd)
            time.sleep(1)
            continue
        try:
            point2 = int(result[index + 3:index + 4])
            print('index:{}', index)
            print('point2:{}', point2)
            point1 = 0
        except Exception as e:
            print(e)
        if point2 > point1:
            key = '替换'
            xiayi.recognize_and_click(text, hwnd, key)
        else:
            key = '分解'
            xiayi.recognize_and_click(text, hwnd, key)

        time.sleep(0.5)
        xiayi.click_at(403, 600, hwnd)
        time.sleep(0.5)





if __name__ == "__main__":
    main()
