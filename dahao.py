import os.path
import threading
import time
import datetime

import win32gui
from loguru import logger

from utils import xiayi

logger.add('logs/dahao_{time:YYYY-MM-DD}.log', rotation="200 MB")  # 每个文件200M


# pyinstaller --name="dahao_controller" --windowed --onefile --clean --exclude PyQt5 --exclude PyQt6 --debug all dahao_controller.py

# pyinstaller --name="dahao" --windowed --onefile --clean --noconfirm dahao.py


def go_system_window_and_wait(hwnd):
    # 读取自己的资源进度情况
    # 追加文本
    # 每天一次
    xiayi.ensure_directory_exists('progress')

    today = datetime.date.today()
    txt_file = str(today) + ".txt"
    txt_file = os.path.join(xiayi.project_root, 'progress', txt_file)
    xiayi.append_nothing_to_txt("", txt_file)

    # 读取文本
    last_line = xiayi.read_txt(txt_file, last_line_only=True)
    # logger.info("整个文件:", last_line)
    if last_line == '':
        last_line = '1 0'
    # 内容映射
    logger.info("最后一行", str(last_line))
    last_level = last_line.split(" ")
    level = int(last_level[0])
    count = int(last_level[1])
    if count == 2 or count == 3:
        level = int(last_level[0]) + 1
        count = 0

    xiayi.print_list(xiayi.XIAYI_DICT2[level])

    # 去系统界面
    goto_system_window(hwnd)

    # 每秒识别一下是否是自己需要的资源
    while True:
        text = xiayi.capture_and_recognize_text(120, 700, 495, 869, hwnd)
        text = str(text)
        if text != '' and xiayi.xiayi_list_contain_judge(xiayi.XIAYI_DICT2[level], text) and text.find(
                '点击加入') > -1 and xiayi.xiayi_list_contain_judge(xiayi.NAMES, text) == True:
            chuli(text, level, count, txt_file, hwnd)
        else:
            xiayi.drag(50, 200, 50, 500, hwnd)
            # 截图并文字识别出当前邀请是否是自己需要的资源
            text = xiayi.capture_and_recognize_text(120, 700, 495, 869, hwnd)
            text = str(text)
            chuli(text, level, count, txt_file, hwnd)
        time.sleep(3)


def chuli(text, level, count, txt_file, hwnd):
    # 判断是否是需要的关卡以及是否是特定的邀请者
    if text == '':
        return
    # 满足1.是需要的关卡资源 2.有点击加入 3.邀请人是特定的邀请人列表里的
    # logger.info(text)
    xiayi.print_list(xiayi.XIAYI_DICT2[level])
    xiayi.print_list(xiayi.NAMES)
    logger.info('---------------')
    logger.info(text.split('\n')[0])
    logger.info('判断是否加入的三个条件--------')
    logger.info('关卡：{}', xiayi.xiayi_list_contain_judge(xiayi.XIAYI_DICT2[level], text))
    logger.info('有点击加入:{}', text.find('点击加入'))
    logger.info('发起者：{}', xiayi.xiayi_list_contain_judge(xiayi.NAMES, text))
    logger.info('判断是否加入的三个条件--------')
    if xiayi.xiayi_list_contain_judge(xiayi.XIAYI_DICT2[level], text) and text.find(
            '点击加入') > -1 and xiayi.xiayi_list_contain_judge(xiayi.NAMES, text) == True:
        # 点击加入
        xiayi.click_at(409, 829, hwnd)
        time.sleep(30)
        # 点击随机技能
        xiayi.click_at(43, 265, hwnd)
        # 先等6分钟
        time.sleep(6 * 60 - 30)

        # 判断结束，每隔一秒循环截图
        xiayi.judge_end_and_exit(hwnd)
        # 刷成功一次，增加资源进度,回写进度文件
        count = count + 1
        text = str(level) + " " + str(count)
        logger.info(text)
        xiayi.append_to_txt(text, txt_file)
        # 继续去系统界面等待
        time.sleep(1)
        goto_system_window(hwnd)


def goto_system_window(hwnd):
    # 先定位到系统界面
    xiayi.click_at(392, 908, hwnd)
    xiayi.click_at(475, 226, hwnd)


# 创建事件对象
stop_event = threading.Event()
pause_event = threading.Event()


def stop():
    stop_event.set()  # 设置停止事件


def pause():
    if pause_event.is_set():
        pause_event.clear()  # 继续执行
    else:
        pause_event.set()  # 暂停执行


def main():
    while not stop_event.is_set():  # 检查是否设置了停止事件
        if pause_event.is_set():  # 检查是否设置了暂停事件
            time.sleep(1)  # 暂停时等待
            continue

        # 执行任务的逻辑

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
        # # 在系统邀请界面等待
        go_system_window_and_wait(hwnd)
        # while True:
        #     print(123)
        #     time.sleep(1)
        # return True  # 执行成功返回True

        time.sleep(2)  # 模拟任务执行时间


if __name__ == "__main__":
    main()
