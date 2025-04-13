import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

class FileSplitterCombiner:
    def __init__(self, master):
        self.master = master
        self.master.title("文件拆分与组合工具")
        self.master.geometry("500x400")  # 设置窗口大小

        # 拆分文件部分
        self.split_frame = ttk.LabelFrame(master, text="拆分文件", padding=(10, 10))
        self.split_frame.pack(padx=10, pady=10, fill="both", expand=True)

        self.split_file_path = tk.StringVar()
        ttk.Label(self.split_frame, text="选择要拆分的文件:").pack(anchor=tk.W)
        ttk.Entry(self.split_frame, textvariable=self.split_file_path, width=50).pack(anchor=tk.W)
        ttk.Button(self.split_frame, text="浏览", command=self.browse_split_file).pack(anchor=tk.W, pady=(5, 0))
        ttk.Button(self.split_frame, text="拆分文件", command=self.split_file).pack(anchor=tk.W, pady=(5, 0))

        # 进度条
        self.progress = ttk.Progressbar(self.split_frame, orient="horizontal", mode="determinate")
        self.progress.pack(fill=tk.X, pady=(10, 0))

        # 组合文件部分
        self.combine_frame = ttk.LabelFrame(master, text="组合文件", padding=(10, 10))
        self.combine_frame.pack(padx=10, pady=10, fill="both", expand=True)

        self.combine_file_paths = tk.StringVar()
        ttk.Label(self.combine_frame, text="输入要组合的文件路径（用逗号分隔）:").pack(anchor=tk.W)
        ttk.Entry(self.combine_frame, textvariable=self.combine_file_paths, width=50).pack(anchor=tk.W)
        ttk.Button(self.combine_frame, text="组合文件", command=self.combine_files).pack(anchor=tk.W, pady=(5, 0))

        # 退出按钮
        ttk.Button(master, text="退出", command=master.quit).pack(pady=(10, 0))

    def browse_split_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.split_file_path.set(file_path)

    def split_file(self):
        file_path = self.split_file_path.get()
        if not file_path or not os.path.isfile(file_path):
            messagebox.showerror("错误", "请选择有效的文件。")
            return
        
        chunk_size = 99 * 1024 * 1024  # 99MB
        file_number = 0
        total_size = os.path.getsize(file_path)
        self.progress['maximum'] = total_size  # 设置进度条最大值

        try:
            with open(file_path, 'rb') as f:
                while True:
                    chunk = f.read(chunk_size)
                    if not chunk:
                        break
                    part_file_name = f"{file_path}.part{file_number}.png"  # 修改后缀为 .png
                    with open(part_file_name, 'wb') as chunk_file:
                        chunk_file.write(chunk)
                    file_number += 1
                    self.progress['value'] += len(chunk)  # 更新进度条
                    self.master.update_idletasks()  # 刷新界面
            messagebox.showinfo("成功", f"文件已拆分为 {file_number} 个部分。")
        except Exception as e:
            messagebox.showerror("错误", f"拆分文件时出错: {e}")
        finally:
            self.progress['value'] = 0  # 重置进度条

    def combine_files(self):
        input_files = self.combine_file_paths.get().split(',')
        input_files = [file.strip() for file in input_files if file.strip()]
        if not input_files:
            messagebox.showerror("错误", "请输入有效的文件路径。")
            return
        
        output_file = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if not output_file:
            return
        
        try:
            with open(output_file, 'wb') as f:
                for input_file in input_files:
                    with open(input_file, 'rb') as chunk_file:
                        f.write(chunk_file.read())
            messagebox.showinfo("成功", "文件已成功组合。")
        except Exception as e:
            messagebox.showerror("错误", f"组合文件时出错: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = FileSplitterCombiner(root)
    root.mainloop()