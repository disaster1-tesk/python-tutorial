# Python异常处理示例

# 基本的try-except结构
try:
    result = 10 / 0
except ZeroDivisionError:
    print("不能除以零！")

# 捕获多种异常类型
try:
    number = int(input("请输入一个数字: "))
    result = 10 / number
    print(f"结果是: {result}")
except ValueError:
    print("输入的不是有效数字！")
except ZeroDivisionError:
    print("不能除以零！")
except Exception as e:
    print(f"发生了未预期的错误: {e}")

# 使用else和finally块
try:
    file = open("test.txt", "r")
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

# 主动抛出异常
def validate_age(age):
    if age < 0:
        raise ValueError("年龄不能为负数")
    if age > 150:
        raise ValueError("年龄不能超过150岁")
    return True

try:
    user_age = -5
    validate_age(user_age)
except ValueError as e:
    print(f"年龄验证失败: {e}")

# 自定义异常类
class CustomError(Exception):
    """自定义异常类"""
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

def check_score(score):
    if score < 0 or score > 100:
        raise CustomError(f"分数 {score} 超出有效范围(0-100)")

try:
    check_score(150)
except CustomError as e:
    print(f"自定义异常: {e.message}")

# 异常链
try:
    try:
        result = 10 / 0
    except ZeroDivisionError as e:
        raise ValueError("处理除零错误时发生新的错误") from e
except ValueError as e:
    print(f"捕获的异常: {e}")
    print(f"原始异常: {e.__cause__}")

# 使用with语句自动处理资源（推荐方式）
try:
    with open("test.txt", "r") as file:
        content = file.read()
        print("文件内容:", content)
except FileNotFoundError:
    print("文件未找到，但我们不需要手动关闭文件")