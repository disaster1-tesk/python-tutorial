# Python标准库使用示例

print("=== 1. os模块示例 ===")
import os

# 获取当前工作目录
current_dir = os.getcwd()
print(f"当前工作目录: {current_dir}")

# 列出当前目录内容
files = os.listdir(".")
print(f"当前目录文件: {files[:5]}...")  # 只显示前5个

# 路径操作
path_example = os.path.join("folder", "subfolder", "file.txt")
print(f"连接路径: {path_example}")

file_exists = os.path.exists(__file__)
print(f"当前文件存在: {file_exists}")

print("\n=== 2. sys模块示例 ===")
import sys

print(f"Python版本: {sys.version}")
print(f"模块搜索路径: {sys.path[0]}")

# 命令行参数示例(在实际运行中会显示真实参数)
print(f"命令行参数: {sys.argv}")

print("\n=== 3. datetime模块示例 ===")
from datetime import datetime, date, timedelta

# 当前日期时间
now = datetime.now()
print(f"当前时间: {now}")

# 格式化日期时间
formatted = now.strftime("%Y-%m-%d %H:%M:%S")
print(f"格式化时间: {formatted}")

# 日期计算
today = date.today()
future_date = today + timedelta(days=10)
print(f"今天: {today}")
print(f"10天后: {future_date}")

print("\n=== 4. math模块示例 ===")
import math

print(f"π的值: {math.pi}")
print(f"e的值: {math.e}")
print(f"sqrt(16): {math.sqrt(16)}")
print(f"sin(π/2): {math.sin(math.pi/2)}")
print(f"log(e): {math.log(math.e)}")

print("\n=== 5. random模块示例 ===")
import random

# 设置随机种子以获得可重现的结果
random.seed(42)

print(f"0-1随机数: {random.random()}")
print(f"1-10随机整数: {random.randint(1, 10)}")

colors = ["红", "绿", "蓝", "黄", "紫"]
print(f"随机选择颜色: {random.choice(colors)}")

# 随机打乱列表
numbers = [1, 2, 3, 4, 5]
random.shuffle(numbers)
print(f"随机打乱后: {numbers}")

print("\n=== 6. json模块示例 ===")
import json

# Python对象转JSON
data = {
    "name": "张三",
    "age": 30,
    "skills": ["Python", "Java", "C++"]
}

json_string = json.dumps(data, ensure_ascii=False, indent=2)
print("JSON字符串:")
print(json_string)

# JSON转Python对象
parsed_data = json.loads(json_string)
print(f"解析后的姓名: {parsed_data['name']}")

# 写入JSON文件
try:
    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print("JSON文件写入成功")
    
    # 读取JSON文件
    with open("data.json", "r", encoding="utf-8") as f:
        loaded_data = json.load(f)
    print(f"从文件读取的姓名: {loaded_data['name']}")
    
    # 清理文件
    os.remove("data.json")
except Exception as e:
    print(f"JSON文件操作失败: {e}")

print("\n=== 7. re模块示例 ===")
import re

text = "我的电话号码是13812345678，邮箱是example@email.com"

# 查找电话号码
phone_pattern = r'1[3-9]\d{9}'
phones = re.findall(phone_pattern, text)
print(f"找到的电话号码: {phones}")

# 查找邮箱
email_pattern = r'\w+@\w+\.\w+'
emails = re.findall(email_pattern, text)
print(f"找到的邮箱: {emails}")

# 替换
masked_text = re.sub(phone_pattern, "***********", text)
print(f"掩码后的文本: {masked_text}")

print("\n=== 8. collections模块示例 ===")
from collections import Counter, defaultdict, namedtuple

# Counter计数器
words = ["apple", "banana", "apple", "cherry", "banana", "apple"]
word_count = Counter(words)
print(f"单词计数: {word_count}")
print(f"最常见的单词: {word_count.most_common(1)}")

# defaultdict默认字典
dd = defaultdict(list)
dd["fruits"].append("apple")
dd["fruits"].append("banana")
print(f"defaultdict示例: {dd}")

# namedtuple命名元组
Point = namedtuple("Point", ["x", "y"])
p = Point(1, 2)
print(f"命名元组: x={p.x}, y={p.y}")

print("\n=== 9. pathlib模块示例 ===")
from pathlib import Path

# 创建Path对象
current_path = Path(".")
file_path = Path(__file__)

print(f"当前目录: {current_path.absolute()}")
print(f"当前文件: {file_path.name}")
print(f"文件后缀: {file_path.suffix}")

# 创建和写入文件
try:
    example_path = Path("example.txt")
    example_path.write_text("这是pathlib示例文件", encoding="utf-8")
    print("pathlib文件写入成功")
    
    content = example_path.read_text(encoding="utf-8")
    print(f"读取内容: {content}")
    
    # 清理文件
    example_path.unlink()
except Exception as e:
    print(f"pathlib文件操作失败: {e}")

print("\n=== 10. itertools模块示例 ===")
import itertools

# 无限计数器
counter = itertools.count(start=10, step=2)
print("计数器前5个值:", [next(counter) for _ in range(5)])

# 组合
colors = ["红", "绿", "蓝"]
combinations = list(itertools.combinations(colors, 2))
print(f"颜色组合: {combinations}")

# 链接迭代器
list1 = [1, 2, 3]
list2 = [4, 5, 6]
chained = list(itertools.chain(list1, list2))
print(f"链接列表: {chained}")

print("\n=== 11. functools模块示例 ===")
from functools import reduce, partial

# reduce函数
numbers = [1, 2, 3, 4, 5]
sum_result = reduce(lambda x, y: x + y, numbers)
print(f"使用reduce计算和: {sum_result}")

# partial函数
def multiply(x, y):
    return x * y

# 创建一个固定第一个参数的函数
double = partial(multiply, 2)
print(f"使用partial创建的double函数: {double(5)}")