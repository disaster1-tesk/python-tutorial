# Python基础语法

---

## 学习目标

完成本章节学习后，你将能够：

| 目标 | 描述 | 重要性 |
|------|------|--------|
| 变量操作 | 理解变量的概念，掌握变量命名规则和赋值操作 | ⭐⭐⭐ 必备 |
| 注释编写 | 学会使用单行注释和多行注释，提高代码可读性 | ⭐⭐⭐ 必备 |
| 缩进理解 | 掌握Python缩进规则，理解代码块的逻辑关系 | ⭐⭐⭐ 必备 |
| 输入输出 | 熟练使用print()输出和input()获取用户输入 | ⭐⭐⭐ 必备 |
| 命名规范 | 遵循PEP 8命名规范，编写可读性强的代码 | ⭐⭐ 重要 |
| 数据类型 | 理解常见数据类型（字符串、数字、布尔值） | ⭐⭐⭐ 必备 |

---

## 预习检查

在开始学习之前，请尝试回答以下问题：

1. 如果要存储一个用户的姓名和年龄，你会如何定义变量？
2. 为什么Python代码中的缩进如此重要？
3. `=` 和 `==` 有什么区别？
4. 如何让程序等待用户输入一个数字并进行计算？

如果你对以上问题还有疑惑，不用担心，通过本章节的学习，你会找到答案！

---

## 章节概览

```
┌─────────────────────────────────────────────────────────┐
│                    Python基础语法                          │
├─────────────────────────────────────────────────────────┤
│  1. 变量和赋值    │  存储数据的容器                        │
│  2. 注释         │  代码的说明文档                        │
│  3. 缩进         │  Python的灵魂                          │
│  4. 输出函数      │  print() 让程序"说话"                  │
│  5. 输入函数      │  input() 让程序"倾听"                  │
│  6. 命名规范      │  写出专业的代码                          │
└─────────────────────────────────────────────────────────┘
```

---

## 1. 变量和赋值

### 知识点解析

**概念定义**：变量就像是一个贴了标签的盒子，我们可以把数据放进盒子里，也可以从盒子里取出数据使用。在Python中，我们不需要提前声明盒子的大小和类型，只需要给它起个名字，然后把数据放进去就可以了。

**核心规则**：
1. 变量名只能包含字母、数字和下划线，不能以数字开头
2. 变量名不能是Python的关键字，如`if`、`for`、`while`等
3. 变量名区分大小写，`name`和`Name`是两个不同的变量
4. 推荐使用小写字母和下划线组合命名，如`student_name`

**常见易错点**：
1. 混淆赋值运算符`=`和等于比较运算符`==`，前者是把右边的值放进左边的变量盒子，后者是判断两边是否相等
2. 使用了关键字作为变量名，如`class = 5`会报错
3. 变量名使用了特殊字符，如`user-name`是不允许的

### 常见错误详解

**错误1：使用关键字作为变量名**
```python
# ❌ 错误示例
class = "Python"
for = 123
if = True

# 🔧 正确做法：避免使用Python保留关键字
class_name = "Python"      # 用下划线区分
loop_counter = 123         # 用描述性名称
condition = True            # 用有意义的名称
```

**错误2：变量名包含非法字符**
```python
# ❌ 错误示例
user-name = "张三"     # 减号不是合法字符
my variable = 10       # 空格不是合法字符
2nd_place = "第二名"    # 不能以数字开头

# 🔧 正确做法：使用字母、数字、下划线组合
user_name = "张三"      # 下划线连接
my_variable = 10        # 下划线连接
second_place = "第二名"  # 英文单词代替数字开头
```

**错误3：变量未定义就使用**
```python
# ❌ 错误示例
print(age)  # NameError: name 'age' is not defined

# 🔧 正确做法：先赋值后使用
age = 25
print(age)  # 输出: 25
```

### 最佳实践

**1. 选择有意义的变量名**
```python
# ❌ 差的命名
a = 5
x = "张三"
tmp = 100

# ✅ 好的命名
student_age = 5
user_name = "张三"
temporary_value = 100
```

**2. 使用一致的命名风格**
```python
# Python推荐使用蛇底式命名(snake_case)
user_name = "张三"
total_score = 250
is_valid = True
```

**3. 适当使用常量命名约定**
```python
# 约定：全大写表示常量（不可修改的值）
MAX_RETRY_COUNT = 3
DEFAULT_TIMEOUT = 30
PI = 3.14159
```

**4. 避免使用拼音或缩写**
```python
# ❌ 不推荐
xingming = "张三"
cs = 85

# ✅ 推荐
student_name = "张三"
chinese_score = 85
```

### 知识扩展

**变量背后的原理**
在Python中，变量实际上是一个"引用"。当你写 `a = 10` 时，Python会在内存中创建一个整数对象10，然后让变量`a`指向这个对象。

```python
a = 10
b = a      # b也指向同一个对象
a = 20     # a现在指向新的对象20

print(b)   # 输出10，因为b仍然指向原来的对象
```

这种机制叫做"引用赋值"，理解这一点对后续学习列表和对象非常重要。

### 自测题

1. 以下哪个变量名是合法的？
   - A. `2nd_place`
   - B. `user-name`
   - C. `student_name`
   - D. `class`

2. 执行以下代码后，x的值是多少？
   ```python
   x = 5
   y = x
   x = 10
   # y = ?
   ```

---

### 实战案例

#### 案例1：学生成绩管理系统
```python
# 学生成绩管理
student_name = "张三"        # 存储学生姓名
math_score = 95             # 数学成绩
english_score = 87          # 英语成绩
science_score = 92          # 科学成绩

# 计算总分和平均分
total_score = math_score + english_score + science_score  # 总分
average_score = total_score / 3                           # 平均分

# 输出结果
print(f"学生姓名: {student_name}")
print(f"总分: {total_score}")
print(f"平均分: {average_score:.2f}")  # 保留两位小数
```

#### 案例2：简单购物车计算
```python
# 商品价格定义
apple_price = 5.5      # 苹果单价
banana_price = 3.0     # 香蕉单价
orange_price = 4.2     # 橙子单价

# 购买数量
apple_count = 3        # 购买3个苹果
banana_count = 5       # 购买5根香蕉
orange_count = 2       # 购买2个橙子

# 计算各项总价
apple_total = apple_price * apple_count      # 苹果总价
banana_total = banana_price * banana_count   # 香蕉总价
orange_total = orange_price * orange_count   # 橙子总价

# 计算购物车总金额
shopping_cart_total = apple_total + banana_total + orange_total

# 输出购物清单
print("购物清单:")
print(f"苹果: {apple_count}个 × {apple_price}元 = {apple_total}元")
print(f"香蕉: {banana_count}根 × {banana_price}元 = {banana_total}元")
print(f"橙子: {orange_count}个 × {orange_price}元 = {orange_total}元")
print(f"总计: {shopping_cart_total}元")
```

### 代码说明

**案例1代码解释**：
1. `student_name = "张三"`：创建一个名为`student_name`的变量，把字符串"张三"放进去
2. `math_score = 95`：创建一个名为`math_score`的变量，把数字95放进去
3. `total_score = math_score + english_score + science_score`：把三个科目的分数相加，结果存入`total_score`变量
4. `average_score = total_score / 3`：用总分除以科目数得到平均分
5. `print(f"学生姓名: {student_name}")`：使用f-string格式化输出，把变量值插入到字符串中

如果把`total_score / 3`改成`total_score / 2`，那么计算出的平均分会偏高，结果就不正确了。

**案例2代码解释**：
1. `apple_price = 5.5`：定义苹果单价为5.5元
2. `apple_count = 3`：定义购买3个苹果
3. `apple_total = apple_price * apple_count`：计算苹果总价=单价×数量
4. `shopping_cart_total = apple_total + banana_total + orange_total`：把所有商品总价相加得到购物车总金额

如果把`*`写成`+`，比如`apple_total = apple_price + apple_count`，那结果就变成了5.5+3=8.5，而不是5.5×3=16.5，计算结果完全错误。

## 2. 注释

### 知识点解析

**概念定义**：注释就是我们在代码中写的"笔记"，这些内容不会被计算机执行，是专门给人看的。就像我们在书上做标记一样，帮助我们和其他人理解代码的作用。

**核心规则**：
1. 单行注释用`#`开头，从`#`开始到行尾的所有内容都会被忽略
2. 多行注释可以用三个单引号`'''`或三个双引号`"""`包围
3. 函数和类下面的字符串（文档字符串）也是一种特殊的注释

**常见易错点**：
1. 忘记在`#`后面加空格，虽然不影响执行，但不规范
2. 多行注释的开始和结束符号不匹配
3. 在注释中写中文时出现编码问题（在现代Python中已较少见）

### 常见错误详解

**错误1：注释描述与代码不符**
```python
# ❌ 错误示例
x = 10  # 将x设置为20
y = x + 5  # 计算差值

# 🔧 正确做法：注释要准确描述代码功能
x = 10   # 初始化变量x为10
y = x + 5  # 计算y等于x加5
```

**错误2：过度注释**
```python
# ❌ 过度注释（说明性废话）
x = 5  # 将5赋值给x

# 🔧 正确做法：只注释复杂的逻辑
result = x * 2 + y / 3 - z  # 复杂的计算公式需要注释
```

**错误3：忘记更新注释**
```python
# ❌ 注释过时
def calculate_score(scores):
    # 返回最高分
    return sum(scores) / len(scores)  # 实际返回的是平均分！

# 🔧 正确做法：修改代码时同步更新注释
def calculate_score(scores):
    # 返回平均分
    return sum(scores) / len(scores)
```

### 注释类型速查表

| 类型 | 语法 | 用途 | 示例 |
|------|------|------|------|
| 单行注释 | `#` | 简短说明 | `# 计算总价` |
| 行内注释 | `#` | 代码同行说明 | `x = x + 1  # 计数器加1` |
| 多行注释 | `'''` 或 `"""` | 多行说明 | 跨行文本块 |
| 文档字符串 | `"""` | 函数/类说明 | `def func(): """说明"""` |

### 最佳实践

**1. 使用文档字符串（Docstring）记录函数**
```python
def calculate_area(radius):
    """
    计算圆的面积

    参数:
        radius (float): 圆的半径

    返回:
        float: 圆的面积

    示例:
        >>> calculate_area(5)
        78.54
    """
    return 3.14159 * radius ** 2
```

**2. 使用TODO标记未完成工作**
```python
def process_data(data):
    # TODO: 完成后添加数据验证
    # FIXME: 这里的算法需要优化
    return transform(data)
```

**3. 注释应该解释"为什么"而不是"是什么"**
```python
# ❌ 差的注释（重复代码内容）
if age >= 18:  # 如果年龄大于等于18
    is_adult = True  # 设置is_adult为True

# ✅ 好的注释（解释原因）
if age >= 18:
    is_adult = True  # 根据法律规定，18岁为法定成年年龄
```

### 知识扩展：三大引号的区别

在Python中，`'`、`"`、`'''`、`"""`都可以表示字符串，但在注释场景下有细微区别：

```python
# 单引号和双引号在单行时等价
text1 = 'Hello'
text2 = "Hello"

# 三引号可以跨行
text3 = """这是
一个多行
字符串"""

# ⚠️ 注意：多行注释其实是多行字符串
# 下面这段代码实际上创建了一个字符串（如果没有赋值给变量，字符串会被丢弃）
"""
这是一段被忽略的文本
可以当作多行注释使用
"""
```

### 自测题

1. 以下哪种注释方式适合记录函数的用途、参数和返回值？
   - A. 单行注释 `#`
   - B. 行内注释
   - C. 文档字符串 `"""..."""`
   - D. 以上都不对

2. 判断正误：注释中的内容会被Python解释器执行。

---

### 实战案例

#### 案例1：带注释的温度转换器
```python
# 温度转换器
# 作者: 张三
# 日期: 2023-01-01

def celsius_to_fahrenheit(celsius):
    """
    将摄氏度转换为华氏度
    公式: F = C * 9/5 + 32
    
    参数:
        celsius (float): 摄氏度温度值
        
    返回:
        float: 对应的华氏度温度值
    """
    # 使用转换公式计算华氏度
    fahrenheit = celsius * 9/5 + 32
    return fahrenheit

# 主程序开始
if __name__ == "__main__":
    # 获取用户输入
    celsius_temp = float(input("请输入摄氏度温度: "))
    
    # 调用转换函数
    fahrenheit_temp = celsius_to_fahrenheit(celsius_temp)
    
    # 输出转换结果
    print(f"{celsius_temp}°C = {fahrenheit_temp:.1f}°F")
```

#### 案例2：带详细注释的简单计算器
```python
"""
简单计算器程序
支持加减乘除四种运算
"""

# 定义加法函数
def add(x, y):
    """加法运算"""
    return x + y

# 定义减法函数
def subtract(x, y):
    """减法运算"""
    return x - y

# 定义乘法函数
def multiply(x, y):
    """乘法运算"""
    return x * y

# 定义除法函数
def divide(x, y):
    """除法运算"""
    # 检查除数是否为0
    if y == 0:
        # 如果除数为0，返回错误提示
        return "错误：除数不能为0"
    # 正常执行除法运算
    return x / y

# 主程序
print("选择运算:")
print("1. 加法")
print("2. 减法")
print("3. 乘法")
print("4. 除法")

# 获取用户选择
choice = input("请输入选择(1/2/3/4): ")

# 获取两个数字
num1 = float(input("请输入第一个数字: "))
num2 = float(input("请输入第二个数字: "))

# 根据用户选择执行相应运算
if choice == '1':
    # 执行加法运算
    result = add(num1, num2)
    print(f"{num1} + {num2} = {result}")
elif choice == '2':
    # 执行减法运算
    result = subtract(num1, num2)
    print(f"{num1} - {num2} = {result}")
elif choice == '3':
    # 执行乘法运算
    result = multiply(num1, num2)
    print(f"{num1} * {num2} = {result}")
elif choice == '4':
    # 执行除法运算
    result = divide(num1, num2)
    print(f"{num1} / {num2} = {result}")
else:
    # 用户输入了无效选择
    print("无效输入")
```

### 代码说明

**案例1代码解释**：
1. `# 温度转换器`：这是单行注释，说明程序名称
2. `"""将摄氏度转换为华氏度..."""`：这是函数的文档字符串，详细说明函数功能、参数和返回值
3. `# 使用转换公式计算华氏度`：解释下面一行代码的作用
4. `if __name__ == "__main__":`：这是一个特殊用法，确保下面的代码只在直接运行此文件时执行

如果删除了`# 获取用户输入`这行注释，程序仍然可以正常运行，但其他人阅读代码时就不容易理解这行代码的作用了。

**案例2代码解释**：
1. `"""简单计算器程序..."""`：这是模块级的文档字符串，说明整个程序的功能
2. 每个函数前都有单行注释说明函数作用
3. `# 检查除数是否为0`：解释为什么要进行这个判断
4. `# 如果除数为0，返回错误提示`：说明处理异常情况的逻辑

如果把`# 检查除数是否为0`改成`# 检查被除数是否为0`，虽然程序还能正常运行，但注释就不准确了，会误导阅读代码的人。

## 3. 缩进

### 知识点解析

**概念定义**：缩进就是代码前面的空格，它在Python中非常重要，因为它决定了哪些代码属于同一个"组"。就像我们写作文时用段落来组织内容一样，Python用缩进来组织代码的逻辑结构。

**核心规则**：
1. Python标准推荐使用4个空格作为一个缩进级别
2. 同一个代码块必须使用相同数量的空格缩进
3. 不要在同一个文件中混用空格和制表符(tab)
4. 冒号`:`后面通常要换行并缩进，表示下面的代码属于这个结构

**常见易错点**：
1. 缩进不一致，比如前面用4个空格，后面用2个空格
2. 混用空格和tab键
3. 忘记在`if`、`for`等语句后加冒号
4. 缩进过多导致代码嵌套太深，难以阅读

### 常见错误详解

**错误1：缩进不一致导致IndentationError**
```python
# ❌ 错误示例
if True:
    x = 1
     x = 2  # 缩进不一致！

# 🔧 正确做法：保持一致的缩进
if True:
    x = 1
    x = 2   # 正确缩进
```

**错误2：混用空格和Tab**
```python
# ❌ 错误示例 - 文件中同时包含空格和Tab
if True:
    x = 1
<Tab>y = 2  # Tab与空格混用

# 🔧 正确做法：在IDE中设置用空格代替Tab
# 大多数现代IDE可以自动处理这个
```

**错误3：复制粘贴后缩进混乱**
```python
# ❌ 从网页复制代码后可能变成这样
def func():
    line1 = "正确"
   line2 = "多了空格"  # 复制导致的错误缩进

# 🔧 正确做法：使用IDE的格式化功能
# PyCharm: Ctrl+Alt+L
# VS Code: Alt+Shift+F
```

### Tab vs 空格：为什么PEP 8推荐空格？

| 对比项 | Tab | 空格 |
|--------|-----|------|
| 可读性 | 不同人设置不同显示效果 | 统一显示 |
| 兼容性 | 可能导致缩进混乱 | 跨环境一致 |
| PEP 8推荐 | ❌ 不推荐 | ✅ 4个空格 |

**为什么Python选择缩进而不是花括号？**
Python的设计哲学是"简洁优美"。通过缩进来表示代码块，强制开发者写出结构清晰的代码。这叫做"Python之禅"的体现。

### 最佳实践

**1. 使用4个空格缩进**
```python
# PEP 8标准
if condition:
    do_something()      # 4个空格
    do_other()          # 4个空格
```

**2. 让IDE自动处理缩进**
```python
# 善用IDE的自动补全和格式化功能
# PyCharm设置: File -> Settings -> Editor -> Code Style -> Python -> Tab改为Spaces
```

**3. 避免过深的嵌套（建议最多3-4层）**
```python
# ❌ 嵌套过深，难以阅读
if a:
    if b:
        if c:
            if d:
                result = 1

# ✅ 使用函数或早期返回减少嵌套
def process():
    if not a:
        return
    if not b:
        return
    if not c:
        return
    if d:
        result = 1
```

### 知识扩展：IDE中的缩进设置

**PyCharm 配置方法**：
1. `File` → `Settings` → `Editor` → `Code Style` → `Python`
2. 勾选 `Use Tab character` 的反选（使用空格）
3. `Tab size` 和 `Indent` 都设置为 4

**VS Code 配置方法**：
```json
// settings.json
{
    "editor.tabSize": 4,
    "editor.insertSpaces": true,
    "editor.detectIndentation": false
}
```

### 自测题

1. 以下代码会输出什么？
   ```python
   if True:
       print("A")
   print("B")
   ```
   - A. 只输出 A
   - B. 只输出 B
   - C. 输出 A 和 B
   - D. 报错

2. Python中表示一个代码块应该使用多少个空格？
   - A. 1个
   - B. 2个
   - C. 4个
   - D. 任意数量，保持一致即可

---

### 实战案例

#### 案例1：成绩等级判断系统
```python
# 学生成绩等级判断
score = 85  # 学生分数

# 根据分数判断等级
if score >= 90:
    # 分数大于等于90是一等
    grade = "优秀"
    print("表现非常出色!")
elif score >= 80:
    # 分数大于等于80是二等
    grade = "良好"
    print("表现不错，继续努力!")
elif score >= 70:
    # 分数大于等于70是三等
    grade = "中等"
    print("还有提升空间!")
elif score >= 60:
    # 分数大于等于60是四等
    grade = "及格"
    print("刚好及格，需要加油!")
else:
    # 分数低于60是五等
    grade = "不及格"
    print("需要更加努力!")

# 输出最终等级
print(f"分数: {score}, 等级: {grade}")
```

#### 案例2：循环打印九九乘法表
```python
# 打印九九乘法表
# 外层循环控制行数
for i in range(1, 10):
    # 内层循环控制列数
    for j in range(1, i+1):
        # 计算乘积并打印
        product = i * j
        print(f"{j}×{i}={product}", end="  ")
    # 每行结束后换行
    print()

# 使用while循环实现相同功能
print("\n使用while循环:")
row = 1
# 控制行数的循环
while row <= 9:
    col = 1
    # 控制列数的循环
    while col <= row:
        # 计算并打印乘积
        product = row * col
        print(f"{col}×{row}={product}", end="  ")
        col += 1
    # 换行
    print()
    row += 1
```

### 代码说明

**案例1代码解释**：
1. `if score >= 90:`：判断分数是否大于等于90
2. 下面的两行代码都比`if`语句多4个空格，表示它们属于这个if语句块
3. `elif score >= 80:`：另一个条件判断，与前面的if属于同一级别
4. 每个条件下的代码块都保持相同的缩进

如果把`grade = "优秀"`这一行的缩进改为2个空格，而其他行保持4个空格，程序就会报错，因为Python要求同一个代码块的缩进必须一致。

**案例2代码解释**：
1. `for i in range(1, 10):`：外层循环
2. `for j in range(1, i+1):`：内层循环，比外层循环多缩进4个空格
3. `print(f"{j}×{i}={product}", end="  ")`：具体的打印语句，与内层循环同级
4. `print()`：与外层循环同级，但与内层循环不同级，表示内层循环结束后执行

如果把内层循环的代码块与外层循环对齐，那么内层循环就不再存在了，程序只会打印每一行的第一个乘法算式。

## 4. 输出函数

### 知识点解析

**概念定义**：输出函数就像我们在电脑屏幕上"说话"一样，可以把程序运行的结果展示给用户看。Python中最常用的输出函数是`print()`，它可以显示文字、数字等各种信息。

**核心规则**：
1. `print()`函数可以把内容显示在屏幕上
2. 可以同时输出多个值，用逗号分隔
3. 可以使用格式化字符串来控制输出格式
4. 可以通过`end`参数控制行尾字符，默认是换行符

**常见易错点**：
1. 忘记加括号，写成`print "hello"`而不是`print("hello")`
2. 混淆`print(变量)`和`print("变量")`，前者输出变量的值，后者输出字面字符串"变量"
3. 格式化字符串时参数个数和占位符不匹配

### print()函数参数详解

`print()`函数有多个参数，可以组合使用：

```python
print(*objects, sep=' ', end='\n', file=sys.stdout, flush=False)
```

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `sep` | 多个输出之间的分隔符 | 空格 |
| `end` | 输出结束符 | 换行符 `\n` |
| `file` | 输出目标 | 标准输出 |
| `flush` | 是否立即刷新 | False |

### print()使用技巧

**1. 用sep参数控制分隔符**
```python
print("苹果", "香蕉", "橙子", sep="、")
# 输出: 苹果、香蕉、橙子

print("2024", "01", "15", sep="-")
# 输出: 2024-01-15
```

**2. 用end参数控制行尾**
```python
print("正在加载", end="")
print("...")  # 不换行，输出: 正在加载...

print("第一步", end=" → ")
print("第二步", end=" → ")
print("完成")  # 输出: 第一步 → 第二步 → 完成
```

**3. 输出到文件**
```python
# 输出到文件
with open("output.txt", "w") as f:
    print("写入文件的内容", file=f)

# 同时输出到屏幕和文件
with open("log.txt", "a") as f:
    print("日志信息", file=f)
```

### 格式化输出对比

| 方法 | 语法 | 适用场景 |
|------|------|----------|
| %格式化 | `"%s %d" % (name, age)` | 简单场景 |
| format() | `"{} {}".format(name, age)` | 中等复杂度 |
| f-string | `f"{name} {age}"` | Python 3.6+，推荐 |

**推荐使用f-string（格式化字符串字面量）**：
```python
name = "张三"
age = 25
score = 95.5

# f-string格式化示例
print(f"姓名: {name}, 年龄: {age}")
print(f"成绩: {score:.1f}")        # 保留1位小数: 95.5
print(f"百分制: {score/100:.1%}")  # 百分比: 95.5%
print(f"右对齐: {score:>8.1f}")    # 右对齐:    95.5
print(f"左对齐: {score:<8.1f}")    # 左对齐: 95.5
print(f"居中对齐: {score:^8.1f}")  # 居中:   95.5
```

### 常见错误详解

**错误1：忘记f-string的f前缀**
```python
name = "张三"
# ❌ 错误
print("我的名字是 {name}")      # 输出: 我的名字是 {name}

# ✅ 正确
print(f"我的名字是 {name}")      # 输出: 我的名字是 张三
```

**错误2：格式化数字时类型错误**
```python
value = 3.14159
# ❌ 错误
print(f"圆周率: {value:.2d}")    # 报错！.2d要求整数

# ✅ 正确
print(f"圆周率: {value:.2f}")    # 输出: 圆周率: 3.14
```

### 知识扩展：print()的底层原理

`print()`函数实际上做了以下几件事：
1. 将所有参数转换为字符串
2. 用`sep`参数连接各字符串
3. 在末尾添加`end`参数
4. 调用`sys.stdout.write()`写入输出

```python
# print("a", "b") 实际上等价于：
import sys
sys.stdout.write("a" + " " + "b" + "\n")
```

### 自测题

1. 如何让print()输出多个值时不换行？
   - A. 设置 `sep=""`
   - B. 设置 `end=""`
   - C. 设置 `flush=True`
   - D. 无法实现

2. 执行以下代码，输出结果是什么？
   ```python
   print("A", "B", sep="-", end="!")
   print("C")
   ```
   - A. A B!C
   - B. A-B!C
   - C. A-B C
   - D. A B! C

---

### 实战案例

#### 案例1：个人健康报告生成器
```python
# 个人健康报告生成器
name = "李四"           # 姓名
age = 25               # 年龄
height = 175           # 身高(cm)
weight = 70            # 体重(kg)

# 计算BMI指数
bmi = weight / (height/100) ** 2

# 根据BMI判断身体状况
if bmi < 18.5:
    status = "偏瘦"
elif bmi < 24:
    status = "正常"
elif bmi < 28:
    status = "偏胖"
else:
    status = "肥胖"

# 输出健康报告
print("===个人健康报告===")
print(f"姓名: {name}")
print(f"年龄: {age}岁")
print(f"身高: {height}cm")
print(f"体重: {weight}kg")
print(f"BMI指数: {bmi:.2f}")
print(f"身体状况: {status}")
print("=" * 18)
```

#### 案例2：简单账单计算器
```python
# 简单账单计算器
print("===餐厅账单===")

# 菜品价格
dishes = [
    ("宫保鸡丁", 38),
    ("鱼香肉丝", 32),
    ("麻婆豆腐", 18),
    ("米饭", 2)
]

# 初始化总价
total = 0

# 打印每道菜的价格
print("菜品清单:")
for dish, price in dishes:
    print(f"{dish:<8} {price:>4}元")
    total += price

# 打印分隔线
print("-" * 15)

# 打印总价
print(f"{'总计':<8} {total:>4}元")

# 计算并打印人均消费(假设3人用餐)
people = 3
per_person = total / people
print(f"人均消费: {per_person:.2f}元")

# 感谢语
print("=" * 15)
print("谢谢惠顾，欢迎再次光临!")
```

### 代码说明

**案例1代码解释**：
1. `print("===个人健康报告===")`：输出固定文本作为标题
2. `print(f"姓名: {name}")`：使用f-string格式化，将变量name的值插入到字符串中
3. `print(f"BMI指数: {bmi:.2f}")`：格式化数字，保留两位小数
4. `print("=" * 18)`：将等号重复18次输出，形成分隔线

如果把`print(f"BMI指数: {bmi:.2f}")`写成`print(f"BMI指数: {bmi:.2d}")`，由于bmi是小数，而`.2d`要求是整数格式，程序就会报错。

**案例2代码解释**：
1. `print("菜品清单:")`：输出标题
2. `print(f"{dish:<8} {price:>4}元")`：格式化输出，`<8`表示左对齐占8个字符，`>4`表示右对齐占4个字符
3. `print("-" * 15)`：输出15个减号作为分隔线
4. `print(f"人均消费: {per_person:.2f}元")`：输出计算结果

如果把`{dish:<8}`改为`{dish:>8}`，菜品名称就会变成右对齐而不是左对齐，影响显示效果。

## 5. 输入函数

### 知识点解析

**概念定义**：输入函数就像我们在和电脑"对话"一样，可以让用户通过键盘把信息告诉程序。Python中用`input()`函数来获取用户的输入，程序会停下来等待用户输入内容。

**核心规则**：
1. `input()`函数会暂停程序执行，等待用户输入
2. `input()`函数总是返回字符串类型，即使输入的是数字
3. 可以给`input()`函数传入提示文字，显示给用户看
4. 需要用变量来保存用户输入的内容

**常见易错点**：
1. 忘记用变量接收`input()`的返回值
2. 忘记将字符串类型的输入转换为需要的数字类型
3. 没有处理用户输入错误的情况，如需要数字却输入了文字

### input()函数深入理解

**函数签名**：
```python
input(prompt='', /)
```
- `prompt`: 显示给用户的提示文字
- `/`: 表示`prompt`只能是位置参数
- 返回值：始终是字符串类型

### 常见错误详解

**错误1：不处理类型转换**
```python
# ❌ 危险代码
age = input("请输入年龄: ")  # 输入"20"
print(age + 5)  # TypeError: can't concat str to int

# ✅ 正确做法
age = int(input("请输入年龄: "))  # 输入"20"
print(age + 5)  # 输出: 25
```

**错误2：不验证输入有效性**
```python
# ❌ 不安全的代码
password = input("请输入密码: ")
# 用户可能输入任意内容，包括空字符串

# ✅ 正确做法：验证输入
password = input("请输入密码: ")
if not password:
    print("密码不能为空！")
elif len(password) < 6:
    print("密码长度至少6位！")
```

**错误3：input()在某些环境下阻塞**
```python
# 在GUI程序中使用input()会卡住界面
# 在Jupyter Notebook中运行良好
# 在命令行中运行良好
# 在某些嵌入式环境中可能不支持

# 建议：了解程序运行环境选择合适的输入方式
```

### 输入验证最佳实践

**1. 基本类型转换+异常处理**
```python
def get_number(prompt):
    """获取有效的数字输入"""
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("请输入有效的数字！")

age = get_number("请输入年龄: ")
print(f"你输入的年龄是: {age}")
```

**2. 带范围验证的数字输入**
```python
def get_score():
    """获取0-100之间的分数"""
    while True:
        try:
            score = float(input("请输入分数 (0-100): "))
            if 0 <= score <= 100:
                return score
            else:
                print("分数必须在0到100之间！")
        except ValueError:
            print("请输入有效的数字！")

score = get_score()
print(f"你输入的分数是: {score}")
```

**3. 带选项验证的选择输入**
```python
def get_choice(options, prompt="请选择"):
    """获取有效的选项"""
    while True:
        choice = input(f"{prompt} ({'/'.join(options)}): ")
        if choice in options:
            return choice
        print(f"无效选择，请输入 {options}")

choice = get_choice(['A', 'B', 'C'], "请选择操作")
print(f"你选择了: {choice}")
```

### 知识扩展：不同场景的输入方式

| 场景 | 推荐方法 | 说明 |
|------|----------|------|
| 命令行程序 | `input()` | 最常用 |
| 图形界面 | `tkinter.Entry` | GUI输入框 |
| Web应用 | `Flask` request | HTTP请求 |
| 自动化测试 | 直接传参 | Mock输入 |
| 游戏开发 | `pygame.event` | 事件驱动 |

### 自测题

1. 执行以下代码，如果用户输入"25"，变量age的类型是什么？
   ```python
   age = input("请输入年龄: ")
   ```
   - A. int
   - B. float
   - C. str
   - D. 不确定

2. 如何让用户输入一个整数并确保输入有效？
   - A. `num = input("输入: ")`
   - B. `num = int(input("输入: "))`
   - C. `num = int(input("输入: "))` 加上 `try-except`
   - D. 无法实现

---

### 实战案例

#### 案例1：简单计算器（增强版）
```python
# 简单计算器 - 用户输入版
print("===简单计算器===")

# 获取用户输入的两个数字
try:
    num1 = float(input("请输入第一个数字: "))
    num2 = float(input("请输入第二个数字: "))
    
    # 获取运算符
    operator = input("请输入运算符 (+, -, *, /): ")
    
    # 根据运算符执行相应计算
    if operator == "+":
        result = num1 + num2
        print(f"{num1} + {num2} = {result}")
    elif operator == "-":
        result = num1 - num2
        print(f"{num1} - {num2} = {result}")
    elif operator == "*":
        result = num1 * num2
        print(f"{num1} * {num2} = {result}")
    elif operator == "/":
        if num2 != 0:
            result = num1 / num2
            print(f"{num1} / {num2} = {result}")
        else:
            print("错误: 除数不能为0")
    else:
        print("错误: 不支持的运算符")
        
except ValueError:
    print("错误: 请输入有效的数字")
```

#### 案例2：个人信息登记系统
```python
# 个人信息登记系统
print("===个人信息登记===")

# 收集用户信息
name = input("请输入您的姓名: ")
age_str = input("请输入您的年龄: ")

# 验证年龄输入
try:
    age = int(age_str)
    if age < 0 or age > 150:
        print("警告: 年龄输入可能有误")
except ValueError:
    print("警告: 年龄应为数字")
    age = 0

# 收集其他信息
city = input("请输入您所在的城市: ")
hobby = input("请输入您的爱好: ")

# 确认是否已婚
married_input = input("您是否已婚? (是/否): ")
if married_input in ["是", "y", "Y", "yes", "Yes"]:
    married = True
else:
    married = False

# 显示登记信息
print("\n===登记信息确认===")
print(f"姓名: {name}")
print(f"年龄: {age}")
print(f"城市: {city}")
print(f"爱好: {hobby}")
print(f"婚姻状况: {'已婚' if married else '未婚'}")

# 确认信息
confirm = input("\n信息是否正确? (是/否): ")
if confirm in ["是", "y", "Y", "yes", "Yes"]:
    print("信息登记成功!")
else:
    print("请重新登记信息")
```

### 代码说明

**案例1代码解释**：
1. `num1 = float(input("请输入第一个数字: "))`：获取用户输入并立即转换为浮点数
2. `operator = input("请输入运算符 (+, -, *, /): ")`：获取运算符，保持字符串类型
3. `try...except ValueError`：捕获可能的输入错误，如果用户输入的不是数字就会执行except块

如果把`float(input(...))`写成`int(input(...))`，那么用户输入小数时就会报错，比如输入3.14会被拒绝。

**案例2代码解释**：
1. `age_str = input("请输入您的年龄: ")`：先以字符串形式获取输入
2. `age = int(age_str)`：再转换为整数，分开处理可以更好地控制错误处理
3. `if married_input in ["是", "y", "Y", "yes", "Yes"]`：检查多种可能的"是"的输入方式

如果用户输入年龄时输入了"二十"而不是"20"，`int(age_str)`会抛出ValueError异常，程序会提示输入错误。

## 6. 命名规范和约定

### 知识点解析

**概念定义**：命名规范就像我们给东西起名字的规则，让所有人都能看懂这个名字代表什么。Python有一套大家都遵守的命名规则，这样无论谁写的代码，其他人都容易理解。

**核心规则**：
1. 变量和函数名使用小写字母，单词间用下划线分隔，如`student_name`
2. 类名使用大驼峰命名法，每个单词首字母大写，如`StudentInfo`
3. 常量名全部用大写字母，单词间用下划线分隔，如`MAX_SIZE`
4. 私有成员（不希望被外部直接访问的）以下划线开头，如`_private_data`

**常见易错点**：
1. 不区分变量、类、常量的命名方式，全都用同一种风格
2. 使用拼音命名，如`mingzi`而不是`name`
3. 命名过于简单，如用`a`、`b`、`x`等，除非在循环计数等简单场景
4. 命名过长，难以阅读

### Python命名风格速查表

| 类型 | 命名风格 | 示例 | 说明 |
|------|----------|------|------|
| 变量 | snake_case | `user_name` | 全小写，下划线连接 |
| 函数 | snake_case | `get_user()` | 动词+名词 |
| 类 | PascalCase | `UserInfo` | 名词，首字母大写 |
| 常量 | UPPER_SNAKE_CASE | `MAX_SIZE` | 全大写，下划线连接 |
| 私有属性 | _snake_case | `_secret` | 单下划线前缀 |
| 特殊属性 | __snake_case | `__init__` | 双下划线前后缀 |
| 模块 | snake_case | `my_module.py` | 全小写 |
| 包 | snake_case | `my_package/` | 全小写 |

### 常见错误详解

**错误1：混淆命名风格**
```python
# ❌ 错误示例
myFunction = "错误"    # 混用驼峰
user_Name = "错误"     # 部分大写
def Get_Name():        # 函数用PascalCase

# ✅ 正确示例
my_function = "正确"   # snake_case
user_name = "正确"     # snake_case
def get_name():        # snake_case
```

**错误2：使用单字母l和大写O**
```python
# ❌ 容易与数字1和0混淆
l = 100  # 小写L
O = "大写O"  # 大写O

# ✅ 正确示例
length = 100
name = "大写O"
```

**错误3：使用魔法数字**
```python
# ❌ 难以理解
if score > 60:
    print("及格")

# ✅ 正确示例
PASS_SCORE = 60
if score > PASS_SCORE:
    print("及格")
```

### 最佳实践

**1. 使用有意义的名称**
```python
# ❌ 差的命名
x = 25
temp = [1, 2, 3]
data = get_data()

# ✅ 好的命名
user_age = 25
sorted_numbers = [1, 2, 3]
database_records = get_data()
```

**2. 布尔变量使用is/has/can前缀**
```python
is_active = True        # 是否活跃
has_permission = True   # 是否有权限
can_edit = True         # 是否可以编辑
is_empty = False        # 是否为空
```

**3. 集合类型使用复数或list/dict后缀**
```python
users = ["张三", "李四"]           # 复数
user_list = ["张三", "李四"]        # list后缀
user_ids = {1, 2, 3}               # 复数
user_dict = {"name": "张三"}        # dict后缀
```

**4. 函数命名使用动词**
```python
def calculate(): pass    # 计算
def get_name(): pass     # 获取
def set_value(): pass    # 设置
def is_valid(): pass     # 判断
def find_user(): pass    # 查找
def validate_input(): pass # 验证
```

### 知识扩展：PEP 8命名建议总结

PEP 8是Python官方代码风格指南，以下是关键建议：

```
命名应反映意图，而非实现：
  ❌ bad: l1, l2, temp, tmp, data
  ✅ good: lowercase, member_age, class

避免使用：
  - 字符'l', 'O', 'I'作为单字符变量
  - 包/模块名中使用连字符(-)
  - 与内置名称冲突（如list, str, dict）

推荐做法：
  - 类名：CapWords（驼峰）
  - 异常名：CapWords + Error后缀
  - 函数名：lowercase + underscores
  - 常量：UPPERCASE + underscores
```

### 自测题

1. 以下哪个变量名最符合Python命名规范？
   - A. `myVariable`
   - B. `my_variable`
   - C. `MyVariable`
   - D. `MY_VARIABLE`

2. 类`StudentInfo`的命名风格叫什么？
   - A. snake_case
   - B. camelCase
   - C. PascalCase
   - D. kebab-case

3. 判断正误：`_private_var`是Python中的私有变量，外部无法访问。

---

### 实战案例

#### 案例1：图书管理系统命名规范示例
```python
# 图书管理系统命名规范示例

# 常量定义（全大写+下划线）
MAX_BOOKS = 1000          # 图书馆最大藏书量
DEFAULT_FINE_RATE = 0.5   # 默认罚款率（元/天）

# 类定义（大驼峰命名）
class BookInfo:
    """图书信息类"""
    def __init__(self, title, author, isbn):
        self.book_title = title     # 实例属性
        self.book_author = author   # 实例属性
        self.book_isbn = isbn       # 实例属性
        self._is_borrowed = False   # 私有属性，以下划线开头
    
    def borrow_book(self):
        """借阅图书方法"""
        if not self._is_borrowed:
            self._is_borrowed = True
            return True
        return False
    
    def return_book(self):
        """归还图书方法"""
        if self._is_borrowed:
            self._is_borrowed = False
            return True
        return False

# 函数定义（小写+下划线）
def calculate_fine(borrow_days):
    """
    计算超期罚款
    
    参数:
        borrow_days (int): 借阅天数
        
    返回:
        float: 罚款金额
    """
    if borrow_days > 30:  # 超过30天开始罚款
        overdue_days = borrow_days - 30
        fine = overdue_days * DEFAULT_FINE_RATE
        return fine
    return 0.0

# 变量命名示例
library_name = "市立图书馆"        # 图书馆名称
total_books = 1500                # 总图书数量
available_books = 1200            # 可借图书数量

# 使用示例
book = BookInfo("Python编程入门", "张三", "978-7-111-12345-6")
book.borrow_book()

fine_amount = calculate_fine(35)  # 借阅35天
print(f"罚款金额: {fine_amount}元")
```

#### 案例2：学生信息管理命名规范示例
```python
# 学生信息管理命名规范示例

# 常量定义
MAX_STUDENTS = 50        # 班级最大学生数
PASS_SCORE = 60          # 及格分数
EXCELLENT_SCORE = 90     # 优秀分数

# 类定义
class StudentRecord:
    """学生记录类"""
    def __init__(self, student_id, name, age):
        # 公有属性
        self.student_id = student_id  # 学号
        self.student_name = name      # 姓名
        self.student_age = age        # 年龄
        # 私有属性
        self._grades = {}             # 成绩字典
        self._attendance = []         # 考勤记录
    
    def add_grade(self, subject, score):
        """添加成绩"""
        if 0 <= score <= 100:
            self._grades[subject] = score
            return True
        return False
    
    def get_average_score(self):
        """计算平均分"""
        if not self._grades:
            return 0
        return sum(self._grades.values()) / len(self._grades)

# 函数定义
def evaluate_performance(average_score):
    """
    评估学业表现
    
    参数:
        average_score (float): 平均分
        
    返回:
        str: 表现等级
    """
    if average_score >= EXCELLENT_SCORE:
        return "优秀"
    elif average_score >= PASS_SCORE:
        return "及格"
    else:
        return "不及格"

def generate_report_card(student):
    """
    生成成绩单
    
    参数:
        student (StudentRecord): 学生对象
    """
    avg_score = student.get_average_score()
    performance = evaluate_performance(avg_score)
    
    print("===成绩单===")
    print(f"学号: {student.student_id}")
    print(f"姓名: {student.student_name}")
    print(f"平均分: {avg_score:.2f}")
    print(f"表现: {performance}")
    print("=" * 12)

# 变量命名示例
class_size = 45                    # 班级人数
student_list = []                  # 学生列表
passed_students_count = 0          # 及格学生数

# 使用示例
student = StudentRecord("2023001", "李明", 18)
student.add_grade("数学", 95)
student.add_grade("英语", 87)
student.add_grade("物理", 92)

generate_report_card(student)
```

### 代码说明

**案例1代码解释**：
1. `MAX_BOOKS = 1000`：常量使用全大写和下划线
2. `class BookInfo:`：类名使用大驼峰命名法
3. `book_title`：变量和属性使用小写加下划线
4. `def borrow_book(self):`：函数和方法也使用小写加下划线
5. `self._is_borrowed`：私有属性以下划线开头

如果把`MAX_BOOKS`写成`maxBooks`，虽然程序能运行，但不符合Python命名规范，其他人阅读代码时会感到困惑。

**案例2代码解释**：
1. `PASS_SCORE = 60`：常量清晰表达其含义
2. `class StudentRecord:`：类名表达出这是学生记录类
3. `student_id`：变量名清晰表达这是学生ID
4. `def get_average_score(self):`：方法名清晰表达其功能
5. `self._grades`：私有属性存储学生成绩

如果把`student_id`简写成`sid`，虽然短一些，但可读性下降，其他开发者可能不清楚这个变量的含义。