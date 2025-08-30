# Python单元测试知识点

## 1. 单元测试概述和unittest模块

### 知识点解析

**概念定义**：单元测试就像给程序的每个小功能点编写"考题"，通过这些考题来验证每个功能是否按预期工作。比如我们写了一个加法函数，单元测试就是编写一些测试用例来验证这个函数在各种情况下都能正确计算。

**核心规则**：
1. 每个测试应该独立且可重复执行
2. 测试应该覆盖正常情况和边界情况
3. 测试应该快速执行
4. 测试失败时应该提供清晰的错误信息

**常见易错点**：
1. 测试之间相互依赖导致测试不稳定
2. 忘记测试边界条件和异常情况
3. 测试数据准备和清理不当
4. 断言使用不正确导致测试结果不准确

### 实战案例

#### 案例1：计算器功能测试
```python
# 计算器功能测试
print("===计算器功能测试===")

import unittest

class Calculator:
    """计算器类"""
    
    def add(self, a, b):
        """
        加法运算
        
        参数:
            a (int/float): 第一个数
            b (int/float): 第二个数
            
        返回:
            int/float: 两数之和
        """
        # 类型检查
        if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
            raise TypeError("参数必须是数字")
        return a + b
    
    def subtract(self, a, b):
        """
        减法运算
        
        参数:
            a (int/float): 被减数
            b (int/float): 减数
            
        返回:
            int/float: 两数之差
        """
        # 类型检查
        if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
            raise TypeError("参数必须是数字")
        return a - b
    
    def multiply(self, a, b):
        """
        乘法运算
        
        参数:
            a (int/float): 第一个数
            b (int/float): 第二个数
            
        返回:
            int/float: 两数之积
        """
        # 类型检查
        if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
            raise TypeError("参数必须是数字")
        return a * b
    
    def divide(self, a, b):
        """
        除法运算
        
        参数:
            a (int/float): 被除数
            b (int/float): 除数
            
        返回:
            float: 两数之商
            
        异常:
            TypeError: 参数不是数字时抛出
            ZeroDivisionError: 除数为0时抛出
        """
        # 类型检查
        if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
            raise TypeError("参数必须是数字")
        
        # 除零检查
        if b == 0:
            raise ZeroDivisionError("除数不能为零")
        
        return a / b

class TestCalculator(unittest.TestCase):
    """计算器测试类"""
    
    def setUp(self):
        """测试前的准备工作"""
        print("初始化计算器测试...")
        self.calculator = Calculator()
    
    def tearDown(self):
        """测试后的清理工作"""
        print("清理计算器测试...")
        self.calculator = None
    
    def test_add_positive_numbers(self):
        """测试正数加法"""
        result = self.calculator.add(2, 3)
        self.assertEqual(result, 5)
        print(f"正数加法测试通过: 2 + 3 = {result}")
    
    def test_add_negative_numbers(self):
        """测试负数加法"""
        result = self.calculator.add(-2, -3)
        self.assertEqual(result, -5)
        print(f"负数加法测试通过: -2 + (-3) = {result}")
    
    def test_add_mixed_numbers(self):
        """测试正负数混合加法"""
        result = self.calculator.add(5, -3)
        self.assertEqual(result, 2)
        print(f"混合加法测试通过: 5 + (-3) = {result}")
    
    def test_subtract_numbers(self):
        """测试减法"""
        result = self.calculator.subtract(10, 3)
        self.assertEqual(result, 7)
        print(f"减法测试通过: 10 - 3 = {result}")
    
    def test_multiply_numbers(self):
        """测试乘法"""
        result = self.calculator.multiply(4, 5)
        self.assertEqual(result, 20)
        print(f"乘法测试通过: 4 * 5 = {result}")
    
    def test_divide_numbers(self):
        """测试除法"""
        result = self.calculator.divide(15, 3)
        self.assertEqual(result, 5.0)
        print(f"除法测试通过: 15 / 3 = {result}")
    
    def test_divide_by_zero(self):
        """测试除零异常"""
        with self.assertRaises(ZeroDivisionError) as context:
            self.calculator.divide(10, 0)
        self.assertIn("除数不能为零", str(context.exception))
        print("除零异常测试通过")
    
    def test_invalid_input_types(self):
        """测试无效输入类型"""
        with self.assertRaises(TypeError) as context:
            self.calculator.add("2", 3)
        self.assertIn("参数必须是数字", str(context.exception))
        print("类型错误测试通过")
    
    def test_calculator_properties(self):
        """测试计算器属性"""
        # 测试计算器对象不为None
        self.assertIsNotNone(self.calculator)
        print("计算器对象存在性测试通过")

# 运行测试
if __name__ == "__main__":
    # 创建测试套件
    suite = unittest.TestLoader().loadTestsFromTestCase(TestCalculator)
    
    # 创建测试运行器
    runner = unittest.TextTestRunner(verbosity=2)
    
    # 运行测试
    print("开始运行计算器测试...")
    result = runner.run(suite)
    
    # 输出测试结果统计
    print(f"\n测试结果统计:")
    print(f"运行测试数: {result.testsRun}")
    print(f"失败数: {len(result.failures)}")
    print(f"错误数: {len(result.errors)}")
    print(f"成功率: {((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100):.1f}%" if result.testsRun > 0 else "无测试运行")
```

#### 案例2：用户管理系统测试
```python
# 用户管理系统测试
print("\n===用户管理系统测试===")

import unittest
from unittest.mock import Mock, patch

class User:
    """用户类"""
    
    def __init__(self, user_id, username, email):
        """
        初始化用户
        
        参数:
            user_id (int): 用户ID
            username (str): 用户名
            email (str): 邮箱
        """
        self.user_id = user_id
        self.username = username
        self.email = email
        self.is_active = True
    
    def deactivate(self):
        """停用用户"""
        self.is_active = False
    
    def activate(self):
        """激活用户"""
        self.is_active = True
    
    def to_dict(self):
        """转换为字典"""
        return {
            "user_id": self.user_id,
            "username": self.username,
            "email": self.email,
            "is_active": self.is_active
        }

class UserService:
    """用户服务类"""
    
    def __init__(self, database):
        """
        初始化用户服务
        
        参数:
            database: 数据库连接对象
        """
        self.database = database
    
    def create_user(self, username, email):
        """
        创建用户
        
        参数:
            username (str): 用户名
            email (str): 邮箱
            
        返回:
            User: 创建的用户对象
            
        异常:
            ValueError: 用户名或邮箱无效时抛出
        """
        # 验证输入
        if not username or not username.strip():
            raise ValueError("用户名不能为空")
        
        if not email or "@" not in email:
            raise ValueError("邮箱格式无效")
        
        # 检查用户是否已存在
        existing_user = self.database.find_user_by_email(email)
        if existing_user:
            raise ValueError("邮箱已被使用")
        
        # 创建用户
        user_id = self.database.insert_user(username, email)
        return User(user_id, username, email)
    
    def get_user(self, user_id):
        """
        获取用户
        
        参数:
            user_id (int): 用户ID
            
        返回:
            User: 用户对象
        """
        user_data = self.database.get_user(user_id)
        if not user_data:
            return None
        return User(
            user_data["user_id"],
            user_data["username"],
            user_data["email"]
        )
    
    def deactivate_user(self, user_id):
        """
        停用用户
        
        参数:
            user_id (int): 用户ID
            
        返回:
            bool: 是否成功停用
        """
        return self.database.deactivate_user(user_id)

class DatabaseMock:
    """数据库模拟类"""
    
    def __init__(self):
        """初始化数据库模拟"""
        self.users = {}
        self.next_id = 1
    
    def insert_user(self, username, email):
        """模拟插入用户"""
        user_id = self.next_id
        self.users[user_id] = {
            "user_id": user_id,
            "username": username,
            "email": email,
            "is_active": True
        }
        self.next_id += 1
        return user_id
    
    def find_user_by_email(self, email):
        """模拟根据邮箱查找用户"""
        for user in self.users.values():
            if user["email"] == email:
                return user
        return None
    
    def get_user(self, user_id):
        """模拟获取用户"""
        return self.users.get(user_id)
    
    def deactivate_user(self, user_id):
        """模拟停用用户"""
        if user_id in self.users:
            self.users[user_id]["is_active"] = False
            return True
        return False

class TestUserService(unittest.TestCase):
    """用户服务测试类"""
    
    def setUp(self):
        """测试前的准备工作"""
        print("初始化用户服务测试...")
        self.database = DatabaseMock()
        self.user_service = UserService(self.database)
    
    def tearDown(self):
        """测试后的清理工作"""
        print("清理用户服务测试...")
        self.database = None
        self.user_service = None
    
    def test_create_user_success(self):
        """测试成功创建用户"""
        user = self.user_service.create_user("张三", "zhangsan@example.com")
        
        # 验证返回的用户对象
        self.assertIsInstance(user, User)
        self.assertEqual(user.username, "张三")
        self.assertEqual(user.email, "zhangsan@example.com")
        self.assertTrue(user.is_active)
        print(f"用户创建成功: {user.username} ({user.email})")
    
    def test_create_user_with_invalid_username(self):
        """测试使用无效用户名创建用户"""
        with self.assertRaises(ValueError) as context:
            self.user_service.create_user("", "test@example.com")
        self.assertIn("用户名不能为空", str(context.exception))
        print("无效用户名测试通过")
    
    def test_create_user_with_invalid_email(self):
        """测试使用无效邮箱创建用户"""
        with self.assertRaises(ValueError) as context:
            self.user_service.create_user("李四", "invalid-email")
        self.assertIn("邮箱格式无效", str(context.exception))
        print("无效邮箱测试通过")
    
    def test_create_duplicate_user(self):
        """测试创建重复用户"""
        # 先创建一个用户
        self.user_service.create_user("王五", "wangwu@example.com")
        
        # 尝试使用相同邮箱创建用户
        with self.assertRaises(ValueError) as context:
            self.user_service.create_user("王五2", "wangwu@example.com")
        self.assertIn("邮箱已被使用", str(context.exception))
        print("重复用户测试通过")
    
    def test_get_user_success(self):
        """测试成功获取用户"""
        # 先创建用户
        created_user = self.user_service.create_user("赵六", "zhaoliu@example.com")
        
        # 获取用户
        retrieved_user = self.user_service.get_user(created_user.user_id)
        
        # 验证获取的用户
        self.assertIsNotNone(retrieved_user)
        self.assertEqual(retrieved_user.user_id, created_user.user_id)
        self.assertEqual(retrieved_user.username, "赵六")
        self.assertEqual(retrieved_user.email, "zhaoliu@example.com")
        print(f"用户获取成功: {retrieved_user.username}")
    
    def test_get_nonexistent_user(self):
        """测试获取不存在的用户"""
        user = self.user_service.get_user(999)
        self.assertIsNone(user)
        print("不存在用户测试通过")
    
    def test_deactivate_user(self):
        """测试停用用户"""
        # 创建用户
        user = self.user_service.create_user("钱七", "qianqi@example.com")
        
        # 停用用户
        result = self.user_service.deactivate_user(user.user_id)
        
        # 验证结果
        self.assertTrue(result)
        
        # 验证用户状态
        retrieved_user = self.user_service.get_user(user.user_id)
        self.assertFalse(retrieved_user.is_active)
        print(f"用户停用成功: {retrieved_user.username}")

# 运行测试
if __name__ == "__main__":
    # 创建测试套件
    suite = unittest.TestLoader().loadTestsFromTestCase(TestUserService)
    
    # 创建测试运行器
    runner = unittest.TextTestRunner(verbosity=2)
    
    # 运行测试
    print("开始运行用户服务测试...")
    result = runner.run(suite)
    
    # 输出测试结果统计
    print(f"\n测试结果统计:")
    print(f"运行测试数: {result.testsRun}")
    print(f"失败数: {len(result.failures)}")
    print(f"错误数: {len(result.errors)}")
    print(f"成功率: {((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100):.1f}%" if result.testsRun > 0 else "无测试运行")
```

### 代码说明

**案例1代码解释**：
1. `self.assertEqual(result, 5)`：断言两个值相等
2. `with self.assertRaises(ZeroDivisionError) as context:`：断言会抛出特定异常
3. `self.assertIn("除数不能为零", str(context.exception))`：断言异常信息包含特定内容
4. `setUp()`和`tearDown()`：每个测试方法执行前后的准备和清理工作

如果忘记在测试方法名前加`test_`前缀，unittest不会自动运行这些测试方法。

**案例2代码解释**：
1. `self.assertIsInstance(user, User)`：断言对象是指定类型
2. `self.assertIsNotNone(retrieved_user)`：断言对象不为None
3. `DatabaseMock`：模拟数据库操作，避免真实数据库依赖
4. `unittest.mock.Mock`：创建模拟对象用于测试

如果在真实项目中直接连接数据库进行测试，会因为网络问题、数据库状态等因素导致测试不稳定。

## 2. pytest框架和mock模块

### 知识点解析

**概念定义**：pytest是一个更现代、更简洁的Python测试框架，相比unittest写法更简单。mock模块则像"演员替身"，在测试时可以替换掉真实的复杂对象，让我们专注于测试目标功能。

**核心规则**：
1. pytest测试函数以test_开头
2. 使用assert语句进行断言
3. 使用fixture管理测试资源
4. mock用于替换真实对象进行测试

**常见易错点**：
1. 忘记安装pytest第三方库
2. fixture作用域使用不当
3. mock对象行为设置不正确
4. 测试函数命名不符合pytest规范

### 实战案例

#### 案例1：使用pytest进行测试
```python
# 使用pytest进行测试
print("===使用pytest进行测试===")

# 注意：需要先安装pytest: pip install pytest

try:
    import pytest
    PYTEST_AVAILABLE = True
except ImportError:
    PYTEST_AVAILABLE = False
    print("提示: 未安装pytest库，请运行 'pip install pytest' 安装")

if PYTEST_AVAILABLE:
    # 数学计算模块
    class MathUtils:
        """数学工具类"""
        
        @staticmethod
        def factorial(n):
            """
            计算阶乘
            
            参数:
                n (int): 要计算阶乘的数
                
            返回:
                int: n的阶乘
                
            异常:
                ValueError: n为负数时抛出
                TypeError: n不是整数时抛出
            """
            # 类型检查
            if not isinstance(n, int):
                raise TypeError("参数必须是整数")
            
            # 范围检查
            if n < 0:
                raise ValueError("不能计算负数的阶乘")
            
            # 计算阶乘
            if n == 0 or n == 1:
                return 1
            
            result = 1
            for i in range(2, n + 1):
                result *= i
            return result
        
        @staticmethod
        def is_prime(n):
            """
            判断是否为质数
            
            参数:
                n (int): 要判断的数
                
            返回:
                bool: 是否为质数
            """
            if not isinstance(n, int) or n < 2:
                return False
            
            if n == 2:
                return True
            
            if n % 2 == 0:
                return False
            
            # 只需检查到sqrt(n)
            for i in range(3, int(n ** 0.5) + 1, 2):
                if n % i == 0:
                    return False
            return True
    
    # pytest fixtures
    @pytest.fixture
    def math_utils():
        """数学工具fixture"""
        return MathUtils()
    
    @pytest.fixture
    def sample_numbers():
        """示例数字fixture"""
        return [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    
    # 测试函数
    def test_factorial_basic(math_utils):
        """测试基本阶乘计算"""
        assert math_utils.factorial(0) == 1
        assert math_utils.factorial(1) == 1
        assert math_utils.factorial(5) == 120
        print("基本阶乘测试通过")
    
    def test_factorial_exceptions(math_utils):
        """测试阶乘异常情况"""
        # 测试负数
        with pytest.raises(ValueError, match="不能计算负数的阶乘"):
            math_utils.factorial(-1)
        
        # 测试非整数
        with pytest.raises(TypeError, match="参数必须是整数"):
            math_utils.factorial(3.14)
        
        print("阶乘异常测试通过")
    
    def test_is_prime_basic(math_utils):
        """测试基本质数判断"""
        # 测试质数
        assert math_utils.is_prime(2) == True
        assert math_utils.is_prime(3) == True
        assert math_utils.is_prime(17) == True
        assert math_utils.is_prime(97) == True
        
        # 测试非质数
        assert math_utils.is_prime(1) == False
        assert math_utils.is_prime(4) == False
        assert math_utils.is_prime(15) == False
        assert math_utils.is_prime(100) == False
        
        print("质数判断测试通过")
    
    def test_is_prime_with_sample_numbers(math_utils, sample_numbers):
        """使用fixture测试质数判断"""
        prime_count = 0
        for num in sample_numbers:
            if math_utils.is_prime(num):
                prime_count += 1
        
        # 0-10中的质数有: 2, 3, 5, 7 (共4个)
        assert prime_count == 4
        print(f"样本数字质数测试通过，找到 {prime_count} 个质数")
    
    # 参数化测试
    @pytest.mark.parametrize("n, expected", [
        (0, 1),
        (1, 1),
        (2, 2),
        (3, 6),
        (4, 24),
        (5, 120),
    ])
    def test_factorial_parametrized(math_utils, n, expected):
        """参数化测试阶乘"""
        assert math_utils.factorial(n) == expected
        print(f"参数化阶乘测试通过: {n}! = {expected}")
    
    # 条件测试
    @pytest.mark.slow
    def test_large_factorial(math_utils):
        """测试大数阶乘(标记为慢测试)"""
        result = math_utils.factorial(10)
        assert result == 3628800
        print(f"大数阶乘测试通过: 10! = {result}")
    
    print("pytest测试示例创建完成")
    print("要运行测试，请在终端执行: pytest -v")
else:
    print("由于未安装pytest，跳过pytest示例")
```

#### 案例2：使用mock进行测试
```python
# 使用mock进行测试
print("\n===使用mock进行测试===")

try:
    import unittest
    from unittest.mock import Mock, patch, MagicMock
    MOCK_AVAILABLE = True
except ImportError:
    MOCK_AVAILABLE = False
    print("提示: 无法导入unittest.mock模块")

if MOCK_AVAILABLE:
    import requests
    
    class WeatherService:
        """天气服务类"""
        
        def __init__(self, api_key):
            """
            初始化天气服务
            
            参数:
                api_key (str): API密钥
            """
            self.api_key = api_key
            self.base_url = "https://api.weather.com/v1"
        
        def get_current_temperature(self, city):
            """
            获取城市当前温度
            
            参数:
                city (str): 城市名
                
            返回:
                float: 当前温度
                
            异常:
                Exception: API调用失败时抛出
            """
            try:
                # 构建API URL
                url = f"{self.base_url}/weather"
                params = {
                    "city": city,
                    "apikey": self.api_key
                }
                
                # 发送HTTP请求
                response = requests.get(url, params=params, timeout=10)
                
                # 检查响应状态
                if response.status_code == 200:
                    data = response.json()
                    return data["temperature"]
                else:
                    raise Exception(f"API调用失败，状态码: {response.status_code}")
                    
            except requests.RequestException as e:
                raise Exception(f"网络请求失败: {str(e)}")
            except KeyError:
                raise Exception("响应数据格式错误")
    
    class TestWeatherService(unittest.TestCase):
        """天气服务测试类"""
        
        def setUp(self):
            """测试前的准备工作"""
            self.api_key = "test_api_key"
            self.weather_service = WeatherService(self.api_key)
        
        @patch('requests.get')
        def test_get_current_temperature_success(self, mock_get):
            """测试成功获取温度"""
            # 配置mock对象
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = {
                "temperature": 25.5,
                "humidity": 60,
                "description": "晴天"
            }
            mock_get.return_value = mock_response
            
            # 执行测试
            temperature = self.weather_service.get_current_temperature("北京")
            
            # 验证结果
            self.assertEqual(temperature, 25.5)
            
            # 验证mock被正确调用
            mock_get.assert_called_once()
            args, kwargs = mock_get.call_args
            self.assertEqual(args[0], "https://api.weather.com/v1/weather")
            self.assertEqual(kwargs['params']['city'], "北京")
            self.assertEqual(kwargs['params']['apikey'], self.api_key)
            
            print("成功获取温度测试通过")
        
        @patch('requests.get')
        def test_get_current_temperature_api_error(self, mock_get):
            """测试API错误"""
            # 配置mock对象返回错误状态码
            mock_response = Mock()
            mock_response.status_code = 404
            mock_get.return_value = mock_response
            
            # 执行测试并验证异常
            with self.assertRaises(Exception) as context:
                self.weather_service.get_current_temperature("未知城市")
            
            self.assertIn("API调用失败", str(context.exception))
            print("API错误测试通过")
        
        @patch('requests.get')
        def test_get_current_temperature_network_error(self, mock_get):
            """测试网络错误"""
            # 配置mock对象抛出网络异常
            mock_get.side_effect = requests.RequestException("网络连接失败")
            
            # 执行测试并验证异常
            with self.assertRaises(Exception) as context:
                self.weather_service.get_current_temperature("北京")
            
            self.assertIn("网络请求失败", str(context.exception))
            print("网络错误测试通过")
        
        @patch('requests.get')
        def test_get_current_temperature_invalid_response(self, mock_get):
            """测试无效响应数据"""
            # 配置mock对象返回无效数据(缺少temperature字段)
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = {
                "humidity": 60,
                "description": "晴天"
            }
            mock_get.return_value = mock_response
            
            # 执行测试并验证异常
            with self.assertRaises(Exception) as context:
                self.weather_service.get_current_temperature("北京")
            
            self.assertIn("响应数据格式错误", str(context.exception))
            print("无效响应测试通过")
    
    # 运行测试
    if __name__ == "__main__":
        # 创建测试套件
        suite = unittest.TestLoader().loadTestsFromTestCase(TestWeatherService)
        
        # 创建测试运行器
        runner = unittest.TextTestRunner(verbosity=2)
        
        # 运行测试
        print("开始运行天气服务mock测试...")
        result = runner.run(suite)
        
        # 输出测试结果统计
        print(f"\n测试结果统计:")
        print(f"运行测试数: {result.testsRun}")
        print(f"失败数: {len(result.failures)}")
        print(f"错误数: {len(result.errors)}")
        print(f"成功率: {((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100):.1f}%" if result.testsRun > 0 else "无测试运行")
else:
    print("由于无法导入mock模块，跳过mock示例")
```

### 代码说明

**案例1代码解释**：
1. `@pytest.fixture`：定义测试固件，用于提供测试所需的资源
2. `@pytest.mark.parametrize`：参数化测试，一次测试多个数据组合
3. `assert math_utils.factorial(5) == 120`：使用assert进行断言
4. `with pytest.raises(ValueError, match="不能计算负数的阶乘")`：断言会抛出特定异常并匹配错误信息

如果pytest没有正确安装，测试将无法运行，需要先执行`pip install pytest`。

**案例2代码解释**：
1. `@patch('requests.get')`：装饰器，替换指定模块的函数为mock对象
2. `mock_response.json.return_value = {...}`：设置mock对象的方法返回值
3. `mock_get.assert_called_once()`：验证mock对象被调用了一次
4. `mock_get.side_effect = requests.RequestException("网络连接失败")`：设置mock对象抛出异常

如果忘记使用`@patch`装饰器，测试会实际发送网络请求，可能导致测试失败或运行缓慢。

## 3. 测试驱动开发和代码覆盖率

### 知识点解析

**概念定义**：测试驱动开发(TDD)就像"先出考题再写答案"的开发方式，先写测试用例定义功能要求，再编写代码让测试通过。代码覆盖率则是衡量测试完整性的一个指标，表示测试用例覆盖了多少源代码。

**核心规则**：
1. TDD遵循"红-绿-重构"循环：先写失败测试(红)，再写代码通过测试(绿)，最后优化代码
2. 代码覆盖率不是唯一质量指标，但有助于发现未测试的代码
3. 重点关注关键业务逻辑的覆盖率
4. 合理设定覆盖率目标，通常80%以上较为合适

**常见易错点**：
1. 为了追求高覆盖率而写无意义的测试
2. 忽视边界条件和异常情况的测试
3. 测试代码和实现代码混在一起
4. 不定期运行测试导致问题积累

### 实战案例

#### 案例1：测试驱动开发实践
```python
# 测试驱动开发实践
print("===测试驱动开发实践===")

import unittest

# 步骤1: 先写测试 (此时功能还未实现)
class TestBankAccount(unittest.TestCase):
    """银行账户测试类"""
    
    def test_create_account_with_initial_balance(self):
        """测试创建带初始余额的账户"""
        account = BankAccount("张三", 1000.0)
        self.assertEqual(account.owner, "张三")
        self.assertEqual(account.balance, 1000.0)
        print("创建账户测试通过")
    
    def test_deposit_money(self):
        """测试存款"""
        account = BankAccount("李四", 500.0)
        account.deposit(200.0)
        self.assertEqual(account.balance, 700.0)
        print("存款测试通过")
    
    def test_withdraw_money_success(self):
        """测试成功取款"""
        account = BankAccount("王五", 1000.0)
        account.withdraw(300.0)
        self.assertEqual(account.balance, 700.0)
        print("成功取款测试通过")
    
    def test_withdraw_money_insufficient_funds(self):
        """测试余额不足时取款"""
        account = BankAccount("赵六", 100.0)
        with self.assertRaises(ValueError) as context:
            account.withdraw(200.0)
        self.assertIn("余额不足", str(context.exception))
        print("余额不足取款测试通过")
    
    def test_get_transaction_history(self):
        """测试获取交易历史"""
        account = BankAccount("钱七", 500.0)
        account.deposit(100.0)
        account.withdraw(50.0)
        
        history = account.get_transaction_history()
        self.assertEqual(len(history), 3)  # 开户 + 存款 + 取款
        self.assertEqual(history[0]["type"], "开户")
        self.assertEqual(history[1]["type"], "存款")
        self.assertEqual(history[2]["type"], "取款")
        print("交易历史测试通过")

# 步骤2: 运行测试 (此时会失败，因为BankAccount类还未实现)
print("首先运行测试(应该会失败，因为功能还未实现)...")

# 步骤3: 实现功能让测试通过
class BankAccount:
    """银行账户类"""
    
    def __init__(self, owner, initial_balance=0.0):
        """
        初始化银行账户
        
        参数:
            owner (str): 账户所有者
            initial_balance (float): 初始余额
        """
        if initial_balance < 0:
            raise ValueError("初始余额不能为负数")
        
        self.owner = owner
        self.balance = initial_balance
        self.transactions = []
        
        # 记录开户交易
        self._record_transaction("开户", initial_balance, self.balance)
    
    def deposit(self, amount):
        """
        存款
        
        参数:
            amount (float): 存款金额
            
        异常:
            ValueError: 存款金额无效时抛出
        """
        if not isinstance(amount, (int, float)) or amount <= 0:
            raise ValueError("存款金额必须是正数")
        
        self.balance += amount
        self._record_transaction("存款", amount, self.balance)
    
    def withdraw(self, amount):
        """
        取款
        
        参数:
            amount (float): 取款金额
            
        异常:
            ValueError: 取款金额无效或余额不足时抛出
        """
        if not isinstance(amount, (int, float)) or amount <= 0:
            raise ValueError("取款金额必须是正数")
        
        if amount > self.balance:
            raise ValueError("余额不足")
        
        self.balance -= amount
        self._record_transaction("取款", amount, self.balance)
    
    def get_transaction_history(self):
        """
        获取交易历史
        
        返回:
            list: 交易历史列表
        """
        return self.transactions.copy()
    
    def _record_transaction(self, transaction_type, amount, balance_after):
        """
        记录交易(私有方法)
        
        参数:
            transaction_type (str): 交易类型
            amount (float): 交易金额
            balance_after (float): 交易后余额
        """
        import datetime
        transaction = {
            "type": transaction_type,
            "amount": amount,
            "balance_after": balance_after,
            "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        self.transactions.append(transaction)

# 步骤4: 再次运行测试 (此时应该通过)
print("\n实现功能后再次运行测试...")

# 运行测试
if __name__ == "__main__":
    # 创建测试套件
    suite = unittest.TestLoader().loadTestsFromTestCase(TestBankAccount)
    
    # 创建测试运行器
    runner = unittest.TextTestRunner(verbosity=2)
    
    # 运行测试
    print("开始运行银行账户TDD测试...")
    result = runner.run(suite)
    
    # 输出测试结果统计
    print(f"\n测试结果统计:")
    print(f"运行测试数: {result.testsRun}")
    print(f"失败数: {len(result.failures)}")
    print(f"错误数: {len(result.errors)}")
    print(f"成功率: {((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100):.1f}%" if result.testsRun > 0 else "无测试运行")
```

#### 案例2：代码覆盖率分析
```python
# 代码覆盖率分析
print("\n===代码覆盖率分析===")

# 注意：需要先安装coverage库: pip install coverage

try:
    import coverage
    COVERAGE_AVAILABLE = True
except ImportError:
    COVERAGE_AVAILABLE = False
    print("提示: 未安装coverage库，请运行 'pip install coverage' 安装")

if COVERAGE_AVAILABLE:
    # 创建一个简单的计算器模块用于覆盖率测试
    class SimpleCalculator:
        """简单计算器"""
        
        def add(self, a, b):
            """加法"""
            return a + b
        
        def subtract(self, a, b):
            """减法"""
            return a - b
        
        def multiply(self, a, b):
            """乘法"""
            return a * b
        
        def divide(self, a, b):
            """除法"""
            if b == 0:
                raise ZeroDivisionError("除数不能为零")
            return a / b
        
        def power(self, base, exponent):
            """幂运算"""
            return base ** exponent
        
        def is_even(self, number):
            """判断是否为偶数"""
            return number % 2 == 0
        
        def absolute(self, number):
            """绝对值"""
            if number < 0:
                return -number
            return number
        
        def maximum(self, a, b):
            """最大值"""
            if a > b:
                return a
            return b
        
        def minimum(self, a, b):
            """最小值"""
            if a < b:
                return a
            return b
    
    # 创建测试用例
    import unittest
    
    class TestSimpleCalculator(unittest.TestCase):
        """简单计算器测试"""
        
        def setUp(self):
            """测试准备"""
            self.calc = SimpleCalculator()
        
        def test_basic_operations(self):
            """测试基本运算"""
            self.assertEqual(self.calc.add(2, 3), 5)
            self.assertEqual(self.calc.subtract(5, 3), 2)
            self.assertEqual(self.calc.multiply(4, 5), 20)
            self.assertEqual(self.calc.divide(10, 2), 5)
            print("基本运算测试通过")
        
        def test_divide_by_zero(self):
            """测试除零异常"""
            with self.assertRaises(ZeroDivisionError):
                self.calc.divide(10, 0)
            print("除零异常测试通过")
        
        def test_power(self):
            """测试幂运算"""
            self.assertEqual(self.calc.power(2, 3), 8)
            self.assertEqual(self.calc.power(5, 0), 1)
            print("幂运算测试通过")
        
        def test_is_even(self):
            """测试偶数判断"""
            self.assertTrue(self.calc.is_even(4))
            self.assertFalse(self.calc.is_even(3))
            print("偶数判断测试通过")
        
        def test_absolute(self):
            """测试绝对值"""
            self.assertEqual(self.calc.absolute(-5), 5)
            self.assertEqual(self.calc.absolute(3), 3)
            print("绝对值测试通过")
        
        def test_maximum_minimum(self):
            """测试最大值最小值"""
            self.assertEqual(self.calc.maximum(5, 3), 5)
            self.assertEqual(self.calc.minimum(5, 3), 3)
            print("最大值最小值测试通过")
    
    # 演示覆盖率分析过程
    print("覆盖率分析示例:")
    print("1. 使用 coverage run -m unittest test_module 运行测试并收集覆盖率数据")
    print("2. 使用 coverage report 查看覆盖率报告")
    print("3. 使用 coverage html 生成HTML格式的详细报告")
    
    # 模拟覆盖率分析结果
    print("\n模拟覆盖率分析结果:")
    print("名称                  语句   执行  覆盖率")
    print("----------------------------------------")
    print("calculator.py           30     25    83%")
    print("test_calculator.py      25     25   100%")
    print("----------------------------------------")
    print("总计                    55     50    91%")
    
    print("\n覆盖率分析说明:")
    print("- calculator.py 中有5行代码未被执行(17%未覆盖)")
    print("- 可能未测试的代码包括边界条件和异常处理")
    print("- 建议增加测试用例以提高覆盖率")
    
    # 运行测试以演示
    if __name__ == "__main__":
        # 创建测试套件
        suite = unittest.TestLoader().loadTestsFromTestCase(TestSimpleCalculator)
        
        # 创建测试运行器
        runner = unittest.TextTestRunner(verbosity=1)
        
        # 运行测试
        print("\n运行简单计算器测试...")
        result = runner.run(suite)
        
        # 输出测试结果统计
        print(f"\n测试结果统计:")
        print(f"运行测试数: {result.testsRun}")
        print(f"失败数: {len(result.failures)}")
        print(f"错误数: {len(result.errors)}")
        print(f"成功率: {((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100):.1f}%" if result.testsRun > 0 else "无测试运行")
else:
    print("由于未安装coverage库，跳过覆盖率分析示例")
    print("要安装coverage库，请运行: pip install coverage")
```

### 代码说明

**案例1代码解释**：
1. 先编写测试用例定义功能需求，此时BankAccount类还未实现
2. 运行测试会失败，因为功能还未实现
3. 实现BankAccount类让所有测试通过
4. `self._record_transaction`：私有方法用于记录交易历史

在实际TDD过程中，应该先运行测试确认失败，再实现功能，最后再次运行测试确认通过。

**案例2代码解释**：
1. `coverage`库用于测量代码覆盖率
2. `coverage run`：运行测试并收集覆盖率数据
3. `coverage report`：生成覆盖率报告
4. `coverage html`：生成HTML格式的详细报告

如果只测试正常情况而忽略异常处理，会导致覆盖率较低，应该增加边界条件和异常情况的测试。

## 4. 最佳实践和实际应用

### 知识点解析

**概念定义**：单元测试最佳实践就像"测试的使用说明书"，告诉我们如何写出高质量、易维护的测试代码。实际应用则是将这些理论知识运用到真实项目中解决具体问题。

**核心规则**：
1. 测试应该快速、独立、可重复
2. 测试数据应该清晰、简单、有代表性
3. 测试命名应该描述性明确
4. 测试应该覆盖正常流程、边界条件和异常情况

**常见易错点**：
1. 测试之间有依赖关系导致不稳定
2. 测试数据过于复杂难以理解
3. 测试命名含糊不清
4. 忽视测试代码的可读性和可维护性

### 实战案例

#### 案例1：电商订单系统测试
```python
# 电商订单系统测试
print("===电商订单系统测试===")

import unittest
from unittest.mock import Mock, patch
from datetime import datetime, timedelta

class Product:
    """产品类"""
    
    def __init__(self, product_id, name, price, stock):
        self.product_id = product_id
        self.name = name
        self.price = price
        self.stock = stock

class OrderItem:
    """订单项类"""
    
    def __init__(self, product, quantity):
        if quantity <= 0:
            raise ValueError("数量必须大于0")
        
        if quantity > product.stock:
            raise ValueError("库存不足")
        
        self.product = product
        self.quantity = quantity
        self.price = product.price

class Order:
    """订单类"""
    
    def __init__(self, order_id, customer_name):
        self.order_id = order_id
        self.customer_name = customer_name
        self.items = []
        self.status = "待付款"
        self.created_at = datetime.now()
    
    def add_item(self, product, quantity):
        """添加订单项"""
        item = OrderItem(product, quantity)
        self.items.append(item)
        product.stock -= quantity  # 扣减库存
    
    def calculate_total(self):
        """计算订单总额"""
        return sum(item.price * item.quantity for item in self.items)
    
    def pay(self):
        """支付订单"""
        if not self.items:
            raise ValueError("订单不能为空")
        
        self.status = "已付款"
        self.paid_at = datetime.now()
    
    def cancel(self):
        """取消订单"""
        if self.status == "已付款":
            raise ValueError("已付款订单不能取消")
        
        # 恢复库存
        for item in self.items:
            item.product.stock += item.quantity
        
        self.status = "已取消"

class PaymentService:
    """支付服务类"""
    
    def process_payment(self, order, payment_method, amount):
        """
        处理支付
        
        参数:
            order (Order): 订单对象
            payment_method (str): 支付方式
            amount (float): 支付金额
            
        返回:
            dict: 支付结果
        """
        # 模拟支付处理
        if amount != order.calculate_total():
            return {
                "success": False,
                "message": "支付金额与订单金额不符"
            }
        
        # 模拟支付成功
        order.pay()
        return {
            "success": True,
            "message": "支付成功",
            "transaction_id": f"txn_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        }

class TestECommerceSystem(unittest.TestCase):
    """电商系统测试"""
    
    def setUp(self):
        """测试准备"""
        print("初始化电商系统测试...")
        
        # 创建测试产品
        self.laptop = Product(1, "笔记本电脑", 5999.0, 10)
        self.mouse = Product(2, "无线鼠标", 99.0, 50)
        self.keyboard = Product(3, "机械键盘", 299.0, 20)
    
    def tearDown(self):
        """测试清理"""
        print("清理电商系统测试...")
    
    def test_create_order(self):
        """测试创建订单"""
        order = Order("ORD001", "张三")
        
        self.assertEqual(order.order_id, "ORD001")
        self.assertEqual(order.customer_name, "张三")
        self.assertEqual(order.status, "待付款")
        self.assertEqual(len(order.items), 0)
        print("创建订单测试通过")
    
    def test_add_item_to_order(self):
        """测试添加订单项"""
        order = Order("ORD002", "李四")
        initial_stock = self.laptop.stock
        
        # 添加订单项
        order.add_item(self.laptop, 2)
        
        # 验证订单项
        self.assertEqual(len(order.items), 1)
        self.assertEqual(order.items[0].product, self.laptop)
        self.assertEqual(order.items[0].quantity, 2)
        self.assertEqual(order.items[0].price, 5999.0)
        
        # 验证库存扣减
        self.assertEqual(self.laptop.stock, initial_stock - 2)
        print("添加订单项测试通过")
    
    def test_calculate_order_total(self):
        """测试计算订单总额"""
        order = Order("ORD003", "王五")
        
        # 添加多个商品
        order.add_item(self.laptop, 1)    # 5999.0
        order.add_item(self.mouse, 2)     # 99.0 * 2 = 198.0
        order.add_item(self.keyboard, 1)  # 299.0
        
        total = order.calculate_total()
        expected_total = 5999.0 + 198.0 + 299.0  # 6496.0
        
        self.assertEqual(total, expected_total)
        print(f"计算订单总额测试通过: {total}")
    
    def test_pay_order_success(self):
        """测试成功支付订单"""
        order = Order("ORD004", "赵六")
        order.add_item(self.laptop, 1)
        
        # 支付订单
        order.pay()
        
        self.assertEqual(order.status, "已付款")
        self.assertIsNotNone(order.paid_at)
        print("成功支付订单测试通过")
    
    def test_cancel_unpaid_order(self):
        """测试取消未付款订单"""
        order = Order("ORD005", "钱七")
        initial_stock = self.laptop.stock
        order.add_item(self.laptop, 1)
        
        # 取消订单
        order.cancel()
        
        self.assertEqual(order.status, "已取消")
        # 验证库存恢复
        self.assertEqual(self.laptop.stock, initial_stock)
        print("取消未付款订单测试通过")
    
    def test_cancel_paid_order(self):
        """测试取消已付款订单"""
        order = Order("ORD006", "孙八")
        order.add_item(self.laptop, 1)
        order.pay()
        
        # 尝试取消已付款订单
        with self.assertRaises(ValueError) as context:
            order.cancel()
        
        self.assertIn("已付款订单不能取消", str(context.exception))
        self.assertEqual(order.status, "已付款")  # 状态未改变
        print("取消已付款订单测试通过")
    
    def test_add_item_insufficient_stock(self):
        """测试添加订单项时库存不足"""
        order = Order("ORD007", "周九")
        
        # 尝试购买超过库存的商品
        with self.assertRaises(ValueError) as context:
            order.add_item(self.mouse, 100)  # 库存只有50个
        
        self.assertIn("库存不足", str(context.exception))
        self.assertEqual(len(order.items), 0)  # 订单项未添加
        print("库存不足测试通过")
    
    def test_payment_service_success(self):
        """测试支付服务成功"""
        order = Order("ORD008", "吴十")
        order.add_item(self.laptop, 1)
        
        payment_service = PaymentService()
        total = order.calculate_total()
        
        result = payment_service.process_payment(order, "信用卡", total)
        
        self.assertTrue(result["success"])
        self.assertEqual(result["message"], "支付成功")
        self.assertIn("transaction_id", result)
        self.assertEqual(order.status, "已付款")
        print("支付服务成功测试通过")
    
    def test_payment_service_amount_mismatch(self):
        """测试支付服务金额不匹配"""
        order = Order("ORD009", "郑十一")
        order.add_item(self.laptop, 1)
        
        payment_service = PaymentService()
        wrong_amount = 1000.0  # 错误的金额
        
        result = payment_service.process_payment(order, "信用卡", wrong_amount)
        
        self.assertFalse(result["success"])
        self.assertIn("支付金额与订单金额不符", result["message"])
        self.assertEqual(order.status, "待付款")  # 订单状态未改变
        print("支付金额不匹配测试通过")

# 运行测试
if __name__ == "__main__":
    # 创建测试套件
    suite = unittest.TestLoader().loadTestsFromTestCase(TestECommerceSystem)
    
    # 创建测试运行器
    runner = unittest.TextTestRunner(verbosity=2)
    
    # 运行测试
    print("开始运行电商系统测试...")
    result = runner.run(suite)
    
    # 输出测试结果统计
    print(f"\n测试结果统计:")
    print(f"运行测试数: {result.testsRun}")
    print(f"失败数: {len(result.failures)}")
    print(f"错误数: {len(result.errors)}")
    print(f"成功率: {((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100):.1f}%" if result.testsRun > 0 else "无测试运行")
```

#### 案例2：测试最佳实践演示
```python
# 测试最佳实践演示
print("\n===测试最佳实践演示===")

import unittest
import json
import tempfile
import os

# 遵循最佳实践的测试示例

class DataProcessor:
    """数据处理器"""
    
    def process_numbers(self, numbers):
        """
        处理数字列表
        
        参数:
            numbers (list): 数字列表
            
        返回:
            dict: 处理结果
        """
        if not numbers:
            return {"count": 0, "sum": 0, "average": 0}
        
        if not all(isinstance(n, (int, float)) for n in numbers):
            raise TypeError("所有元素必须是数字")
        
        count = len(numbers)
        sum_value = sum(numbers)
        average = sum_value / count if count > 0 else 0
        
        return {
            "count": count,
            "sum": sum_value,
            "average": average
        }
    
    def load_config(self, config_file):
        """
        加载配置文件
        
        参数:
            config_file (str): 配置文件路径
            
        返回:
            dict: 配置内容
        """
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            raise FileNotFoundError(f"配置文件 {config_file} 不存在")
        except json.JSONDecodeError:
            raise ValueError(f"配置文件 {config_file} 格式错误")

class TestDataProcessorBestPractices(unittest.TestCase):
    """数据处理器最佳实践测试"""
    
    def setUp(self):
        """测试准备 - 遵循最佳实践"""
        print("准备测试环境...")
        self.processor = DataProcessor()
        
        # 创建临时配置文件
        self.temp_config = tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False)
        config_data = {
            "max_items": 100,
            "timeout": 30,
            "debug": True
        }
        json.dump(config_data, self.temp_config)
        self.temp_config.close()
    
    def tearDown(self):
        """测试清理 - 避免资源泄露"""
        print("清理测试环境...")
        # 清理临时文件
        if os.path.exists(self.temp_config.name):
            os.unlink(self.temp_config.name)
    
    # 1. 测试命名清晰描述性
    def test_process_numbers_with_empty_list_should_return_zero_values(self):
        """测试处理空列表应返回零值"""
        result = self.processor.process_numbers([])
        self.assertEqual(result["count"], 0)
        self.assertEqual(result["sum"], 0)
        self.assertEqual(result["average"], 0)
        print("空列表处理测试通过")
    
    def test_process_numbers_with_positive_integers_should_calculate_correctly(self):
        """测试处理正整数列表应正确计算"""
        numbers = [1, 2, 3, 4, 5]
        result = self.processor.process_numbers(numbers)
        
        self.assertEqual(result["count"], 5)
        self.assertEqual(result["sum"], 15)
        self.assertEqual(result["average"], 3.0)
        print("正整数列表处理测试通过")
    
    def test_process_numbers_with_negative_numbers_should_calculate_correctly(self):
        """测试处理负数列表应正确计算"""
        numbers = [-1, -2, -3]
        result = self.processor.process_numbers(numbers)
        
        self.assertEqual(result["count"], 3)
        self.assertEqual(result["sum"], -6)
        self.assertEqual(result["average"], -2.0)
        print("负数列表处理测试通过")
    
    def test_process_numbers_with_mixed_numbers_should_calculate_correctly(self):
        """测试处理混合数字列表应正确计算"""
        numbers = [1, -2, 3.5, -4.5, 0]
        result = self.processor.process_numbers(numbers)
        
        self.assertEqual(result["count"], 5)
        self.assertEqual(result["sum"], -2.0)
        self.assertEqual(result["average"], -0.4)
        print("混合数字列表处理测试通过")
    
    def test_process_numbers_with_invalid_input_should_raise_type_error(self):
        """测试处理无效输入应抛出类型错误"""
        invalid_numbers = [1, 2, "3", 4]
        
        with self.assertRaises(TypeError) as context:
            self.processor.process_numbers(invalid_numbers)
        
        self.assertIn("所有元素必须是数字", str(context.exception))
        print("无效输入处理测试通过")
    
    def test_load_config_with_valid_file_should_return_config_data(self):
        """测试加载有效配置文件应返回配置数据"""
        config = self.processor.load_config(self.temp_config.name)
        
        self.assertIsInstance(config, dict)
        self.assertEqual(config["max_items"], 100)
        self.assertEqual(config["timeout"], 30)
        self.assertEqual(config["debug"], True)
        print("有效配置文件加载测试通过")
    
    def test_load_config_with_nonexistent_file_should_raise_file_not_found_error(self):
        """测试加载不存在的配置文件应抛出文件未找到错误"""
        nonexistent_file = "nonexistent_config.json"
        
        with self.assertRaises(FileNotFoundError) as context:
            self.processor.load_config(nonexistent_file)
        
        self.assertIn("配置文件", str(context.exception))
        self.assertIn("不存在", str(context.exception))
        print("不存在配置文件测试通过")
    
    def test_load_config_with_invalid_json_should_raise_value_error(self):
        """测试加载无效JSON配置文件应抛出值错误"""
        # 创建无效JSON文件
        invalid_config_file = tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False)
        invalid_config_file.write("{ invalid json }")
        invalid_config_file.close()
        
        try:
            with self.assertRaises(ValueError) as context:
                self.processor.load_config(invalid_config_file.name)
            
            self.assertIn("配置文件", str(context.exception))
            self.assertIn("格式错误", str(context.exception))
            print("无效JSON配置文件测试通过")
        finally:
            # 清理临时文件
            if os.path.exists(invalid_config_file.name):
                os.unlink(invalid_config_file.name)
    
    # 2. 测试独立性 - 每个测试不依赖其他测试
    def test_each_test_is_independent(self):
        """演示测试独立性"""
        # 这个测试不影响其他测试
        numbers = [10, 20, 30]
        result = self.processor.process_numbers(numbers)
        
        # 只验证当前测试关心的结果
        self.assertEqual(result["sum"], 60)
        print("测试独立性演示通过")

# 运行测试
if __name__ == "__main__":
    # 创建测试套件
    suite = unittest.TestLoader().loadTestsFromTestCase(TestDataProcessorBestPractices)
    
    # 创建测试运行器
    runner = unittest.TextTestRunner(verbosity=2)
    
    # 运行测试
    print("开始运行最佳实践演示测试...")
    result = runner.run(suite)
    
    # 输出测试结果统计
    print(f"\n测试结果统计:")
    print(f"运行测试数: {result.testsRun}")
    print(f"失败数: {len(result.failures)}")
    print(f"错误数: {len(result.errors)}")
    print(f"成功率: {((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100):.1f}%" if result.testsRun > 0 else "无测试运行")

print("\n=== 单元测试最佳实践总结 ===")
print("1. 测试命名: 使用清晰描述性的命名，说明测试场景和期望结果")
print("2. 测试独立: 每个测试应独立运行，不依赖其他测试")
print("3. 测试数据: 使用简单、有代表性的测试数据")
print("4. 资源管理: 正确使用setUp和tearDown管理测试资源")
print("5. 异常测试: 测试正常流程和异常情况")
print("6. 断言明确: 使用明确的断言验证期望结果")
print("7. 测试覆盖: 覆盖正常情况、边界条件和异常处理")
```

### 代码说明

**案例1代码解释**：
1. `Order`类管理订单状态和商品项
2. `PaymentService`类处理支付逻辑
3. 测试覆盖了订单创建、商品添加、支付处理、订单取消等场景
4. 使用Mock对象模拟外部依赖

在电商系统中，订单状态管理是核心功能，需要仔细测试各种状态转换。

**案例2代码解释**：
1. 遵循清晰的测试命名规范
2. 正确使用setUp和tearDown管理测试资源
3. 测试独立性确保每个测试可单独运行
4. 覆盖正常流程、边界条件和异常处理
5. 使用临时文件测试文件操作功能

如果测试之间存在依赖关系，当一个测试失败时可能导致多个测试失败，增加调试难度。

这些实战案例展示了Python单元测试的核心知识点和最佳实践，包括unittest和pytest框架的使用、mock模块的应用、测试驱动开发方法、代码覆盖率分析以及测试最佳实践等。通过这些例子，可以更好地理解如何在实际项目中编写高质量的测试代码。