import threading
import os
from tkinter import Tk, Label, Button, ttk, StringVar, Entry, filedialog, messagebox
from downloader import Downloader

class DownloaderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("软件下载器")
        self.root.geometry("550x300")
        self.root.resizable(False, False)  # 禁止窗口宽度和高度的调整

        # 下载选项
        self.options = {
            "请选择需下载的软件": None,
            "HiBit Uninstaller 3.2.50": "https://www.hibitsoft.ir/HiBitUninstaller/HiBitUninstaller-setup-3.2.50.exe",
            "VSCode (Windows 64位)": "https://update.code.visualstudio.com/latest/win32-x64/stable",
            "Python 3.12.8 (Windows 64位)": "https://www.python.org/ftp/python/3.12.8/python-3.12.8-amd64.exe",
            "Bandizip": "https://www.bandisoft.com/bandizip/dl.php?web",
            "微信": "https://dldir1v6.qq.com/weixin/Windows/WeChatSetup.exe",
            "Todesk 4.7.6.2": "https://dl.todesk.com/irrigation/ToDesk_4.7.6.2.exe",
            "网易邮箱大师 5": "https://res.126.net/dl/client/pcmail/dashi/mail5.exe?action=banner_win_dl&device_id=e54264ff840a8ca99555b2a2249068a8_v1&os_version=10&uuid=31ac795b-27db-43fa-9ac4-c11f034ca5c1&device=desktop&os=Windows&product=mailwin&resolution=2560x1600"
        }

        # 设置窗口图标
        icon_path = os.path.join("icon", "download_icon.ico")
        if os.path.exists(icon_path):
            self.root.iconbitmap(icon_path)  # 使用 .ico 文件
        else:
            print("图标文件未找到！请检查路径。")


        self.download_url = StringVar()
        self.download_url.set("请选择需下载的软件")  # 默认选项
        self.custom_link = StringVar()  # 自定义下载链接
        self.download_path = StringVar()  # 保存下载路径
        self.download_path.set("选择保存路径...")  # 默认显示提示

        # 初始化 Downloader
        self.downloader = Downloader()

        # 下载状态
        self.is_paused = False  # 标记是否为暂停状态

        # 界面元素
        row = 0  # 初始行数

        # 软件选择行
        Label(root, text="选择要下载的软件：").grid(row=row, column=0, sticky="w", padx=20, pady=5)
        self.option_menu = ttk.Combobox(root, values=list(self.options.keys()), textvariable=self.download_url, state="readonly")
        self.option_menu.grid(row=row, column=1, sticky="ew", padx=20, pady=5)
        self.option_menu.bind("<<ComboboxSelected>>", self.update_download_link)
        row += 1

        # 下载链接行
        Label(root, text="下载链接：").grid(row=row, column=0, sticky="w", padx=20, pady=5)
        self.link_entry = Entry(root, textvariable=self.custom_link, width=50)
        self.link_entry.grid(row=row, column=1, sticky="ew", padx=20, pady=5)
        row += 1

        # 保存路径行
        Label(root, text="下载保存路径：").grid(row=row, column=0, sticky="w", padx=20, pady=5)
        path_frame = ttk.Frame(root)
        path_frame.grid(row=row, column=1, sticky="ew", padx=20, pady=5)

        self.path_entry = Entry(path_frame, textvariable=self.download_path, state="readonly", width=40)
        self.path_entry.pack(side="left", fill="x", expand=True, padx=0)
        self.browse_button = Button(path_frame, text="浏览", command=self.browse_path)
        self.browse_button.pack(side="right")
        row += 1

        # 进度条
        self.progress = ttk.Progressbar(root, orient="horizontal", length=400, mode="determinate")
        self.progress.grid(row=row, column=0, columnspan=2, sticky="ew", padx=20, pady=10)
        row += 1

        # 状态信息
        self.status_label = Label(root, text="", fg="blue")
        self.status_label.grid(row=row, column=0, columnspan=2, sticky="w", padx=20, pady=5)
        row += 1

        self.speed_label = Label(root, text="下载速度: 0 KB/s", fg="green")  # 显示下载速度
        self.speed_label.grid(row=row, column=0, columnspan=2, sticky="w", padx=20, pady=5)
        row += 1

        # 操作按钮
        self.download_button = Button(root, text="开始下载", command=self.toggle_download)
        self.download_button.grid(row=row, column=0, sticky="w", padx=20, pady=10)

        self.pause_button = Button(root, text="暂停下载", command=self.pause_download, state="disabled")
        self.pause_button.grid(row=row, column=1, sticky="e", padx=20, pady=10)

        # 下载控制
        self.thread = None
        self.current_save_path = None  # 当前保存路径

    def browse_path(self):
        """打开文件夹选择对话框"""
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            self.download_path.set(folder_selected)

    def update_download_link(self, event):
        """更新下载链接"""
        selected_software = self.download_url.get()
        default_link = self.options.get(selected_software, "")
        self.custom_link.set(default_link)  # 将默认链接显示到输入框中

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

        # 使用用户输入的下载链接
        download_link = self.custom_link.get()
        if not download_link or not download_link.startswith("http"):
            messagebox.showerror("错误", "请输入有效的下载链接！")
            return

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
        elif selected_software == "微信":
            self.current_save_path = os.path.join(save_dir, "WeChatSetup.exe")
        elif selected_software == "HiBit Uninstaller 3.2.50":
            self.current_save_path = os.path.join(save_dir, "HiBitUninstaller-setup-3.2.50.exe")
        elif selected_software == "Todesk 4.7.6.2":
            self.current_save_path = os.path.join(save_dir, "ToDesk_setup_4.7.6.2.exe")
        elif selected_software == "网易邮箱大师 5":
            self.current_save_path = os.path.join(save_dir, "mail5.exe")
        else:
            self.current_save_path = os.path.join(save_dir, download_link.split("/")[-1])  # 使用链接中的文件名

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
            target=self.download_file_with_progress, args=(download_link, self.current_save_path)
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
        if self.current_save_path:
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
