# Python异常处理知识点

## 1. 异常的概念

异常是程序执行过程中发生的错误或异常情况，它会中断正常的程序执行流程。

### 异常的特点
- **中断性**：异常会中断当前的执行流程
- **可捕获性**：可以通过try-except语句捕获和处理
- **传递性**：如果不处理，异常会向上传递
- **信息性**：异常包含详细的错误信息

### 异常处理的重要性
```python
# 不处理异常的代码
def divide_numbers(a, b):
    return a / b

# 这会导致程序崩溃
# result = divide_numbers(10, 0)  # ZeroDivisionError

# 处理异常的代码
def safe_divide(a, b):
    try:
        return a / b
    except ZeroDivisionError:
        print("错误：除数不能为零")
        return None

result = safe_divide(10, 0)  # 错误：除数不能为零
print(result)  # None
```

## 2. 常见的内置异常类型

Python提供了丰富的内置异常类型，用于处理各种错误情况。

### 基础异常类型
```python
# Exception: 所有异常的基类
try:
    raise Exception("这是一个异常")
except Exception as e:
    print(f"捕获到异常: {e}")

# ValueError: 传入无效值时引发
try:
    number = int("abc")
except ValueError as e:
    print(f"值错误: {e}")  # invalid literal for int() with base 10: 'abc'

# TypeError: 类型错误
try:
    result = "hello" + 5
except TypeError as e:
    print(f"类型错误: {e}")  # can only concatenate str (not "int") to str

# IndexError: 序列索引超出范围
try:
    my_list = [1, 2, 3]
    print(my_list[5])
except IndexError as e:
    print(f"索引错误: {e}")  # list index out of range

# KeyError: 字典键不存在
try:
    my_dict = {"name": "Alice"}
    print(my_dict["age"])
except KeyError as e:
    print(f"键错误: {e}")  # 'age'
```

### 文件相关异常
```python
# FileNotFoundError: 文件未找到
try:
    with open("nonexistent.txt", "r") as file:
        content = file.read()
except FileNotFoundError as e:
    print(f"文件未找到: {e}")

# IOError: 输入输出错误
try:
    with open("/root/protected_file.txt", "w") as file:
        file.write("内容")
except IOError as e:
    print(f"IO错误: {e}")
```

### 数学运算异常
```python
# ZeroDivisionError: 除零错误
try:
    result = 10 / 0
except ZeroDivisionError as e:
    print(f"除零错误: {e}")

# OverflowError: 数值运算结果超出范围
try:
    import math
    result = math.exp(1000)
except OverflowError as e:
    print(f"溢出错误: {e}")
```

## 3. try-except语句

try-except语句用于捕获和处理异常。

### 基本语法
```python
try:
    # 可能引发异常的代码
    statement
except ExceptionType:
    # 处理特定类型的异常
    statement
except ExceptionType as e:
    # 处理异常并获取异常对象
    statement
else:
    # 没有异常时执行
    statement
finally:
    # 无论是否有异常都会执行
    statement
```

### 使用示例
```python
# 基本try-except
try:
    number = int(input("请输入一个数字: "))
    result = 10 / number
    print(f"结果是: {result}")
except ValueError:
    print("输入的不是有效数字！")
except ZeroDivisionError:
    print("不能除以零！")

# 捕获多个异常
try:
    # 一些可能出错的操作
    pass
except (ValueError, TypeError, IndexError) as e:
    print(f"发生了预期的错误: {e}")

# 捕获所有异常
try:
    # 一些操作
    pass
except Exception as e:
    print(f"发生了未预期的错误: {e}")
    # 通常不推荐这样做，应该具体处理特定异常

# else子句
try:
    file = open("example.txt", "r")
    content = file.read()
except FileNotFoundError:
    print("文件未找到！")
else:
    print("文件读取成功")
    print(content)
finally:
    try:
        file.close()
        print("文件已关闭")
    except:
        print("文件未打开或已关闭")
```

## 4. raise语句

raise语句用于主动抛出异常。

### 基本用法
```python
# 抛出内置异常
def validate_age(age):
    if age < 0:
        raise ValueError("年龄不能为负数")
    if age > 150:
        raise ValueError("年龄不能超过150岁")
    return True

try:
    validate_age(-5)
except ValueError as e:
    print(f"验证失败: {e}")

# 抛出异常并保留原始异常信息
def process_data(data):
    try:
        # 一些处理
        result = 10 / data
    except ZeroDivisionError as e:
        raise ValueError("数据处理失败") from e

try:
    process_data(0)
except ValueError as e:
    print(f"捕获到异常: {e}")
    print(f"原始异常: {e.__cause__}")
```

## 5. 自定义异常

通过继承Exception类创建自定义异常。

### 基本语法
```python
class CustomError(Exception):
    """自定义异常类"""
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

# 使用自定义异常
def check_score(score):
    if score < 0 or score > 100:
        raise CustomError(f"分数 {score} 超出有效范围(0-100)")

try:
    check_score(150)
except CustomError as e:
    print(f"自定义异常: {e.message}")
```

### 复杂的自定义异常
```python
class ValidationError(Exception):
    """验证错误异常"""
    def __init__(self, field, value, message):
        self.field = field
        self.value = value
        self.message = message
        super().__init__(f"{field}字段验证失败: {message} (值: {value})")
    
    def to_dict(self):
        """转换为字典格式"""
        return {
            "field": self.field,
            "value": self.value,
            "message": self.message
        }

class BusinessLogicError(Exception):
    """业务逻辑错误"""
    def __init__(self, operation, reason):
        self.operation = operation
        self.reason = reason
        super().__init__(f"业务操作'{operation}'失败: {reason}")

# 使用复杂自定义异常
def validate_user_data(user_data):
    if not user_data.get("email"):
        raise ValidationError("email", user_data.get("email"), "邮箱不能为空")
    
    if "@" not in user_data["email"]:
        raise ValidationError("email", user_data["email"], "邮箱格式不正确")

def create_user(user_data):
    try:
        validate_user_data(user_data)
        # 创建用户的业务逻辑
        print("用户创建成功")
    except ValidationError as e:
        raise BusinessLogicError("创建用户", str(e)) from e

# 测试
try:
    create_user({"name": "张三"})
except BusinessLogicError as e:
    print(f"业务错误: {e}")
    print(f"操作: {e.operation}")
    print(f"原因: {e.reason}")
```

## 6. 异常链和上下文

使用raise...from语法可以链接异常，保留原始异常信息。

### 异常链
```python
def low_level_function():
    """底层函数"""
    raise ValueError("底层错误")

def mid_level_function():
    """中层函数"""
    try:
        low_level_function()
    except ValueError as e:
        # 重新抛出异常，保留原始异常信息
        raise RuntimeError("中层处理失败") from e

def high_level_function():
    """高层函数"""
    try:
        mid_level_function()
    except RuntimeError as e:
        # 再次重新抛出异常
        raise BusinessLogicError("高层业务处理", str(e)) from e

# 测试异常链
try:
    high_level_function()
except BusinessLogicError as e:
    print(f"捕获到异常: {e}")
    print(f"直接原因: {e.__cause__}")
    print(f"根本原因: {e.__cause__.__cause__}")
```

## 7. 上下文管理器和with语句

实现__enter__和__exit__方法的类可以作为上下文管理器。

### 自定义上下文管理器
```python
class DatabaseConnection:
    """数据库连接上下文管理器"""
    
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.connection = None
    
    def __enter__(self):
        print(f"连接到数据库 {self.host}:{self.port}")
        # 模拟建立连接
        self.connection = f"连接到{self.host}"
        return self.connection
    
    def __exit__(self, exc_type, exc_value, traceback):
        print("关闭数据库连接")
        self.connection = None
        # 如果有异常，可以选择是否抑制
        if exc_type:
            print(f"发生异常: {exc_type.__name__}: {exc_value}")
        return False  # 不抑制异常

# 使用自定义上下文管理器
try:
    with DatabaseConnection("localhost", 5432) as conn:
        print(f"使用连接: {conn}")
        # 模拟数据库操作
        raise ValueError("数据库操作失败")
except ValueError as e:
    print(f"捕获到异常: {e}")
```

### 使用contextlib模块
```python
from contextlib import contextmanager
import time

@contextmanager
def timer():
    """计时上下文管理器"""
    start_time = time.time()
    try:
        yield
    finally:
        end_time = time.time()
        print(f"执行时间: {end_time - start_time:.4f}秒")

@contextmanager
def temporary_file(filename):
    """临时文件上下文管理器"""
    print(f"创建临时文件: {filename}")
    try:
        yield filename
    finally:
        print(f"删除临时文件: {filename}")

# 使用上下文管理器
with timer():
    time.sleep(1)
    print("执行一些操作")

with temporary_file("temp.txt") as filename:
    print(f"处理文件: {filename}")
```

## 8. 实际应用场景

### 文件操作异常处理
```python
import json
import os

def read_config_file(filename):
    """读取配置文件"""
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            config = json.load(file)
        return config
    except FileNotFoundError:
        print(f"配置文件 {filename} 不存在，使用默认配置")
        return {}
    except json.JSONDecodeError as e:
        print(f"配置文件格式错误: {e}")
        return {}
    except PermissionError:
        print(f"没有权限读取文件 {filename}")
        return {}
    except Exception as e:
        print(f"读取配置文件时发生未知错误: {e}")
        return {}

def write_config_file(filename, config):
    """写入配置文件"""
    try:
        # 确保目录存在
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        
        with open(filename, 'w', encoding='utf-8') as file:
            json.dump(config, file, indent=2, ensure_ascii=False)
        print(f"配置已保存到 {filename}")
    except PermissionError:
        print(f"没有权限写入文件 {filename}")
    except OSError as e:
        print(f"文件系统错误: {e}")
    except Exception as e:
        print(f"保存配置文件时发生未知错误: {e}")

# 使用示例
config = read_config_file("config/app.json")
config["debug"] = True
write_config_file("config/app.json", config)
```

### 网络请求异常处理
```python
import requests
from time import sleep

def fetch_data_with_retry(url, max_retries=3):
    """带重试机制的数据获取"""
    for attempt in range(max_retries):
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()  # 检查HTTP错误
            return response.json()
        except requests.exceptions.Timeout:
            print(f"请求超时 (尝试 {attempt + 1}/{max_retries})")
        except requests.exceptions.ConnectionError:
            print(f"连接错误 (尝试 {attempt + 1}/{max_retries})")
        except requests.exceptions.HTTPError as e:
            print(f"HTTP错误: {e}")
            break  # HTTP错误通常不需要重试
        except requests.exceptions.RequestException as e:
            print(f"请求异常: {e}")
        except json.JSONDecodeError:
            print("响应不是有效的JSON格式")
            break  # 格式错误通常不需要重试
        
        if attempt < max_retries - 1:
            wait_time = 2 ** attempt  # 指数退避
            print(f"等待 {wait_time} 秒后重试...")
            sleep(wait_time)
    
    return None

# 使用示例
# data = fetch_data_with_retry("https://api.example.com/data")
```

## 9. 最佳实践

### 只捕获可以处理的异常
```python
# 好的做法
def process_user_input(user_input):
    try:
        number = int(user_input)
        return number * 2
    except ValueError:
        # 我们知道如何处理这种错误
        print("请输入有效的数字")
        return None

# 避免捕获所有异常
def bad_example():
    try:
        # 一些操作
        pass
    except Exception:  # 不好的做法
        pass  # 忽略所有异常

# 更好的做法
def good_example():
    try:
        # 一些操作
        pass
    except (ValueError, TypeError):  # 具体的异常类型
        # 处理特定的预期错误
        pass
    except Exception as e:
        # 记录未预期的错误，然后重新抛出
        print(f"未预期的错误: {e}")
        raise
```

### 记录异常信息
```python
import logging

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def divide_with_logging(a, b):
    """带日志记录的除法运算"""
    try:
        result = a / b
        logger.info(f"成功计算 {a} / {b} = {result}")
        return result
    except ZeroDivisionError as e:
        logger.error(f"除零错误: 尝试计算 {a} / {b}", exc_info=True)
        raise
    except TypeError as e:
        logger.error(f"类型错误: 尝试计算 {a} / {b}", exc_info=True)
        raise

# 使用示例
try:
    divide_with_logging(10, 0)
except ZeroDivisionError:
    print("处理除零错误")
```

### 清理资源
```python
# 使用with语句确保资源清理
def process_file(filename):
    """处理文件"""
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            data = file.read()
            # 处理数据
            processed_data = data.upper()
        
        # 文件会自动关闭
        with open(f"processed_{filename}", 'w', encoding='utf-8') as file:
            file.write(processed_data)
            
        print("文件处理完成")
    except FileNotFoundError:
        print(f"文件 {filename} 不存在")
    except PermissionError:
        print(f"没有权限访问文件 {filename}")
    except Exception as e:
        print(f"处理文件时发生错误: {e}")
```

### 提供有意义的错误信息
```python
class InsufficientFundsError(Exception):
    """余额不足异常"""
    def __init__(self, balance, amount):
        self.balance = balance
        self.amount = amount
        super().__init__(
            f"余额不足: 当前余额 {balance}, 尝试提取 {amount}"
        )

class BankAccount:
    def __init__(self, account_number, initial_balance=0):
        self.account_number = account_number
        self.balance = initial_balance
    
    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("提取金额必须大于0")
        
        if amount > self.balance:
            raise InsufficientFundsError(self.balance, amount)
        
        self.balance -= amount
        return self.balance

# 使用示例
account = BankAccount("123456", 1000)
try:
    account.withdraw(1500)
except InsufficientFundsError as e:
    print(f"错误: {e}")
    print(f"当前余额: {e.balance}")
    print(f"尝试提取: {e.amount}")
```