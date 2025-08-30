# Python文件操作知识点

## 1. 文件操作基础

文件操作是程序与外部存储交互的重要方式，用于持久化数据存储。

### 文件操作的重要性
- **数据持久化**：程序关闭后数据不会丢失
- **配置管理**：存储和读取配置信息
- **日志记录**：记录程序运行状态和错误信息
- **数据交换**：与其他程序或系统交换数据

### 文件操作的基本流程
```python
# 1. 打开文件
# 2. 读取或写入数据
# 3. 关闭文件

# 基本示例
try:
    # 打开文件
    file = open("example.txt", "w", encoding="utf-8")
    
    # 写入数据
    file.write("Hello, World!")
    
    # 关闭文件
    file.close()
except Exception as e:
    print(f"文件操作错误: {e}")
```

## 2. open()函数

Python通过内置的`open()`函数来打开文件。

### 基本语法
```python
open(file, mode='r', buffering=-1, encoding=None, errors=None, newline=None, closefd=True, opener=None)
```

### 参数详解
- **file**: 文件路径（相对路径或绝对路径）
- **mode**: 打开模式
- **encoding**: 文件编码（处理文本文件时重要）
- **errors**: 编码错误处理方式

### 打开模式
```python
# 只读模式（默认）
file = open("example.txt", "r")

# 写入模式（覆盖原内容）
file = open("example.txt", "w")

# 追加模式（在文件末尾添加）
file = open("example.txt", "a")

# 读写模式
file = open("example.txt", "r+")  # 读写，文件必须存在
file = open("example.txt", "w+")  # 读写，覆盖原内容
file = open("example.txt", "a+")  # 读写，追加模式

# 二进制模式
file = open("image.jpg", "rb")   # 二进制只读
file = open("data.bin", "wb")    # 二进制写入
file = open("output.bin", "ab")  # 二进制追加
```

### 使用示例
```python
# 指定编码打开文件
with open("chinese.txt", "r", encoding="utf-8") as file:
    content = file.read()

# 处理编码错误
with open("mixed.txt", "r", encoding="utf-8", errors="ignore") as file:
    content = file.read()

# 使用绝对路径
import os
file_path = os.path.join("/home/user", "documents", "data.txt")
with open(file_path, "r") as file:
    content = file.read()
```

## 3. 文件读取方法

Python提供了多种方法来读取文件内容。

### read()方法
```python
# 读取整个文件内容
with open("example.txt", "r", encoding="utf-8") as file:
    content = file.read()
    print(content)

# 读取指定字符数
with open("example.txt", "r", encoding="utf-8") as file:
    chunk = file.read(10)  # 读取前10个字符
    print(chunk)
```

### readline()方法
```python
# 读取一行内容
with open("example.txt", "r", encoding="utf-8") as file:
    line = file.readline()
    print(line)

# 逐行读取文件
with open("example.txt", "r", encoding="utf-8") as file:
    for line in file:
        print(line.strip())  # strip()去除换行符
```

### readlines()方法
```python
# 读取所有行，返回列表
with open("example.txt", "r", encoding="utf-8") as file:
    lines = file.readlines()
    for line in lines:
        print(line.strip())

# 使用列表推导式处理行
with open("numbers.txt", "r", encoding="utf-8") as file:
    numbers = [int(line.strip()) for line in file if line.strip()]
    print(f"数字列表: {numbers}")
```

### 实际应用示例
```python
def read_config_file(filename):
    """读取配置文件"""
    config = {}
    try:
        with open(filename, "r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()
                if line and not line.startswith("#"):  # 忽略空行和注释
                    key, value = line.split("=", 1)
                    config[key.strip()] = value.strip()
    except FileNotFoundError:
        print(f"配置文件 {filename} 不存在")
    except Exception as e:
        print(f"读取配置文件错误: {e}")
    return config

# 配置文件示例 (config.txt):
# # 这是注释
# host=localhost
# port=8080
# debug=true

config = read_config_file("config.txt")
print(config)  # {'host': 'localhost', 'port': '8080', 'debug': 'true'}
```

## 4. 文件写入方法

Python提供了多种方法来写入文件内容。

### write()方法
```python
# 写入字符串
with open("output.txt", "w", encoding="utf-8") as file:
    file.write("Hello, World!\n")
    file.write("这是第二行\n")

# 写入数字（需要转换为字符串）
with open("numbers.txt", "w", encoding="utf-8") as file:
    for i in range(5):
        file.write(f"{i}\n")
```

### writelines()方法
```python
# 写入字符串列表
lines = ["第一行\n", "第二行\n", "第三行\n"]
with open("output.txt", "w", encoding="utf-8") as file:
    file.writelines(lines)

# 使用列表推导式
data = ["apple", "banana", "orange"]
with open("fruits.txt", "w", encoding="utf-8") as file:
    file.writelines([f"{item}\n" for item in data])
```

### 追加模式
```python
# 追加内容到文件末尾
with open("log.txt", "a", encoding="utf-8") as file:
    file.write(f"[{datetime.now()}] 新的日志条目\n")

# 条件性写入
def log_message(message, log_file="app.log"):
    """记录日志消息"""
    import datetime
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] {message}\n"
    
    with open(log_file, "a", encoding="utf-8") as file:
        file.write(log_entry)

log_message("应用程序启动")
log_message("用户登录成功")
```

## 5. with语句（上下文管理器）

推荐使用with语句进行文件操作，确保文件正确关闭。

### 基本用法
```python
# 使用with语句自动管理文件
with open("example.txt", "r", encoding="utf-8") as file:
    content = file.read()
    print(content)
# 文件会自动关闭，即使发生异常

# 不使用with语句（不推荐）
file = open("example.txt", "r", encoding="utf-8")
try:
    content = file.read()
    print(content)
finally:
    file.close()  # 必须手动关闭
```

### 多文件操作
```python
# 同时处理多个文件
with open("input.txt", "r", encoding="utf-8") as infile, \
     open("output.txt", "w", encoding="utf-8") as outfile:
    for line in infile:
        processed_line = line.upper()
        outfile.write(processed_line)
```

### 自定义上下文管理器
```python
from contextlib import contextmanager

@contextmanager
def managed_file(filename, mode="r"):
    """自定义文件管理器"""
    print(f"打开文件: {filename}")
    file = open(filename, mode, encoding="utf-8")
    try:
        yield file
    finally:
        print(f"关闭文件: {filename}")
        file.close()

# 使用自定义上下文管理器
with managed_file("example.txt", "w") as file:
    file.write("Hello from custom context manager!")
```

## 6. 文件定位

文件定位允许在文件中移动指针位置。

### tell()方法
```python
# 获取当前文件指针位置
with open("example.txt", "r", encoding="utf-8") as file:
    print(f"初始位置: {file.tell()}")  # 0
    
    content = file.read(10)
    print(f"读取后位置: {file.tell()}")  # 10
```

### seek()方法
```python
# 移动文件指针位置
with open("example.txt", "r", encoding="utf-8") as file:
    # 移动到文件开头
    file.seek(0)
    print(file.read(5))  # 读取前5个字符
    
    # 移动到第10个字符
    file.seek(10)
    print(file.read(5))  # 从第10个字符开始读取5个字符
    
    # 移动到文件末尾前10个字符
    file.seek(-10, 2)  # 2表示从文件末尾开始
    print(file.read())  # 读取最后10个字符
```

### 实际应用：随机访问文件
```python
import struct

def write_records(filename, records):
    """写入固定长度记录"""
    with open(filename, "wb") as file:
        for record in records:
            # 假设每条记录是两个整数
            data = struct.pack("ii", record[0], record[1])
            file.write(data)

def read_record(filename, record_number):
    """读取指定记录"""
    record_size = 8  # 两个整数，每个4字节
    with open(filename, "rb") as file:
        file.seek(record_number * record_size)
        data = file.read(record_size)
        if len(data) == record_size:
            return struct.unpack("ii", data)
        return None

# 使用示例
records = [(1, 100), (2, 200), (3, 300)]
write_records("data.bin", records)

record = read_record("data.bin", 1)  # 读取第二条记录
print(record)  # (2, 200)
```

## 7. 文件和目录操作

使用os和os.path模块进行文件和目录操作。

### 基本文件操作
```python
import os

# 检查文件是否存在
if os.path.exists("example.txt"):
    print("文件存在")

# 检查是否为文件
if os.path.isfile("example.txt"):
    print("这是一个文件")

# 检查是否为目录
if os.path.isdir("documents"):
    print("这是一个目录")

# 获取文件大小
size = os.path.getsize("example.txt")
print(f"文件大小: {size} 字节")

# 删除文件
if os.path.exists("temp.txt"):
    os.remove("temp.txt")
    print("文件已删除")
```

### 目录操作
```python
import os

# 创建目录
os.mkdir("new_directory")  # 创建单层目录
os.makedirs("parent/child/grandchild", exist_ok=True)  # 创建多层目录

# 列出目录内容
files = os.listdir(".")
print("当前目录文件:", files)

# 遍历目录树
for root, dirs, files in os.walk("."):
    print(f"目录: {root}")
    for file in files:
        print(f"  文件: {file}")

# 改变当前工作目录
original_dir = os.getcwd()
os.chdir("new_directory")
print("当前目录:", os.getcwd())
os.chdir(original_dir)  # 恢复原目录
```

### 路径操作
```python
import os.path

# 路径拼接
file_path = os.path.join("documents", "data", "file.txt")
print(file_path)  # documents/data/file.txt (Unix) 或 documents\data\file.txt (Windows)

# 路径分解
directory, filename = os.path.split("/home/user/documents/file.txt")
print(f"目录: {directory}, 文件名: {filename}")

name, extension = os.path.splitext("document.pdf")
print(f"文件名: {name}, 扩展名: {extension}")

# 获取绝对路径
absolute_path = os.path.abspath("relative/path/file.txt")
print(f"绝对路径: {absolute_path}")

# 规范化路径
normalized_path = os.path.normpath("a/b/../c/./d")
print(f"规范化路径: {normalized_path}")
```

## 8. pathlib模块

pathlib模块提供了面向对象的文件系统路径操作。

### 基本用法
```python
from pathlib import Path

# 创建Path对象
current_path = Path(".")
file_path = Path("documents/file.txt")
absolute_path = Path("/home/user/documents/file.txt")

# 路径操作
print(f"当前目录: {current_path.absolute()}")
print(f"文件名: {file_path.name}")
print(f"文件 stem: {file_path.stem}")
print(f"扩展名: {file_path.suffix}")
print(f"父目录: {file_path.parent}")

# 创建目录
new_dir = Path("new_directory")
new_dir.mkdir(exist_ok=True)

# 创建多层目录
nested_dir = Path("parent/child/grandchild")
nested_dir.mkdir(parents=True, exist_ok=True)

# 列出目录内容
for item in current_path.iterdir():
    if item.is_file():
        print(f"文件: {item}")
    elif item.is_dir():
        print(f"目录: {item}")
```

### 文件读写操作
```python
from pathlib import Path

# 文本文件读写
file_path = Path("example.txt")

# 写入文本
file_path.write_text("Hello, World!\n这是第二行", encoding="utf-8")

# 读取文本
content = file_path.read_text(encoding="utf-8")
print(content)

# 二进制文件读写
binary_file = Path("data.bin")
data = b"Binary data example"
binary_file.write_bytes(data)
read_data = binary_file.read_bytes()
print(read_data)
```

### 路径匹配
```python
from pathlib import Path

# 查找文件
current_dir = Path(".")

# 查找所有.txt文件
txt_files = list(current_dir.glob("*.txt"))
print("TXT文件:", txt_files)

# 递归查找所有.py文件
py_files = list(current_dir.rglob("*.py"))
print("Python文件:", py_files)

# 使用更复杂的模式
config_files = list(current_dir.glob("**/config.*"))
print("配置文件:", config_files)
```

## 9. 文件处理最佳实践

### 使用with语句处理文件
```python
# 好的做法
with open("data.txt", "r", encoding="utf-8") as file:
    data = file.read()

# 避免的做法
file = open("data.txt", "r", encoding="utf-8")
data = file.read()
file.close()  # 可能忘记关闭
```

### 明确指定文件编码
```python
# 好的做法
with open("chinese.txt", "r", encoding="utf-8") as file:
    content = file.read()

# 避免的做法
with open("chinese.txt", "r") as file:  # 可能出现编码问题
    content = file.read()
```

### 处理大文件
```python
def process_large_file(filename):
    """逐行处理大文件"""
    with open(filename, "r", encoding="utf-8") as file:
        for line_number, line in enumerate(file, 1):
            # 处理每一行
            processed_line = line.strip().upper()
            if processed_line:
                print(f"第{line_number}行: {processed_line}")

def process_large_file_with_buffer(filename, buffer_size=8192):
    """使用缓冲区处理大文件"""
    with open(filename, "r", encoding="utf-8") as file:
        while True:
            chunk = file.read(buffer_size)
            if not chunk:
                break
            # 处理数据块
            print(f"处理 {len(chunk)} 字符")
```

### 错误处理
```python
def safe_file_operation(filename):
    """安全的文件操作"""
    try:
        with open(filename, "r", encoding="utf-8") as file:
            content = file.read()
        return content
    except FileNotFoundError:
        print(f"文件 {filename} 不存在")
        return None
    except PermissionError:
        print(f"没有权限读取文件 {filename}")
        return None
    except UnicodeDecodeError:
        print(f"文件 {filename} 编码错误")
        return None
    except Exception as e:
        print(f"读取文件时发生未知错误: {e}")
        return None
```

## 10. 实际应用场景

### 配置文件处理
```python
import json
from pathlib import Path

class ConfigManager:
    """配置管理器"""
    
    def __init__(self, config_file="config.json"):
        self.config_file = Path(config_file)
        self.config = self.load_config()
    
    def load_config(self):
        """加载配置"""
        if self.config_file.exists():
            try:
                return json.loads(self.config_file.read_text(encoding="utf-8"))
            except json.JSONDecodeError:
                print("配置文件格式错误，使用默认配置")
                return {}
        return {}
    
    def save_config(self):
        """保存配置"""
        self.config_file.write_text(
            json.dumps(self.config, indent=2, ensure_ascii=False),
            encoding="utf-8"
        )
    
    def get(self, key, default=None):
        """获取配置值"""
        return self.config.get(key, default)
    
    def set(self, key, value):
        """设置配置值"""
        self.config[key] = value
        self.save_config()

# 使用示例
config = ConfigManager()
config.set("database_url", "sqlite:///app.db")
config.set("debug", True)
print(config.get("database_url"))  # sqlite:///app.db
```

### 日志文件处理
```python
import datetime
from pathlib import Path

class Logger:
    """简单日志记录器"""
    
    def __init__(self, log_file="app.log"):
        self.log_file = Path(log_file)
    
    def log(self, level, message):
        """记录日志"""
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {level}: {message}\n"
        
        with open(self.log_file, "a", encoding="utf-8") as file:
            file.write(log_entry)
    
    def info(self, message):
        """信息日志"""
        self.log("INFO", message)
    
    def error(self, message):
        """错误日志"""
        self.log("ERROR", message)
    
    def warning(self, message):
        """警告日志"""
        self.log("WARNING", message)

# 使用示例
logger = Logger()
logger.info("应用程序启动")
logger.warning("这是一个警告")
logger.error("发生错误")
```

### CSV文件处理
```python
import csv
from pathlib import Path

def read_csv(filename):
    """读取CSV文件"""
    data = []
    try:
        with open(filename, "r", encoding="utf-8", newline="") as file:
            reader = csv.DictReader(file)
            for row in reader:
                data.append(row)
    except FileNotFoundError:
        print(f"文件 {filename} 不存在")
    except Exception as e:
        print(f"读取CSV文件错误: {e}")
    return data

def write_csv(filename, data, fieldnames):
    """写入CSV文件"""
    try:
        with open(filename, "w", encoding="utf-8", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)
    except Exception as e:
        print(f"写入CSV文件错误: {e}")

# 使用示例
data = [
    {"name": "张三", "age": "25", "city": "北京"},
    {"name": "李四", "age": "30", "city": "上海"},
    {"name": "王五", "age": "35", "city": "广州"}
]

write_csv("people.csv", data, ["name", "age", "city"])
read_data = read_csv("people.csv")
for row in read_data:
    print(row)
```