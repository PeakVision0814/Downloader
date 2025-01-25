# 下载器软件

由于每次安装新系统需要下载各种必需软件，因此想了个办法编写了一个程序用于简易的Windows 64位软件安装包下载，以节省每次新系统装机时间和步骤。

这是一个基于 `Python` 和 `Tkinter` 的图形化软件下载工具，支持多种常用软件的断点续传下载。用户可以选择需要下载的软件，设置保存路径，并实时查看下载进度和速度。

## 功能特点

- **支持多种常用软件下载**：
  - VSCode (Windows 64位)
  - Python 3.12.8 (Windows 64位)
  - Bandizip
  - （可轻松扩展更多软件）
  
- **断点续传**：
  - 支持下载暂停后继续下载，不会重新开始。
  
- **实时进度显示**：
  - 进度条显示下载完成百分比。
  - 显示当前下载速度，支持 KB/s 和 MB/s 动态切换。

- **用户友好的界面**：
  - 提供下拉菜单选择下载的软件。
  - 设置保存路径，避免覆盖已有文件。
  - 下载完成后显示提示标语，明确下载状态。

## 使用指南

### 1. 环境要求

- Python 版本：3.8+
- 依赖库：
  - `requests`
  - `tkinter`（标准库，无需单独安装）

### 2. 克隆

将代码克隆到自己的仓库中

```bash
https://github.com/PeakVision0814/Downloader.git
```

### 3. 安装依赖

在命令行中运行以下命令安装所需依赖：

```bash
pip install requests
```

### 4. 运行程序

下载源码后，运行以下命令启动程序：

```bash
python downloader_ui.py
```

## 界面说明

1. **软件选择**：
   - 在下拉菜单中选择要下载的软件。如果未选择有效选项，系统会弹出警告。
   
2. **保存路径设置**：
   - 点击“浏览”按钮选择文件保存路径。

3. **下载控制**：
   - 点击“开始下载”启动下载。
   - 在下载过程中，可以点击“暂停下载”暂停任务，随后可通过“继续下载”从暂停处恢复。

4. **下载状态**：
   - 显示下载进度条和实时速度。
   - 下载完成后弹出提示框显示下载结果。

## 软件扩展

### 新增下载软件

1. **添加下载选项**：
   在 `downloader_ui.py` 中的 `self.options` 字典中添加新软件的名称和下载链接，例如：
   
   ```python
   self.options = {
       "7-Zip": "https://www.7-zip.org/a/7z2301-x64.exe",
   }
   ```
   
2. **设置保存文件名**：
   在 `start_download` 方法中，为新软件指定文件保存名称，例如：
   
   ```python
   elif selected_software == "7-Zip":
       self.current_save_path = os.path.join(save_dir, "7z2301-x64.exe")
   ```

## 注意事项

1. **断点续传**：
   - 如果文件已部分下载，工具会自动从上次暂停的地方继续下载。

2. **网络要求**：
   - 请确保网络连接正常，避免下载中断。

3. **使用权限**：
   - 本工具仅限用于公开可下载的软件，请勿用于未经授权的资源下载。
   - 本工具仅提供学习使用，请勿进行商用。

## 贡献

欢迎对本项目提出改进建议或提交代码贡献，如果您对本工具有任何建议，欢迎您通过以下方式联系作者：

- 邮箱：perished_hgp@qq.com
- GitHub：[@Peakvision0814](https://github.com/PeakVision0814)

## 许可协议

本项目基于 [MIT License](LICENSE) 许可协议开源发布。