import time
from pprint import pprint

import win32api
import win32con

from utils import xiayi


def main():
    # 初始化窗口大小
    key_prefix = '墨迹大侠'
    hwnd = xiayi.init(key_prefix)

    name_list = []

    for i in range(14):
        text = xiayi.capture_and_recognize_text(44, 694, 456, 810, hwnd, False, True)
        # pprint(text)
        name_list.append(text)

        drag1(517, 744, 56, 740)
        time.sleep(1)

    pprint(name_list)
    pprint(len(name_list))


def drag(start_x, start_y, end_x, end_y):
    win32api.SetCursorPos((start_x, start_y))

    # 按下鼠标
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)

    # time.sleep(2)
    win32api.SetCursorPos((end_x, end_y))
    # 释放鼠标
    # time.sleep(3)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)


def drag1(start_x, start_y, end_x, end_y, duration=0.5):
    # window_left, window_top, window_right, window_bottom = win32gui.GetWindowRect(hwnd)
    # start_x, start_y = window_right - start_x, window_bottom - start_y
    # end_x, end_y = window_right - end_x, window_bottom - end_y

    """执行拖动操作"""
    # 移动到起始位置
    win32api.SetCursorPos((start_x, start_y))
    time.sleep(0.1)

    # 按下鼠标
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)

    # 计算移动步骤
    steps = 20
    sleep_time = duration / steps
    dx = (end_x - start_x) / steps
    dy = (end_y - start_y) / steps

    # 平滑移动
    for i in range(steps):
        x = int(start_x + dx * (i + 1))
        y = int(start_y + dy * (i + 1))
        win32api.SetCursorPos((x, y))
        time.sleep(sleep_time)

    # 释放鼠标
    time.sleep(2)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
    time.sleep(0.2)


if __name__ == '__main__':
    main()
