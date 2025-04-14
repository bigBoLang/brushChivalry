import win32gui
import win32con
import win32api
import time
from pynput import mouse

def get_windows_by_title_prefix(prefix):
    """获取指定标题前缀的所有窗口句柄"""
    result = []
    def callback(hwnd, windows):
        if win32gui.IsWindowVisible(hwnd):
            title = win32gui.GetWindowText(hwnd)
            if title.startswith(prefix):
                windows.append(hwnd)
    win32gui.EnumWindows(callback, result)
    return result

def click_at(x, y, double_click=False):
    """在指定坐标执行点击"""
    # 激活窗口
    win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)  # 恢复窗口
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

def drag(start_x, start_y, end_x, end_y, duration=0.5):
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

class ClickRecorder:
    def __init__(self):
        self.last_click_time = 0
        self.last_click_pos = None
        self.drag_start = None
        self.is_dragging = False

    def on_click(self, x, y, button, pressed):
        """鼠标点击事件回调"""
        if button == mouse.Button.left:
            hwnd = win32gui.WindowFromPoint((x, y))
            title = win32gui.GetWindowText(hwnd)
            
            if title.startswith("墨迹大侠"):
                window_left, window_top, _, _ = win32gui.GetWindowRect(hwnd)
                relative_x = x - window_left
                relative_y = y - window_top
                
                if pressed:
                    # 开始可能的拖动
                    self.drag_start = (x, y)
                    current_time = time.time()
                    
                    # 检测双击
                    if (current_time - self.last_click_time < 0.3 and 
                        self.last_click_pos == (relative_x, relative_y)):
                        print(f"\n双击位置: ({relative_x}, {relative_y})")
                    else:
                        print(f"\n单击位置: ({relative_x}, {relative_y})")
                        
                    self.last_click_time = current_time
                    self.last_click_pos = (relative_x, relative_y)
                else:
                    # 检测是否为拖动
                    if self.drag_start:
                        dx = x - self.drag_start[0]
                        dy = y - self.drag_start[1]
                        if abs(dx) > 5 or abs(dy) > 5:  # 移动超过5像素认为是拖动
                            print(f"\n拖动: 从({relative_x-dx}, {relative_y-dy}) 到 ({relative_x}, {relative_y})")
                        self.drag_start = None

    def on_move(self, x, y):
        """鼠标移动事件回调"""
        pass

def main():
    windows = get_windows_by_title_prefix("墨迹大侠")
    
    if not windows:
        print("未找到墨迹大侠窗口")
        return
    
    print(f"找到 {len(windows)} 个墨迹大侠窗口:")
    for hwnd in windows:
        title = win32gui.GetWindowText(hwnd)
        left, top, right, bottom = win32gui.GetWindowRect(hwnd)
        print(f"\n窗口标题: {title}")
        print(f"窗口句柄: {hwnd}")
        print(f"窗口位置: 左={left}, 上={top}, 右={right}, 下={bottom}")

    print("\n请在墨迹大侠窗口内操作:")
    print("- 单击: 显示点击位置")
    print("- 双击: 显示双击位置")
    print("- 拖动: 显示拖动起点和终点")
    print("按Ctrl+C退出程序")

    # recorder = ClickRecorder()
    window_left, window_top, window_right, window_bottom = win32gui.GetWindowRect(hwnd)
    x = window_left + 200
    y = window_top + 500
    start_x,start_y = window_right -100,window_bottom - 300
    end_x,end_y = window_right - 100,window_bottom - 500
    # 单击
    # click_at(x, y)

    # 双击
    # click_at(x, y, double_click=True)

    # 拖动
    drag(start_x, start_y, end_x, end_y, duration=0.5)

if __name__ == "__main__":
    main()
