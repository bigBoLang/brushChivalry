import os.path
import threading
import time
import datetime
from pprint import pprint

import win32gui

from loguru import logger

from utils import xiayi

logger.add('logs/xihao_{time:YYYY-MM-DD}.log', rotation="200 MB")  # 每个文件200M


def main():
    # 找到目标窗口
    hwnd = xiayi.get_window_by_title_prefix("墨迹大侠")

    if not hwnd:
        logger.info("未找到墨迹大侠窗口")
        return False  # 返回False表示未找到窗口

    title = win32gui.GetWindowText(hwnd)
    logger.info(f"找到窗口: {title}")

    # # 设置窗口大小和位置
    xiayi.set_window_pos(hwnd, -6, 0, 568, 1033)
    time.sleep(1)






if __name__ == '__main__':
    main()
