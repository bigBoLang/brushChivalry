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
        key = '鼓舞'
        xiayi.recognize_and_click(text, hwnd, key)
        time.sleep(0.1)





if __name__ == "__main__":
    main()
