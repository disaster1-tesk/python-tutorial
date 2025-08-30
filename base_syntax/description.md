# Python基础语法知识点

## 1. 变量和赋值

Python中的变量不需要声明类型，直接赋值即可。变量名区分大小写，可以包含字母、数字和下划线，但不能以数字开头。

### 特点
- **动态类型**：变量的类型在运行时确定
- **弱类型**：同一个变量可以赋不同类型的值
- **引用语义**：变量实际上是对象的引用

### 变量命名规范
- 推荐使用小写字母和下划线组合（snake_case）
- 不能使用Python关键字作为变量名
- 避免使用内置函数名作为变量名

### 变量赋值
```python
# 基本赋值
name = "Alice"
age = 25

# 多重赋值
a = b = c = 10

# 多变量赋值
x, y, z = 1, 2, 3

# 交换变量值
a, b = b, a
```

### 实际应用场景
- 存储用户输入和配置参数
- 保存计算结果和中间值
- 控制程序流程的状态标志

## 2. 注释

注释是代码中的说明文字，不会被解释器执行，用于提高代码可读性。

### 注释类型
- **单行注释**：使用 `#` 符号
- **多行注释**：使用三引号 `'''` 或 `"""`
- **文档字符串**：在函数、类、模块开头使用三引号添加文档说明

### 使用示例
```python
# 这是单行注释

"""
这是多行注释
可以写很多行
用于详细说明代码功能
"""

def calculate_area(radius):
    """
    计算圆的面积
    
    Args:
        radius (float): 圆的半径
        
    Returns:
        float: 圆的面积
    """
    return 3.14159 * radius ** 2
```

### 实际应用场景
- 解释复杂逻辑和算法思路
- 记录代码变更和版本信息
- 临时禁用代码段进行调试
- 为团队协作提供代码说明

## 3. 缩进

Python使用缩进来表示代码块，这是Python语法的重要组成部分。

### 缩进规则
- **标准缩进**：4个空格（PEP 8规范）
- **一致性**：同一代码块必须使用相同的缩进
- **避免混用**：不要在同一文件中混用空格和制表符

### 使用示例
```python
# 正确的缩进
if age >= 18:
    print("成年人")
    if age >= 60:
        print("老年人")
else:
    print("未成年人")

# 函数定义中的缩进
def greet(name):
    message = f"你好, {name}!"
    return message

# 类定义中的缩进
class Person:
    def __init__(self, name):
        self.name = name
    
    def introduce(self):
        return f"我是{self.name}"
```

### 实际应用场景
- 定义函数体和类体
- 控制条件语句和循环体
- 组织代码结构和层次关系

## 4. 输出函数

`print()`函数用于输出信息到控制台，是Python中最常用的输出方式。

### 基本用法
```python
# 基本输出
print("Hello, World!")

# 多参数输出
print("姓名:", "张三", "年龄:", 25)

# 格式化输出
name = "李四"
age = 30
print("姓名: %s, 年龄: %d" % (name, age))
print("姓名: {}, 年龄: {}".format(name, age))
print(f"姓名: {name}, 年龄: {age}")

# 指定分隔符和结束符
print("a", "b", "c", sep="-", end="!\n")
```

### 实际应用场景
- 调试信息输出和变量值查看
- 程序运行状态显示
- 用户交互和结果展示
- 日志信息输出

## 5. 输入函数

`input()`函数用于从用户获取输入，返回的是字符串类型。

### 基本用法
```python
# 基本输入
user_input = input("请输入内容: ")

# 类型转换
age = int(input("请输入年龄: "))
height = float(input("请输入身高: "))

# 输入验证
while True:
    try:
        number = int(input("请输入一个数字: "))
        break
    except ValueError:
        print("输入无效，请重新输入")
```

### 实际应用场景
- 用户交互和数据录入
- 配置设置和参数输入
- 测试用例的手动输入
- 命令行工具的参数获取

## 6. 命名规范和约定

Python有一套推荐的命名规范，有助于提高代码的可读性和一致性。

### 命名约定
- **模块名**：全小写，可使用下划线
- **函数名和变量名**：小写字母，单词间用下划线分隔
- **常量名**：大写字母，单词间用下划线分隔
- **类名**：采用大驼峰命名法（CamelCase）
- **私有成员**：以单下划线开头

### 使用示例
```python
# 模块名: my_module.py

# 常量
MAX_SIZE = 100
DEFAULT_NAME = "Unknown"

# 函数和变量
def calculate_sum(a, b):
    result = a + b
    return result

user_name = "Alice"
user_age = 25

# 类名
class DataProcessor:
    def __init__(self):
        self._private_data = []
    
    def process(self):
        pass
```

### 实际应用场景
- 团队协作开发中的代码规范
- 开源项目贡献的代码风格
- 提高代码可读性和维护性
- 遵循社区最佳实践

## 7. 基本运算符

Python支持多种运算符用于执行不同的操作。

### 运算符类型
- **算术运算符**：`+`、`-`、`*`、`/`、`//`、`%`、`**`
- **比较运算符**：`==`、`!=`、`<`、`>`、`<=`、`>=`
- **逻辑运算符**：`and`、`or`、`not`
- **赋值运算符**：`=`、`+=`、`-=`、`*=`、`/=`等

### 使用示例
```python
# 算术运算
a, b = 10, 3
print(a + b)   # 13
print(a - b)   # 7
print(a * b)   # 30
print(a / b)   # 3.333...
print(a // b)  # 3
print(a % b)   # 1
print(a ** b)  # 1000

# 比较运算
print(a > b)   # True
print(a == b)  # False
print(a != b)  # True

# 逻辑运算
x, y = True, False
print(x and y)  # False
print(x or y)   # True
print(not x)    # False

# 赋值运算
c = 5
c += 3  # 等价于 c = c + 3
```

### 实际应用场景
- 数学计算和科学运算
- 条件判断和流程控制
- 数据处理和转换
- 算法实现和逻辑运算

## 8. 字符串基础

字符串是Python中常用的数据类型，用于表示文本信息。

### 字符串定义
```python
# 单引号
str1 = 'Hello'

# 双引号
str2 = "World"

# 三引号（多行字符串）
str3 = """这是
多行
字符串"""

# 转义字符
path = "C:\\Users\\Name\\Documents"
message = "换行符:\n制表符:\t"
```

### 字符串操作
```python
# 字符串拼接
full_name = "张" + "三"
greeting = "Hello" + " " + "World"

# 字符串重复
line = "-" * 20

# 字符串方法
text = "hello world"
print(text.upper())      # HELLO WORLD
print(text.capitalize()) # Hello world
print(text.replace("world", "Python"))  # hello Python
```

### 实际应用场景
- 文本处理和自然语言处理
- 用户界面显示和交互
- 文件路径处理和系统操作
- 配置文件和数据格式处理