import threading
import os
from tkinter import Tk, Label, Button, ttk, StringVar, Entry, filedialog, messagebox
from downloader import Downloader

class DownloaderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("软件下载器")
        self.root.geometry("500x350")

        # 下载选项
        self.options = {
            "请选择需下载的软件": None,  # 新增提示选项
            "VSCode (Windows 64位)": "https://update.code.visualstudio.com/latest/win32-x64/stable",
            "Python 3.12.8 (Windows 64位)": "https://www.python.org/ftp/python/3.12.8/python-3.12.8-amd64.exe",
            "Bandizip": "https://www.bandisoft.com/bandizip/dl.php?web",
            "微信": "https://dldir1v6.qq.com/weixin/Windows/WeChatSetup.exe", # 修正为微信下载地址
        }

        self.download_url = StringVar()
        self.download_url.set("请选择需下载的软件")  # 默认选项
        self.download_path = StringVar()  # 保存下载路径
        self.download_path.set("选择保存路径...")  # 默认显示提示

        # 初始化 Downloader
        self.downloader = Downloader()

        # 下载状态
        self.is_paused = False  # 标记是否为暂停状态

        # 界面元素
        Label(root, text="选择要下载的软件：").pack(pady=5)
        self.option_menu = ttk.Combobox(root, values=list(self.options.keys()), textvariable=self.download_url, state="readonly")
        self.option_menu.pack(pady=5)

        Label(root, text="下载保存路径：").pack(pady=5)
        path_frame = ttk.Frame(root)
        path_frame.pack(pady=5, fill="x", padx=10)
        
        self.path_entry = Entry(path_frame, textvariable=self.download_path, state="readonly", width=40)
        self.path_entry.pack(side="left", fill="x", expand=True, padx=5)
        self.browse_button = Button(path_frame, text="浏览", command=self.browse_path)
        self.browse_button.pack(side="right")

        self.progress = ttk.Progressbar(root, orient="horizontal", length=400, mode="determinate")
        self.progress.pack(pady=10)

        self.status_label = Label(root, text="", fg="blue")
        self.status_label.pack(pady=5)

        self.speed_label = Label(root, text="下载速度: 0 KB/s", fg="green")  # 显示下载速度
        self.speed_label.pack(pady=5)

        self.download_button = Button(root, text="开始下载", command=self.toggle_download)
        self.download_button.pack(side="left", padx=20)

        self.pause_button = Button(root, text="暂停下载", command=self.pause_download, state="disabled")
        self.pause_button.pack(side="right", padx=20)

        # 下载控制
        self.thread = None
        self.current_url = None  # 当前下载的 URL
        self.current_save_path = None  # 当前保存路径

    def browse_path(self):
        """打开文件夹选择对话框"""
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            self.download_path.set(folder_selected)

    def toggle_download(self):
        """切换下载状态（开始或继续下载）"""
        if not self.is_paused:  # 开始下载
            self.start_download()
        else:  # 继续下载
            self.resume_download()

    def start_download(self):
        """开始下载"""
        selected_software = self.download_url.get()

        # 检查用户是否选择了有效的下载选项
        if selected_software == "请选择需下载的软件":
            messagebox.showwarning("警告", "请选择需下载的软件")
            return

        self.current_url = self.options[selected_software]
        save_dir = self.download_path.get()

        if save_dir == "选择保存路径..." or not save_dir:
            messagebox.showwarning("警告", "请先选择保存路径！")
            return

        # 针对不同软件设置保存文件名
        if selected_software == "VSCode (Windows 64位)":
            self.current_save_path = os.path.join(save_dir, "VSCodeSetup.exe")
        elif selected_software == "Python 3.12.8 (Windows 64位)":
            self.current_save_path = os.path.join(save_dir, "python-3.12.8-amd64.exe")
        elif selected_software == "Bandizip":
            self.current_save_path = os.path.join(save_dir, "BANDIZIP-SETUP-STD-X64.exe")
        elif selected_software == "微信 (Windows 64位)":
            self.current_save_path = os.path.join(save_dir, "WeChatSetup.exe")

        else:
            self.current_save_path = os.path.join(save_dir, self.current_url.split("/")[-1])  # 默认使用原始文件名

        if self.thread and self.thread.is_alive():
            messagebox.showinfo("提示", "下载正在进行中！")
            return

        self.downloader.is_paused = False
        self.is_paused = False  # 状态标记为非暂停
        self.download_button.config(text="下载中", state="disabled")
        self.pause_button.config(state="normal")
        self.status_label.config(text="正在下载中...")
        self.speed_label.config(text="下载速度: 0 KB/s")  # 重置速度显示

        # 创建新线程执行下载
        self.thread = threading.Thread(
            target=self.download_file_with_progress, args=(self.current_url, self.current_save_path)
        )
        self.thread.start()

    def pause_download(self):
        """暂停下载"""
        self.downloader.pause_download()
        self.is_paused = True  # 状态标记为暂停
        self.download_button.config(text="继续下载", state="normal")
        self.pause_button.config(state="disabled")
        self.status_label.config(text="下载已暂停")
        self.speed_label.config(text="下载速度: 0 KB/s")  # 暂停时速度归零

    def resume_download(self):
        """继续下载"""
        if self.current_url and self.current_save_path:
            self.start_download()  # 重新调用开始下载

    def download_file_with_progress(self, url, save_path):
        """带进度回调的下载方法"""
        def update_progress(value, speed):
            self.progress["value"] = value
            self.speed_label.config(text=f"下载速度: {speed}")  # 直接显示动态单位速度
            self.root.update_idletasks()

        try:
            message = self.downloader.download_file(url, save_path, update_progress)
            self.status_label.config(text=message, fg="green" if "完成" in message else "orange")

            # 修改弹窗提示，使用当前选择的软件名称
            selected_software = self.download_url.get()
            messagebox.showinfo("提示", f"{selected_software} 下载完成！")

        except Exception as e:
            self.status_label.config(text="下载失败", fg="red")
            messagebox.showerror("错误", f"下载失败：{e}")
        finally:
            self.download_button.config(text="开始下载", state="normal")
            self.pause_button.config(state="disabled")
            self.speed_label.config(text="下载速度: 0 KB/s")  # 下载结束时速度归零
            self.is_paused = False

if __name__ == "__main__":
    root = Tk()
    app = DownloaderApp(root)
    root.mainloop()