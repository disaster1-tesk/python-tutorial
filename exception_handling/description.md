# Python异常处理知识点

## 1. 异常的概念和类型

### 知识点解析

**概念定义**：异常就像程序运行过程中遇到的"意外情况"，比如我们想把字符串"abc"转换成数字就会出错，或者想除以0这样的非法操作。异常处理就是教程序如何优雅地应对这些意外，而不是直接崩溃。

**核心规则**：
1. 异常会中断程序的正常执行流程
2. 可以通过try-except语句捕获和处理异常
3. 如果不处理异常，程序会终止并显示错误信息
4. Python提供了丰富的内置异常类型处理各种错误情况

**常见易错点**：
1. 忘记处理可能出错的代码，导致程序意外终止
2. 捕获过于宽泛的异常（如except Exception），难以定位具体问题
3. 在异常处理中再次引发新的异常
4. 忽略异常后的资源清理工作

### 实战案例

#### 案例1：学生成绩管理系统
```python
# 学生成绩管理系统
print("===学生成绩管理系统===")

# 定义自定义异常
class InvalidScoreError(Exception):
    """无效成绩异常"""
    def __init__(self, score, message="成绩无效"):
        self.score = score
        self.message = f"{message}: {score}。成绩应在0-100之间。"
        super().__init__(self.message)

class StudentNotFoundError(Exception):
    """学生未找到异常"""
    def __init__(self, student_name):
        self.student_name = student_name
        self.message = f"未找到学生: {student_name}"
        super().__init__(self.message)

# 学生成绩管理类
class GradeManager:
    """学生成绩管理器"""
    
    def __init__(self):
        self.students = {}  # 存储学生信息
    
    def add_student(self, name):
        """
        添加学生
        
        参数:
            name (str): 学生姓名
        """
        if not isinstance(name, str) or not name.strip():
            raise ValueError("学生姓名必须是非空字符串")
        
        if name in self.students:
            print(f"警告: 学生 {name} 已存在")
        else:
            self.students[name] = []
            print(f"成功添加学生: {name}")
    
    def add_score(self, name, score):
        """
        添加成绩
        
        参数:
            name (str): 学生姓名
            score (float): 成绩
        """
        # 验证学生是否存在
        if name not in self.students:
            raise StudentNotFoundError(name)
        
        # 验证成绩是否有效
        if not isinstance(score, (int, float)):
            raise InvalidScoreError(score, "成绩必须是数字")
        
        if score < 0 or score > 100:
            raise InvalidScoreError(score)
        
        # 添加成绩
        self.students[name].append(score)
        print(f"成功为 {name} 添加成绩: {score}")
    
    def get_average(self, name):
        """
        计算学生平均成绩
        
        参数:
            name (str): 学生姓名
            
        返回:
            float: 平均成绩
        """
        if name not in self.students:
            raise StudentNotFoundError(name)
        
        scores = self.students[name]
        if not scores:
            raise ValueError(f"学生 {name} 没有成绩记录")
        
        return sum(scores) / len(scores)
    
    def get_student_info(self, name):
        """
        获取学生信息
        
        参数:
            name (str): 学生姓名
            
        返回:
            dict: 学生信息
        """
        if name not in self.students:
            raise StudentNotFoundError(name)
        
        scores = self.students[name]
        info = {
            "name": name,
            "scores": scores,
            "count": len(scores)
        }
        
        if scores:
            info["average"] = sum(scores) / len(scores)
        else:
            info["average"] = 0
        
        return info

# 使用成绩管理系统
print("===系统使用演示===")
grade_manager = GradeManager()

# 正常操作
try:
    # 添加学生
    grade_manager.add_student("张三")
    grade_manager.add_student("李四")
    
    # 添加成绩
    grade_manager.add_score("张三", 85)
    grade_manager.add_score("张三", 92)
    grade_manager.add_score("李四", 78)
    
    # 获取学生信息
    zhang_san_info = grade_manager.get_student_info("张三")
    print(f"张三信息: {zhang_san_info}")
    
    li_si_average = grade_manager.get_average("李四")
    print(f"李四平均分: {li_si_average:.2f}")
    
except (InvalidScoreError, StudentNotFoundError, ValueError) as e:
    print(f"操作失败: {e}")

# 演示异常处理
print("\n===异常处理演示===")

# 1. 处理无效成绩
try:
    grade_manager.add_score("张三", 150)  # 超出范围的成绩
except InvalidScoreError as e:
    print(f"成绩错误: {e}")

# 2. 处理学生未找到
try:
    grade_manager.add_score("王五", 80)  # 不存在的学生
except StudentNotFoundError as e:
    print(f"学生错误: {e}")

# 3. 处理无效数据类型
try:
    grade_manager.add_score("张三", "优秀")  # 非数字成绩
except InvalidScoreError as e:
    print(f"数据类型错误: {e}")

# 4. 处理没有成绩记录的情况
try:
    grade_manager.add_student("王五")
    average = grade_manager.get_average("王五")  # 没有成绩记录
    print(f"王五平均分: {average}")
except ValueError as e:
    print(f"计算错误: {e}")
```

#### 案例2：文件操作安全系统
```python
# 文件操作安全系统
print("\n===文件操作安全系统===")

import json
import os
from datetime import datetime

# 自定义文件操作异常
class FileOperationError(Exception):
    """文件操作异常基类"""
    def __init__(self, operation, filename, message):
        self.operation = operation
        self.filename = filename
        self.message = message
        super().__init__(f"文件{operation}操作失败 - {filename}: {message}")

class FileReadError(FileOperationError):
    """文件读取错误"""
    def __init__(self, filename, message):
        super().__init__("读取", filename, message)

class FileWriteError(FileOperationError):
    """文件写入错误"""
    def __init__(self, filename, message):
        super().__init__("写入", filename, message)

# 安全文件操作类
class SafeFileManager:
    """安全文件管理器"""
    
    @staticmethod
    def read_json_file(filename):
        """
        安全读取JSON文件
        
        参数:
            filename (str): 文件名
            
        返回:
            dict: 解析后的数据
        """
        try:
            # 检查文件是否存在
            if not os.path.exists(filename):
                raise FileReadError(filename, "文件不存在")
            
            # 检查是否为文件（而非目录）
            if not os.path.isfile(filename):
                raise FileReadError(filename, "路径不是文件")
            
            # 读取文件
            with open(filename, 'r', encoding='utf-8') as file:
                data = json.load(file)
            
            print(f"成功读取文件: {filename}")
            return data
            
        except PermissionError:
            raise FileReadError(filename, "没有读取权限")
        except json.JSONDecodeError as e:
            raise FileReadError(filename, f"JSON格式错误: {e}")
        except UnicodeDecodeError:
            raise FileReadError(filename, "文件编码错误")
        except Exception as e:
            raise FileReadError(filename, f"未知错误: {e}")
    
    @staticmethod
    def write_json_file(filename, data):
        """
        安全写入JSON文件
        
        参数:
            filename (str): 文件名
            data (dict): 要写入的数据
        """
        try:
            # 确保目录存在
            directory = os.path.dirname(filename)
            if directory and not os.path.exists(directory):
                os.makedirs(directory, exist_ok=True)
            
            # 写入文件
            with open(filename, 'w', encoding='utf-8') as file:
                json.dump(data, file, indent=2, ensure_ascii=False)
            
            print(f"成功写入文件: {filename}")
            
        except PermissionError:
            raise FileWriteError(filename, "没有写入权限")
        except OSError as e:
            raise FileWriteError(filename, f"文件系统错误: {e}")
        except TypeError as e:
            raise FileWriteError(filename, f"数据类型错误: {e}")
        except Exception as e:
            raise FileWriteError(filename, f"未知错误: {e}")
    
    @staticmethod
    def backup_file(filename):
        """
        备份文件
        
        参数:
            filename (str): 要备份的文件名
        """
        if not os.path.exists(filename):
            print(f"文件 {filename} 不存在，无需备份")
            return
        
        # 生成备份文件名
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        name, ext = os.path.splitext(filename)
        backup_filename = f"{name}_{timestamp}{ext}"
        
        try:
            with open(filename, 'r', encoding='utf-8') as src, \
                 open(backup_filename, 'w', encoding='utf-8') as dst:
                dst.write(src.read())
            
            print(f"文件备份成功: {backup_filename}")
            return backup_filename
            
        except Exception as e:
            raise FileOperationError("备份", filename, f"备份失败: {e}")

# 使用安全文件操作
print("===文件操作演示===")

# 创建示例数据
config_data = {
    "app_name": "学生成绩管理系统",
    "version": "1.0.0",
    "debug": True,
    "database": {
        "host": "localhost",
        "port": 5432,
        "name": "student_grades"
    },
    "features": ["成绩录入", "统计分析", "报表生成"]
}

# 安全文件管理器实例
file_manager = SafeFileManager()

# 正常文件操作
try:
    # 写入配置文件
    file_manager.write_json_file("config/app.json", config_data)
    
    # 读取配置文件
    loaded_config = file_manager.read_json_file("config/app.json")
    print(f"读取的配置: {loaded_config['app_name']} v{loaded_config['version']}")
    
    # 备份文件
    backup_file = file_manager.backup_file("config/app.json")
    
except FileOperationError as e:
    print(f"文件操作失败: {e}")
except Exception as e:
    print(f"未预期的错误: {e}")

# 演示异常处理
print("\n===异常处理演示===")

# 1. 处理文件不存在
try:
    data = file_manager.read_json_file("nonexistent.json")
except FileReadError as e:
    print(f"读取错误: {e}")

# 2. 处理权限错误（在某些系统上可能不会触发）
try:
    # 尝试写入系统目录（可能会失败）
    file_manager.write_json_file("/root/test.json", {"test": "data"})
except FileWriteError as e:
    print(f"写入错误: {e}")

# 3. 处理JSON格式错误
try:
    # 创建一个格式错误的JSON文件
    with open("invalid.json", 'w', encoding='utf-8') as f:
        f.write("{invalid json}")
    
    # 尝试读取
    data = file_manager.read_json_file("invalid.json")
except FileReadError as e:
    print(f"格式错误: {e}")
finally:
    # 清理测试文件
    if os.path.exists("invalid.json"):
        os.remove("invalid.json")

# 4. 处理目录不存在（实际上会被自动创建）
try:
    file_manager.write_json_file("new_directory/config.json", {"key": "value"})
    data = file_manager.read_json_file("new_directory/config.json")
    print(f"目录创建成功，读取数据: {data}")
except FileOperationError as e:
    print(f"操作失败: {e}")
```

### 代码说明

**案例1代码解释**：
1. `class InvalidScoreError(Exception):`：自定义异常类继承自Exception
2. `raise InvalidScoreError(score)`：在适当时机主动抛出异常
3. `try: ... except InvalidScoreError as e:`：捕获并处理特定异常
4. `super().__init__(self.message)`：调用父类构造函数初始化异常信息

如果写成`except Exception as e:`而不是`except (InvalidScoreError, StudentNotFoundError, ValueError) as e:`，虽然能捕获所有异常，但会掩盖具体问题，不利于调试。

**案例2代码解释**：
1. `with open(filename, 'r', encoding='utf-8') as file:`：使用with语句确保文件自动关闭
2. `except PermissionError:`：捕获特定的权限错误异常
3. `except json.JSONDecodeError as e:`：捕获JSON解析错误
4. `os.makedirs(directory, exist_ok=True)`：自动创建不存在的目录

如果忘记使用with语句或try-finally，在发生异常时文件可能无法正确关闭，造成资源泄露。

## 2. try-except语句和异常处理

### 知识点解析

**概念定义**：try-except语句就像给程序配备了一个"安全网"，在执行可能出错的代码前先做好准备，一旦出错就跳转到指定的处理代码，避免程序崩溃。

**核心规则**：
1. try块包含可能引发异常的代码
2. except块处理特定类型的异常
3. 可以有多个except块处理不同类型的异常
4. else块在没有异常时执行
5. finally块无论是否有异常都会执行

**常见易错点**：
1. except块顺序错误，导致后面的异常处理永远不会执行
2. 在except块中再次引发异常但没有正确处理
3. 忘记在finally块中进行必要的资源清理
4. 使用过于宽泛的异常捕获，掩盖了具体问题

### 实战案例

#### 案例1：网络请求模拟器
```python
# 网络请求模拟器
print("===网络请求模拟器===")

import random
import time
from typing import Optional

# 自定义网络异常
class NetworkError(Exception):
    """网络错误基类"""
    pass

class TimeoutError(NetworkError):
    """超时错误"""
    def __init__(self, url, timeout):
        self.url = url
        self.timeout = timeout
        super().__init__(f"请求 {url} 超时 ({timeout}秒)")

class ConnectionError(NetworkError):
    """连接错误"""
    def __init__(self, url):
        self.url = url
        super().__init__(f"无法连接到 {url}")

class HTTPError(NetworkError):
    """HTTP错误"""
    def __init__(self, url, status_code):
        self.url = url
        self.status_code = status_code
        super().__init__(f"HTTP {status_code} 错误: {url}")

# 模拟网络请求类
class NetworkSimulator:
    """网络请求模拟器"""
    
    @staticmethod
    def fetch_data(url: str, timeout: int = 5) -> Optional[dict]:
        """
        模拟获取网络数据
        
        参数:
            url (str): 请求地址
            timeout (int): 超时时间（秒）
            
        返回:
            dict or None: 返回的数据或None
        """
        print(f"正在请求: {url}")
        
        # 模拟网络延迟
        time.sleep(random.uniform(0.1, 1.0))
        
        # 模拟不同的网络情况
        error_type = random.choice(['success', 'success', 'success', 'timeout', 'connection', 'http_404', 'http_500'])
        
        if error_type == 'timeout':
            raise TimeoutError(url, timeout)
        elif error_type == 'connection':
            raise ConnectionError(url)
        elif error_type == 'http_404':
            raise HTTPError(url, 404)
        elif error_type == 'http_500':
            raise HTTPError(url, 500)
        else:
            # 模拟成功响应
            return {
                "url": url,
                "status": "success",
                "data": {
                    "id": random.randint(1, 1000),
                    "name": f"数据项 {random.randint(1, 100)}",
                    "value": random.uniform(0, 100)
                },
                "timestamp": time.time()
            }
    
    @staticmethod
    def fetch_with_retry(url: str, max_retries: int = 3, timeout: int = 5) -> Optional[dict]:
        """
        带重试机制的网络请求
        
        参数:
            url (str): 请求地址
            max_retries (int): 最大重试次数
            timeout (int): 超时时间
            
        返回:
            dict or None: 返回的数据或None
        """
        for attempt in range(max_retries):
            try:
                print(f"第 {attempt + 1} 次尝试请求 {url}")
                data = NetworkSimulator.fetch_data(url, timeout)
                print(f"请求成功: {url}")
                return data
                
            except TimeoutError as e:
                print(f"超时错误: {e}")
                if attempt < max_retries - 1:
                    wait_time = 2 ** attempt  # 指数退避
                    print(f"等待 {wait_time} 秒后重试...")
                    time.sleep(wait_time)
                else:
                    print("达到最大重试次数，放弃请求")
                    
            except ConnectionError as e:
                print(f"连接错误: {e}")
                if attempt < max_retries - 1:
                    wait_time = 1
                    print(f"等待 {wait_time} 秒后重试...")
                    time.sleep(wait_time)
                else:
                    print("达到最大重试次数，放弃请求")
                    
            except HTTPError as e:
                print(f"HTTP错误: {e}")
                if e.status_code >= 500 and attempt < max_retries - 1:
                    # 服务器错误可以重试
                    wait_time = 1
                    print(f"等待 {wait_time} 秒后重试...")
                    time.sleep(wait_time)
                else:
                    # 客户端错误(4xx)或达到最大重试次数
                    print("无法重试，放弃请求")
                    break
                    
            except Exception as e:
                print(f"未预期的错误: {e}")
                break
        
        return None

# 使用网络请求模拟器
print("===网络请求演示===")

# 测试URL列表
urls = [
    "https://api.example.com/users",
    "https://api.example.com/products",
    "https://api.example.com/orders"
]

# 创建网络模拟器实例
simulator = NetworkSimulator()

# 发送请求
for url in urls:
    print(f"\n--- 请求 {url} ---")
    try:
        data = simulator.fetch_with_retry(url, max_retries=3)
        if data:
            print(f"获取到数据: {data['data']}")
        else:
            print("未能获取到数据")
    except Exception as e:
        print(f"请求完全失败: {e}")

# 演示不同类型的异常处理
print("\n===不同类型异常处理===")

# 1. 单次请求（不带重试）
print("1. 单次请求演示:")
try:
    data = NetworkSimulator.fetch_data("https://api.test.com/data")
    print(f"请求成功: {data}")
except TimeoutError as e:
    print(f"处理超时: {e}")
except ConnectionError as e:
    print(f"处理连接错误: {e}")
except HTTPError as e:
    if e.status_code == 404:
        print(f"页面未找到: {e}")
    elif e.status_code >= 500:
        print(f"服务器错误: {e}")
    else:
        print(f"其他HTTP错误: {e}")
except NetworkError as e:
    print(f"其他网络错误: {e}")
except Exception as e:
    print(f"完全未预期的错误: {e}")

# 2. 带重试的请求
print("\n2. 带重试的请求演示:")
data = simulator.fetch_with_retry("https://api.retry.com/data", max_retries=2)
if data:
    print(f"重试后成功: {data}")
else:
    print("重试后仍然失败")
```

#### 案例2：数据库操作模拟器
```python
# 数据库操作模拟器
print("\n===数据库操作模拟器===")

import random
import time
from contextlib import contextmanager

# 数据库异常定义
class DatabaseError(Exception):
    """数据库错误基类"""
    pass

class ConnectionError(DatabaseError):
    """连接错误"""
    def __init__(self, message="数据库连接失败"):
        super().__init__(message)

class QueryError(DatabaseError):
    """查询错误"""
    def __init__(self, query, message="查询执行失败"):
        self.query = query
        super().__init__(f"{message}: {query}")

class TransactionError(DatabaseError):
    """事务错误"""
    def __init__(self, message="事务执行失败"):
        super().__init__(message)

# 模拟数据库连接
class DatabaseConnection:
    """模拟数据库连接"""
    
    def __init__(self, host, port, database):
        self.host = host
        self.port = port
        self.database = database
        self.connected = False
        self.transaction_active = False
    
    def connect(self):
        """连接数据库"""
        print(f"正在连接数据库 {self.host}:{self.port}/{self.database}")
        time.sleep(0.1)  # 模拟连接时间
        
        # 模拟连接可能失败
        if random.choice([True, True, True, False]):
            self.connected = True
            print("数据库连接成功")
        else:
            raise ConnectionError("无法连接到数据库服务器")
    
    def disconnect(self):
        """断开数据库连接"""
        if self.connected:
            print("断开数据库连接")
            self.connected = False
    
    def execute_query(self, query):
        """
        执行查询
        
        参数:
            query (str): SQL查询语句
            
        返回:
            list: 查询结果
        """
        if not self.connected:
            raise ConnectionError("数据库未连接")
        
        print(f"执行查询: {query}")
        time.sleep(0.05)  # 模拟查询时间
        
        # 模拟查询可能失败
        if "INVALID" in query.upper():
            raise QueryError(query, "无效的SQL语法")
        
        if "ERROR" in query.upper():
            raise QueryError(query, "查询执行错误")
        
        # 模拟查询结果
        if "SELECT" in query.upper():
            # 模拟返回数据
            row_count = random.randint(0, 10)
            result = []
            for i in range(row_count):
                result.append({
                    "id": i + 1,
                    "name": f"记录 {i + 1}",
                    "value": random.randint(1, 100)
                })
            return result
        else:
            # INSERT, UPDATE, DELETE等操作
            return [{"affected_rows": random.randint(0, 5)}]
    
    def begin_transaction(self):
        """开始事务"""
        if not self.connected:
            raise ConnectionError("数据库未连接")
        
        if self.transaction_active:
            raise TransactionError("事务已在进行中")
        
        self.transaction_active = True
        print("开始事务")
    
    def commit(self):
        """提交事务"""
        if not self.connected:
            raise ConnectionError("数据库未连接")
        
        if not self.transaction_active:
            raise TransactionError("没有活动的事务")
        
        print("提交事务")
        self.transaction_active = False
    
    def rollback(self):
        """回滚事务"""
        if not self.connected:
            raise ConnectionError("数据库未连接")
        
        if not self.transaction_active:
            raise TransactionError("没有活动的事务")
        
        print("回滚事务")
        self.transaction_active = False
    
    def __enter__(self):
        """上下文管理器入口"""
        self.connect()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """上下文管理器出口"""
        if exc_type is not None:
            # 如果有异常，回滚事务
            if self.transaction_active:
                try:
                    self.rollback()
                except:
                    pass  # 忽略回滚时的错误
        
        self.disconnect()
        return False  # 不抑制异常

# 数据库操作管理器
class DatabaseManager:
    """数据库操作管理器"""
    
    def __init__(self, host, port, database):
        self.host = host
        self.port = port
        self.database = database
    
    def get_user(self, user_id):
        """
        获取用户信息
        
        参数:
            user_id (int): 用户ID
            
        返回:
            dict: 用户信息
        """
        with DatabaseConnection(self.host, self.port, self.database) as conn:
            query = f"SELECT * FROM users WHERE id = {user_id}"
            results = conn.execute_query(query)
            
            if results:
                return results[0]
            else:
                raise QueryError(query, "用户未找到")
    
    def update_user(self, user_id, name, email):
        """
        更新用户信息
        
        参数:
            user_id (int): 用户ID
            name (str): 用户名
            email (str): 邮箱
            
        返回:
            bool: 是否更新成功
        """
        with DatabaseConnection(self.host, self.port, self.database) as conn:
            conn.begin_transaction()
            try:
                query = f"UPDATE users SET name = '{name}', email = '{email}' WHERE id = {user_id}"
                result = conn.execute_query(query)
                conn.commit()
                return result[0]["affected_rows"] > 0
            except Exception as e:
                conn.rollback()
                raise e
    
    def create_user_with_retry(self, name, email, max_retries=3):
        """
        创建用户（带重试机制）
        
        参数:
            name (str): 用户名
            email (str): 邮箱
            max_retries (int): 最大重试次数
            
        返回:
            int: 新用户ID
        """
        for attempt in range(max_retries):
            try:
                with DatabaseConnection(self.host, self.port, self.database) as conn:
                    query = f"INSERT INTO users (name, email) VALUES ('{name}', '{email}')"
                    result = conn.execute_query(query)
                    new_id = random.randint(1000, 9999)
                    print(f"用户创建成功，ID: {new_id}")
                    return new_id
                    
            except ConnectionError as e:
                print(f"连接错误 (尝试 {attempt + 1}/{max_retries}): {e}")
                if attempt < max_retries - 1:
                    time.sleep(1)
                else:
                    raise e
            except QueryError as e:
                print(f"查询错误: {e}")
                raise e  # 查询错误通常不需要重试
            except Exception as e:
                print(f"未预期错误: {e}")
                raise e

# 使用数据库操作模拟器
print("===数据库操作演示===")

# 创建数据库管理器
db_manager = DatabaseManager("localhost", 5432, "testdb")

# 正常操作
print("1. 正常数据库操作:")
try:
    # 获取用户
    user = db_manager.get_user(1)
    print(f"获取到用户: {user}")
    
    # 更新用户
    success = db_manager.update_user(1, "新名字", "new@example.com")
    print(f"用户更新: {'成功' if success else '失败'}")
    
except QueryError as e:
    print(f"查询错误: {e}")
except ConnectionError as e:
    print(f"连接错误: {e}")
except Exception as e:
    print(f"其他错误: {e}")

# 演示异常处理
print("\n===异常处理演示===")

# 1. 处理连接错误
print("1. 连接错误处理:")
try:
    # 模拟多次尝试连接
    user_id = db_manager.create_user_with_retry("测试用户", "test@example.com", max_retries=2)
    print(f"创建用户成功，ID: {user_id}")
except ConnectionError as e:
    print(f"连接失败: {e}")
except Exception as e:
    print(f"其他错误: {e}")

# 2. 处理查询错误
print("\n2. 查询错误处理:")
try:
    with DatabaseConnection("localhost", 5432, "testdb") as conn:
        # 执行无效查询
        result = conn.execute_query("INVALID SQL STATEMENT")
        print(f"查询结果: {result}")
except QueryError as e:
    print(f"SQL错误: {e}")
except ConnectionError as e:
    print(f"连接错误: {e}")

# 3. 处理事务错误
print("\n3. 事务错误处理:")
try:
    with DatabaseConnection("localhost", 5432, "testdb") as conn:
        conn.begin_transaction()
        try:
            # 执行可能失败的操作
            conn.execute_query("INSERT INTO users (name) VALUES ('测试')")
            # 模拟另一个可能失败的操作
            conn.execute_query("ERROR QUERY")
            conn.commit()
        except Exception as e:
            print(f"操作失败: {e}")
            conn.rollback()
            raise e
except DatabaseError as e:
    print(f"数据库错误: {e}")

# 4. 使用上下文管理器的自动资源管理
print("\n4. 自动资源管理:")
try:
    with DatabaseConnection("localhost", 5432, "testdb") as conn:
        result = conn.execute_query("SELECT * FROM users")
        print(f"查询结果: {len(result)} 条记录")
        # 即使发生异常，连接也会自动关闭
        raise ValueError("模拟意外错误")
except ValueError as e:
    print(f"业务逻辑错误: {e}")
except DatabaseError as e:
    print(f"数据库错误: {e}")
```

### 代码说明

**案例1代码解释**：
1. `try: ... except TimeoutError as e:`：按异常类型顺序捕获特定异常
2. `for attempt in range(max_retries):`：实现重试机制
3. `time.sleep(2 ** attempt)`：指数退避策略，逐渐增加等待时间
4. `except Exception as e: break`：捕获未预期异常并终止重试

如果把`except TimeoutError`和`except NetworkError`的顺序颠倒，由于TimeoutError是NetworkError的子类，TimeoutError的处理永远不会被执行。

**案例2代码解释**：
1. `def __enter__(self):`和`def __exit__(self, exc_type, exc_val, exc_tb):`：实现上下文管理器协议
2. `with DatabaseConnection(...) as conn:`：使用with语句自动管理资源
3. `if exc_type is not None: self.rollback()`：在上下文退出时有异常则回滚事务
4. `return False`：不抑制异常，让异常继续向上传播

如果在`__exit__`方法中返回True而不是False，会抑制所有异常，这通常不是我们想要的行为。

## 3. 自定义异常和异常链

### 知识点解析

**概念定义**：自定义异常就像为特定业务场景创建的"专业错误标签"，让错误信息更加明确和具体。异常链就像"错误的传承记录"，保留了从最初错误到最后错误的完整路径。

**核心规则**：
1. 自定义异常类应继承自Exception或其子类
2. 异常类应提供有意义的错误信息
3. 使用raise...from语法创建异常链
4. 异常链帮助调试复杂错误场景

**常见易错点**：
1. 自定义异常信息不明确，难以定位问题
2. 忘记调用父类的构造函数
3. 滥用异常链，导致错误信息过于复杂
4. 在异常链中泄露敏感信息

### 实战案例

#### 案例1：电商系统异常处理
```python
# 电商系统异常处理
print("===电商系统异常处理===")

# 电商系统自定义异常
class ECommerceError(Exception):
    """电商系统错误基类"""
    def __init__(self, message, error_code=None):
        self.message = message
        self.error_code = error_code
        super().__init__(self.message)
    
    def __str__(self):
        if self.error_code:
            return f"[错误代码: {self.error_code}] {self.message}"
        return self.message

class ValidationError(ECommerceError):
    """验证错误"""
    def __init__(self, field, value, message):
        self.field = field
        self.value = value
        error_message = f"字段 '{field}' 验证失败: {message} (值: {value})"
        super().__init__(error_message, "VALIDATION_ERROR")

class BusinessLogicError(ECommerceError):
    """业务逻辑错误"""
    def __init__(self, operation, reason):
        self.operation = operation
        self.reason = reason
        error_message = f"业务操作 '{operation}' 失败: {reason}"
        super().__init__(error_message, "BUSINESS_LOGIC_ERROR")

class PaymentError(ECommerceError):
    """支付错误"""
    def __init__(self, payment_method, reason):
        self.payment_method = payment_method
        self.reason = reason
        error_message = f"支付方式 '{payment_method}' 支付失败: {reason}"
        super().__init__(error_message, "PAYMENT_ERROR")

class InventoryError(ECommerceError):
    """库存错误"""
    def __init__(self, product_id, requested, available):
        self.product_id = product_id
        self.requested = requested
        self.available = available
        error_message = f"商品 {product_id} 库存不足: 请求 {requested}, 可用 {available}"
        super().__init__(error_message, "INVENTORY_ERROR")

# 电商系统类
class ECommerceSystem:
    """电商系统"""
    
    def __init__(self):
        # 模拟商品库存
        self.inventory = {
            "P001": 10,  # 商品ID: 库存数量
            "P002": 5,
            "P003": 0
        }
        
        # 模拟用户账户
        self.users = {
            "user1": {"balance": 1000, "email": "user1@example.com"},
            "user2": {"balance": 50, "email": "user2@example.com"}
        }
    
    def validate_order(self, user_id, product_id, quantity):
        """
        验证订单
        
        参数:
            user_id (str): 用户ID
            product_id (str): 商品ID
            quantity (int): 数量
            
        异常:
            ValidationError: 验证失败
            BusinessLogicError: 业务逻辑错误
        """
        print(f"验证订单: 用户={user_id}, 商品={product_id}, 数量={quantity}")
        
        # 验证用户
        if user_id not in self.users:
            raise ValidationError("user_id", user_id, "用户不存在")
        
        # 验证商品
        if product_id not in self.inventory:
            raise ValidationError("product_id", product_id, "商品不存在")
        
        # 验证数量
        if not isinstance(quantity, int) or quantity <= 0:
            raise ValidationError("quantity", quantity, "数量必须是正整数")
        
        # 验证库存
        available = self.inventory[product_id]
        if quantity > available:
            raise InventoryError(product_id, quantity, available)
        
        print("订单验证通过")
    
    def process_payment(self, user_id, amount, payment_method):
        """
        处理支付
        
        参数:
            user_id (str): 用户ID
            amount (float): 金额
            payment_method (str): 支付方式
            
        异常:
            PaymentError: 支付失败
            BusinessLogicError: 业务逻辑错误
        """
        print(f"处理支付: 用户={user_id}, 金额={amount}, 方式={payment_method}")
        
        # 验证支付方式
        valid_methods = ["credit_card", "debit_card", "paypal", "alipay"]
        if payment_method not in valid_methods:
            raise PaymentError(payment_method, "不支持的支付方式")
        
        # 模拟支付处理
        import random
        if payment_method == "credit_card":
            # 信用卡支付有5%失败率
            if random.random() < 0.05:
                raise PaymentError(payment_method, "信用卡验证失败")
        elif payment_method == "paypal":
            # PayPal支付有2%失败率
            if random.random() < 0.02:
                raise PaymentError(payment_method, "PayPal账户余额不足")
        
        # 验证用户余额
        user_balance = self.users[user_id]["balance"]
        if amount > user_balance:
            raise BusinessLogicError("支付", f"余额不足: 需要 {amount}, 可用 {user_balance}")
        
        # 扣除余额
        self.users[user_id]["balance"] -= amount
        print(f"支付成功，用户余额: {self.users[user_id]['balance']}")
    
    def place_order(self, user_id, product_id, quantity, payment_method):
        """
        下订单
        
        参数:
            user_id (str): 用户ID
            product_id (str): 商品ID
            quantity (int): 数量
            payment_method (str): 支付方式
            
        返回:
            dict: 订单信息
        """
        try:
            # 1. 验证订单
            try:
                self.validate_order(user_id, product_id, quantity)
            except ValidationError as e:
                raise BusinessLogicError("下单", "订单验证失败") from e
            except InventoryError as e:
                raise BusinessLogicError("下单", "库存检查失败") from e
            
            # 2. 计算金额（假设单价为100）
            unit_price = 100
            total_amount = unit_price * quantity
            
            # 3. 处理支付
            try:
                self.process_payment(user_id, total_amount, payment_method)
            except PaymentError as e:
                raise BusinessLogicError("下单", "支付处理失败") from e
            except BusinessLogicError:
                raise  # 重新抛出业务逻辑错误
            
            # 4. 更新库存
            self.inventory[product_id] -= quantity
            print(f"库存更新: {product_id} 剩余 {self.inventory[product_id]}")
            
            # 5. 生成订单
            import random
            order_id = f"ORD{random.randint(10000, 99999)}"
            order = {
                "order_id": order_id,
                "user_id": user_id,
                "product_id": product_id,
                "quantity": quantity,
                "total_amount": total_amount,
                "payment_method": payment_method,
                "status": "completed"
            }
            
            print(f"订单创建成功: {order_id}")
            return order
            
        except BusinessLogicError:
            raise  # 重新抛出业务逻辑错误
        except Exception as e:
            raise BusinessLogicError("下单", "系统内部错误") from e

# 使用电商系统
print("===电商系统演示===")

# 创建电商系统实例
ecommerce = ECommerceSystem()

# 正常下单流程
print("1. 正常下单:")
try:
    order = ecommerce.place_order("user1", "P001", 2, "credit_card")
    print(f"下单成功: {order}")
except ECommerceError as e:
    print(f"下单失败: {e}")

# 演示各种异常处理
print("\n===异常处理演示===")

# 1. 处理验证错误
print("1. 验证错误处理:")
try:
    ecommerce.place_order("nonexistent_user", "P001", 2, "credit_card")
except BusinessLogicError as e:
    print(f"业务逻辑错误: {e}")
    print(f"原始异常: {e.__cause__}")

# 2. 处理库存错误
print("\n2. 库存错误处理:")
try:
    ecommerce.place_order("user1", "P003", 1, "credit_card")  # P003库存为0
except BusinessLogicError as e:
    print(f"业务逻辑错误: {e}")
    print(f"原始异常: {e.__cause__}")

# 3. 处理支付错误
print("\n3. 支付错误处理:")
try:
    ecommerce.place_order("user2", "P001", 5, "paypal")  # user2余额不足
except BusinessLogicError as e:
    print(f"业务逻辑错误: {e}")
    # 注意：这里可能没有直接原因，因为BusinessLogicError直接抛出

# 4. 处理不支持的支付方式
print("\n4. 支付方式错误处理:")
try:
    ecommerce.place_order("user1", "P001", 1, "bitcoin")  # 不支持的支付方式
except BusinessLogicError as e:
    print(f"业务逻辑错误: {e}")
    print(f"原始异常: {e.__cause__}")

# 5. 展示异常链
print("\n5. 异常链示例:")
try:
    # 故意触发一个复杂的错误场景
    ecommerce.place_order("user1", "P999", -1, "invalid_method")
except ECommerceError as e:
    print(f"捕获到异常: {e}")
    current_exception = e
    level = 0
    while current_exception.__cause__:
        level += 1
        current_exception = current_exception.__cause__
        print(f"  原因层级 {level}: {current_exception} ({type(current_exception).__name__})")
```

#### 案例2：数据处理管道异常处理
```python
# 数据处理管道异常处理
print("\n===数据处理管道异常处理===")

# 数据处理异常
class DataProcessingError(Exception):
    """数据处理错误基类"""
    def __init__(self, stage, message):
        self.stage = stage
        self.message = message
        super().__init__(f"在{stage}阶段发生错误: {message}")

class DataValidationError(DataProcessingError):
    """数据验证错误"""
    def __init__(self, stage, field, value, reason):
        self.field = field
        self.value = value
        self.reason = reason
        message = f"字段'{field}'验证失败: {reason} (值: {value})"
        super().__init__(stage, message)

class DataTransformationError(DataProcessingError):
    """数据转换错误"""
    def __init__(self, stage, data, reason):
        self.data = data
        self.reason = reason
        message = f"数据转换失败: {reason} (数据: {data})"
        super().__init__(stage, message)

class DataStorageError(DataProcessingError):
    """数据存储错误"""
    def __init__(self, stage, operation, reason):
        self.operation = operation
        self.reason = reason
        message = f"数据存储操作'{operation}'失败: {reason}"
        super().__init__(stage, message)

# 数据处理管道
class DataProcessingPipeline:
    """数据处理管道"""
    
    def __init__(self):
        self.processed_data = []
        self.errors = []
    
    def load_data(self, source):
        """
        加载数据
        
        参数:
            source (str): 数据源
            
        返回:
            list: 原始数据
        """
        print(f"从 {source} 加载数据")
        
        # 模拟数据加载
        if source == "invalid_source":
            raise DataProcessingError("数据加载", "无效的数据源")
        
        # 模拟返回一些原始数据
        return [
            {"id": 1, "name": "张三", "age": 25, "salary": 8000},
            {"id": 2, "name": "李四", "age": 30, "salary": 12000},
            {"id": 3, "name": "王五", "age": -5, "salary": 15000},  # 无效年龄
            {"id": 4, "name": "", "age": 28, "salary": 10000},     # 空名字
            {"id": 5, "name": "赵六", "age": 35, "salary": "invalid"},  # 无效薪资
        ]
    
    def validate_data(self, raw_data):
        """
        验证数据
        
        参数:
            raw_data (list): 原始数据
            
        返回:
            list: 验证通过的数据
        """
        print("验证数据")
        valid_data = []
        
        for record in raw_data:
            try:
                # 验证ID
                if not isinstance(record.get("id"), int) or record["id"] <= 0:
                    raise DataValidationError(
                        "数据验证", 
                        "id", 
                        record.get("id"), 
                        "ID必须是正整数"
                    )
                
                # 验证姓名
                if not isinstance(record.get("name"), str) or not record["name"].strip():
                    raise DataValidationError(
                        "数据验证", 
                        "name", 
                        record.get("name"), 
                        "姓名不能为空"
                    )
                
                # 验证年龄
                if not isinstance(record.get("age"), int) or record["age"] < 0 or record["age"] > 150:
                    raise DataValidationError(
                        "数据验证", 
                        "age", 
                        record.get("age"), 
                        "年龄必须在0-150之间"
                    )
                
                # 验证薪资
                if not isinstance(record.get("salary"), (int, float)) or record["salary"] < 0:
                    raise DataValidationError(
                        "数据验证", 
                        "salary", 
                        record.get("salary"), 
                        "薪资必须是非负数"
                    )
                
                valid_data.append(record)
                
            except DataValidationError as e:
                print(f"记录验证失败: {e}")
                self.errors.append(str(e))
        
        if not valid_data:
            raise DataProcessingError("数据验证", "没有通过验证的数据记录")
        
        print(f"验证完成，{len(valid_data)}条记录通过验证")
        return valid_data
    
    def transform_data(self, valid_data):
        """
        转换数据
        
        参数:
            valid_data (list): 验证通过的数据
            
        返回:
            list: 转换后的数据
        """
        print("转换数据")
        transformed_data = []
        
        for record in valid_data:
            try:
                # 数据转换
                transformed_record = {
                    "employee_id": f"EMP{record['id']:03d}",
                    "full_name": record["name"].strip().title(),
                    "birth_year": 2023 - record["age"],
                    "monthly_salary": record["salary"],
                    "annual_salary": record["salary"] * 12,
                    "salary_level": self._categorize_salary(record["salary"])
                }
                
                transformed_data.append(transformed_record)
                
            except Exception as e:
                raise DataTransformationError(
                    "数据转换", 
                    record, 
                    f"转换记录时发生错误: {e}"
                ) from e
        
        print(f"转换完成，处理了{len(transformed_data)}条记录")
        return transformed_data
    
    def _categorize_salary(self, salary):
        """分类薪资等级"""
        if salary < 5000:
            return "低"
        elif salary < 10000:
            return "中"
        elif salary < 20000:
            return "高"
        else:
            return "很高"
    
    def store_data(self, transformed_data, destination):
        """
        存储数据
        
        参数:
            transformed_data (list): 转换后的数据
            destination (str): 存储目标
        """
        print(f"存储数据到 {destination}")
        
        if destination == "invalid_destination":
            raise DataStorageError("数据存储", "保存", "无效的存储目标")
        
        # 模拟数据存储
        try:
            import json
            with open(f"{destination}.json", "w", encoding="utf-8") as f:
                json.dump(transformed_data, f, ensure_ascii=False, indent=2)
            
            self.processed_data.extend(transformed_data)
            print(f"数据存储成功，共{len(transformed_data)}条记录")
            
        except Exception as e:
            raise DataStorageError(
                "数据存储", 
                "保存", 
                f"存储数据时发生错误: {e}"
            ) from e
    
    def process(self, source, destination):
        """
        执行完整的数据处理流程
        
        参数:
            source (str): 数据源
            destination (str): 存储目标
        """
        try:
            # 1. 加载数据
            try:
                raw_data = self.load_data(source)
            except DataProcessingError as e:
                raise DataProcessingError("数据处理管道", "数据加载失败") from e
            
            # 2. 验证数据
            try:
                valid_data = self.validate_data(raw_data)
            except DataProcessingError as e:
                raise DataProcessingError("数据处理管道", "数据验证失败") from e
            
            # 3. 转换数据
            try:
                transformed_data = self.transform_data(valid_data)
            except DataTransformationError as e:
                raise DataProcessingError("数据处理管道", "数据转换失败") from e
            
            # 4. 存储数据
            try:
                self.store_data(transformed_data, destination)
            except DataStorageError as e:
                raise DataProcessingError("数据处理管道", "数据存储失败") from e
                
            print("数据处理管道执行完成")
            return transformed_data
            
        except DataProcessingError:
            raise  # 重新抛出数据处理错误
        except Exception as e:
            raise DataProcessingError("数据处理管道", f"管道执行过程中发生未预期错误: {e}") from e

# 使用数据处理管道
print("===数据处理管道演示===")

# 创建数据处理管道实例
pipeline = DataProcessingPipeline()

# 正常数据处理流程
print("1. 正常数据处理:")
try:
    result = pipeline.process("employee_database", "processed_employees")
    print(f"处理完成，共处理{len(result)}条记录")
    for record in result[:2]:  # 只显示前2条
        print(f"  {record}")
except DataProcessingError as e:
    print(f"处理失败: {e}")

# 演示异常处理
print("\n===异常处理演示===")

# 1. 处理数据源错误
print("1. 数据源错误处理:")
try:
    pipeline.process("invalid_source", "output")
except DataProcessingError as e:
    print(f"管道错误: {e}")
    print(f"原始错误: {e.__cause__}")

# 2. 处理数据验证错误
print("\n2. 数据验证错误处理:")
try:
    # 创建包含更多无效数据的管道
    invalid_pipeline = DataProcessingPipeline()
    # 手动添加全无效数据来触发验证错误
    invalid_data = [
        {"id": -1, "name": "", "age": -5, "salary": "invalid"},
        {"id": 0, "name": "  ", "age": 200, "salary": -1000}
    ]
    
    # 直接调用验证方法来演示
    valid_data = invalid_pipeline.validate_data(invalid_data)
    print(f"意外通过验证的数据: {valid_data}")
except DataProcessingError as e:
    print(f"验证错误: {e}")

# 3. 处理数据转换错误
print("\n3. 数据转换错误处理:")
try:
    # 模拟转换过程中的意外错误
    pipeline_test = DataProcessingPipeline()
    # 创建一个会导致转换错误的数据
    test_data = [{"id": 1, "name": "测试", "age": 25, "salary": None}]
    
    # 直接调用转换方法来演示
    transformed = pipeline_test.transform_data(test_data)
    print(f"意外转换成功的数据: {transformed}")
except DataProcessingError as e:
    print(f"转换错误: {e}")
    if e.__cause__:
        print(f"原始错误: {e.__cause__}")

# 4. 处理存储错误
print("\n4. 数据存储错误处理:")
try:
    # 创建一些有效数据用于存储测试
    valid_data = [
        {
            "employee_id": "EMP001",
            "full_name": "张三",
            "birth_year": 1998,
            "monthly_salary": 8000,
            "annual_salary": 96000,
            "salary_level": "高"
        }
    ]
    pipeline.store_data(valid_data, "invalid_destination")
except DataProcessingError as e:
    print(f"存储错误: {e}")
    print(f"原始错误: {e.__cause__}")

# 5. 展示完整的异常链
print("\n5. 完整异常链示例:")
try:
    # 创建一个会引发多个层级错误的场景
    pipeline_complex = DataProcessingPipeline()
    pipeline_complex.process("invalid_source", "invalid_destination")
except DataProcessingError as e:
    print(f"顶级异常: {e}")
    current = e
    level = 0
    while current.__cause__:
        level += 1
        current = current.__cause__
        print(f"  异常链层级 {level}: {current} ({type(current).__name__})")
        # 限制显示层级以避免过长输出
        if level > 3:
            print("  ... (更多层级)")
            break
```

### 代码说明

**案例1代码解释**：
1. `class ECommerceError(Exception):`：自定义异常基类，包含错误代码
2. `raise BusinessLogicError("下单", "订单验证失败") from e`：使用from创建异常链
3. `except ValidationError as e: ... raise BusinessLogicError(...) from e`：捕获底层异常并抛出高层异常
4. `e.__cause__`：访问异常链中的原始异常

如果忘记使用`from e`语法，异常链会断开，丢失原始错误信息，不利于调试。

**案例2代码解释**：
1. `class DataProcessingError(Exception):`：针对特定领域的异常基类
2. `def _categorize_salary(self, salary):`：私有方法处理薪资分类逻辑
3. `with open(f"{destination}.json", "w", encoding="utf-8") as f:`：使用with语句确保文件正确关闭
4. 多层异常处理，每层都有明确的职责和错误类型

如果在数据处理管道中不使用异常链，当出现错误时很难定位是哪个具体环节出了问题。

## 4. 上下文管理器和资源管理

### 知识点解析

**概念定义**：上下文管理器就像一个"智能管家"，它知道什么时候该准备资源（如打开文件、建立连接），什么时候该清理资源（如关闭文件、断开连接），确保资源得到妥善管理。

**核心规则**：
1. 实现`__enter__`和`__exit__`方法的类可以作为上下文管理器
2. 使用with语句自动管理上下文管理器
3. `__enter__`方法在进入with块时调用
4. `__exit__`方法在退出with块时调用，即使发生异常也会执行

**常见易错点**：
1. 忘记实现`__exit__`方法中的资源清理逻辑
2. 在`__exit__`方法中错误地抑制异常
3. 不正确处理`__exit__`方法的参数
4. 在上下文管理器中处理异常时再次引发异常

### 实战案例

#### 案例1：数据库连接管理器
```python
# 数据库连接管理器
print("===数据库连接管理器===")

import time
import random
from contextlib import contextmanager

# 数据库异常
class DatabaseConnectionError(Exception):
    """数据库连接错误"""
    def __init__(self, message):
        super().__init__(f"数据库连接错误: {message}")

class DatabaseOperationError(Exception):
    """数据库操作错误"""
    def __init__(self, operation, message):
        super().__init__(f"数据库操作'{operation}'错误: {message}")

# 数据库连接上下文管理器
class DatabaseConnection:
    """数据库连接上下文管理器"""
    
    def __init__(self, host, port, database, username, password):
        self.host = host
        self.port = port
        self.database = database
        self.username = username
        self.password = password
        self.connection_id = None
        self.is_connected = False
        self.transaction_active = False
    
    def __enter__(self):
        """进入上下文"""
        print(f"正在连接数据库 {self.host}:{self.port}/{self.database}")
        
        # 模拟连接过程
        time.sleep(0.1)
        
        # 模拟连接可能失败
        if random.choice([True, True, True, False]):  # 75% 成功率
            self.connection_id = f"conn_{random.randint(1000, 9999)}"
            self.is_connected = True
            print(f"数据库连接成功: {self.connection_id}")
            return self
        else:
            raise DatabaseConnectionError("无法建立数据库连接")
    
    def __exit__(self, exc_type, exc_value, traceback):
        """退出上下文"""
        print(f"关闭数据库连接: {self.connection_id}")
        
        if exc_type is not None:
            # 如果有异常发生
            print(f"检测到异常: {exc_type.__name__}: {exc_value}")
            if self.transaction_active:
                print("回滚未完成的事务")
                self.transaction_active = False
        
        # 模拟关闭连接
        time.sleep(0.05)
        self.is_connected = False
        self.connection_id = None
        print("数据库连接已关闭")
        
        # 返回False表示不抑制异常
        return False
    
    def execute_query(self, query):
        """
        执行查询
        
        参数:
            query (str): SQL查询语句
            
        返回:
            list: 查询结果
        """
        if not self.is_connected:
            raise DatabaseConnectionError("数据库未连接")
        
        print(f"执行查询: {query}")
        time.sleep(0.05)
        
        # 模拟查询可能失败
        if "INVALID" in query.upper():
            raise DatabaseOperationError("查询", "无效的SQL语法")
        
        # 模拟查询结果
        if "SELECT" in query.upper():
            row_count = random.randint(0, 5)
            result = []
            for i in range(row_count):
                result.append({
                    "id": i + 1,
                    "name": f"记录 {i + 1}",
                    "value": random.randint(1, 100)
                })
            return result
        else:
            return [{"affected_rows": random.randint(0, 3)}]
    
    def begin_transaction(self):
        """开始事务"""
        if not self.is_connected:
            raise DatabaseConnectionError("数据库未连接")
        
        if self.transaction_active:
            raise DatabaseOperationError("事务", "事务已在进行中")
        
        self.transaction_active = True
        print("事务开始")
    
    def commit(self):
        """提交事务"""
        if not self.is_connected:
            raise DatabaseConnectionError("数据库未连接")
        
        if not self.transaction_active:
            raise DatabaseOperationError("事务", "没有活动的事务")
        
        print("提交事务")
        self.transaction_active = False
    
    def rollback(self):
        """回滚事务"""
        if not self.is_connected:
            raise DatabaseConnectionError("数据库未连接")
        
        if not self.transaction_active:
            raise DatabaseOperationError("事务", "没有活动的事务")
        
        print("回滚事务")
        self.transaction_active = False

# 使用contextlib创建上下文管理器
@contextmanager
def database_session(host, port, database, username, password):
    """
    数据库会话上下文管理器
    
    参数:
        host (str): 主机地址
        port (int): 端口
        database (str): 数据库名
        username (str): 用户名
        password (str): 密码
    """
    connection = None
    try:
        print("初始化数据库会话")
        connection = DatabaseConnection(host, port, database, username, password)
        yield connection.__enter__()
    except Exception as e:
        print(f"会话期间发生异常: {e}")
        raise
    finally:
        if connection:
            print("清理数据库会话")
            connection.__exit__(None, None, None)

# 使用数据库连接
print("===数据库连接演示===")

# 1. 使用类上下文管理器
print("1. 使用类上下文管理器:")
try:
    with DatabaseConnection("localhost", 5432, "testdb", "user", "password") as conn:
        # 执行数据库操作
        result = conn.execute_query("SELECT * FROM users")
        print(f"查询结果: {len(result)} 条记录")
        
        # 开始事务
        conn.begin_transaction()
        try:
            conn.execute_query("INSERT INTO users (name) VALUES ('测试用户')")
            conn.execute_query("UPDATE users SET name = '新名字' WHERE id = 1")
            conn.commit()
            print("事务提交成功")
        except Exception as e:
            print(f"事务失败: {e}")
            conn.rollback()
            raise
except DatabaseConnectionError as e:
    print(f"连接错误: {e}")
except DatabaseOperationError as e:
    print(f"操作错误: {e}")

# 2. 使用函数上下文管理器
print("\n2. 使用函数上下文管理器:")
try:
    with database_session("localhost", 5432, "testdb", "user", "password") as session:
        result = session.execute_query("SELECT * FROM products")
        print(f"会话查询结果: {len(result)} 条记录")
        
        # 模拟会话中的操作
        session.execute_query("UPDATE products SET price = price * 1.1")
        print("价格更新完成")
except DatabaseConnectionError as e:
    print(f"会话连接错误: {e}")
except DatabaseOperationError as e:
    print(f"会话操作错误: {e}")
except Exception as e:
    print(f"会话未预期错误: {e}")

# 演示异常处理
print("\n===异常处理演示===")

# 1. 处理连接失败
print("1. 连接失败处理:")
try:
    # 多次尝试连接以确保触发失败情况
    with DatabaseConnection("invalid_host", 5432, "testdb", "user", "password") as conn:
        print("意外连接成功")
except DatabaseConnectionError as e:
    print(f"连接失败（正常）: {e}")

# 2. 处理查询错误
print("\n2. 查询错误处理:")
try:
    with DatabaseConnection("localhost", 5432, "testdb", "user", "password") as conn:
        # 执行无效查询
        result = conn.execute_query("INVALID SQL STATEMENT")
        print(f"意外查询成功: {result}")
except DatabaseOperationError as e:
    print(f"查询错误（正常）: {e}")
except DatabaseConnectionError as e:
    print(f"连接错误: {e}")

# 3. 处理事务中的异常
print("\n3. 事务异常处理:")
try:
    with DatabaseConnection("localhost", 5432, "testdb", "user", "password") as conn:
        conn.begin_transaction()
        try:
            conn.execute_query("INSERT INTO users (name) VALUES ('用户1')")
            # 模拟一个会导致错误的操作
            conn.execute_query("INVALID SQL")
            conn.commit()
        except DatabaseOperationError as e:
            print(f"事务中操作失败: {e}")
            conn.rollback()
            raise  # 重新抛出异常
except DatabaseOperationError as e:
    print(f"事务失败（正常）: {e}")

# 4. 演示资源自动清理
print("\n4. 资源自动清理演示:")
try:
    with DatabaseConnection("localhost", 5432, "testdb", "user", "password") as conn:
        print(f"使用连接: {conn.connection_id}")
        # 模拟一些操作
        conn.execute_query("SELECT 1")
        # 故意引发异常
        raise ValueError("模拟业务逻辑错误")
except ValueError as e:
    print(f"业务逻辑错误: {e}")
    print("注意：即使发生异常，数据库连接也会自动关闭")
```

#### 案例2：文件处理和资源管理
```python
# 文件处理和资源管理
print("\n===文件处理和资源管理===")

import os
import json
import csv
import tempfile
from contextlib import contextmanager
from datetime import datetime

# 文件处理异常
class FileProcessingError(Exception):
    """文件处理错误"""
    def __init__(self, operation, filename, message):
        self.operation = operation
        self.filename = filename
        super().__init__(f"文件{operation}操作 '{filename}' 失败: {message}")

# 文件备份管理器
class FileManager:
    """文件管理器"""
    
    def __init__(self, backup_dir="backups"):
        self.backup_dir = backup_dir
        # 确保备份目录存在
        os.makedirs(backup_dir, exist_ok=True)
    
    @contextmanager
    def safe_file_operation(self, filename, mode='r', encoding='utf-8'):
        """
        安全文件操作上下文管理器
        
        参数:
            filename (str): 文件名
            mode (str): 文件打开模式
            encoding (str): 文件编码
        """
        file_handle = None
        backup_filename = None
        temp_filename = None
        
        try:
            print(f"开始安全文件操作: {filename}")
            
            # 如果是写入操作，先创建备份
            if 'w' in mode or 'a' in mode:
                if os.path.exists(filename):
                    # 创建备份
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    name, ext = os.path.splitext(os.path.basename(filename))
                    backup_filename = os.path.join(
                        self.backup_dir, 
                        f"{name}_{timestamp}{ext}"
                    )
                    
                    # 复制文件作为备份
                    with open(filename, 'rb') as src, open(backup_filename, 'wb') as dst:
                        dst.write(src.read())
                    print(f"已创建备份: {backup_filename}")
                
                # 创建临时文件进行写入
                temp_fd, temp_filename = tempfile.mkstemp(suffix=ext or '.tmp')
                file_handle = os.fdopen(temp_fd, mode, encoding=encoding)
                print(f"使用临时文件: {temp_filename}")
            else:
                # 读取操作直接打开文件
                file_handle = open(filename, mode, encoding=encoding)
                print(f"打开文件: {filename}")
            
            # 返回文件句柄
            yield file_handle
            
        except Exception as e:
            print(f"文件操作期间发生错误: {e}")
            # 如果有临时文件，删除它
            if temp_filename and os.path.exists(temp_filename):
                os.unlink(temp_filename)
                print(f"已删除临时文件: {temp_filename}")
            raise
        else:
            # 操作成功完成
            if temp_filename and os.path.exists(temp_filename):
                # 关闭文件
                if file_handle:
                    file_handle.close()
                
                # 原子性地替换原文件
                if os.path.exists(filename):
                    os.replace(temp_filename, filename)
                else:
                    os.rename(temp_filename, filename)
                print(f"已安全替换文件: {filename}")
        finally:
            # 确保文件被关闭
            if file_handle and not file_handle.closed:
                file_handle.close()
                print("文件句柄已关闭")
    
    def get_backup_list(self):
        """获取备份文件列表"""
        backups = []
        for filename in os.listdir(self.backup_dir):
            filepath = os.path.join(self.backup_dir, filename)
            if os.path.isfile(filepath):
                stat = os.stat(filepath)
                backups.append({
                    'filename': filename,
                    'filepath': filepath,
                    'size': stat.st_size,
                    'modified': datetime.fromtimestamp(stat.st_mtime)
                })
        return sorted(backups, key=lambda x: x['modified'], reverse=True)

# 使用contextlib创建更简单的文件管理器
@contextmanager
def managed_json_file(filename, mode='r'):
    """
    管理JSON文件的上下文管理器
    
    参数:
        filename (str): JSON文件名
        mode (str): 文件模式 ('r' 或 'w')
    """
    file_handle = None
    temp_filename = None
    
    try:
        if mode == 'w':
            # 写入模式使用临时文件
            temp_fd, temp_filename = tempfile.mkstemp(suffix='.json')
            file_handle = os.fdopen(temp_fd, 'w', encoding='utf-8')
        else:
            # 读取模式直接打开
            file_handle = open(filename, mode, encoding='utf-8')
        
        if mode == 'r':
            # 读取并解析JSON
            data = json.load(file_handle)
            yield data
        else:
            # 准备写入，返回一个可调用对象
            def write_json(data):
                json.dump(data, file_handle, ensure_ascii=False, indent=2)
            yield write_json
            
    except json.JSONDecodeError as e:
        raise FileProcessingError("JSON解析", filename, f"JSON格式错误: {e}")
    except Exception as e:
        # 清理临时文件
        if temp_filename and os.path.exists(temp_filename):
            os.unlink(temp_filename)
        raise
    else:
        # 写入成功，替换原文件
        if mode == 'w' and temp_filename:
            file_handle.close()  # 先关闭文件
            if os.path.exists(filename):
                os.replace(temp_filename, filename)
            else:
                os.rename(temp_filename, filename)
            print(f"JSON文件已安全写入: {filename}")
    finally:
        if file_handle and not file_handle.closed:
            file_handle.close()

# 使用文件管理器
print("===文件管理演示===")

# 创建文件管理器实例
file_manager = FileManager()

# 准备测试数据
test_config = {
    "app_name": "文件管理演示",
    "version": "1.0.0",
    "features": ["安全写入", "自动备份", "异常恢复"],
    "settings": {
        "debug": True,
        "max_file_size": 1024000
    }
}

# 1. 使用安全文件操作
print("1. 安全文件操作:")
try:
    # 写入配置文件
    with file_manager.safe_file_operation("config.json", "w") as f:
        json.dump(test_config, f, ensure_ascii=False, indent=2)
    print("配置文件写入成功")
    
    # 读取配置文件
    with file_manager.safe_file_operation("config.json", "r") as f:
        loaded_config = json.load(f)
    print(f"配置文件读取成功: {loaded_config['app_name']}")
    
except FileProcessingError as e:
    print(f"文件处理错误: {e}")
except Exception as e:
    print(f"未预期错误: {e}")

# 2. 使用JSON文件管理器
print("\n2. JSON文件管理器:")
try:
    # 写入JSON文件
    with managed_json_file("data.json", "w") as write_func:
        write_func({
            "users": [
                {"id": 1, "name": "张三", "email": "zhangsan@example.com"},
                {"id": 2, "name": "李四", "email": "lisi@example.com"}
            ],
            "created_at": datetime.now().isoformat()
        })
    print("JSON数据写入成功")
    
    # 读取JSON文件
    with managed_json_file("data.json", "r") as data:
        print(f"读取到 {len(data['users'])} 个用户")
        for user in data['users']:
            print(f"  - {user['name']} ({user['email']})")
            
except FileProcessingError as e:
    print(f"JSON处理错误: {e}")
except Exception as e:
    print(f"未预期错误: {e}")

# 演示异常处理和备份功能
print("\n===异常处理和备份演示===")

# 1. 演示备份功能
print("1. 备份功能演示:")
try:
    # 修改文件多次以创建多个备份
    for i in range(3):
        with file_manager.safe_file_operation("config.json", "w") as f:
            test_config["version"] = f"1.0.{i}"
            test_config["last_modified"] = datetime.now().isoformat()
            json.dump(test_config, f, ensure_ascii=False, indent=2)
        time.sleep(1)  # 确保时间戳不同
    
    # 查看备份
    backups = file_manager.get_backup_list()
    print(f"创建了 {len(backups)} 个备份:")
    for backup in backups[:3]:  # 只显示最近3个
        print(f"  - {backup['filename']} ({backup['size']} 字节, {backup['modified']})")
        
except Exception as e:
    print(f"备份演示错误: {e}")

# 2. 处理写入异常
print("\n2. 写入异常处理:")
try:
    with file_manager.safe_file_operation("protected_file.json", "w") as f:
        # 模拟写入过程中发生错误
        f.write('{"valid": "json"')
        # 故意不关闭对象，导致JSON格式错误
        raise ValueError("模拟写入过程中的错误")
except ValueError as e:
    print(f"写入过程中发生错误: {e}")
    print("检查文件是否保持原状，临时文件是否被清理")

# 3. 处理JSON格式错误
print("\n3. JSON格式错误处理:")
try:
    # 创建一个格式错误的JSON文件
    with open("invalid.json", "w", encoding="utf-8") as f:
        f.write("{invalid json content}")
    
    # 尝试读取
    with managed_json_file("invalid.json", "r") as data:
        print("意外成功读取无效JSON")
except FileProcessingError as e:
    print(f"JSON格式错误（正常）: {e}")
finally:
    # 清理测试文件
    if os.path.exists("invalid.json"):
        os.remove("invalid.json")

# 4. 演示原子性操作
print("\n4. 原子性操作演示:")
original_content = "这是原始内容\n"
try:
    # 创建原始文件
    with open("atomic_test.txt", "w", encoding="utf-8") as f:
        f.write(original_content)
    
    print("原始文件内容:")
    with open("atomic_test.txt", "r", encoding="utf-8") as f:
        print(f"  {repr(f.read())}")
    
    # 使用安全操作尝试修改文件，但在中途引发异常
    try:
        with file_manager.safe_file_operation("atomic_test.txt", "w") as f:
            f.write("这是新内容的第一行\n")
            f.write("这是新内容的第二行\n")
            # 模拟在写入过程中发生错误
            raise IOError("模拟磁盘写入错误")
    except IOError as e:
        print(f"写入过程中发生错误: {e}")
    
    # 检查文件是否保持原始状态
    print("错误发生后文件内容:")
    with open("atomic_test.txt", "r", encoding="utf-8") as f:
        content = f.read()
        print(f"  {repr(content)}")
        if content == original_content:
            print("原子性操作成功：文件保持原始状态")
        else:
            print("原子性操作失败：文件被部分修改")
            
except Exception as e:
    print(f"原子性演示错误: {e}")
finally:
    # 清理测试文件
    for filename in ["atomic_test.txt", "config.json", "data.json"]:
        if os.path.exists(filename):
            os.remove(filename)
```

### 代码说明

**案例1代码解释**：
1. `def __enter__(self):`：上下文管理器入口，负责初始化资源
2. `def __exit__(self, exc_type, exc_value, traceback):`：上下文管理器出口，负责清理资源
3. `with DatabaseConnection(...) as conn:`：使用with语句自动管理数据库连接
4. `return False`：在`__exit__`中返回False表示不抑制异常

如果在`__exit__`方法中返回True，会抑制所有异常，这通常不是我们想要的行为，会隐藏程序中的问题。

**案例2代码解释**：
1. `@contextmanager`：装饰器将函数转换为上下文管理器
2. `temp_fd, temp_filename = tempfile.mkstemp(suffix='.json')`：创建临时文件确保原子性写入
3. `os.replace(temp_filename, filename)`：原子性地替换原文件
4. `try...except...else...finally`：确保资源得到正确管理

如果直接写入目标文件而不是使用临时文件，当写入过程中发生异常时，原文件可能被破坏，而使用临时文件可以避免这个问题。

## 5. 最佳实践和注意事项

### 知识点解析

**概念定义**：最佳实践就像经验丰富的老师傅传授的工作技巧，帮助我们写出更可靠、更易维护的异常处理代码。注意事项则是容易踩坑的地方，提前了解可以避免犯错。

**核心规则**：
1. 只捕获能够处理的异常
2. 提供有意义的错误信息
3. 正确清理资源
4. 合理使用异常链
5. 记录重要的异常信息

**常见易错点**：
1. 滥用"捕获所有异常"模式
2. 忽视异常处理的性能影响
3. 在异常处理中再次引发异常
4. 忘记记录重要的错误信息
5. 过度使用自定义异常

### 实战案例

#### 案例1：API服务异常处理最佳实践
```python
# API服务异常处理最佳实践
print("===API服务异常处理最佳实践===")

import logging
import traceback
from datetime import datetime
from typing import Dict, Any, Optional

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# API异常定义
class APIError(Exception):
    """API错误基类"""
    def __init__(self, message: str, status_code: int = 500, error_code: str = None):
        self.message = message
        self.status_code = status_code
        self.error_code = error_code
        super().__init__(self.message)

class ValidationError(APIError):
    """验证错误"""
    def __init__(self, field: str, value: Any, message: str):
        self.field = field
        self.value = value
        error_message = f"字段 '{field}' 验证失败: {message}"
        super().__init__(error_message, 400, "VALIDATION_ERROR")

class AuthenticationError(APIError):
    """认证错误"""
    def __init__(self, message: str = "认证失败"):
        super().__init__(message, 401, "AUTHENTICATION_ERROR")

class AuthorizationError(APIError):
    """授权错误"""
    def __init__(self, message: str = "权限不足"):
        super().__init__(message, 403, "AUTHORIZATION_ERROR")

class ResourceNotFoundError(APIError):
    """资源未找到错误"""
    def __init__(self, resource_type: str, resource_id: Any):
        self.resource_type = resource_type
        self.resource_id = resource_id
        message = f"{resource_type} '{resource_id}' 未找到"
        super().__init__(message, 404, "RESOURCE_NOT_FOUND")

# API服务类
class APIService:
    """API服务"""
    
    def __init__(self):
        self.users = {
            1: {"id": 1, "name": "张三", "role": "admin", "active": True},
            2: {"id": 2, "name": "李四", "role": "user", "active": True},
            3: {"id": 3, "name": "王五", "role": "user", "active": False}
        }
        
        self.posts = {
            1: {"id": 1, "title": "第一篇文章", "author_id": 1, "content": "文章内容1"},
            2: {"id": 2, "title": "第二篇文章", "author_id": 2, "content": "文章内容2"}
        }
    
    def _log_error(self, error: Exception, context: Dict[str, Any] = None):
        """
        记录错误日志
        
        参数:
            error (Exception): 异常对象
            context (dict): 上下文信息
        """
        error_info = {
            "type": type(error).__name__,
            "message": str(error),
            "timestamp": datetime.now().isoformat(),
        }
        
        if context:
            error_info["context"] = context
        
        # 记录堆栈跟踪（仅在开发环境中）
        if logger.isEnabledFor(logging.DEBUG):
            error_info["traceback"] = traceback.format_exc()
        
        logger.error(f"API错误: {error_info}")
    
    def _validate_user_access(self, user_id: int, target_user_id: int = None, required_role: str = None):
        """
        验证用户访问权限
        
        参数:
            user_id (int): 当前用户ID
            target_user_id (int): 目标用户ID（可选）
            required_role (str): 所需角色（可选）
            
        异常:
            AuthenticationError: 认证失败
            AuthorizationError: 授权失败
        """
        # 验证用户是否存在
        if user_id not in self.users:
            raise AuthenticationError("用户不存在")
        
        user = self.users[user_id]
        
        # 验证用户是否激活
        if not user["active"]:
            raise AuthenticationError("用户账户已被禁用")
        
        # 验证角色权限
        if required_role and user["role"] != required_role:
            # 管理员有所有权限
            if user["role"] != "admin":
                raise AuthorizationError(f"需要 {required_role} 权限")
        
        # 验证是否可以访问目标用户
        if target_user_id and target_user_id != user_id:
            # 用户只能访问自己的数据，管理员可以访问所有数据
            if user["role"] != "admin":
                raise AuthorizationError("无权访问其他用户的数据")
    
    def get_user(self, current_user_id: int, target_user_id: int) -> Dict[str, Any]:
        """
        获取用户信息
        
        参数:
            current_user_id (int): 当前用户ID
            target_user_id (int): 目标用户ID
            
        返回:
            dict: 用户信息
            
        异常:
            AuthenticationError: 认证失败
            AuthorizationError: 授权失败
            ResourceNotFoundError: 用户未找到
        """
        context = {
            "operation": "get_user",
            "current_user_id": current_user_id,
            "target_user_id": target_user_id
        }
        
        try:
            # 验证访问权限
            self._validate_user_access(current_user_id, target_user_id)
            
            # 验证目标用户是否存在
            if target_user_id not in self.users:
                raise ResourceNotFoundError("用户", target_user_id)
            
            # 返回用户信息（不包含敏感信息）
            user = self.users[target_user_id].copy()
            user.pop("active", None)  # 移除激活状态信息
            return user
            
        except (AuthenticationError, AuthorizationError, ResourceNotFoundError):
            # 记录安全相关错误
            logger.warning(f"访问被拒绝: {context}")
            raise
        except Exception as e:
            # 记录未预期错误
            self._log_error(e, context)
            raise APIError("内部服务器错误", 500, "INTERNAL_ERROR") from e
    
    def create_post(self, user_id: int, title: str, content: str) -> Dict[str, Any]:
        """
        创建文章
        
        参数:
            user_id (int): 用户ID
            title (str): 文章标题
            content (str): 文章内容
            
        返回:
            dict: 创建的文章
            
        异常:
            AuthenticationError: 认证失败
            ValidationError: 验证失败
        """
        context = {
            "operation": "create_post",
            "user_id": user_id,
            "title": title
        }
        
        try:
            # 验证用户权限
            self._validate_user_access(user_id)
            
            # 验证输入数据
            if not title or not title.strip():
                raise ValidationError("title", title, "标题不能为空")
            
            if len(title) > 100:
                raise ValidationError("title", title, "标题不能超过100个字符")
            
            if not content or not content.strip():
                raise ValidationError("content", "[...]", "内容不能为空")
            
            if len(content) > 10000:
                raise ValidationError("content", f"[{len(content)} chars]", "内容不能超过10000个字符")
            
            # 创建文章
            new_id = max(self.posts.keys()) + 1 if self.posts else 1
            post = {
                "id": new_id,
                "title": title.strip(),
                "content": content.strip(),
                "author_id": user_id,
                "created_at": datetime.now().isoformat()
            }
            
            self.posts[new_id] = post
            logger.info(f"用户 {user_id} 创建了文章 {new_id}")
            return post
            
        except (AuthenticationError, ValidationError):
            # 直接重新抛出客户端错误
            raise
        except Exception as e:
            # 记录服务器错误
            self._log_error(e, context)
            raise APIError("内部服务器错误", 500, "INTERNAL_ERROR") from e
    
    def delete_post(self, user_id: int, post_id: int) -> bool:
        """
        删除文章
        
        参数:
            user_id (int): 用户ID
            post_id (int): 文章ID
            
        返回:
            bool: 是否删除成功
            
        异常:
            AuthenticationError: 认证失败
            AuthorizationError: 授权失败
            ResourceNotFoundError: 文章未找到
        """
        context = {
            "operation": "delete_post",
            "user_id": user_id,
            "post_id": post_id
        }
        
        try:
            # 验证用户权限
            self._validate_user_access(user_id)
            
            # 验证文章是否存在
            if post_id not in self.posts:
                raise ResourceNotFoundError("文章", post_id)
            
            post = self.posts[post_id]
            
            # 验证删除权限（只能删除自己的文章，管理员除外）
            user = self.users[user_id]
            if post["author_id"] != user_id and user["role"] != "admin":
                raise AuthorizationError("只能删除自己的文章")
            
            # 删除文章
            del self.posts[post_id]
            logger.info(f"用户 {user_id} 删除了文章 {post_id}")
            return True
            
        except (AuthenticationError, AuthorizationError, ResourceNotFoundError):
            # 记录安全相关错误
            logger.warning(f"删除操作被拒绝: {context}")
            raise
        except Exception as e:
            # 记录服务器错误
            self._log_error(e, context)
            raise APIError("内部服务器错误", 500, "INTERNAL_ERROR") from e

# API控制器（模拟Web框架的控制器）
class APIController:
    """API控制器"""
    
    def __init__(self):
        self.service = APIService()
    
    def handle_get_user(self, current_user_id: int, target_user_id: int) -> Dict[str, Any]:
        """
        处理获取用户请求
        
        参数:
            current_user_id (int): 当前用户ID
            target_user_id (int): 目标用户ID
            
        返回:
            dict: 响应数据
        """
        try:
            user = self.service.get_user(current_user_id, target_user_id)
            return {
                "success": True,
                "data": user,
                "status_code": 200
            }
        except AuthenticationError as e:
            return {
                "success": False,
                "error": {
                    "message": str(e),
                    "code": e.error_code,
                    "status_code": e.status_code
                },
                "status_code": e.status_code
            }
        except AuthorizationError as e:
            return {
                "success": False,
                "error": {
                    "message": str(e),
                    "code": e.error_code,
                    "status_code": e.status_code
                },
                "status_code": e.status_code
            }
        except ResourceNotFoundError as e:
            return {
                "success": False,
                "error": {
                    "message": str(e),
                    "code": e.error_code,
                    "status_code": e.status_code
                },
                "status_code": e.status_code
            }
        except APIError as e:
            # 记录服务器错误
            logger.error(f"服务器错误: {e}")
            return {
                "success": False,
                "error": {
                    "message": "内部服务器错误",
                    "code": e.error_code,
                    "status_code": e.status_code
                },
                "status_code": e.status_code
            }
    
    def handle_create_post(self, user_id: int, title: str, content: str) -> Dict[str, Any]:
        """
        处理创建文章请求
        
        参数:
            user_id (int): 用户ID
            title (str): 文章标题
            content (str): 文章内容
            
        返回:
            dict: 响应数据
        """
        try:
            post = self.service.create_post(user_id, title, content)
            return {
                "success": True,
                "data": post,
                "status_code": 201
            }
        except ValidationError as e:
            return {
                "success": False,
                "error": {
                    "message": str(e),
                    "code": e.error_code,
                    "status_code": e.status_code
                },
                "status_code": e.status_code
            }
        except AuthenticationError as e:
            return {
                "success": False,
                "error": {
                    "message": str(e),
                    "code": e.error_code,
                    "status_code": e.status_code
                },
                "status_code": e.status_code
            }
        except APIError as e:
            logger.error(f"服务器错误: {e}")
            return {
                "success": False,
                "error": {
                    "message": "内部服务器错误",
                    "code": e.error_code,
                    "status_code": e.status_code
                },
                "status_code": e.status_code
            }

# 使用API服务
print("===API服务演示===")

# 创建API控制器
controller = APIController()

# 正常操作
print("1. 正常API操作:")
try:
    # 用户1获取自己的信息
    response = controller.handle_get_user(1, 1)
    print(f"获取用户信息: {response}")
    
    # 用户1创建文章
    response = controller.handle_create_post(1, "我的新文章", "这是文章内容")
    print(f"创建文章: {response}")
    
except Exception as e:
    print(f"意外错误: {e}")

# 演示最佳实践
print("\n===最佳实践演示===")

# 1. 处理认证错误
print("1. 认证错误处理:")
response = controller.handle_get_user(999, 1)  # 不存在的用户
print(f"认证错误响应: {response}")

# 2. 处理授权错误
print("\n2. 授权错误处理:")
response = controller.handle_get_user(2, 1)  # 用户2试图访问用户1的信息
print(f"授权错误响应: {response}")

# 3. 处理验证错误
print("\n3. 验证错误处理:")
response = controller.handle_create_post(1, "", "内容")  # 空标题
print(f"验证错误响应: {response}")

response = controller.handle_create_post(1, "A" * 150, "内容")  # 标题过长
print(f"验证错误响应: {response}")

# 4. 处理资源未找到错误
print("\n4. 资源未找到错误处理:")
# 模拟直接调用服务方法来演示
try:
    user = controller.service.get_user(1, 999)  # 不存在的用户
    print(f"意外获取到用户: {user}")
except ResourceNotFoundError as e:
    print(f"资源未找到（正常）: {e}")

# 5. 演示错误日志记录
print("\n5. 错误日志记录演示:")
try:
    # 模拟一个会导致服务器错误的操作
    # 这里我们手动引发一个未预期的错误来演示日志记录
    raise ValueError("模拟服务器内部错误")
except ValueError as e:
    # 在实际应用中，这类错误会在服务层被捕获并记录
    logger.error(f"捕获到未预期错误: {e}")
    logger.debug("详细堆栈跟踪:", exc_info=True)

# 6. 演示异常链的正确使用
print("\n6. 异常链演示:")
try:
    try:
        # 底层操作失败
        raise ValueError("数据库连接失败")
    except ValueError as e:
        # 中层处理转换为业务异常
        raise APIError("服务暂时不可用", 503, "SERVICE_UNAVAILABLE") from e
except APIError as e:
    print(f"业务异常: {e}")
    print(f"原始异常: {e.__cause__}")
```

#### 案例2：异常处理性能和模式
```python
# 异常处理性能和模式
print("\n===异常处理性能和模式===")

import time
import logging
from contextlib import suppress

# 配置性能测试日志
perf_logger = logging.getLogger("performance")
perf_logger.setLevel(logging.INFO)

# 性能测试工具
def time_operation(operation, *args, **kwargs):
    """
    测量操作执行时间
    
    参数:
        operation: 要测量的函数
        *args, **kwargs: 传递给函数的参数
        
    返回:
        tuple: (结果, 执行时间)
    """
    start_time = time.perf_counter()
    try:
        result = operation(*args, **kwargs)
        end_time = time.perf_counter()
        return result, end_time - start_time
    except Exception as e:
        end_time = time.perf_counter()
        raise e.__class__(f"{e} (执行时间: {end_time - start_time:.6f}秒)") from e

# 测试数据
test_data = list(range(10000))

# 不同的错误处理模式
class ErrorHandlingPatterns:
    """错误处理模式演示"""
    
    @staticmethod
    def lookup_with_exception_handling(data, target):
        """
        使用异常处理的查找（EAFP - Easier to Ask for Forgiveness than Permission）
        
        参数:
            data (list): 数据列表
            target: 目标值
            
        返回:
            int: 索引或-1
        """
        try:
            return data.index(target)
        except ValueError:
            return -1
    
    @staticmethod
    def lookup_with_condition_check(data, target):
        """
        使用条件检查的查找（LBYL - Look Before You Leap）
        
        参数:
            data (list): 数据列表
            target: 目标值
            
        返回:
            int: 索引或-1
        """
        if target in data:
            return data.index(target)
        else:
            return -1
    
    @staticmethod
    def safe_division_with_exception(dividend, divisor):
        """
        使用异常处理的安全除法
        
        参数:
            dividend: 被除数
            divisor: 除数
            
        返回:
            float: 结果或None
        """
        try:
            return dividend / divisor
        except ZeroDivisionError:
            return None
    
    @staticmethod
    def safe_division_with_check(dividend, divisor):
        """
        使用条件检查的安全除法
        
        参数:
            dividend: 被除数
            divisor: 除数
            
        返回:
            float: 结果或None
        """
        if divisor == 0:
            return None
        return dividend / divisor
    
    @staticmethod
    def process_items_with_exceptions(items):
        """
        使用异常处理处理项目列表
        
        参数:
            items (list): 项目列表
            
        返回:
            tuple: (成功数量, 失败数量)
        """
        success_count = 0
        failure_count = 0
        
        for item in items:
            try:
                # 模拟可能失败的处理
                if item < 0:
                    raise ValueError(f"负数不被允许: {item}")
                if item % 1000 == 777:
                    raise RuntimeError(f"特殊数字导致错误: {item}")
                
                # 模拟处理
                result = item ** 2
                success_count += 1
            except (ValueError, RuntimeError) as e:
                failure_count += 1
                # 记录但不中断处理
                if failure_count <= 5:  # 只记录前几个错误
                    perf_logger.warning(f"处理项目时出错: {e}")
        
        return success_count, failure_count
    
    @staticmethod
    def process_items_without_exceptions(items):
        """
        不使用异常处理处理项目列表
        
        参数:
            items (list): 项目列表
            
        返回:
            tuple: (成功数量, 失败数量)
        """
        success_count = 0
        failure_count = 0
        
        for item in items:
            # 使用条件检查而不是异常处理
            if item < 0:
                failure_count += 1
                if failure_count <= 5:
                    perf_logger.warning(f"跳过负数: {item}")
                continue
            
            if item % 1000 == 777:
                failure_count += 1
                if failure_count <= 5:
                    perf_logger.warning(f"跳过特殊数字: {item}")
                continue
            
            # 模拟处理
            result = item ** 2
            success_count += 1
        
        return success_count, failure_count

# 性能比较
print("===性能比较===")

patterns = ErrorHandlingPatterns()

# 1. 查找操作性能比较
print("1. 查找操作性能比较:")

# 测试异常处理方式
target_exists = 5000
target_not_exists = -1

result1, time1 = time_operation(
    patterns.lookup_with_exception_handling, 
    test_data, 
    target_exists
)
print(f"  异常处理方式（找到）: {result1}, 时间: {time1:.6f}秒")

result2, time2 = time_operation(
    patterns.lookup_with_exception_handling, 
    test_data, 
    target_not_exists
)
print(f"  异常处理方式（未找到）: {result2}, 时间: {time2:.6f}秒")

# 测试条件检查方式
result3, time3 = time_operation(
    patterns.lookup_with_condition_check, 
    test_data, 
    target_exists
)
print(f"  条件检查方式（找到）: {result3}, 时间: {time3:.6f}秒")

result4, time4 = time_operation(
    patterns.lookup_with_condition_check, 
    test_data, 
    target_not_exists
)
print(f"  条件检查方式（未找到）: {result4}, 时间: {time4:.6f}秒")

# 2. 除法操作性能比较
print("\n2. 除法操作性能比较:")

# 测试异常处理方式
result5, time5 = time_operation(
    patterns.safe_division_with_exception, 
    100, 
    5
)
print(f"  异常处理方式（正常）: {result5}, 时间: {time5:.6f}秒")

result6, time6 = time_operation(
    patterns.safe_division_with_exception, 
    100, 
    0
)
print(f"  异常处理方式（除零）: {result6}, 时间: {time6:.6f}秒")

# 测试条件检查方式
result7, time7 = time_operation(
    patterns.safe_division_with_check, 
    100, 
    5
)
print(f"  条件检查方式（正常）: {result7}, 时间: {time7:.6f}秒")

result8, time8 = time_operation(
    patterns.safe_division_with_check, 
    100, 
    0
)
print(f"  条件检查方式（除零）: {result8}, 时间: {time8:.6f}秒")

# 3. 批量处理性能比较
print("\n3. 批量处理性能比较:")

# 准备测试数据（包含一些会导致错误的数据）
test_items = list(range(1000)) + [-1, -2, 777, 1777, 2777]

result9, time9 = time_operation(
    patterns.process_items_with_exceptions, 
    test_items
)
print(f"  异常处理方式: 成功{result9[0]}, 失败{result9[1]}, 时间: {time9:.6f}秒")

result10, time10 = time_operation(
    patterns.process_items_without_exceptions, 
    test_items
)
print(f"  条件检查方式: 成功{result10[0]}, 失败{result10[1]}, 时间: {time10:.6f}秒")

# 最佳实践演示
print("\n===最佳实践演示===")

# 1. 使用contextlib.suppress简化异常处理
print("1. 使用contextlib.suppress:")

# 传统方式
print("  传统方式:")
try:
    result = int("abc")
except ValueError:
    result = 0
print(f"    结果: {result}")

# 使用suppress
print("  使用suppress:")
with suppress(ValueError):
    result = int("abc")
else:
    result = 0
print(f"    结果: {result}")

# 2. 异常处理的粒度控制
print("\n2. 异常处理粒度控制:")

def process_data_granular(data):
    """细粒度异常处理"""
    results = []
    errors = []
    
    for i, item in enumerate(data):
        try:
            # 可能失败的操作1
            try:
                processed = item.upper()  # 字符串操作
            except AttributeError:
                processed = str(item).upper()
            
            # 可能失败的操作2
            try:
                length = len(processed)
            except TypeError:
                length = 0
            
            results.append((processed, length))
            
        except Exception as e:
            errors.append(f"项目 {i}: {e}")
    
    return results, errors

def process_data_coarse(data):
    """粗粒度异常处理"""
    try:
        results = []
        for item in data:
            processed = str(item).upper()
            length = len(processed)
            results.append((processed, length))
        return results, []
    except Exception as e:
        return [], [f"处理失败: {e}"]

# 测试数据
mixed_data = ["hello", 123, None, "world", [1, 2, 3]]

results1, errors1 = process_data_granular(mixed_data)
print(f"  细粒度处理: 结果{len(results1)}, 错误{len(errors1)}")
print(f"    结果: {results1}")
if errors1:
    print(f"    错误: {errors1}")

results2, errors2 = process_data_coarse(mixed_data)
print(f"  粗粒度处理: 结果{len(results2)}, 错误{len(errors2)}")
if errors2:
    print(f"    错误: {errors2}")

# 3. 异常信息的最佳实践
print("\n3. 异常信息最佳实践:")

# 不好的异常信息
try:
    user_id = "abc"
    age = int(user_id)  # 这会失败
except ValueError:
    print("  不好的做法: 转换失败")  # 信息不明确

# 好的异常信息
try:
    user_id = "abc"
    age = int(user_id)
except ValueError as e:
    print(f"  好的做法: 用户ID '{user_id}' 转换为年龄时失败: {e}")

# 4. 资源清理的最佳实践
print("\n4. 资源清理最佳实践:")

class Resource:
    """模拟资源"""
    def __init__(self, name):
        self.name = name
        self.is_open = True
        print(f"  打开资源: {self.name}")
    
    def close(self):
        if self.is_open:
            print(f"  关闭资源: {self.name}")
            self.is_open = False
    
    def __del__(self):
        self.close()

# 不好的资源管理
print("  不好的做法:")
def bad_resource_management():
    resource = Resource("数据库连接")
    # 模拟可能失败的操作
    raise ValueError("操作失败")
    resource.close()  # 这行不会执行

try:
    bad_resource_management()
except ValueError:
    print("  操作失败，但资源可能未正确关闭")

# 好的资源管理
print("\n  好的做法:")
def good_resource_management():
    resource = None
    try:
        resource = Resource("文件句柄")
        # 模拟可能失败的操作
        raise ValueError("操作失败")
    except ValueError:
        print("  捕获到错误")
        raise
    finally:
        if resource:
            resource.close()

try:
    good_resource_management()
except ValueError:
    print("  操作失败，但资源已正确关闭")

# 使用with语句的最佳资源管理
print("\n  使用with语句:")
class ManagedResource:
    def __init__(self, name):
        self.name = name
        self.is_open = True
        print(f"  创建资源: {self.name}")
    
    def __enter__(self):
        print(f"  进入资源上下文: {self.name}")
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        print(f"  退出资源上下文: {self.name}")
        self.is_open = False
        return False  # 不抑制异常

def best_resource_management():
    with ManagedResource("网络连接") as resource:
        # 模拟可能失败的操作
        raise ValueError("网络操作失败")

try:
    best_resource_management()
except ValueError:
    print("  操作失败，但资源已自动清理")

print("\n===总结===")
print("异常处理最佳实践:")
print("1. 只捕获能够处理的异常")
print("2. 提供有意义的错误信息")
print("3. 正确清理资源（使用with语句或finally）")
print("4. 合理使用异常链保留错误上下文")
print("5. 考虑性能影响，选择合适的错误处理模式")
print("6. 记录重要的错误信息用于调试")
print("7. 不要滥用自定义异常")
```

### 代码说明

**案例1代码解释**：
1. `class APIError(Exception):`：为API服务创建专门的异常基类
2. `def _log_error(self, error: Exception, context: Dict[str, Any] = None):`：集中处理错误日志记录
3. `except (AuthenticationError, AuthorizationError, ResourceNotFoundError):`：只捕获能够处理的特定异常
4. `raise APIError("内部服务器错误", 500, "INTERNAL_ERROR") from e`：使用异常链保留原始错误信息

如果在API服务中捕获所有异常(`except Exception`)而不区分类型，会隐藏具体问题，不利于调试和维护。

**案例2代码解释**：
1. `time_operation(operation, *args, **kwargs):`：性能测试工具函数
2. `with suppress(ValueError):`：使用contextlib.suppress简化异常处理
3. EAFP vs LBYL：演示了两种不同的错误处理哲学
4. `finally:`和`with`语句：确保资源得到正确清理

如果在性能敏感的代码中频繁使用异常处理（EAFP模式），而错误情况很少发生，可能比条件检查（LBYL模式）更慢，因为异常处理有额外开销。