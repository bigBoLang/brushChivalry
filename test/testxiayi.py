from aip import AipOcr
import win32gui
import win32con
from PIL import Image, ImageGrab
import os
import time

# 百度 OCR 配置
APP_ID = '6690251'
API_KEY = 'g0B8vbOJtFSAgGYuFDbAWGtN'
SECRET_KEY = 'v5PuD7xxFKJFoNIavBGVvnLeopp9InU4'

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

def capture_window(hwnd):
    """捕获窗口指定区域的截图"""
    try:
        # 获取窗口位置
        window_left, window_top, window_right, window_bottom = win32gui.GetWindowRect(hwnd)
        print(f"窗口位置: 左={window_left}, 上={window_top}, 右={window_right}, 下={window_bottom}")

        # 计算要截取的区域（相对于屏幕的绝对坐标）
        x1 = window_left + 120    # 左上角x坐标
        y1 = window_top + 700    # 左上角y坐标
        x2 = window_left + 495   # 右下角x坐标
        y2 = window_top + 869    # 右下角y坐标

        print(f"截图区域: ({x1}, {y1}) -> ({x2}, {y2})")

        # 截取指定区域
        img = ImageGrab.grab(bbox=(x1, y1, x2, y2))
        return img

    except Exception as e:
        print(f"截图时出错: {str(e)}")
        return None

def recognize_text(image_path):
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

def main():
    hwnd = get_window_by_title_prefix("墨迹大侠")
    if not hwnd:
        print("未找到墨迹大侠窗口")
        return

    title = win32gui.GetWindowText(hwnd)
    print(f"找到窗口: {title}")

    try:
        while True:
            # 捕获整个窗口的截图
            img = capture_window(hwnd)
            if img:
                # 保存截图
                img.save("capture.png")
                print("已保存截图到 capture.png")

                # 识别文字
                text = recognize_text("capture.png")
                if text.strip():
                    print("\n识别到的文字:")
                    print("-" * 40)
                    print(text.strip())
                    print("-" * 40)
                else:
                    print("未识别到文字")

            # 等待用户输入
            input("\n按回车键继续截图，Ctrl+C退出...")

    except KeyboardInterrupt:
        print("\n程序已退出")

if __name__ == "__main__":
    main()
