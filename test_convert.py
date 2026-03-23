import opencc

# 测试繁体转简体
converter = opencc.OpenCC("t2s")
test_text = "這是一個測試"
result = converter.convert(test_text)
print(f"繁体转简体: {test_text} -> {result}")

# 测试简体转繁体
converter = opencc.OpenCC("s2t")
test_text = "这是一个测试"
result = converter.convert(test_text)
print(f"简体转繁体: {test_text} -> {result}")
