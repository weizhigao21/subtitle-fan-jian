import opencc


# 测试SRT文件转换
def test_srt_convert():
    converter = opencc.OpenCC("t2s")

    # 读取测试文件
    with open("test.srt", "r", encoding="utf-8") as f:
        lines = f.readlines()

    converted_lines = []
    for line in lines:
        # 跳过序号行和时间戳行
        if line.strip().isdigit() or "-->" in line:
            converted_lines.append(line)
        else:
            # 转换文本行
            if line.strip():
                converted_line = converter.convert(line)
                converted_lines.append(converted_line)
            else:
                converted_lines.append(line)

    # 写入输出文件
    with open("test_converted.srt", "w", encoding="utf-8") as f:
        f.writelines(converted_lines)

    print("转换完成，输出文件: test_converted.srt")

    # 显示转换结果
    with open("test_converted.srt", "r", encoding="utf-8") as f:
        content = f.read()
    print("转换后的内容:")
    print(content)


if __name__ == "__main__":
    test_srt_convert()
