import time
from pprint import pprint
from sys import exception
from time import sleep

from utils import xiayi


def get_rank(hwnd):
    text = xiayi.capture_and_recognize_text(35, 230, 502, 372, hwnd, True)
    pprint(text)
    pprint(text[0][0][1][0])
    try:
        rank = str(text[0][0][1][0]).split('：')[1]
    except IndexError as e:
        pprint(f"数据错误: {str(e)}")
        return False
    return rank


def main():
    hwnd = xiayi.get_window_by_title_prefix("墨迹大侠")
    # 极限排名数组
    # rank_list = [900, 790, 670, 540, 420, 300, 205, 110, 55, 32, 9, 1]
    rank_list = [900, 792, 672, 542, 422, 302, 207, 112, 57, 34, 11, 1]
    for i in range(100):
        text = xiayi.capture_and_recognize_text(175, 194, 212, 215, hwnd, False, True)
        pprint('text:{}')
        pprint(text)
        if not text or str(text) == '[None]':
            print(11)
            time.sleep(15)
            continue
        if text == '未上榜':
            my_rank = 900
        else:
            my_rank = int(text)
        times = 0
        pprint('my_rank:{}' + str(my_rank))
        index = rank_list.index(my_rank)
        while True:
            rank = get_rank(hwnd)
            if not rank or rank == '0' or len(rank) > 3:
                time.sleep(15)
                continue
            try:
                rank = int(rank)
            except exception() as e:
                pprint(f"数据错误: {str(e)}")
                continue
            pprint(rank)
            if rank <= rank_list[index + 1]:
                pprint(rank)
                break
            # 点击刷新
            pprint('刷新')
            xiayi.click_at(271, 886, hwnd)
            time.sleep(11)
            times += 1
        # 点击挑战
        pprint('挑战')
        # xiayi.click_at(433, 306, hwnd)
        time.sleep(1)
        # xiayi.click_at(405, 630, hwnd)
        pprint(times)
        time.sleep(1)
        time.sleep(500000000)


if __name__ == "__main__":
    main()
