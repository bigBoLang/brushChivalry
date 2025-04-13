import sys
import os
import time
from pprint import pprint
import random

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
        key = '锻铸'
        recognize_and_click(text, hwnd, key)
        time.sleep(4)
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
            xiayi.click_at(260, 512, hwnd)
        point2 = int(result[index + 3:index + 4])
        print('index:{}', index)
        print('point2:{}', point2)

        if point2 > point1:
            key = '替换'
            recognize_and_click(text, hwnd, key)
        else:
            key = '分解'
            recognize_and_click(text, hwnd, key)

        time.sleep(0.5)
        xiayi.click_at(403, 600, hwnd)
        time.sleep(0.5)


def recognize_and_click(text, hwnd, key):
    res = get_loc_by_text(text[0], key)
    if res is None:
        return
    x, y = get_random_point(res)
    # pprint(x, y)
    x = int(x)
    y = int(y)
    xiayi.click_at(x, y, hwnd)


def get_loc_by_text(data_list, text):
    for data in data_list:
        if data[1][0] == text:
            return data[0]
    return None


def get_random_point(corners):
    # 提取 x 和 y 坐标
    x_coords = [point[0] for point in corners]
    y_coords = [point[1] for point in corners]

    # 计算边界
    min_x = min(x_coords)
    max_x = max(x_coords)
    min_y = min(y_coords)
    max_y = max(y_coords)

    # 生成随机点
    random_x = random.uniform(min_x, max_x)
    random_y = random.uniform(min_y, max_y)

    return random_x, random_y


if __name__ == "__main__":
    main()
