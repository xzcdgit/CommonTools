import socket
import csv
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog

def check_port(ip, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)  # 设置超时时间为1秒
    try:
        sock.connect((ip, port))
    except socket.error:
        return False
    return True

def load_csv():
    file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if not file_path:
        return

    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            name = row['名称']
            ip = row['ip']
            port = int(row['端口'])
            remark = row['备注']
            is_open = check_port(ip, port)
            status = "开放" if is_open else "关闭"
            tree.insert("", "end", values=(name, ip, port, status, remark))
            root.update_idletasks()  # 更新界面

def clear_results():
    for item in tree.get_children():
        tree.delete(item)

# 创建主窗口
root = tk.Tk()
root.title("端口检测工具")

# 创建表格
tree = ttk.Treeview(root, columns=("名称", "IP", "端口", "测试结果", "备注"), show="headings")
tree.heading("名称", text="名称")
tree.heading("IP", text="IP")
tree.heading("端口", text="端口")
tree.heading("测试结果", text="测试结果")
tree.heading("备注", text="备注")
tree.pack(fill=tk.BOTH, expand=True)

# 创建按钮框架
button_frame = tk.Frame(root)
button_frame.pack(pady=10)

# 创建加载CSV按钮
load_button = tk.Button(button_frame, text="加载CSV文件", command=load_csv)
load_button.pack(side=tk.LEFT, padx=5)

# 创建清空结果按钮
clear_button = tk.Button(button_frame, text="清空结果", command=clear_results)
clear_button.pack(side=tk.LEFT, padx=5)

# 运行主循环
root.mainloop()
