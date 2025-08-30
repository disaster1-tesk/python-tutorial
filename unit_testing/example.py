# Python单元测试示例

print("=== 1. 创建被测试的代码 ===")

# 创建一个简单的计算器模块用于测试
calculator_code = '''
"""简单的计算器模块"""

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
        self.result = 0
    
    def add(self, value):
        """加法"""
        self.result += value
        return self.result
    
    def subtract(self, value):
        """减法"""
        self.result -= value
        return self.result
    
    def get_result(self):
        """获取结果"""
        return self.result
    
    def clear(self):
        """清零"""
        self.result = 0
        return self.result
'''

# 写入计算器模块
try:
    with open("calculator.py", "w", encoding="utf-8") as f:
        f.write(calculator_code)
    print("计算器模块创建成功: calculator.py")
except Exception as e:
    print(f"创建计算器模块失败: {e}")

print("\n=== 2. 使用unittest模块 ===")

unittest_example = '''
"""unittest示例"""

import unittest
import calculator

class TestCalculatorFunctions(unittest.TestCase):
    """测试计算器函数"""
    
    def test_add(self):
        """测试加法函数"""
        self.assertEqual(calculator.add(2, 3), 5)
        self.assertEqual(calculator.add(-1, 1), 0)
        self.assertEqual(calculator.add(0, 0), 0)
    
    def test_subtract(self):
        """测试减法函数"""
        self.assertEqual(calculator.subtract(5, 3), 2)
        self.assertEqual(calculator.subtract(0, 5), -5)
    
    def test_multiply(self):
        """测试乘法函数"""
        self.assertEqual(calculator.multiply(3, 4), 12)
        self.assertEqual(calculator.multiply(-2, 3), -6)
        self.assertEqual(calculator.multiply(0, 100), 0)
    
    def test_divide(self):
        """测试除法函数"""
        self.assertEqual(calculator.divide(10, 2), 5)
        self.assertEqual(calculator.divide(9, 3), 3)
        
        # 测试异常
        with self.assertRaises(ValueError):
            calculator.divide(10, 0)

class TestCalculatorClass(unittest.TestCase):
    """测试计算器类"""
    
    def setUp(self):
        """测试前的准备工作"""
        self.calc = calculator.Calculator()
    
    def tearDown(self):
        """测试后的清理工作"""
        pass
    
    def test_calculator_add(self):
        """测试计算器加法"""
        result = self.calc.add(5)
        self.assertEqual(result, 5)
        
        result = self.calc.add(3)
        self.assertEqual(result, 8)
    
    def test_calculator_subtract(self):
        """测试计算器减法"""
        self.calc.add(10)
        result = self.calc.subtract(3)
        self.assertEqual(result, 7)
    
    def test_calculator_clear(self):
        """测试计算器清零"""
        self.calc.add(5)
        result = self.calc.clear()
        self.assertEqual(result, 0)

if __name__ == "__main__":
    unittest.main()
'''

# 写入unittest示例
try:
    with open("test_calculator_unittest.py", "w", encoding="utf-8") as f:
        f.write(unittest_example)
    print("unittest示例创建成功: test_calculator_unittest.py")
except Exception as e:
    print(f"创建unittest示例失败: {e}")

print("\n=== 3. 使用mock模块 ===")

mock_example = '''
"""mock示例"""

from unittest.mock import Mock, patch
import unittest
import calculator

class TestWithMock(unittest.TestCase):
    """使用mock的测试示例"""
    
    def test_mock_object(self):
        """测试mock对象"""
        # 创建mock对象
        mock_obj = Mock()
        mock_obj.method.return_value = "mocked result"
        
        # 调用mock方法
        result = mock_obj.method()
        self.assertEqual(result, "mocked result")
        
        # 验证方法被调用
        mock_obj.method.assert_called_once()
    
    # 注意：这个示例需要requests库，实际运行时可能需要安装
    @patch('requests.get')
    def test_mock_external_api(self, mock_get):
        """测试mock外部API"""
        # 模拟API响应
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {"key": "value"}
        
        # 这里应该调用实际使用requests的函数
        # response = requests.get("http://example.com")
        # 由于我们没有这样的函数，这里只是演示mock的用法
        self.assertEqual(mock_get.return_value.status_code, 200)

if __name__ == "__main__":
    unittest.main()
'''

# 写入mock示例
try:
    with open("test_mock_example.py", "w", encoding="utf-8") as f:
        f.write(mock_example)
    print("mock示例创建成功: test_mock_example.py")
except Exception as e:
    print(f"创建mock示例失败: {e}")

print("\n=== 4. pytest框架示例 ===")
print("pytest是一个更现代、更简洁的测试框架")
print("需要先安装: pip install pytest")

pytest_example = '''
"""pytest示例"""

import calculator
import pytest

# pytest不需要继承任何类，函数名以test_开头即可

def test_add():
    """测试加法"""
    assert calculator.add(2, 3) == 5
    assert calculator.add(-1, 1) == 0
    assert calculator.add(0, 0) == 0

def test_subtract():
    """测试减法"""
    assert calculator.subtract(5, 3) == 2
    assert calculator.subtract(0, 5) == -5

def test_divide():
    """测试除法"""
    assert calculator.divide(10, 2) == 5
    assert calculator.divide(9, 3) == 3
    
    # 测试异常
    with pytest.raises(ValueError):
        calculator.divide(10, 0)

class TestCalculatorClass:
    """测试计算器类"""
    
    def setup_method(self):
        """每个测试方法前执行"""
        self.calc = calculator.Calculator()
    
    def test_calculator_add(self):
        """测试计算器加法"""
        assert self.calc.add(5) == 5
        assert self.calc.add(3) == 8
    
    def test_calculator_subtract(self):
        """测试计算器减法"""
        self.calc.add(10)
        assert self.calc.subtract(3) == 7

# 参数化测试示例
@pytest.mark.parametrize("a, b, expected", [
    (2, 3, 5),
    (0, 0, 0),
    (-1, 1, 0),
    (10, -5, 5)
])
def test_add_parametrized(a, b, expected):
    """参数化测试加法"""
    assert calculator.add(a, b) == expected
'''

# 写入pytest示例
try:
    with open("test_calculator_pytest.py", "w", encoding="utf-8") as f:
        f.write(pytest_example)
    print("pytest示例创建成功: test_calculator_pytest.py")
except Exception as e:
    print(f"创建pytest示例失败: {e}")

print("\n=== 5. 运行测试的方法 ===")
print("1. 运行unittest:")
print("   python -m unittest test_calculator_unittest.py")
print("   python -m unittest test_calculator_unittest.TestCalculatorFunctions")
print("   python -m unittest test_calculator_unittest.TestCalculatorFunctions.test_add")
print()
print("2. 运行pytest (需要先安装pytest):")
print("   pytest test_calculator_pytest.py")
print("   pytest test_calculator_pytest.py::test_add")
print("   pytest -v  # 详细输出")
print()
print("3. 生成代码覆盖率报告 (需要先安装coverage):")
print("   coverage run -m unittest test_calculator_unittest.py")
print("   coverage report")
print("   coverage html  # 生成HTML报告")

print("\n=== 6. 测试驱动开发(TDD)示例 ===")
print("TDD开发流程:")
print("1. 编写测试")
print("2. 运行测试(失败)")
print("3. 编写刚好能让测试通过的实现")
print("4. 运行测试(通过)")
print("5. 重构代码")
print("6. 重复以上步骤")

tdd_example = '''
"""TDD示例 - 先写测试，再写实现"""

# 这是TDD的测试部分
import unittest

class TestFibonacci(unittest.TestCase):
    def test_fibonacci(self):
        # 测试用例
        self.assertEqual(fibonacci(0), 0)
        self.assertEqual(fibonacci(1), 1)
        self.assertEqual(fibonacci(2), 1)
        self.assertEqual(fibonacci(3), 2)
        self.assertEqual(fibonacci(4), 3)
        self.assertEqual(fibonacci(5), 5)

def fibonacci(n):
    """斐波那契数列"""
    # 这是根据测试逐步完善的实现
    if n <= 1:
        return n
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b

if __name__ == "__main__":
    unittest.main()
'''

print("TDD示例展示了测试驱动开发的理念")

# 清理创建的示例文件
import os
files_to_clean = [
    "calculator.py",
    "test_calculator_unittest.py", 
    "test_mock_example.py",
    "test_calculator_pytest.py"
]

print("\n=== 7. 清理示例文件 ===")
for file in files_to_clean:
    try:
        os.remove(file)
        print(f"已删除示例文件: {file}")
    except FileNotFoundError:
        print(f"文件不存在: {file}")
    except Exception as e:
        print(f"删除文件 {file} 失败: {e}")

print("\n=== 8. 单元测试最佳实践 ===")
print("1. 测试应该独立且可重复")
print("2. 测试应该快速执行")
print("3. 测试应该使用简单且清晰的输入数据")
print("4. 测试应该覆盖正常情况和边界情况")
print("5. 测试应该针对接口而不是实现")
print("6. 保持测试代码的可读性和可维护性")
print("7. 定期运行测试，确保代码质量")
print("8. 使用持续集成(CI)自动运行测试")