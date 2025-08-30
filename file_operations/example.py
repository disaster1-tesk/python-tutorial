# Python文件操作示例

# 基本文件写入操作
try:
    # 使用with语句自动处理文件关闭
    with open("example.txt", "w", encoding="utf-8") as file:
        file.write("这是第一行内容\n")
        file.write("这是第二行内容\n")
        file.writelines(["这是第三行内容\n", "这是第四行内容\n"])
    print("文件写入成功")
except Exception as e:
    print(f"文件写入失败: {e}")

# 基本文件读取操作
try:
    # 读取整个文件内容
    with open("example.txt", "r", encoding="utf-8") as file:
        content = file.read()
        print("文件全部内容:")
        print(content)
except FileNotFoundError:
    print("文件未找到")
except Exception as e:
    print(f"文件读取失败: {e}")

# 逐行读取文件
try:
    with open("example.txt", "r", encoding="utf-8") as file:
        print("逐行读取文件:")
        for line_number, line in enumerate(file, 1):
            print(f"第{line_number}行: {line.strip()}")
except FileNotFoundError:
    print("文件未找到")

# 使用readline()逐行读取
try:
    with open("example.txt", "r", encoding="utf-8") as file:
        print("使用readline()逐行读取:")
        line_number = 1
        line = file.readline()
        while line:
            print(f"第{line_number}行: {line.strip()}")
            line = file.readline()
            line_number += 1
except FileNotFoundError:
    print("文件未找到")

# 文件定位操作
try:
    with open("example.txt", "r", encoding="utf-8") as file:
        print("文件定位操作:")
        print(f"当前文件指针位置: {file.tell()}")
        
        content = file.read(5)  # 读取前5个字符
        print(f"读取内容: '{content}'")
        print(f"当前文件指针位置: {file.tell()}")
        
        file.seek(0)  # 回到文件开头
        print(f"重置后文件指针位置: {file.tell()}")
        
        first_line = file.readline()
        print(f"第一行: {first_line.strip()}")
except FileNotFoundError:
    print("文件未找到")

# 追加模式写入
try:
    with open("example.txt", "a", encoding="utf-8") as file:
        file.write("这是追加的一行内容\n")
    print("追加写入成功")
    
    # 验证追加内容
    with open("example.txt", "r", encoding="utf-8") as file:
        print("追加后的文件内容:")
        print(file.read())
except Exception as e:
    print(f"追加写入失败: {e}")

# 处理不存在的文件
try:
    with open("nonexistent.txt", "r") as file:
        content = file.read()
except FileNotFoundError:
    print("尝试读取不存在的文件时捕获到FileNotFoundError")

# 二进制文件操作示例
try:
    # 写入二进制文件
    with open("binary_example.bin", "wb") as file:
        data = b"Binary data example \x00\x01\x02\x03"
        file.write(data)
    print("二进制文件写入成功")
    
    # 读取二进制文件
    with open("binary_example.bin", "rb") as file:
        binary_data = file.read()
        print(f"二进制文件内容: {binary_data}")
except Exception as e:
    print(f"二进制文件操作失败: {e}")

# 使用pathlib模块进行文件操作（Python 3.4+）
try:
    from pathlib import Path
    
    # 创建Path对象
    file_path = Path("pathlib_example.txt")
    
    # 写入文件
    file_path.write_text("这是使用pathlib写入的内容", encoding="utf-8")
    print("使用pathlib写入文件成功")
    
    # 读取文件
    content = file_path.read_text(encoding="utf-8")
    print(f"使用pathlib读取内容: {content}")
    
except ImportError:
    print("pathlib模块不可用（Python版本低于3.4）")
except Exception as e:
    print(f"使用pathlib操作文件失败: {e}")