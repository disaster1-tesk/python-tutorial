# Python模块和包知识点

## 1. 模块的概念

模块是一个包含Python代码的文件，通常以.py为扩展名，是组织和重用代码的基本单位。

### 模块的特点
- **代码组织**：将相关的函数、类、变量组织在一起
- **代码重用**：可以在多个程序中导入和使用
- **命名空间**：提供独立的命名空间，避免命名冲突
- **维护性**：便于代码的维护和更新

### 创建简单模块
```python
# math_utils.py - 数学工具模块
"""数学工具模块"""

PI = 3.14159

def add(a, b):
    """加法函数"""
    return a + b

def subtract(a, b):
    """减法函数"""
    return a - b

def multiply(a, b):
    """乘法函数"""
    return a * b

def divide(a, b):
    """除法函数"""
    if b == 0:
        raise ValueError("除数不能为零")
    return a / b

class Calculator:
    """计算器类"""
    def __init__(self):
        self.history = []
    
    def calculate(self, operation, a, b):
        """执行计算"""
        if operation == "add":
            result = add(a, b)
        elif operation == "subtract":
            result = subtract(a, b)
        elif operation == "multiply":
            result = multiply(a, b)
        elif operation == "divide":
            result = divide(a, b)
        else:
            raise ValueError("不支持的操作")
        
        self.history.append(f"{a} {operation} {b} = {result}")
        return result
```

## 2. 导入模块的方式

Python提供了多种导入模块的方式，每种方式有不同的使用场景。

### import语句
```python
# 导入整个模块
import math
print(math.pi)
print(math.sqrt(16))

# 使用别名导入
import numpy as np
import pandas as pd

# 导入多个模块
import os, sys, json
```

### from...import语句
```python
# 从模块中导入特定函数或类
from math import pi, sqrt
print(pi)
print(sqrt(16))

# 导入所有公共对象（不推荐）
from math import *

# 使用别名导入
from datetime import datetime as dt
now = dt.now()
print(now)
```

### 相对导入和绝对导入
```python
# 绝对导入
from mypackage.utils import helper_function
from mypackage.subpackage.module import MyClass

# 相对导入（在包内部使用）
from .utils import helper_function          # 同级目录
from ..utils import helper_function         # 上级目录
from .subpackage.module import MyClass      # 子包
```

### 条件导入
```python
# 根据条件导入不同的模块
try:
    import ujson as json  # 如果有ujson，优先使用
except ImportError:
    import json  # 否则使用标准库json

# 可选功能导入
try:
    import matplotlib.pyplot as plt
    HAS_MATPLOTLIB = True
except ImportError:
    HAS_MATPLOTLIB = False

def plot_data(data):
    if HAS_MATPLOTLIB:
        plt.plot(data)
        plt.show()
    else:
        print("matplotlib未安装，无法绘制图表")
```

## 3. 标准库模块

Python提供了丰富的标准库模块，覆盖了各种常用功能。

### 系统相关模块
```python
# os模块 - 操作系统接口
import os

# 获取当前工作目录
current_dir = os.getcwd()
print(f"当前目录: {current_dir}")

# 列出目录内容
files = os.listdir(".")
print(f"文件列表: {files}")

# 创建目录
os.makedirs("new_directory", exist_ok=True)

# 环境变量
home_dir = os.environ.get("HOME", "未设置")
print(f"家目录: {home_dir}")

# sys模块 - 系统相关参数和函数
import sys

# 命令行参数
print(f"脚本名: {sys.argv[0]}")
print(f"参数: {sys.argv[1:]}")

# Python版本
print(f"Python版本: {sys.version}")

# 退出程序
# sys.exit(0)  # 正常退出
# sys.exit(1)  # 异常退出
```

### 数据处理模块
```python
# json模块 - JSON数据处理
import json

# 数据序列化
data = {"name": "张三", "age": 25, "skills": ["Python", "Java"]}
json_string = json.dumps(data, ensure_ascii=False, indent=2)
print(json_string)

# 数据反序列化
parsed_data = json.loads(json_string)
print(f"姓名: {parsed_data['name']}")

# 文件操作
with open("data.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

with open("data.json", "r", encoding="utf-8") as f:
    loaded_data = json.load(f)
    print(loaded_data)

# datetime模块 - 日期和时间处理
from datetime import datetime, date, timedelta

# 当前时间
now = datetime.now()
print(f"当前时间: {now}")

# 格式化时间
formatted = now.strftime("%Y-%m-%d %H:%M:%S")
print(f"格式化时间: {formatted}")

# 解析时间字符串
parsed_time = datetime.strptime("2023-01-01 12:00:00", "%Y-%m-%d %H:%M:%S")
print(f"解析时间: {parsed_time}")

# 日期计算
today = date.today()
future_date = today + timedelta(days=30)
print(f"30天后: {future_date}")
```

### 数学和随机数模块
```python
# math模块 - 数学函数
import math

print(f"π: {math.pi}")
print(f"e: {math.e}")
print(f"平方根: {math.sqrt(16)}")
print(f"正弦值: {math.sin(math.pi/2)}")
print(f"对数: {math.log(math.e)}")

# random模块 - 随机数生成
import random

# 随机浮点数
print(f"0-1随机数: {random.random()}")

# 随机整数
print(f"1-10随机整数: {random.randint(1, 10)}")

# 随机选择
colors = ["红", "绿", "蓝", "黄"]
print(f"随机颜色: {random.choice(colors)}")

# 随机打乱
numbers = [1, 2, 3, 4, 5]
random.shuffle(numbers)
print(f"打乱后: {numbers}")

# 随机采样
sample = random.sample(range(1, 100), 5)
print(f"随机采样: {sample}")
```

## 4. 自定义模块

创建自己的模块文件，实现代码的模块化和重用。

### 模块结构
```python
# my_module.py - 自定义模块示例
"""自定义模块示例"""

# 模块级常量
VERSION = "1.0.0"
AUTHOR = "开发者"

# 模块级变量
_counter = 0

# 模块级函数
def get_version():
    """获取模块版本"""
    return VERSION

def increment_counter():
    """增加计数器"""
    global _counter
    _counter += 1
    return _counter

# 类定义
class DataProcessor:
    """数据处理器"""
    
    def __init__(self):
        self.data = []
    
    def add_data(self, item):
        """添加数据"""
        self.data.append(item)
    
    def process(self):
        """处理数据"""
        return [item * 2 for item in self.data]

# 模块初始化代码
print(f"模块 {__name__} 已加载，版本: {VERSION}")

# 受保护的函数（约定）
def _internal_function():
    """内部函数"""
    return "这是内部函数"

# 私有函数（名称改写）
def __private_function():
    """私有函数"""
    return "这是私有函数"
```

### 使用自定义模块
```python
# main.py - 使用自定义模块
import my_module

# 使用模块功能
print(f"版本: {my_module.get_version()}")
print(f"计数: {my_module.increment_counter()}")

# 使用类
processor = my_module.DataProcessor()
processor.add_data(1)
processor.add_data(2)
processor.add_data(3)
result = processor.process()
print(f"处理结果: {result}")

# 访问模块级变量
print(f"计数器值: {my_module._counter}")
```

## 5. 包的概念

包是一种组织模块的层次结构，是包含`__init__.py`文件的目录。

### 包的结构
```
mypackage/
    __init__.py
    module1.py
    module2.py
    subpackage/
        __init__.py
        module3.py
        module4.py
```

### 创建包
```python
# mypackage/__init__.py
"""我的包"""

__version__ = "1.0.0"
__author__ = "开发者"

# 包级别的初始化代码
print("mypackage包已初始化")

# 定义包的公共接口
from .module1 import function1
from .module2 import Class2

# 控制导入的公共接口
__all__ = ['function1', 'Class2', '__version__']
```

```python
# mypackage/module1.py
"""模块1"""

def function1():
    """函数1"""
    return "这是模块1的函数1"

def helper_function():
    """辅助函数"""
    return "这是模块1的辅助函数"
```

```python
# mypackage/module2.py
"""模块2"""

class Class2:
    """类2"""
    def __init__(self, name):
        self.name = name
    
    def greet(self):
        return f"你好, {self.name}!"
```

```python
# mypackage/subpackage/__init__.py
"""子包"""

from .module3 import SubClass
```

```python
# mypackage/subpackage/module3.py
"""模块3"""

class SubClass:
    """子类"""
    def __init__(self, value):
        self.value = value
    
    def get_value(self):
        return self.value
```

### 使用包
```python
# 使用包的不同方式
import mypackage
from mypackage import module1
from mypackage.module2 import Class2
from mypackage.subpackage import module3
from mypackage.subpackage.module3 import SubClass

# 访问包内容
print(mypackage.__version__)
print(module1.function1())

obj = Class2("张三")
print(obj.greet())

sub_obj = SubClass(42)
print(sub_obj.get_value())
```

## 6. 包的导入

包的导入方式与模块类似，但支持更复杂的层次结构。

### 导入包中的模块
```python
# 导入包中的模块
import mypackage.module1
result = mypackage.module1.function1()

# 从包中导入模块
from mypackage import module1
result = module1.function1()

# 从包的模块中导入特定对象
from mypackage.module1 import function1
result = function1()

# 导入子包
from mypackage.subpackage.module3 import SubClass
obj = SubClass(100)
```

### 包的相对导入
```python
# mypackage/module1.py中的相对导入
from .module2 import Class2          # 同级模块
from .subpackage.module3 import SubClass  # 子包模块
from ..utils import helper          # 上级包模块（如果存在）

# mypackage/subpackage/module3.py中的相对导入
from ..module1 import function1      # 上级包模块
from . import SubClass              # 同级导入
```

## 7. sys.path和模块搜索路径

Python在`sys.path`列表中指定的路径中搜索模块。

### 查看和修改模块搜索路径
```python
import sys
import os

# 查看当前模块搜索路径
print("模块搜索路径:")
for path in sys.path:
    print(f"  {path}")

# 添加自定义路径
custom_path = "/path/to/my/modules"
if custom_path not in sys.path:
    sys.path.insert(0, custom_path)
    print(f"已添加路径: {custom_path}")

# 使用环境变量添加路径
# export PYTHONPATH="/path/to/my/modules:$PYTHONPATH"

# 动态添加路径
project_root = os.path.dirname(os.path.abspath(__file__))
modules_path = os.path.join(project_root, "modules")
if modules_path not in sys.path:
    sys.path.append(modules_path)
```

## 8. __name__和__main__

每个模块都有一个`__name__`属性，用于区分模块是被导入还是直接运行。

### 模块的双重用途
```python
# utility.py - 实用工具模块
"""实用工具模块"""

def add(a, b):
    """加法函数"""
    return a + b

def subtract(a, b):
    """减法函数"""
    return a - b

def main():
    """主函数"""
    print("实用工具模块")
    print(f"2 + 3 = {add(2, 3)}")
    print(f"5 - 2 = {subtract(5, 2)}")

if __name__ == "__main__":
    # 当脚本被直接运行时执行
    main()
else:
    # 当模块被导入时执行
    print(f"模块 {__name__} 被导入")
```

### 实际应用示例
```python
# calculator.py - 计算器模块
"""计算器模块"""

class Calculator:
    def add(self, a, b):
        return a + b
    
    def subtract(self, a, b):
        return a - b

def main():
    """命令行计算器"""
    import sys
    
    if len(sys.argv) != 4:
        print("用法: python calculator.py <操作> <数字1> <数字2>")
        print("操作: add, subtract")
        return
    
    operation = sys.argv[1]
    num1 = float(sys.argv[2])
    num2 = float(sys.argv[3])
    
    calc = Calculator()
    
    if operation == "add":
        result = calc.add(num1, num2)
    elif operation == "subtract":
        result = calc.subtract(num1, num2)
    else:
        print("不支持的操作")
        return
    
    print(f"结果: {result}")

if __name__ == "__main__":
    main()
```

## 9. 模块搜索和加载机制

### 模块缓存
```python
import sys

# 查看已加载的模块
print("已加载的模块:")
for name in sorted(sys.modules.keys()):
    if not name.startswith("_"):  # 过滤内置模块
        print(f"  {name}")

# 模块只在第一次导入时执行
# utils.py
def get_counter():
    import utils
    return utils.counter

# 第一次导入时会执行模块级代码
# 后续导入不会重新执行
```

### 重新加载模块
```python
import importlib

# 重新加载模块（开发时有用）
import my_module
importlib.reload(my_module)  # 重新加载模块

# 动态导入模块
module_name = "math"
math_module = importlib.import_module(module_name)
print(math_module.sqrt(16))
```

## 10. 实际应用场景

### 项目模块化组织
```python
# 项目结构示例
"""
myproject/
    __init__.py
    main.py
    config/
        __init__.py
        settings.py
        database.py
    models/
        __init__.py
        user.py
        product.py
    views/
        __init__.py
        user_view.py
        product_view.py
    utils/
        __init__.py
        helpers.py
        validators.py
"""

# config/settings.py
"""配置设置"""

DEBUG = True
DATABASE_URL = "sqlite:///app.db"
SECRET_KEY = "your-secret-key"

# models/user.py
"""用户模型"""

class User:
    def __init__(self, username, email):
        self.username = username
        self.email = email
    
    def __str__(self):
        return f"User({self.username})"

# utils/helpers.py
"""辅助函数"""

def format_currency(amount):
    return f"¥{amount:.2f}"

def validate_email(email):
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

# main.py
"""主程序"""

from config.settings import DEBUG
from models.user import User
from utils.helpers import format_currency, validate_email

def main():
    if DEBUG:
        print("调试模式已启用")
    
    user = User("张三", "zhangsan@example.com")
    print(user)
    
    amount = 1234.56
    print(f"金额: {format_currency(amount)}")
    
    email = "test@example.com"
    if validate_email(email):
        print(f"邮箱 {email} 格式正确")

if __name__ == "__main__":
    main()
```

### 第三方库管理
```python
# requirements.txt
"""
requests==2.28.1
numpy==1.24.0
pandas==1.5.2
matplotlib==3.6.2
"""

# setup.py - 包配置文件
from setuptools import setup, find_packages

setup(
    name="myproject",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "requests>=2.28.0",
        "numpy>=1.24.0",
        "pandas>=1.5.0",
    ],
    author="开发者",
    author_email="developer@example.com",
    description="我的Python项目",
    python_requires=">=3.7",
)
```

## 11. 最佳实践

### 模块命名规范
```python
# 好的命名
# my_utils.py
# data_processor.py
# user_authentication.py

# 避免的命名
# MyUtils.py  # 避免大写
# 123utils.py  # 避免数字开头
# my-utils.py  # 避免特殊字符
```

### 导入语句组织
```python
# 标准库导入
import os
import sys
import json
from datetime import datetime

# 第三方库导入
import requests
import numpy as np
import pandas as pd

# 本地应用/库导入
from mypackage.utils import helper_function
from mypackage.models import User, Product

# 在函数内部导入（避免循环导入）
def heavy_computation():
    from scipy import stats  # 只在需要时导入
    # 计算逻辑
    pass
```

### 使用__all__控制公共接口
```python
# mymodule.py
"""我的模块"""

__all__ = ['public_function', 'PublicClass']

def public_function():
    """公共函数"""
    return "这是公共函数"

def _private_function():
    """私有函数"""
    return "这是私有函数"

class PublicClass:
    """公共类"""
    pass

class _PrivateClass:
    """私有类"""
    pass

# 当使用 from mymodule import * 时，只会导入 __all__ 中列出的对象
```

### 避免循环导入
```python
# 方案1: 重构代码结构
# 方案2: 延迟导入
# 方案3: 使用导入钩子

# user.py
class User:
    def __init__(self, name):
        self.name = name
    
    def get_orders(self):
        # 延迟导入避免循环导入
        from order import Order
        return Order.get_user_orders(self)

# order.py
class Order:
    @staticmethod
    def get_user_orders(user):
        # 订单逻辑
        return []
```