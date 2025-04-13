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
    pprint(123)


if __name__ == '__main__':
    main()
