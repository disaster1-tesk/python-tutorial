# Python单元测试知识点

## 1. 单元测试概述

单元测试是软件测试的一种，用于测试程序中最小可测试单元（通常是函数或方法）。

### 单元测试的重要性
- **早期发现问题**：在开发过程中及早发现和修复错误
- **提高代码质量**：确保代码按预期工作
- **便于重构**：提供安全网，支持代码重构
- **文档作用**：测试用例可以作为代码使用示例

### 测试驱动开发 (TDD)
```python
# TDD开发流程:
# 1. 编写测试
# 2. 运行测试(失败)
# 3. 编写刚好能让测试通过的实现
# 4. 运行测试(通过)
# 5. 重构代码
# 6. 重复以上步骤
```

## 2. unittest模块

unittest是Python标准库中的单元测试框架，基于JUnit模式。

### 基本测试类结构
```python
import unittest

class TestExample(unittest.TestCase):
    """测试示例类"""
    
    def setUp(self):
        """测试前的准备工作"""
        self.test_data = [1, 2, 3, 4, 5]
    
    def tearDown(self):
        """测试后的清理工作"""
        # 清理资源
        pass
    
    def test_example(self):
        """示例测试方法"""
        self.assertEqual(sum(self.test_data), 15)
    
    def test_another_example(self):
        """另一个示例测试方法"""
        self.assertIn(3, self.test_data)

# 运行测试
# if __name__ == '__main__':
#     unittest.main()
```

### 常用断言方法
```python
import unittest

class TestAssertions(unittest.TestCase):
    """断言方法示例"""
    
    def test_equality(self):
        """相等性断言"""
        self.assertEqual(1 + 1, 2)
        self.assertNotEqual(1 + 1, 3)
    
    def test_boolean(self):
        """布尔值断言"""
        self.assertTrue(True)
        self.assertFalse(False)
    
    def test_none(self):
        """None值断言"""
        self.assertIsNone(None)
        self.assertIsNotNone("not none")
    
    def test_membership(self):
        """成员关系断言"""
        self.assertIn('a', 'abc')
        self.assertNotIn('d', 'abc')
    
    def test_exceptions(self):
        """异常断言"""
        with self.assertRaises(ZeroDivisionError):
            1 / 0
        
        with self.assertRaises(ValueError) as context:
            int("not a number")
        self.assertIn("invalid literal", str(context.exception))
    
    def test_approximate_equality(self):
        """近似相等断言"""
        self.assertAlmostEqual(0.1 + 0.2, 0.3, places=7)
```

## 3. 编写测试用例

### 测试固件 (Fixtures)
```python
import unittest

class TestWithFixtures(unittest.TestCase):
    """带固件的测试示例"""
    
    @classmethod
    def setUpClass(cls):
        """测试类执行前运行一次"""
        print("设置测试类")
        cls.shared_resource = "共享资源"
    
    @classmethod
    def tearDownClass(cls):
        """测试类执行后运行一次"""
        print("清理测试类")
        cls.shared_resource = None
    
    def setUp(self):
        """每个测试方法前运行"""
        print("设置测试方法")
        self.test_list = [1, 2, 3]
    
    def tearDown(self):
        """每个测试方法后运行"""
        print("清理测试方法")
        self.test_list = None
    
    def test_list_append(self):
        """测试列表添加元素"""
        self.test_list.append(4)
        self.assertEqual(self.test_list, [1, 2, 3, 4])
    
    def test_list_length(self):
        """测试列表长度"""
        self.assertEqual(len(self.test_list), 3)
```

### 测试套件
```python
import unittest

class TestMath(unittest.TestCase):
    def test_addition(self):
        self.assertEqual(1 + 1, 2)
    
    def test_subtraction(self):
        self.assertEqual(5 - 3, 2)

class TestString(unittest.TestCase):
    def test_concatenation(self):
        self.assertEqual("Hello" + " " + "World", "Hello World")
    
    def test_uppercase(self):
        self.assertEqual("hello".upper(), "HELLO")

# 创建测试套件
def suite():
    suite = unittest.TestSuite()
    suite.addTest(TestMath('test_addition'))
    suite.addTest(TestString('test_concatenation'))
    return suite

# 运行测试套件
# if __name__ == '__main__':
#     runner = unittest.TextTestRunner()
#     runner.run(suite())
```

## 4. mock模块

mock模块用于创建模拟对象，替换真实对象进行测试。

### 基本Mock使用
```python
from unittest.mock import Mock, patch
import unittest

class TestWithMock(unittest.TestCase):
    """Mock使用示例"""
    
    def test_mock_object(self):
        """测试Mock对象"""
        # 创建Mock对象
        mock_obj = Mock()
        mock_obj.method.return_value = "mocked result"
        
        # 调用Mock方法
        result = mock_obj.method()
        self.assertEqual(result, "mocked result")
        
        # 验证方法被调用
        mock_obj.method.assert_called_once()
    
    def test_mock_attributes(self):
        """测试Mock属性"""
        mock_obj = Mock()
        mock_obj.attribute = "mocked attribute"
        self.assertEqual(mock_obj.attribute, "mocked attribute")
        
        # 动态设置属性
        mock_obj.dynamic_attr = 42
        self.assertEqual(mock_obj.dynamic_attr, 42)
```

### patch装饰器
```python
from unittest.mock import patch
import unittest
import requests

class WeatherService:
    """天气服务类"""
    def get_temperature(self, city):
        response = requests.get(f"http://api.weather.com/{city}")
        return response.json()['temperature']

class TestWeatherService(unittest.TestCase):
    """测试天气服务"""
    
    @patch('requests.get')
    def test_get_temperature(self, mock_get):
        """测试获取温度"""
        # 配置Mock响应
        mock_response = Mock()
        mock_response.json.return_value = {'temperature': 25}
        mock_get.return_value = mock_response
        
        # 测试
        service = WeatherService()
        temp = service.get_temperature('Beijing')
        self.assertEqual(temp, 25)
        
        # 验证requests.get被正确调用
        mock_get.assert_called_once_with('http://api.weather.com/Beijing')
```

## 5. pytest框架

pytest是第三方测试框架，比unittest更简洁。

### 基本pytest测试
```python
# test_example.py
import pytest

# pytest不需要继承任何类，函数名以test_开头即可

def add(a, b):
    """加法函数"""
    return a + b

def test_add():
    """测试加法"""
    assert add(2, 3) == 5
    assert add(-1, 1) == 0
    assert add(0, 0) == 0

def test_add_negative():
    """测试负数加法"""
    assert add(-2, -3) == -5

# pytest支持类形式的测试
class TestAdd:
    """加法测试类"""
    
    def test_add_positive(self):
        assert add(1, 2) == 3
    
    def test_add_zero(self):
        assert add(5, 0) == 5
```

### pytest fixtures
```python
import pytest

# fixtures用于设置测试环境
@pytest.fixture
def sample_data():
    """示例数据fixture"""
    return [1, 2, 3, 4, 5]

@pytest.fixture
def database_connection():
    """数据库连接fixture"""
    print("建立数据库连接")
    connection = "数据库连接对象"
    yield connection
    print("关闭数据库连接")

def test_with_fixture(sample_data):
    """使用fixture的测试"""
    assert len(sample_data) == 5
    assert sum(sample_data) == 15

def test_with_database(database_connection):
    """使用数据库fixture的测试"""
    assert database_connection == "数据库连接对象"
```

### 参数化测试
```python
import pytest

def multiply(a, b):
    """乘法函数"""
    return a * b

# 参数化测试
@pytest.mark.parametrize("a, b, expected", [
    (2, 3, 6),
    (0, 5, 0),
    (-1, 1, -1),
    (10, -2, -20),
])
def test_multiply(a, b, expected):
    """参数化测试乘法"""
    assert multiply(a, b) == expected

# 多参数化组合
@pytest.mark.parametrize("x", [1, 2, 3])
@pytest.mark.parametrize("y", [4, 5, 6])
def test_combination(x, y):
    """组合参数化测试"""
    result = x + y
    assert result > 0
```

## 6. 测试驱动开发(TDD)

TDD是一种先写测试再写实现的开发方法。

### TDD示例
```python
# 首先写测试
import unittest

class TestCalculator(unittest.TestCase):
    """计算器测试"""
    
    def setUp(self):
        self.calc = Calculator()
    
    def test_add(self):
        """测试加法"""
        result = self.calc.add(2, 3)
        self.assertEqual(result, 5)
    
    def test_subtract(self):
        """测试减法"""
        result = self.calc.subtract(5, 3)
        self.assertEqual(result, 2)

# 然后实现功能（使其通过测试）
class Calculator:
    """计算器类"""
    def add(self, a, b):
        """加法"""
        return a + b
    
    def subtract(self, a, b):
        """减法"""
        return a - b

# 重构优化
class Calculator:
    """计算器类"""
    def add(self, a, b):
        """加法"""
        if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
            raise TypeError("参数必须是数字")
        return a + b
    
    def subtract(self, a, b):
        """减法"""
        if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
            raise TypeError("参数必须是数字")
        return a - b
```

## 7. 代码覆盖率

代码覆盖率衡量测试用例对源代码的覆盖程度。

### 使用coverage.py
```bash
# 安装coverage
# pip install coverage

# 运行测试并生成覆盖率报告
# coverage run -m unittest test_module.py
# coverage report
# coverage html  # 生成HTML报告
```

### 覆盖率示例
```python
# math_utils.py
def is_even(number):
    """判断是否为偶数"""
    return number % 2 == 0

def is_positive(number):
    """判断是否为正数"""
    return number > 0

def factorial(n):
    """计算阶乘"""
    if n < 0:
        raise ValueError("阶乘不能计算负数")
    if n == 0 or n == 1:
        return 1
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result

# test_math_utils.py
import unittest
from math_utils import is_even, is_positive, factorial

class TestMathUtils(unittest.TestCase):
    def test_is_even(self):
        self.assertTrue(is_even(2))
        self.assertFalse(is_even(3))
    
    def test_is_positive(self):
        self.assertTrue(is_positive(5))
        self.assertFalse(is_positive(-1))
        self.assertFalse(is_positive(0))
    
    def test_factorial(self):
        self.assertEqual(factorial(0), 1)
        self.assertEqual(factorial(1), 1)
        self.assertEqual(factorial(5), 120)
        
        with self.assertRaises(ValueError):
            factorial(-1)
```

## 8. 实际应用场景

### Web API测试
```python
import unittest
from unittest.mock import Mock, patch
import json

class APIClient:
    """API客户端"""
    def __init__(self, base_url):
        self.base_url = base_url
    
    def get_user(self, user_id):
        """获取用户信息"""
        # 实际实现会使用requests等库
        pass

class TestAPIClient(unittest.TestCase):
    """API客户端测试"""
    
    def setUp(self):
        self.client = APIClient("https://api.example.com")
    
    @patch('requests.get')
    def test_get_user_success(self, mock_get):
        """测试成功获取用户"""
        # 模拟API响应
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'id': 1,
            'name': '张三',
            'email': 'zhangsan@example.com'
        }
        mock_get.return_value = mock_response
        
        # 测试
        user = self.client.get_user(1)
        self.assertEqual(user['name'], '张三')
    
    @patch('requests.get')
    def test_get_user_not_found(self, mock_get):
        """测试用户不存在"""
        # 模拟404响应
        mock_response = Mock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response
        
        # 测试
        with self.assertRaises(Exception):
            self.client.get_user(999)
```

### 数据库操作测试
```python
import unittest
from unittest.mock import Mock, patch

class UserRepository:
    """用户仓库"""
    def __init__(self, database):
        self.database = database
    
    def save_user(self, user):
        """保存用户"""
        return self.database.insert('users', user)
    
    def find_user(self, user_id):
        """查找用户"""
        return self.database.select('users', {'id': user_id})

class TestUserRepository(unittest.TestCase):
    """用户仓库测试"""
    
    def setUp(self):
        self.mock_db = Mock()
        self.repo = UserRepository(self.mock_db)
    
    def test_save_user(self):
        """测试保存用户"""
        user = {'name': '张三', 'email': 'zhangsan@example.com'}
        self.mock_db.insert.return_value = 1
        
        result = self.repo.save_user(user)
        self.assertEqual(result, 1)
        self.mock_db.insert.assert_called_once_with('users', user)
    
    def test_find_user(self):
        """测试查找用户"""
        expected_user = {'id': 1, 'name': '张三'}
        self.mock_db.select.return_value = expected_user
        
        user = self.repo.find_user(1)
        self.assertEqual(user, expected_user)
        self.mock_db.select.assert_called_once_with('users', {'id': 1})
```

## 9. 最佳实践

### 测试独立性
```python
import unittest

class TestIndependent(unittest.TestCase):
    """独立测试示例"""
    
    def test_sort_list(self):
        """测试列表排序"""
        original = [3, 1, 4, 1, 5]
        sorted_list = sorted(original)
        self.assertEqual(sorted_list, [1, 1, 3, 4, 5])
        # 确保原列表未被修改
        self.assertEqual(original, [3, 1, 4, 1, 5])
    
    def test_string_upper(self):
        """测试字符串大写"""
        original = "hello"
        upper_string = original.upper()
        self.assertEqual(upper_string, "HELLO")
        # 确保原字符串未被修改
        self.assertEqual(original, "hello")
```

### 测试数据管理
```python
import unittest
import json
import os

class TestDataManagement(unittest.TestCase):
    """测试数据管理"""
    
    @classmethod
    def setUpClass(cls):
        """准备测试数据文件"""
        cls.test_data = {
            'users': [
                {'id': 1, 'name': '张三'},
                {'id': 2, 'name': '李四'}
            ]
        }
        with open('test_data.json', 'w', encoding='utf-8') as f:
            json.dump(cls.test_data, f, ensure_ascii=False)
    
    @classmethod
    def tearDownClass(cls):
        """清理测试数据文件"""
        if os.path.exists('test_data.json'):
            os.remove('test_data.json')
    
    def test_load_test_data(self):
        """测试加载测试数据"""
        with open('test_data.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        self.assertEqual(data, self.test_data)
```

### 测试命名规范
```python
import unittest

class TestNamingConventions(unittest.TestCase):
    """测试命名规范"""
    
    def test_should_return_true_for_even_numbers(self):
        """测试偶数应该返回True"""
        self.assertTrue(is_even(2))
        self.assertTrue(is_even(4))
    
    def test_should_return_false_for_odd_numbers(self):
        """测试奇数应该返回False"""
        self.assertFalse(is_even(1))
        self.assertFalse(is_even(3))
    
    def test_should_raise_exception_for_negative_input(self):
        """测试负数输入应该抛出异常"""
        with self.assertRaises(ValueError):
            factorial(-1)
    
    def test_calculate_total_with_multiple_items(self):
        """测试计算多个商品总价"""
        items = [{'price': 10}, {'price': 20}, {'price': 30}]
        total = calculate_total(items)
        self.assertEqual(total, 60)
```

### 持续集成测试
```yaml
# .github/workflows/test.yml
# name: Tests
# 
# on: [push, pull_request]
# 
# jobs:
#   test:
#     runs-on: ubuntu-latest
#     
#     steps:
#     - uses: actions/checkout@v2
#     
#     - name: Set up Python
#       uses: actions/setup-python@v2
#       with:
#         python-version: 3.9
#     
#     - name: Install dependencies
#       run: |
#         pip install -r requirements.txt
#         pip install pytest coverage
#     
#     - name: Run tests
#       run: |
#         coverage run -m pytest
#         coverage report
#         coverage xml
#     
#     - name: Upload coverage
#       uses: codecov/codecov-action@v1
```

## 10. 测试策略和类型

### 单元测试 vs 集成测试 vs 端到端测试
```python
# 单元测试 - 测试最小单元
def test_add_function():
    assert add(2, 3) == 5

# 集成测试 - 测试模块间交互
def test_database_repository():
    db = MockDatabase()
    repo = UserRepository(db)
    user = repo.save_user({'name': '张三'})
    assert user.id is not None

# 端到端测试 - 测试完整业务流程
def test_user_registration_flow():
    # 模拟完整的用户注册流程
    response = client.post('/register', data={
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'password123'
    })
    assert response.status_code == 200
    assert '欢迎注册' in response.text
```

### 性能测试
```python
import time
import unittest

class TestPerformance(unittest.TestCase):
    """性能测试"""
    
    def test_function_performance(self):
        """测试函数性能"""
        start_time = time.time()
        result = expensive_function()
        end_time = time.time()
        
        execution_time = end_time - start_time
        self.assertLess(execution_time, 1.0)  # 应该在1秒内完成
        self.assertIsNotNone(result)
```

通过系统地学习和应用这些单元测试知识点，可以显著提高代码质量和开发效率，确保软件的稳定性和可靠性。