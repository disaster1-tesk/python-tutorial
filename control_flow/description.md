# Python控制流知识点

## 1. 条件语句 (if-elif-else)

### 知识点解析

**概念定义**：条件语句就像我们在生活中做决定一样，根据不同的情况选择不同的行动方案。比如"如果下雨，我就带伞；否则我就穿凉鞋"。在Python中，我们使用if语句来实现这种逻辑判断。

**核心规则**：
1. if语句后面必须跟一个冒号(:)
2. if语句下面的代码块必须缩进（通常为4个空格）
3. 可以使用elif（else if的缩写）来检查多个条件
4. else语句是可选的，用于处理所有未被前面条件匹配的情况

**常见易错点**：
1. 忘记在if语句后加冒号
2. 缩进不一致导致语法错误
3. 混淆赋值运算符(=)和比较运算符(==)
4. 条件表达式中使用了错误的逻辑运算符

### 实战案例

#### 案例1：学生成绩评定系统
```python
# 学生成绩评定系统
print("===学生成绩评定系统===")

# 获取学生分数
score_str = input("请输入学生的分数 (0-100): ")

# 验证输入并转换为数字
try:
    score = float(score_str)
    
    # 检查分数范围
    if score < 0 or score > 100:
        print("错误: 分数应该在0-100之间")
    else:
        # 根据分数判断等级
        if score >= 90:
            grade = "A (优秀)"
        elif score >= 80:
            grade = "B (良好)"
        elif score >= 70:
            grade = "C (中等)"
        elif score >= 60:
            grade = "D (及格)"
        else:
            grade = "F (不及格)"
        
        # 输出结果
        print(f"分数: {score}")
        print(f"等级: {grade}")
        
except ValueError:
    print("错误: 请输入有效的数字")
```

#### 案例2：简单用户登录系统
```python
# 简单用户登录系统
print("===用户登录系统===")

# 预设的用户名和密码
valid_username = "admin"
valid_password = "123456"

# 获取用户输入
username = input("请输入用户名: ")
password = input("请输入密码: ")

# 验证用户信息
if username == valid_username:
    # 用户名正确，检查密码
    if password == valid_password:
        print("登录成功! 欢迎进入系统")
        print("您可以访问所有功能")
    else:
        print("密码错误，请重新输入")
else:
    # 用户名错误
    if username == "":
        print("用户名不能为空")
    else:
        print("用户名不存在")

# 演示嵌套条件的另一种写法
print("\n使用逻辑运算符的写法:")
if username == valid_username and password == valid_password:
    print("登录成功! 欢迎进入系统")
elif username != valid_username:
    print("用户名不存在")
else:
    print("密码错误，请重新输入")
```

### 代码说明

**案例1代码解释**：
1. `if score < 0 or score > 100:`：检查分数是否在有效范围内，使用or运算符表示"或者"
2. `elif score >= 80:`：elif是"else if"的缩写，用于检查另一个条件
3. `else:`：处理所有未被前面条件匹配的情况，这里对应分数低于60分
4. 每个条件后面都有冒号，下面的代码都进行了缩进

如果把 `elif score >= 80:` 写成 `if score >= 80:`，那么当输入95分时，程序会先打印"A (优秀)"，然后又检查到满足`score >= 80`的条件，又会打印"B (良好)"，这显然不是我们想要的结果。

**案例2代码解释**：
1. `if username == valid_username:`：使用双等号(==)比较两个值是否相等
2. `if password == valid_password:`：嵌套的if语句，只有当用户名正确时才会检查密码
3. `if username == valid_username and password == valid_password:`：使用and运算符同时检查两个条件
4. 注意区分赋值(=)和比较(==)，如果写成`if username = valid_username`会报语法错误

如果把 `username == valid_username` 写成 `username = valid_username`，这会变成赋值操作而不是比较操作，不仅逻辑错误，还会修改username变量的值。

## 2. 循环语句 (for 和 while)

### 知识点解析

**概念定义**：循环语句就像我们日常生活中的重复动作一样，比如"每天跑步5圈"或者"把所有苹果洗一遍"。在Python中，我们使用for循环和while循环来重复执行某些操作。

**核心规则**：
1. for循环用于遍历序列（如列表、字符串等）
2. while循环在条件为真时重复执行
3. 两种循环都可以使用break语句提前退出，continue语句跳过当前迭代
4. 循环体内的代码必须缩进

**常见易错点**：
1. while循环条件设置不当导致无限循环
2. 忘记在循环中更新循环变量，造成死循环
3. 循环缩进错误
4. 在for循环中修改正在遍历的序列

### 实战案例

#### 案例1：数字猜谜游戏
```python
# 数字猜谜游戏
print("===数字猜谜游戏===")
print("我想了一个1到100之间的数字，你能猜到吗？")

import random

# 生成1到100之间的随机数
target_number = random.randint(1, 100)
attempts = 0  # 记录尝试次数

# 使用while循环实现游戏主逻辑
while True:
    # 获取用户输入
    guess_str = input("请输入你猜的数字 (输入'quit'退出): ")
    
    # 检查是否要退出游戏
    if guess_str.lower() == 'quit':
        print(f"游戏结束! 我想的数字是 {target_number}")
        break
    
    # 验证输入
    try:
        guess = int(guess_str)
        attempts += 1  # 增加尝试次数
        
        # 比较猜测和目标数字
        if guess < target_number:
            print("太小了! 再试一次")
        elif guess > target_number:
            print("太大了! 再试一次")
        else:
            print(f"恭喜你! 你猜对了!")
            print(f"我想的数字是 {target_number}")
            print(f"你总共猜了 {attempts} 次")
            break
            
    except ValueError:
        print("请输入有效的数字!")
```

#### 案例2：学生成绩统计分析
```python
# 学生成绩统计分析
print("===学生成绩统计分析===")

# 学生成绩列表
scores = [85, 92, 78, 96, 88, 76, 89, 94, 82, 90]

# 使用for循环计算总分
total_score = 0
for score in scores:
    total_score += score  # 累加每个分数

# 计算平均分
average_score = total_score / len(scores)

# 使用for循环找出最高分和最低分
max_score = scores[0]  # 初始化为第一个分数
min_score = scores[0]  # 初始化为第一个分数

for score in scores:
    if score > max_score:
        max_score = score
    if score < min_score:
        min_score = score

# 统计各等级人数
grade_count = {"优秀": 0, "良好": 0, "中等": 0, "及格": 0, "不及格": 0}

for score in scores:
    if score >= 90:
        grade_count["优秀"] += 1
    elif score >= 80:
        grade_count["良好"] += 1
    elif score >= 70:
        grade_count["中等"] += 1
    elif score >= 60:
        grade_count["及格"] += 1
    else:
        grade_count["不及格"] += 1

# 输出统计结果
print(f"学生成绩: {scores}")
print(f"学生总数: {len(scores)}")
print(f"总分: {total_score}")
print(f"平均分: {average_score:.2f}")
print(f"最高分: {max_score}")
print(f"最低分: {min_score}")
print(f"分数范围: {max_score - min_score}")

print("\n等级分布:")
for grade, count in grade_count.items():
    percentage = count / len(scores) * 100
    print(f"  {grade}: {count}人 ({percentage:.1f}%)")

# 使用range()和for循环打印成绩排名
print("\n成绩排名:")
sorted_scores = sorted(scores, reverse=True)  # 降序排列

for i in range(len(sorted_scores)):
    rank = i + 1
    score = sorted_scores[i]
    print(f"  第{rank}名: {score}分")
```

### 代码说明

**案例1代码解释**：
1. `while True:`：创建一个无限循环，直到遇到break语句才退出
2. `attempts += 1`：每次猜测后增加尝试次数，这是防止死循环的关键
3. `if guess_str.lower() == 'quit':`：使用lower()方法将输入转换为小写进行比较
4. `break`：在猜对或用户选择退出时跳出循环

如果忘记写 `attempts += 1`，虽然不影响游戏功能，但就无法统计用户的尝试次数了。如果写成 `while attempts < 10:` 但忘记在循环中增加attempts的值，就会造成死循环。

**案例2代码解释**：
1. `for score in scores:`：遍历成绩列表中的每个元素
2. `total_score += score`：累加每个分数得到总分
3. `for i in range(len(sorted_scores)):`：使用range()生成索引序列
4. `sorted(scores, reverse=True)`：对成绩进行降序排列

如果在遍历列表时修改列表本身，如在`for score in scores:`循环中执行`scores.append(100)`，可能会导致意外的结果或无限循环。

## 3. 循环控制语句 (break 和 continue)

### 知识点解析

**概念定义**：循环控制语句就像是给重复动作设置特殊规则一样。break就像"停止"按钮，一旦按下就立即停止所有重复；continue就像"跳过"按钮，跳过当前这一次，继续下一次重复。

**核心规则**：
1. break语句用于立即退出循环
2. continue语句用于跳过当前迭代，继续下一次循环
3. 这两个语句可以在for循环和while循环中使用
4. 在嵌套循环中，它们只影响最内层的循环

**常见易错点**：
1. 在错误的位置使用break或continue，导致逻辑错误
2. 忘记在使用continue时更新循环变量，可能造成无限循环
3. 在嵌套循环中误以为break会退出所有循环

### 实战案例

#### 案例1：密码验证系统
```python
# 密码验证系统
print("===密码验证系统===")

# 预设的正确密码
correct_password = "python123"
max_attempts = 3  # 最大尝试次数

# 使用for循环限制尝试次数
for attempt in range(1, max_attempts + 1):
    password = input(f"请输入密码 (尝试 {attempt}/{max_attempts}): ")
    
    # 检查密码是否正确
    if password == correct_password:
        print("密码正确! 欢迎进入系统")
        break  # 密码正确，退出循环
    else:
        if attempt < max_attempts:
            print("密码错误，请重试")
            retry = input("是否继续尝试? (y/n): ")
            if retry.lower() != 'y':
                print("用户取消操作")
                break  # 用户选择不继续，退出循环
        else:
            print("密码错误次数过多，账户已被锁定")
        
        continue  # 继续下一次尝试（在for循环中这行实际上不需要）

# 演示while循环中的break和continue
print("\n===菜单系统演示===")
while True:
    print("\n请选择操作:")
    print("1. 查看信息")
    print("2. 修改设置")
    print("3. 退出程序")
    
    choice = input("请输入选项 (1-3): ")
    
    if choice == "1":
        print("正在查看信息...")
        # 模拟查看信息的操作
        continue  # 完成操作后继续显示菜单
    elif choice == "2":
        print("正在修改设置...")
        # 模拟修改设置的操作
        continue  # 完成操作后继续显示菜单
    elif choice == "3":
        confirm = input("确定要退出吗? (y/n): ")
        if confirm.lower() == 'y':
            print("程序退出")
            break  # 退出程序
        else:
            print("取消退出")
            continue  # 继续显示菜单
    else:
        print("无效选项，请重新选择")
        continue  # 无效选项，继续显示菜单
```

#### 案例2：数据过滤和处理
```python
# 数据过滤和处理
print("===数据过滤和处理===")

# 模拟用户输入的数据，包含有效和无效数据
raw_data = ["10", "20", "abc", "30", "-5", "40", "", "50", "xyz", "60"]

print("原始数据:", raw_data)

# 使用continue过滤无效数据
print("\n处理后的有效数据:")
valid_numbers = []

for item in raw_data:
    # 跳过空字符串
    if item == "":
        print(f"跳过空数据: '{item}'")
        continue
    
    # 尝试转换为数字
    try:
        number = int(item)
        # 跳过负数
        if number < 0:
            print(f"跳过负数: {number}")
            continue
        
        # 添加有效数据
        valid_numbers.append(number)
        print(f"添加有效数据: {number}")
        
    except ValueError:
        # 跳过无法转换的字符串
        print(f"跳过无效数据: '{item}'")
        continue

print(f"\n有效数据列表: {valid_numbers}")

# 使用break在找到特定条件时提前结束
print("\n===搜索特定数据===")
target = 40
print(f"搜索目标: {target}")

for i, number in enumerate(valid_numbers):
    print(f"检查索引 {i} 的值: {number}")
    
    if number == target:
        print(f"找到目标值 {target}，位于索引 {i}")
        break  # 找到目标后立即退出循环
else:
    # for-else结构：循环正常结束时执行
    print(f"未找到目标值 {target}")

# 演示嵌套循环中的break和continue
print("\n===嵌套循环演示===")
matrix = [
    [1, 2, 3, 4],
    [5, 6, 7, 8],
    [9, 10, 11, 12],
    [13, 14, 15, 16]
]

print("矩阵数据:")
for row in matrix:
    print(row)

print("\n查找大于10的偶数:")
found = False

for i, row in enumerate(matrix):
    for j, element in enumerate(row):
        # 如果是奇数，跳过
        if element % 2 != 0:
            continue
        
        # 如果小于等于10，跳过
        if element <= 10:
            continue
        
        # 找到符合条件的数
        print(f"找到大于10的偶数: {element}，位置: [{i}][{j}]")
        found = True
        break  # 退出内层循环
    if found:
        break  # 退出外层循环

if not found:
    print("未找到大于10的偶数")
```

### 代码说明

**案例1代码解释**：
1. `for attempt in range(1, max_attempts + 1):`：使用range()限制循环次数
2. `break`：在密码正确或用户选择退出时跳出循环
3. `continue`：在for循环中，continue会直接进入下一次迭代
4. `while True:`：创建无限循环，完全依赖break语句退出

如果把验证密码正确性的`break`语句删除，即使密码正确，循环也会继续执行，直到达到最大尝试次数，这不是我们想要的行为。

**案例2代码解释**：
1. `continue`：在遇到无效数据时跳过处理步骤，继续处理下一个数据
2. `break`：在找到目标数据后立即退出搜索循环，提高效率
3. `for-else`结构：只有当for循环正常结束（没有被break中断）时，else块才会执行
4. 嵌套循环中的`break`：只退出最内层的循环

如果在嵌套循环中只使用一个`break`来退出外层循环，实际上只能退出内层循环，外层循环会继续执行。要退出多层循环，需要使用标志变量或其它方法。

## 4. 比较和逻辑运算符

### 知识点解析

**概念定义**：比较和逻辑运算符就像我们做判断时用的连接词一样。比较运算符用来比较两个值的大小关系（如"大于"、"等于"），逻辑运算符用来组合多个条件（如"并且"、"或者"）。

**核心规则**：
1. 比较运算符：==（等于）、!=（不等于）、<（小于）、>（大于）、<=（小于等于）、>=（大于等于）
2. 逻辑运算符：and（并且）、or（或者）、not（非）
3. 可以使用括号来明确运算优先级
4. Python支持短路求值，提高程序效率

**常见易错点**：
1. 混淆赋值运算符(=)和比较运算符(==)
2. 逻辑运算符优先级错误，如`True or False and False`结果是True而不是False
3. 比较不同类型的值导致意外结果
4. 忘记使用括号明确复杂的逻辑表达式

### 实战案例

#### 案例1：用户注册验证系统
```python
# 用户注册验证系统
print("===用户注册验证系统===")

def validate_username(username):
    """验证用户名"""
    print(f"验证用户名: '{username}'")
    
    # 检查用户名长度
    if len(username) < 3:
        print("  错误: 用户名至少需要3个字符")
        return False
    
    # 检查用户名是否包含非法字符
    illegal_chars = [' ', '!', '@', '#', '$', '%', '^', '&', '*']
    for char in illegal_chars:
        if char in username:
            print(f"  错误: 用户名不能包含字符 '{char}'")
            return False
    
    print("  用户名验证通过")
    return True

def validate_password(password):
    """验证密码"""
    print(f"验证密码: '{password}'")
    
    # 检查密码长度
    if len(password) < 6:
        print("  错误: 密码至少需要6个字符")
        return False
    
    # 检查是否包含数字
    has_digit = False
    for char in password:
        if char.isdigit():
            has_digit = True
            break
    
    if not has_digit:
        print("  错误: 密码必须包含至少一个数字")
        return False
    
    # 检查是否包含字母
    has_letter = False
    for char in password:
        if char.isalpha():
            has_letter = True
            break
    
    if not has_letter:
        print("  错误: 密码必须包含至少一个字母")
        return False
    
    print("  密码验证通过")
    return True

def validate_email(email):
    """验证邮箱"""
    print(f"验证邮箱: '{email}'")
    
    # 检查是否包含@符号
    if '@' not in email:
        print("  错误: 邮箱必须包含@符号")
        return False
    
    # 检查是否包含点号
    if '.' not in email:
        print("  错误: 邮箱格式不正确")
        return False
    
    # 检查@符号是否在适当位置
    at_index = email.find('@')
    if at_index == 0 or at_index == len(email) - 1:
        print("  错误: @符号位置不正确")
        return False
    
    print("  邮箱验证通过")
    return True

# 主程序
print("请输入注册信息:")

# 验证用户名
while True:
    username = input("用户名 (至少3个字符，不能包含空格和特殊符号): ")
    if validate_username(username):
        break
    print("请重新输入用户名\n")

# 验证密码
while True:
    password = input("密码 (至少6个字符，必须包含数字和字母): ")
    if validate_password(password):
        break
    print("请重新输入密码\n")

# 验证邮箱
while True:
    email = input("邮箱: ")
    if validate_email(email):
        break
    print("请重新输入邮箱\n")

# 综合验证所有信息
print("\n===注册信息确认===")
print(f"用户名: {username}")
print(f"密码: {'*' * len(password)}")  # 隐藏密码显示
print(f"邮箱: {email}")

# 检查用户名和邮箱是否已存在（模拟）
existing_usernames = ['admin', 'user1', 'test']
existing_emails = ['admin@example.com', 'user1@example.com']

username_exists = username in existing_usernames
email_exists = email in existing_emails

if username_exists or email_exists:
    print("注册失败:")
    if username_exists:
        print("  用户名已存在")
    if email_exists:
        print("  邮箱已被注册")
else:
    print("注册成功! 欢迎加入我们")
```

#### 案例2：成绩评估和推荐系统
```python
# 成绩评估和推荐系统
print("===成绩评估和推荐系统===")

# 学生信息和成绩
students = [
    {"name": "张三", "math": 95, "english": 87, "science": 92},
    {"name": "李四", "math": 78, "english": 82, "science": 75},
    {"name": "王五", "math": 90, "english": 88, "science": 94},
    {"name": "赵六", "math": 58, "english": 65, "science": 70},
    {"name": "钱七", "math": 88, "english": 90, "science": 85}
]

# 评估标准
EXCELLENT_THRESHOLD = 90  # 优秀门槛
GOOD_THRESHOLD = 80       # 良好门槛
PASS_THRESHOLD = 60       # 及格门槛

print("学生成绩评估:")

for student in students:
    name = student["name"]
    math = student["math"]
    english = student["english"]
    science = student["science"]
    
    # 计算平均分
    average = (math + english + science) / 3
    
    # 评估各科成绩
    print(f"\n{name}的成绩分析:")
    print(f"  数学: {math}分")
    print(f"  英语: {english}分")
    print(f"  科学: {science}分")
    print(f"  平均分: {average:.2f}分")
    
    # 检查是否有不及格科目
    failed_subjects = []
    if math < PASS_THRESHOLD:
        failed_subjects.append("数学")
    if english < PASS_THRESHOLD:
        failed_subjects.append("英语")
    if science < PASS_THRESHOLD:
        failed_subjects.append("科学")
    
    # 综合评估
    if not failed_subjects and average >= EXCELLENT_THRESHOLD:
        # 优秀学生：各科及格且平均分90以上
        print(f"  评估结果: 优秀")
        print(f"  建议: 保持现有学习状态，可考虑参与竞赛")
    elif not failed_subjects and average >= GOOD_THRESHOLD:
        # 良好学生：各科及格且平均分80以上
        print(f"  评估结果: 良好")
        print(f"  建议: 继续努力，争取进入优秀行列")
    elif not failed_subjects:
        # 及格学生：各科及格但平均分低于80
        print(f"  评估结果: 及格")
        print(f"  建议: 需要加强学习，提高整体成绩")
    else:
        # 有不及格科目
        print(f"  评估结果: 需要改进")
        print(f"  不及格科目: {', '.join(failed_subjects)}")
        print(f"  建议: 重点补习不及格科目，寻求老师帮助")
    
    # 使用逻辑运算符的复杂条件判断
    # 检查是否在特定科目表现突出
    math_excellent = math >= EXCELLENT_THRESHOLD
    english_excellent = english >= EXCELLENT_THRESHOLD
    science_excellent = science >= EXCELLENT_THRESHOLD
    
    # 如果数学优秀但英语不优秀，建议加强英语
    if math_excellent and not english_excellent:
        print(f"  特别建议: 数学成绩优秀，但英语需要加强")
    
    # 如果英语和科学都优秀但数学一般，建议保持优势
    if english_excellent and science_excellent and math < EXCELLENT_THRESHOLD:
        print(f"  特别建议: 英语和科学成绩优秀，继续保持，同时提升数学")
    
    # 如果所有科目都优秀，给予特别表扬
    if math_excellent and english_excellent and science_excellent:
        print(f"  特别表扬: 所有科目成绩优秀，是全科发展的典范")

# 使用复杂逻辑运算符筛选学生
print(f"\n===学生筛选结果===")

# 筛选数学和英语都优秀的学生
print("数学和英语都优秀的学生:")
for student in students:
    if student["math"] >= EXCELLENT_THRESHOLD and student["english"] >= EXCELLENT_THRESHOLD:
        average = (student["math"] + student["english"] + student["science"]) / 3
        print(f"  {student['name']}: 数学{student['math']}分, 英语{student['english']}分, 平均分{average:.2f}分")

# 筛选至少有一科优秀的学生
print("\n至少有一科优秀的学生:")
for student in students:
    if (student["math"] >= EXCELLENT_THRESHOLD or 
        student["english"] >= EXCELLENT_THRESHOLD or 
        student["science"] >= EXCELLENT_THRESHOLD):
        print(f"  {student['name']}")

# 筛选没有不及格科目的学生
print("\n没有不及格科目的学生:")
for student in students:
    if (student["math"] >= PASS_THRESHOLD and 
        student["english"] >= PASS_THRESHOLD and 
        student["science"] >= PASS_THRESHOLD):
        print(f"  {student['name']}")

# 演示短路求值
print(f"\n===短路求值演示===")

def check_condition_a():
    print("  检查条件A")
    return False

def check_condition_b():
    print("  检查条件B")
    return True

print("测试 and 运算符的短路求值:")
print("表达式: check_condition_a() and check_condition_b()")
result = check_condition_a() and check_condition_b()
print(f"结果: {result}")
print("注意: 由于条件A为False，条件B没有被检查（短路）")

print("\n测试 or 运算符的短路求值:")
print("表达式: check_condition_b() or check_condition_a()")
result = check_condition_b() or check_condition_a()
print(f"结果: {result}")
print("注意: 由于条件B为True，条件A没有被检查（短路）")
```

### 代码说明

**案例1代码解释**：
1. `if len(username) < 3:`：使用比较运算符检查用户名长度
2. `if char in username:`：使用成员运算符检查字符是否在字符串中
3. `if username_exists or email_exists:`：使用or运算符检查用户名或邮箱是否存在
4. `if math_excellent and not english_excellent:`：使用and和not运算符组合复杂条件

如果把 `if char in username:` 写成 `if char == username:`，这样只能检查字符是否与整个用户名相等，而不是检查字符是否在用户名中，逻辑就完全错误了。

**案例2代码解释**：
1. `if not failed_subjects and average >= EXCELLENT_THRESHOLD:`：使用not运算符检查列表是否为空
2. `if math_excellent and english_excellent and science_excellent:`：使用多个and运算符组合条件
3. `if (student["math"] >= EXCELLENT_THRESHOLD or ...):`：使用or运算符检查至少一个条件
4. 短路求值演示了Python在逻辑运算中的优化机制

如果把复杂的逻辑条件写成 `if math >= 90 and english >= 90 or science >= 90:` 而不使用括号，由于and的优先级高于or，实际逻辑会变成 `(math >= 90 and english >= 90) or science >= 90`，这可能不是我们想要的结果。

## 5. 三元运算符

### 知识点解析

**概念定义**：三元运算符就像我们做简单选择时的快捷表达方式。比如"如果天气好就去公园，否则就在家休息"可以简化为"天气好去公园，否则在家"。在Python中，三元运算符让我们可以用一行代码表达简单的if-else逻辑。

**核心规则**：
1. 语法格式：`值1 if 条件 else 值2`
2. 条件为真时返回值1，条件为假时返回值2
3. 三元运算符只能用于简单的条件判断
4. 可以嵌套使用，但不建议过度嵌套

**常见易错点**：
1. 混淆三元运算符的语法顺序
2. 在复杂逻辑中强行使用三元运算符，导致代码难以理解
3. 忘记三元运算符是从左到右结合的
4. 在需要执行多个语句时错误地使用三元运算符

### 实战案例

#### 案例1：成绩等级转换器
```python
# 成绩等级转换器
print("===成绩等级转换器===")

def get_grade_letter(score):
    """使用三元运算符获取成绩等级"""
    return "A" if score >= 90 else "B" if score >= 80 else "C" if score >= 70 else "D" if score >= 60 else "F"

def get_grade_description(score):
    """使用三元运算符获取成绩描述"""
    return "优秀" if score >= 90 else "良好" if score >= 80 else "中等" if score >= 70 else "及格" if score >= 60 else "不及格"

# 测试不同分数
test_scores = [95, 85, 75, 65, 55, 100, 0]

print("分数转换结果:")
print(f"{'分数':<6} {'等级':<4} {'描述':<4}")
print("-" * 20)

for score in test_scores:
    letter = get_grade_letter(score)
    description = get_grade_description(score)
    print(f"{score:<6} {letter:<4} {description:<4}")

# 使用三元运算符处理用户输入
print(f"\n===交互式成绩查询===")
while True:
    score_input = input("请输入分数 (0-100，输入'quit'退出): ")
    
    if score_input.lower() == 'quit':
        print("程序退出")
        break
    
    try:
        score = float(score_input)
        
        # 验证分数范围
        if score < 0 or score > 100:
            print("错误: 分数应在0-100之间")
            continue
        
        # 使用三元运算符判断是否及格
        status = "及格" if score >= 60 else "不及格"
        
        # 获取等级和描述
        letter = get_grade_letter(score)
        description = get_grade_description(score)
        
        # 使用三元运算符给出学习建议
        suggestion = ("继续保持" if score >= 90 else 
                     "再接再厉" if score >= 80 else 
                     "需要努力" if score >= 70 else 
                     "加倍努力" if score >= 60 else 
                     "急需补习")
        
        print(f"分数: {score}")
        print(f"等级: {letter} ({description})")
        print(f"状态: {status}")
        print(f"建议: {suggestion}")
        print()
        
    except ValueError:
        print("错误: 请输入有效的数字")
```

#### 案例2：用户权限和折扣系统
```python
# 用户权限和折扣系统
print("===用户权限和折扣系统===")

# 用户信息
users = {
    "admin": {"role": "administrator", "level": 5, "is_vip": True},
    "vip_user": {"role": "user", "level": 3, "is_vip": True},
    "regular_user": {"role": "user", "level": 1, "is_vip": False},
    "guest": {"role": "guest", "level": 0, "is_vip": False}
}

# 商品信息
products = {
    "笔记本电脑": 5999,
    "手机": 3999,
    "平板": 2999,
    "耳机": 299,
    "充电器": 99
}

def get_user_discount(user_info):
    """根据用户信息获取折扣率"""
    role = user_info["role"]
    is_vip = user_info["is_vip"]
    level = user_info["level"]
    
    # 使用三元运算符确定折扣
    discount = 0.9 if role == "administrator" else 0.95 if is_vip else 1.0
    
    # 根据等级额外折扣
    level_discount = 0.98 if level >= 3 else 0.99 if level >= 1 else 1.0
    
    # 组合折扣
    final_discount = discount * level_discount
    return final_discount

def get_access_level(user_info):
    """根据用户信息获取访问级别"""
    role = user_info["role"]
    level = user_info["level"]
    
    # 使用三元运算符确定访问级别
    access = "完全访问" if role == "administrator" else "受限访问" if role == "user" else "只读访问"
    return access

def calculate_final_price(original_price, user_info):
    """计算最终价格"""
    discount = get_user_discount(user_info)
    final_price = original_price * discount
    return round(final_price, 2)

# 演示不同用户的权限和折扣
print("用户权限和折扣信息:")
print(f"{'用户名':<12} {'角色':<12} {'VIP':<6} {'等级':<6} {'折扣':<6} {'访问级别':<8}")
print("-" * 60)

for username, user_info in users.items():
    discount = get_user_discount(user_info)
    access_level = get_access_level(user_info)
    is_vip = "是" if user_info["is_vip"] else "否"
    
    print(f"{username:<12} {user_info['role']:<12} {is_vip:<6} {user_info['level']:<6} {discount:<6.2f} {access_level:<8}")

# 演示商品价格计算
print(f"\n===商品价格计算===")
print("不同用户购买商品的最终价格:")
selected_product = "笔记本电脑"
original_price = products[selected_product]

print(f"商品: {selected_product}")
print(f"原价: {original_price}元")
print(f"{'用户名':<12} {'折扣率':<8} {'最终价格':<10} {'节省金额':<10}")
print("-" * 45)

for username, user_info in users.items():
    final_price = calculate_final_price(original_price, user_info)
    discount_rate = get_user_discount(user_info)
    saved_amount = original_price - final_price
    
    print(f"{username:<12} {discount_rate:<8.2f} {final_price:<10.2f} {saved_amount:<10.2f}")

# 使用三元运算符处理购物车
print(f"\n===购物车价格计算===")

# 模拟购物车
shopping_carts = {
    "admin": ["笔记本电脑", "手机", "耳机"],
    "vip_user": ["平板", "耳机", "充电器"],
    "regular_user": ["耳机", "充电器"],
    "guest": ["充电器"]
}

def calculate_cart_total(cart, user_info):
    """计算购物车总价"""
    total = 0
    for item in cart:
        if item in products:
            item_price = calculate_final_price(products[item], user_info)
            total += item_price
    return round(total, 2)

# 计算各用户购物车总价
for username, cart in shopping_carts.items():
    user_info = users[username]
    cart_total = calculate_cart_total(cart, user_info)
    
    # 使用三元运算符判断是否免运费
    shipping_fee = 0 if cart_total >= 1000 else 50 if cart_total >= 500 else 100
    final_total = cart_total + shipping_fee
    
    # 使用三元运算符给出运费提示
    shipping_msg = "免运费" if shipping_fee == 0 else f"运费: {shipping_fee}元"
    
    print(f"{username}的购物车:")
    print(f"  商品: {', '.join(cart)}")
    print(f"  商品总价: {cart_total}元")
    print(f"  运费: {shipping_msg}")
    print(f"  最终总价: {final_total}元")
    print()

# 演示三元运算符在列表推导式中的应用
print("===列表推导式中的三元运算符===")

# 原始分数列表
scores = [95, 85, 75, 65, 55, 100, 30, 88]

# 使用三元运算符在列表推导式中过滤和转换数据
passed_scores = [score for score in scores if score >= 60]
grade_descriptions = ["及格" if score >= 60 else "不及格" for score in scores]
bonus_scores = [score + 5 if score < 90 else score for score in scores]  # 为非优秀成绩加分

print(f"原始分数: {scores}")
print(f"及格分数: {passed_scores}")
print(f"成绩描述: {grade_descriptions}")
print(f"加分后分数: {bonus_scores}")

# 使用三元运算符和字典推导式
grade_dict = {score: "优秀" if score >= 90 else "良好" if score >= 80 else "中等" if score >= 70 else "及格" if score >= 60 else "不及格" for score in scores}
print(f"分数等级字典: {grade_dict}")
```

### 代码说明

**案例1代码解释**：
1. `return "A" if score >= 90 else "B" if score >= 80 else ...`：嵌套的三元运算符实现多条件判断
2. `status = "及格" if score >= 60 else "不及格"`：简单的二元条件判断
3. `suggestion = ("继续保持" if score >= 90 else ...)`：使用括号和换行提高可读性
4. 三元运算符使代码更加简洁，避免了多个if-elif-else语句

如果把三元运算符写成 `score >= 60 ? "及格" : "不及格"`，这会报语法错误，因为这是其他语言（如C、Java）的语法，Python使用`if-else`语法。

**案例2代码解释**：
1. `discount = 0.9 if role == "administrator" else 0.95 if is_vip else 1.0`：根据用户角色确定折扣
2. `is_vip = "是" if user_info["is_vip"] else "否"`：将布尔值转换为中文描述
3. `shipping_fee = 0 if cart_total >= 1000 else 50 if cart_total >= 500 else 100`：多级条件判断运费
4. 在列表推导式中使用三元运算符：`[score + 5 if score < 90 else score for score in scores]`

如果在需要执行多个语句的情况下强行使用三元运算符，如 `print("及格") if score >= 60 else print("不及格")`，虽然语法正确，但降低了代码可读性，应该使用传统的if-else语句。