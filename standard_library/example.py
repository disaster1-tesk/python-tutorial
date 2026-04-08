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

import contextlib

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

# ============================================================
# 11. functools 进阶示例
# ============================================================
print("\n=== 11. functools 进阶 ===")

import functools
import time as time_mod

# --- lru_cache 缓存 ---
@functools.lru_cache(maxsize=128)
def fibonacci(n):
    """递归计算斐波那契数（带缓存，避免重复计算）"""
    if n < 2:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)

print(f"fibonacci(35) = {fibonacci(35)}")
print(f"缓存信息: {fibonacci.cache_info()}")

# --- partial 偏函数 ---
def log(level, message):
    ts = time_mod.strftime("%H:%M:%S")
    print(f"  [{ts}] [{level}] {message}")

info_log = functools.partial(log, "INFO")
error_log = functools.partial(log, "ERROR")
info_log("系统启动")
error_log("连接超时")

# --- wraps 保留元信息 ---
def timer_decorator(func):
    """计时装饰器（使用 wraps 保留原函数信息）"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time_mod.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time_mod.perf_counter() - start
        print(f"  {func.__name__} 执行耗时: {elapsed:.4f}s")
        return result
    return wrapper

@timer_decorator
def slow_function():
    """这是一个慢函数的文档字符串"""
    time_mod.sleep(0.05)
    return "done"

result = slow_function()
print(f"  函数名保留: {slow_function.__name__}")
print(f"  文档保留: {slow_function.__doc__}")
print(f"  返回值: {result}")

# --- singledispatch 泛型函数 ---
@functools.singledispatch
def process_data(data):
    print(f"  默认处理: {data}")

@process_data.register(int)
def _(data):
    print(f"  处理整数: {data} x 2 = {data * 2}")

@process_data.register(list)
def _(data):
    print(f"  处理列表: 长度={len(data)}, 内容={data}")

@process_data.register(str)
def _(data):
    print(f"  处理字符串: '{data}' (长度={len(data)})")

print("singledispatch 示例:")
process_data(42)
process_data([1, 2, 3])
process_data("hello")
process_data(3.14)


# ============================================================
# 12. itertools 进阶示例
# ============================================================
print("\n=== 12. itertools 进阶 ===")

# --- chain：合并多个可迭代对象 ---
headers = ["姓名", "年龄", "城市"]
row1 = ["张三", 28, "北京"]
row2 = ["李四", 32, "上海"]
all_data = list(itertools.chain(headers, row1, row2))
print(f"chain 合并: {all_data}")

# --- product：笛卡尔积 ---
sizes = ["S", "M", "L"]
colors = ["红", "蓝"]
variants = list(itertools.product(colors, sizes))
print(f"product 笛卡尔积: {variants} (共{len(variants)}种)")

# --- permutations vs combinations ---
team = ["A", "B", "C"]
print(f"permutations(2): {list(itertools.permutations(team, 2))}")
print(f"combinations(2): {list(itertools.combinations(team, 2))}")
print(f"combinations_with_replacement(2): {list(itertools.combinations_with_replacement(team, 2))}")

# --- groupby：分组（必须先排序！）---
data = [("水果", "苹果"), ("蔬菜", "白菜"), ("水果", "香蕉"),
        ("肉类", "牛肉"), ("蔬菜", "萝卜"), ("水果", "橙子")]
data.sort(key=lambda x: x[0])
print("groupby 分组:")
for category, items in itertools.groupby(data, key=lambda x: x[0]):
    print(f"  {category}: {[item[1] for item in items]}")

# --- accumulate：累积计算 ---
sales = [100, 200, 150, 300, 250]
cumsum = list(itertools.accumulate(sales))
print(f"accumulate 累加: {cumsum}")

# --- islice：惰性切片 ---
def fake_lines():
    for i in range(1, 1000000):
        yield f"第{i}行数据"

first_3 = list(itertools.islice(fake_lines(), 3))
print(f"islice 前3行: {first_3}")

# --- starmap ---
points = [(1, 2), (3, 4), (5, 6)]
distances = list(itertools.starmap(lambda x, y: (x**2 + y**2)**0.5, points))
print(f"starmap 计算距离: {distances}")


# ============================================================
# 13. subprocess 进阶示例
# ============================================================
print("\n=== 13. subprocess 进阶 ===")

# --- run：基本用法 ---
result = subprocess.run(
    [sys.executable, "--version"],
    capture_output=True,
    text=True,
)
print(f"Python 版本: {result.stdout.strip()}")

# --- check=True：命令失败时抛出异常 ---
try:
    result = subprocess.run(
        [sys.executable, "-c", "print('Hello from subprocess!')"],
        capture_output=True, text=True, check=True,
    )
    print(f"子进程输出: {result.stdout.strip()}")
except subprocess.CalledProcessError as e:
    print(f"命令失败: {e}")

# --- timeout：超时控制 ---
try:
    subprocess.run(
        [sys.executable, "-c", "import time; time.sleep(10)"],
        timeout=2,
        capture_output=True, text=True,
    )
except subprocess.TimeoutExpired:
    print("命令执行超时（已设2秒限制）!")

# --- Popen：实时交互 ---
process = subprocess.Popen(
    [sys.executable, "-c", "import sys; print(sys.stdin.read().upper())"],
    stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
)
stdout, stderr = process.communicate(input="hello world\n")
print(f"Popen 管道输出: {stdout.strip()}")


# ============================================================
# 14. pathlib 进阶示例
# ============================================================
print("\n=== 14. pathlib 进阶 ===")

# --- glob / rglob ---
current = Path(".")
py_files = list(current.rglob("*.py"))
print(f"当前目录 Python 文件数: {len(py_files)}")

md_files = list(current.glob("**/*.md"))
print(f"当前目录 Markdown 文件数: {len(md_files)}")

# --- 文件信息 ---
if py_files:
    sample = py_files[0]
    stat = sample.stat()
    print(f"示例文件: {sample.name}")
    print(f"  大小: {stat.st_size} 字节")
    print(f"  扩展名: {sample.suffix}")
    print(f"  父目录: {sample.parent.name}")

# --- 按扩展名统计 ---
from collections import Counter as Counter2
extensions = Counter2(
    f.suffix for f in current.rglob("*")
    if f.is_file() and f.suffix
)
print(f"文件类型分布 (Top 5): {dict(extensions.most_common(5))}")

# --- pathlib vs os.path 对比 ---
print("\npathlib vs os.path:")
print(f"  拼接路径: Path('a') / 'b' / 'c' = {Path('a') / 'b' / 'c'}")
print(f"  获取扩展名: Path('test.py').suffix = '{Path('test.py').suffix}'")
print(f"  获取文件名: Path('/a/b/test.py').name = '{Path('/a/b/test.py').name}'")
print(f"  获取父目录: Path('/a/b/test.py').parent = '{Path('/a/b/test.py').parent}'")


# ============================================================
# 15. contextlib 进阶示例
# ============================================================
print("\n=== 15. contextlib 进阶 ===")

# --- @contextmanager：计时器 ---
@contextlib.contextmanager
def timer(name):
    """计时上下文管理器"""
    start = time_mod.perf_counter()
    print(f"  [{name}] 开始...")
    try:
        yield
    finally:
        elapsed = time_mod.perf_counter() - start
        print(f"  [{name}] 完成，耗时: {elapsed:.4f}s")

with timer("数据处理"):
    time_mod.sleep(0.1)
    total = sum(range(1000000))

# --- suppress：抑制异常 ---
print("\nsuppress 示例:")
with contextlib.suppress(FileNotFoundError):
    open("nonexistent_file.txt", "r")
print("  FileNotFoundError 被抑制，程序继续执行")

# --- ExitStack：动态管理多个上下文 ---
print("\nExitStack 示例:")
with contextlib.ExitStack() as stack:
    files = []
    for i in range(3):
        f = stack.enter_context(open(f"temp_{i}.txt", "w", encoding="utf-8"))
        f.write(f"文件{i}的内容\n")
        files.append(f)
        print(f"  创建 temp_{i}.txt")
    print("  所有文件已打开，with块结束后自动关闭")

# 清理临时文件
import os
for i in range(3):
    try:
        os.remove(f"temp_{i}.txt")
        print(f"  已删除 temp_{i}.txt")
    except FileNotFoundError:
        pass

# --- redirect_stdout：捕获输出 ---
print("\nredirect_stdout 示例:")
import io

f = io.StringIO()
with contextlib.redirect_stdout(f):
    print("这行输出被重定向了")
    print("这行也是")
captured = f.getvalue()
print(f"  捕获到 {len(captured.splitlines())} 行输出")
print(f"  内容: {captured.strip()}")

print("\n✅ 所有标准库示例运行完毕！")