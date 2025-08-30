# Python数据类型知识点

## 1. 数字类型 (Numeric Types)

### int (整数)
整数是没有小数部分的数字，可以是正数、负数或零。

#### 特点
- 任意精度，只受内存限制
- 支持二进制(0b)、八进制(0o)、十六进制(0x)表示
- 在Python 3中，int类型统一了Python 2中的int和long类型

#### 使用示例
```python
# 基本整数
age = 25
temperature = -10
zero = 0

# 不同进制表示
binary_num = 0b1010    # 二进制，等于10
octal_num = 0o12       # 八进制，等于10
hex_num = 0xA          # 十六进制，等于10

# 大整数
big_number = 123456789012345678901234567890
```

#### 实际应用场景
- 计数和索引操作
- 循环控制变量
- 数组和列表的索引
- 数学计算中的整数运算

### float (浮点数)
浮点数是带有小数部分的数字，用于表示实数。

#### 特点
- 双精度浮点数（64位）
- 存在精度问题，不适合精确计算
- 支持科学计数法表示

#### 使用示例
```python
# 基本浮点数
pi = 3.14159
temperature = -5.5
zero_point = 0.0

# 科学计数法
large_number = 1.5e10    # 1.5 * 10^10
small_number = 2.3e-5    # 2.3 * 10^-5

# 特殊值
import math
not_a_number = float('nan')
infinity = float('inf')
```

#### 实际应用场景
- 科学计算和工程应用
- 测量值和传感器数据
- 图形和图像处理
- 金融计算（需要注意精度问题）

### complex (复数)
复数由实部和虚部组成，虚部以j或J结尾。

#### 特点
- 实部和虚部都是浮点数
- 支持复数运算
- 常用于工程计算和信号处理

#### 使用示例
```python
# 复数定义
z1 = 3 + 4j
z2 = complex(2, -1)  # 2-1j

# 复数运算
print(z1 + z2)       # (5+3j)
print(z1 * z2)       # (10+5j)
print(z1.conjugate()) # (3-4j)

# 访问实部和虚部
print(z1.real)       # 3.0
print(z1.imag)       # 4.0
```

#### 实际应用场景
- 工程计算和电路分析
- 信号处理和傅里叶变换
- 量子计算和物理模拟
- 数学研究和教育

## 2. 布尔类型 (Boolean Type)

### bool
布尔类型只有两个值：True和False，通常用于条件判断。

#### 特点
- 实际上是int的子类，True=1，False=0
- 支持逻辑运算
- 用于控制程序流程

#### 使用示例
```python
# 基本布尔值
is_python_fun = True
is_java_better = False

# 比较运算结果
result = 5 > 3  # True
result = 5 < 3  # False

# 逻辑运算
print(True and False)  # False
print(True or False)   # True
print(not True)        # False

# 真值测试
print(bool(0))         # False
print(bool(1))         # True
print(bool(""))        # False
print(bool("Hello"))   # True
print(bool([]))        # False
print(bool([1, 2, 3])) # True
```

#### 实际应用场景
- 逻辑判断和条件控制
- 开关控制和状态标记
- 用户权限和认证检查
- 数据验证和错误处理

## 3. 序列类型 (Sequence Types)

### str (字符串)
字符串是由字符组成的不可变序列。

#### 特点
- 不可变性：创建后不能修改
- 支持索引和切片操作
- 丰富的字符串方法

#### 使用示例
```python
# 字符串创建
name = "Alice"
message = 'Hello, World!'
multiline = """这是
多行
字符串"""

# 索引和切片
text = "Python"
print(text[0])     # 'P'
print(text[-1])    # 'n'
print(text[1:4])   # 'yth'
print(text[::-1])  # 'nohtyP'

# 字符串方法
text = "hello world"
print(text.upper())        # 'HELLO WORLD'
print(text.split())        # ['hello', 'world']
print(text.replace('o', '0'))  # 'hell0 w0rld'
```

#### 实际应用场景
- 文本处理和自然语言处理
- 用户界面显示和交互
- 文件路径处理和系统操作
- 配置文件和数据格式处理

### list (列表)
列表是可变的有序元素集合。

#### 特点
- 可变性：可以修改、添加、删除元素
- 有序性：元素保持插入顺序
- 可包含不同类型元素

#### 使用示例
```python
# 列表创建
numbers = [1, 2, 3, 4, 5]
mixed = [1, "hello", 3.14, True]
empty = []

# 列表操作
fruits = ["apple", "banana", "orange"]
fruits.append("grape")      # 添加元素
fruits.insert(1, "kiwi")    # 在指定位置插入
fruits.remove("banana")     # 删除指定元素
fruits.pop()                # 删除并返回最后一个元素

# 列表切片
print(fruits[1:3])          # 获取子列表
fruits[0] = "mango"         # 修改元素
```

#### 实际应用场景
- 数据存储和批量处理
- 动态数组和缓冲区
- 算法实现和数据结构
- 配置管理和数据集合

### tuple (元组)
元组是不可变的有序元素集合。

#### 特点
- 不可变性：创建后不能修改
- 可以作为字典键使用
- 性能比列表略高

#### 使用示例
```python
# 元组创建
coordinates = (10, 20)
rgb_color = (255, 128, 0)
person = ("Alice", 25, "Engineer")
empty_tuple = ()

# 元组操作
x, y = coordinates           # 元组解包
name, age, job = person     # 多重赋值

# 访问元素
print(coordinates[0])        # 10
print(person[1:3])          # (25, 'Engineer')
```

#### 实际应用场景
- 坐标表示和几何计算
- 数据库记录和结构化数据
- 函数多返回值
- 配置项和常量集合

## 4. 映射类型 (Mapping Type)

### dict (字典)
字典是键值对的集合，提供高效的键值映射。

#### 特点
- 键必须是不可变类型且唯一
- 值可以是任意类型
- 查找效率高（哈希表实现）
- 无序性（Python 3.7+保持插入顺序）

#### 使用示例
```python
# 字典创建
person = {"name": "Alice", "age": 25, "job": "Engineer"}
empty_dict = {}
using_dict = dict(name="Bob", age=30)

# 字典操作
person["city"] = "Beijing"      # 添加键值对
person["age"] = 26              # 修改值
del person["job"]               # 删除键值对

# 访问值
print(person["name"])           # "Alice"
print(person.get("salary", 0))  # 获取值，不存在返回默认值

# 字典方法
print(person.keys())            # 所有键
print(person.values())          # 所有值
print(person.items())           # 所有键值对
```

#### 实际应用场景
- 配置信息和设置管理
- 缓存和索引构建
- JSON数据处理
- 数据库记录映射

## 5. 集合类型 (Set Types)

### set (集合)
集合是不重复元素的无序集合。

#### 特点
- 元素不重复
- 元素必须是不可变类型
- 支持集合运算（并、交、差等）
- 高效的成员关系测试

#### 使用示例
```python
# 集合创建
numbers = {1, 2, 3, 4, 5}
fruits = set(["apple", "banana", "orange"])
empty_set = set()

# 集合操作
numbers.add(6)                  # 添加元素
numbers.remove(1)               # 删除元素
numbers.discard(10)             # 删除元素（不存在不报错）

# 集合运算
set1 = {1, 2, 3}
set2 = {3, 4, 5}
print(set1 | set2)              # 并集: {1, 2, 3, 4, 5}
print(set1 & set2)              # 交集: {3}
print(set1 - set2)              # 差集: {1, 2}
print(set1 ^ set2)              # 对称差集: {1, 2, 4, 5}
```

#### 实际应用场景
- 去重和唯一性检查
- 成员关系测试
- 数据分析和统计
- 权限管理和标签系统

### frozenset (不可变集合)
不可变版本的集合。

#### 特点
- 不可变性：创建后不能修改
- 可以作为字典的键或其他集合的元素
- 支持所有set的操作（除了修改操作）

#### 使用示例
```python
# 不可变集合创建
frozen = frozenset([1, 2, 3, 4, 5])

# 作为字典键
dict_with_frozenset_key = {frozen: "value"}

# 集合运算（与set相同）
set1 = frozenset([1, 2, 3])
set2 = frozenset([3, 4, 5])
print(set1 | set2)  # frozenset({1, 2, 3, 4, 5})
```

#### 实际应用场景
- 需要不可变集合的场景
- 作为字典键使用
- 函数参数传递（保证不被修改）

## 6. 类型检查和转换

### 类型检查
```python
# 使用type()函数
print(type(42))           # <class 'int'>
print(type(3.14))         # <class 'float'>
print(type("Hello"))      # <class 'str'>

# 使用isinstance()函数（推荐）
print(isinstance(42, int))        # True
print(isinstance(42, (int, float)))  # True（检查多个类型）
```

### 类型转换
```python
# 显式类型转换
num_str = "123"
num_int = int(num_str)      # 字符串转整数
num_float = float(num_str)  # 字符串转浮点数

# 数值类型转换
int_to_float = float(42)    # 整数转浮点数
float_to_int = int(3.14)    # 浮点数转整数（截断小数部分）

# 序列类型转换
list_to_tuple = tuple([1, 2, 3])    # 列表转元组
tuple_to_list = list((1, 2, 3))     # 元组转列表
str_to_list = list("hello")         # 字符串转字符列表
```

## 7. 实际应用场景

### 数据分析
```python
# 使用列表存储数据
sales_data = [100, 150, 200, 175, 300]

# 使用字典存储结构化数据
employee = {
    "name": "Alice",
    "department": "Engineering",
    "salary": 75000,
    "skills": ["Python", "Java", "SQL"]
}
```

### Web开发
```python
# HTTP请求参数处理
request_params = {
    "user_id": 12345,
    "action": "login",
    "timestamp": "2023-01-01T12:00:00Z"
}

# 响应数据构建
response_data = {
    "status": "success",
    "data": {"user_name": "Alice", "login_time": "2023-01-01"},
    "message": "Login successful"
}
```

### 科学计算
```python
# 使用复数进行工程计算
impedance = 50 + 30j  # 50Ω电阻和30Ω电抗
current = 2 + 0j      # 2A电流
voltage = impedance * current  # 欧姆定律
```

### 文本处理
```python
# 文本分析
text = "Python is a powerful programming language"
words = text.split()  # ['Python', 'is', 'a', 'powerful', 'programming', 'language']
unique_words = set(words)  # 去重
word_count = len(words)    # 计数
```

## 8. 最佳实践

### 选择合适的数据类型
```python
# 根据使用场景选择
# 需要修改数据时使用列表
shopping_cart = ["apple", "banana"]
shopping_cart.append("orange")

# 不需要修改且需要作为字典键时使用元组
coordinates_map = {(0, 0): "origin", (1, 1): "point A"}

# 需要快速查找时使用集合
valid_extensions = {".txt", ".pdf", ".doc"}
if file_extension in valid_extensions:
    process_file()
```

### 注意可变类型和不可变类型的特性差异
```python
# 可变类型的副作用
list1 = [1, 2, 3]
list2 = list1  # 两个变量指向同一个列表
list2.append(4)
print(list1)   # [1, 2, 3, 4] - list1也被修改了

# 避免副作用
list1 = [1, 2, 3]
list2 = list1.copy()  # 创建副本
list2.append(4)
print(list1)   # [1, 2, 3] - list1未被修改
```

### 使用类型提示提高代码可读性
```python
from typing import List, Dict, Tuple

def process_data(numbers: List[int]) -> Dict[str, int]:
    """处理数字列表，返回统计信息"""
    return {
        "count": len(numbers),
        "sum": sum(numbers),
        "average": sum(numbers) // len(numbers) if numbers else 0
    }

def get_coordinates() -> Tuple[float, float]:
    """获取坐标"""
    return (10.5, 20.3)
```