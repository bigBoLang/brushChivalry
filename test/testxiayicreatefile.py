import json
import os
import time
from datetime import datetime
import logging
from logging.handlers import RotatingFileHandler

def setup_logging():
    """设置日志系统"""
    try:
        # 创建logs目录
        if not os.path.exists('logs'):
            os.makedirs('logs')

        # 生成日志文件名
        log_file = os.path.join('logs', f'file_operations_{datetime.now().strftime("%Y%m%d")}.log')

        # 创建日志格式
        formatter = logging.Formatter(
            '%(asctime)s [%(levelname)s] %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

        # 设置文件处理器（滚动日志，最大10MB，保留5个备份）
        file_handler = RotatingFileHandler(
            log_file, 
            maxBytes=10*1024*1024,  # 10MB
            backupCount=5,
            encoding='utf-8'
        )
        file_handler.setFormatter(formatter)

        # 设置控制台处理器
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)

        # 配置根日志记录器
        logger = logging.getLogger()
        logger.setLevel(logging.DEBUG)
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

        logging.info(f"日志系统初始化完成，日志文件: {log_file}")
        return log_file

    except Exception as e:
        print(f"设置日志系统时出错: {str(e)}")
        return None

def save_to_json(data, filename):
    """保存数据到JSON文件"""
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        logging.info(f"数据已保存到: {filename}")
        return True
    except Exception as e:
        logging.error(f"保存文件时出错: {str(e)}")
        return False

def load_from_json(filename):
    """从JSON文件加载数据"""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
        logging.info(f"已从 {filename} 加载数据")
        return data
    except FileNotFoundError:
        logging.warning(f"文件不存在: {filename}")
        return None
    except Exception as e:
        logging.error(f"读取文件时出错: {str(e)}")
        return None

def save_to_txt(text, filename):
    """保存文本到TXT文件"""
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(text)
        logging.info(f"文本已保存到: {filename}")
        return True
    except Exception as e:
        logging.error(f"保存文件时出错: {str(e)}")
        return False

def append_to_txt(text, filename):
    """追加文本到TXT文件"""
    try:
        with open(filename, 'a', encoding='utf-8') as f:
            f.write(text + '\n')
        logging.info(f"文本已追加到: {filename}")
        return True
    except Exception as e:
        logging.error(f"追加文件时出错: {str(e)}")
        return False

def read_txt(filename, last_line_only=False):
    """读取TXT文件"""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            if last_line_only:
                lines = f.readlines()
                content = lines[-1] if lines else ""
                logging.info(f"已读取文件最后一行: {filename}")
            else:
                content = f.read()
                logging.info(f"已读取整个文件: {filename}")
        return content
    except FileNotFoundError:
        logging.warning(f"文件不存在: {filename}")
        return None
    except Exception as e:
        logging.error(f"读取文件时出错: {str(e)}")
        return None

def main():
    # 设置日志系统
    log_file = setup_logging()
    if not log_file:
        return

    logging.info("程序启动")
    
    try:
        # 创建示例数据
        click_data = {
            "clicks": [
                {
                    "x": 100,
                    "y": 200,
                    "type": "single",
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                },
                {
                    "x": 150,
                    "y": 250,
                    "type": "double",
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
            ]
        }

        # 示例1：JSON文件操作
        json_file = "clicks.json"
        logging.info("\n=== JSON文件操作演示 ===")
        save_to_json(click_data, json_file)
        loaded_data = load_from_json(json_file)
        if loaded_data:
            logging.info("加载的数据:")
            logging.info(json.dumps(loaded_data, ensure_ascii=False, indent=4))

        # 示例2：TXT文件操作
        txt_file = "log.txt"
        logging.info("\n=== TXT文件操作演示 ===")
        
        save_to_txt("这是第一行\n这是第二行", txt_file)
        append_to_txt(f"这是追加的内容 - {datetime.now()}", txt_file)
        
        # 读取文本（全部内容）
        logging.info("\n=== 显示全部内容 ===")
        content = read_txt(txt_file)
        if content:
            logging.info("文件内容:")
            logging.info(content)

        # 读取文本（仅最后一行）
        logging.info("\n=== 显示最后一行 ===")
        last_line = read_txt(txt_file, last_line_only=True)
        if last_line:
            logging.info("最后一行内容:")
            logging.info(last_line.strip())

        # 示例3：自动生成文件名
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        auto_filename = f"clicks_{timestamp}.json"
        logging.info(f"\n=== 使用时间戳生成文件名: {auto_filename} ===")
        save_to_json(click_data, auto_filename)

    except Exception as e:
        logging.error(f"程序运行时出错: {str(e)}", exc_info=True)
    
    logging.info("程序结束")

if __name__ == "__main__":
    main()
