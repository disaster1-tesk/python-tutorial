# Python函数示例

# 基本函数定义和调用
import keyword

print(keyword.kwlist)

def greet(name):
    """打招呼函数"""
    return f"你好, {name}!"

print(greet("张三"))

# 带默认参数的函数
def introduce(name, age=20, city="北京"):
    """自我介绍函数"""
    return f"我叫{name}, 今年{age}岁, 来自{city}"

print(introduce("李四"))
print(introduce("王五", 25))
print(introduce("赵六", 30, "上海"))

# 关键字参数
print(introduce(name="钱七", city="广州", age=28))

# 可变位置参数
def sum_all(*args):
    """计算所有参数的和"""
    total = 0
    for num in args:
        total += num
    return total

print("求和结果:", sum_all(1, 2, 3, 4, 5))

# 可变关键字参数
def print_info(**args):
    """打印个人信息"""
    for key, value in args.items():
        print(f"{key}: {value}")

print_info(name="张三", age=25, job="程序员")

# 作用域示例
global_var = "我是全局变量"

def test_scope():
    local_var = "我是局部变量"
    print(global_var)  # 可以访问全局变量
    print(local_var)   # 可以访问局部变量
    return local_var

test_scope()
# print(local_var)  # 这会报错，因为局部变量无法在函数外访问

# 匿名函数(lambda)
square = lambda x: x * x
print("5的平方是:", square(5))

# 高阶函数示例
numbers = [1, 2, 3, 4, 5]
squared_numbers = list(map(lambda x: x**2, numbers))
print("平方后的数字:", squared_numbers)

even_numbers = list(filter(lambda x: x % 2 == 0, numbers))
print("偶数:", even_numbers)

# 递归函数示例
def factorial(n):
    """计算阶乘"""
    if n <= 1:
        return 1
    else:
        return n * factorial(n - 1)

print("5的阶乘是:", factorial(5))

# 嵌套函数和闭包
def outer_function(x):
    """外层函数"""
    def inner_function(y):
        """内层函数"""
        return x + y
    return inner_function

add_five = outer_function(5)
print("闭包示例:", add_five(3))