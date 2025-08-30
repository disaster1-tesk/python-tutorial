# Python控制流知识点

## 1. 条件语句 (if-elif-else)

条件语句用于根据不同的条件执行不同的代码块。

### 基本语法
```python
if condition1:
    # condition1为True时执行
    statement1
elif condition2:
    # condition2为True时执行
    statement2
else:
    # 所有条件都为False时执行
    statement3
```

### 使用示例
```python
# 简单if语句
age = 18
if age >= 18:
    print("已成年")

# if-else语句
score = 85
if score >= 60:
    print("及格")
else:
    print("不及格")

# if-elif-else语句
grade = 85
if grade >= 90:
    letter_grade = "A"
elif grade >= 80:
    letter_grade = "B"
elif grade >= 70:
    letter_grade = "C"
elif grade >= 60:
    letter_grade = "D"
else:
    letter_grade = "F"
print(f"成绩等级: {letter_grade}")

# 嵌套if语句
username = "admin"
password = "123456"
if username == "admin":
    if password == "123456":
        print("登录成功")
    else:
        print("密码错误")
else:
    print("用户名不存在")
```

### 实际应用场景
- 用户认证和权限控制
- 数据验证和过滤
- 菜单系统和用户交互
- 状态机和业务逻辑处理

## 2. 循环语句

### for循环
for循环用于遍历序列或其他可迭代对象。

#### 基本语法
```python
for item in iterable:
    statement
```

#### 使用示例
```python
# 遍历列表
fruits = ["苹果", "香蕉", "橙子"]
for fruit in fruits:
    print(f"我喜欢吃{fruit}")

# 使用range()函数
for i in range(5):
    print(f"数字: {i}")

# 带起始值和步长的range()
for i in range(2, 10, 2):
    print(f"偶数: {i}")  # 2, 4, 6, 8

# 使用enumerate()获取索引
fruits = ["苹果", "香蕉", "橙子"]
for index, fruit in enumerate(fruits):
    print(f"第{index+1}个水果是{fruit}")

# 遍历字典
person = {"name": "张三", "age": 25, "city": "北京"}
for key, value in person.items():
    print(f"{key}: {value}")

# 嵌套循环
matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
for row in matrix:
    for element in row:
        print(element, end=" ")
    print()  # 换行
```

### while循环
while循环在条件为真时重复执行代码块。

#### 基本语法
```python
while condition:
    statement
```

#### 使用示例
```python
# 基本while循环
count = 0
while count < 5:
    print(f"计数: {count}")
    count += 1

# 用户输入验证
while True:
    user_input = input("请输入一个正数（输入'quit'退出）: ")
    if user_input == 'quit':
        break
    try:
        number = float(user_input)
        if number > 0:
            print(f"你输入的正数是: {number}")
            break
        else:
            print("请输入正数")
    except ValueError:
        print("请输入有效的数字")

# 条件监控
import time
start_time = time.time()
while time.time() - start_time < 10:  # 运行10秒
    print("程序运行中...")
    time.sleep(1)
```

### 实际应用场景
- 数据处理和批量操作
- 用户输入等待和验证
- 定时任务和监控
- 游戏循环和动画控制

## 3. 循环控制语句

### break语句
立即终止循环。

#### 使用示例
```python
# 在for循环中使用break
for i in range(10):
    if i == 5:
        break
    print(i)  # 输出: 0 1 2 3 4

# 在while循环中使用break
count = 0
while True:
    if count >= 3:
        break
    print(f"计数: {count}")
    count += 1

# 嵌套循环中的break
for i in range(3):
    for j in range(3):
        if j == 1:
            break
        print(f"i={i}, j={j}")
    print(f"外层循环 i={i}")
```

### continue语句
跳过当前迭代，继续下一次循环。

#### 使用示例
```python
# 在for循环中使用continue
for i in range(5):
    if i == 2:
        continue
    print(i)  # 输出: 0 1 3 4

# 在while循环中使用continue
count = 0
while count < 5:
    count += 1
    if count == 3:
        continue
    print(f"计数: {count}")

# 数据过滤
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
for num in numbers:
    if num % 2 == 0:
        continue  # 跳过偶数
    print(f"奇数: {num}")
```

### else子句
当循环正常结束时执行（没有被break中断）。

#### 使用示例
```python
# for循环的else子句
for i in range(3):
    print(i)
else:
    print("循环正常结束")  # 会执行

# 被break中断的for循环
for i in range(3):
    if i == 1:
        break
    print(i)
else:
    print("循环正常结束")  # 不会执行

# while循环的else子句
count = 0
while count < 3:
    print(count)
    count += 1
else:
    print("循环正常结束")  # 会执行

# 搜索示例
numbers = [1, 3, 5, 7, 9]
target = 6
for num in numbers:
    if num == target:
        print(f"找到了{target}")
        break
else:
    print(f"未找到{target}")
```

## 4. 比较和逻辑运算符

### 比较运算符
```python
# 基本比较
print(5 > 3)    # True
print(5 < 3)    # False
print(5 == 5)   # True
print(5 != 3)   # True
print(5 >= 5)   # True
print(5 <= 3)   # False

# 身份比较
a = [1, 2, 3]
b = [1, 2, 3]
c = a
print(a == b)   # True (值相等)
print(a is b)   # False (不同对象)
print(a is c)   # True (同一对象)

# 成员关系
fruits = ["苹果", "香蕉", "橙子"]
print("苹果" in fruits)      # True
print("葡萄" not in fruits)  # True
```

### 逻辑运算符
```python
# and运算符
print(True and True)    # True
print(True and False)   # False
print(False and True)   # False
print(False and False)  # False

# or运算符
print(True or True)     # True
print(True or False)    # True
print(False or True)    # True
print(False or False)   # False

# not运算符
print(not True)         # False
print(not False)        # True

# 短路求值
def true_func():
    print("true_func被调用")
    return True

def false_func():
    print("false_func被调用")
    return False

# and短路：第一个为False时不会调用第二个
result = false_func() and true_func()  # 只输出"false_func被调用"

# or短路：第一个为True时不会调用第二个
result = true_func() or false_func()   # 只输出"true_func被调用"
```

## 5. 三元运算符

三元运算符提供了一种简洁的条件表达式。

### 基本语法
```python
value_if_true if condition else value_if_false
```

### 使用示例
```python
# 基本用法
age = 20
status = "成年人" if age >= 18 else "未成年人"
print(status)

# 在列表推导式中使用
numbers = [1, 2, 3, 4, 5]
results = ["偶数" if x % 2 == 0 else "奇数" for x in numbers]
print(results)  # ['奇数', '偶数', '奇数', '偶数', '奇数']

# 复杂条件
score = 85
grade = "优秀" if score >= 90 else "良好" if score >= 80 else "及格" if score >= 60 else "不及格"
print(grade)  # 良好

# 与函数结合
def get_discount(is_vip):
    return 0.8 if is_vip else 1.0

price = 100
is_vip = True
final_price = price * get_discount(is_vip)
print(f"最终价格: {final_price}")  # 80.0
```

## 6. 异常处理中的控制流

异常处理也会影响程序控制流。

### try-except-else-finally语句
```python
try:
    # 可能出错的代码
    result = 10 / 0
except ZeroDivisionError:
    # 处理特定异常
    print("除零错误")
except Exception as e:
    # 处理其他异常
    print(f"其他错误: {e}")
else:
    # 没有异常时执行
    print(f"计算结果: {result}")
finally:
    # 总是执行
    print("清理工作")
```

### 实际应用场景
- 错误处理和恢复
- 资源清理和安全操作
- 用户输入验证
- 网络请求和文件操作

## 7. 实际应用场景

### 用户认证和权限控制
```python
def authenticate_user(username, password):
    # 模拟用户数据库
    users = {
        "admin": {"password": "admin123", "role": "administrator"},
        "user1": {"password": "user123", "role": "user"}
    }
    
    if username in users:
        if users[username]["password"] == password:
            return users[username]["role"]
        else:
            return "密码错误"
    else:
        return "用户不存在"

# 使用示例
role = authenticate_user("admin", "admin123")
if role == "administrator":
    print("管理员权限")
elif role == "user":
    print("普通用户权限")
else:
    print(f"认证失败: {role}")
```

### 数据验证和过滤
```python
def validate_and_process_data(data_list):
    valid_data = []
    invalid_count = 0
    
    for item in data_list:
        # 数据验证
        if isinstance(item, (int, float)) and item > 0:
            valid_data.append(item)
        else:
            invalid_count += 1
            print(f"无效数据: {item}")
    
    # 处理有效数据
    if valid_data:
        average = sum(valid_data) / len(valid_data)
        print(f"有效数据平均值: {average}")
    else:
        print("没有有效数据")
    
    print(f"无效数据数量: {invalid_count}")

# 使用示例
data = [1, 2, -1, "invalid", 3.5, 0, 4]
validate_and_process_data(data)
```

### 菜单系统和用户交互
```python
def menu_system():
    menu_options = {
        "1": "查看信息",
        "2": "添加数据",
        "3": "删除数据",
        "4": "退出程序"
    }
    
    while True:
        print("\n=== 菜单系统 ===")
        for key, value in menu_options.items():
            print(f"{key}. {value}")
        
        choice = input("请选择操作 (1-4): ")
        
        if choice == "1":
            print("查看信息功能")
        elif choice == "2":
            print("添加数据功能")
        elif choice == "3":
            print("删除数据功能")
        elif choice == "4":
            print("退出程序")
            break
        else:
            print("无效选择，请重新输入")

# 运行菜单系统
# menu_system()
```

### 算法实现和搜索操作
```python
def binary_search(arr, target):
    """二分查找算法"""
    left, right = 0, len(arr) - 1
    
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    
    return -1  # 未找到

# 使用示例
sorted_array = [1, 3, 5, 7, 9, 11, 13, 15]
target = 7
index = binary_search(sorted_array, target)
if index != -1:
    print(f"找到目标值 {target}，索引为 {index}")
else:
    print(f"未找到目标值 {target}")
```

## 8. 最佳实践

### 保持条件表达式简洁明了
```python
# 好的做法
if user.is_authenticated and user.has_permission:
    perform_action()

# 避免复杂的条件表达式
if (user.is_authenticated and user.has_permission and 
    user.account_active and not user.is_locked):
    perform_action()

# 改进：使用辅助函数
def can_perform_action(user):
    return (user.is_authenticated and user.has_permission and 
            user.account_active and not user.is_locked)

if can_perform_action(user):
    perform_action()
```

### 避免过深的嵌套
```python
# 不好的做法
def process_data(data):
    if data is not None:
        if len(data) > 0:
            if isinstance(data, list):
                for item in data:
                    if item > 0:
                        print(item)

# 改进：提前返回
def process_data(data):
    if data is None or len(data) == 0 or not isinstance(data, list):
        return
    
    for item in data:
        if item > 0:
            print(item)
```

### 使用有意义的变量名
```python
# 不清晰的变量名
if x > 18 and y < 60 and z == 1:
    do_something()

# 清晰的变量名
is_adult = age >= 18
is_working_age = age < 60
is_employed = employment_status == 1

if is_adult and is_working_age and is_employed:
    process_employee()
```

### 合理使用短路求值特性
```python
# 安全的列表访问
data = [1, 2, 3]
index = 5

# 避免索引错误
if index < len(data) and data[index] > 0:
    print(data[index])

# 字典安全访问
user_data = {"name": "Alice"}
# 避免键错误
if "age" in user_data and user_data["age"] > 18:
    print("成年人")
```