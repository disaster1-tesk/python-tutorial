# Python高级特性知识点

## 1. 列表推导式 (List Comprehensions)

列表推导式是一种简洁地创建列表的语法结构，比传统的循环更高效且更具可读性。

### 基本语法
```python
[expression for item in iterable if condition]
```

### 使用示例
```python
# 基本列表推导式
squares = [x**2 for x in range(10)]
print(squares)  # [0, 1, 4, 9, 16, 25, 36, 49, 64, 81]

# 带条件的列表推导式
even_squares = [x**2 for x in range(10) if x % 2 == 0]
print(even_squares)  # [0, 4, 16, 36, 64]

# 使用函数的列表推导式
words = ["hello", "world", "python"]
upper_words = [word.upper() for word in words]
print(upper_words)  # ['HELLO', 'WORLD', 'PYTHON']

# 复杂表达式的列表推导式
numbers = [1, 2, 3, 4, 5]
results = [x if x % 2 == 0 else x * 2 for x in numbers]
print(results)  # [2, 2, 6, 4, 10]
```

### 嵌套列表推导式
```python
# 嵌套循环
matrix = [[i*3 + j for j in range(1, 4)] for i in range(3)]
print(matrix)  # [[1, 2, 3], [4, 5, 6], [7, 8, 9]]

# 扁平化嵌套列表
nested_list = [[1, 2], [3, 4], [5, 6]]
flattened = [item for sublist in nested_list for item in sublist]
print(flattened)  # [1, 2, 3, 4, 5, 6]

# 复杂嵌套示例
matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
diagonal = [matrix[i][i] for i in range(len(matrix))]
print(diagonal)  # [1, 5, 9]
```

## 2. 字典和集合推导式

### 字典推导式
```python
# 基本字典推导式
square_dict = {x: x**2 for x in range(5)}
print(square_dict)  # {0: 0, 1: 1, 2: 4, 3: 9, 4: 16}

# 带条件的字典推导式
even_square_dict = {x: x**2 for x in range(10) if x % 2 == 0}
print(even_square_dict)  # {0: 0, 2: 4, 4: 16, 6: 36, 8: 64}

# 从列表创建字典
keys = ["name", "age", "city"]
values = ["张三", 25, "北京"]
person_dict = {k: v for k, v in zip(keys, values)}
print(person_dict)  # {'name': '张三', 'age': 25, 'city': '北京'}

# 反转字典
original = {"a": 1, "b": 2, "c": 3}
reversed_dict = {v: k for k, v in original.items()}
print(reversed_dict)  # {1: 'a', 2: 'b', 3: 'c'}
```

### 集合推导式
```python
# 基本集合推导式
unique_lengths = {len(word) for word in ["apple", "banana", "cherry", "date"]}
print(unique_lengths)  # {4, 5, 6}

# 带条件的集合推导式
even_numbers = {x for x in range(20) if x % 2 == 0}
print(even_numbers)  # {0, 2, 4, 6, 8, 10, 12, 14, 16, 18}

# 从字符串创建字符集合
text = "hello world"
unique_chars = {char for char in text if char != ' '}
print(unique_chars)  # {'r', 'd', 'w', 'l', 'o', 'e', 'h'}

# 去重操作
numbers = [1, 2, 2, 3, 3, 3, 4, 4, 4, 4]
unique_numbers = {x for x in numbers}
print(unique_numbers)  # {1, 2, 3, 4}
```

## 3. 生成器 (Generators)

生成器是一种特殊的迭代器，按需生成值，节省内存。

### 生成器函数
```python
# 生成器函数
def countdown(n):
    """倒计时生成器"""
    while n > 0:
        yield n
        n -= 1

# 使用生成器
for num in countdown(5):
    print(num)  # 5, 4, 3, 2, 1

# 生成器对象
gen = countdown(3)
print(next(gen))  # 3
print(next(gen))  # 2
print(next(gen))  # 1
# print(next(gen))  # StopIteration 异常
```

### 生成器表达式
```python
# 生成器表达式
even_numbers = (x for x in range(10) if x % 2 == 0)
print(list(even_numbers))  # [0, 2, 4, 6, 8]

# 与列表推导式的比较
# 列表推导式 - 立即创建所有元素
squares_list = [x**2 for x in range(5)]
print(squares_list)  # [0, 1, 4, 9, 16]

# 生成器表达式 - 按需生成元素
squares_gen = (x**2 for x in range(5))
print(list(squares_gen))  # [0, 1, 4, 9, 16]

# 内存使用比较
import sys
list_comp = [x for x in range(1000000)]
gen_exp = (x for x in range(1000000))
print(f"列表推导式大小: {sys.getsizeof(list_comp)} 字节")
print(f"生成器表达式大小: {sys.getsizeof(gen_exp)} 字节")
```

### 实际应用示例
```python
def fibonacci_generator(n):
    """斐波那契数列生成器"""
    a, b = 0, 1
    count = 0
    while count < n:
        yield a
        a, b = b, a + b
        count += 1

# 使用斐波那契生成器
fib_gen = fibonacci_generator(10)
print(list(fib_gen))  # [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]

def read_large_file(file_path):
    """逐行读取大文件的生成器"""
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            yield line.strip()

# 使用文件读取生成器
# for line in read_large_file('large_file.txt'):
#     process_line(line)
```

## 4. 装饰器 (Decorators)

装饰器用于修改或增强函数或类的行为，使用@语法糖应用。

### 基本装饰器
```python
# 基本装饰器
def my_decorator(func):
    """简单装饰器"""
    def wrapper(*args, **kwargs):
        print("函数调用前")
        result = func(*args, **kwargs)
        print("函数调用后")
        return result
    return wrapper

@my_decorator
def say_hello(name):
    """打招呼函数"""
    print(f"你好, {name}!")

say_hello("张三")
# 输出:
# 函数调用前
# 你好, 张三!
# 函数调用后
```

### 带参数的装饰器
```python
# 带参数的装饰器
def repeat(times):
    """重复执行装饰器"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            for _ in range(times):
                result = func(*args, **kwargs)
            return result
        return wrapper
    return decorator

@repeat(3)
def greet():
    """问候函数"""
    print("欢迎!")

greet()
# 输出:
# 欢迎!
# 欢迎!
# 欢迎!
```

### 类装饰器
```python
# 类装饰器
class CountCalls:
    """计数调用次数的装饰器"""
    def __init__(self, func):
        self.func = func
        self.count = 0
    
    def __call__(self, *args, **kwargs):
        self.count += 1
        print(f"函数 {self.func.__name__} 被调用了 {self.count} 次")
        return self.func(*args, **kwargs)

@CountCalls
def say_hello():
    """打招呼函数"""
    print("Hello!")

say_hello()  # 函数 say_hello 被调用了 1 次
say_hello()  # 函数 say_hello 被调用了 2 次
```

### functools.wraps的使用
```python
from functools import wraps

def my_decorator(func):
    """保持原函数元信息的装饰器"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        """装饰器包装函数"""
        print("装饰器执行")
        return func(*args, **kwargs)
    return wrapper

@my_decorator
def example_function():
    """示例函数"""
    print("原函数执行")

print(example_function.__name__)  # example_function (而不是wrapper)
print(example_function.__doc__)   # 示例函数 (而不是装饰器包装函数)
```

### 实用装饰器示例
```python
import time
from functools import wraps

def timer(func):
    """计时装饰器"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"{func.__name__} 执行时间: {end_time - start_time:.4f}秒")
        return result
    return wrapper

def cache(func):
    """简单缓存装饰器"""
    cached_results = {}
    
    @wraps(func)
    def wrapper(*args, **kwargs):
        key = str(args) + str(sorted(kwargs.items()))
        if key not in cached_results:
            cached_results[key] = func(*args, **kwargs)
        return cached_results[key]
    return wrapper

@timer
@cache
def fibonacci(n):
    """计算斐波那契数列"""
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

print(fibonacci(10))  # 计算并缓存结果
print(fibonacci(10))  # 直接从缓存获取结果
```

## 5. 上下文管理器 (Context Managers)

上下文管理器用于资源管理，确保正确获取和释放资源。

### 使用类实现上下文管理器
```python
class MyContextManager:
    """自定义上下文管理器"""
    def __enter__(self):
        print("进入上下文")
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        print("退出上下文")
        if exc_type:
            print(f"异常类型: {exc_type}")
            print(f"异常值: {exc_value}")
        return False  # 不抑制异常

# 使用自定义上下文管理器
with MyContextManager() as cm:
    print("在上下文内部")
    # raise ValueError("测试异常")
```

### 使用contextlib模块
```python
from contextlib import contextmanager

@contextmanager
def my_context():
    """使用contextmanager装饰器"""
    print("上下文开始")
    try:
        yield "资源"
    finally:
        print("上下文结束")

# 使用contextmanager
with my_context() as resource:
    print(f"使用{resource}")

# 数据库连接示例
@contextmanager
def database_connection():
    """模拟数据库连接"""
    print("建立数据库连接")
    try:
        connection = "数据库连接对象"
        yield connection
    finally:
        print("关闭数据库连接")

with database_connection() as conn:
    print(f"使用{conn}执行操作")
```

### 实际应用示例
```python
import threading
from contextlib import contextmanager

@contextmanager
def lock_manager(lock):
    """锁管理器"""
    lock.acquire()
    try:
        yield
    finally:
        lock.release()

# 使用锁管理器
lock = threading.Lock()
with lock_manager(lock):
    # 执行需要同步的代码
    print("执行线程安全操作")
```

## 6. 迭代器和可迭代对象

### 可迭代对象
```python
class CountDown:
    """倒计时可迭代对象"""
    def __init__(self, start):
        self.start = start
    
    def __iter__(self):
        return CountDownIterator(self.start)

class CountDownIterator:
    """倒计时迭代器"""
    def __init__(self, start):
        self.current = start
    
    def __iter__(self):
        return self
    
    def __next__(self):
        if self.current <= 0:
            raise StopIteration
        self.current -= 1
        return self.current + 1

# 使用自定义可迭代对象
for num in CountDown(3):
    print(num)  # 3, 2, 1
```

### 生成器作为迭代器
```python
def count_up_to(maximum):
    """计数到最大值的生成器"""
    count = 1
    while count <= maximum:
        yield count
        count += 1

# 使用生成器
counter = count_up_to(5)
print(next(counter))  # 1
print(next(counter))  # 2
for num in counter:
    print(num)  # 3, 4, 5
```

## 7. 生成器表达式 vs 列表推导式

### 内存效率比较
```python
import sys

# 列表推导式 - 立即创建所有元素
list_comp = [x**2 for x in range(100000)]
print(f"列表推导式大小: {sys.getsizeof(list_comp)} 字节")

# 生成器表达式 - 按需生成元素
gen_exp = (x**2 for x in range(100000))
print(f"生成器表达式大小: {sys.getsizeof(gen_exp)} 字节")

# 性能比较
import time

# 列表推导式
start_time = time.time()
sum_squares_list = sum([x**2 for x in range(1000000)])
list_time = time.time() - start_time

# 生成器表达式
start_time = time.time()
sum_squares_gen = sum(x**2 for x in range(1000000))
gen_time = time.time() - start_time

print(f"列表推导式时间: {list_time:.4f}秒")
print(f"生成器表达式时间: {gen_time:.4f}秒")
```

## 8. 匿名函数 (Lambda Functions)

Lambda函数是简短的、一次性的函数。

### 基本用法
```python
# 基本lambda函数
square = lambda x: x * x
print(square(5))  # 25

# 在高阶函数中使用
numbers = [1, 2, 3, 4, 5]

# map函数
squared = list(map(lambda x: x**2, numbers))
print(squared)  # [1, 4, 9, 16, 25]

# filter函数
evens = list(filter(lambda x: x % 2 == 0, numbers))
print(evens)  # [2, 4]

# sorted函数
students = [("张三", 25), ("李四", 20), ("王五", 30)]
sorted_by_age = sorted(students, key=lambda x: x[1])
print(sorted_by_age)  # [('李四', 20), ('张三', 25), ('王五', 30)]
```

### 复杂lambda函数
```python
# 多参数lambda函数
add = lambda x, y: x + y
print(add(3, 5))  # 8

# 条件表达式
max_value = lambda x, y: x if x > y else y
print(max_value(10, 5))  # 10

# 嵌套lambda函数
compose = lambda f, g: lambda x: f(g(x))
add_one = lambda x: x + 1
multiply_two = lambda x: x * 2
composed = compose(multiply_two, add_one)
print(composed(5))  # 12
```

## 9. 函数式编程工具

### map, filter, reduce
```python
from functools import reduce

# map函数
numbers = [1, 2, 3, 4, 5]
squared = list(map(lambda x: x**2, numbers))
print(squared)  # [1, 4, 9, 16, 25]

# filter函数
evens = list(filter(lambda x: x % 2 == 0, numbers))
print(evens)  # [2, 4]

# reduce函数
sum_all = reduce(lambda x, y: x + y, numbers)
print(sum_all)  # 15

product = reduce(lambda x, y: x * y, numbers)
print(product)  # 120
```

### zip和enumerate
```python
# zip函数
names = ["张三", "李四", "王五"]
ages = [25, 30, 35]
name_age_pairs = list(zip(names, ages))
print(name_age_pairs)  # [('张三', 25), ('李四', 30), ('王五', 35)]

# 解压
name_list, age_list = zip(*name_age_pairs)
print(name_list)  # ('张三', '李四', '王五')
print(age_list)   # (25, 30, 35)

# enumerate函数
fruits = ["苹果", "香蕉", "橙子"]
for index, fruit in enumerate(fruits):
    print(f"{index}: {fruit}")
# 0: 苹果
# 1: 香蕉
# 2: 橙子
```

## 10. 类的特殊方法 (魔术方法)

### 基本特殊方法
```python
class Book:
    """书籍类"""
    def __init__(self, title, author, pages):
        self.title = title
        self.author = author
        self.pages = pages
    
    def __str__(self):
        """字符串表示"""
        return f"《{self.title}》 by {self.author}"
    
    def __repr__(self):
        """开发者字符串表示"""
        return f"Book('{self.title}', '{self.author}', {self.pages})"
    
    def __len__(self):
        """长度"""
        return self.pages
    
    def __eq__(self, other):
        """相等比较"""
        if isinstance(other, Book):
            return self.title == other.title and self.author == other.author
        return False
    
    def __lt__(self, other):
        """小于比较"""
        if isinstance(other, Book):
            return self.pages < other.pages
        return NotImplemented

# 使用特殊方法
book1 = Book("Python编程", "张三", 300)
book2 = Book("Java编程", "李四", 400)

print(str(book1))        # 《Python编程》 by 张三
print(repr(book1))       # Book('Python编程', '张三', 300)
print(len(book1))        # 300
print(book1 == book2)    # False
print(book1 < book2)     # True
```

### 容器类特殊方法
```python
class CustomList:
    """自定义列表类"""
    def __init__(self):
        self._items = []
    
    def __len__(self):
        return len(self._items)
    
    def __getitem__(self, index):
        return self._items[index]
    
    def __setitem__(self, index, value):
        self._items[index] = value
    
    def __delitem__(self, index):
        del self._items[index]
    
    def __iter__(self):
        return iter(self._items)
    
    def append(self, item):
        self._items.append(item)

# 使用自定义列表
custom_list = CustomList()
custom_list.append(1)
custom_list.append(2)
custom_list.append(3)

print(len(custom_list))      # 3
print(custom_list[0])        # 1
custom_list[0] = 10
print(custom_list[0])        # 10
for item in custom_list:
    print(item)              # 10, 2, 3
```

## 11. 属性管理

### property装饰器
```python
class Circle:
    """圆形类"""
    def __init__(self, radius):
        self._radius = radius
    
    @property
    def radius(self):
        """半径属性"""
        return self._radius
    
    @radius.setter
    def radius(self, value):
        """半径设置器"""
        if value < 0:
            raise ValueError("半径不能为负数")
        self._radius = value
    
    @radius.deleter
    def radius(self):
        """半径删除器"""
        print("删除半径")
        self._radius = 0
    
    @property
    def area(self):
        """面积属性（只读）"""
        return 3.14159 * self._radius ** 2
    
    @property
    def diameter(self):
        """直径属性"""
        return 2 * self._radius
    
    @diameter.setter
    def diameter(self, value):
        """通过直径设置半径"""
        self.radius = value / 2

# 使用属性管理
circle = Circle(5)
print(f"半径: {circle.radius}")      # 5
print(f"面积: {circle.area}")        # 78.53975
print(f"直径: {circle.diameter}")    # 10

circle.radius = 10
print(f"新半径: {circle.radius}")    # 10
print(f"新面积: {circle.area}")      # 314.159

circle.diameter = 30
print(f"通过直径设置的半径: {circle.radius}")  # 15
```

## 12. 元类 (Metaclasses)

元类是类的类，用于创建类。

### 基本元类
```python
class SingletonMeta(type):
    """单例元类"""
    _instances = {}
    
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

class Database(metaclass=SingletonMeta):
    """数据库连接类（单例）"""
    def __init__(self):
        self.connection = "数据库连接"
    
    def query(self, sql):
        return f"执行查询: {sql}"

# 测试单例
db1 = Database()
db2 = Database()
print(db1 is db2)  # True
```

### 属性验证元类
```python
class ValidatedMeta(type):
    """属性验证元类"""
    def __new__(cls, name, bases, attrs):
        # 为所有属性添加验证
        for key, value in list(attrs.items()):
            if not key.startswith('_') and callable(value):
                attrs[key] = cls._wrap_method(value)
        return super().__new__(cls, name, bases, attrs)
    
    @staticmethod
    def _wrap_method(method):
        def wrapper(self, *args, **kwargs):
            print(f"调用方法: {method.__name__}")
            return method(self, *args, **kwargs)
        return wrapper

class MyClass(metaclass=ValidatedMeta):
    def hello(self):
        return "Hello, World!"

# 使用带验证的类
obj = MyClass()
print(obj.hello())  # 调用方法: hello \n Hello, World!
```

## 13. 描述符 (Descriptors)

描述符实现了`__get__`、`__set__`、`__delete__`方法的类。

### 基本描述符
```python
class PositiveNumber:
    """正数描述符"""
    def __init__(self, name):
        self.name = name
    
    def __get__(self, instance, owner):
        if instance is None:
            return self
        return instance.__dict__.get(self.name, 0)
    
    def __set__(self, instance, value):
        if value < 0:
            raise ValueError(f"{self.name} 必须是正数")
        instance.__dict__[self.name] = value
    
    def __delete__(self, instance):
        del instance.__dict__[self.name]

class Product:
    """产品类"""
    price = PositiveNumber("price")
    quantity = PositiveNumber("quantity")
    
    def __init__(self, name, price, quantity):
        self.name = name
        self.price = price
        self.quantity = quantity
    
    @property
    def total_value(self):
        return self.price * self.quantity

# 使用描述符
product = Product("笔记本电脑", 5999, 10)
print(f"总价: {product.total_value}")  # 59990

# product.price = -100  # ValueError: price 必须是正数
```

## 14. 协程 (Coroutines)

协程是使用`async def`定义的函数，用于异步编程。

### 基本协程
```python
import asyncio

async def hello():
    """异步打招呼函数"""
    print("Hello")
    await asyncio.sleep(1)  # 模拟异步操作
    print("World")

async def main():
    """主协程"""
    await hello()

# 运行协程
# asyncio.run(main())
```

### 协程并发
```python
import asyncio
import time

async def fetch_data(name, delay):
    """模拟数据获取"""
    print(f"开始获取 {name} 的数据")
    await asyncio.sleep(delay)
    print(f"完成获取 {name} 的数据")
    return f"{name} 的数据"

async def main():
    """并发执行多个协程"""
    start_time = time.time()
    
    # 并发执行
    results = await asyncio.gather(
        fetch_data("任务1", 2),
        fetch_data("任务2", 1),
        fetch_data("任务3", 3)
    )
    
    end_time = time.time()
    print(f"所有任务完成，耗时: {end_time - start_time:.2f}秒")
    for result in results:
        print(result)

# asyncio.run(main())
```

## 15. 实际应用场景

### 数据处理管道
```python
def data_pipeline(data):
    """数据处理管道"""
    # 生成器处理大数据
    def read_data():
        for item in data:
            yield item
    
    def filter_data(data_gen):
        for item in data_gen:
            if item > 0:
                yield item
    
    def transform_data(data_gen):
        for item in data_gen:
            yield item * 2
    
    def aggregate_data(data_gen):
        total = 0
        count = 0
        for item in data_gen:
            total += item
            count += 1
        return total, count
    
    # 构建管道
    pipeline = aggregate_data(
        transform_data(
            filter_data(
                read_data()
            )
        )
    )
    return pipeline

# 使用数据管道
data = [-1, 2, -3, 4, 5, -6, 7, 8]
total, count = data_pipeline(data)
print(f"总和: {total}, 数量: {count}")  # 总和: 36, 数量: 5
```

### 缓存装饰器
```python
from functools import wraps
import time

def lru_cache(maxsize=128):
    """LRU缓存装饰器"""
    def decorator(func):
        cache = {}
        access_times = {}
        
        @wraps(func)
        def wrapper(*args, **kwargs):
            key = str(args) + str(sorted(kwargs.items()))
            current_time = time.time()
            
            # 检查缓存
            if key in cache:
                access_times[key] = current_time
                return cache[key]
            
            # 计算结果
            result = func(*args, **kwargs)
            
            # 管理缓存大小
            if len(cache) >= maxsize:
                # 删除最久未使用的项
                oldest_key = min(access_times, key=access_times.get)
                del cache[oldest_key]
                del access_times[oldest_key]
            
            # 添加到缓存
            cache[key] = result
            access_times[key] = current_time
            
            return result
        return wrapper
    return decorator

@lru_cache(maxsize=3)
def expensive_function(n):
    """耗时函数"""
    time.sleep(0.1)  # 模拟耗时操作
    return n * n

# 测试缓存
print(expensive_function(5))  # 计算并缓存
print(expensive_function(5))  # 从缓存获取
print(expensive_function(3))  # 计算并缓存
print(expensive_function(4))  # 计算并缓存
print(expensive_function(5))  # 从缓存获取
```

## 16. 最佳实践

### 选择合适的特性
```python
# 好的做法：根据需求选择
# 处理大量数据时使用生成器
def process_large_dataset(filename):
    with open(filename, 'r') as file:
        for line in file:  # 逐行处理，节省内存
            yield process_line(line)

# 简单数据转换使用列表推导式
numbers = [1, 2, 3, 4, 5]
squares = [x**2 for x in numbers if x % 2 == 0]

# 复杂逻辑使用普通函数
def complex_calculation(data):
    # 复杂的计算逻辑
    pass
```

### 保持代码可读性
```python
# 好的做法：保持简洁
# 简单的lambda函数
numbers = [1, 2, 3, 4, 5]
evens = list(filter(lambda x: x % 2 == 0, numbers))

# 复杂逻辑使用命名函数
def is_valid_user(user):
    return user.is_active and user.has_permission and user.email_verified

valid_users = list(filter(is_valid_user, users))
```

### 注意性能影响
```python
# 性能考虑
import time

# 列表推导式 vs 循环
def list_comprehension_test():
    return [x**2 for x in range(100000)]

def loop_test():
    result = []
    for x in range(100000):
        result.append(x**2)
    return result

# 测试性能
start = time.time()
list_comprehension_test()
print(f"列表推导式时间: {time.time() - start:.4f}秒")

start = time.time()
loop_test()
print(f"循环时间: {time.time() - start:.4f}秒")
```