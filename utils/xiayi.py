import os
import time
from pathlib import Path
from pprint import pprint
from types import NoneType

import win32api
import win32con
import win32gui
from PIL import ImageGrab
from aip import AipOcr
from loguru import logger
from paddleocr import PaddleOCR

# 切换文件继续记录
logger.add('../logs/xiayi_{time:YYYY-MM-DD}.log', rotation="200 MB")  # 每个文件200M
# logger.add('../logs/xiayi_{time}.log', rotation='00:00') # 每天0点新建文件继续记录

# 清理
# logger.add('../logs/xiayi_{time}.log', retention='10 days') # 10天一清理

# 压缩
# logger.add('../logs/xiayi_{time}.log', compression='zip') # 压缩为zip

# from logger import get_logger
# 百度 OCR 配置
APP_ID = '6690251'
API_KEY = 'g0B8vbOJtFSAgGYuFDbAWGtN'
SECRET_KEY = 'v5PuD7xxFKJFoNIavBGVvnLeopp9InU4'

XIAYI_DICT1 = {'杏花村': 1, '丐帮': 2, '峨嵋派': 3, '齐云山': 4, '武当山': 5}
XIAYI_DICT2 = {1: {'杏花村', '桃花谷'}, 2: {'丐帮', '正帮'}, 3: {'峨眉派','心素派'}, 4: {'齐云山', '华山派'},
               5: {'武当山', '武当派'}}
NAMES = ('5米每月刷侠义', '侠义领导者', '波浪')

ocr = PaddleOCR(use_angle_cls=True, lang="ch")  # need to run only once to download and load model into memory

# 直接获取logger实例
# logger = get_logger("xiayi")

# 获取当前脚本的目录
script_directory = Path(__file__).resolve().parent

# 向上查找，直到找到项目根目录
# project_root = script_directory.parent
project_root = os.path.join(os.path.expanduser('~'), 'xiayi')


# print(f"项目根目录: {project_root}")


def get_window_by_title_prefix(prefix):
    """获取指定标题前缀的窗口句柄"""
    result = []

    def callback(hwnd, windows):
        if win32gui.IsWindowVisible(hwnd):
            title = win32gui.GetWindowText(hwnd)
            if title.startswith(prefix):
                windows.append(hwnd)

    win32gui.EnumWindows(callback, result)
    return result[0] if result else None


# 判断结束，点击推出
def judge_end_and_exit(hwnd):
    # 判断结束，每隔一秒循环截图
    while True:
        text = capture_and_recognize_text(0, 0, 0, 0, hwnd)
        text = str(text)
        logger.info(text)
        if text.find('结算奖励') > -1:
            now = time.strftime("%Y%m%d%H%M%S", time.localtime())
            logger.info(now)
            img = capture_window(0, 0, 0, 0, hwnd)
            if img:
                # 保存截图
                ensure_directory_exists('imgs')
                file_name = "capture_" + now + ".png"
                path = os.path.join(str(project_root), 'imgs', file_name)
                img.save(path)
                logger.info("已保存截图到 " + file_name)
            else:
                logger.info("结算奖励截图失败!")
            break
        time.sleep(1)
    # 点击退出，继续在系统界面等待
    click_at(273, 998, hwnd)


def capture_window(x1, y1, x2, y2, hwnd):
    """捕获窗口指定区域的截图"""
    try:
        # 获取窗口位置
        window_left, window_top, window_right, window_bottom = win32gui.GetWindowRect(hwnd)
        # logger.info(f"窗口位置: 左={window_left}, 上={window_top}, 右={window_right}, 下={window_bottom}")
        # 计算要截取的区域（相对于屏幕的绝对坐标）
        if x1 == 0:
            x1 = window_left
            y1 = window_top
            x2 = window_right
            y2 = window_bottom
        else:
            x1 = window_left + x1  # 左上角x坐标
            y1 = window_top + y1  # 左上角y坐标
            x2 = window_left + x2  # 右下角x坐标
            y2 = window_top + y2  # 右下角y坐标

        logger.info(f"截图区域: ({x1}, {y1}) -> ({x2}, {y2})")

        # 截取指定区域
        img = ImageGrab.grab(bbox=(x1, y1, x2, y2))
        return img

    except Exception as e:
        logger.info(f"截图时出错: {str(e)}")
        return None


def recognize_text_baidu(image_path):
    """使用百度 OCR API 识别文字"""
    client = AipOcr(APP_ID, API_KEY, SECRET_KEY)

    # 读取图片
    with open(image_path, 'rb') as fp:
        image = fp.read()

    # 调用通用文字识别（高精度版）
    options = {
        'detect_direction': 'true',
        'language_type': 'CHN_ENG',
    }
    result = client.basicAccurate(image, options)

    # 提取识别文字
    if 'words_result' in result:
        return '\n'.join([item['words'] for item in result['words_result']])
    return ''


def recognize_text_paddleocr(image_path, loc=False):
    if not os.path.exists(image_path):
        print(f"文件不存在: {image_path}")
        return  # 或者其他处理逻辑

    # ocr = PaddleOCR()  # 初始化OCR
    result = ocr.ocr(image_path, cls=True)
    if result is None or str(result) == '[None]' or len(result) == 0 or loc:
        pprint('直接返回')
        return result
    pprint('------------')
    pprint(result)
    pprint('------------')
    pprint(str(result))
    pprint(type(result))
    pprint(type(result) == NoneType)
    pprint(result is [None])
    pprint(str(result) == '[None]')
    # 提取识别到的文本
    extracted_texts = []
    for line in result:
        for word_info in line:
            text = word_info[1][0]  # 提取文本
            extracted_texts.append(text)
    # print(extracted_texts)
    return extracted_texts


def print_list(res):
    for re in res:
        logger.info(re)


def xiayi_list_contain_judge(data_list, text):
    for e in data_list:
        if text.find(e) > -1:
            return True
    return False


def click_at(x, y, hwnd, double_click=False):
    window_left, window_top, window_right, window_bottom = win32gui.GetWindowRect(hwnd)
    x = window_left + x
    y = window_top + y

    """在指定坐标执行点击"""
    win32api.SetCursorPos((x, y))
    time.sleep(0.1)  # 等待鼠标移动到位

    # 执行点击
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    time.sleep(0.1)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)

    # 如果是双击，执行第二次点击
    if double_click:
        time.sleep(0.1)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
        time.sleep(0.1)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)

    time.sleep(0.2)
    # 单击
    # click_at(x, y)

    # 双击
    # click_at(x, y, double_click=True)

    # 拖动
    # drag(start_x, start_y, end_x, end_y, duration=0.5)


def drag(start_x, start_y, end_x, end_y, hwnd, duration=0.5):
    window_left, window_top, window_right, window_bottom = win32gui.GetWindowRect(hwnd)
    start_x, start_y = window_right - start_x, window_bottom - start_y
    end_x, end_y = window_right - end_x, window_bottom - end_y

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
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
    time.sleep(0.2)


def set_window_pos(hwnd, x, y, width, height):
    """根据窗口句柄设置窗口位置和大小"""
    if hwnd:
        try:
            # 如果窗口是最小化状态，先恢复它
            if win32gui.IsIconic(hwnd):
                win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
                logger.info(f"已恢复最小化窗口")
                time.sleep(0.1)  # 给窗口一些恢复的时间

            # 设置窗口位置和大小，并保持在最前端 (HWND_TOPMOST)
            win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, x, y, width, height,
                                  win32con.SWP_SHOWWINDOW)

            # 设置窗口扩展样式，使其始终保持在最前端
            # style = win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)
            # win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, style | win32con.WS_EX_TOPMOST)

            # 尝试激活窗口
            # try:
            #     win32gui.ShowWindow(hwnd, win32con.SW_SHOW)
            #     win32gui.BringWindowToTop(hwnd)
            # except Exception as e:
            #     logger.info(f"激活窗口时出现警告（不影响使用）: {str(e)}")

            title = win32gui.GetWindowText(hwnd)
            logger.info(f"已设置窗口 '{title}' (句柄: {hwnd}):")
            logger.info(f"位置: ({x}, {y})")
            logger.info(f"大小: {width} x {height}")
            logger.info("已设置为始终保持在最前端")

        except Exception as e:
            logger.info(f"设置窗口时出现错误: {str(e)}")
    else:
        logger.info(f"无效的窗口句柄: {hwnd}")


def append_to_txt(text, filename):
    """追加文本到TXT文件"""
    try:
        with open(filename, 'a', encoding='utf-8') as f:
            f.write('\n' + text)
        logger.info(f"文本已追加到: {filename}")
        return True
    except Exception as e:
        logger.info(f"追加文件时出错: {str(e)}")
        return False


def append_nothing_to_txt(text, filename):
    """追加文本到TXT文件"""
    try:
        with open(filename, 'a', encoding='utf-8') as f:
            f.write(text)
        logger.info(f"文本已追加到: {filename}")
        return True
    except Exception as e:
        logger.info(f"追加文件时出错: {str(e)}")
        return False


def read_txt(filename, last_line_only=False):
    """读取TXT文件
    参数:
        filename: 文件名
        last_line_only: 是否只返回最后一行
    """
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            if last_line_only:
                # 方法1：读取所有行并获取最后一行
                lines = f.readlines()
                content = lines[-1] if lines else ""
                logger.info(f"已读取文件最后一行: {filename}")
            else:
                content = f.read()
                logger.info(f"已读取整个文件: {filename}")
        return content
    except FileNotFoundError:
        logger.info(f"文件不存在: {filename}")
        return None
    except Exception as e:
        logger.info(f"读取文件时出错: {str(e)}")
        return None


def capture_and_recognize_text(x1, y1, x2, y2, hwnd, loc=False):
    # 捕获窗口的截图
    img = capture_window(x1, y1, x2, y2, hwnd)
    text = ''
    if img:
        # 保存截图
        ensure_directory_exists('imgs')
        path = os.path.join(str(project_root), 'imgs', 'capture.png')
        # path = str(project_root) + "/imgs/capture.png"
        img.save(path)
        logger.info("已保存截图到 {}", path)
        # 识别文字
        text = recognize_text_paddleocr(path, loc)
        return text


# def get_root_path():
#     # 获取当前脚本的目录
#     script_directory = Path(__file__).resolve().parent
#
#     # 向上查找，直到找到项目根目录
#     project_root = script_directory.parent
#     print(f"项目根目录: {project_root}")
#     return project_root


def ensure_directory_exists(sub_dir, parent_dir=project_root):
    # 构建完整的子目录路径
    full_path = os.path.join(parent_dir, sub_dir)

    # 判断子目录是否存在
    if not os.path.exists(full_path):
        # 如果不存在，则创建子目录
        os.makedirs(full_path)
        print(f"创建目录: {full_path}")
    else:
        print(f"目录已存在: {full_path}")

def init():
    # 找到目标窗口
    hwnd = get_window_by_title_prefix("墨迹大侠")

    if not hwnd:
        logger.info("未找到墨迹大侠窗口")
        return False  # 返回False表示未找到窗口

    title = win32gui.GetWindowText(hwnd)
    logger.info(f"找到窗口: {title}")

    # # 设置窗口大小和位置
    set_window_pos(hwnd, -6, 0, 568, 1033)
    time.sleep(1)
    return hwnd

def main():
    # image_path = 'capture.png'  # 确保这个路径是正确的
    # print(f"正在处理的图像路径: {image_path}")
    # print(os.getcwd())
    # recognize_text_paddleocr(image_path)
    # print(os.path.expanduser("~/.paddleocr/"))
    # 使用绝对路径
    # file_path = os.path.join(os.getcwd(), 'progress', '20250411.txt')
    # print(file_path)
    # print(os.getcwd())
    # if not os.path.exists('progress'):
    #     os.makedirs('progress')
    # txt_file = "progress/20250411.txt"
    # append_nothing_to_txt("", file_path)

    # print (os.environ['HOME'])

    # print (os.path.expandvars('$HOME'))
    # print (os.path.expanduser('~'))
    # project_root = os.path.join(os.path.expanduser('~'), 'xiayi')
    path = os.path.join(str(project_root), 'imgs', 'capture.png')
    # path = str(project_root) + "/imgs/capture.png"
    # img.save(path)
    # logger.info("已保存截图到 {}", path)
    # 识别文字
    text = recognize_text_paddleocr(path)
    pprint(text)


if __name__ == "__main__":
    main()
