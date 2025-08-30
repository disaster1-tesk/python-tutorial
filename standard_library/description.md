# Python标准库使用知识点

## 1. os模块 - 操作系统接口

os模块提供了与操作系统交互的功能。

### 基本文件和目录操作
```python
import os

# 获取当前工作目录
current_dir = os.getcwd()
print(f"当前目录: {current_dir}")

# 改变当前工作目录
# os.chdir("/path/to/directory")

# 列出目录内容
files = os.listdir(".")
print(f"当前目录文件: {files}")

# 创建目录
# os.mkdir("new_directory")  # 创建单层目录
# os.makedirs("parent/child/grandchild", exist_ok=True)  # 创建多层目录

# 删除目录
# os.rmdir("empty_directory")  # 删除空目录
# os.removedirs("parent/child")  # 删除多层空目录

# 删除文件
# os.remove("file.txt")

# 重命名文件或目录
# os.rename("old_name.txt", "new_name.txt")
```

### 路径操作
```python
import os.path

# 路径拼接
file_path = os.path.join("documents", "data", "file.txt")
print(f"拼接路径: {file_path}")

# 路径分解
directory, filename = os.path.split("/home/user/documents/file.txt")
print(f"目录: {directory}, 文件名: {filename}")

name, extension = os.path.splitext("document.pdf")
print(f"文件名: {name}, 扩展名: {extension}")

# 路径检查
print(f"路径是否存在: {os.path.exists('example.txt')}")
print(f"是否为文件: {os.path.isfile('example.txt')}")
print(f"是否为目录: {os.path.isdir('documents')}")

# 获取文件信息
if os.path.exists("example.txt"):
    size = os.path.getsize("example.txt")
    print(f"文件大小: {size} 字节")
```

### 环境变量
```python
import os

# 获取环境变量
home_dir = os.environ.get("HOME", "未设置")
print(f"家目录: {home_dir}")

path_dirs = os.environ.get("PATH", "").split(":")
print(f"PATH目录: {path_dirs[:3]}...")  # 只显示前3个

# 设置环境变量
# os.environ["MY_VAR"] = "my_value"
```

## 2. sys模块 - 系统相关参数和函数

sys模块提供了与Python解释器和系统环境交互的功能。

### 程序参数和退出
```python
import sys

# 命令行参数
print(f"脚本名: {sys.argv[0]}")
print(f"参数列表: {sys.argv[1:]}")

# 程序退出
# sys.exit(0)  # 正常退出
# sys.exit(1)  # 异常退出

# 标准输入输出
# sys.stdout.write("直接写入标准输出\n")
# sys.stderr.write("错误信息\n")
```

### 系统信息
```python
import sys

# Python版本信息
print(f"Python版本: {sys.version}")
print(f"Python版本信息: {sys.version_info}")

# 平台信息
print(f"平台: {sys.platform}")

# 模块搜索路径
print("模块搜索路径:")
for i, path in enumerate(sys.path[:5]):  # 只显示前5个
    print(f"  {i+1}. {path}")
```

## 3. datetime模块 - 日期和时间处理

datetime模块提供了处理日期和时间的功能。

### 基本日期时间对象
```python
from datetime import datetime, date, time, timedelta

# 当前日期时间
now = datetime.now()
print(f"当前时间: {now}")

# 创建特定日期时间
specific_datetime = datetime(2023, 12, 25, 14, 30, 0)
print(f"特定时间: {specific_datetime}")

# 日期对象
today = date.today()
print(f"今天: {today}")

# 时间对象
current_time = time(14, 30, 0)
print(f"当前时间: {current_time}")
```

### 日期时间格式化
```python
from datetime import datetime

# 格式化日期时间
now = datetime.now()
formatted = now.strftime("%Y-%m-%d %H:%M:%S")
print(f"格式化时间: {formatted}")

# 常用格式
print(f"ISO格式: {now.isoformat()}")
print(f"日期: {now.strftime('%Y年%m月%d日')}")
print(f"时间: {now.strftime('%H时%M分%S秒')}")

# 解析日期时间字符串
date_string = "2023-12-25 14:30:00"
parsed_date = datetime.strptime(date_string, "%Y-%m-%d %H:%M:%S")
print(f"解析时间: {parsed_date}")
```

### 日期时间计算
```python
from datetime import datetime, timedelta

# 日期计算
now = datetime.now()
future = now + timedelta(days=30, hours=5, minutes=30)
past = now - timedelta(weeks=2)

print(f"现在: {now}")
print(f"30天5小时30分钟后: {future}")
print(f"2周前: {past}")

# 日期差计算
date1 = datetime(2023, 1, 1)
date2 = datetime(2023, 12, 31)
diff = date2 - date1
print(f"相差天数: {diff.days}")
```

## 4. math模块 - 数学函数

math模块提供了数学常数和函数。

### 数学常数
```python
import math

print(f"π: {math.pi}")
print(f"e: {math.e}")
print(f"τ (2π): {math.tau}")
print(f"无穷大: {math.inf}")
print(f"非数字: {math.nan}")
```

### 基本数学函数
```python
import math

# 数值函数
print(f"绝对值: {math.fabs(-5.5)}")
print(f"向上取整: {math.ceil(4.2)}")
print(f"向下取整: {math.floor(4.8)}")
print(f"四舍五入: {round(math.sqrt(2), 4)}")

# 幂和对数函数
print(f"2的3次方: {math.pow(2, 3)}")
print(f"平方根: {math.sqrt(16)}")
print(f"自然对数: {math.log(math.e)}")
print(f"以10为底的对数: {math.log10(100)}")

# 三角函数
print(f"sin(π/2): {math.sin(math.pi/2)}")
print(f"cos(0): {math.cos(0)}")
print(f"tan(π/4): {math.tan(math.pi/4)}")

# 角度转换
print(f"90度转弧度: {math.radians(90)}")
print(f"π弧度转角度: {math.degrees(math.pi)}")
```

## 5. random模块 - 随机数生成

random模块提供了生成随机数的功能。

### 基本随机数生成
```python
import random

# 随机浮点数
print(f"0-1随机数: {random.random()}")
print(f"1-10随机数: {random.uniform(1, 10)}")

# 随机整数
print(f"1-10随机整数: {random.randint(1, 10)}")
print(f"1-10随机整数(不包含10): {random.randrange(1, 10)}")

# 随机选择
colors = ["红", "绿", "蓝", "黄", "紫"]
print(f"随机颜色: {random.choice(colors)}")
print(f"随机选择3个颜色: {random.choices(colors, k=3)}")

# 随机采样(不重复)
print(f"随机采样3个颜色: {random.sample(colors, 3)}")
```

### 随机序列操作
```python
import random

# 随机打乱序列
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
random.shuffle(numbers)
print(f"打乱后: {numbers}")

# 设置随机种子
random.seed(42)
print(f"种子42的随机数: {random.random()}")

random.seed(42)  # 重新设置相同种子
print(f"相同种子的随机数: {random.random()}")
```

## 6. json模块 - JSON数据处理

json模块提供了JSON数据的编码和解码功能。

### JSON编码和解码
```python
import json

# Python对象转JSON
data = {
    "name": "张三",
    "age": 25,
    "skills": ["Python", "Java", "JavaScript"],
    "married": True,
    "children": None
}

json_string = json.dumps(data, ensure_ascii=False, indent=2)
print("JSON字符串:")
print(json_string)

# JSON转Python对象
parsed_data = json.loads(json_string)
print(f"解析后的姓名: {parsed_data['name']}")
print(f"技能列表: {parsed_data['skills']}")
```

### 文件操作
```python
import json

# 写入JSON文件
data = {"name": "李四", "age": 30, "city": "北京"}

with open("data.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

# 读取JSON文件
with open("data.json", "r", encoding="utf-8") as f:
    loaded_data = json.load(f)
    print(f"从文件读取: {loaded_data}")
```

## 7. re模块 - 正则表达式

re模块提供了正则表达式匹配功能。

### 基本匹配操作
```python
import re

text = "我的电话号码是13812345678，邮箱是example@email.com"

# 查找匹配
phone_pattern = r'1[3-9]\d{9}'
phones = re.findall(phone_pattern, text)
print(f"找到的电话号码: {phones}")

email_pattern = r'\w+@\w+\.\w+'
emails = re.findall(email_pattern, text)
print(f"找到的邮箱: {emails}")

# 搜索匹配
if re.search(phone_pattern, text):
    print("文本中包含电话号码")

# 匹配开头
if re.match(r'我的', text):
    print("文本以'我的'开头")
```

### 替换和分割
```python
import re

text = "电话:13812345678, 邮箱:example@email.com"

# 替换
masked_text = re.sub(r'1[3-9]\d{9}', '***********', text)
print(f"掩码后: {masked_text}")

# 分割
parts = re.split(r'[,，]', text)
print(f"分割结果: {parts}")

# 编译正则表达式（提高性能）
pattern = re.compile(r'\w+@\w+\.\w+')
emails = pattern.findall(text)
print(f"编译模式查找: {emails}")
```

## 8. collections模块 - 高性能容器数据类型

collections模块提供了高性能的容器数据类型。

### Counter计数器
```python
from collections import Counter

# 统计元素出现次数
words = ["apple", "banana", "apple", "cherry", "banana", "apple"]
word_count = Counter(words)
print(f"单词计数: {word_count}")

# 最常见的元素
print(f"最常见的单词: {word_count.most_common(2)}")

# 更新计数
word_count.update(["apple", "date"])
print(f"更新后: {word_count}")
```

### defaultdict默认字典
```python
from collections import defaultdict

# 默认值字典
dd = defaultdict(list)
dd["fruits"].append("apple")
dd["fruits"].append("banana")
dd["vegetables"].append("carrot")
print(f"defaultdict: {dict(dd)}")

# 使用lambda设置默认值
dd2 = defaultdict(lambda: "未知")
dd2["name"] = "张三"
print(f"姓名: {dd2['name']}")
print(f"年龄: {dd2['age']}")  # 返回"未知"
```

### namedtuple命名元组
```python
from collections import namedtuple

# 创建命名元组
Point = namedtuple("Point", ["x", "y"])
p1 = Point(1, 2)
p2 = Point(x=3, y=4)

print(f"点1: x={p1.x}, y={p1.y}")
print(f"点2: {p2}")

# 命名元组是不可变的
# p1.x = 5  # 会报错
```

### deque双端队列
```python
from collections import deque

# 创建双端队列
dq = deque([1, 2, 3])
print(f"初始队列: {dq}")

# 两端操作
dq.append(4)        # 右端添加
dq.appendleft(0)    # 左端添加
print(f"添加元素后: {dq}")

popped = dq.pop()       # 右端弹出
popleft = dq.popleft()  # 左端弹出
print(f"弹出元素: {popped}, {popleft}")
print(f"弹出后: {dq}")
```

## 9. urllib模块 - URL处理

urllib模块提供了URL处理功能。

### URL解析
```python
from urllib.parse import urlparse, urlunparse, parse_qs

# 解析URL
url = "https://www.example.com:8080/path/to/page?param1=value1&param2=value2#section"
parsed = urlparse(url)

print(f"协议: {parsed.scheme}")
print(f"域名: {parsed.netloc}")
print(f"路径: {parsed.path}")
print(f"参数: {parsed.params}")
print(f"查询: {parsed.query}")
print(f"片段: {parsed.fragment}")

# 解析查询参数
query_params = parse_qs(parsed.query)
print(f"查询参数: {query_params}")

# 构建URL
new_url = urlunparse(('https', 'newdomain.com', '/newpath', '', 'key=value', ''))
print(f"构建的URL: {new_url}")
```

### URL编码
```python
from urllib.parse import urlencode, quote, unquote

# 编码查询参数
params = {
    "name": "张三",
    "age": 25,
    "city": "北京"
}
encoded_params = urlencode(params)
print(f"编码参数: {encoded_params}")

# URL编码/解码
text = "hello world 你好"
encoded_text = quote(text)
print(f"编码文本: {encoded_text}")
decoded_text = unquote(encoded_text)
print(f"解码文本: {decoded_text}")
```

## 10. pathlib模块 - 面向对象的文件系统路径

pathlib模块提供了面向对象的文件系统路径操作。

### 基本路径操作
```python
from pathlib import Path

# 创建Path对象
current_path = Path(".")
file_path = Path("documents/file.txt")
absolute_path = Path("/home/user/documents/file.txt")

# 路径属性
print(f"当前目录: {current_path.absolute()}")
print(f"文件名: {file_path.name}")
print(f"stem: {file_path.stem}")
print(f"扩展名: {file_path.suffix}")
print(f"父目录: {file_path.parent}")

# 路径拼接
new_path = Path("documents") / "data" / "file.txt"
print(f"拼接路径: {new_path}")
```

### 文件操作
```python
from pathlib import Path

# 创建目录
# new_dir = Path("new_directory")
# new_dir.mkdir(exist_ok=True)

# # 创建多层目录
# nested_dir = Path("parent/child/grandchild")
# nested_dir.mkdir(parents=True, exist_ok=True)

# 文件读写
file_path = Path("example.txt")

# 写入文本
# file_path.write_text("Hello, World!\n这是第二行", encoding="utf-8")

# 读取文本
if file_path.exists():
    content = file_path.read_text(encoding="utf-8")
    print(f"文件内容:\n{content}")

# 二进制操作
# binary_file = Path("data.bin")
# binary_file.write_bytes(b"Binary data")
# data = binary_file.read_bytes()
```

## 11. itertools模块 - 高效的迭代器函数

itertools模块提供了高效的迭代器函数。

### 无限迭代器
```python
import itertools

# 计数器
counter = itertools.count(start=10, step=2)
print("计数器前5个值:", [next(counter) for _ in range(5)])

# 循环迭代
cycle = itertools.cycle(['A', 'B', 'C'])
print("循环前6个值:", [next(cycle) for _ in range(6)])

# 重复值
repeat = itertools.repeat('Hello', 3)
print("重复值:", list(repeat))
```

### 组合迭代器
```python
import itertools

# 链接迭代器
list1 = [1, 2, 3]
list2 = [4, 5, 6]
chained = list(itertools.chain(list1, list2))
print(f"链接列表: {chained}")

# 组合
colors = ["红", "绿", "蓝"]
combinations = list(itertools.combinations(colors, 2))
print(f"颜色组合: {combinations}")

# 排列
permutations = list(itertools.permutations(colors, 2))
print(f"颜色排列: {permutations}")

# 笛卡尔积
letters = ['A', 'B']
numbers = [1, 2]
product = list(itertools.product(letters, numbers))
print(f"笛卡尔积: {product}")
```

## 12. functools模块 - 高阶函数和可调用对象

functools模块提供了高阶函数和可调用对象的操作工具。

### 装饰器相关
```python
from functools import wraps, partial

# wraps装饰器
def my_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print("装饰器执行")
        return func(*args, **kwargs)
    return wrapper

@my_decorator
def example_function():
    """示例函数"""
    return "原函数执行"

print(example_function.__name__)  # example_function
print(example_function.__doc__)   # 示例函数

# partial偏函数
def multiply(x, y, z):
    return x * y * z

# 创建偏函数
double = partial(multiply, 2, 1)
print(f"double(5): {double(5)}")  # 10

triple = partial(multiply, z=3)
print(f"triple(2, 4): {triple(2, 4)}")  # 24
```

### reduce函数
```python
from functools import reduce

# 累积函数应用
numbers = [1, 2, 3, 4, 5]

# 求和
sum_result = reduce(lambda x, y: x + y, numbers)
print(f"求和: {sum_result}")  # 15

# 求积
product_result = reduce(lambda x, y: x * y, numbers)
print(f"求积: {product_result}")  # 120

# 找最大值
max_result = reduce(lambda x, y: x if x > y else y, numbers)
print(f"最大值: {max_result}")  # 5
```

## 13. logging模块 - 日志记录

logging模块提供了灵活的日志记录功能。

### 基本日志记录
```python
import logging

# 配置日志
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# 创建logger
logger = logging.getLogger(__name__)

# 不同级别的日志
logger.debug("这是调试信息")
logger.info("这是普通信息")
logger.warning("这是警告信息")
logger.error("这是错误信息")
logger.critical("这是严重错误信息")
```

### 文件日志记录
```python
import logging

# 配置文件日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("app.log", encoding="utf-8"),
        logging.StreamHandler()  # 同时输出到控制台
    ]
)

logger = logging.getLogger(__name__)

logger.info("应用程序启动")
logger.warning("这是一个警告")
logger.error("发生错误")
```

## 14. argparse模块 - 命令行参数解析

argparse模块提供了命令行参数解析功能。

### 基本参数解析
```python
import argparse

# 创建解析器
parser = argparse.ArgumentParser(description="这是一个示例程序")

# 添加参数
parser.add_argument("name", help="用户姓名")
parser.add_argument("-a", "--age", type=int, default=0, help="用户年龄")
parser.add_argument("-v", "--verbose", action="store_true", help="详细输出")

# 解析参数
# args = parser.parse_args()
# print(f"姓名: {args.name}")
# print(f"年龄: {args.age}")
# if args.verbose:
#     print("详细模式已启用")
```

### 复杂参数解析
```python
import argparse

parser = argparse.ArgumentParser(description="文件处理工具")

# 位置参数
parser.add_argument("input_file", help="输入文件路径")

# 可选参数
parser.add_argument("-o", "--output", help="输出文件路径")
parser.add_argument("-f", "--format", choices=["json", "csv", "xml"], default="json", help="输出格式")

# 多值参数
parser.add_argument("--tags", nargs="+", help="标签列表")

# 计数参数
parser.add_argument("-v", "--verbose", action="count", default=0, help="增加详细程度")

# args = parser.parse_args()
# print(f"输入文件: {args.input_file}")
# print(f"输出文件: {args.output}")
# print(f"格式: {args.format}")
# print(f"标签: {args.tags}")
# print(f"详细级别: {args.verbose}")
```

## 15. 实际应用场景

### 文件监控和处理
```python
import os
import time
from pathlib import Path

def monitor_directory(directory_path, interval=5):
    """监控目录变化"""
    directory = Path(directory_path)
    if not directory.exists():
        print(f"目录 {directory_path} 不存在")
        return
    
    print(f"开始监控目录: {directory_path}")
    last_files = set(directory.iterdir())
    
    try:
        while True:
            time.sleep(interval)
            current_files = set(directory.iterdir())
            
            # 检查新增文件
            new_files = current_files - last_files
            for file in new_files:
                print(f"新增文件: {file}")
            
            # 检查删除文件
            deleted_files = last_files - current_files
            for file in deleted_files:
                print(f"删除文件: {file}")
            
            last_files = current_files
    except KeyboardInterrupt:
        print("监控已停止")

# monitor_directory("./test_directory")
```

### 数据处理和分析
```python
import json
import csv
from collections import Counter
from datetime import datetime

def analyze_user_data(json_file):
    """分析用户数据"""
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # 统计用户年龄分布
        ages = [user['age'] for user in data]
        age_counter = Counter(ages)
        print("年龄分布:")
        for age, count in age_counter.most_common():
            print(f"  {age}岁: {count}人")
        
        # 统计城市分布
        cities = [user['city'] for user in data]
        city_counter = Counter(cities)
        print("\n城市分布:")
        for city, count in city_counter.most_common():
            print(f"  {city}: {count}人")
        
        # 计算平均年龄
        avg_age = sum(ages) / len(ages)
        print(f"\n平均年龄: {avg_age:.1f}岁")
        
    except Exception as e:
        print(f"分析数据时出错: {e}")

# 示例数据
sample_data = [
    {"name": "张三", "age": 25, "city": "北京"},
    {"name": "李四", "age": 30, "city": "上海"},
    {"name": "王五", "age": 25, "city": "北京"},
    {"name": "赵六", "age": 35, "city": "广州"},
]

# with open("users.json", "w", encoding="utf-8") as f:
#     json.dump(sample_data, f, ensure_ascii=False, indent=2)
# 
# analyze_user_data("users.json")
```

## 16. 最佳实践

### 正确处理路径分隔符
```python
import os
from pathlib import Path

# 好的做法：使用os.path.join或pathlib
file_path = os.path.join("documents", "data", "file.txt")
# 或者
file_path = Path("documents") / "data" / "file.txt"

# 避免的做法：硬编码路径分隔符
# file_path = "documents\\data\\file.txt"  # Windows
# file_path = "documents/data/file.txt"    # Unix
```

### 使用with语句处理资源
```python
# 好的做法：使用with语句
with open("data.txt", "r", encoding="utf-8") as file:
    content = file.read()

# 避免的做法：手动关闭文件
file = open("data.txt", "r", encoding="utf-8")
try:
    content = file.read()
finally:
    file.close()
```

### 合理使用异常处理
```python
import json

def safe_json_load(filename):
    """安全加载JSON文件"""
    try:
        with open(filename, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"文件 {filename} 不存在")
        return None
    except json.JSONDecodeError as e:
        print(f"JSON格式错误: {e}")
        return None
    except Exception as e:
        print(f"加载文件时发生未知错误: {e}")
        return None
```