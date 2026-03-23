# 字幕繁简转换工具

版本: 1.0.0

## 功能介绍

这是一个用于转换字幕文件繁简体的桌面工具，支持以下功能：

- 支持 SRT、ASS、SSA 等字幕格式
- 繁体转简体 / 简体转繁体
- 批量转换
- 拖放文件支持
- 自动检测文件编码

## 使用方法

### 方式一：直接运行 Python 脚本

1. 安装依赖：
```bash
pip install -r requirements.txt
```

2. 运行程序：
```bash
python subtitle_converter.py
```

### 方式二：使用打包的 exe 文件

直接运行 `dist/SubtitleConverter.exe`

## 打包说明

### 打包要求

- Python 3.6+
- PyInstaller

### 打包步骤

1. 安装 PyInstaller（如未安装）：
```bash
pip install pyinstaller
```

2. 运行打包脚本：
```bash
build.bat
```

3. 打包完成后，exe 文件位于 `dist/SubtitleConverter.exe`

### 版本号管理

- 版本号定义在 `subtitle_converter.py` 文件中的 `__version__` 变量
- 版本信息定义在 `version_info.txt` 文件中
- 修改版本号时需要同时更新这两个文件

## 文件说明

- `subtitle_converter.py` - 主程序
- `version_info.txt` - Windows exe 版本信息
- `build.bat` - 打包脚本
- `requirements.txt` - Python 依赖列表

## 依赖库

- `tkinter` - GUI 界面
- `tkinterdnd2` - 拖放支持
- `opencc-python-reimplemented` - 繁简转换

## 许可证

Copyright (C) 2026 weizhigao21
