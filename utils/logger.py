import os
import logging
import logging.handlers
from datetime import datetime
import colorama
from colorama import Fore, Style
import functools

# 初始化colorama
colorama.init()


class ColoredFormatter(logging.Formatter):
    """自定义的彩色日志格式器"""
    COLORS = {
        'DEBUG': Fore.BLUE,
        'INFO': Fore.GREEN,
        'WARNING': Fore.YELLOW,
        'ERROR': Fore.RED,
        'CRITICAL': Fore.RED + Style.BRIGHT,
    }

    def format(self, record):
        if getattr(record, 'color_enabled', True):
            levelname = record.levelname
            if levelname in self.COLORS:
                record.levelname = f"{self.COLORS[levelname]}{levelname}{Style.RESET_ALL}"
        return super().format(record)


class Logger:
    _instance = None
    _initialized = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not Logger._initialized:
            self._loggers = {}
            self._setup_basic_config()
            Logger._initialized = True

    def _setup_basic_config(self):
        """基础配置"""
        # 创建logs目录
        log_dir = os.path.join(os.getcwd(), 'logs')
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        # 基本日志格式
        self.base_format = '%(asctime)s [%(levelname)s] [%(name)s:%(filename)s:%(lineno)d] %(message)s'
        self.date_format = '%Y-%m-%d %H:%M:%S'

    def _create_file_handler(self, logger_name):
        """创建文件处理器"""
        log_file = os.path.join('logs', f'{logger_name}_{datetime.now().strftime("%Y%m%d")}.log')
        file_handler = logging.handlers.RotatingFileHandler(
            log_file,
            maxBytes=10 * 1024 * 1024,  # 10MB
            backupCount=5,
            encoding='utf-8'
        )
        file_handler.setFormatter(logging.Formatter(self.base_format, self.date_format))
        return file_handler

    def _create_console_handler(self):
        """创建控制台处理器"""
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(ColoredFormatter(self.base_format, self.date_format))
        return console_handler

    def get_logger(self, name):
        """获取logger实例"""
        if name not in self._loggers:
            logger = logging.getLogger(name)
            logger.setLevel(logging.DEBUG)

            # 清除现有处理器
            logger.handlers.clear()

            # 添加处理器
            logger.addHandler(self._create_file_handler(name))
            logger.addHandler(self._create_console_handler())

            # 防止日志向上传递
            logger.propagate = False

            self._loggers[name] = logger

        return self._loggers[name]


def get_logger(name=None):
    """
    获取logger的装饰器或直接返回logger实例
    """
    if name is None:
        # 作为装饰器使用
        def decorator(cls_or_func):
            if isinstance(cls_or_func, type):  # 如果是类
                original_init = cls_or_func.__init__

                @functools.wraps(original_init)
                def new_init(self, *args, **kwargs):
                    self.logger = Logger().get_logger(cls_or_func.__name__)
                    original_init(self, *args, **kwargs)

                cls_or_func.__init__ = new_init
                return cls_or_func
            else:  # 如果是函数
                return Logger().get_logger(cls_or_func.__name__)

        return decorator
    else:
        # 直接返回logger实例
        return Logger().get_logger(name)