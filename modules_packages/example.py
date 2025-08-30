# Python模块和包示例

# 导入标准库模块
import math
import random
from datetime import datetime
import os.path as path

print("=== 标准库模块示例 ===")
# 使用math模块
print(f"π的值: {math.pi}")
print(f"2的平方根: {math.sqrt(2)}")
print(f"向上取整 4.3: {math.ceil(4.3)}")

# 使用random模块
print(f"0到1之间的随机数: {random.random()}")
print(f"1到10之间的随机整数: {random.randint(1, 10)}")

# 使用datetime模块
now = datetime.now()
print(f"当前时间: {now}")
print(f"当前年份: {now.year}")

# 使用os.path模块
current_file = __file__
print(f"当前文件的绝对路径: {path.abspath(current_file)}")
print(f"当前文件的目录: {path.dirname(path.abspath(current_file))}")

# 创建自定义模块示例
print("\n=== 自定义模块示例 ===")

# 创建一个简单的自定义模块文件
calculator_content = '''
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

# 模块级别的变量
PI = 3.14159

# 当模块被直接运行时执行的代码
if __name__ == "__main__":
    print("计算器模块被直接运行")
    print(f"10 + 5 = {add(10, 5)}")
'''

# 写入自定义模块文件
try:
    with open("calculator.py", "w", encoding="utf-8") as f:
        f.write(calculator_content)
    print("自定义模块calculator.py创建成功")
except Exception as e:
    print(f"创建自定义模块失败: {e}")

# 导入并使用自定义模块
try:
    import calculator
    
    print(f"使用自定义模块进行计算:")
    print(f"10 + 5 = {calculator.add(10, 5)}")
    print(f"10 - 5 = {calculator.subtract(10, 5)}")
    print(f"10 * 5 = {calculator.multiply(10, 5)}")
    print(f"10 / 5 = {calculator.divide(10, 5)}")
    print(f"模块中的PI值: {calculator.PI}")
except Exception as e:
    print(f"使用自定义模块失败: {e}")

# 使用from...import导入特定函数
try:
    from calculator import add, multiply
    
    print(f"\n使用from导入的函数:")
    print(f"3 + 7 = {add(3, 7)}")
    print(f"3 * 7 = {multiply(3, 7)}")
except Exception as e:
    print(f"使用from导入失败: {e}")

# 使用别名导入
try:
    import calculator as calc
    from datetime import datetime as dt
    
    print(f"\n使用别名导入:")
    print(f"8 + 2 = {calc.add(8, 2)}")
    print(f"当前时间: {dt.now()}")
except Exception as e:
    print(f"使用别名导入失败: {e}")

# 包的创建和使用示例
print("\n=== 包的示例 ===")

# 创建包结构
import os

# 创建包目录
try:
    os.makedirs("mypackage", exist_ok=True)
    
    # 创建__init__.py文件
    init_content = '''
"""mypackage包的初始化文件"""

__version__ = "1.0.0"

print("mypackage包已导入")
'''
    
    with open("mypackage/__init__.py", "w", encoding="utf-8") as f:
        f.write(init_content)
    
    # 创建包中的模块
    utils_content = '''
"""工具模块"""

def greet(name):
    """问候函数"""
    return f"你好, {name}!"

def calculate_area(radius):
    """计算圆的面积"""
    return 3.14159 * radius ** 2
'''
    
    with open("mypackage/utils.py", "w", encoding="utf-8") as f:
        f.write(utils_content)
    
    print("包mypackage创建成功")
    
    # 导入和使用包
    import mypackage.utils as utils
    
    print(f"使用包中的函数:")
    print(utils.greet("张三"))
    print(f"半径为5的圆面积: {utils.calculate_area(5)}")
    
except Exception as e:
    print(f"包操作失败: {e}")

# 演示__name__和__main__的用法
main_demo_content = '''
"""演示__name__和__main__的用法"""

def main_function():
    print("这是主函数")

def helper_function():
    print("这是辅助函数")

# 当脚本被直接运行时执行
if __name__ == "__main__":
    print("__name__的值:", __name__)
    print("脚本被直接运行")
    main_function()
else:
    print("__name__的值:", __name__)
    print("模块被导入")
'''

try:
    with open("main_demo.py", "w", encoding="utf-8") as f:
        f.write(main_demo_content)
    print("\nmain_demo.py创建成功")
    
    # 直接运行脚本
    import subprocess
    print("直接运行脚本的输出:")
    result = subprocess.run(["python", "main_demo.py"], capture_output=True, text=True)
    print(result.stdout)
    
except Exception as e:
    print(f"演示__name__失败: {e}")

# 清理创建的示例文件
cleanup_files = ["calculator.py", "main_demo.py", "example.txt", "binary_example.bin", "pathlib_example.txt"]
cleanup_dirs = ["mypackage"]

for file in cleanup_files:
    try:
        os.remove(file)
        print(f"已删除文件: {file}")
    except FileNotFoundError:
        pass
    except Exception as e:
        print(f"删除文件{file}失败: {e}")

for directory in cleanup_dirs:
    try:
        import shutil
        shutil.rmtree(directory)
        print(f"已删除目录: {directory}")
    except Exception as e:
        print(f"删除目录{directory}失败: {e}")