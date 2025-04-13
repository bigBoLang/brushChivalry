import datetime
import queue
import threading
import tkinter as tk
from tkinter import ttk, scrolledtext
from loguru import logger
from dahao import main as dahao_main, stop as dahao_stop, setup_logger  # 导入 setup_logger

# 创建一个全局事件
stop_event = threading.Event()

class DahaoController:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("大号控制器")

        # 获取屏幕宽度和高度
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # 设置窗口大小
        window_width = 600
        window_height = 500

        # 计算窗口位置，使其靠右侧显示
        x_position = screen_width - window_width
        y_position = (screen_height - window_height) // 2  # 垂直居中

        # 设置窗口位置和大小
        self.root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")
        
        # 设置主题色
        self.style = ttk.Style()
        self.style.configure('Custom.TButton', padding=5)
        self.style.configure('Custom.TFrame', background='#f0f0f0')
        
        self.running = False
        self.paused = False
        self.thread = None
        self.log_queue = queue.Queue()
        
        self.setup_ui()
        self.setup_shortcuts()
        self.start_log_monitor()
        
        # 绑定窗口关闭事件
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
    def on_closing(self):
        """处理窗口关闭事件"""
        if self.running:
            stop_event.set()  # 设置停止事件
        self.root.destroy()  # 关闭窗口
        
    def setup_shortcuts(self):
        # 绑定快捷键
        self.root.bind('<F9>', lambda e: self.start())
        self.root.bind('<F10>', lambda e: self.pause())
        self.root.bind('<F11>', lambda e: self.stop())
        
    def setup_ui(self):
        # 主容器
        main_frame = ttk.Frame(self.root, style='Custom.TFrame')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 顶部状态区域
        status_frame = ttk.Frame(main_frame)
        status_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.status_label = ttk.Label(
            status_frame, 
            text="状态: 未运行",
            font=('Microsoft YaHei UI', 10)
        )
        self.status_label.pack(side=tk.LEFT)
        
        # 按钮区域
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(0, 10))
        
        # 创建按钮，使用更现代的样式
        self.start_btn = ttk.Button(
            button_frame,
            text="开始 (F9)",
            command=self.start,
            style='Custom.TButton',
            width=15
        )
        self.start_btn.pack(side=tk.LEFT, padx=5)
        
        self.pause_btn = ttk.Button(
            button_frame,
            text="暂停 (F10)",
            command=self.pause,
            style='Custom.TButton',
            width=15
        )
        self.pause_btn.pack(side=tk.LEFT, padx=5)
        self.pause_btn["state"] = "disabled"
        
        self.stop_btn = ttk.Button(
            button_frame,
            text="停止 (F11)",
            command=self.stop,
            style='Custom.TButton',
            width=15
        )
        self.stop_btn.pack(side=tk.LEFT, padx=5)
        self.stop_btn["state"] = "disabled"
        
        # 日志区域
        log_frame = ttk.LabelFrame(main_frame, text="运行日志", padding=5)
        log_frame.pack(fill=tk.BOTH, expand=True)
        
        self.log_text = scrolledtext.ScrolledText(
            log_frame,
            height=20,
            font=('Microsoft YaHei UI', 11),
            background='#ffffff',
            wrap=tk.WORD
        )
        self.log_text.pack(fill=tk.BOTH, expand=True)
        
        # 设置日志文本只读
        self.log_text.configure(state='disabled')
        
        # 设置标签字体
        self.style.configure('TLabelframe.Label', font=('Microsoft YaHei UI', 10))
        
        # 设置时间戳标签样式
        self.log_text.tag_configure('timestamp', font=('Microsoft YaHei UI', 8))  # 设置时间戳字体为8号
    
    def add_log(self, message):
        timestamp = datetime.datetime.now().strftime('%H:%M:%S')  # 只保留时:分:秒
        formatted_message = f'[{timestamp}] {message}'  # 组合时间戳和消息
        self.log_queue.put(formatted_message)  # 将组合后的消息放入队列
    
    def update_log_display(self):
        while True:
            try:
                # 非阻塞方式获取日志
                message = self.log_queue.get_nowait()
                self.log_text.configure(state='normal')
                # 插入日志消息，使用默认字体
                self.log_text.insert(tk.END, f'{message}\n')
                self.log_text.see(tk.END)  # 滚动到最新位置
                self.log_text.configure(state='disabled')
            except queue.Empty:
                break
        # 每100ms检查一次日志队列
        self.root.after(100, self.update_log_display)
    
    def start_log_monitor(self):
        self.update_log_display()
        
    def run_dahao(self):
        # 设置日志处理器
        setup_logger(self.log_queue)  # 将日志队列传递给设置函数
        # 运行 dahao.py 的主函数
        try:
            self.add_log("开始执行任务...")
            dahao_main()  # 直接调用 dahao.py 的主函数
            self.add_log("任务执行完成。")
        except Exception as e:
            self.add_log(f"执行出错: {e}")
        finally:
            self.update_buttons_stopped()  # 更新按钮状态
    
    def start(self):
        if not self.running and self.start_btn["state"] != "disabled":
            self.running = True
            self.paused = False
            self.thread = threading.Thread(target=self.run_dahao)
            self.thread.start()  # 启动线程运行 dahao_main
            
            self.start_btn["state"] = "disabled"
            self.pause_btn["state"] = "normal"
            self.stop_btn["state"] = "normal"
            self.status_label["text"] = "状态: 运行中"
            self.add_log("程序已启动")
    
    def pause(self):
        if self.running:
            self.paused = not self.paused  # 切换暂停状态
            if self.paused:
                self.pause_btn["text"] = "继续 (F10)"
                self.status_label["text"] = "状态: 已暂停"
                self.add_log("程序已暂停")
            else:
                self.pause_btn["text"] = "暂停 (F10)"
                self.status_label["text"] = "状态: 运行中"
                self.add_log("程序已继续")
    
    def stop(self):
        if self.running:
            stop_event.set()  # 设置停止事件
            self.running = False
            self.paused = False
            self.add_log("程序已请求停止")
            self.update_buttons_stopped()
    
    def update_buttons_stopped(self):
        self.start_btn["state"] = "normal"
        self.pause_btn["state"] = "disabled"
        self.stop_btn["state"] = "disabled"
        self.pause_btn["text"] = "暂停 (F10)"
        self.status_label["text"] = "状态: 已停止"
    
    def run(self):
        # 将窗口置顶
        self.root.attributes('-topmost', True)
        self.root.mainloop()

if __name__ == "__main__":
    app = DahaoController()
    app.run() 