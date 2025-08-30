# Python调试技巧示例

print("=== 1. print()调试法 ===")

def calculate_average(numbers):
    """计算平均值"""
    total = 0
    count = 0
    # print调试：输出中间结果
    print(f"输入的数字列表: {numbers}")
    
    for num in numbers:
        total += num
        count += 1
        print(f"当前数字: {num}, 累计总和: {total}, 计数: {count}")
    
    if count == 0:
        return 0
    
    average = total / count
    print(f"总和: {total}, 数量: {count}, 平均值: {average}")
    return average

# 测试print调试
numbers = [1, 2, 3, 4, 5]
result = calculate_average(numbers)
print(f"最终结果: {result}\n")

print("=== 2. 使用logging模块调试 ===")
import logging

# 配置日志
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def factorial(n):
    """计算阶乘"""
    logging.debug(f"开始计算 {n} 的阶乘")
    
    if n < 0:
        logging.error("阶乘不能计算负数")
        raise ValueError("阶乘不能计算负数")
    
    if n == 0 or n == 1:
        logging.debug("基础情况: 0! = 1! = 1")
        return 1
    
    result = 1
    for i in range(2, n + 1):
        result *= i
        logging.debug(f"计算过程: result = {result} (={result//i} * {i})")
    
    logging.info(f"{n}的阶乘计算完成: {result}")
    return result

# 测试logging调试
try:
    print("计算5的阶乘:")
    result = factorial(5)
    print(f"5! = {result}\n")
    
    print("尝试计算-1的阶乘:")
    factorial(-1)
except ValueError as e:
    print(f"捕获异常: {e}\n")

print("=== 3. 使用traceback模块 ===")
import traceback

def function_a():
    """函数A"""
    print("执行函数A")
    function_b()

def function_b():
    """函数B"""
    print("执行函数B")
    function_c()

def function_c():
    """函数C"""
    print("执行函数C")
    raise Exception("在函数C中发生异常")

# 测试traceback
print("演示异常追踪:")
try:
    function_a()
except Exception as e:
    print("捕获到异常:")
    print(f"异常信息: {e}")
    print("完整异常追踪:")
    traceback.print_exc()
    print()

print("=== 4. 使用pdb调试器 ===")
print("pdb是Python内置的调试器")
print("使用方法:")
print("1. 在代码中插入 'import pdb; pdb.set_trace()' 设置断点")
print("2. 命令行运行 'python -m pdb script.py' 启动调试")
print()

pdb_example = '''
"""pdb调试示例"""

import pdb

def buggy_function(x, y):
    """有问题的函数"""
    # 设置断点
    pdb.set_trace()
    
    result = x * y
    # 假设这里有逻辑错误
    if result > 0:
        result -= 10
    else:
        result += 10
    return result

# 调用函数进行调试
# buggy_function(5, 3)
'''

print("pdb常用命令:")
print("n (next)     - 执行下一行")
print("s (step)     - 进入函数内部")
print("c (continue) - 继续执行")
print("l (list)     - 显示当前代码")
print("p variable   - 打印变量值")
print("q (quit)     - 退出调试器")
print()

print("=== 5. 异常处理和调试 ===")

def safe_divide(a, b):
    """安全除法"""
    try:
        result = a / b
        return result
    except ZeroDivisionError as e:
        print(f"除零错误: {e}")
        # 打印详细的异常信息
        traceback.print_exc()
        return None
    except TypeError as e:
        print(f"类型错误: {e}")
        traceback.print_exc()
        return None
    except Exception as e:
        print(f"未预期的错误: {e}")
        traceback.print_exc()
        return None

# 测试异常处理
print("测试安全除法:")
print(f"10 / 2 = {safe_divide(10, 2)}")
print(f"10 / 0 = {safe_divide(10, 0)}")
print(f"10 / 'a' = {safe_divide(10, 'a')}")
print()

print("=== 6. 性能分析示例 ===")
print("使用cProfile进行性能分析:")
print()

profile_example = '''
"""性能分析示例"""

import cProfile
import functools

def fibonacci(n):
    """计算斐波那契数列"""
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

@functools.lru_cache(maxsize=None)
def fibonacci_cached(n):
    """带缓存的斐波那契数列"""
    if n <= 1:
        return n
    return fibonacci_cached(n-1) + fibonacci_cached(n-2)

def performance_test():
    """性能测试"""
    # 测试未缓存版本
    result1 = fibonacci(20)
    print(f"fibonacci(20) = {result1}")
    
    # 测试缓存版本
    result2 = fibonacci_cached(100)
    print(f"fibonacci_cached(100) = {result2}")

# 运行性能分析
# cProfile.run('performance_test()')
'''

print("运行性能分析命令:")
print("cProfile.run('performance_test()')")
print()

print("=== 7. 调试最佳实践 ===")
print("1. 理解问题现象，能够复现问题")
print("2. 使用最小化可复现示例")
print("3. 一次只改变一个变量")
print("4. 使用日志而不是print进行调试")
print("5. 编写测试用例防止问题重现")
print("6. 记录调试过程和解决方案")
print("7. 使用版本控制跟踪代码变化")
print("8. 利用IDE的调试功能")
print()

print("=== 8. 常见调试场景 ===")
print("1. 变量值不符合预期")
print("2. 程序异常退出")
print("3. 死循环或性能问题")
print("4. 内存使用过高")
print("5. 并发问题")
print("6. 网络请求失败")
print()

print("调试是一个需要耐心和技巧的过程，熟练掌握各种调试工具和方法能够大大提高解决问题的效率。")