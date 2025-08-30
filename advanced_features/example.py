# Python高级特性示例

print("=== 1. 列表推导式 ===")
# 基本列表推导式
squares = [x**2 for x in range(10)]
print(f"0-9的平方: {squares}")

# 带条件的列表推导式
even_squares = [x**2 for x in range(10) if x % 2 == 0]
print(f"0-9中偶数的平方: {even_squares}")

# 嵌套列表推导式
matrix = [[i*3 + j for j in range(1, 4)] for i in range(3)]
print(f"3x3矩阵: {matrix}")

print("\n=== 2. 字典和集合推导式 ===")
# 字典推导式
square_dict = {x: x**2 for x in range(5)}
print(f"数字和平方的字典: {square_dict}")

# 集合推导式
unique_lengths = {len(word) for word in ["apple", "banana", "cherry", "date"]}
print(f"单词长度集合: {unique_lengths}")

print("\n=== 3. 生成器 ===")
# 生成器函数
def countdown(n):
    while n > 0:
        yield n
        n -= 1

# 使用生成器
print("倒计时生成器:")
for num in countdown(5):
    print(num)

# 生成器表达式
even_numbers = (x for x in range(10) if x % 2 == 0)
print(f"偶数生成器: {list(even_numbers)}")

print("\n=== 4. 装饰器 ===")
# 基本装饰器
def my_decorator(func):
    def wrapper(*args, **kwargs):
        print("函数调用前")
        result = func(*args, **kwargs)
        print("函数调用后")
        return result
    return wrapper

@my_decorator
def say_hello(name):
    print(f"你好, {name}!")

say_hello("张三")

# 带参数的装饰器
def repeat(times):
    def decorator(func):
        def wrapper(*args, **kwargs):
            for _ in range(times):
                result = func(*args, **kwargs)
            return result
        return wrapper
    return decorator

@repeat(3)
def greet():
    print("欢迎!")

greet()

print("\n=== 5. 上下文管理器 ===")
# 使用类实现上下文管理器
class MyContextManager:
    def __enter__(self):
        print("进入上下文")
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        print("退出上下文")
        if exc_type:
            print(f"异常类型: {exc_type}")
        return False

with MyContextManager() as cm:
    print("在上下文内部")

# 使用contextlib模块
from contextlib import contextmanager

@contextmanager
def my_context():
    print("上下文开始")
    try:
        yield "资源"
    finally:
        print("上下文结束")

with my_context() as resource:
    print(f"使用{resource}")

print("\n=== 6. 迭代器和可迭代对象 ===")
class CountDown:
    def __init__(self, start):
        self.start = start
    
    def __iter__(self):
        return self
    
    def __next__(self):
        if self.start <= 0:
            raise StopIteration
        self.start -= 1
        return self.start + 1

print("自定义迭代器:")
for num in CountDown(3):
    print(num)

print("\n=== 7. 函数式编程工具 ===")
numbers = [1, 2, 3, 4, 5]

# map函数
squared = list(map(lambda x: x**2, numbers))
print(f"平方: {squared}")

# filter函数
evens = list(filter(lambda x: x % 2 == 0, numbers))
print(f"偶数: {evens}")

# zip函数
names = ["张三", "李四", "王五"]
ages = [25, 30, 35]
name_age_pairs = list(zip(names, ages))
print(f"姓名年龄对: {name_age_pairs}")

print("\n=== 8. 类的特殊方法 ===")
class Book:
    def __init__(self, title, author):
        self.title = title
        self.author = author
    
    def __str__(self):
        return f"《{self.title}》 by {self.author}"
    
    def __repr__(self):
        return f"Book('{self.title}', '{self.author}')"
    
    def __len__(self):
        return len(self.title)

book = Book("Python编程", "张三")
print(f"str(): {str(book)}")
print(f"repr(): {repr(book)}")
print(f"len(): {len(book)}")

print("\n=== 9. 属性管理 ===")
class Circle:
    def __init__(self, radius):
        self._radius = radius
    
    @property
    def radius(self):
        return self._radius
    
    @radius.setter
    def radius(self, value):
        if value < 0:
            raise ValueError("半径不能为负数")
        self._radius = value
    
    @property
    def area(self):
        return 3.14159 * self._radius ** 2

circle = Circle(5)
print(f"半径: {circle.radius}")
print(f"面积: {circle.area}")
circle.radius = 10
print(f"新半径: {circle.radius}")
print(f"新面积: {circle.area}")

print("\n=== 10. 其他高级特性 ===")
# 使用enumerate
fruits = ["苹果", "香蕉", "橙子"]
print("使用enumerate:")
for index, fruit in enumerate(fruits, 1):
    print(f"{index}. {fruit}")

# 使用unpacking
point = (3, 4)
x, y = point
print(f"解包点坐标: x={x}, y={y}")

# 使用*args和**kwargs
def demo_args_kwargs(*args, **kwargs):
    print(f"位置参数: {args}")
    print(f"关键字参数: {kwargs}")

demo_args_kwargs(1, 2, 3, name="张三", age=25)