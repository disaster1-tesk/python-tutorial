# Python函数知识点

## 1. 函数定义和调用

### 知识点解析

**概念定义**：函数就像一个专门做特定工作的"机器人"，你告诉它要做什么（定义函数），然后在需要的时候叫它去做（调用函数）。比如我们定义一个"洗苹果"的函数，每次需要洗苹果时就调用这个函数，而不需要每次都重新说明怎么洗。

**核心规则**：
1. 使用`def`关键字定义函数，后面跟函数名和括号
2. 函数名后必须跟一对括号，即使没有参数也要写括号
3. 函数体必须缩进（通常4个空格）
4. 使用`return`语句返回结果，如果没有return语句，默认返回None

**常见易错点**：
1. 忘记在函数名后加括号
2. 定义函数后忘记调用函数，导致代码不执行
3. 缩进不一致导致语法错误
4. return语句位置错误，导致函数提前或无法返回正确结果

### 实战案例

#### 案例1：简单计算器函数
```python
# 简单计算器函数
print("===简单计算器函数===")

# 定义加法函数
def add(a, b):
    """计算两个数的和"""
    result = a + b
    return result

# 定义减法函数
def subtract(a, b):
    """计算两个数的差"""
    result = a - b
    return result

# 定义乘法函数
def multiply(a, b):
    """计算两个数的积"""
    result = a * b
    return result

# 定义除法函数
def divide(a, b):
    """计算两个数的商"""
    # 检查除数是否为0
    if b == 0:
        return "错误：除数不能为0"
    result = a / b
    return result

# 使用函数进行计算
print("计算器演示:")
num1 = 10
num2 = 3

print(f"{num1} + {num2} = {add(num1, num2)}")
print(f"{num1} - {num2} = {subtract(num1, num2)}")
print(f"{num1} * {num2} = {multiply(num1, num2)}")
print(f"{num1} / {num2} = {divide(num1, num2)}")

# 演示除数为0的情况
print(f"{num1} / 0 = {divide(num1, 0)}")
```

#### 案例2：学生成绩处理函数
```python
# 学生成绩处理函数
print("\n===学生成绩处理函数===")

# 定义计算平均分的函数
def calculate_average(scores):
    """
    计算成绩列表的平均分
    
    参数:
        scores (list): 成绩列表
        
    返回:
        float: 平均分，如果列表为空则返回0
    """
    # 检查列表是否为空
    if not scores:
        return 0
    
    # 计算总分
    total = 0
    for score in scores:
        total += score
    
    # 计算平均分
    average = total / len(scores)
    return average

# 定义获取等级的函数
def get_grade(average_score):
    """
    根据平均分获取等级
    
    参数:
        average_score (float): 平均分
        
    返回:
        str: 等级描述
    """
    if average_score >= 90:
        return "优秀"
    elif average_score >= 80:
        return "良好"
    elif average_score >= 70:
        return "中等"
    elif average_score >= 60:
        return "及格"
    else:
        return "不及格"

# 定义打印成绩报告的函数
def print_report(student_name, scores):
    """
    打印学生成绩报告
    
    参数:
        student_name (str): 学生姓名
        scores (list): 成绩列表
    """
    print(f"\n=== {student_name}的成绩报告 ===")
    print(f"各科成绩: {scores}")
    
    # 计算平均分
    average = calculate_average(scores)
    print(f"平均分: {average:.2f}")
    
    # 获取等级
    grade = get_grade(average)
    print(f"等级: {grade}")

# 使用函数处理学生成绩
students_scores = {
    "张三": [95, 87, 92, 88, 90],
    "李四": [78, 82, 75, 80, 77],
    "王五": [88, 90, 94, 89, 92]
}

# 为每个学生打印成绩报告
for name, scores in students_scores.items():
    print_report(name, scores)
```

### 代码说明

**案例1代码解释**：
1. `def add(a, b):`：使用def关键字定义函数，add是函数名，a和b是参数
2. `result = a + b`：在函数内部执行加法运算
3. `return result`：使用return语句返回计算结果
4. `print(f"{num1} + {num2} = {add(num1, num2)}")`：调用add函数并打印结果

如果忘记写`return result`，函数会返回None，这样就无法获得计算结果。如果把`return result`写在`if b == 0:`判断之前，会导致函数总是返回result而无法处理除数为0的情况。

**案例2代码解释**：
1. `def calculate_average(scores):`：定义带参数的函数
2. `"""计算成绩列表的平均分"""`：函数的文档字符串，说明函数功能
3. `if not scores:`：检查参数是否为空列表
4. `for score in scores:`：遍历成绩列表计算总分
5. `average = total / len(scores)`：计算平均分
6. `return average`：返回计算结果

如果把`total = 0`放在for循环内部，每次循环都会重新初始化total为0，导致计算结果错误。如果忘记处理空列表的情况，当传入空列表时会出现除零错误。

## 2. 参数类型和使用

### 知识点解析

**概念定义**：函数参数就像我们给"机器人"下达命令时提供的具体信息。比如让"洗苹果"机器人工作时，我们需要告诉它洗几个苹果、用什么水温等信息，这些就是参数。

**核心规则**：
1. 位置参数：按照位置顺序传递，调用时必须提供相应数量的参数
2. 默认参数：为参数设置默认值，调用时可以不传入该参数
3. 关键字参数：通过参数名指定参数值，可以不按顺序
4. 可变参数：可以接收任意数量的参数

**常见易错点**：
1. 位置参数和关键字参数混用时顺序错误
2. 默认参数使用可变对象（如列表）作为默认值
3. 在定义默认参数时使用了变量而不是常量
4. 可变参数和关键字参数使用不当

### 实战案例

#### 案例1：用户信息处理系统
```python
# 用户信息处理系统
print("===用户信息处理系统===")

# 定义创建用户档案的函数（使用默认参数）
def create_user_profile(name, age=18, city="北京", hobbies=None):
    """
    创建用户档案
    
    参数:
        name (str): 用户姓名
        age (int): 年龄，默认18
        city (str): 城市，默认"北京"
        hobbies (list): 爱好列表，默认为空列表
        
    返回:
        dict: 用户档案字典
    """
    # 注意：不要使用 hobbies=[] 作为默认值，因为可变默认值会在多次调用间共享
    if hobbies is None:
        hobbies = []
    
    profile = {
        "name": name,
        "age": age,
        "city": city,
        "hobbies": hobbies
    }
    
    return profile

# 定义添加爱好的函数
def add_hobby(profile, *hobbies):
    """
    为用户档案添加爱好
    
    参数:
        profile (dict): 用户档案
        *hobbies: 可变数量的爱好参数
    """
    for hobby in hobbies:
        if hobby not in profile["hobbies"]:
            profile["hobbies"].append(hobby)

# 定义更新用户信息的函数
def update_user_info(profile, **updates):
    """
    更新用户信息
    
    参数:
        profile (dict): 用户档案
        **updates: 要更新的信息（关键字参数）
    """
    for key, value in updates.items():
        if key in profile:
            profile[key] = value
        else:
            print(f"警告: 不存在的字段 '{key}'")

# 演示不同方式创建用户档案
print("1. 使用位置参数创建用户:")
user1 = create_user_profile("张三", 25, "上海", ["读书", "游泳"])
print(f"用户1: {user1}")

print("\n2. 使用默认参数创建用户:")
user2 = create_user_profile("李四")
print(f"用户2: {user2}")

print("\n3. 使用关键字参数创建用户:")
user3 = create_user_profile(name="王五", age=30, hobbies=["音乐", "旅行"])
print(f"用户3: {user3}")

print("\n4. 使用混合参数创建用户:")
user4 = create_user_profile("赵六", city="广州")
print(f"用户4: {user4}")

# 演示添加爱好
print("\n===添加爱好===")
add_hobby(user1, "电影", "游戏")
print(f"用户1添加爱好后: {user1}")

add_hobby(user2, "绘画", "烹饪", "摄影")
print(f"用户2添加爱好后: {user2}")

# 演示更新用户信息
print("\n===更新用户信息===")
update_user_info(user3, age=31, city="深圳")
print(f"用户3更新信息后: {user3}")

update_user_info(user4, name="赵六六", invalid_field="测试")
print(f"用户4更新信息后: {user4}")
```

#### 案例2：灵活的数学计算函数
```python
# 灵活的数学计算函数
print("\n===灵活的数学计算函数===")

# 定义计算多个数之和的函数
def calculate_sum(*numbers):
    """
    计算多个数的和
    
    参数:
        *numbers: 可变数量的数字参数
        
    返回:
        float: 所有数字的和
    """
    total = 0
    for num in numbers:
        total += num
    return total

# 定义计算统计信息的函数
def calculate_statistics(*numbers):
    """
    计算数字列表的统计信息
    
    参数:
        *numbers: 可变数量的数字参数
        
    返回:
        dict: 包含统计信息的字典
    """
    if not numbers:
        return {"count": 0, "sum": 0, "average": 0, "min": None, "max": None}
    
    total = calculate_sum(*numbers)  # 调用其他函数
    count = len(numbers)
    average = total / count
    min_value = min(numbers)
    max_value = max(numbers)
    
    return {
        "count": count,
        "sum": total,
        "average": average,
        "min": min_value,
        "max": max_value
    }

# 定义格式化输出统计信息的函数
def print_statistics(title, **stats):
    """
    格式化输出统计信息
    
    参数:
        title (str): 标题
        **stats: 统计信息（关键字参数）
    """
    print(f"\n=== {title} ===")
    for key, value in stats.items():
        if isinstance(value, float):
            print(f"{key}: {value:.2f}")
        else:
            print(f"{key}: {value}")

# 演示可变位置参数
print("===可变位置参数演示===")
print(f"1个数的和: {calculate_sum(10)}")
print(f"3个数的和: {calculate_sum(1, 2, 3)}")
print(f"5个数的和: {calculate_sum(1, 2, 3, 4, 5)}")
print(f"10个数的和: {calculate_sum(1, 2, 3, 4, 5, 6, 7, 8, 9, 10)}")

# 演示可变关键字参数
print("\n===可变关键字参数演示===")
print_statistics("销售数据", 销售额=10000, 利润=2000, 客户数=50)
print_statistics("网站数据", 访问量=50000, 注册数=1000, 转化率=0.02)

# 演示综合使用
print("\n===综合使用演示===")
# 计算学生成绩统计
math_scores = [85, 92, 78, 96, 88, 90, 87, 94, 89, 91]
stats = calculate_statistics(*math_scores)  # 解包列表作为参数
print_statistics("数学成绩统计", **stats)  # 解包字典作为关键字参数

# 计算不同班级的平均分
class_a_scores = [85, 90, 88, 92, 87]
class_b_scores = [78, 82, 85, 80, 79]
class_c_scores = [95, 96, 94, 98, 97]

class_a_avg = calculate_statistics(*class_a_scores)["average"]
class_b_avg = calculate_statistics(*class_b_scores)["average"]
class_c_avg = calculate_statistics(*class_c_scores)["average"]

print_statistics(
    "各班级平均分",
    一班平均分=class_a_avg,
    二班平均分=class_b_avg,
    三班平均分=class_c_avg
)
```

### 代码说明

**案例1代码解释**：
1. `def create_user_profile(name, age=18, city="北京", hobbies=None):`：定义了位置参数、默认参数和可选参数
2. `if hobbies is None: hobbies = []`：正确处理可变默认参数的方式
3. `def add_hobby(profile, *hobbies):`：使用*接收可变数量的位置参数
4. `def update_user_info(profile, **updates):`：使用**接收可变数量的关键字参数

如果写成`def create_user_profile(name, age=18, city="北京", hobbies=[]):`，会导致所有用户共享同一个hobbies列表，添加一个用户的爱好会影响其他用户。

**案例2代码解释**：
1. `def calculate_sum(*numbers):`：使用*numbers接收任意数量的数字参数
2. `def calculate_statistics(*numbers):`：在函数内部可以像使用列表一样使用numbers
3. `calculate_sum(*numbers)`：调用其他函数时使用*解包参数
4. `print_statistics("数学成绩统计", **stats)`：使用**解包字典作为关键字参数

如果在调用函数时忘记使用*解包列表，如`calculate_statistics(math_scores)`，会把整个列表作为一个参数传递，而不是把列表中的元素作为多个参数传递。

## 3. 作用域和变量访问

### 知识点解析

**概念定义**：作用域就像不同区域的"权限管理"，有些变量只能在特定区域内使用。就像学校里每个班级有自己的教室（局部作用域），而学校的公共设施（全局作用域）所有班级都可以使用。

**核心规则**：
1. 局部作用域：在函数内部定义的变量只能在函数内部访问
2. 全局作用域：在函数外部定义的变量可以在整个程序中访问
3. 使用global关键字可以在函数内部修改全局变量
4. 使用nonlocal关键字可以在嵌套函数中修改外层函数的变量

**常见易错点**：
1. 在函数内部意外创建了同名的局部变量，而不是使用全局变量
2. 忘记使用global关键字就试图修改全局变量
3. 在嵌套函数中错误地使用变量访问规则
4. 混淆变量查找顺序（LEGB规则：Local->Enclosing->Global->Built-in）

### 实战案例

#### 案例1：计数器和配置管理系统
```python
# 计数器和配置管理系统
print("===计数器和配置管理系统===")

# 全局变量
app_version = "1.0.0"  # 应用版本
debug_mode = True      # 调试模式
max_users = 1000       # 最大用户数
active_users = 0       # 活跃用户数

# 配置函数
def get_app_info():
    """获取应用信息（只读全局变量）"""
    print(f"应用版本: {app_version}")
    print(f"调试模式: {'开启' if debug_mode else '关闭'}")
    print(f"最大用户数: {max_users}")
    print(f"当前活跃用户数: {active_users}")

# 用户管理函数
def add_user(username):
    """
    添加用户（修改全局变量）
    
    参数:
        username (str): 用户名
    """
    global active_users  # 声明要修改全局变量
    
    if active_users >= max_users:
        print("错误: 用户数已达上限")
        return False
    
    active_users += 1
    print(f"用户 '{username}' 添加成功，当前活跃用户数: {active_users}")
    
    # 调试信息
    if debug_mode:
        print(f"调试: 新增用户 {username}")
    
    return True

def remove_user(username):
    """
    移除用户（修改全局变量）
    
    参数:
        username (str): 用户名
    """
    global active_users  # 声明要修改全局变量
    
    if active_users <= 0:
        print("错误: 没有活跃用户")
        return False
    
    active_users -= 1
    print(f"用户 '{username}' 移除成功，当前活跃用户数: {active_users}")
    
    # 调试信息
    if debug_mode:
        print(f"调试: 移除用户 {username}")
    
    return True

# 配置更新函数
def update_config(new_version=None, new_debug_mode=None, new_max_users=None):
    """
    更新配置（修改多个全局变量）
    
    参数:
        new_version (str): 新版本号
        new_debug_mode (bool): 新调试模式
        new_max_users (int): 新最大用户数
    """
    global app_version, debug_mode, max_users  # 声明要修改的全局变量
    
    if new_version is not None:
        old_version = app_version
        app_version = new_version
        print(f"版本已从 {old_version} 更新为 {app_version}")
    
    if new_debug_mode is not None:
        old_debug_mode = debug_mode
        debug_mode = new_debug_mode
        print(f"调试模式已从 {'开启' if old_debug_mode else '关闭'} 更新为 {'开启' if debug_mode else '关闭'}")
    
    if new_max_users is not None:
        old_max_users = max_users
        max_users = new_max_users
        print(f"最大用户数已从 {old_max_users} 更新为 {max_users}")

# 演示全局变量的使用
print("初始应用信息:")
get_app_info()

print("\n===用户管理演示===")
add_user("张三")
add_user("李四")
add_user("王五")

print("\n当前应用信息:")
get_app_info()

remove_user("李四")

print("\n更新后应用信息:")
get_app_info()

print("\n===配置更新演示===")
update_config(new_version="1.1.0", new_debug_mode=False, new_max_users=2000)

print("\n更新后应用信息:")
get_app_info()
```

#### 案例2：嵌套函数和闭包应用
```python
# 嵌套函数和闭包应用
print("\n===嵌套函数和闭包应用===")

# 创建计数器工厂函数
def create_counter(initial_value=0):
    """
    创建计数器（闭包示例）
    
    参数:
        initial_value (int): 初始值
        
    返回:
        function: 计数器函数
    """
    count = initial_value  # 外层函数的局部变量
    
    def counter(step=1):
        """
        计数器函数（内层函数）
        
        参数:
            step (int): 步长
            
        返回:
            int: 当前计数值
        """
        nonlocal count  # 声明要修改外层函数的变量
        count += step
        return count
    
    return counter  # 返回内层函数

# 创建不同的计数器
print("===计数器演示===")
counter1 = create_counter()      # 默认初始值0
counter2 = create_counter(10)    # 初始值10
counter3 = create_counter(-5)    # 初始值-5

print("第一次调用:")
print(f"计数器1: {counter1()}")  # 1
print(f"计数器2: {counter2()}")  # 11
print(f"计数器3: {counter3()}")  # -4

print("\n第二次调用:")
print(f"计数器1: {counter1(2)}")  # 3 (增加2)
print(f"计数器2: {counter2(5)}")  # 16 (增加5)
print(f"计数器3: {counter3()}")   # -3 (增加1)

print("\n第三次调用:")
print(f"计数器1: {counter1()}")   # 4 (增加1)
print(f"计数器2: {counter2()}")   # 17 (增加1)
print(f"计数器3: {counter3(-2)}") # -5 (减少2)

# 创建配置管理器（更复杂的闭包应用）
def create_config_manager():
    """
    创建配置管理器
    
    返回:
        dict: 包含配置操作函数的字典
    """
    config = {}  # 配置字典
    
    def set_config(key, value):
        """设置配置项"""
        config[key] = value
        print(f"配置项 '{key}' 已设置为 '{value}'")
    
    def get_config(key, default=None):
        """获取配置项"""
        return config.get(key, default)
    
    def list_config():
        """列出所有配置项"""
        if not config:
            print("暂无配置项")
        else:
            print("当前配置项:")
            for key, value in config.items():
                print(f"  {key}: {value}")
    
    def clear_config():
        """清空所有配置"""
        config.clear()
        print("所有配置项已清空")
    
    # 返回包含所有操作函数的字典
    return {
        "set": set_config,
        "get": get_config,
        "list": list_config,
        "clear": clear_config
    }

# 使用配置管理器
print("\n===配置管理器演示===")
config_manager = create_config_manager()

# 设置配置项
config_manager["set"]("数据库地址", "localhost:3306")
config_manager["set"]("最大连接数", 100)
config_manager["set"]("调试模式", True)

# 列出配置项
config_manager["list"]()

# 获取配置项
db_host = config_manager["get"]("数据库地址")
max_connections = config_manager["get"]("最大连接数")
print(f"\n数据库地址: {db_host}")
print(f"最大连接数: {max_connections}")

# 获取不存在的配置项
cache_size = config_manager["get"]("缓存大小", 1024)  # 提供默认值
print(f"缓存大小: {cache_size}")

# 清空配置
config_manager["clear"]()
config_manager["list"]()
```

### 代码说明

**案例1代码解释**：
1. `global active_users`：在函数内部声明要修改全局变量
2. `global app_version, debug_mode, max_users`：同时声明多个全局变量
3. `if debug_mode:`：在函数内部读取全局变量的值
4. 函数可以读取全局变量，但要修改必须使用global关键字

如果在`add_user`函数中忘记写`global active_users`，而直接写`active_users += 1`，Python会创建一个同名的局部变量，不会修改全局变量，且会报错"local variable 'active_users' referenced before assignment"。

**案例2代码解释**：
1. `nonlocal count`：在内层函数中声明要修改外层函数的变量
2. `return counter`：外层函数返回内层函数，形成闭包
3. `count`变量被内层函数"捕获"，即使外层函数执行完毕也不会被销毁
4. 每个通过`create_counter`创建的计数器都有独立的`count`变量

如果在`counter`函数中忘记写`nonlocal count`，而直接写`count += step`，会出现与全局变量类似的问题，Python会尝试创建局部变量count，但由于没有初始化就使用，会报错。

## 4. 匿名函数和高阶函数

### 知识点解析

**概念定义**：匿名函数就像"一次性"的简单工具，不需要给它起名字，用完就扔。高阶函数则是能够接收函数作为参数或返回函数的函数，就像"函数工厂"一样。

**核心规则**：
1. 使用lambda关键字创建匿名函数
2. lambda函数只能包含表达式，不能包含语句
3. 高阶函数可以接收函数作为参数
4. 高阶函数可以返回函数作为结果

**常见易错点**：
1. 在lambda函数中使用复杂的逻辑或语句
2. 忘记lambda函数的限制，试图在其中使用print等语句
3. 在循环中创建lambda函数时变量绑定问题
4. 滥用lambda函数，使代码难以理解

### 实战案例

#### 案例1：数据处理和排序
```python
# 数据处理和排序
print("===数据处理和排序===")

# 学生数据
students = [
    {"name": "张三", "age": 20, "score": 85, "class": "A"},
    {"name": "李四", "age": 19, "score": 92, "class": "B"},
    {"name": "王五", "age": 21, "score": 78, "class": "A"},
    {"name": "赵六", "age": 20, "score": 96, "class": "C"},
    {"name": "钱七", "age": 19, "score": 88, "class": "B"}
]

print("原始学生数据:")
for student in students:
    print(f"  {student}")

# 使用lambda函数进行排序
print("\n===排序演示===")

# 按分数排序（降序）
students_by_score = sorted(students, key=lambda x: x["score"], reverse=True)
print("\n按分数排序（降序）:")
for i, student in enumerate(students_by_score, 1):
    print(f"  {i}. {student['name']}: {student['score']}分")

# 按年龄排序（升序）
students_by_age = sorted(students, key=lambda x: x["age"])
print("\n按年龄排序（升序）:")
for student in students_by_age:
    print(f"  {student['name']}: {student['age']}岁")

# 按姓名排序
students_by_name = sorted(students, key=lambda x: x["name"])
print("\n按姓名排序:")
for student in students_by_name:
    print(f"  {student['name']}")

# 使用map和lambda函数处理数据
print("\n===数据处理演示===")

# 计算每个学生的分数加权值（假设权重为1.2）
weighted_scores = list(map(lambda x: x["score"] * 1.2, students))
print("加权分数:")
for i, (student, weighted_score) in enumerate(zip(students, weighted_scores)):
    print(f"  {student['name']}: {student['score']} -> {weighted_score:.1f}")

# 生成学生简介
student_profiles = list(map(
    lambda x: f"{x['name']}({x['age']}岁), {x['class']}班, {x['score']}分", 
    students
))
print("\n学生简介:")
for profile in student_profiles:
    print(f"  {profile}")

# 使用filter和lambda函数筛选数据
print("\n===数据筛选演示===")

# 筛选分数大于等于90的学生
excellent_students = list(filter(lambda x: x["score"] >= 90, students))
print("优秀学生（90分及以上）:")
for student in excellent_students:
    print(f"  {student['name']}: {student['score']}分")

# 筛选A班学生
class_a_students = list(filter(lambda x: x["class"] == "A", students))
print("\nA班学生:")
for student in class_a_students:
    print(f"  {student['name']}: {student['score']}分")

# 筛选19岁的学生
young_students = list(filter(lambda x: x["age"] == 19, students))
print("\n19岁学生:")
for student in young_students:
    print(f"  {student['name']}: {student['age']}岁")

# 综合使用：筛选A班且分数大于80的学生
a_class_good_students = list(filter(
    lambda x: x["class"] == "A" and x["score"] > 80, 
    students
))
print("\nA班且分数大于80的学生:")
for student in a_class_good_students:
    print(f"  {student['name']}: {student['score']}分")
```

#### 案例2：函数式编程工具
```python
# 函数式编程工具
print("\n===函数式编程工具===")

# 定义高阶函数：通用数据处理器
def data_processor(data, process_func):
    """
    通用数据处理器
    
    参数:
        data (list): 数据列表
        process_func (function): 处理函数
        
    返回:
        list: 处理后的数据列表
    """
    return [process_func(item) for item in data]

# 定义高阶函数：条件筛选器
def conditional_filter(data, condition_func):
    """
    条件筛选器
    
    参数:
        data (list): 数据列表
        condition_func (function): 条件函数
        
    返回:
        list: 符合条件的数据列表
    """
    return [item for item in data if condition_func(item)]

# 定义高阶函数：数据聚合器
def data_aggregator(data, aggregate_func, initial_value=0):
    """
    数据聚合器
    
    参数:
        data (list): 数据列表
        aggregate_func (function): 聚合函数
        initial_value: 初始值
        
    返回:
        聚合结果
    """
    result = initial_value
    for item in data:
        result = aggregate_func(result, item)
    return result

# 测试数据
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
words = ["apple", "banana", "cherry", "date", "elderberry"]

print("原始数据:")
print(f"数字: {numbers}")
print(f"单词: {words}")

# 使用高阶函数处理数据
print("\n===使用自定义高阶函数===")

# 平方处理
squared_numbers = data_processor(numbers, lambda x: x ** 2)
print(f"平方: {squared_numbers}")

# 转换为大写
uppercase_words = data_processor(words, lambda x: x.upper())
print(f"大写: {uppercase_words}")

# 添加前缀
prefixed_words = data_processor(words, lambda x: f"fruit_{x}")
print(f"添加前缀: {prefixed_words}")

# 筛选偶数
even_numbers = conditional_filter(numbers, lambda x: x % 2 == 0)
print(f"偶数: {even_numbers}")

# 筛选长度大于5的单词
long_words = conditional_filter(words, lambda x: len(x) > 5)
print(f"长单词: {long_words}")

# 计算总和
total_sum = data_aggregator(numbers, lambda acc, x: acc + x)
print(f"总和: {total_sum}")

# 计算乘积
product = data_aggregator(numbers, lambda acc, x: acc * x, 1)
print(f"乘积: {product}")

# 找到最大值
max_value = data_aggregator(numbers[1:], lambda acc, x: x if x > acc else acc, numbers[0])
print(f"最大值: {max_value}")

# 创建函数工厂
def create_multiplier(factor):
    """
    创建乘法器函数工厂
    
    参数:
        factor (number): 乘数因子
        
    返回:
        function: 乘法器函数
    """
    return lambda x: x * factor

def create_power(exponent):
    """
    创建幂运算函数工厂
    
    参数:
        exponent (number): 指数
        
    返回:
        function: 幂运算函数
    """
    return lambda x: x ** exponent

# 使用函数工厂
print("\n===函数工厂演示===")

# 创建不同的乘法器
double = create_multiplier(2)
triple = create_multiplier(3)
multiply_by_5 = create_multiplier(5)

print("乘法器测试:")
test_numbers = [1, 2, 3, 4, 5]
print(f"原始数字: {test_numbers}")
print(f"双倍: {[double(x) for x in test_numbers]}")
print(f"三倍: {[triple(x) for x in test_numbers]}")
print(f"五倍: {[multiply_by_5(x) for x in test_numbers]}")

# 创建不同的幂运算函数
square = create_power(2)
cube = create_power(3)
power_4 = create_power(4)

print("\n幂运算测试:")
print(f"原始数字: {test_numbers}")
print(f"平方: {[square(x) for x in test_numbers]}")
print(f"立方: {[cube(x) for x in test_numbers]}")
print(f"四次方: {[power_4(x) for x in test_numbers]}")

# 组合函数使用
print("\n===函数组合演示===")

# 创建复合函数：先平方再加倍
square_and_double = lambda x: double(square(x))
print(f"平方后加倍: {[square_and_double(x) for x in [1, 2, 3, 4]]}")

# 使用map、filter和lambda的组合
print("\n组合操作示例:")
# 找到偶数的平方
even_squares = list(map(
    lambda x: x ** 2,
    filter(lambda x: x % 2 == 0, numbers)
))
print(f"偶数的平方: {even_squares}")

# 找到长度大于4的单词并转为大写
long_words_upper = list(map(
    lambda x: x.upper(),
    filter(lambda x: len(x) > 4, words)
))
print(f"长单词大写: {long_words_upper}")
```

### 代码说明

**案例1代码解释**：
1. `key=lambda x: x["score"]`：使用lambda函数作为sorted函数的key参数
2. `map(lambda x: x["score"] * 1.2, students)`：使用lambda函数处理每个元素
3. `filter(lambda x: x["score"] >= 90, students)`：使用lambda函数作为筛选条件
4. lambda函数只能包含表达式，如`x["score"] * 1.2`，不能包含语句

如果在lambda函数中写`lambda x: print(x["name"]); x["score"] * 1.2`，会报语法错误，因为lambda函数中不能包含语句。

**案例2代码解释**：
1. `data_processor(data, process_func)`：高阶函数接收函数作为参数
2. `return [process_func(item) for item in data]`：对数据列表中的每个元素应用处理函数
3. `create_multiplier(factor)`：函数工厂，返回一个新的函数
4. `return lambda x: x * factor`：返回lambda函数，形成闭包

如果在循环中创建lambda函数时直接引用循环变量，如`[lambda x: x * i for i in range(3)]`，所有lambda函数都会使用最后一个i的值，需要使用默认参数来解决：`[lambda x, i=i: x * i for i in range(3)]`。

## 5. 递归函数

### 知识点解析

**概念定义**：递归函数就像俄罗斯套娃一样，函数在执行过程中调用自己。每次调用都处理问题的一小部分，直到遇到最简单的情况（基础情况），然后逐层返回结果。

**核心规则**：
1. 必须有基础情况（递归终止条件），否则会无限递归
2. 递归情况必须向基础情况靠近
3. 每次递归调用都应该处理规模更小的问题

**常见易错点**：
1. 忘记设置或错误设置基础情况，导致无限递归
2. 递归调用没有向基础情况靠近，导致栈溢出
3. 递归层次过深导致性能问题
4. 没有充分利用记忆化技术优化重复计算

### 实战案例

#### 案例1：数学计算和数列
```python
# 数学计算和数列
print("===数学计算和数列===")

# 计算阶乘（递归实现）
def factorial(n):
    """
    计算阶乘
    
    参数:
        n (int): 要计算阶乘的数
        
    返回:
        int: n的阶乘
    """
    # 基础情况：0! = 1, 1! = 1
    if n <= 1:
        return 1
    
    # 递归情况：n! = n * (n-1)!
    return n * factorial(n - 1)

# 计算斐波那契数列
def fibonacci(n):
    """
    计算斐波那契数列第n项
    
    参数:
        n (int): 项数
        
    返回:
        int: 第n项的值
    """
    # 基础情况：F(0) = 0, F(1) = 1
    if n <= 1:
        return n
    
    # 递归情况：F(n) = F(n-1) + F(n-2)
    return fibonacci(n - 1) + fibonacci(n - 2)

# 优化版斐波那契数列（记忆化）
fibonacci_cache = {}

def fibonacci_memo(n):
    """
    计算斐波那契数列第n项（记忆化版本）
    
    参数:
        n (int): 项数
        
    返回:
        int: 第n项的值
    """
    # 检查缓存
    if n in fibonacci_cache:
        return fibonacci_cache[n]
    
    # 基础情况
    if n <= 1:
        result = n
    else:
        # 递归情况
        result = fibonacci_memo(n - 1) + fibonacci_memo(n - 2)
    
    # 缓存结果
    fibonacci_cache[n] = result
    return result

# 计算幂运算
def power(base, exponent):
    """
    计算幂运算
    
    参数:
        base (number): 底数
        exponent (int): 指数
        
    返回:
        number: base的exponent次方
    """
    # 基础情况
    if exponent == 0:
        return 1
    if exponent == 1:
        return base
    
    # 递归情况
    if exponent > 0:
        return base * power(base, exponent - 1)
    else:
        # 处理负指数
        return 1 / power(base, -exponent)

# 演示递归函数
print("===阶乘计算===")
test_numbers = [0, 1, 2, 3, 4, 5, 6]
for num in test_numbers:
    result = factorial(num)
    print(f"{num}! = {result}")

print("\n===斐波那契数列===")
print("普通递归版本:")
for i in range(10):
    result = fibonacci(i)
    print(f"F({i}) = {result}")

print("\n记忆化版本:")
for i in range(10):
    result = fibonacci_memo(i)
    print(f"F({i}) = {result}")

print("\n===幂运算===")
test_cases = [(2, 3), (3, 4), (5, 0), (2, -3)]
for base, exp in test_cases:
    result = power(base, exp)
    if exp >= 0:
        print(f"{base}^{exp} = {result}")
    else:
        print(f"{base}^{exp} = {result:.4f}")
```

#### 案例2：数据结构和算法
```python
# 数据结构和算法
print("\n===数据结构和算法===")

# 二分查找（递归实现）
def binary_search_recursive(arr, target, left=0, right=None):
    """
    二分查找（递归实现）
    
    参数:
        arr (list): 有序数组
        target: 要查找的目标值
        left (int): 左边界
        right (int): 右边界
        
    返回:
        int: 目标值的索引，未找到返回-1
    """
    # 初始化右边界
    if right is None:
        right = len(arr) - 1
    
    # 基础情况：查找范围无效
    if left > right:
        return -1
    
    # 计算中间位置
    mid = (left + right) // 2
    
    # 基础情况：找到目标值
    if arr[mid] == target:
        return mid
    
    # 递归情况：在左半部分查找
    if arr[mid] > target:
        return binary_search_recursive(arr, target, left, mid - 1)
    
    # 递归情况：在右半部分查找
    return binary_search_recursive(arr, target, mid + 1, right)

# 计算最大公约数（欧几里得算法）
def gcd(a, b):
    """
    计算最大公约数
    
    参数:
        a (int): 第一个数
        b (int): 第二个数
        
    返回:
        int: 最大公约数
    """
    # 基础情况：b为0时，a就是最大公约数
    if b == 0:
        return a
    
    # 递归情况：gcd(a, b) = gcd(b, a % b)
    return gcd(b, a % b)

# 树结构遍历
class TreeNode:
    """树节点"""
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

def print_tree_inorder(node):
    """
    中序遍历二叉树（递归实现）
    
    参数:
        node (TreeNode): 树节点
    """
    # 基础情况：节点为空
    if node is None:
        return
    
    # 递归情况：左->根->右
    print_tree_inorder(node.left)   # 遍历左子树
    print(node.value, end=" ")      # 访问根节点
    print_tree_inorder(node.right)  # 遍历右子树

def print_tree_preorder(node):
    """
    前序遍历二叉树（递归实现）
    
    参数:
        node (TreeNode): 树节点
    """
    # 基础情况：节点为空
    if node is None:
        return
    
    # 递归情况：根->左->右
    print(node.value, end=" ")      # 访问根节点
    print_tree_preorder(node.left)  # 遍历左子树
    print_tree_preorder(node.right) # 遍历右子树

def print_tree_postorder(node):
    """
    后序遍历二叉树（递归实现）
    
    参数:
        node (TreeNode): 树节点
    """
    # 基础情况：节点为空
    if node is None:
        return
    
    # 递归情况：左->右->根
    print_tree_postorder(node.left)  # 遍历左子树
    print_tree_postorder(node.right) # 遍历右子树
    print(node.value, end=" ")       # 访问根节点

# 演示递归算法
print("===二分查找===")
sorted_array = [1, 3, 5, 7, 9, 11, 13, 15, 17, 19]
targets = [7, 1, 19, 4, 20]

for target in targets:
    index = binary_search_recursive(sorted_array, target)
    if index != -1:
        print(f"找到 {target}，索引为 {index}")
    else:
        print(f"未找到 {target}")

print("\n===最大公约数===")
gcd_test_cases = [(48, 18), (56, 42), (17, 13), (100, 25)]
for a, b in gcd_test_cases:
    result = gcd(a, b)
    print(f"gcd({a}, {b}) = {result}")

print("\n===二叉树遍历===")
# 创建二叉树
#       1
#      / \
#     2   3
#    / \   \
#   4   5   6
root = TreeNode(1)
root.left = TreeNode(2)
root.right = TreeNode(3)
root.left.left = TreeNode(4)
root.left.right = TreeNode(5)
root.right.right = TreeNode(6)

print("中序遍历 (左->根->右): ", end="")
print_tree_inorder(root)
print()

print("前序遍历 (根->左->右): ", end="")
print_tree_preorder(root)
print()

print("后序遍历 (左->右->根): ", end="")
print_tree_postorder(root)
print()

# 文件系统遍历（模拟）
def traverse_directory(path, level=0):
    """
    递归遍历目录结构
    
    参数:
        path (str): 目录路径
        level (int): 缩进级别
    """
    # 基础情况：这里简化处理，实际应该检查路径是否存在
    indent = "  " * level
    
    # 模拟目录内容
    if path == "/":
        contents = ["home", "usr", "var", "etc"]
    elif path == "/home":
        contents = ["user1", "user2", "docs"]
    elif path == "/home/user1":
        contents = ["Desktop", "Documents", "Downloads"]
    else:
        contents = []
    
    print(f"{indent}{path}/")
    
    # 递归情况：遍历子目录
    for item in contents:
        item_path = f"{path}/{item}" if path != "/" else f"/{item}"
        if item in ["home", "usr", "var", "etc", "user1", "user2", "Desktop", "Documents", "Downloads"]:
            traverse_directory(item_path, level + 1)

print("\n===目录结构遍历===")
traverse_directory("/")
```

### 代码说明

**案例1代码解释**：
1. `if n <= 1: return 1`：阶乘函数的基础情况
2. `return n * factorial(n - 1)`：递归情况，规模不断减小
3. `if n in fibonacci_cache:`：记忆化版本中检查缓存
4. `fibonacci_cache[n] = result`：将结果存储到缓存中

如果在阶乘函数中忘记写`if n <= 1: return 1`基础情况，调用`factorial(5)`会导致无限递归，最终栈溢出。

**案例2代码解释**：
1. `if left > right: return -1`：二分查找的基础情况（未找到）
2. `if arr[mid] == target: return mid`：二分查找的基础情况（找到）
3. `return binary_search_recursive(arr, target, left, mid - 1)`：在左半部分递归查找
4. `if b == 0: return a`：欧几里得算法的基础情况

如果在二分查找中写成`return binary_search_recursive(arr, target, left, mid)`而不是`return binary_search_recursive(arr, target, left, mid - 1)`，会导致在查找不存在的元素时无法终止递归。

## 6. 装饰器

### 知识点解析

**概念定义**：装饰器就像给函数"包装"一层额外功能的工具，它可以在不修改原函数代码的情况下，为函数增加新的行为。就像给手机套上保护壳，手机还是那个手机，但有了额外的保护功能。

**核心规则**：
1. 装饰器是一个函数，它接收一个函数作为参数并返回一个新的函数
2. 使用@符号应用装饰器
3. 装饰器可以修改函数的行为、添加功能或处理函数的输入输出

**常见易错点**：
1. 忘记装饰器函数需要返回一个函数
2. 在装饰器中错误处理函数的参数和返回值
3. 忽略装饰器对函数元信息（如__name__、__doc__）的影响
4. 在需要传递参数给装饰器时处理不当

### 实战案例

#### 案例1：实用装饰器集合
```python
# 实用装饰器集合
print("===实用装饰器集合===")

# 导入需要的模块
import time
import functools

# 计时装饰器
def timer(func):
    """
    计时装饰器：测量函数执行时间
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"{func.__name__} 执行时间: {end_time - start_time:.4f}秒")
        return result
    return wrapper

# 日志装饰器
def logger(func):
    """
    日志装饰器：记录函数调用
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print(f"调用函数 {func.__name__}")
        print(f"参数: args={args}, kwargs={kwargs}")
        result = func(*args, **kwargs)
        print(f"{func.__name__} 执行完成，返回值: {result}")
        return result
    return wrapper

# 重试装饰器
def retry(max_attempts=3, delay=1):
    """
    重试装饰器：在函数失败时自动重试
    
    参数:
        max_attempts (int): 最大尝试次数
        delay (float): 重试间隔（秒）
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_attempts):
                try:
                    result = func(*args, **kwargs)
                    print(f"{func.__name__} 执行成功")
                    return result
                except Exception as e:
                    print(f"{func.__name__} 第{attempt + 1}次尝试失败: {e}")
                    if attempt < max_attempts - 1:
                        print(f"等待 {delay} 秒后重试...")
                        time.sleep(delay)
                    else:
                        print(f"{func.__name__} 已达到最大尝试次数，执行失败")
                        raise
        return wrapper
    return decorator

# 缓存装饰器（简单版本）
def simple_cache(func):
    """
    简单缓存装饰器：缓存函数结果
    """
    cache = {}
    
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # 创建缓存键
        key = str(args) + str(sorted(kwargs.items()))
        
        # 检查缓存
        if key in cache:
            print(f"{func.__name__} 从缓存返回结果")
            return cache[key]
        
        # 执行函数并缓存结果
        result = func(*args, **kwargs)
        cache[key] = result
        print(f"{func.__name__} 执行并缓存结果")
        return result
    
    return wrapper

# 使用装饰器的函数
@timer
@logger
def calculate_sum(n):
    """
    计算1到n的和
    
    参数:
        n (int): 上限
        
    返回:
        int: 和
    """
    total = 0
    for i in range(1, n + 1):
        total += i
    return total

@timer
@simple_cache
def fibonacci_decorated(n):
    """
    计算斐波那契数列（装饰器版本）
    
    参数:
        n (int): 项数
        
    返回:
        int: 第n项
    """
    if n <= 1:
        return n
    return fibonacci_decorated(n - 1) + fibonacci_decorated(n - 2)

@retry(max_attempts=3, delay=0.5)
def risky_operation(success_rate=0.5):
    """
    模拟可能失败的操作
    
    参数:
        success_rate (float): 成功率
        
    返回:
        str: 成功消息
    """
    import random
    if random.random() > success_rate:
        raise Exception("操作失败")
    return "操作成功"

# 演示装饰器
print("===计时和日志装饰器===")
result = calculate_sum(100)
print(f"结果: {result}\n")

print("===缓存装饰器===")
print("第一次调用:")
fib_10 = fibonacci_decorated(10)
print(f"fibonacci(10) = {fib_10}\n")

print("第二次调用:")
fib_10_again = fibonacci_decorated(10)
print(f"fibonacci(10) = {fib_10_again}\n")

print("计算不同的值:")
fib_8 = fibonacci_decorated(8)
print(f"fibonacci(8) = {fib_8}\n")

print("===重试装饰器===")
print("高成功率操作:")
try:
    result = risky_operation(0.7)
    print(f"结果: {result}\n")
except Exception as e:
    print(f"最终失败: {e}\n")

print("低成功率操作:")
try:
    result = risky_operation(0.1)
    print(f"结果: {result}\n")
except Exception as e:
    print(f"最终失败: {e}\n")
```

#### 案例2：Web应用装饰器
```python
# Web应用装饰器
print("===Web应用装饰器===")

# 模拟用户会话
current_user = None
user_permissions = set()

# 用户登录装饰器
def login_required(func):
    """
    登录检查装饰器：确保用户已登录
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        global current_user
        if current_user is None:
            print(f"错误: 调用 {func.__name__} 前请先登录")
            return None
        return func(*args, **kwargs)
    return wrapper

# 权限检查装饰器
def permission_required(permission):
    """
    权限检查装饰器：确保用户具有指定权限
    
    参数:
        permission (str): 需要的权限
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            global current_user, user_permissions
            if current_user is None:
                print(f"错误: 调用 {func.__name__} 前请先登录")
                return None
            if permission not in user_permissions:
                print(f"错误: 用户 {current_user} 没有权限 '{permission}'")
                return None
            return func(*args, **kwargs)
        return wrapper
    return decorator

# 请求日志装饰器
def request_logger(func):
    """
    请求日志装饰器：记录Web请求
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        global current_user
        user_info = current_user if current_user else "未登录用户"
        print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {user_info} 访问 {func.__name__}")
        result = func(*args, **kwargs)
        print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {func.__name__} 响应: {result}")
        return result
    return wrapper

# 性能监控装饰器
def performance_monitor(threshold=1.0):
    """
    性能监控装饰器：监控函数执行时间
    
    参数:
        threshold (float): 时间阈值（秒）
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            result = func(*args, **kwargs)
            end_time = time.time()
            execution_time = end_time - start_time
            
            if execution_time > threshold:
                print(f"警告: {func.__name__} 执行时间过长 ({execution_time:.4f}秒 > {threshold}秒)")
            
            return result
        return wrapper
    return decorator

# 模拟Web应用函数
@request_logger
@login_required
def view_profile():
    """查看个人资料"""
    return f"用户 {current_user} 的个人资料"

@request_logger
@login_required
@permission_required("admin")
def manage_users():
    """管理用户"""
    return "用户管理页面"

@request_logger
@performance_monitor(threshold=0.5)
def slow_data_processing():
    """模拟慢速数据处理"""
    time.sleep(1)  # 模拟耗时操作
    return "数据处理完成"

@request_logger
def public_page():
    """公开页面"""
    return "欢迎访问我们的网站"

# 用户管理函数
def login(username, permissions=None):
    """用户登录"""
    global current_user, user_permissions
    current_user = username
    user_permissions = set(permissions) if permissions else set()
    print(f"用户 {username} 登录成功")

def logout():
    """用户登出"""
    global current_user, user_permissions
    print(f"用户 {current_user} 登出")
    current_user = None
    user_permissions = set()

# 演示Web应用装饰器
print("===未登录访问===")
result1 = view_profile()
print(f"结果: {result1}\n")

result2 = manage_users()
print(f"结果: {result2}\n")

result3 = public_page()
print(f"结果: {result3}\n")

print("===普通用户登录===")
login("张三", ["user"])
print()

result4 = view_profile()
print(f"结果: {result4}\n")

result5 = manage_users()
print(f"结果: {result5}\n")

result6 = public_page()
print(f"结果: {result6}\n")

print("===管理员登录===")
logout()
login("管理员", ["user", "admin"])
print()

result7 = view_profile()
print(f"结果: {result7}\n")

result8 = manage_users()
print(f"结果: {result8}\n")

result9 = slow_data_processing()
print(f"结果: {result9}\n")

print("===登出后访问===")
logout()
print()

result10 = view_profile()
print(f"结果: {result10}\n")
```

### 代码说明

**案例1代码解释**：
1. `@functools.wraps(func)`：保持原函数的元信息（如__name__、__doc__）
2. `def wrapper(*args, **kwargs):`：装饰器的包装函数接收任意参数
3. `return decorator`：参数化装饰器返回真正的装饰器函数
4. `cache = {}`：在装饰器内部维护缓存状态

如果忘记使用`@functools.wraps(func)`，被装饰函数的`__name__`属性会变成`wrapper`，而不是原来的函数名。

**案例2代码解释**：
1. `def permission_required(permission):`：参数化装饰器，接收权限参数
2. `global current_user, user_permissions`：在装饰器中访问全局状态
3. 多个装饰器可以叠加使用，如`@request_logger`、`@login_required`、`@permission_required("admin")`
4. 装饰器按从上到下的顺序应用

如果在嵌套装饰器中顺序错误，比如把权限检查放在登录检查之前，可能会导致逻辑错误，因为权限检查依赖于用户已登录的前提。

## 7. 最佳实践和注意事项

### 知识点解析

**概念定义**：最佳实践就像经验丰富的老师傅传授的工作技巧，帮助我们写出更清晰、更可靠、更易于维护的代码。注意事项则是容易踩坑的地方，提前了解可以避免犯错。

**核心规则**：
1. 函数应该短小精悍，只做一件事
2. 使用有意义的函数名和参数名
3. 合理使用参数默认值
4. 添加适当的文档字符串
5. 避免副作用和全局状态依赖

**常见易错点**：
1. 函数过长过复杂，难以理解和维护
2. 函数名和参数名含义不清
3. 滥用可变对象作为默认参数
4. 忽略错误处理和边界条件
5. 函数之间耦合度过高

### 实战案例

#### 案例1：良好的函数设计
```python
# 良好的函数设计
print("===良好的函数设计===")

# 不好的函数设计示例
def bad_process_student_data(name, age, scores, operation):
    """不好的函数设计：功能太多，参数混乱"""
    # 数据验证
    if not name or not isinstance(name, str):
        return "错误：姓名无效"
    if not isinstance(age, int) or age < 0 or age > 150:
        return "错误：年龄无效"
    if not isinstance(scores, list) or not scores:
        return "错误：成绩无效"
    
    # 根据操作类型执行不同功能
    if operation == "average":
        total = 0
        for score in scores:
            total += score
        return total / len(scores)
    elif operation == "grade":
        total = 0
        for score in scores:
            total += score
        average = total / len(scores)
        if average >= 90:
            return "优秀"
        elif average >= 80:
            return "良好"
        elif average >= 70:
            return "中等"
        elif average >= 60:
            return "及格"
        else:
            return "不及格"
    elif operation == "report":
        total = 0
        for score in scores:
            total += score
        average = total / len(scores)
        if average >= 90:
            grade = "优秀"
        elif average >= 80:
            grade = "良好"
        elif average >= 70:
            grade = "中等"
        elif average >= 60:
            grade = "及格"
        else:
            grade = "不及格"
        return f"学生: {name}, 年龄: {age}, 平均分: {average:.2f}, 等级: {grade}"
    else:
        return "错误：不支持的操作"

# 改进的函数设计
def validate_student_name(name):
    """
    验证学生姓名
    
    参数:
        name (str): 学生姓名
        
    返回:
        bool: 验证结果
    """
    return isinstance(name, str) and len(name.strip()) > 0

def validate_student_age(age):
    """
    验证学生年龄
    
    参数:
        age (int): 学生年龄
        
    返回:
        bool: 验证结果
    """
    return isinstance(age, int) and 0 <= age <= 150

def validate_student_scores(scores):
    """
    验证学生成绩
    
    参数:
        scores (list): 成绩列表
        
    返回:
        bool: 验证结果
    """
    return isinstance(scores, list) and len(scores) > 0 and all(isinstance(score, (int, float)) for score in scores)

def calculate_average_score(scores):
    """
    计算平均分
    
    参数:
        scores (list): 成绩列表
        
    返回:
        float: 平均分
    """
    if not validate_student_scores(scores):
        raise ValueError("成绩数据无效")
    
    return sum(scores) / len(scores)

def get_grade_from_average(average):
    """
    根据平均分获取等级
    
    参数:
        average (float): 平均分
        
    返回:
        str: 等级
    """
    if average >= 90:
        return "优秀"
    elif average >= 80:
        return "良好"
    elif average >= 70:
        return "中等"
    elif average >= 60:
        return "及格"
    else:
        return "不及格"

def generate_student_report(name, age, scores):
    """
    生成学生成绩报告
    
    参数:
        name (str): 学生姓名
        age (int): 学生年龄
        scores (list): 成绩列表
        
    返回:
        str: 成绩报告
    """
    # 验证输入数据
    if not validate_student_name(name):
        raise ValueError("姓名无效")
    if not validate_student_age(age):
        raise ValueError("年龄无效")
    if not validate_student_scores(scores):
        raise ValueError("成绩数据无效")
    
    # 计算平均分
    average = calculate_average_score(scores)
    
    # 获取等级
    grade = get_grade_from_average(average)
    
    # 生成报告
    report = f"=== 学生成绩报告 ===\n"
    report += f"姓名: {name}\n"
    report += f"年龄: {age}\n"
    report += f"各科成绩: {scores}\n"
    report += f"平均分: {average:.2f}\n"
    report += f"等级: {grade}\n"
    
    return report

# 演示良好的函数设计
print("===改进前的函数设计===")
result1 = bad_process_student_data("张三", 20, [85, 90, 78, 92], "average")
print(f"平均分: {result1}")

result2 = bad_process_student_data("张三", 20, [85, 90, 78, 92], "grade")
print(f"等级: {result2}")

result3 = bad_process_student_data("张三", 20, [85, 90, 78, 92], "report")
print(f"报告:\n{result3}")

print("\n===改进后的函数设计===")
try:
    # 验证数据
    name = "张三"
    age = 20
    scores = [85, 90, 78, 92]
    
    # 计算平均分
    average = calculate_average_score(scores)
    print(f"平均分: {average:.2f}")
    
    # 获取等级
    grade = get_grade_from_average(average)
    print(f"等级: {grade}")
    
    # 生成报告
    report = generate_student_report(name, age, scores)
    print(f"报告:\n{report}")
    
except ValueError as e:
    print(f"错误: {e}")
```

#### 案例2：避免常见错误
```python
# 避免常见错误
print("\n===避免常见错误===")

# 错误1：可变对象作为默认参数
print("===错误1：可变对象作为默认参数===")

# 错误的做法
def add_item_wrong(item, target_list=[]):
    """错误：使用可变对象作为默认参数"""
    target_list.append(item)
    return target_list

# 演示错误
print("错误的做法:")
list1 = add_item_wrong("苹果")
print(f"第一次调用: {list1}")

list2 = add_item_wrong("香蕉")
print(f"第二次调用: {list2}")  # 意外包含了"苹果"
print(f"第一次结果也变了: {list1}")  # 同一个列表对象

# 正确的做法
def add_item_correct(item, target_list=None):
    """正确：合理处理默认参数"""
    if target_list is None:
        target_list = []
    target_list.append(item)
    return target_list

# 演示正确的做法
print("\n正确的做法:")
list3 = add_item_correct("苹果")
print(f"第一次调用: {list3}")

list4 = add_item_correct("香蕉")
print(f"第二次调用: {list4}")  # 只包含"香蕉"
print(f"第一次结果不变: {list3}")  # 仍然只包含"苹果"

# 错误2：忽略函数副作用
print("\n===错误2：忽略函数副作用===")

# 带有副作用的函数
global_counter = 0

def process_with_side_effect(data):
    """带有副作用的函数"""
    global global_counter
    global_counter += 1  # 修改全局状态
    return [x * global_counter for x in data]

# 演示副作用问题
print("带有副作用的函数:")
data1 = [1, 2, 3]
result1 = process_with_side_effect(data1)
print(f"第一次调用: {result1}, 全局计数器: {global_counter}")

result2 = process_with_side_effect(data1)
print(f"第二次调用: {result2}, 全局计数器: {global_counter}")

# 无副作用的函数
def process_without_side_effect(data, multiplier):
    """无副作用的函数"""
    return [x * multiplier for x in data]

# 演示无副作用的做法
print("\n无副作用的函数:")
data2 = [1, 2, 3]
result3 = process_without_side_effect(data2, 1)
print(f"第一次调用: {result3}")

result4 = process_without_side_effect(data2, 2)
print(f"第二次调用: {result4}")

# 错误3：函数过长过复杂
print("\n===错误3：函数过长过复杂===")

# 过长的函数
def complex_calculation_old(x, y, z):
    """过长过复杂的函数"""
    # 第一部分：数据验证
    if not isinstance(x, (int, float)):
        return "错误：x必须是数字"
    if not isinstance(y, (int, float)):
        return "错误：y必须是数字"
    if not isinstance(z, (int, float)):
        return "错误：z必须是数字"
    
    # 第二部分：计算平方
    x_squared = x * x
    y_squared = y * y
    z_squared = z * z
    
    # 第三部分：计算和
    sum_of_squares = x_squared + y_squared + z_squared
    
    # 第四部分：计算平方根
    import math
    if sum_of_squares < 0:
        return "错误：无法计算负数的平方根"
    result = math.sqrt(sum_of_squares)
    
    # 第五部分：格式化结果
    formatted_result = f"sqrt({x}² + {y}² + {z}²) = {result:.4f}"
    
    # 第六部分：日志记录
    print(f"执行了复杂计算: x={x}, y={y}, z={z}")
    print(f"中间结果: x²={x_squared}, y²={y_squared}, z²={z_squared}")
    print(f"最终结果: {formatted_result}")
    
    return formatted_result

# 重构为多个小函数
def validate_number(value, name):
    """验证数字"""
    if not isinstance(value, (int, float)):
        raise ValueError(f"{name}必须是数字")

def calculate_square(x):
    """计算平方"""
    return x * x

def calculate_sum_of_squares(x, y, z):
    """计算平方和"""
    return calculate_square(x) + calculate_square(y) + calculate_square(z)

def calculate_square_root(value):
    """计算平方根"""
    import math
    if value < 0:
        raise ValueError("无法计算负数的平方根")
    return math.sqrt(value)

def format_calculation_result(x, y, z, result):
    """格式化计算结果"""
    return f"sqrt({x}² + {y}² + {z}²) = {result:.4f}"

def log_calculation(x, y, z, intermediate_results, final_result):
    """记录计算日志"""
    print(f"执行了计算: x={x}, y={y}, z={z}")
    print(f"中间结果: {intermediate_results}")
    print(f"最终结果: {final_result}")

def complex_calculation_new(x, y, z):
    """重构后的复杂计算函数"""
    # 验证输入
    validate_number(x, "x")
    validate_number(y, "y")
    validate_number(z, "z")
    
    # 计算平方和
    sum_of_squares = calculate_sum_of_squares(x, y, z)
    
    # 计算平方根
    result = calculate_square_root(sum_of_squares)
    
    # 格式化结果
    formatted_result = format_calculation_result(x, y, z, result)
    
    # 记录日志
    intermediate = {
        "x²": calculate_square(x),
        "y²": calculate_square(y),
        "z²": calculate_square(z)
    }
    log_calculation(x, y, z, intermediate, formatted_result)
    
    return formatted_result

# 演示重构效果
print("重构前的复杂函数:")
result_old = complex_calculation_old(3, 4, 5)
print(f"结果: {result_old}")

print("\n重构后的函数:")
result_new = complex_calculation_new(3, 4, 5)
print(f"结果: {result_new}")

# 错误4：忽略错误处理
print("\n===错误4：忽略错误处理===")

# 没有错误处理的函数
def divide_without_error_handling(a, b):
    """没有错误处理的除法函数"""
    return a / b

# 有错误处理的函数
def divide_with_error_handling(a, b):
    """有错误处理的除法函数"""
    try:
        if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
            raise TypeError("参数必须是数字")
        if b == 0:
            raise ValueError("除数不能为零")
        return a / b
    except (TypeError, ValueError) as e:
        print(f"计算错误: {e}")
        return None

# 演示错误处理的重要性
print("没有错误处理:")
try:
    result1 = divide_without_error_handling(10, 0)
    print(f"10 / 0 = {result1}")
except ZeroDivisionError as e:
    print(f"捕获到错误: {e}")

print("\n有错误处理:")
result2 = divide_with_error_handling(10, 0)
print(f"10 / 0 = {result2}")

result3 = divide_with_error_handling(10, "abc")
print(f"10 / 'abc' = {result3}")

result4 = divide_with_error_handling(10, 2)
print(f"10 / 2 = {result4}")
```

### 代码说明

**案例1代码解释**：
1. `bad_process_student_data`函数违反了"单一职责原则"，一个函数做了太多事情
2. 改进后的函数每个只负责一个特定任务，如`validate_student_name`、`calculate_average_score`等
3. 使用有意义的函数名和参数名，如`get_grade_from_average`清楚表达了函数功能
4. 添加了适当的文档字符串说明函数用途、参数和返回值

如果继续使用`bad_process_student_data`这样的函数，当需要修改成绩计算逻辑时，会影响所有操作，增加了维护难度和出错风险。

**案例2代码解释**：
1. `add_item_wrong`函数使用`[]`作为默认参数，导致多个调用共享同一个列表对象
2. `process_with_side_effect`函数修改全局状态，使得函数行为不可预测
3. `complex_calculation_old`函数过长过复杂，难以理解和维护
4. `divide_without_error_handling`函数没有处理除零等异常情况

如果在团队开发中使用这些有问题的函数，会导致难以调试的bug和维护困难。通过重构和遵循最佳实践，可以大大提高代码质量和可维护性。