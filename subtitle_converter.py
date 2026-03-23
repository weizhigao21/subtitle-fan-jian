import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

__version__ = "1.0.0"

try:
    from tkinterdnd2 import DND_FILES, TkinterDnD

    DND_AVAILABLE = True
except ImportError:
    DND_AVAILABLE = False
    print("警告: tkinterdnd2 未安装，拖放功能将不可用。请运行: pip install tkinterdnd2")

try:
    import opencc

    OPENCC_AVAILABLE = True
except ImportError:
    OPENCC_AVAILABLE = False
    print("错误: opencc 未安装。请运行: pip install opencc-python-reimplemented")


class SubtitleConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title(f"字幕繁简转换工具 v{__version__}")
        self.root.geometry("600x450")

        # 初始化转换器
        self.converter = None

        # 文件列表
        self.file_list = []

        self.setup_ui()

    def setup_ui(self):
        # 主框架
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky="nsew")

        # 配置网格权重
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(1, weight=1)

        # 标题
        title_label = ttk.Label(
            main_frame, text="字幕繁简转换工具", font=("Arial", 16, "bold")
        )
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 10))

        # 文件列表框
        list_frame = ttk.LabelFrame(
            main_frame, text="文件列表 (拖放文件到此处)", padding="5"
        )
        list_frame.grid(row=1, column=0, columnspan=3, sticky="nsew", pady=(0, 10))
        list_frame.columnconfigure(0, weight=1)
        list_frame.rowconfigure(0, weight=1)

        self.file_listbox = tk.Listbox(list_frame, selectmode=tk.EXTENDED)
        self.file_listbox.grid(row=0, column=0, sticky="nsew")

        # 添加滚动条
        scrollbar = ttk.Scrollbar(
            list_frame, orient=tk.VERTICAL, command=self.file_listbox.yview
        )
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.file_listbox.configure(yscrollcommand=scrollbar.set)

        # 启用拖放
        if DND_AVAILABLE:
            self.file_listbox.drop_target_register(DND_FILES)
            self.file_listbox.dnd_bind("<<Drop>>", self.on_drop)

        # 按钮框架
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=2, column=0, columnspan=3, pady=(0, 10))

        # 添加文件按钮
        add_btn = ttk.Button(button_frame, text="添加文件", command=self.add_files)
        add_btn.grid(row=0, column=0, padx=(0, 5))

        # 移除选中按钮
        remove_btn = ttk.Button(
            button_frame, text="移除选中", command=self.remove_selected
        )
        remove_btn.grid(row=0, column=1, padx=(0, 5))

        # 清空列表按钮
        clear_btn = ttk.Button(button_frame, text="清空列表", command=self.clear_list)
        clear_btn.grid(row=0, column=2, padx=(0, 5))

        # 转换选项框架
        option_frame = ttk.LabelFrame(main_frame, text="转换选项", padding="5")
        option_frame.grid(row=3, column=0, columnspan=3, sticky="ew", pady=(0, 10))

        # 转换方向
        self.convert_direction = tk.StringVar(value="t2s")
        ttk.Radiobutton(
            option_frame,
            text="繁体转简体",
            variable=self.convert_direction,
            value="t2s",
        ).grid(row=0, column=0, padx=(0, 10))
        ttk.Radiobutton(
            option_frame,
            text="简体转繁体",
            variable=self.convert_direction,
            value="s2t",
        ).grid(row=0, column=1)

        # 输出目录选项
        self.output_option = tk.StringVar(value="same")
        ttk.Radiobutton(
            option_frame, text="保存到原目录", variable=self.output_option, value="same"
        ).grid(row=1, column=0, padx=(0, 10), pady=(5, 0))
        ttk.Radiobutton(
            option_frame,
            text="选择输出目录",
            variable=self.output_option,
            value="choose",
        ).grid(row=1, column=1, pady=(5, 0))

        # 转换按钮
        convert_btn = ttk.Button(
            main_frame, text="开始转换", command=self.start_convert
        )
        convert_btn.grid(row=4, column=0, columnspan=3, pady=(0, 10))

        # 状态栏
        self.status_var = tk.StringVar(value="就绪")
        status_bar = ttk.Label(
            main_frame, textvariable=self.status_var, relief=tk.SUNKEN
        )
        status_bar.grid(row=5, column=0, columnspan=3, sticky="ew")

        # 绑定双击事件打开文件
        self.file_listbox.bind("<Double-1>", self.open_file_location)

    def detect_encoding(self, file_path):
        """检测文件编码"""
        encodings = ["utf-8", "gbk", "gb2312", "big5", "utf-16", "utf-32"]
        for encoding in encodings:
            try:
                with open(file_path, "r", encoding=encoding) as f:
                    f.read()
                return encoding
            except (UnicodeDecodeError, UnicodeError):
                continue
        return "utf-8"  # 默认返回UTF-8

    def on_drop(self, event):
        """拖放文件处理"""
        files = self.root.tk.splitlist(event.data)
        for file_path in files:
            if file_path not in self.file_list:
                self.file_list.append(file_path)
                self.file_listbox.insert(tk.END, file_path)
        self.update_status(f"已添加 {len(files)} 个文件")

    def add_files(self):
        """通过文件对话框添加文件"""
        filetypes = [("字幕文件", "*.srt *.ass *.ssa *.sub *.txt"), ("所有文件", "*.*")]
        files = filedialog.askopenfilenames(title="选择字幕文件", filetypes=filetypes)
        for file_path in files:
            if file_path not in self.file_list:
                self.file_list.append(file_path)
                self.file_listbox.insert(tk.END, file_path)
        if files:
            self.update_status(f"已添加 {len(files)} 个文件")

    def remove_selected(self):
        """移除选中的文件"""
        selected_indices = self.file_listbox.curselection()
        if not selected_indices:
            return

        # 从后往前删除，避免索引变化
        for index in reversed(selected_indices):
            self.file_listbox.delete(index)
            del self.file_list[index]

        self.update_status(f"已移除 {len(selected_indices)} 个文件")

    def clear_list(self):
        """清空文件列表"""
        self.file_listbox.delete(0, tk.END)
        self.file_list.clear()
        self.update_status("文件列表已清空")

    def open_file_location(self, event):
        """双击打开文件所在目录"""
        selection = self.file_listbox.curselection()
        if selection:
            index = selection[0]
            file_path = self.file_list[index]
            if os.path.exists(file_path):
                os.startfile(os.path.dirname(file_path))

    def start_convert(self):
        """开始转换"""
        if not OPENCC_AVAILABLE:
            messagebox.showerror(
                "错误", "opencc 未安装，请运行: pip install opencc-python-reimplemented"
            )
            return

        if not self.file_list:
            messagebox.showwarning("警告", "请先添加字幕文件")
            return

        # 获取转换方向
        direction = self.convert_direction.get()

        # 初始化转换器
        try:
            self.converter = opencc.OpenCC(direction)
        except Exception as e:
            messagebox.showerror("错误", f"初始化转换器失败: {e}")
            return

        # 确定输出目录
        output_dir = None
        if self.output_option.get() == "choose":
            output_dir = filedialog.askdirectory(title="选择输出目录")
            if not output_dir:
                return

        # 转换每个文件
        total_files = len(self.file_list)
        success_count = 0
        error_files = []

        for i, input_file in enumerate(self.file_list):
            self.update_status(
                f"正在转换 ({i + 1}/{total_files}): {os.path.basename(input_file)}"
            )
            self.root.update()

            try:
                # 确定输出文件路径
                if output_dir:
                    output_file = os.path.join(output_dir, os.path.basename(input_file))
                else:
                    # 在原目录创建"简体"或"繁体"文件夹
                    input_dir = os.path.dirname(input_file)
                    folder_name = "简体" if direction == "t2s" else "繁体"
                    output_folder = os.path.join(input_dir, folder_name)
                    os.makedirs(output_folder, exist_ok=True)
                    output_file = os.path.join(
                        output_folder, os.path.basename(input_file)
                    )

                # 转换文件
                self.convert_subtitle_file(input_file, output_file)
                success_count += 1

            except Exception as e:
                error_files.append((os.path.basename(input_file), str(e)))

        # 显示结果
        result_msg = f"转换完成！成功: {success_count}/{total_files}"
        if error_files:
            result_msg += "\n\n失败文件:\n"
            for filename, error in error_files:
                result_msg += f"• {filename}: {error}\n"

        messagebox.showinfo("转换结果", result_msg)
        self.update_status("转换完成")

    def convert_subtitle_file(self, input_file, output_file):
        """转换单个字幕文件"""
        # 检测编码
        encoding = self.detect_encoding(input_file)

        # 根据文件扩展名选择不同的处理方式
        ext = os.path.splitext(input_file)[1].lower()

        if ext == ".srt":
            self.convert_srt_file(input_file, output_file, encoding)
        elif ext in [".ass", ".ssa"]:
            self.convert_ass_file(input_file, output_file, encoding)
        else:
            # 默认当作文本文件处理
            self.convert_text_file(input_file, output_file, encoding)

    def convert_srt_file(self, input_file, output_file, encoding="utf-8"):
        """转换SRT格式字幕"""
        with open(input_file, "r", encoding=encoding) as f:
            lines = f.readlines()

        converted_lines = []
        for line in lines:
            # 跳过序号行和时间戳行
            if line.strip().isdigit() or "-->" in line:
                converted_lines.append(line)
            else:
                # 转换文本行
                if line.strip():
                    converted_line = self.converter.convert(line)
                    converted_lines.append(converted_line)
                else:
                    converted_lines.append(line)

        with open(output_file, "w", encoding="utf-8") as f:
            f.writelines(converted_lines)

    def convert_ass_file(self, input_file, output_file, encoding="utf-8"):
        """转换ASS/SSA格式字幕"""
        with open(input_file, "r", encoding=encoding) as f:
            lines = f.readlines()

        converted_lines = []
        in_events_section = False

        for line in lines:
            # 检查是否进入Events部分
            if line.strip().startswith("[Events]"):
                in_events_section = True
                converted_lines.append(line)
                continue

            # 检查是否离开Events部分（遇到新的section）
            if line.strip().startswith("[") and not line.strip().startswith("[Events]"):
                in_events_section = False
                converted_lines.append(line)
                continue

            # 只在Events部分转换文本
            if in_events_section:
                # 对于Dialogue行，只转换文本部分
                if line.startswith("Dialogue:") or line.startswith("Comment:"):
                    parts = line.split(",", 9)  # ASS格式有10个字段
                    if len(parts) >= 10:
                        # 转换最后一个字段（文本）
                        parts[9] = self.converter.convert(parts[9])
                        converted_line = ",".join(parts)
                        converted_lines.append(converted_line)
                    else:
                        converted_lines.append(line)
                else:
                    converted_lines.append(line)
            else:
                converted_lines.append(line)

        with open(output_file, "w", encoding="utf-8") as f:
            f.writelines(converted_lines)

    def convert_text_file(self, input_file, output_file, encoding="utf-8"):
        """转换普通文本文件"""
        with open(input_file, "r", encoding=encoding) as f:
            content = f.read()

        converted_content = self.converter.convert(content)

        with open(output_file, "w", encoding="utf-8") as f:
            f.write(converted_content)

    def update_status(self, message):
        """更新状态栏"""
        self.status_var.set(message)
        self.root.update()


def main():
    # 使用TkinterDnD代替普通Tk
    if DND_AVAILABLE:
        root = TkinterDnD.Tk()
    else:
        root = tk.Tk()
    app = SubtitleConverterApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
