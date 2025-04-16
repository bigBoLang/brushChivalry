import os.path
import threading
import time
import datetime

import win32gui
from loguru import logger
from sympy import pprint

from utils import xiayi


# logger.add('logs/dahao_{time:YYYY-MM-DD}.log', rotation="200 MB")  # 每个文件200M
def setup_logger(log_queue):
    logger.remove()  # 移除默认的日志处理器
    logger.add("logs/dahao_{time:YYYY-MM-DD}.log", rotation="200 MB")  # 每个文件200M
    logger.add(lambda msg: log_queue.put(msg), level="INFO")  # 将日志输出到队列


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

    for i in range(10):
        # 读取文本
        last_line = xiayi.read_txt(txt_file, last_line_only=True)
        # logger.info("整个文件:", last_line)
        if last_line == '':
            last_line = '1 0'
        # 内容映射
        logger.info("最后一行", str(last_line))
        if str(last_line) == '5 2':
            logger.info('今天的侠义已经刷完啦！！！')
            break
        last_level = last_line.split(" ")
        level = int(last_level[0])
        count = int(last_level[1])
        if count == 2:
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
                flag = chuli(text, level, count, txt_file, hwnd)
            else:
                xiayi.drag(516, 843, 516, 643, hwnd)
                # 截图并文字识别出当前邀请是否是自己需要的资源
                text = xiayi.capture_and_recognize_text(120, 700, 495, 869, hwnd)
                text = str(text)
                flag = chuli(text, level, count, txt_file, hwnd)
            logger.info('flag:{}', flag)
            time.sleep(2)
            if flag:
                break


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
        logger.info('休眠360s')
        time.sleep(360)

        # 判断结束，每隔一秒循环截图
        xiayi.judge_end_and_exit(hwnd)
        # 刷成功一次，增加资源进度,回写进度文件
        count = count + 1
        text = str(level) + " " + str(count)
        logger.info(text)
        xiayi.append_to_txt(text, txt_file)
        # 继续去系统界面等待
        time.sleep(1)
        return True
        # goto_system_window(hwnd)
    return False


def goto_system_window(hwnd):
    # 先定位到系统界面
    logger.info('跳转到系统界面!!!!')
    time.sleep(1)
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
    # 初始化
    hwnds = xiayi.init('墨迹大侠', False)
    if not hwnds:
        return False

    result = xiayi.recognize_dahao(hwnds)
    logger.info('识别结果句柄：{}', result)
    for hwnd in result:
        # 在系统邀请界面等待
        go_system_window_and_wait(hwnd)


if __name__ == "__main__":
    # xiayi.get_window_by_title_prefix('墨迹大侠')
    main()
