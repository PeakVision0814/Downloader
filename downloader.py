import requests
import time
import os

class Downloader:
    def __init__(self):
        self.is_paused = False

    def download_file(self, url, save_path, progress_callback=None):
        """下载文件并允许断点续传"""
        try:
            # 如果文件已部分下载，获取当前文件大小
            downloaded_size = 0
            if os.path.exists(save_path):
                downloaded_size = os.path.getsize(save_path)

            # 获取文件的总大小
            headers = {"Range": f"bytes={downloaded_size}-"}
            response = requests.get(url, stream=True, headers=headers)
            response.raise_for_status()
            total_size = int(response.headers.get("Content-Range", "0").split("/")[-1])

            chunk_size = 1024
            last_report_time = time.time()
            speed = 0

            # 打开文件（追加模式）
            with open(save_path, "ab") as file:
                for chunk in response.iter_content(chunk_size=chunk_size):
                    if self.is_paused:
                        return "下载已暂停"
                    
                    if chunk:
                        file.write(chunk)
                        downloaded_size += len(chunk)
                    
                    # 每 1 秒刷新一次速度
                    current_time = time.time()
                    if current_time - last_report_time >= 1:
                        # 计算速度（KB/s 或 MB/s）
                        speed = downloaded_size / (current_time - last_report_time) / 1024
                        last_report_time = current_time
                        downloaded_size = 0

                        # 调整单位（如果速度超过 1 MB/s）
                        if speed >= 1024:
                            speed_text = f"{speed / 1024:.2f} MB/s"
                        else:
                            speed_text = f"{speed:.2f} KB/s"

                        # 更新进度和速度
                        if progress_callback:
                            progress = (file.tell() / total_size) * 100
                            progress_callback(progress, speed_text)
            
            return f"下载完成：{save_path}"
        
        except requests.exceptions.RequestException as e:
            raise Exception(f"下载失败: {e}")
    
    def pause_download(self):
        """暂停下载"""
        self.is_paused = True