# Python类与对象知识点

## 1. 类的定义和对象创建

### 知识点解析

**概念定义**：类就像制作饼干的模具，定义了饼干的形状和大小，而对象就是用这个模具制作出来的具体饼干。在Python中，类是用来创建具有相同属性和行为的对象的模板。

**核心规则**：
1. 使用`class`关键字定义类，类名通常使用大驼峰命名法（如Person、BankAccount）
2. 类体必须缩进（通常4个空格）
3. 使用`__init__`方法定义构造函数，用于初始化对象
4. 通过类名加括号的方式创建对象实例

**常见易错点**：
1. 忘记在类定义后加冒号
2. 构造函数名写错，应该是`__init__`而不是`__init`或`init__`
3. 忘记在构造函数的第一个参数写`self`
4. 创建对象时忘记加括号

### 实战案例

#### 案例1：学生信息管理系统
```python
# 学生信息管理系统
print("===学生信息管理系统===")

# 定义学生类
class Student:
    """学生类"""
    
    def __init__(self, name, student_id, age):
        """
        初始化学生对象
        
        参数:
            name (str): 学生姓名
            student_id (str): 学生学号
            age (int): 学生年龄
        """
        self.name = name          # 学生姓名（实例属性）
        self.student_id = student_id  # 学生学号（实例属性）
        self.age = age            # 学生年龄（实例属性）
        self.courses = []         # 选修课程列表（实例属性）
        self.grades = {}          # 成绩字典（实例属性）
    
    def introduce(self):
        """自我介绍方法"""
        return f"我是{self.name}，学号是{self.student_id}，今年{self.age}岁"
    
    def enroll_course(self, course_name):
        """
        选修课程
        
        参数:
            course_name (str): 课程名称
        """
        if course_name not in self.courses:
            self.courses.append(course_name)
            print(f"{self.name}成功选修课程: {course_name}")
        else:
            print(f"{self.name}已经选修了{course_name}")
    
    def add_grade(self, course_name, grade):
        """
        添加成绩
        
        参数:
            course_name (str): 课程名称
            grade (float): 成绩
        """
        if course_name in self.courses:
            self.grades[course_name] = grade
            print(f"{self.name}的{course_name}成绩已录入: {grade}分")
        else:
            print(f"错误: {self.name}未选修{course_name}课程")
    
    def get_average_grade(self):
        """计算平均成绩"""
        if not self.grades:
            return 0
        return sum(self.grades.values()) / len(self.grades)
    
    def print_transcript(self):
        """打印成绩单"""
        print(f"\n=== {self.name}的成绩单 ===")
        print(f"姓名: {self.name}")
        print(f"学号: {self.student_id}")
        print(f"年龄: {self.age}")
        print("选修课程:")
        for course in self.courses:
            grade = self.grades.get(course, "未录入")
            print(f"  {course}: {grade}")
        print(f"平均成绩: {self.get_average_grade():.2f}")

# 创建学生对象
student1 = Student("张三", "2023001", 20)
student2 = Student("李四", "2023002", 19)

# 使用学生对象
print(student1.introduce())
print(student2.introduce())

# 选修课程
student1.enroll_course("Python编程")
student1.enroll_course("数据结构")
student1.enroll_course("算法设计")

student2.enroll_course("Python编程")
student2.enroll_course("高等数学")

# 添加成绩
student1.add_grade("Python编程", 95)
student1.add_grade("数据结构", 87)
student1.add_grade("算法设计", 92)

student2.add_grade("Python编程", 88)
student2.add_grade("高等数学", 90)

# 打印成绩单
student1.print_transcript()
student2.print_transcript()
```

#### 案例2：图书管理系统
```python
# 图书管理系统
print("\n===图书管理系统===")

# 定义图书类
class Book:
    """图书类"""
    
    def __init__(self, title, author, isbn, price=0):
        """
        初始化图书对象
        
        参数:
            title (str): 书名
            author (str): 作者
            isbn (str): ISBN号
            price (float): 价格，默认为0
        """
        self.title = title        # 书名
        self.author = author      # 作者
        self.isbn = isbn          # ISBN号
        self.price = price        # 价格
        self.is_borrowed = False  # 借阅状态
        self.borrower = None      # 借阅者
    
    def borrow(self, borrower_name):
        """
        借阅图书
        
        参数:
            borrower_name (str): 借阅者姓名
            
        返回:
            bool: 借阅是否成功
        """
        if self.is_borrowed:
            print(f"《{self.title}》已被{self.borrower}借阅，无法再次借阅")
            return False
        else:
            self.is_borrowed = True
            self.borrower = borrower_name
            print(f"《{self.title}》借阅成功，借阅者: {borrower_name}")
            return True
    
    def return_book(self):
        """归还图书"""
        if self.is_borrowed:
            borrower = self.borrower
            self.is_borrowed = False
            self.borrower = None
            print(f"《{self.title}》归还成功，归还者: {borrower}")
            return True
        else:
            print(f"《{self.title}》未被借阅")
            return False
    
    def get_info(self):
        """获取图书信息"""
        status = "已借出" if self.is_borrowed else "在馆"
        borrower_info = f"借阅者: {self.borrower}" if self.is_borrowed else ""
        return f"《{self.title}》 作者: {self.author} ISBN: {self.isbn} 价格: {self.price}元 状态: {status} {borrower_info}"

# 创建图书对象
book1 = Book("Python编程入门", "张三", "978-7-111-12345-6", 59.8)
book2 = Book("数据结构与算法", "李四", "978-7-111-12346-3", 79.5)
book3 = Book("设计模式", "王五", "978-7-111-12347-0", 89.0)

# 使用图书对象
print("图书馆藏书:")
print(book1.get_info())
print(book2.get_info())
print(book3.get_info())

print("\n===借阅操作===")
# 借阅图书
book1.borrow("张小明")
book2.borrow("李小红")
book1.borrow("王小刚")  # 尝试重复借阅

print("\n借阅后状态:")
print(book1.get_info())
print(book2.get_info())

print("\n===归还操作===")
# 归还图书
book1.return_book()
book2.return_book()

print("\n归还后状态:")
print(book1.get_info())
print(book2.get_info())
```

### 代码说明

**案例1代码解释**：
1. `class Student:`：使用class关键字定义学生类
2. `def __init__(self, name, student_id, age):`：定义构造函数，self是必须的第一个参数
3. `self.name = name`：在构造函数中初始化实例属性
4. `student1 = Student("张三", "2023001", 20)`：通过类名加括号创建对象实例

如果把`__init__`写成`init`或`__init`，会导致构造函数不被正确识别，创建对象时不会自动调用初始化代码。

**案例2代码解释**：
1. `self.is_borrowed = False`：定义图书的借阅状态属性
2. `def borrow(self, borrower_name):`：定义实例方法，第一个参数必须是self
3. `book1 = Book("Python编程入门", "张三", "978-7-111-12345-6", 59.8)`：创建图书对象
4. `book1.borrow("张小明")`：调用对象的方法

如果在调用方法时忘记写括号，如`book1.borrow`而不是`book1.borrow("张小明")`，这会返回方法对象而不是执行方法。

## 2. 实例属性和类属性

### 知识点解析

**概念定义**：实例属性就像每个人独有的特征（如身高、体重），每个对象都有自己独立的副本；类属性就像群体共有的特征（如人类都有两只眼睛），所有对象共享同一个值。

**核心规则**：
1. 实例属性在`__init__`方法中定义，使用`self.属性名`的形式
2. 类属性在类体中直接定义，不属于任何方法
3. 实例属性每个对象独立拥有，类属性所有对象共享
4. 通过`实例名.属性名`访问实例属性，通过`类名.属性名`或`实例名.属性名`访问类属性

**常见易错点**：
1. 在类体中错误地定义实例属性
2. 混淆实例属性和类属性的访问方式
3. 意外修改类属性影响所有实例
4. 在实例方法中错误地修改类属性

### 实战案例

#### 案例1：员工管理系统
```python
# 员工管理系统
print("===员工管理系统===")

# 定义员工类
class Employee:
    """员工类"""
    
    # 类属性 - 所有员工共享
    company_name = "科技有限公司"  # 公司名称
    employee_count = 0            # 员工总数
    
    def __init__(self, name, position, salary):
        """
        初始化员工对象
        
        参数:
            name (str): 员工姓名
            position (str): 职位
            salary (float): 薪资
        """
        # 实例属性 - 每个员工独有
        self.name = name          # 员工姓名
        self.position = position  # 职位
        self.salary = salary      # 薪资
        
        # 每创建一个员工，员工总数加1
        Employee.employee_count += 1
        self.employee_id = Employee.employee_count  # 员工编号
    
    def get_info(self):
        """获取员工信息"""
        return f"ID: {self.employee_id}, 姓名: {self.name}, 职位: {self.position}, 薪资: {self.salary}元"
    
    @classmethod
    def get_company_info(cls):
        """获取公司信息（类方法）"""
        return f"公司名称: {cls.company_name}, 员工总数: {cls.employee_count}"
    
    def work(self):
        """工作方法"""
        return f"{self.name}正在工作"

# 创建员工对象
print("创建员工:")
emp1 = Employee("张三", "程序员", 12000)
print(emp1.get_info())

emp2 = Employee("李四", "设计师", 10000)
print(emp2.get_info())

emp3 = Employee("王五", "产品经理", 15000)
print(emp3.get_info())

# 查看公司信息
print(f"\n{Employee.get_company_info()}")

# 修改类属性
print("\n公司更名:")
Employee.company_name = "创新科技有限公司"
print(f"{Employee.get_company_info()}")

# 每个员工的公司名称都变了
print(f"员工1的公司: {emp1.company_name}")
print(f"员工2的公司: {emp2.company_name}")
print(f"员工3的公司: {emp3.company_name}")
```

#### 案例2：银行账户系统
```python
# 银行账户系统
print("\n===银行账户系统===")

# 定义银行账户类
class BankAccount:
    """银行账户类"""
    
    # 类属性
    bank_name = "Python银行"  # 银行名称
    interest_rate = 0.03      # 年利率
    total_accounts = 0        # 账户总数
    
    def __init__(self, account_holder, initial_balance=0):
        """
        初始化银行账户
        
        参数:
            account_holder (str): 账户持有人
            initial_balance (float): 初始余额，默认为0
        """
        # 实例属性
        self.account_holder = account_holder  # 账户持有人
        self.balance = initial_balance        # 账户余额
        self.transaction_history = []         # 交易历史
        
        # 增加账户总数
        BankAccount.total_accounts += 1
        self.account_number = f"ACC{BankAccount.total_accounts:06d}"  # 账户号码
    
    def deposit(self, amount):
        """
        存款
        
        参数:
            amount (float): 存款金额
            
        返回:
            bool: 操作是否成功
        """
        if amount > 0:
            self.balance += amount
            self.transaction_history.append(f"存款 +{amount}元")
            print(f"{self.account_holder}存款{amount}元成功，当前余额{self.balance}元")
            return True
        else:
            print("存款金额必须大于0")
            return False
    
    def withdraw(self, amount):
        """
        取款
        
        参数:
            amount (float): 取款金额
            
        返回:
            bool: 操作是否成功
        """
        if amount <= 0:
            print("取款金额必须大于0")
            return False
        elif amount > self.balance:
            print("余额不足")
            return False
        else:
            self.balance -= amount
            self.transaction_history.append(f"取款 -{amount}元")
            print(f"{self.account_holder}取款{amount}元成功，当前余额{self.balance}元")
            return True
    
    def get_balance(self):
        """查询余额"""
        return self.balance
    
    def calculate_interest(self):
        """计算利息（类属性的使用示例）"""
        interest = self.balance * BankAccount.interest_rate
        return interest
    
    @classmethod
    def change_interest_rate(cls, new_rate):
        """
        修改利率（类方法）
        
        参数:
            new_rate (float): 新利率
        """
        old_rate = cls.interest_rate
        cls.interest_rate = new_rate
        print(f"利率从{old_rate:.2%}调整为{new_rate:.2%}")
    
    def print_statement(self):
        """打印账户明细"""
        print(f"\n=== 账户明细 ===")
        print(f"银行: {self.bank_name}")
        print(f"账户号码: {self.account_number}")
        print(f"账户持有人: {self.account_holder}")
        print(f"当前余额: {self.balance}元")
        print(f"年利率: {BankAccount.interest_rate:.2%}")
        print(f"预计年利息: {self.calculate_interest():.2f}元")
        if self.transaction_history:
            print("交易历史:")
            for transaction in self.transaction_history[-5:]:  # 只显示最近5笔交易
                print(f"  {transaction}")

# 创建银行账户
print("创建银行账户:")
account1 = BankAccount("张三", 1000)
account2 = BankAccount("李四", 5000)

# 查看账户信息
account1.print_statement()
account2.print_statement()

# 进行交易
print("\n===进行交易===")
account1.deposit(500)
account1.withdraw(200)
account2.deposit(1000)
account2.withdraw(3000)

# 查看更新后的账户信息
print("\n交易后账户信息:")
account1.print_statement()
account2.print_statement()

# 修改利率
print("\n===修改利率===")
print(f"修改前利率: {BankAccount.interest_rate:.2%}")
BankAccount.change_interest_rate(0.05)  # 调整为5%
print(f"修改后利率: {BankAccount.interest_rate:.2%}")

# 查看利率调整后的账户信息
print("\n利率调整后账户信息:")
account1.print_statement()
account2.print_statement()

# 查看银行统计信息
print(f"\n银行统计信息:")
print(f"银行名称: {BankAccount.bank_name}")
print(f"总账户数: {BankAccount.total_accounts}")
```

### 代码说明

**案例1代码解释**：
1. `company_name = "科技有限公司"`：类属性，在类体中直接定义
2. `self.name = name`：实例属性，在`__init__`方法中定义
3. `Employee.employee_count += 1`：在构造函数中修改类属性
4. `Employee.get_company_info()`：通过类名调用类方法

如果在实例方法中写`self.company_name = "新公司"`，这会为该实例创建一个同名的实例属性，而不是修改类属性，其他实例仍会使用原来的类属性。

**案例2代码解释**：
1. `interest_rate = 0.03`：类属性，所有账户共享相同的利率
2. `self.balance = initial_balance`：实例属性，每个账户有独立的余额
3. `BankAccount.total_accounts += 1`：通过类名修改类属性
4. `self.account_number = f"ACC{BankAccount.total_accounts:06d}"`：使用类属性生成账户号码

如果将`BankAccount.interest_rate`写成`self.interest_rate`，在修改利率时会为当前实例创建实例属性，而不是修改所有账户共享的类属性。

## 3. 实例方法、类方法和静态方法

### 知识点解析

**概念定义**：实例方法就像每个人都能做的个人动作（如吃饭、睡觉）；类方法就像群体共同的行为（如人类繁衍）；静态方法就像与类相关但不需要特定对象的工具函数（如计算工具）。

**核心规则**：
1. 实例方法第一个参数是`self`，代表实例本身
2. 类方法使用`@classmethod`装饰器，第一个参数是`cls`，代表类本身
3. 静态方法使用`@staticmethod`装饰器，没有特殊参数
4. 实例方法通过实例调用，类方法和静态方法可以通过类或实例调用

**常见易错点**：
1. 忘记在实例方法中写`self`参数
2. 混淆类方法和静态方法的用途
3. 在类方法中错误地使用`self`而不是`cls`
4. 在静态方法中试图访问实例或类属性

### 实战案例

#### 案例1：数学工具类
```python
# 数学工具类
print("===数学工具类===")

import math

class MathUtils:
    """数学工具类"""
    
    # 类属性
    pi = 3.141592653589793
    e = 2.718281828459045
    
    def __init__(self, precision=2):
        """
        初始化数学工具
        
        参数:
            precision (int): 计算精度（小数点后位数）
        """
        self.precision = precision  # 实例属性：精度
    
    # 实例方法
    def round_result(self, number):
        """
        四舍五入结果（实例方法）
        
        参数:
            number (float): 要四舍五入的数字
            
        返回:
            float: 四舍五入后的结果
        """
        return round(number, self.precision)
    
    def power(self, base, exponent):
        """
        幂运算（实例方法）
        
        参数:
            base (float): 底数
            exponent (float): 指数
            
        返回:
            float: 幂运算结果
        """
        result = base ** exponent
        return self.round_result(result)
    
    # 类方法
    @classmethod
    def circle_area(cls, radius):
        """
        计算圆面积（类方法）
        
        参数:
            radius (float): 半径
            
        返回:
            float: 圆面积
        """
        area = cls.pi * radius ** 2
        return area
    
    @classmethod
    def get_constants(cls):
        """
        获取数学常数（类方法）
        
        返回:
            dict: 包含数学常数的字典
        """
        return {
            "pi": cls.pi,
            "e": cls.e
        }
    
    # 静态方法
    @staticmethod
    def is_even(number):
        """
        判断是否为偶数（静态方法）
        
        参数:
            number (int): 要判断的数字
            
        返回:
            bool: 是否为偶数
        """
        return number % 2 == 0
    
    @staticmethod
    def gcd(a, b):
        """
        计算最大公约数（静态方法）
        
        参数:
            a (int): 第一个数
            b (int): 第二个数
            
        返回:
            int: 最大公约数
        """
        while b:
            a, b = b, a % b
        return a
    
    @staticmethod
    def factorial(n):
        """
        计算阶乘（静态方法）
        
        参数:
            n (int): 要计算阶乘的数
            
        返回:
            int: 阶乘结果
        """
        if n <= 1:
            return 1
        result = 1
        for i in range(2, n + 1):
            result *= i
        return result

# 使用实例方法
print("===实例方法===")
math_utils = MathUtils(3)  # 精度为3位小数
print(f"2的3.5次方: {math_utils.power(2, 3.5)}")
print(f"四舍五入π: {math_utils.round_result(math_utils.pi)}")

# 使用类方法
print("\n===类方法===")
radius = 5
area = MathUtils.circle_area(radius)
print(f"半径为{radius}的圆面积: {area:.2f}")

constants = MathUtils.get_constants()
print(f"数学常数: π={constants['pi']:.6f}, e={constants['e']:.6f}")

# 使用静态方法
print("\n===静态方法===")
number = 15
print(f"{number}是偶数吗? {MathUtils.is_even(number)}")

a, b = 48, 18
print(f"{a}和{b}的最大公约数: {MathUtils.gcd(a, b)}")

n = 5
print(f"{n}的阶乘: {MathUtils.factorial(n)}")

# 演示方法调用方式
print("\n===方法调用方式===")
# 实例方法只能通过实例调用
# MathUtils.power(2, 3)  # 这会报错

# 类方法和静态方法可以通过类或实例调用
print(f"通过类调用圆面积: {MathUtils.circle_area(3):.2f}")
print(f"通过实例调用圆面积: {math_utils.circle_area(3):.2f}")

print(f"通过类调用判断偶数: {MathUtils.is_even(4)}")
print(f"通过实例调用判断偶数: {math_utils.is_even(4)}")
```

#### 案例2：日期时间工具类
```python
# 日期时间工具类
print("\n===日期时间工具类===")

from datetime import datetime, timedelta

class DateTimeUtils:
    """日期时间工具类"""
    
    # 类属性
    work_hours_start = 9   # 工作时间开始（小时）
    work_hours_end = 18    # 工作时间结束（小时）
    
    def __init__(self, timezone_offset=0):
        """
        初始化日期时间工具
        
        参数:
            timezone_offset (int): 时区偏移（小时）
        """
        self.timezone_offset = timezone_offset  # 实例属性：时区偏移
    
    # 实例方法
    def get_current_time(self):
        """
        获取当前时间（考虑时区）
        
        返回:
            datetime: 当前时间
        """
        current_time = datetime.now()
        if self.timezone_offset != 0:
            current_time += timedelta(hours=self.timezone_offset)
        return current_time
    
    def format_time(self, dt, format_string="%Y-%m-%d %H:%M:%S"):
        """
        格式化时间
        
        参数:
            dt (datetime): 要格式化的时间
            format_string (str): 格式字符串
            
        返回:
            str: 格式化后的时间字符串
        """
        return dt.strftime(format_string)
    
    def is_work_time(self, dt=None):
        """
        判断是否为工作时间
        
        参数:
            dt (datetime): 要判断的时间，默认为当前时间
            
        返回:
            bool: 是否为工作时间
        """
        if dt is None:
            dt = self.get_current_time()
        hour = dt.hour
        return self.work_hours_start <= hour < self.work_hours_end
    
    # 类方法
    @classmethod
    def get_weekday_name(cls, date=None):
        """
        获取星期名称（类方法）
        
        参数:
            date (datetime): 日期，默认为今天
            
        返回:
            str: 星期名称
        """
        if date is None:
            date = datetime.now()
        weekdays = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"]
        return weekdays[date.weekday()]
    
    @classmethod
    def is_leap_year(cls, year):
        """
        判断是否为闰年（类方法）
        
        参数:
            year (int): 年份
            
        返回:
            bool: 是否为闰年
        """
        return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)
    
    # 静态方法
    @staticmethod
    def days_between(date1, date2):
        """
        计算两个日期之间的天数差（静态方法）
        
        参数:
            date1 (datetime): 第一个日期
            date2 (datetime): 第二个日期
            
        返回:
            int: 天数差（绝对值）
        """
        delta = date2 - date1
        return abs(delta.days)
    
    @staticmethod
    def add_days(date, days):
        """
        给日期添加天数（静态方法）
        
        参数:
            date (datetime): 原日期
            days (int): 要添加的天数
            
        返回:
            datetime: 新日期
        """
        return date + timedelta(days=days)

# 使用实例方法
print("===实例方法===")
# 创建不同时区的工具实例
local_time = DateTimeUtils()  # 本地时间
eastern_time = DateTimeUtils(5)  # 东五区时间
western_time = DateTimeUtils(-8)  # 西八区时间

print(f"本地时间: {local_time.format_time(local_time.get_current_time())}")
print(f"东五区时间: {eastern_time.format_time(eastern_time.get_current_time())}")
print(f"西八区时间: {western_time.format_time(western_time.get_current_time())}")

print(f"本地是否为工作时间: {local_time.is_work_time()}")

# 使用类方法
print("\n===类方法===")
today = datetime.now()
print(f"今天是: {DateTimeUtils.get_weekday_name(today)}")

year = 2024
print(f"{year}年是闰年吗? {DateTimeUtils.is_leap_year(year)}")

# 使用静态方法
print("\n===静态方法===")
date1 = datetime(2023, 1, 1)
date2 = datetime(2023, 12, 31)
days_diff = DateTimeUtils.days_between(date1, date2)
print(f"2023年1月1日到12月31日相差 {days_diff} 天")

future_date = DateTimeUtils.add_days(today, 100)
print(f"100天后的日期: {future_date.strftime('%Y-%m-%d')}")

# 综合示例
print("\n===综合示例===")
# 创建一个项目管理时间工具
project_time = DateTimeUtils()

# 获取当前时间
current_time = project_time.get_current_time()
print(f"项目开始时间: {project_time.format_time(current_time)}")

# 判断是否为工作时间
if project_time.is_work_time():
    print("现在是工作时间，可以开始工作")
else:
    print("现在是非工作时间")

# 计算项目结束时间（30天后）
end_time = DateTimeUtils.add_days(current_time, 30)
print(f"项目预计结束时间: {project_time.format_time(end_time, '%Y年%m月%d日')}")

# 计算项目持续天数
duration = DateTimeUtils.days_between(current_time, end_time)
print(f"项目持续天数: {duration} 天")

# 判断结束日期是星期几
end_weekday = DateTimeUtils.get_weekday_name(end_time)
print(f"项目结束日是: {end_weekday}")
```

### 代码说明

**案例1代码解释**：
1. `def power(self, base, exponent):`：实例方法，需要访问实例属性`self.precision`
2. `@classmethod def circle_area(cls, radius):`：类方法，使用`cls.pi`访问类属性
3. `@staticmethod def is_even(number):`：静态方法，不访问任何实例或类属性
4. `math_utils.power(2, 3.5)`：实例方法必须通过实例调用

如果在静态方法中写`self.precision`或`cls.pi`，会报错，因为静态方法没有`self`或`cls`参数。

**案例2代码解释**：
1. `def get_current_time(self):`：实例方法，使用实例属性`self.timezone_offset`
2. `@classmethod def get_weekday_name(cls, date=None):`：类方法，与类相关但不依赖实例
3. `@staticmethod def days_between(date1, date2):`：静态方法，纯粹的工具函数
4. `DateTimeUtils.is_leap_year(2024)`：类方法可以通过类名直接调用

如果把`is_leap_year`设计为实例方法，就需要先创建实例才能调用，这不符合逻辑，因为闰年判断与具体的时区实例无关。

## 4. 封装和访问控制

### 知识点解析

**概念定义**：封装就像保险箱，把重要的东西（数据）放在里面，只通过特定的接口（方法）来操作。访问控制就像设置不同级别的权限，有些东西任何人都可以看（公有），有些只限内部使用（受保护），有些则是绝对私密的（私有）。

**核心规则**：
1. 公有成员：正常命名，可以随意访问
2. 受保护成员：单下划线前缀（_），约定为内部使用
3. 私有成员：双下划线前缀（__），名称会被改写
4. 通过属性和方法提供安全的数据访问接口

**常见易错点**：
1. 过度使用私有成员，导致子类无法继承
2. 忘记提供必要的访问接口
3. 混淆受保护成员和私有成员的命名规则
4. 错误地认为私有成员完全无法访问

### 实战案例

#### 案例1：游戏角色类
```python
# 游戏角色类
print("===游戏角色类===")

class GameCharacter:
    """游戏角色类"""
    
    def __init__(self, name, max_health=100):
        """
        初始化游戏角色
        
        参数:
            name (str): 角色名称
            max_health (int): 最大生命值
        """
        # 公有属性
        self.name = name                    # 角色名称
        
        # 受保护属性（约定为内部使用）
        self._level = 1                     # 等级
        self._experience = 0                # 经验值
        self._max_health = max_health       # 最大生命值
        
        # 私有属性（名称改写）
        self.__health = max_health          # 当前生命值
        self.__attack_power = 10            # 攻击力
        self.__defense = 5                  # 防御力
        self.__is_alive = True              # 是否存活
    
    # 公有方法
    def attack(self, target):
        """
        攻击目标
        
        参数:
            target (GameCharacter): 攻击目标
        """
        if not self.__is_alive:
            print(f"{self.name}已经死亡，无法攻击")
            return
        
        if not target.__is_alive:
            print(f"{target.name}已经死亡")
            return
        
        damage = max(1, self.__attack_power - target.__defense)
        print(f"{self.name}攻击{target.name}，造成{damage}点伤害")
        target.__take_damage(damage)
    
    def get_status(self):
        """获取角色状态"""
        status = "存活" if self.__is_alive else "死亡"
        return f"{self.name} (等级: {self._level}, 生命值: {self.__health}/{self._max_health}, 状态: {status})"
    
    # 受保护方法（约定为内部使用）
    def _gain_experience(self, exp):
        """
        获得经验值（受保护方法）
        
        参数:
            exp (int): 获得的经验值
        """
        self._experience += exp
        print(f"{self.name}获得了{exp}点经验值")
        
        # 检查是否升级
        required_exp = self._level * 100
        if self._experience >= required_exp:
            self._level_up()
    
    def _level_up(self):
        """升级（受保护方法）"""
        self._level += 1
        self._experience = 0
        self._max_health += 20
        self.__health = self._max_health  # 回满血
        self.__attack_power += 5
        self.__defense += 2
        print(f"{self.name}升级到{self._level}级！属性提升！")
    
    # 私有方法
    def __take_damage(self, damage):
        """
        承受伤害（私有方法）
        
        参数:
            damage (int): 伤害值
        """
        self.__health = max(0, self.__health - damage)
        print(f"{self.name}剩余生命值: {self.__health}")
        
        if self.__health == 0:
            self.__is_alive = False
            print(f"{self.name}死亡了！")
    
    def __regenerate_health(self):
        """恢复生命值（私有方法）"""
        if self.__is_alive:
            heal_amount = self._max_health // 10
            self.__health = min(self._max_health, self.__health + heal_amount)
            print(f"{self.name}恢复了{heal_amount}点生命值")

# 创建游戏角色
print("创建游戏角色:")
hero = GameCharacter("勇士", 150)
monster = GameCharacter("哥布林", 80)

# 查看初始状态
print("\n初始状态:")
print(hero.get_status())
print(monster.get_status())

# 进行战斗
print("\n===战斗开始===")
hero.attack(monster)
monster.attack(hero)
hero.attack(monster)
hero.attack(monster)  # 最后一击

# 检查战斗后状态
print("\n战斗后状态:")
print(hero.get_status())
print(monster.get_status())

# 演示访问控制
print("\n===访问控制演示===")
# 公有属性可以直接访问
print(f"角色名称: {hero.name}")

# 受保护属性可以访问，但不建议（约定为内部使用）
print(f"角色等级: {hero._level}")

# 私有属性无法直接访问
try:
    print(f"角色生命值: {hero.__health}")  # 这会报错
except AttributeError as e:
    print(f"错误: {e}")

# 但可以通过名称改写访问私有属性（不推荐）
print(f"通过名称改写访问生命值: {hero._GameCharacter__health}")

# 私有方法无法直接调用
try:
    hero.__take_damage(10)  # 这会报错
except AttributeError as e:
    print(f"错误: {e}")

# 但同样可以通过名称改写调用（不推荐）
# hero._GameCharacter__take_damage(10)
```

#### 案例2：银行账户安全系统
```python
# 银行账户安全系统
print("\n===银行账户安全系统===")

class SecureBankAccount:
    """安全银行账户类"""
    
    def __init__(self, account_holder, initial_balance=0, pin="1234"):
        """
        初始化安全银行账户
        
        参数:
            account_holder (str): 账户持有人
            initial_balance (float): 初始余额
            pin (str): PIN码
        """
        # 公有属性
        self.account_holder = account_holder  # 账户持有人
        
        # 受保护属性
        self._account_number = self._generate_account_number()  # 账户号码
        self._balance = initial_balance  # 余额
        self._transaction_history = []   # 交易历史
        
        # 私有属性
        self.__pin = pin                 # PIN码
        self.__failed_attempts = 0       # 失败尝试次数
        self.__is_locked = False         # 是否被锁定
        self.__security_questions = {}   # 安全问题
    
    # 公有方法
    def deposit(self, amount, pin):
        """
        存款
        
        参数:
            amount (float): 存款金额
            pin (str): PIN码
            
        返回:
            bool: 操作是否成功
        """
        if not self._verify_pin(pin):
            return False
        
        if self.__is_locked:
            print("账户已被锁定，请联系银行")
            return False
        
        if amount <= 0:
            print("存款金额必须大于0")
            return False
        
        self._balance += amount
        self._transaction_history.append(f"存款 +{amount}元")
        print(f"存款成功，当前余额: {self._balance}元")
        return True
    
    def withdraw(self, amount, pin):
        """
        取款
        
        参数:
            amount (float): 取款金额
            pin (str): PIN码
            
        返回:
            bool: 操作是否成功
        """
        if not self._verify_pin(pin):
            return False
        
        if self.__is_locked:
            print("账户已被锁定，请联系银行")
            return False
        
        if amount <= 0:
            print("取款金额必须大于0")
            return False
        
        if amount > self._balance:
            print("余额不足")
            return False
        
        self._balance -= amount
        self._transaction_history.append(f"取款 -{amount}元")
        print(f"取款成功，当前余额: {self._balance}元")
        return True
    
    def get_balance(self, pin):
        """
        查询余额
        
        参数:
            pin (str): PIN码
            
        返回:
            float or None: 余额或None（验证失败）
        """
        if not self._verify_pin(pin):
            return None
        
        if self.__is_locked:
            print("账户已被锁定，请联系银行")
            return None
        
        return self._balance
    
    def set_security_question(self, question, answer, pin):
        """
        设置安全问题
        
        参数:
            question (str): 问题
            answer (str): 答案
            pin (str): PIN码
        """
        if not self._verify_pin(pin):
            return False
        
        self.__security_questions[question] = answer
        print("安全问题设置成功")
        return True
    
    def change_pin(self, old_pin, new_pin):
        """
        修改PIN码
        
        参数:
            old_pin (str): 旧PIN码
            new_pin (str): 新PIN码
            
        返回:
            bool: 操作是否成功
        """
        if not self._verify_pin(old_pin):
            return False
        
        if len(new_pin) != 4 or not new_pin.isdigit():
            print("PIN码必须是4位数字")
            return False
        
        self.__pin = new_pin
        print("PIN码修改成功")
        return True
    
    def print_statement(self, pin):
        """
        打印账户明细
        
        参数:
            pin (str): PIN码
        """
        if not self._verify_pin(pin):
            return False
        
        if self.__is_locked:
            print("账户已被锁定，请联系银行")
            return False
        
        print(f"\n=== 账户明细 ===")
        print(f"账户持有人: {self.account_holder}")
        print(f"账户号码: {self._account_number}")
        print(f"当前余额: {self._balance}元")
        print("最近交易记录:")
        for transaction in self._transaction_history[-5:]:  # 显示最近5笔交易
            print(f"  {transaction}")
        return True
    
    # 受保护方法
    def _generate_account_number(self):
        """生成账户号码（受保护方法）"""
        import random
        return f"ACC{random.randint(100000, 999999)}"
    
    def _log_transaction(self, transaction):
        """
        记录交易（受保护方法）
        
        参数:
            transaction (str): 交易记录
        """
        self._transaction_history.append(transaction)
        if len(self._transaction_history) > 100:  # 限制历史记录数量
            self._transaction_history.pop(0)
    
    # 私有方法
    def __verify_pin_internal(self, pin):
        """
        验证PIN码（私有方法）
        
        参数:
            pin (str): PIN码
            
        返回:
            bool: 验证是否成功
        """
        if self.__is_locked:
            return False
        
        if pin == self.__pin:
            self.__failed_attempts = 0  # 重置失败次数
            return True
        else:
            self.__failed_attempts += 1
            print(f"PIN码错误，还有{3 - self.__failed_attempts}次机会")
            
            if self.__failed_attempts >= 3:
                self.__is_locked = True
                print("账户已被锁定，请联系银行")
            
            return False
    
    # 公有包装方法，用于调用私有验证方法
    def _verify_pin(self, pin):
        """
        验证PIN码（受保护方法，供内部调用）
        
        参数:
            pin (str): PIN码
            
        返回:
            bool: 验证是否成功
        """
        return self.__verify_pin_internal(pin)

# 使用安全银行账户
print("创建安全银行账户:")
account = SecureBankAccount("张三", 1000, "1234")

# 正常操作
print("\n===正常操作===")
account.deposit(500, "1234")
account.withdraw(200, "1234")
print(f"余额查询: {account.get_balance('1234')}元")
account.print_statement("1234")

# 设置安全问题
print("\n===设置安全问题===")
account.set_security_question("你的第一只宠物叫什么？", "小白", "1234")
account.set_security_question("你最喜欢的颜色是什么？", "蓝色", "1234")

# 修改PIN码
print("\n===修改PIN码===")
account.change_pin("1234", "5678")

# 使用新PIN码
print("\n===使用新PIN码===")
account.deposit(300, "5678")
print(f"余额查询: {account.get_balance('5678')}元")

# PIN码错误尝试
print("\n===PIN码错误尝试===")
account.withdraw(100, "0000")  # 错误PIN码
account.withdraw(100, "1111")  # 错误PIN码
account.withdraw(100, "2222")  # 错误PIN码，账户将被锁定

# 尝试在锁定状态下操作
print("\n===账户锁定后尝试操作===")
account.deposit(100, "5678")  # 即使是正确PIN码也无法操作

# 演示访问控制
print("\n===访问控制演示===")
# 公有属性可以直接访问
print(f"账户持有人: {account.account_holder}")

# 受保护属性可以访问，但不建议
print(f"账户号码: {account._account_number}")

# 私有属性无法直接访问
try:
    print(f"PIN码: {account.__pin}")  # 这会报错
except AttributeError as e:
    print(f"错误: 无法直接访问私有属性")

# 通过名称改写访问私有属性（强烈不推荐）
print(f"通过名称改写访问PIN码: {account._SecureBankAccount__pin}")

# 私有方法无法直接调用
try:
    account.__verify_pin_internal("1234")  # 这会报错
except AttributeError as e:
    print(f"错误: 无法直接调用私有方法")
```

### 代码说明

**案例1代码解释**：
1. `self.name`：公有属性，可以直接访问
2. `self._level`：受保护属性，约定为内部使用
3. `self.__health`：私有属性，名称会被改写为`_GameCharacter__health`
4. `def __take_damage(self, damage):`：私有方法，名称会被改写

如果在类外部写`hero.__health = 100`，这不会修改真正的私有属性，而是创建了一个新的公有属性`__health`。

**案例2代码解释**：
1. `self.account_holder`：公有属性
2. `self._balance`：受保护属性，用于存储余额
3. `self.__pin`：私有属性，存储敏感的PIN码
4. `def __verify_pin_internal(self, pin):`：私有方法，用于验证PIN码

如果把`__pin`设计为受保护属性`_pin`，虽然可以正常工作，但安全性降低，因为外部代码可能会意外修改PIN码。

## 5. 继承和多态

### 知识点解析

**概念定义**：继承就像子女继承父母的特征，子类可以拥有父类的属性和方法；多态就像同一种行为在不同对象上表现出不同的效果，比如同样是"叫"，狗会"汪汪"，猫会"喵喵"。

**核心规则**：
1. 使用`class 子类名(父类名):`语法实现继承
2. 使用`super()`调用父类的方法
3. 子类可以重写父类的方法
4. 多态允许不同类的对象对同一消息做出不同的响应

**常见易错点**：
1. 忘记调用父类的`__init__`方法
2. 在重写方法时忘记调用父类的同名方法
3. 混淆方法重写和方法重载的概念
4. 不理解多态的实际应用场景

### 实战案例

#### 案例1：媒体播放器系统
```python
# 媒体播放器系统
print("===媒体播放器系统===")

# 基类：媒体
class Media:
    """媒体基类"""
    
    def __init__(self, title, duration):
        """
        初始化媒体对象
        
        参数:
            title (str): 标题
            duration (int): 时长（秒）
        """
        self.title = title
        self.duration = duration
        self.is_playing = False
    
    def play(self):
        """播放媒体"""
        if not self.is_playing:
            self.is_playing = True
            print(f"开始播放: {self.title}")
        else:
            print(f"{self.title}已经在播放中")
    
    def pause(self):
        """暂停媒体"""
        if self.is_playing:
            self.is_playing = False
            print(f"暂停播放: {self.title}")
        else:
            print(f"{self.title}未在播放")
    
    def stop(self):
        """停止媒体"""
        self.is_playing = False
        print(f"停止播放: {self.title}")
    
    def get_info(self):
        """获取媒体信息"""
        minutes, seconds = divmod(self.duration, 60)
        return f"标题: {self.title}, 时长: {minutes:02d}:{seconds:02d}"

# 子类：音乐
class Music(Media):
    """音乐类"""
    
    def __init__(self, title, duration, artist, album):
        """
        初始化音乐对象
        
        参数:
            title (str): 歌曲名
            duration (int): 时长（秒）
            artist (str): 艺术家
            album (str): 专辑
        """
        super().__init__(title, duration)  # 调用父类构造方法
        self.artist = artist
        self.album = album
    
    def play(self):
        """重写播放方法"""
        super().play()  # 调用父类方法
        print(f"艺术家: {self.artist}, 专辑: {self.album}")
    
    def get_info(self):
        """重写获取信息方法"""
        base_info = super().get_info()
        return f"{base_info}, 艺术家: {self.artist}, 专辑: {self.album}"

# 子类：视频
class Video(Media):
    """视频类"""
    
    def __init__(self, title, duration, director, resolution):
        """
        初始化视频对象
        
        参数:
            title (str): 视频标题
            duration (int): 时长（秒）
            director (str): 导演
            resolution (str): 分辨率
        """
        super().__init__(title, duration)  # 调用父类构造方法
        self.director = director
        self.resolution = resolution
    
    def play(self):
        """重写播放方法"""
        super().play()  # 调用父类方法
        print(f"导演: {self.director}, 分辨率: {self.resolution}")
    
    def get_info(self):
        """重写获取信息方法"""
        base_info = super().get_info()
        return f"{base_info}, 导演: {self.director}, 分辨率: {self.resolution}"

# 子类：播客
class Podcast(Media):
    """播客类"""
    
    def __init__(self, title, duration, host, episode):
        """
        初始化播客对象
        
        参数:
            title (str): 播客标题
            duration (int): 时长（秒）
            host (str): 主持人
            episode (int): 期数
        """
        super().__init__(title, duration)  # 调用父类构造方法
        self.host = host
        self.episode = episode
    
    def play(self):
        """重写播放方法"""
        super().play()  # 调用父类方法
        print(f"主持人: {self.host}, 第{self.episode}期")
    
    def get_info(self):
        """重写获取信息方法"""
        base_info = super().get_info()
        return f"{base_info}, 主持人: {self.host}, 期数: {self.episode}"

# 使用继承和多态
print("创建媒体对象:")
song = Music("夜曲", 240, "周杰伦", "十一月的萧邦")
movie = Video("阿凡达", 9300, "詹姆斯·卡梅隆", "1080p")
podcast = Podcast("代码时间", 3600, "技术播客", 123)

# 演示多态
print("\n===多态演示===")
media_list = [song, movie, podcast]

for media in media_list:
    print(f"\n{media.get_info()}")
    media.play()
    media.pause()
    media.stop()

# 演示继承
print("\n===继承演示===")
print("音乐信息:")
print(song.get_info())

print("\n视频信息:")
print(movie.get_info())

print("\n播客信息:")
print(podcast.get_info())
```

#### 案例2：图形绘制系统
```python
# 图形绘制系统
print("\n===图形绘制系统===")

import math

# 基类：图形
class Shape:
    """图形基类"""
    
    def __init__(self, color="黑色"):
        """
        初始化图形
        
        参数:
            color (str): 颜色
        """
        self.color = color
    
    def area(self):
        """计算面积（抽象方法）"""
        raise NotImplementedError("子类必须实现area方法")
    
    def perimeter(self):
        """计算周长（抽象方法）"""
        raise NotImplementedError("子类必须实现perimeter方法")
    
    def draw(self):
        """绘制图形"""
        print(f"用{self.color}颜色绘制图形")
    
    def get_info(self):
        """获取图形信息"""
        return f"颜色: {self.color}"

# 子类：矩形
class Rectangle(Shape):
    """矩形类"""
    
    def __init__(self, width, height, color="黑色"):
        """
        初始化矩形
        
        参数:
            width (float): 宽度
            height (float): 高度
            color (str): 颜色
        """
        super().__init__(color)
        self.width = width
        self.height = height
    
    def area(self):
        """计算矩形面积"""
        return self.width * self.height
    
    def perimeter(self):
        """计算矩形周长"""
        return 2 * (self.width + self.height)
    
    def draw(self):
        """绘制矩形"""
        super().draw()
        print(f"绘制一个{self.color}的矩形，宽{self.width}，高{self.height}")
    
    def get_info(self):
        """获取矩形信息"""
        base_info = super().get_info()
        return f"{base_info}, 形状: 矩形, 宽: {self.width}, 高: {self.height}"

# 子类：圆形
class Circle(Shape):
    """圆形类"""
    
    def __init__(self, radius, color="黑色"):
        """
        初始化圆形
        
        参数:
            radius (float): 半径
            color (str): 颜色
        """
        super().__init__(color)
        self.radius = radius
    
    def area(self):
        """计算圆形面积"""
        return math.pi * self.radius ** 2
    
    def perimeter(self):
        """计算圆形周长"""
        return 2 * math.pi * self.radius
    
    def draw(self):
        """绘制圆形"""
        super().draw()
        print(f"绘制一个{self.color}的圆形，半径{self.radius}")
    
    def get_info(self):
        """获取圆形信息"""
        base_info = super().get_info()
        return f"{base_info}, 形状: 圆形, 半径: {self.radius}"

# 子类：三角形
class Triangle(Shape):
    """三角形类"""
    
    def __init__(self, a, b, c, color="黑色"):
        """
        初始化三角形
        
        参数:
            a (float): 边长a
            b (float): 边长b
            c (float): 边长c
            color (str): 颜色
        """
        super().__init__(color)
        self.a = a
        self.b = b
        self.c = c
        
        # 验证三角形合法性
        if not self._is_valid():
            raise ValueError("无效的三角形边长")
    
    def _is_valid(self):
        """验证三角形是否合法"""
        return (self.a + self.b > self.c and 
                self.a + self.c > self.b and 
                self.b + self.c > self.a)
    
    def area(self):
        """计算三角形面积（海伦公式）"""
        s = self.perimeter() / 2
        return math.sqrt(s * (s - self.a) * (s - self.b) * (s - self.c))
    
    def perimeter(self):
        """计算三角形周长"""
        return self.a + self.b + self.c
    
    def draw(self):
        """绘制三角形"""
        super().draw()
        print(f"绘制一个{self.color}的三角形，边长分别为{self.a}, {self.b}, {self.c}")
    
    def get_info(self):
        """获取三角形信息"""
        base_info = super().get_info()
        return f"{base_info}, 形状: 三角形, 边长: {self.a}, {self.b}, {self.c}"

# 图形管理器
class ShapeManager:
    """图形管理器"""
    
    def __init__(self):
        self.shapes = []
    
    def add_shape(self, shape):
        """添加图形"""
        self.shapes.append(shape)
        print(f"添加图形: {shape.__class__.__name__}")
    
    def calculate_total_area(self):
        """计算所有图形的总面积"""
        total = 0
        for shape in self.shapes:
            total += shape.area()
        return total
    
    def draw_all_shapes(self):
        """绘制所有图形"""
        print("=== 绘制所有图形 ===")
        for shape in self.shapes:
            shape.draw()
            print()
    
    def get_statistics(self):
        """获取图形统计信息"""
        if not self.shapes:
            return "没有图形"
        
        info = f"总共有{len(self.shapes)}个图形:\n"
        for i, shape in enumerate(self.shapes, 1):
            info += f"  {i}. {shape.get_info()}\n"
            info += f"     面积: {shape.area():.2f}, 周长: {shape.perimeter():.2f}\n"
        
        total_area = self.calculate_total_area()
        info += f"总面积: {total_area:.2f}"
        
        return info

# 使用图形系统
print("创建图形对象:")
rectangle = Rectangle(5, 3, "红色")
circle = Circle(4, "蓝色")
triangle = Triangle(3, 4, 5, "绿色")

# 创建图形管理器
manager = ShapeManager()

# 添加图形
manager.add_shape(rectangle)
manager.add_shape(circle)
manager.add_shape(triangle)

# 显示统计信息
print("\n===图形统计信息===")
print(manager.get_statistics())

# 绘制所有图形
manager.draw_all_shapes()

# 演示多态
print("===多态演示===")
shapes = [rectangle, circle, triangle]

for shape in shapes:
    print(f"\n图形类型: {shape.__class__.__name__}")
    print(f"面积: {shape.area():.2f}")
    print(f"周长: {shape.perimeter():.2f}")
    shape.draw()

# 演示继承
print("\n===继承演示===")
print("矩形信息:")
print(rectangle.get_info())

print("\n圆形信息:")
print(circle.get_info())

print("\n三角形信息:")
print(triangle.get_info())
```

### 代码说明

**案例1代码解释**：
1. `class Music(Media):`：Music类继承自Media类
2. `super().__init__(title, duration)`：调用父类的构造方法
3. `def play(self):`：子类重写父类的方法
4. `super().play()`：在重写方法中调用父类的同名方法

如果在子类的`__init__`方法中忘记调用`super().__init__()`，父类的属性将不会被初始化。

**案例2代码解释**：
1. `class Rectangle(Shape):`：Rectangle类继承自Shape类
2. `raise NotImplementedError("子类必须实现area方法")`：在基类中定义抽象方法
3. 每个子类都必须实现`area`和`perimeter`方法
4. `manager.add_shape(rectangle)`：利用多态，管理器可以接受任何Shape子类的实例

如果子类没有实现父类的抽象方法，当创建子类实例并调用该方法时会抛出NotImplementedError异常。

## 6. 特殊方法和属性装饰器

### 知识点解析

**概念定义**：特殊方法就像Python为类提供的"魔法接口"，让我们可以自定义类在特定情况下的行为，如用加号相加、用print打印等。属性装饰器则让我们可以像访问属性一样使用方法，让代码更加简洁自然。

**核心规则**：
1. 特殊方法以双下划线开头和结尾，如`__str__`、`__add__`
2. 属性装饰器使用`@property`、`@属性名.setter`、`@属性名.deleter`
3. 特殊方法在特定操作时自动调用
4. 属性装饰器让方法可以像属性一样访问

**常见易错点**：
1. 特殊方法名写错，如`__str_`或`_str__`
2. 在属性setter中忘记做数据验证
3. 递归调用属性getter/setter导致无限循环
4. 忘记特殊方法应该返回适当的值

### 实战案例

#### 案例1：复数类
```python
# 复数类
print("===复数类===")

import math

class ComplexNumber:
    """复数类"""
    
    def __init__(self, real=0, imag=0):
        """
        初始化复数
        
        参数:
            real (float): 实部
            imag (float): 虚部
        """
        self.real = real
        self.imag = imag
    
    # 字符串表示
    def __str__(self):
        """字符串表示（用于print）"""
        if self.imag == 0:
            return str(self.real)
        elif self.real == 0:
            return f"{self.imag}i"
        elif self.imag > 0:
            return f"{self.real} + {self.imag}i"
        else:
            return f"{self.real} - {abs(self.imag)}i"
    
    def __repr__(self):
        """开发者字符串表示（用于调试）"""
        return f"ComplexNumber({self.real}, {self.imag})"
    
    # 算术运算
    def __add__(self, other):
        """加法运算"""
        if isinstance(other, ComplexNumber):
            return ComplexNumber(self.real + other.real, self.imag + other.imag)
        elif isinstance(other, (int, float)):
            return ComplexNumber(self.real + other, self.imag)
        return NotImplemented
    
    def __radd__(self, other):
        """右加法运算（当左边不是复数时）"""
        return self.__add__(other)
    
    def __sub__(self, other):
        """减法运算"""
        if isinstance(other, ComplexNumber):
            return ComplexNumber(self.real - other.real, self.imag - other.imag)
        elif isinstance(other, (int, float)):
            return ComplexNumber(self.real - other, self.imag)
        return NotImplemented
    
    def __mul__(self, other):
        """乘法运算"""
        if isinstance(other, ComplexNumber):
            real = self.real * other.real - self.imag * other.imag
            imag = self.real * other.imag + self.imag * other.real
            return ComplexNumber(real, imag)
        elif isinstance(other, (int, float)):
            return ComplexNumber(self.real * other, self.imag * other)
        return NotImplemented
    
    def __rmul__(self, other):
        """右乘法运算"""
        return self.__mul__(other)
    
    def __truediv__(self, other):
        """除法运算"""
        if isinstance(other, ComplexNumber):
            denominator = other.real ** 2 + other.imag ** 2
            if denominator == 0:
                raise ZeroDivisionError("除数不能为零")
            real = (self.real * other.real + self.imag * other.imag) / denominator
            imag = (self.imag * other.real - self.real * other.imag) / denominator
            return ComplexNumber(real, imag)
        elif isinstance(other, (int, float)):
            if other == 0:
                raise ZeroDivisionError("除数不能为零")
            return ComplexNumber(self.real / other, self.imag / other)
        return NotImplemented
    
    # 比较运算
    def __eq__(self, other):
        """相等比较"""
        if isinstance(other, ComplexNumber):
            return self.real == other.real and self.imag == other.imag
        elif isinstance(other, (int, float)):
            return self.real == other and self.imag == 0
        return False
    
    def __ne__(self, other):
        """不等比较"""
        return not self.__eq__(other)
    
    # 其他特殊方法
    def __abs__(self):
        """绝对值（模）"""
        return math.sqrt(self.real ** 2 + self.imag ** 2)
    
    def __neg__(self):
        """负号运算"""
        return ComplexNumber(-self.real, -self.imag)
    
    def __pow__(self, power):
        """幂运算"""
        if isinstance(power, int) and power >= 0:
            result = ComplexNumber(1, 0)
            for _ in range(power):
                result = result * self
            return result
        return NotImplemented
    
    # 属性装饰器
    @property
    def conjugate(self):
        """共轭复数（只读属性）"""
        return ComplexNumber(self.real, -self.imag)
    
    @property
    def modulus(self):
        """模（只读属性）"""
        return abs(self)
    
    @property
    def argument(self):
        """幅角（只读属性）"""
        return math.atan2(self.imag, self.real)

# 使用复数类
print("创建复数:")
c1 = ComplexNumber(3, 4)
c2 = ComplexNumber(1, -2)
c3 = ComplexNumber(5)  # 纯实数

print(f"c1 = {c1}")
print(f"c2 = {c2}")
print(f"c3 = {c3}")

# 算术运算
print("\n===算术运算===")
print(f"c1 + c2 = {c1 + c2}")
print(f"c1 - c2 = {c1 - c2}")
print(f"c1 * c2 = {c1 * c2}")
print(f"c1 / c2 = {c1 / c2}")

# 与数字运算
print(f"c1 + 5 = {c1 + 5}")
print(f"3 * c2 = {3 * c2}")

# 比较运算
print("\n===比较运算===")
print(f"c1 == c2: {c1 == c2}")
print(f"c3 == 5: {c3 == 5}")

# 其他运算
print("\n===其他运算===")
print(f"|c1| = {abs(c1)}")
print(f"-c1 = {-c1}")
print(f"c1^2 = {c1 ** 2}")

# 属性装饰器
print("\n===属性装饰器===")
print(f"c1的共轭: {c1.conjugate}")
print(f"c1的模: {c1.modulus}")
print(f"c1的幅角: {c1.argument:.4f} 弧度")

# 演示特殊方法调用
print("\n===特殊方法调用===")
print("使用str():", str(c1))
print("使用repr():", repr(c1))
print("在列表中:", [c1, c2])
print("在字典中:", {c1: "复数1", c2: "复数2"})
```

#### 案例2：温度转换类
```python
# 温度转换类
print("\n===温度转换类===")

class Temperature:
    """温度类"""
    
    def __init__(self, celsius=0):
        """
        初始化温度
        
        参数:
            celsius (float): 摄氏度
        """
        self._celsius = celsius
    
    # 字符串表示
    def __str__(self):
        """字符串表示"""
        return f"{self.celsius}°C ({self.fahrenheit}°F)"
    
    def __repr__(self):
        """开发者字符串表示"""
        return f"Temperature({self.celsius})"
    
    # 比较运算
    def __eq__(self, other):
        """相等比较"""
        if isinstance(other, Temperature):
            return self.celsius == other.celsius
        return False
    
    def __lt__(self, other):
        """小于比较"""
        if isinstance(other, Temperature):
            return self.celsius < other.celsius
        return NotImplemented
    
    def __le__(self, other):
        """小于等于比较"""
        if isinstance(other, Temperature):
            return self.celsius <= other.celsius
        return NotImplemented
    
    def __gt__(self, other):
        """大于比较"""
        if isinstance(other, Temperature):
            return self.celsius > other.celsius
        return NotImplemented
    
    def __ge__(self, other):
        """大于等于比较"""
        if isinstance(other, Temperature):
            return self.celsius >= other.celsius
        return NotImplemented
    
    # 算术运算
    def __add__(self, other):
        """加法运算"""
        if isinstance(other, Temperature):
            return Temperature(self.celsius + other.celsius)
        elif isinstance(other, (int, float)):
            return Temperature(self.celsius + other)
        return NotImplemented
    
    def __sub__(self, other):
        """减法运算"""
        if isinstance(other, Temperature):
            return Temperature(self.celsius - other.celsius)
        elif isinstance(other, (int, float)):
            return Temperature(self.celsius - other)
        return NotImplemented
    
    # 属性装饰器
    @property
    def celsius(self):
        """摄氏度属性"""
        return self._celsius
    
    @celsius.setter
    def celsius(self, value):
        """摄氏度属性设置器"""
        if value < -273.15:
            raise ValueError("温度不能低于绝对零度(-273.15°C)")
        self._celsius = value
    
    @property
    def fahrenheit(self):
        """华氏度属性"""
        return self.celsius * 9/5 + 32
    
    @fahrenheit.setter
    def fahrenheit(self, value):
        """华氏度属性设置器"""
        celsius_value = (value - 32) * 5/9
        self.celsius = celsius_value
    
    @property
    def kelvin(self):
        """开尔文温度属性"""
        return self.celsius + 273.15
    
    @kelvin.setter
    def kelvin(self, value):
        """开尔文温度属性设置器"""
        if value < 0:
            raise ValueError("开尔文温度不能为负数")
        self.celsius = value - 273.15
    
    # 类方法
    @classmethod
    def from_fahrenheit(cls, fahrenheit):
        """从华氏度创建温度对象"""
        celsius = (fahrenheit - 32) * 5/9
        return cls(celsius)
    
    @classmethod
    def from_kelvin(cls, kelvin):
        """从开尔文温度创建温度对象"""
        if kelvin < 0:
            raise ValueError("开尔文温度不能为负数")
        celsius = kelvin - 273.15
        return cls(celsius)
    
    # 实例方法
    def to_fahrenheit(self):
        """转换为华氏度"""
        return self.fahrenheit
    
    def to_kelvin(self):
        """转换为开尔文温度"""
        return self.kelvin

# 使用温度类
print("创建温度对象:")
temp1 = Temperature(25)  # 25°C
temp2 = Temperature.from_fahrenheit(100)  # 100°F
temp3 = Temperature.from_kelvin(300)  # 300K

print(f"温度1: {temp1}")
print(f"温度2: {temp2}")
print(f"温度3: {temp3}")

# 属性访问
print("\n===属性访问===")
print(f"温度1摄氏度: {temp1.celsius}°C")
print(f"温度1华氏度: {temp1.fahrenheit}°F")
print(f"温度1开尔文: {temp1.kelvin}K")

# 属性设置
print("\n===属性设置===")
temp1.celsius = 0
print(f"设置为0°C: {temp1}")

temp1.fahrenheit = 32
print(f"设置为32°F: {temp1}")

temp1.kelvin = 273.15
print(f"设置为273.15K: {temp1}")

# 比较运算
print("\n===比较运算===")
print(f"temp1 == temp2: {temp1 == temp2}")
print(f"temp1 < temp2: {temp1 < temp2}")
print(f"temp1 > temp2: {temp1 > temp2}")

# 算术运算
print("\n===算术运算===")
temp_sum = temp1 + temp2
print(f"temp1 + temp2 = {temp_sum}")

temp_diff = temp1 - 5
print(f"temp1 - 5 = {temp_diff}")

# 演示错误处理
print("\n===错误处理===")
try:
    temp1.celsius = -300  # 低于绝对零度
except ValueError as e:
    print(f"错误: {e}")

try:
    temp1.kelvin = -10  # 负开尔文温度
except ValueError as e:
    print(f"错误: {e}")

# 演示特殊方法
print("\n===特殊方法演示===")
print("使用str():", str(temp1))
print("使用repr():", repr(temp1))

temperatures = [temp1, temp2, temp3]
print("温度排序:")
for temp in sorted(temperatures):
    print(f"  {temp}")
```

### 代码说明

**案例1代码解释**：
1. `def __str__(self):`：定义对象的字符串表示，用于print等场景
2. `def __add__(self, other):`：定义加法运算行为
3. `def __eq__(self, other):`：定义相等比较行为
4. `@property def conjugate(self):`：定义只读属性

如果在`__add__`方法中忘记处理`other`不是ComplexNumber的情况，当执行`c1 + "abc"`时会出错而不是返回NotImplemented。

**案例2代码解释**：
1. `def __lt__(self, other):`：定义小于比较行为
2. `@celsius.setter def celsius(self, value):`：定义摄氏度属性的设置器
3. `@classmethod def from_fahrenheit(cls, fahrenheit):`：定义类方法创建实例
4. `def __add__(self, other):`：定义温度相加的行为

如果在setter中忘记数据验证，如允许摄氏度低于绝对零度，会导致不合理的温度值。

## 7. 最佳实践和注意事项

### 知识点解析

**概念定义**：最佳实践就像经验丰富的老师傅传授的工作技巧，帮助我们写出更清晰、更可靠、更易于维护的面向对象代码。注意事项则是容易踩坑的地方，提前了解可以避免犯错。

**核心规则**：
1. 遵循单一职责原则，一个类只负责一项功能
2. 合理使用继承和组合，优先使用组合
3. 使用属性装饰器提供安全的数据访问
4. 正确使用访问控制保护内部实现
5. 为类和方法编写清晰的文档字符串

**常见易错点**：
1. 创建过于复杂的"上帝类"，违反单一职责原则
2. 滥用继承，导致类层次结构过于复杂
3. 忽略数据验证和边界条件检查
4. 过度使用私有成员，影响代码的可扩展性
5. 忘记为代码编写文档和注释

### 实战案例

#### 案例1：遵循单一职责原则
```python
# 遵循单一职责原则
print("===遵循单一职责原则===")

# 不好的设计：一个类负责太多功能
class BadUser:
    """不好的用户类设计"""
    
    def __init__(self, name, email):
        self.name = name
        self.email = email
        self.posts = []
        self.messages = []
    
    # 用户管理功能
    def save_to_database(self):
        print(f"保存用户 {self.name} 到数据库")
    
    def send_email(self, subject, content):
        print(f"发送邮件给 {self.email}: {subject}")
    
    # 内容管理功能
    def create_post(self, title, content):
        post = {"title": title, "content": content, "author": self.name}
        self.posts.append(post)
        print(f"用户 {self.name} 创建了文章: {title}")
    
    def send_message(self, recipient, content):
        message = {"from": self.name, "to": recipient, "content": content}
        self.messages.append(message)
        print(f"用户 {self.name} 发送消息给 {recipient}")
    
    # 数据验证功能
    def validate_email(self):
        return "@" in self.email
    
    def validate_name(self):
        return len(self.name) > 0

# 改进的设计：拆分为多个专门的类
class User:
    """用户类（只负责用户基本信息）"""
    
    def __init__(self, name, email):
        self.name = name
        self.email = email

class UserRepository:
    """用户仓库类（只负责用户数据存储）"""
    
    def save(self, user):
        print(f"保存用户 {user.name} 到数据库")
    
    def find_by_email(self, email):
        print(f"从数据库查找邮箱为 {email} 的用户")
        return None

class EmailService:
    """邮件服务类（只负责邮件发送）"""
    
    def send(self, to, subject, content):
        print(f"发送邮件给 {to}: {subject}")

class Post:
    """文章类（只负责文章内容）"""
    
    def __init__(self, title, content, author):
        self.title = title
        self.content = content
        self.author = author

class PostManager:
    """文章管理类（只负责文章操作）"""
    
    def __init__(self):
        self.posts = []
    
    def create_post(self, title, content, author):
        post = Post(title, content, author)
        self.posts.append(post)
        print(f"用户 {author} 创建了文章: {title}")
        return post

class Message:
    """消息类（只负责消息内容）"""
    
    def __init__(self, sender, recipient, content):
        self.sender = sender
        self.recipient = recipient
        self.content = content

class MessageService:
    """消息服务类（只负责消息操作）"""
    
    def __init__(self):
        self.messages = []
    
    def send_message(self, sender, recipient, content):
        message = Message(sender, recipient, content)
        self.messages.append(message)
        print(f"用户 {sender} 发送消息给 {recipient}")

class Validator:
    """验证器类（只负责数据验证）"""
    
    @staticmethod
    def validate_email(email):
        return "@" in email and "." in email
    
    @staticmethod
    def validate_name(name):
        return isinstance(name, str) and len(name.strip()) > 0

# 使用改进后的设计
print("===使用改进后的设计===")

# 创建用户
user = User("张三", "zhangsan@example.com")

# 验证用户数据
validator = Validator()
if validator.validate_name(user.name) and validator.validate_email(user.email):
    print("用户数据验证通过")
else:
    print("用户数据验证失败")

# 保存用户
user_repo = UserRepository()
user_repo.save(user)

# 发送邮件
email_service = EmailService()
email_service.send(user.email, "欢迎注册", "欢迎使用我们的服务")

# 创建文章
post_manager = PostManager()
post = post_manager.create_post("我的第一篇文章", "这是文章内容", user.name)

# 发送消息
message_service = MessageService()
message_service.send_message(user.name, "李四", "你好，我是张三")
```

#### 案例2：合理使用继承和组合
```python
# 合理使用继承和组合
print("\n===合理使用继承和组合===")

# 不好的设计：过度使用继承
class BadVehicle:
    """车辆基类"""
    
    def __init__(self, brand, model):
        self.brand = brand
        self.model = model
    
    def start_engine(self):
        print("启动引擎")

class BadCar(BadVehicle):
    """汽车类（继承）"""
    
    def __init__(self, brand, model, doors):
        super().__init__(brand, model)
        self.doors = doors

class BadBoat(BadVehicle):
    """船只类（继承）"""
    
    def __init__(self, brand, model, length):
        super().__init__(brand, model)
        self.length = length
    
    def start_engine(self):  # 重写方法
        print("启动船用引擎")

class BadAirplane(BadVehicle):
    """飞机类（继承）"""
    
    def __init__(self, brand, model, wingspan):
        super().__init__(brand, model)
        self.wingspan = wingspan
    
    def start_engine(self):  # 重写方法
        print("启动喷气引擎")

# 改进的设计：使用组合
class Engine:
    """引擎类"""
    
    def __init__(self, engine_type, horsepower):
        self.engine_type = engine_type
        self.horsepower = horsepower
    
    def start(self):
        print(f"启动{self.engine_type}引擎 ({self.horsepower}马力)")

class Vehicle:
    """车辆基类"""
    
    def __init__(self, brand, model):
        self.brand = brand
        self.model = model

class Car(Vehicle):
    """汽车类（使用组合）"""
    
    def __init__(self, brand, model, doors, engine):
        super().__init__(brand, model)
        self.doors = doors
        self.engine = engine  # 组合引擎
    
    def start(self):
        print(f"汽车 {self.brand} {self.model} 启动:")
        self.engine.start()

class Boat(Vehicle):
    """船只类（使用组合）"""
    
    def __init__(self, brand, model, length, engine):
        super().__init__(brand, model)
        self.length = length
        self.engine = engine  # 组合引擎
    
    def start(self):
        print(f"船只 {self.brand} {self.model} 启动:")
        self.engine.start()

class Airplane(Vehicle):
    """飞机类（使用组合）"""
    
    def __init__(self, brand, model, wingspan, engine):
        super().__init__(brand, model)
        self.wingspan = wingspan
        self.engine = engine  # 组合引擎
    
    def start(self):
        print(f"飞机 {self.brand} {self.model} 启动:")
        self.engine.start()

# 使用改进后的设计
print("===使用改进后的设计===")

# 创建不同的引擎
car_engine = Engine("汽油", 200)
boat_engine = Engine("柴油", 500)
jet_engine = Engine("喷气", 10000)

# 创建不同的载具
car = Car("丰田", "凯美瑞", 4, car_engine)
boat = Boat("游艇", "豪华版", 20, boat_engine)
airplane = Airplane("波音", "737", 35, jet_engine)

# 启动载具
vehicles = [car, boat, airplane]
for vehicle in vehicles:
    vehicle.start()
    print()

# 演示组合的灵活性
print("===演示组合的灵活性===")
# 同一个引擎可以用于不同类型的载具
electric_engine = Engine("电动", 150)

electric_car = Car("特斯拉", "Model 3", 4, electric_engine)
electric_boat = Boat("电动艇", "小型版", 5, electric_engine)

electric_car.start()
electric_boat.start()
```

### 代码说明

**案例1代码解释**：
1. `BadUser`类违反了单一职责原则，一个类负责用户管理、内容管理、数据验证等多项功能
2. 改进后拆分为`User`、`UserRepository`、`EmailService`、`PostManager`、`MessageService`、`Validator`等多个专门的类
3. 每个类只负责一项功能，职责清晰，易于维护和扩展

如果继续使用`BadUser`这样的设计，当需要修改邮件发送功能时，可能会影响用户管理功能，增加了维护难度和出错风险。

**案例2代码解释**：
1. `BadVehicle`及其子类过度使用继承，导致每个子类都需要重写`start_engine`方法
2. 改进后使用组合，将`Engine`类作为组件组合到不同的载具类中
3. 每种载具都可以使用不同类型的引擎，更加灵活

如果使用继承的方式，当需要添加新的引擎类型时，可能需要修改多个子类；而使用组合的方式，只需要创建新的引擎类即可，符合开闭原则。

这些最佳实践帮助我们编写出更加清晰、可维护、可扩展的面向对象代码。通过遵循这些原则，我们可以避免常见的设计错误，提高代码质量。