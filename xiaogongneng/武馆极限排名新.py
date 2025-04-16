import time
from pprint import pprint
from sys import exception
from time import sleep
from loguru import logger

from utils import xiayi
from playsound import playsound
import pyttsx3

logger.add('../logs/wu_guan_ji_xian_rank_{time:YYYY-MM-DD}.log', rotation="200 MB")  # 每个文件200M
engine = pyttsx3.init()



# 设置语音属性（可选）
engine.setProperty('rate', 150)  # 语速
engine.setProperty('volume', 1)  # 音量（0.0 到 1.0）

def get_rank(hwnd):
    text = xiayi.capture_and_recognize_text(35, 230, 502, 372, hwnd, True)
    logger.info(str(text))
    logger.info(str(text[0][0][1][0]))
    try:
        rank = str(text[0][0][1][0]).split('：')[1]
    except IndexError as e:
        pprint(f"数据错误: {str(e)}")
        return False
    return rank


def main():
    hwnd = xiayi.get_window_by_title_prefix("墨迹大侠")
    # 极限排名数组
    rank_list = ['900', '790', '670', '540', '420', '300', '205', '110', '55', '32', '9', '1']
    for i in range(100):

        while True:
            rank = get_rank(hwnd)
            logger.info((rank))
            # engine.say(rank)
            # 等待语音播放完成
            # engine.runAndWait()
            if rank_list.__contains__(rank):
                pprint(rank)
                break
            # 点击刷新
            # 转换文本为语音
            logger.info('刷新')
            xiayi.click_at(271, 856, hwnd)
            time.sleep(11)

        # 点击挑战
        logger.info('挑战')
        # while True:
        #     playsound("../y2460.wav")
        xiayi.click_at(433, 306, hwnd)
        time.sleep(1)
        xiayi.click_at(405, 630, hwnd)
        # time.sleep(100000000000)
        time.sleep(1)



if __name__ == "__main__":
    main()
