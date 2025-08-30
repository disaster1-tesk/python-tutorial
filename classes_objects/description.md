# Python类与对象知识点

## 1. 类的定义

类是面向对象编程的核心概念，它是一种用于创建对象的蓝图。

### 基本语法
```python
class ClassName:
    """类文档字符串"""
    # 类属性
    # 构造方法
    # 实例方法
    # 类方法
    # 静态方法
```

### 使用示例
```python
class Person:
    """人类"""
    
    # 类属性
    species = "Homo sapiens"
    
    def __init__(self, name, age):
        """构造方法"""
        # 实例属性
        self.name = name
        self.age = age
    
    def introduce(self):
        """自我介绍方法"""
        return f"我是{self.name}，今年{self.age}岁。"
    
    def have_birthday(self):
        """过生日"""
        self.age += 1
        print(f"{self.name}现在{self.age}岁了！")

# 创建对象
person1 = Person("张三", 25)
person2 = Person("李四", 30)

print(person1.introduce())  # 我是张三，今年25岁。
print(person2.introduce())  # 我是李四，今年30岁。
person1.have_birthday()     # 张三现在26岁了！
```

## 2. 对象的创建

通过类名加括号的方式创建对象(实例)，这个过程称为实例化。

### 使用示例
```python
class Car:
    """汽车类"""
    def __init__(self, brand, model, year):
        self.brand = brand
        self.model = model
        self.year = year
        self.mileage = 0  # 默认里程为0
    
    def drive(self, miles):
        """驾驶汽车"""
        self.mileage += miles
        print(f"驾驶了{miles}公里，总里程{self.mileage}公里")

# 创建多个对象
car1 = Car("丰田", "卡罗拉", 2020)
car2 = Car("本田", "雅阁", 2021)

print(f"{car1.brand} {car1.model} {car1.year}")  # 丰田 卡罗拉 2020
print(f"{car2.brand} {car2.model} {car2.year}")  # 本田 雅阁 2021

car1.drive(100)  # 驾驶了100公里，总里程100公里
car2.drive(200)  # 驾驶了200公里，总里程200公里
```

## 3. 构造方法

`__init__`方法是类的构造方法，在创建对象时自动调用。

### 使用示例
```python
class BankAccount:
    """银行账户类"""
    
    def __init__(self, account_number, owner, initial_balance=0):
        """
        初始化银行账户
        
        Args:
            account_number (str): 账户号码
            owner (str): 账户所有者
            initial_balance (float): 初始余额，默认为0
        """
        self.account_number = account_number
        self.owner = owner
        self.balance = initial_balance
        self.transaction_history = []  # 交易历史
    
    def deposit(self, amount):
        """存款"""
        if amount > 0:
            self.balance += amount
            self.transaction_history.append(f"存款 +{amount}")
            print(f"存款{amount}元，当前余额{self.balance}元")
        else:
            print("存款金额必须大于0")
    
    def withdraw(self, amount):
        """取款"""
        if amount > 0 and amount <= self.balance:
            self.balance -= amount
            self.transaction_history.append(f"取款 -{amount}")
            print(f"取款{amount}元，当前余额{self.balance}元")
        elif amount > self.balance:
            print("余额不足")
        else:
            print("取款金额必须大于0")

# 创建账户
account = BankAccount("123456789", "张三", 1000)
account.deposit(500)   # 存款500元，当前余额1500元
account.withdraw(200)  # 取款200元，当前余额1300元
```

## 4. 实例属性和类属性

### 实例属性
属于特定实例的属性，在`__init__`方法中定义。

### 类属性
属于类本身的属性，在类中直接定义。

```python
class Employee:
    """员工类"""
    
    # 类属性
    company_name = "科技有限公司"
    employee_count = 0  # 员工计数器
    
    def __init__(self, name, position, salary):
        # 实例属性
        self.name = name
        self.position = position
        self.salary = salary
        
        # 每创建一个员工，计数器加1
        Employee.employee_count += 1
        self.employee_id = Employee.employee_count
    
    def get_info(self):
        """获取员工信息"""
        return f"ID: {self.employee_id}, 姓名: {self.name}, 职位: {self.position}"
    
    @classmethod
    def get_company_info(cls):
        """获取公司信息"""
        return f"公司名称: {cls.company_name}, 员工总数: {cls.employee_count}"

# 创建员工
emp1 = Employee("张三", "程序员", 8000)
emp2 = Employee("李四", "设计师", 7000)

print(emp1.get_info())  # ID: 1, 姓名: 张三, 职位: 程序员
print(emp2.get_info())  # ID: 2, 姓名: 李四, 职位: 设计师
print(Employee.get_company_info())  # 公司名称: 科技有限公司, 员工总数: 2

# 修改类属性
Employee.company_name = "新科技有限公司"
print(Employee.get_company_info())  # 公司名称: 新科技有限公司, 员工总数: 2
```

## 5. 实例方法、类方法和静态方法

### 实例方法
普通方法，第一个参数是self，表示实例本身。

### 类方法
使用@classmethod装饰器，第一个参数是cls，表示类本身。

### 静态方法
使用@staticmethod装饰器，不需要特殊参数。

```python
class MathUtils:
    """数学工具类"""
    
    # 类属性
    pi = 3.14159
    
    def __init__(self, precision=2):
        """初始化精度"""
        self.precision = precision
    
    # 实例方法
    def round_number(self, number):
        """四舍五入到指定精度"""
        return round(number, self.precision)
    
    # 类方法
    @classmethod
    def circle_area(cls, radius):
        """计算圆面积的类方法"""
        return cls.pi * radius ** 2
    
    # 静态方法
    @staticmethod
    def is_even(number):
        """判断是否为偶数的静态方法"""
        return number % 2 == 0
    
    @staticmethod
    def gcd(a, b):
        """计算最大公约数"""
        while b:
            a, b = b, a % b
        return a

# 使用实例方法
utils = MathUtils(3)
print(utils.round_number(3.14159))  # 3.142

# 使用类方法
print(MathUtils.circle_area(5))  # 78.53975

# 使用静态方法
print(MathUtils.is_even(4))  # True
print(MathUtils.gcd(48, 18))  # 6
```

## 6. 封装

封装是面向对象编程的重要特性，通过访问控制来隐藏实现细节。

### 访问级别约定
- **公有成员**：正常命名，可以随意访问
- **受保护成员**：单下划线前缀(_)，约定为内部使用
- **私有成员**：双下划线前缀(__)，名称改写

```python
class BankAccount:
    """银行账户类（封装示例）"""
    
    def __init__(self, account_number, initial_balance=0):
        self.account_number = account_number      # 公有属性
        self._balance = initial_balance           # 受保护属性
        self.__pin = "1234"                       # 私有属性
    
    def deposit(self, amount):
        """存款"""
        if amount > 0:
            self._balance += amount
            return True
        return False
    
    def withdraw(self, amount, pin):
        """取款"""
        if self.__verify_pin(pin) and amount > 0 and amount <= self._balance:
            self._balance -= amount
            return True
        return False
    
    def get_balance(self, pin):
        """获取余额"""
        if self.__verify_pin(pin):
            return self._balance
        return None
    
    def __verify_pin(self, pin):
        """验证密码（私有方法）"""
        return pin == self.__pin
    
    def _log_transaction(self, transaction):
        """记录交易（受保护方法）"""
        print(f"记录交易: {transaction}")

# 使用示例
account = BankAccount("123456789", 1000)

# 公有属性可以直接访问
print(account.account_number)  # 123456789

# 受保护属性可以访问，但约定不直接访问
print(account._balance)  # 1000

# 私有属性不能直接访问
# print(account.__pin)  # AttributeError

# 通过公共方法访问私有数据
account.deposit(500)
print(account.get_balance("1234"))  # 1500

# 私有属性的实际名称（名称改写）
print(account._BankAccount__pin)  # 1234
```

## 7. 继承

继承允许子类继承父类的属性和方法，实现代码重用。

### 基本语法
```python
class ChildClass(ParentClass):
    # 子类定义
```

### 使用示例
```python
class Animal:
    """动物基类"""
    
    def __init__(self, name, species):
        self.name = name
        self.species = species
    
    def make_sound(self):
        """发出声音"""
        pass
    
    def info(self):
        """基本信息"""
        return f"我是{self.name}，属于{self.species}物种"

class Dog(Animal):
    """狗类（继承自动物类）"""
    
    def __init__(self, name, breed):
        super().__init__(name, "犬科")
        self.breed = breed
    
    def make_sound(self):
        """重写父类方法"""
        return "汪汪汪！"
    
    def fetch(self):
        """特有的方法"""
        return f"{self.name}正在捡球"

class Cat(Animal):
    """猫类（继承自动物类）"""
    
    def __init__(self, name, color):
        super().__init__(name, "猫科")
        self.color = color
    
    def make_sound(self):
        """重写父类方法"""
        return "喵喵喵！"
    
    def climb(self):
        """特有的方法"""
        return f"{self.name}正在爬树"

# 创建对象
dog = Dog("旺财", "金毛")
cat = Cat("咪咪", "橘色")

print(dog.info())           # 我是旺财，属于犬科物种
print(dog.make_sound())     # 汪汪汪！
print(dog.fetch())          # 旺财正在捡球

print(cat.info())           # 我是咪咪，属于猫科物种
print(cat.make_sound())     # 喵喵喵！
print(cat.climb())          # 咪咪正在爬树
```

### 多重继承
```python
class Flyable:
    """可飞行的"""
    def fly(self):
        return "正在飞行"

class Swimmable:
    """可游泳的"""
    def swim(self):
        return "正在游泳"

class Duck(Animal, Flyable, Swimmable):
    """鸭子类（多重继承）"""
    
    def __init__(self, name):
        super().__init__(name, "鸭科")
    
    def make_sound(self):
        return "嘎嘎嘎！"

# 创建鸭子对象
duck = Duck("唐老鸭")
print(duck.info())      # 我是唐老鸭，属于鸭科物种
print(duck.make_sound()) # 嘎嘎嘎！
print(duck.fly())       # 正在飞行
print(duck.swim())      # 正在游泳
```

## 8. 多态

多态允许不同类的对象对同一消息做出不同的响应。

```python
class Shape:
    """形状基类"""
    
    def area(self):
        """计算面积"""
        pass
    
    def perimeter(self):
        """计算周长"""
        pass

class Rectangle(Shape):
    """矩形类"""
    
    def __init__(self, width, height):
        self.width = width
        self.height = height
    
    def area(self):
        return self.width * self.height
    
    def perimeter(self):
        return 2 * (self.width + self.height)

class Circle(Shape):
    """圆形类"""
    
    def __init__(self, radius):
        self.radius = radius
    
    def area(self):
        return 3.14159 * self.radius ** 2
    
    def perimeter(self):
        return 2 * 3.14159 * self.radius

class Triangle(Shape):
    """三角形类"""
    
    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c
    
    def area(self):
        # 使用海伦公式计算面积
        s = (self.a + self.b + self.c) / 2
        return (s * (s - self.a) * (s - self.b) * (s - self.c)) ** 0.5
    
    def perimeter(self):
        return self.a + self.b + self.c

# 多态示例
shapes = [
    Rectangle(5, 3),
    Circle(4),
    Triangle(3, 4, 5)
]

for shape in shapes:
    print(f"面积: {shape.area():.2f}, 周长: {shape.perimeter():.2f}")
```

## 9. 特殊方法(魔术方法)

特殊方法以双下划线开头和结尾，用于实现类的特殊行为。

```python
class Vector:
    """向量类"""
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __str__(self):
        """字符串表示"""
        return f"Vector({self.x}, {self.y})"
    
    def __repr__(self):
        """开发者字符串表示"""
        return f"Vector(x={self.x}, y={self.y})"
    
    def __add__(self, other):
        """加法运算"""
        if isinstance(other, Vector):
            return Vector(self.x + other.x, self.y + other.y)
        return NotImplemented
    
    def __mul__(self, scalar):
        """数乘运算"""
        if isinstance(scalar, (int, float)):
            return Vector(self.x * scalar, self.y * scalar)
        return NotImplemented
    
    def __eq__(self, other):
        """相等比较"""
        if isinstance(other, Vector):
            return self.x == other.x and self.y == other.y
        return False
    
    def __len__(self):
        """向量的长度"""
        return int((self.x ** 2 + self.y ** 2) ** 0.5)
    
    def __abs__(self):
        """向量的模"""
        return (self.x ** 2 + self.y ** 2) ** 0.5

# 使用特殊方法
v1 = Vector(3, 4)
v2 = Vector(1, 2)

print(str(v1))        # Vector(3, 4)
print(repr(v1))       # Vector(x=3, y=4)
print(v1 + v2)        # Vector(4, 6)
print(v1 * 3)         # Vector(9, 12)
print(v1 == v2)       # False
print(len(v1))        # 5
print(abs(v1))        # 5.0
```

## 10. 属性装饰器

@property装饰器将方法变为属性访问。

```python
class Temperature:
    """温度类"""
    
    def __init__(self, celsius=0):
        self._celsius = celsius
    
    @property
    def celsius(self):
        """摄氏度属性（只读）"""
        return self._celsius
    
    @celsius.setter
    def celsius(self, value):
        """摄氏度属性的setter"""
        if value < -273.15:
            raise ValueError("温度不能低于绝对零度")
        self._celsius = value
    
    @celsius.deleter
    def celsius(self):
        """摄氏度属性的deleter"""
        print("删除摄氏度值")
        self._celsius = 0
    
    @property
    def fahrenheit(self):
        """华氏度属性（只读）"""
        return self._celsius * 9/5 + 32
    
    @fahrenheit.setter
    def fahrenheit(self, value):
        """华氏度属性的setter"""
        self.celsius = (value - 32) * 5/9

# 使用属性装饰器
temp = Temperature(25)
print(f"摄氏度: {temp.celsius}")      # 摄氏度: 25
print(f"华氏度: {temp.fahrenheit}")   # 华氏度: 77.0

temp.celsius = 30
print(f"摄氏度: {temp.celsius}")      # 摄氏度: 30
print(f"华氏度: {temp.fahrenheit}")   # 华氏度: 86.0

temp.fahrenheit = 100
print(f"摄氏度: {temp.celsius:.2f}")  # 摄氏度: 37.78
```

## 11. 实际应用场景

### 数据建模和抽象
```python
class Product:
    """产品类"""
    
    def __init__(self, name, price, category):
        self.name = name
        self.price = price
        self.category = category
        self.reviews = []
    
    def add_review(self, rating, comment):
        """添加评价"""
        self.reviews.append({
            'rating': rating,
            'comment': comment
        })
    
    def average_rating(self):
        """平均评分"""
        if not self.reviews:
            return 0
        return sum(review['rating'] for review in self.reviews) / len(self.reviews)
    
    def __str__(self):
        return f"{self.name} - ¥{self.price} ({self.category})"

class ShoppingCart:
    """购物车类"""
    
    def __init__(self):
        self.items = []
    
    def add_item(self, product, quantity=1):
        """添加商品"""
        self.items.append({
            'product': product,
            'quantity': quantity
        })
    
    def total_price(self):
        """总价格"""
        return sum(item['product'].price * item['quantity'] for item in self.items)
    
    def __str__(self):
        items_str = "\n".join([f"{item['product'].name} x{item['quantity']}" 
                              for item in self.items])
        return f"购物车:\n{items_str}\n总计: ¥{self.total_price()}"

# 使用示例
laptop = Product("笔记本电脑", 5999, "电子产品")
phone = Product("智能手机", 3999, "电子产品")

laptop.add_review(5, "非常好用")
laptop.add_review(4, "性价比高")

cart = ShoppingCart()
cart.add_item(laptop, 1)
cart.add_item(phone, 2)

print(cart)
print(f"笔记本电脑平均评分: {laptop.average_rating()}")
```

## 12. 最佳实践

### 遵循单一职责原则
```python
# 不好的做法
class User:
    def __init__(self, name, email):
        self.name = name
        self.email = email
    
    def save_to_database(self):
        # 保存到数据库
        pass
    
    def send_email(self):
        # 发送邮件
        pass
    
    def validate_email(self):
        # 验证邮箱
        pass

# 改进：拆分为多个类
class User:
    def __init__(self, name, email):
        self.name = name
        self.email = email

class UserRepository:
    def save(self, user):
        # 保存用户到数据库
        pass

class EmailService:
    def send(self, email, message):
        # 发送邮件
        pass

class EmailValidator:
    def validate(self, email):
        # 验证邮箱
        pass
```

### 合理使用继承和组合
```python
# 组合优于继承
class Engine:
    def __init__(self, horsepower):
        self.horsepower = horsepower
    
    def start(self):
        return "引擎启动"

class Car:
    def __init__(self, brand, model, engine):
        self.brand = brand
        self.model = model
        self.engine = engine  # 组合
    
    def start(self):
        return f"{self.brand} {self.model} {self.engine.start()}"

engine = Engine(200)
car = Car("丰田", "凯美瑞", engine)
print(car.start())  # 丰田 凯美瑞 引擎启动
```