import time
from pprint import pprint

from loguru import logger

from utils import xiayi

logger.add('logs/xihao_{time:YYYY-MM-DD}.log', rotation="200 MB")  # 每个文件200M


# call:beforestart
#
# echo for2 game 1
# for /l %%i in (1, 1, 2) do (
#     echo game 1
#     call:jumptoone
#     call:fornext 0
#     call:play
# )

def before_start(hwnd):
    # 直接用点击
    wait_time = 0
    for i in range(4):
        # 精英
        xiayi.click_at(325, 292, hwnd)
        invite(hwnd)


def next_game(hwnd, times):
    # 选关
    xiayi.click_at(279, 456, hwnd)
    for i in range(times):
        # 右边箭头
        xiayi.click_at(533, 467, hwnd)
    # 选择
    xiayi.click_at(283, 983, hwnd)


def invite(hwnd):
    # 加号，邀请好友
    xiayi.click_at(367, 646, hwnd)
    # 在线玩家
    xiayi.click_at(346, 215, hwnd)
    # 快捷喊话
    xiayi.click_at(139, 899, hwnd)
    # 叉号
    xiayi.click_at(522, 144, hwnd)
    # 普通
    xiayi.click_at(240, 290, hwnd)


def jump_to_one(hwnd):
    # 精英
    xiayi.click_at(325, 292, hwnd)
    # 选关
    xiayi.click_at(279, 456, hwnd)
    # 左边箭头
    for i in range(20):
        xiayi.click_at(26, 469, hwnd)
    # 选择
    xiayi.click_at(283, 983, hwnd)


def main():
    # 初始化：找到窗口，设置窗口大小，位置
    hwnd = xiayi.init()
    if not hwnd:
        return False

    # before_start(hwnd)

    for i in range(5):
        for j in range(2):
            logger.info('第' + str(i + 1) + '关,' + '第' + str(j + 1) + '次')
            # 跳到第一关
            jump_to_one(hwnd)
            # 下一关
            next_game(hwnd, i)
            # 邀请好友
            invite(hwnd)
            # 点击挑战
            xiayi.click_at(285, 807, hwnd)
            pprint('开始')
            start = time.time()
            # 休眠6分钟
            # 判断结束
            # 先等6分钟
            time.sleep(6 * 60 - 30)

            # 判断结束，每隔一秒循环截图
            xiayi.judge_end_and_exit(hwnd)
            end = time.time()
            logger.info('用时:' + str(end - start))


if __name__ == '__main__':
    main()
