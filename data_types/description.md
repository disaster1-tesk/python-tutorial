# Python数据类型知识点

## 1. 数字类型 (Numeric Types)

### 知识点解析

**概念定义**：数字类型就像我们在生活中使用的各种数字一样，Python中有三种主要的数字类型：整数（int）就像我们数数时用的1、2、3；浮点数（float）就像我们测量时用的3.14、2.5；复数（complex）就像我们在高等数学中用的3+4j。

**核心规则**：
1. 整数（int）没有小数点，可以是正数、负数或零
2. 浮点数（float）有小数点，用来表示小数
3. 复数（complex）由实部和虚部组成，虚部以j或J结尾
4. 可以使用type()函数查看数据类型

**常见易错点**：
1. 混淆整数除法和浮点数除法，在Python 3中 `/` 总是返回浮点数，`//` 才是整数除法
2. 浮点数精度问题，如0.1+0.2不等于0.3
3. 在需要整数的地方误用了字符串，如"5"+3会报错

### 实战案例

#### 案例1：简单计算器
```python
# 简单计算器演示数字类型
print("===计算器演示===")

# 整数运算
a = 10
b = 3
print(f"整数运算: {a} 和 {b}")
print(f"加法: {a} + {b} = {a + b}")
print(f"减法: {a} - {b} = {a - b}")
print(f"乘法: {a} * {b} = {a * b}")
print(f"浮点数除法: {a} / {b} = {a / b}")      # 结果是浮点数
print(f"整数除法: {a} // {b} = {a // b}")      # 结果是整数
print(f"求余: {a} % {b} = {a % b}")
print(f"幂运算: {a} ** {b} = {a ** b}")

# 浮点数运算
x = 10.5
y = 3.2
print(f"\n浮点数运算: {x} 和 {y}")
print(f"加法: {x} + {y} = {x + y}")
print(f"减法: {x} - {y} = {x - y}")

# 浮点数精度问题演示
print(f"\n浮点数精度问题:")
print(f"0.1 + 0.2 = {0.1 + 0.2}")  # 实际结果是0.30000000000000004
print(f"0.1 + 0.2 == 0.3 ? {0.1 + 0.2 == 0.3}")  # 结果是False

# 复数运算
z1 = 3 + 4j
z2 = 1 + 2j
print(f"\n复数运算: {z1} 和 {z2}")
print(f"加法: {z1} + {z2} = {z1 + z2}")
print(f"减法: {z1} - {z2} = {z1 - z2}")
print(f"乘法: {z1} * {z2} = {z1 * z2}")
```

#### 案例2：学生成绩统计分析
```python
# 学生成绩统计分析
print("===学生成绩统计分析===")

# 学生成绩（整数）
math_scores = [85, 92, 78, 96, 88, 78, 95, 89, 91, 87]
english_scores = [90, 85, 82, 94, 89, 85, 92, 88, 90, 86]

# 计算数学成绩统计
math_total = sum(math_scores)           # 总分
math_count = len(math_scores)           # 人数
math_average = math_total / math_count  # 平均分（浮点数）

# 计算英语成绩统计
english_total = sum(english_scores)
english_count = len(english_scores)
english_average = english_total / english_count

# 找出最高分和最低分
math_max = max(math_scores)
math_min = min(math_scores)
english_max = max(english_scores)
english_min = min(english_scores)

# 输出统计结果
print(f"数学成绩分析:")
print(f"  参考人数: {math_count}")
print(f"  总分: {math_total}")
print(f"  平均分: {math_average:.2f}")  # 保留两位小数
print(f"  最高分: {math_max}")
print(f"  最低分: {math_min}")

print(f"\n英语成绩分析:")
print(f"  参考人数: {english_count}")
print(f"  总分: {english_total}")
print(f"  平均分: {english_average:.2f}")
print(f"  最高分: {english_max}")
print(f"  最低分: {english_min}")

# 计算两科成绩的相关性（简化版）
# 使用复数表示成绩对，实部为数学成绩，虚部为英语成绩
score_pairs = [complex(math_scores[i], english_scores[i]) 
               for i in range(len(math_scores))]
print(f"\n成绩对表示（复数形式）:")
for i, pair in enumerate(score_pairs[:5]):  # 只显示前5个
    print(f"  学生{i+1}: 数学{pair.real:.0f}分, 英语{pair.imag:.0f}分")
```

### 代码说明

**案例1代码解释**：
1. `a = 10` 和 `b = 3`：创建两个整数变量
2. `a / b`：使用单斜杠进行除法运算，结果是浮点数3.3333333333333335
3. `a // b`：使用双斜杠进行整数除法，结果是整数3
4. `0.1 + 0.2`：演示浮点数精度问题，结果不是精确的0.3
5. `z1 = 3 + 4j`：创建复数，3是实部，4j是虚部

如果把 `a // b` 写成 `a / b`，对于10除以3，结果会从整数3变成浮点数3.3333333333333335。

**案例2代码解释**：
1. `math_scores = [85, 92, 78, ...]`：创建整数列表存储成绩
2. `math_average = math_total / math_count`：计算平均分，结果是浮点数
3. `print(f"平均分: {math_average:.2f}")`：格式化输出，保留两位小数
4. `complex(math_scores[i], english_scores[i])`：使用复数来表示成对的数据

如果把 `math_average = math_total / math_count` 写成 `math_average = math_total // math_count`，那么平均分就会变成整数，丢失了小数部分，不够精确。

## 2. 布尔类型 (Boolean Type)

### 知识点解析

**概念定义**：布尔类型就像开关一样，只有两种状态：真(True)或假(False)。它用于表示是/否、开/关、对/错这样的二元状态。在Python中，布尔类型以True和False表示。

**核心规则**：
1. 布尔类型只有两个值：True和False（注意首字母大写）
2. 布尔值常用于条件判断和逻辑运算
3. 在数值运算中，True等于1，False等于0
4. 任何对象都可以被测试为布尔值，空值通常为False，非空值通常为True

**常见易错点**：
1. 混淆True/False与"True"/"False"，前者是布尔值，后者是字符串
2. 在条件判断中误用赋值符=而不是比较符==
3. 对空列表、空字典等的布尔值判断错误

### 实战案例

#### 案例1：用户登录验证系统
```python
# 用户登录验证系统
print("===用户登录验证系统===")

# 模拟用户数据库
users_db = {
    "admin": "admin123",
    "user1": "pass456",
    "user2": "mypassword"
}

# 登录函数
def login(username, password):
    """
    用户登录验证
    
    参数:
        username (str): 用户名
        password (str): 密码
        
    返回:
        bool: 登录成功返回True，失败返回False
    """
    # 检查用户名是否存在
    if username in users_db:
        # 检查密码是否正确
        if users_db[username] == password:
            return True  # 登录成功
    return False  # 登录失败

# 年龄验证函数
def is_adult(age):
    """
    判断是否成年
    
    参数:
        age (int): 年龄
        
    返回:
        bool: 成年返回True，未成年返回False
    """
    return age >= 18

# 主程序
print("请输入登录信息:")
username = input("用户名: ")
password = input("密码: ")

# 验证登录
login_success = login(username, password)
if login_success:
    print("登录成功!")
    
    # 登录成功后进行年龄验证
    try:
        age = int(input("请输入您的年龄: "))
        adult_status = is_adult(age)
        if adult_status:
            print("您是成年人，可以访问所有内容")
        else:
            print("您是未成年人，部分内容受限")
    except ValueError:
        print("年龄输入错误")
else:
    print("用户名或密码错误，登录失败")
```

#### 案例2：学生成绩评定系统
```python
# 学生成绩评定系统
print("===学生成绩评定系统===")

def evaluate_score(score):
    """
    根据分数评定等级
    
    参数:
        score (int): 分数
        
    返回:
        tuple: (等级, 是否及格)
    """
    if score >= 90:
        return ("优秀", True)
    elif score >= 80:
        return ("良好", True)
    elif score >= 70:
        return ("中等", True)
    elif score >= 60:
        return ("及格", True)
    else:
        return ("不及格", False)

def check_award_eligibility(grades):
    """
    检查是否符合奖学金条件
    
    参数:
        grades (list): 各科成绩列表
        
    返回:
        bool: 符合条件返回True，否则返回False
    """
    # 条件1: 所有科目及格
    all_passed = all(grade >= 60 for grade in grades)
    
    # 条件2: 平均分85以上
    average = sum(grades) / len(grades)
    high_average = average >= 85
    
    # 条件3: 没有科目低于70分
    no_low_grades = all(grade >= 70 for grade in grades)
    
    # 同时满足三个条件才能获得奖学金
    return all_passed and high_average and no_low_grades

# 学生成绩数据
students_data = {
    "张三": [95, 87, 92, 88],
    "李四": [78, 82, 75, 80],
    "王五": [90, 92, 88, 94],
    "赵六": [58, 65, 70, 62]
}

# 评定每个学生的成绩
for name, grades in students_data.items():
    print(f"\n学生: {name}")
    print(f"各科成绩: {grades}")
    
    # 计算总分和平均分
    total = sum(grades)
    average = total / len(grades)
    print(f"总分: {total}, 平均分: {average:.2f}")
    
    # 评定等级
    grade, passed = evaluate_score(average)
    print(f"等级: {grade}, 是否及格: {'是' if passed else '否'}")
    
    # 检查奖学金资格
    award_eligible = check_award_eligibility(grades)
    print(f"奖学金资格: {'符合' if award_eligible else '不符合'}")
```

### 代码说明

**案例1代码解释**：
1. `return True` 和 `return False`：函数返回布尔值表示成功或失败
2. `if login_success:`：直接使用布尔变量进行条件判断
3. `age >= 18`：比较运算返回布尔值
4. `adult_status = is_adult(age)`：接收函数返回的布尔值

如果把 `users_db[username] == password` 写成 `users_db[username] = password`，这会变成赋值操作而不是比较操作，不仅逻辑错误，还会修改数据库。

**案例2代码解释**：
1. `all(grade >= 60 for grade in grades)`：使用all()函数检查所有成绩是否及格
2. `all_passed and high_average and no_low_grades`：使用逻辑与运算符组合多个条件
3. `{'是' if passed else '否'}`：使用条件表达式根据布尔值选择输出内容

如果把 `all(grade >= 60 for grade in grades)` 写成 `any(grade >= 60 for grade in grades)`，那么只要有一个科目及格就会返回True，而不是要求所有科目都及格。

## 3. 字符串类型 (String Type)

### 知识点解析

**概念定义**：字符串就像一串珠子，每个珠子都是一个字符。在Python中，字符串是用来存储文本信息的数据类型，可以是一个字母、一个词，或者一整段文字。

**核心规则**：
1. 字符串可以用单引号(')、双引号(")或三引号('''或""")包围
2. 字符串是不可变的，一旦创建就不能修改
3. 可以使用索引访问字符串中的单个字符
4. 支持各种字符串方法，如upper()、lower()、split()等

**常见易错点**：
1. 混淆字符串和变量名，如print(hello)和print("hello")完全不同
2. 字符串索引越界，如对长度为5的字符串访问索引5
3. 忘记字符串是不可变的，试图直接修改字符串中的字符

### 实战案例

#### 案例1：个人信息处理系统
```python
# 个人信息处理系统
print("===个人信息处理系统===")

# 获取用户输入
name = input("请输入您的姓名: ")
age_str = input("请输入您的年龄: ")
email = input("请输入您的邮箱: ")

# 字符串处理
# 去除姓名前后的空格并首字母大写
processed_name = name.strip().title()
print(f"处理后的姓名: {processed_name}")

# 验证年龄输入
if age_str.isdigit():  # 检查是否全为数字
    age = int(age_str)
    age_category = "成年人" if age >= 18 else "未成年人"
    print(f"年龄: {age}岁 ({age_category})")
else:
    print("年龄输入有误")

# 邮箱处理和验证
processed_email = email.strip().lower()  # 转换为小写并去除空格
if "@" in processed_email and "." in processed_email:
    print(f"邮箱: {processed_email}")
    
    # 提取邮箱服务商
    at_index = processed_email.find("@")
    domain = processed_email[at_index+1:]
    print(f"邮箱服务商: {domain}")
else:
    print("邮箱格式不正确")

# 密码强度检查
password = input("请设置密码: ")
def check_password_strength(pwd):
    """
    检查密码强度
    
    参数:
        pwd (str): 密码
        
    返回:
        str: 强度评价
    """
    if len(pwd) < 6:
        return "弱"
    elif len(pwd) < 10:
        return "中等"
    else:
        # 检查是否包含数字、大写字母、小写字母和特殊字符
        has_digit = any(c.isdigit() for c in pwd)
        has_upper = any(c.isupper() for c in pwd)
        has_lower = any(c.islower() for c in pwd)
        has_special = any(c in "!@#$%^&*()" for c in pwd)
        
        if has_digit and has_upper and has_lower and has_special:
            return "强"
        else:
            return "中等"

password_strength = check_password_strength(password)
print(f"密码强度: {password_strength}")
```

#### 案例2：文本分析工具
```python
# 文本分析工具
print("===文本分析工具===")

# 示例文本
text = """
Python是一种广泛使用的解释型、高级编程、通用型编程语言。
Python支持多种编程范型，主要包括面向对象、命令式、函数式和过程式编程。
Python于1991年首次发布，由Guido van Rossum创建。
Python的设计哲学强调代码的可读性和简洁的语法。
"""

print("原文本:")
print(text)

# 基本文本统计
char_count = len(text)  # 字符总数
word_count = len(text.split())  # 词数（以空格分割）
line_count = len(text.splitlines())  # 行数

print(f"\n基本统计:")
print(f"字符数: {char_count}")
print(f"词数: {word_count}")
print(f"行数: {line_count}")

# 字符频率分析
def analyze_char_frequency(text):
    """
    分析字符频率
    
    参数:
        text (str): 要分析的文本
        
    返回:
        dict: 字符频率字典
    """
    frequency = {}
    for char in text.lower():  # 转换为小写进行统计
        if char.isalpha():  # 只统计字母
            frequency[char] = frequency.get(char, 0) + 1
    
    # 按频率排序
    sorted_frequency = sorted(frequency.items(), key=lambda x: x[1], reverse=True)
    return sorted_frequency

char_frequency = analyze_char_frequency(text)
print(f"\n字母频率前5名:")
for char, count in char_frequency[:5]:
    print(f"  {char}: {count}次")

# 关键词搜索
keywords = ["python", "编程", "代码"]
print(f"\n关键词出现次数:")
for keyword in keywords:
    count = text.lower().count(keyword.lower())
    print(f"  '{keyword}': {count}次")

# 文本替换示例
print(f"\n文本替换:")
replaced_text = text.replace("Python", "Python语言")
print("将'Python'替换为'Python语言'后的文本:")
print(replaced_text[:100] + "...")  # 只显示前100个字符

# 字符串切片示例
print(f"\n字符串切片:")
print(f"前20个字符: '{text[:20]}'")
print(f"后20个字符: '{text[-20:]}'")
print(f"中间20个字符: '{text[len(text)//2-10:len(text)//2+10]}'")
```

### 代码说明

**案例1代码解释**：
1. `name.strip().title()`：链式调用字符串方法，先去除空格再首字母大写
2. `age_str.isdigit()`：检查字符串是否全为数字
3. `processed_email.find("@")`：查找字符@的位置
4. `any(c.isdigit() for c in pwd)`：检查密码中是否包含数字

如果把 `name.strip().title()` 写成 `name.title().strip()`，虽然结果相同，但逻辑上应该是先去空格再处理大小写更合理。

**案例2代码解释**：
1. `len(text.split())`：使用split()分割字符串后计算词数
2. `text.lower().count(keyword.lower())`：转换为小写后进行不区分大小写的计数
3. `text[:20]`：使用切片获取字符串的前20个字符
4. `frequency.get(char, 0)`：字典的get方法，如果键不存在则返回默认值0

如果把 `text.split()` 写成 `text.split("")`，试图用空字符串分割，会导致错误，因为split()的参数不能为空字符串。

## 4. 列表类型 (List Type)

### 知识点解析

**概念定义**：列表就像一个有序的盒子队列，每个盒子里可以放不同的东西。在Python中，列表是一种有序的集合，可以存储任意类型的元素，并且可以随时添加、删除或修改其中的元素。

**核心规则**：
1. 列表用方括号[]定义，元素之间用逗号分隔
2. 列表是可变的，可以修改、添加、删除元素
3. 列表中的元素可以是不同的数据类型
4. 列表支持索引和切片操作

**常见易错点**：
1. 列表索引越界，如对长度为3的列表访问索引3
2. 混淆append()和extend()方法的使用
3. 浅拷贝问题，直接赋值会导致两个变量指向同一个列表

### 实战案例

#### 案例1：购物车管理系统
```python
# 购物车管理系统
print("===购物车管理系统===")

# 初始化购物车
shopping_cart = []

# 商品信息
products = {
    1: {"name": "苹果", "price": 5.5},
    2: {"name": "香蕉", "price": 3.0},
    3: {"name": "橙子", "price": 4.2},
    4: {"name": "牛奶", "price": 12.0},
    5: {"name": "面包", "price": 8.5}
}

def display_products():
    """显示商品列表"""
    print("\n商品列表:")
    for id, product in products.items():
        print(f"{id}. {product['name']} - {product['price']}元")

def add_to_cart(product_id, quantity):
    """
    添加商品到购物车
    
    参数:
        product_id (int): 商品ID
        quantity (int): 数量
    """
    if product_id in products:
        product = products[product_id]
        # 检查商品是否已在购物车中
        for item in shopping_cart:
            if item['id'] == product_id:
                item['quantity'] += quantity
                print(f"已将{quantity}个{product['name']}添加到购物车")
                return
        
        # 商品不在购物车中，添加新项
        shopping_cart.append({
            'id': product_id,
            'name': product['name'],
            'price': product['price'],
            'quantity': quantity
        })
        print(f"已将{quantity}个{product['name']}添加到购物车")
    else:
        print("无效的商品ID")

def display_cart():
    """显示购物车内容"""
    if not shopping_cart:
        print("\n购物车为空")
        return
    
    print("\n购物车内容:")
    total = 0
    for i, item in enumerate(shopping_cart, 1):
        subtotal = item['price'] * item['quantity']
        total += subtotal
        print(f"{i}. {item['name']} - {item['price']}元 × {item['quantity']} = {subtotal:.2f}元")
    
    print(f"总计: {total:.2f}元")

def remove_from_cart(index):
    """
    从购物车中移除商品
    
    参数:
        index (int): 商品在购物车中的序号（从1开始）
    """
    if 1 <= index <= len(shopping_cart):
        removed_item = shopping_cart.pop(index-1)
        print(f"已从购物车中移除{removed_item['name']}")
    else:
        print("无效的序号")

# 主程序
while True:
    print("\n===菜单===")
    print("1. 查看商品列表")
    print("2. 添加商品到购物车")
    print("3. 查看购物车")
    print("4. 移除购物车中的商品")
    print("5. 退出")
    
    choice = input("请选择操作 (1-5): ")
    
    if choice == "1":
        display_products()
    elif choice == "2":
        display_products()
        try:
            product_id = int(input("请输入商品ID: "))
            quantity = int(input("请输入数量: "))
            add_to_cart(product_id, quantity)
        except ValueError:
            print("输入无效，请输入数字")
    elif choice == "3":
        display_cart()
    elif choice == "4":
        display_cart()
        if shopping_cart:
            try:
                index = int(input("请输入要移除的商品序号: "))
                remove_from_cart(index)
            except ValueError:
                print("输入无效，请输入数字")
    elif choice == "5":
        print("谢谢使用，再见!")
        break
    else:
        print("无效选择，请重新输入")
```

#### 案例2：学生成绩管理器
```python
# 学生成绩管理器
print("===学生成绩管理器===")

# 学生信息列表
students = []

def add_student(name, student_id):
    """
    添加学生
    
    参数:
        name (str): 学生姓名
        student_id (str): 学生学号
    """
    # 检查学号是否已存在
    for student in students:
        if student['id'] == student_id:
            print(f"学号 {student_id} 已存在")
            return
    
    # 添加新学生
    students.append({
        'name': name,
        'id': student_id,
        'scores': []  # 成绩列表
    })
    print(f"已添加学生: {name} ({student_id})")

def add_score(student_id, subject, score):
    """
    添加成绩
    
    参数:
        student_id (str): 学生学号
        subject (str): 科目
        score (float): 分数
    """
    for student in students:
        if student['id'] == student_id:
            # 添加成绩
            student['scores'].append({
                'subject': subject,
                'score': score
            })
            print(f"已为 {student['name']} 添加 {subject} 成绩: {score}")
            return
    print(f"未找到学号为 {student_id} 的学生")

def display_student_info(student_id):
    """
    显示学生信息
    
    参数:
        student_id (str): 学生学号
    """
    for student in students:
        if student['id'] == student_id:
            print(f"\n学生信息:")
            print(f"姓名: {student['name']}")
            print(f"学号: {student['id']}")
            
            if student['scores']:
                print("成绩列表:")
                total = 0
                for score_info in student['scores']:
                    print(f"  {score_info['subject']}: {score_info['score']}")
                    total += score_info['score']
                average = total / len(student['scores'])
                print(f"平均分: {average:.2f}")
            else:
                print("暂无成绩记录")
            return
    print(f"未找到学号为 {student_id} 的学生")

def get_top_students(subject, count=3):
    """
    获取某科目前几名学生
    
    参数:
        subject (str): 科目
        count (int): 前几名数量
    """
    # 收集指定科目的成绩
    subject_scores = []
    for student in students:
        for score_info in student['scores']:
            if score_info['subject'] == subject:
                subject_scores.append({
                    'name': student['name'],
                    'id': student['id'],
                    'score': score_info['score']
                })
    
    # 按成绩排序
    subject_scores.sort(key=lambda x: x['score'], reverse=True)
    
    # 显示前几名
    print(f"\n{subject} 科目前 {min(count, len(subject_scores))} 名:")
    for i, score_info in enumerate(subject_scores[:count], 1):
        print(f"{i}. {score_info['name']} ({score_info['id']}): {score_info['score']}")

# 示例数据
add_student("张三", "2023001")
add_student("李四", "2023002")
add_student("王五", "2023003")

add_score("2023001", "数学", 95)
add_score("2023001", "英语", 87)
add_score("2023001", "物理", 92)

add_score("2023002", "数学", 88)
add_score("2023002", "英语", 92)
add_score("2023002", "物理", 85)

add_score("2023003", "数学", 90)
add_score("2023003", "英语", 88)
add_score("2023003", "物理", 94)

# 显示学生信息
display_student_info("2023001")
display_student_info("2023002")

# 显示数学成绩排名
get_top_students("数学", 3)

# 列表操作示例
print(f"\n===列表操作示例===")
print(f"当前学生总数: {len(students)}")

# 添加新学生
add_student("赵六", "2023004")

# 使用列表推导式获取所有学生姓名
names = [student['name'] for student in students]
print(f"所有学生姓名: {names}")

# 使用filter获取有成绩记录的学生
students_with_scores = list(filter(lambda s: len(s['scores']) > 0, students))
print(f"有成绩记录的学生数: {len(students_with_scores)}")

# 使用map计算每个学生的平均分
def calculate_average(student):
    if student['scores']:
        total = sum(score_info['score'] for score_info in student['scores'])
        return total / len(student['scores'])
    return 0

averages = list(map(calculate_average, students))
print(f"学生平均分列表: {[round(avg, 2) for avg in averages]}")
```

### 代码说明

**案例1代码解释**：
1. `shopping_cart = []`：创建空列表作为购物车
2. `shopping_cart.append({...})`：向列表末尾添加新元素
3. `shopping_cart.pop(index-1)`：移除并返回指定索引的元素
4. `for item in shopping_cart:`：遍历列表中的每个元素

如果把 `shopping_cart.pop(index-1)` 写成 `shopping_cart.remove(index-1)`，会出错，因为remove()方法是根据值删除元素，而不是根据索引。

**案例2代码解释**：
1. `students = []`：创建存储学生信息的列表
2. `student['scores'].append({...})`：向嵌套列表中添加成绩
3. `students.sort(key=lambda x: x['score'], reverse=True)`：使用自定义键函数排序
4. `[student['name'] for student in students]`：使用列表推导式提取姓名

如果把 `students_with_scores = list(filter(lambda s: len(s['scores']) > 0, students))` 中的 `> 0` 写成 `> 1`，那么只有成绩记录超过1条的学生才会被筛选出来。

## 5. 元组类型 (Tuple Type)

### 知识点解析

**概念定义**：元组就像一个固定顺序的盒子队列，一旦放好就不能再改变顺序或内容。在Python中，元组是一种有序但不可变的集合，用圆括号()定义，可以存储任意类型的元素。

**核心规则**：
1. 元组用圆括号()定义，元素之间用逗号分隔
2. 元组是不可变的，创建后不能修改、添加或删除元素
3. 元组支持索引和切片操作
4. 元组可以作为字典的键使用

**常见易错点**：
1. 混淆元组和列表的使用场景，该用列表时用了元组
2. 试图修改元组元素导致TypeError
3. 定义单元素元组时忘记逗号，如(5)而不是(5,)

### 实战案例

#### 案例1：地理位置和坐标系统
```python
# 地理位置和坐标系统
print("===地理位置和坐标系统===")

# 城市坐标 (纬度, 经度)
cities_coordinates = {
    "北京": (39.9042, 116.4074),
    "上海": (31.2304, 121.4737),
    "广州": (23.1291, 113.2644),
    "深圳": (22.5431, 114.0579),
    "杭州": (30.2741, 120.1551)
}

def calculate_distance(coord1, coord2):
    """
    简化版距离计算（实际应用中应使用更精确的公式）
    
    参数:
        coord1 (tuple): 坐标1 (纬度, 经度)
        coord2 (tuple): 坐标2 (纬度, 经度)
        
    返回:
        float: 距离（简化计算）
    """
    lat_diff = coord1[0] - coord2[0]
    lon_diff = coord1[1] - coord2[1]
    # 简化的距离计算（仅作演示）
    distance = (lat_diff**2 + lon_diff**2)**0.5
    return distance * 100  # 放大倍数便于观察

def find_nearest_city(target_city):
    """
    查找最近的城市
    
    参数:
        target_city (str): 目标城市名
        
    返回:
        tuple: (最近城市名, 距离)
    """
    if target_city not in cities_coordinates:
        return None, None
    
    target_coord = cities_coordinates[target_city]
    nearest_city = None
    min_distance = float('inf')
    
    for city, coord in cities_coordinates.items():
        if city != target_city:
            distance = calculate_distance(target_coord, coord)
            if distance < min_distance:
                min_distance = distance
                nearest_city = city
    
    return nearest_city, min_distance

# 显示所有城市坐标
print("城市坐标信息:")
for city, coord in cities_coordinates.items():
    print(f"{city}: 纬度 {coord[0]}, 经度 {coord[1]}")

# 计算城市间距离
print(f"\n城市间距离计算:")
distance = calculate_distance(cities_coordinates["北京"], cities_coordinates["上海"])
print(f"北京到上海的简化距离: {distance:.2f}")

# 查找最近城市
nearest_city, distance = find_nearest_city("杭州")
if nearest_city:
    print(f"杭州最近的城市是: {nearest_city}, 距离: {distance:.2f}")

# 元组解包示例
print(f"\n===元组解包示例===")
beijing_coord = cities_coordinates["北京"]
lat, lon = beijing_coord  # 元组解包
print(f"北京坐标解包: 纬度={lat}, 经度={lon}")

# 多重赋值
x, y = 10, 20  # 这实际上也是元组解包
print(f"多重赋值: x={x}, y={y}")

# 函数返回多个值
def get_city_info(city):
    """
    获取城市信息
    
    参数:
        city (str): 城市名
        
    返回:
        tuple: (城市名, 纬度, 经度)
    """
    if city in cities_coordinates:
        coord = cities_coordinates[city]
        return city, coord[0], coord[1]  # 返回元组
    return None, None, None

# 接收多个返回值
city_name, latitude, longitude = get_city_info("广州")
print(f"广州信息: 城市={city_name}, 纬度={latitude}, 经度={longitude}")
```

#### 案例2：学生成绩记录系统
```python
# 学生成绩记录系统
print("===学生成绩记录系统===")

# 使用元组存储学生成绩 (姓名, 学号, 数学, 英语, 物理)
student_records = [
    ("张三", "2023001", 95, 87, 92),
    ("李四", "2023002", 88, 92, 85),
    ("王五", "2023003", 90, 88, 94),
    ("赵六", "2023004", 78, 85, 80),
    ("钱七", "2023005", 92, 90, 88)
]

def print_student_record(record):
    """
    打印学生记录
    
    参数:
        record (tuple): 学生记录元组
    """
    name, student_id, math, english, physics = record
    total = math + english + physics
    average = total / 3
    
    print(f"姓名: {name:>4} | 学号: {student_id} | "
          f"数学: {math:>3} | 英语: {english:>3} | 物理: {physics:>3} | "
          f"总分: {total:>3} | 平均分: {average:>5.2f}")

def find_top_student(subject_index):
    """
    查找单科最高分学生
    
    参数:
        subject_index (int): 科目索引 (数学=2, 英语=3, 物理=4)
        
    返回:
        tuple: 最高分学生记录
    """
    # 科目索引映射
    subject_names = {2: "数学", 3: "英语", 4: "物理"}
    
    # 按指定科目分数排序
    sorted_records = sorted(student_records, 
                          key=lambda record: record[subject_index], 
                          reverse=True)
    
    top_student = sorted_records[0]
    subject_name = subject_names[subject_index]
    top_score = top_student[subject_index]
    
    print(f"{subject_name}最高分: {top_score}分")
    print(f"获得者: {top_student[0]} ({top_student[1]})")
    
    return top_student

def calculate_class_statistics():
    """计算班级统计信息"""
    # 使用列表推导式提取各科成绩
    math_scores = [record[2] for record in student_records]
    english_scores = [record[3] for record in student_records]
    physics_scores = [record[4] for record in student_records]
    
    # 计算各科统计信息
    subjects = [
        ("数学", math_scores),
        ("英语", english_scores),
        ("物理", physics_scores)
    ]
    
    print("\n班级成绩统计:")
    print("-" * 50)
    for subject_name, scores in subjects:
        average = sum(scores) / len(scores)
        max_score = max(scores)
        min_score = min(scores)
        print(f"{subject_name}: 平均分={average:>5.2f}, "
              f"最高分={max_score:>3}, 最低分={min_score:>3}")

# 显示所有学生成绩
print("学生成绩单:")
print("=" * 70)
for record in student_records:
    print_student_record(record)

# 查找各科最高分
print(f"\n各科最高分:")
print("-" * 30)
find_top_student(2)  # 数学
find_top_student(3)  # 英语
find_top_student(4)  # 物理

# 班级统计
calculate_class_statistics()

# 元组不可变性演示
print(f"\n===元组不可变性演示===")
sample_record = student_records[0]
print(f"原始记录: {sample_record}")

# 尝试修改元组（会导致错误）
try:
    sample_record[2] = 100  # 尝试修改数学成绩
except TypeError as e:
    print(f"错误: {e}")
    print("说明: 元组是不可变的，不能直接修改其元素")

# 正确的做法：创建新元组
name, student_id, math, english, physics = sample_record
updated_record = (name, student_id, 100, english, physics)  # 修改数学成绩为100
print(f"更新后的记录: {updated_record}")

# 元组作为字典键的示例
print(f"\n===元组作为字典键===")
# 使用(学号, 科目)作为键存储详细成绩信息
detailed_scores = {
    ("2023001", "数学"): {"score": 95, "class_rank": 2, "grade_rank": 1},
    ("2023001", "英语"): {"score": 87, "class_rank": 4, "grade_rank": 3},
    ("2023001", "物理"): {"score": 92, "class_rank": 3, "grade_rank": 2}
}

# 查询特定学生成绩
student_id = "2023001"
subject = "数学"
if (student_id, subject) in detailed_scores:
    score_info = detailed_scores[(student_id, subject)]
    print(f"学生 {student_id} 的 {subject} 成绩:")
    print(f"  分数: {score_info['score']}")
    print(f"  班级排名: {score_info['class_rank']}")
    print(f"  年级排名: {score_info['grade_rank']}")
```

### 代码说明

**案例1代码解释**：
1. `cities_coordinates = {"北京": (39.9042, 116.4074), ...}`：使用元组存储坐标
2. `lat, lon = beijing_coord`：元组解包，将元组中的值分别赋给变量
3. `return city, coord[0], coord[1]`：函数返回元组
4. `x, y = 10, 20`：多重赋值实际上也是元组解包

如果把 `cities_coordinates["北京"]` 定义为列表 `[39.9042, 116.4074]` 而不是元组，程序仍能正常工作，但使用元组更合适，因为坐标是固定不变的。

**案例2代码解释**：
1. `student_records = [("张三", "2023001", 95, 87, 92), ...]`：使用元组列表存储学生记录
2. `name, student_id, math, english, physics = record`：解包元组获取各项信息
3. `sorted(student_records, key=lambda record: record[subject_index], reverse=True)`：使用元组元素作为排序键
4. `("2023001", "数学")`：使用元组作为字典的键

如果试图修改元组中的值，如 `record[2] = 100`，会抛出TypeError异常，因为元组是不可变的。

## 6. 字典类型 (Dictionary Type)

### 知识点解析

**概念定义**：字典就像现实生活中的字典一样，通过"单词"（键）可以查到对应的"解释"（值）。在Python中，字典是一种可变的映射类型，存储键值对，通过键可以快速找到对应的值。

**核心规则**：
1. 字典用花括号{}定义，键值对之间用逗号分隔，键和值之间用冒号分隔
2. 字典是可变的，可以添加、修改、删除键值对
3. 键必须是不可变类型（如字符串、数字、元组），且不能重复
4. 值可以是任意类型，且可以重复

**常见易错点**：
1. 试图使用可变类型（如列表）作为字典的键
2. 访问不存在的键导致KeyError
3. 混淆字典的键和值
4. 使用中括号[]访问不存在的键时没有处理异常

### 实战案例

#### 案例1：学生信息管理系统
```python
# 学生信息管理系统
print("===学生信息管理系统===")

# 学生信息字典，键为学号，值为包含学生信息的字典
students = {
    "2023001": {
        "name": "张三",
        "age": 18,
        "major": "计算机科学",
        "courses": ["Python编程", "数据结构", "算法设计"],
        "grades": {"Python编程": 95, "数据结构": 87, "算法设计": 92}
    },
    "2023002": {
        "name": "李四",
        "age": 19,
        "major": "电子信息",
        "courses": ["电路分析", "信号与系统", "数字电路"],
        "grades": {"电路分析": 88, "信号与系统": 92, "数字电路": 85}
    },
    "2023003": {
        "name": "王五",
        "age": 18,
        "major": "机械工程",
        "courses": ["机械制图", "材料力学", "热力学"],
        "grades": {"机械制图": 90, "材料力学": 88, "热力学": 94}
    }
}

def add_student(student_id, name, age, major):
    """
    添加学生
    
    参数:
        student_id (str): 学号
        name (str): 姓名
        age (int): 年龄
        major (str): 专业
    """
    if student_id in students:
        print(f"学号 {student_id} 已存在")
        return
    
    students[student_id] = {
        "name": name,
        "age": age,
        "major": major,
        "courses": [],
        "grades": {}
    }
    print(f"已添加学生: {name} ({student_id})")

def add_course(student_id, course_name):
    """
    为学生添加课程
    
    参数:
        student_id (str): 学号
        course_name (str): 课程名
    """
    if student_id not in students:
        print(f"未找到学号为 {student_id} 的学生")
        return
    
    student = students[student_id]
    if course_name not in student["courses"]:
        student["courses"].append(course_name)
        print(f"已为 {student['name']} 添加课程: {course_name}")
    else:
        print(f"{student['name']} 已选修课程: {course_name}")

def add_grade(student_id, course_name, grade):
    """
    为学生添加成绩
    
    参数:
        student_id (str): 学号
        course_name (str): 课程名
        grade (float): 成绩
    """
    if student_id not in students:
        print(f"未找到学号为 {student_id} 的学生")
        return
    
    student = students[student_id]
    if course_name not in student["courses"]:
        print(f"{student['name']} 未选修课程: {course_name}")
        return
    
    student["grades"][course_name] = grade
    print(f"已为 {student['name']} 的 {course_name} 添加成绩: {grade}")

def display_student_info(student_id):
    """
    显示学生信息
    
    参数:
        student_id (str): 学号
    """
    if student_id not in students:
        print(f"未找到学号为 {student_id} 的学生")
        return
    
    student = students[student_id]
    print(f"\n===学生信息===")
    print(f"姓名: {student['name']}")
    print(f"学号: {student_id}")
    print(f"年龄: {student['age']}")
    print(f"专业: {student['major']}")
    
    print(f"选修课程: {', '.join(student['courses'])}")
    
    if student["grades"]:
        print("成绩信息:")
        total = 0
        count = 0
        for course, grade in student["grades"].items():
            print(f"  {course}: {grade}")
            total += grade
            count += 1
        average = total / count if count > 0 else 0
        print(f"平均成绩: {average:.2f}")
    else:
        print("暂无成绩记录")

def search_students_by_major(major):
    """
    根据专业查找学生
    
    参数:
        major (str): 专业名称
    """
    found_students = []
    for student_id, student_info in students.items():
        if student_info["major"] == major:
            found_students.append((student_id, student_info))
    
    if found_students:
        print(f"\n{major} 专业学生列表:")
        for student_id, student_info in found_students:
            print(f"  {student_info['name']} ({student_id})")
    else:
        print(f"未找到 {major} 专业的学生")

# 演示系统功能
print("当前学生信息:")
for student_id in students:
    display_student_info(student_id)

# 添加新学生
add_student("2023004", "赵六", 19, "计算机科学")

# 为学生添加课程和成绩
add_course("2023004", "Python编程")
add_grade("2023004", "Python编程", 88)

# 显示更新后的信息
display_student_info("2023004")

# 按专业查找学生
search_students_by_major("计算机科学")

# 字典操作示例
print(f"\n===字典操作示例===")
print(f"学生总数: {len(students)}")

# 遍历字典的几种方式
print("遍历字典 - 方法1 (键):")
for student_id in students:
    print(f"  学号: {student_id}, 姓名: {students[student_id]['name']}")

print("遍历字典 - 方法2 (键值对):")
for student_id, student_info in students.items():
    print(f"  学号: {student_id}, 姓名: {student_info['name']}")

# 使用get方法安全访问
student = students.get("2023005", {"name": "未找到"})
print(f"查找不存在的学生: {student['name']}")

# 字典推导式示例
# 创建一个只包含姓名和专业的字典
student_names_majors = {sid: {"name": info["name"], "major": info["major"]} 
                       for sid, info in students.items()}
print(f"学生姓名专业字典: {student_names_majors}")
```

#### 案例2：商品库存管理系统
```python
# 商品库存管理系统
print("===商品库存管理系统===")

# 商品库存信息
# 键为商品编码，值为包含商品信息的字典
inventory = {
    "P001": {
        "name": "苹果",
        "category": "水果",
        "price": 5.5,
        "stock": 100,
        "supplier": "果园供应商"
    },
    "P002": {
        "name": "香蕉",
        "category": "水果",
        "price": 3.0,
        "stock": 150,
        "supplier": "热带水果供应商"
    },
    "P003": {
        "name": "牛奶",
        "category": "乳制品",
        "price": 12.0,
        "stock": 50,
        "supplier": "乳业公司"
    },
    "P004": {
        "name": "面包",
        "category": "烘焙食品",
        "price": 8.5,
        "stock": 80,
        "supplier": "面包房"
    }
}

def display_inventory():
    """显示库存信息"""
    print("\n===商品库存信息===")
    print(f"{'编码':<6} {'商品名':<8} {'类别':<8} {'价格':<6} {'库存':<6} {'供应商':<12}")
    print("-" * 55)
    for code, product in inventory.items():
        print(f"{code:<6} {product['name']:<8} {product['category']:<8} "
              f"{product['price']:<6} {product['stock']:<6} {product['supplier']:<12}")

def add_product(code, name, category, price, stock, supplier):
    """
    添加商品
    
    参数:
        code (str): 商品编码
        name (str): 商品名
        category (str): 类别
        price (float): 价格
        stock (int): 库存
        supplier (str): 供应商
    """
    if code in inventory:
        print(f"商品编码 {code} 已存在")
        return False
    
    inventory[code] = {
        "name": name,
        "category": category,
        "price": price,
        "stock": stock,
        "supplier": supplier
    }
    print(f"已添加商品: {name} ({code})")
    return True

def update_stock(code, quantity):
    """
    更新库存
    
    参数:
        code (str): 商品编码
        quantity (int): 数量变化（正数为进货，负数为销售）
    """
    if code not in inventory:
        print(f"商品编码 {code} 不存在")
        return False
    
    product = inventory[code]
    new_stock = product["stock"] + quantity
    
    if new_stock < 0:
        print(f"库存不足，当前库存: {product['stock']}, 需要: {abs(quantity)}")
        return False
    
    product["stock"] = new_stock
    action = "进货" if quantity > 0 else "销售"
    print(f"已{action} {product['name']} {abs(quantity)} 件，当前库存: {new_stock}")
    return True

def search_by_category(category):
    """
    根据类别搜索商品
    
    参数:
        category (str): 商品类别
    """
    found_products = {code: product for code, product in inventory.items() 
                     if product["category"] == category}
    
    if found_products:
        print(f"\n{category} 类别商品:")
        for code, product in found_products.items():
            print(f"  {product['name']} ({code}): 价格 {product['price']}元, "
                  f"库存 {product['stock']} 件")
    else:
        print(f"未找到 {category} 类别的商品")

def get_low_stock_products(threshold=20):
    """
    获取低库存商品
    
    参数:
        threshold (int): 库存阈值
    """
    low_stock_products = {code: product for code, product in inventory.items() 
                         if product["stock"] < threshold}
    
    if low_stock_products:
        print(f"\n低库存商品 (库存 < {threshold}):")
        for code, product in low_stock_products.items():
            print(f"  {product['name']} ({code}): 库存 {product['stock']} 件")
    else:
        print(f"没有库存低于 {threshold} 的商品")

def calculate_inventory_value():
    """计算库存总价值"""
    total_value = 0
    print("\n===库存价值统计===")
    for code, product in inventory.items():
        value = product["price"] * product["stock"]
        total_value += value
        print(f"{product['name']}: {product['price']}元 × {product['stock']}件 = {value:.2f}元")
    
    print(f"库存总价值: {total_value:.2f}元")
    return total_value

# 演示系统功能
display_inventory()

# 添加新商品
add_product("P005", "橙子", "水果", 4.2, 120, "柑橘供应商")

# 更新库存（销售）
update_stock("P001", -10)  # 销售10个苹果
update_stock("P003", -5)   # 销售5盒牛奶

# 更新库存（进货）
update_stock("P002", 50)   # 进货50根香蕉

# 按类别搜索
search_by_category("水果")

# 查找低库存商品
get_low_stock_products(60)

# 计算库存总价值
calculate_inventory_value()

# 字典方法示例
print(f"\n===字典方法示例===")
# 获取所有键
product_codes = list(inventory.keys())
print(f"所有商品编码: {product_codes}")

# 获取所有值
product_names = [product["name"] for product in inventory.values()]
print(f"所有商品名: {product_names}")

# 更新字典
new_products = {
    "P006": {
        "name": "鸡蛋",
        "category": "农副产品",
        "price": 15.0,
        "stock": 200,
        "supplier": "农场"
    }
}

# 使用update方法添加新产品
inventory.update(new_products)
print(f"使用update方法添加了 {len(new_products)} 个新商品")

# 使用pop方法移除商品
removed_product = inventory.pop("P006", None)
if removed_product:
    print(f"已移除商品: {removed_product['name']}")
else:
    print("未找到要移除的商品")

# 使用setdefault方法
inventory.setdefault("P007", {
    "name": "矿泉水",
    "category": "饮品",
    "price": 2.0,
    "stock": 300,
    "supplier": "水厂"
})
print(f"使用setdefault方法添加了商品: {inventory['P007']['name']}")
```

### 代码说明

**案例1代码解释**：
1. `students = {"2023001": {...}, ...}`：创建嵌套字典存储学生信息
2. `students[student_id] = {...}`：向字典添加新的键值对
3. `student["courses"].append(course_name)`：访问嵌套列表并添加元素
4. `for student_id, student_info in students.items():`：遍历字典的键值对

如果把学号用作字典的值而不是键，如 `{"name": "张三", "id": "2023001"}`，那么查找学生时就需要遍历整个列表，效率会很低。

**案例2代码解释**：
1. `inventory = {"P001": {...}, ...}`：使用商品编码作为键的字典
2. `inventory.get("P005", {"name": "未找到"})`：安全地访问可能不存在的键
3. `inventory.update(new_products)`：使用update方法批量添加键值对
4. `{code: product for code, product in inventory.items() if product["stock"] < threshold}`：字典推导式

如果试图用列表作为字典的键，如 `inventory[["P", "0", "0", "1"]] = {...}`，会抛出TypeError，因为列表是可变类型，不能作为字典的键。

## 7. 集合类型 (Set Type)

### 知识点解析

**概念定义**：集合就像一个装不重复物品的袋子，袋子里的物品没有顺序，而且每个物品只能有一份。在Python中，集合是一种无序且不重复的元素集合，用花括号{}或set()函数创建。

**核心规则**：
1. 集合用花括号{}或set()函数创建
2. 集合中的元素不能重复
3. 集合是可变的，可以添加或删除元素
4. 集合支持数学上的集合运算，如并集、交集、差集等

**常见易错点**：
1. 试图创建空集合时使用{}而不是set()，因为{}创建的是空字典
2. 试图将可变类型（如列表）添加到集合中
3. 试图通过索引访问集合元素，因为集合是无序的
4. 忘记集合会自动去除重复元素

### 实战案例

#### 案例1：用户标签和兴趣系统
```python
# 用户标签和兴趣系统
print("===用户标签和兴趣系统===")

# 用户兴趣标签系统
user_interests = {
    "张三": {"编程", "游戏", "音乐", "电影"},
    "李四": {"阅读", "旅行", "摄影", "编程"},
    "王五": {"游戏", "篮球", "音乐", "美食"},
    "赵六": {"编程", "阅读", "电影", "旅行"},
    "钱七": {"音乐", "美食", "摄影", "篮球"}
}

def add_user_interest(username, interest):
    """
    为用户添加兴趣标签
    
    参数:
        username (str): 用户名
        interest (str): 兴趣标签
    """
    if username not in user_interests:
        user_interests[username] = set()
    
    user_interests[username].add(interest)
    print(f"已为 {username} 添加兴趣标签: {interest}")

def remove_user_interest(username, interest):
    """
    为用户移除兴趣标签
    
    参数:
        username (str): 用户名
        interest (str): 兴趣标签
    """
    if username in user_interests and interest in user_interests[username]:
        user_interests[username].remove(interest)
        print(f"已为 {username} 移除兴趣标签: {interest}")
    else:
        print(f"用户 {username} 没有 {interest} 兴趣标签")

def find_common_interests(user1, user2):
    """
    查找两个用户的共同兴趣
    
    参数:
        user1 (str): 用户1
        user2 (str): 用户2
        
    返回:
        set: 共同兴趣集合
    """
    if user1 not in user_interests or user2 not in user_interests:
        print("用户不存在")
        return set()
    
    common = user_interests[user1] & user_interests[user2]  # 交集运算
    return common

def find_all_interests():
    """
    查找所有用户的兴趣
    
    返回:
        set: 所有不重复的兴趣集合
    """
    all_interests = set()
    for interests in user_interests.values():
        all_interests.update(interests)
    return all_interests

def recommend_friends(username, threshold=2):
    """
    为用户推荐朋友（基于共同兴趣）
    
    参数:
        username (str): 用户名
        threshold (int): 成为朋友的最小共同兴趣数
    """
    if username not in user_interests:
        print(f"用户 {username} 不存在")
        return
    
    user_interest_set = user_interests[username]
    recommendations = []
    
    for other_user, interests in user_interests.items():
        if other_user != username:
            common_interests = user_interest_set & interests
            if len(common_interests) >= threshold:
                recommendations.append((other_user, common_interests))
    
    if recommendations:
        print(f"\n为 {username} 推荐的朋友:")
        for friend, common_interests in recommendations:
            print(f"  {friend}: 共同兴趣 {', '.join(common_interests)}")
    else:
        print(f"没有为 {username} 找到合适的推荐朋友")

# 演示系统功能
print("用户兴趣标签:")
for username, interests in user_interests.items():
    print(f"{username}: {', '.join(interests)}")

# 为用户添加兴趣
add_user_interest("张三", "摄影")
add_user_interest("新用户", "编程")

# 查找共同兴趣
common = find_common_interests("张三", "李四")
print(f"\n张三和李四的共同兴趣: {', '.join(common)}")

# 查找所有兴趣
all_interests = find_all_interests()
print(f"\n所有用户的兴趣: {', '.join(all_interests)}")

# 推荐朋友
recommend_friends("张三", 2)

# 集合运算示例
print(f"\n===集合运算示例===")
zhang_interests = user_interests["张三"]
li_interests = user_interests["李四"]
wang_interests = user_interests["王五"]

# 并集 - 所有不重复的兴趣
union_interests = zhang_interests | li_interests | wang_interests
print(f"张三、李四、王五的所有兴趣: {', '.join(union_interests)}")

# 交集 - 三人都有的兴趣
intersection_interests = zhang_interests & li_interests & wang_interests
print(f"三人都有的兴趣: {', '.join(intersection_interests) if intersection_interests else '无'}")

# 差集 - 张三有但李四没有的兴趣
difference_interests = zhang_interests - li_interests
print(f"张三有但李四没有的兴趣: {', '.join(difference_interests)}")

# 对称差集 - 两人中只有一人有的兴趣
symmetric_difference = zhang_interests ^ li_interests
print(f"张三和李四中只有一人有的兴趣: {', '.join(symmetric_difference)}")
```

#### 案例2：问卷调查数据分析
```python
# 问卷调查数据分析
print("===问卷调查数据分析===")

# 模拟问卷调查数据
# 每个集合代表选择该选项的用户ID
survey_results = {
    "Q1": {  # 问题1: 您最常使用的编程语言是?
        "Python": {1, 2, 3, 5, 7, 8, 10, 12, 15, 18, 20},
        "Java": {2, 4, 6, 8, 9, 11, 13, 15, 17, 19},
        "JavaScript": {1, 3, 5, 6, 9, 10, 14, 16, 18, 20},
        "C++": {4, 7, 11, 12, 13, 17, 19}
    },
    "Q2": {  # 问题2: 您最感兴趣的技术领域是?
        "人工智能": {1, 3, 5, 8, 10, 12, 15, 18},
        "Web开发": {2, 4, 6, 9, 11, 14, 16, 19, 20},
        "移动开发": {1, 7, 8, 13, 15, 17},
        "数据科学": {2, 3, 5, 10, 12, 18, 20}
    }
}

def analyze_survey_question(question_id):
    """
    分析单个问题的调查结果
    
    参数:
        question_id (str): 问题ID
    """
    if question_id not in survey_results:
        print(f"问题 {question_id} 不存在")
        return
    
    print(f"\n===问题 {question_id} 分析===")
    options = survey_results[question_id]
    total_respondents = len(set().union(*options.values()))  # 总参与人数
    
    print(f"总参与人数: {total_respondents}")
    
    # 计算每个选项的选择人数和比例
    option_stats = []
    for option, users in options.items():
        count = len(users)
        percentage = count / total_respondents * 100
        option_stats.append((option, count, percentage))
    
    # 按选择人数排序
    option_stats.sort(key=lambda x: x[1], reverse=True)
    
    print("选项统计:")
    for option, count, percentage in option_stats:
        print(f"  {option}: {count}人 ({percentage:.1f}%)")

def find_correlations():
    """查找不同问题之间的相关性"""
    print(f"\n===选项相关性分析===")
    
    q1_options = survey_results["Q1"]
    q2_options = survey_results["Q2"]
    
    # 分析编程语言和兴趣领域的关系
    for lang, lang_users in q1_options.items():
        print(f"\n{lang} 用户的兴趣分布:")
        for field, field_users in q2_options.items():
            common_users = lang_users & field_users  # 交集
            if common_users:
                percentage = len(common_users) / len(lang_users) * 100
                print(f"  {field}: {len(common_users)}人 ({percentage:.1f}%)")

def get_user_segments():
    """获取用户细分群体"""
    print(f"\n===用户细分分析===")
    
    # 获取所有用户ID
    all_users = set()
    for options in survey_results.values():
        for users in options.values():
            all_users.update(users)
    
    print(f"总用户数: {len(all_users)}")
    
    # 分析用户群体
    python_users = survey_results["Q1"]["Python"]
    ai_interest_users = survey_results["Q2"]["人工智能"]
    web_dev_users = survey_results["Q2"]["Web开发"]
    
    # Python且对AI感兴趣的用户
    python_ai_users = python_users & ai_interest_users
    print(f"Python且对AI感兴趣的用户: {len(python_ai_users)}人")
    
    # JavaScript且对Web开发感兴趣的用户
    js_users = survey_results["Q1"]["JavaScript"]
    js_web_users = js_users & web_dev_users
    print(f"JavaScript且对Web开发感兴趣的用户: {len(js_web_users)}人")
    
    # 只对AI感兴趣的用户（不包括同时对其他领域感兴趣的）
    only_ai_users = ai_interest_users - web_dev_users
    print(f"只对AI感兴趣的用户: {len(only_ai_users)}人")

# 执行分析
analyze_survey_question("Q1")
analyze_survey_question("Q2")
find_correlations()
get_user_segments()

# 集合操作示例
print(f"\n===集合操作示例===")
# 创建集合的不同方法
set1 = {1, 2, 3, 4, 5}
set2 = set([3, 4, 5, 6, 7])
set3 = set("hello")  # 从字符串创建集合

print(f"set1: {set1}")
print(f"set2: {set2}")
print(f"set3: {set3} (从字符串'hello'创建，自动去重)")

# 空集合的正确创建方法
empty_set = set()  # 正确方法
# empty_dict = {}  # 这是创建空字典，不是空集合
print(f"空集合: {empty_set}")

# 集合的增删操作
sample_set = {1, 2, 3}
print(f"原始集合: {sample_set}")

sample_set.add(4)  # 添加元素
print(f"添加4后: {sample_set}")

sample_set.update([5, 6])  # 添加多个元素
print(f"添加5,6后: {sample_set}")

sample_set.discard(3)  # 删除元素（不存在不报错）
print(f"删除3后: {sample_set}")

sample_set.remove(1)  # 删除元素（不存在会报错）
print(f"删除1后: {sample_set}")

# 集合的成员测试
print(f"2是否在集合中: {2 in sample_set}")
print(f"10是否在集合中: {10 in sample_set}")

# 集合推导式
squares = {x**2 for x in range(1, 6)}
print(f"1到5的平方集合: {squares}")

# 使用集合去重
duplicate_list = [1, 2, 2, 3, 3, 3, 4, 4, 4, 4]
unique_list = list(set(duplicate_list))
print(f"原列表: {duplicate_list}")
print(f"去重后: {unique_list}")
```

### 代码说明

**案例1代码解释**：
1. `user_interests = {"张三": {"编程", "游戏", "音乐", "电影"}, ...}`：使用集合存储用户的兴趣标签
2. `user_interests[username].add(interest)`：向集合中添加元素
3. `user_interests[user1] & user_interests[user2]`：使用&运算符计算交集
4. `user_interests[username].remove(interest)`：从集合中移除元素

如果使用列表而不是集合存储兴趣标签，如 `{"张三": ["编程", "游戏", "编程"]}`，会出现重复元素，且查找效率较低。

**案例2代码解释**：
1. `survey_results = {"Q1": {"Python": {1, 2, 3, ...}, ...}, ...}`：使用嵌套集合存储调查数据
2. `len(set().union(*options.values()))`：计算总参与人数，使用union合并所有集合
3. `lang_users & field_users`：找出同时选择两个选项的用户
4. `{x**2 for x in range(1, 6)}`：使用集合推导式创建集合

如果试图将列表添加到集合中，如 `sample_set.add([1, 2, 3])`，会抛出TypeError，因为列表是可变类型，不能作为集合元素。