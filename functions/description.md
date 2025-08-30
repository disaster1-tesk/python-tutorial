# Python函数知识点

## 1. 函数定义

函数是组织好的、可重复使用的、用来实现单一或相关联功能的代码块。

### 基本语法
```python
def function_name(parameters):
    """文档字符串"""
    statement
    return value
```

### 使用示例
```python
# 无参函数
def greet():
    """打招呼函数"""
    print("Hello, World!")

# 有参函数
def greet_person(name):
    """向指定人员打招呼"""
    print(f"Hello, {name}!")

# 带返回值的函数
def add(a, b):
    """计算两个数的和"""
    return a + b

# 调用函数
greet()
greet_person("Alice")
result = add(3, 5)
print(f"3 + 5 = {result}")
```

### 实际应用场景
- 封装可重用的代码逻辑
- 提高代码的模块化程度
- 便于测试和维护

## 2. 参数类型

### 位置参数
按照位置顺序传递的参数。

```python
def introduce(name, age, city):
    """自我介绍"""
    print(f"我叫{name}，今年{age}岁，来自{city}")

# 按位置传递参数
introduce("张三", 25, "北京")
# introduce("李四", 30)  # 错误：缺少参数
```

### 默认参数
为参数设置默认值，调用时可以不传入该参数。

```python
def introduce(name, age=20, city="北京"):
    """自我介绍（带默认值）"""
    print(f"我叫{name}，今年{age}岁，来自{city}")

# 使用默认值
introduce("张三")           # 我叫张三，今年20岁，来自北京
introduce("李四", 25)       # 我叫李四，今年25岁，来自北京
introduce("王五", 30, "上海") # 我叫王五，今年30岁，来自上海

# 使用关键字参数
introduce(name="赵六", city="广州")  # 我叫赵六，今年20岁，来自广州
```

### 关键字参数
通过参数名指定参数值。

```python
def create_profile(name, age, email, phone=None):
    """创建用户档案"""
    profile = {
        "name": name,
        "age": age,
        "email": email
    }
    if phone:
        profile["phone"] = phone
    return profile

# 使用关键字参数（可以不按顺序）
profile = create_profile(
    email="alice@example.com",
    name="Alice",
    age=25,
    phone="13800138000"
)
print(profile)
```

### 可变参数
- `*args`：用于接收任意数量的位置参数
- `**kwargs`：用于接收任意数量的关键字参数

```python
def sum_all(*args):
    """计算所有参数的和"""
    total = 0
    for num in args:
        total += num
    return total

def print_info(**kwargs):
    """打印个人信息"""
    for key, value in kwargs.items():
        print(f"{key}: {value}")

# 使用可变位置参数
print(sum_all(1, 2, 3, 4, 5))  # 15

# 使用可变关键字参数
print_info(name="张三", age=25, job="程序员")

# 组合使用
def flexible_function(required_param, *args, **kwargs):
    """灵活参数函数示例"""
    print(f"必需参数: {required_param}")
    print(f"位置参数: {args}")
    print(f"关键字参数: {kwargs}")

flexible_function("必需", 1, 2, 3, name="张三", age=25)
```

### 参数解包
```python
def greet(first_name, last_name):
    """问候函数"""
    print(f"Hello, {first_name} {last_name}!")

# 列表解包
name_list = ["张", "三"]
greet(*name_list)  # Hello, 张 三!

# 字典解包
name_dict = {"first_name": "李", "last_name": "四"}
greet(**name_dict)  # Hello, 李 四!
```

## 3. 作用域

### 局部作用域
在函数内部定义的变量只能在函数内部访问。

```python
def test_local_scope():
    local_var = "我是局部变量"
    print(local_var)  # 可以访问

test_local_scope()
# print(local_var)  # 错误：无法在函数外访问
```

### 全局作用域
在函数外部定义的变量可以在整个模块中访问。

```python
global_var = "我是全局变量"

def test_global_scope():
    print(global_var)  # 可以访问全局变量

test_global_scope()
print(global_var)  # 也可以在函数外访问
```

### global关键字
在函数内部修改全局变量。

```python
counter = 0

def increment():
    global counter
    counter += 1
    print(f"计数器: {counter}")

increment()  # 计数器: 1
increment()  # 计数器: 2
print(f"全局计数器: {counter}")  # 全局计数器: 2
```

### nonlocal关键字
在嵌套函数中修改外层函数的变量。

```python
def outer_function(x):
    """外层函数"""
    def inner_function(y):
        """内层函数"""
        nonlocal x
        x += y
        return x
    return inner_function

add_five = outer_function(5)
print(add_five(3))  # 8
print(add_five(2))  # 10
```

## 4. 匿名函数

使用lambda关键字创建匿名函数。

### 基本语法
```python
lambda parameters: expression
```

### 使用示例
```python
# 基本lambda函数
square = lambda x: x * x
print(square(5))  # 25

# 在高阶函数中使用
numbers = [1, 2, 3, 4, 5]
squared = list(map(lambda x: x**2, numbers))
print(squared)  # [1, 4, 9, 16, 25]

# 过滤操作
even_numbers = list(filter(lambda x: x % 2 == 0, numbers))
print(even_numbers)  # [2, 4]

# 排序操作
students = [("张三", 25), ("李四", 20), ("王五", 30)]
# 按年龄排序
sorted_students = sorted(students, key=lambda x: x[1])
print(sorted_students)  # [('李四', 20), ('张三', 25), ('王五', 30)]
```

## 5. 文档字符串

在函数定义后的三引号字符串称为文档字符串(docstring)。

### 格式规范
```python
def calculate_area(radius):
    """
    计算圆的面积
    
    Args:
        radius (float): 圆的半径
        
    Returns:
        float: 圆的面积
        
    Raises:
        ValueError: 当半径为负数时抛出
        
    Example:
        >>> calculate_area(5)
        78.53975
    """
    if radius < 0:
        raise ValueError("半径不能为负数")
    return 3.14159 * radius ** 2
```

### 访问文档字符串
```python
def greet(name):
    """向指定人员打招呼"""
    print(f"Hello, {name}!")

print(greet.__doc__)  # 向指定人员打招呼
help(greet)  # 显示详细帮助信息
```

## 6. 高级特性

### 递归
函数调用自身。

```python
def factorial(n):
    """计算阶乘（递归实现）"""
    if n <= 1:
        return 1
    else:
        return n * factorial(n - 1)

def fibonacci(n):
    """计算斐波那契数列（递归实现）"""
    if n <= 1:
        return n
    else:
        return fibonacci(n-1) + fibonacci(n-2)

# 使用示例
print(f"5! = {factorial(5)}")  # 5! = 120
print(f"斐波那契数列第10项: {fibonacci(10)}")  # 55
```

### 装饰器
用于修改函数行为的高级技术。

```python
def timer_decorator(func):
    """计时装饰器"""
    import time
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"{func.__name__} 执行时间: {end_time - start_time:.4f}秒")
        return result
    return wrapper

def log_decorator(func):
    """日志装饰器"""
    def wrapper(*args, **kwargs):
        print(f"调用函数 {func.__name__}")
        result = func(*args, **kwargs)
        print(f"函数 {func.__name__} 执行完成")
        return result
    return wrapper

# 使用装饰器
@timer_decorator
@log_decorator
def slow_function():
    """慢速函数示例"""
    import time
    time.sleep(1)
    return "完成"

# 调用函数
result = slow_function()
```

### 闭包
内部函数可以访问外部函数的变量。

```python
def create_multiplier(n):
    """创建乘法器"""
    def multiplier(x):
        return x * n
    return multiplier

# 创建不同的乘法器
double = create_multiplier(2)
triple = create_multiplier(3)

print(double(5))   # 10
print(triple(5))   # 15

# 计数器闭包
def create_counter():
    """创建计数器"""
    count = 0
    def counter():
        nonlocal count
        count += 1
        return count
    return counter

counter1 = create_counter()
counter2 = create_counter()

print(counter1())  # 1
print(counter1())  # 2
print(counter2())  # 1
```

## 7. 函数式编程特性

### 高阶函数
接受函数作为参数或返回函数的函数。

```python
def apply_operation(numbers, operation):
    """对数字列表应用操作"""
    return [operation(x) for x in numbers]

def square(x):
    return x ** 2

def cube(x):
    return x ** 3

numbers = [1, 2, 3, 4, 5]
squared = apply_operation(numbers, square)
cubed = apply_operation(numbers, cube)
print(f"平方: {squared}")  # [1, 4, 9, 16, 25]
print(f"立方: {cubed}")    # [1, 8, 27, 64, 125]
```

### 纯函数
相同输入总是产生相同输出，没有副作用。

```python
# 纯函数示例
def add(a, b):
    """纯函数：加法"""
    return a + b

def calculate_tax(amount, rate):
    """纯函数：计算税额"""
    return amount * rate

# 非纯函数示例
counter = 0
def increment_counter():
    """非纯函数：修改全局状态"""
    global counter
    counter += 1
    return counter
```

## 8. 实际应用场景

### API设计和封装
```python
def validate_email(email):
    """验证邮箱格式"""
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def send_email(to, subject, body, cc=None, bcc=None):
    """
    发送邮件
    
    Args:
        to (str or list): 收件人
        subject (str): 邮件主题
        body (str): 邮件正文
        cc (list, optional): 抄送列表
        bcc (list, optional): 密送列表
    """
    if isinstance(to, str):
        to = [to]
    
    # 验证邮箱格式
    all_recipients = to + (cc or []) + (bcc or [])
    for email in all_recipients:
        if not validate_email(email):
            raise ValueError(f"无效的邮箱地址: {email}")
    
    # 模拟发送邮件
    print(f"发送邮件给: {', '.join(to)}")
    print(f"主题: {subject}")
    print(f"正文: {body}")
    if cc:
        print(f"抄送: {', '.join(cc)}")
    if bcc:
        print(f"密送: {', '.join(bcc)}")

# 使用示例
send_email(
    to="user@example.com",
    subject="测试邮件",
    body="这是一封测试邮件",
    cc=["manager@example.com"]
)
```

### 数据处理和转换
```python
def process_sales_data(sales_records):
    """处理销售数据"""
    def calculate_commission(sale):
        """计算佣金"""
        return sale['amount'] * 0.1 if sale['amount'] > 1000 else 0
    
    def format_record(sale):
        """格式化记录"""
        return {
            'id': sale['id'],
            'salesperson': sale['salesperson'],
            'amount': sale['amount'],
            'commission': calculate_commission(sale)
        }
    
    # 处理所有记录
    processed_records = [format_record(record) for record in sales_records]
    
    # 计算总佣金
    total_commission = sum(record['commission'] for record in processed_records)
    
    return {
        'records': processed_records,
        'total_commission': total_commission
    }

# 使用示例
sales_data = [
    {'id': 1, 'salesperson': '张三', 'amount': 1500},
    {'id': 2, 'salesperson': '李四', 'amount': 800},
    {'id': 3, 'salesperson': '王五', 'amount': 2000}
]

result = process_sales_data(sales_data)
print(f"总佣金: {result['total_commission']}")
for record in result['records']:
    print(f"{record['salesperson']}: 佣金 {record['commission']}")
```

## 9. 最佳实践

### 函数应该短小精悍，只做一件事
```python
# 不好的做法
def process_user_data(name, age, email):
    # 验证数据
    if not name or not email:
        raise ValueError("姓名和邮箱不能为空")
    if age < 0 or age > 150:
        raise ValueError("年龄必须在0-150之间")
    
    # 格式化数据
    formatted_name = name.strip().title()
    formatted_email = email.strip().lower()
    
    # 保存到数据库
    # db.save_user(formatted_name, age, formatted_email)
    
    # 发送欢迎邮件
    # send_welcome_email(formatted_email)
    
    return {"name": formatted_name, "age": age, "email": formatted_email}

# 改进：拆分为多个小函数
def validate_user_data(name, age, email):
    """验证用户数据"""
    if not name or not email:
        raise ValueError("姓名和邮箱不能为空")
    if age < 0 or age > 150:
        raise ValueError("年龄必须在0-150之间")

def format_user_data(name, age, email):
    """格式化用户数据"""
    return {
        "name": name.strip().title(),
        "age": age,
        "email": email.strip().lower()
    }

def save_user_to_database(user_data):
    """保存用户到数据库"""
    # db.save_user(**user_data)
    pass

def send_welcome_email(email):
    """发送欢迎邮件"""
    # send_email(email, "欢迎加入", "欢迎使用我们的服务")
    pass

def create_user(name, age, email):
    """创建用户"""
    validate_user_data(name, age, email)
    user_data = format_user_data(name, age, email)
    save_user_to_database(user_data)
    send_welcome_email(user_data["email"])
    return user_data
```

### 使用有意义的函数名和参数名
```python
# 不清晰的命名
def calc(x, y, z):
    return x * y * z

# 清晰的命名
def calculate_volume(length, width, height):
    """计算长方体体积"""
    return length * width * height
```

### 合理使用参数默认值
```python
# 好的做法
def create_connection(host, port=3306, timeout=30):
    """创建数据库连接"""
    # 连接逻辑
    pass

# 避免可变对象作为默认值
# 不好的做法
def add_item(item, target_list=[]):  # 危险！
    target_list.append(item)
    return target_list

# 改进
def add_item(item, target_list=None):
    """添加项目到列表"""
    if target_list is None:
        target_list = []
    target_list.append(item)
    return target_list
```

### 添加适当的文档字符串
```python
def binary_search(arr, target):
    """
    在有序数组中使用二分查找算法查找目标值
    
    时间复杂度: O(log n)
    空间复杂度: O(1)
    
    Args:
        arr (list): 有序数组
        target: 要查找的目标值
        
    Returns:
        int: 目标值的索引，如果未找到返回-1
        
    Example:
        >>> binary_search([1, 3, 5, 7, 9], 5)
        2
        >>> binary_search([1, 3, 5, 7, 9], 4)
        -1
    """
    left, right = 0, len(arr) - 1
    
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    
    return -1
```