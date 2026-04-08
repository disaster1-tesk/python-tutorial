# Python类型注解与代码质量

## 1. 类型注解基础

### 知识点解析

**概念定义**：类型注解就像给代码加上"标签"，告诉阅读者（以及工具）每个变量、参数和返回值应该是什么类型。它不影响程序运行，但能让代码更易读，并允许静态分析工具在运行前发现错误。就像仓库里给货物贴上种类标签，不改变货物本身，但让管理更清晰。

**核心规则**：
1. 变量注解：`变量名: 类型 = 值`，如 `name: str = "张三"`
2. 函数参数注解：`def func(param: 类型) -> 返回类型:`
3. 注解不强制类型检查，运行时不会因类型不符而报错（除非手动检查）
4. Python 3.5+ 支持基础注解，3.9+ 内置集合直接支持泛型（如 `list[int]`），3.10+ 支持联合类型 `X | Y`
5. 使用 `from __future__ import annotations` 在旧版 Python 中延迟求值注解

**常见易错点**：
1. 把注解当做真正的类型限制——运行时 `x: int = "hello"` 不会报错
2. Python 3.9 以下用 `list[int]` 会报错，应使用 `from typing import List` 或加 `from __future__ import annotations`
3. 注解复杂类型时遗漏 `Optional`——能接收 `None` 的参数要用 `Optional[T]` 或 `T | None`
4. 在函数签名中写 `-> None` 表示无返回值，省略 `->` 与写 `-> None` 含义相同但后者更明确

### 实战案例

#### 案例1：从无注解到有注解的重构
```python
# 类型注解基础演示
from __future__ import annotations
from typing import Optional, Union

print("===类型注解基础===")

# 1. 变量注解
user_name: str = "张三"
user_age: int = 25
user_score: float = 98.5
is_active: bool = True
user_tags: list[str] = ["Python", "后端", "数据分析"]
user_info: dict[str, int] = {"语文": 90, "数学": 95, "英语": 88}

print(f"用户: {user_name}, 年龄: {user_age}, 分数: {user_score}")
print(f"标签: {user_tags}")
print(f"成绩: {user_info}")

# 2. 函数注解：无注解 vs 有注解对比
# 无注解版本（难以理解参数类型）
def greet_old(name, age, greeting=None):
    if greeting is None:
        greeting = "你好"
    return f"{greeting}，{name}！你今年{age}岁了。"

# 有注解版本（清晰明了）
def greet(name: str, age: int, greeting: Optional[str] = None) -> str:
    """生成问候语

    Args:
        name: 用户姓名
        age: 用户年龄
        greeting: 自定义问候语，默认为"你好"

    Returns:
        格式化的问候字符串
    """
    if greeting is None:
        greeting = "你好"
    return f"{greeting}，{name}！你今年{age}岁了。"

print("\n===函数注解对比===")
print(greet("张三", 25))
print(greet("李四", 30, "嗨"))

# 3. 联合类型（接受多种类型）
def process_id(user_id: Union[int, str]) -> str:
    """处理用户ID，可以是整数或字符串"""
    return f"用户ID: {str(user_id).zfill(6)}"

# Python 3.10+ 可以写成：def process_id(user_id: int | str) -> str:
print("\n===联合类型===")
print(process_id(42))
print(process_id("U00123"))

# 4. 可选类型（允许 None）
def find_user(user_id: int) -> Optional[dict[str, str]]:
    """查找用户，不存在返回 None"""
    users = {1: {"name": "张三", "email": "zhang@example.com"}}
    return users.get(user_id)

result = find_user(1)
if result:
    print(f"\n找到用户: {result['name']}")

result2 = find_user(99)
if result2 is None:
    print("未找到用户ID=99的用户")
```

#### 案例2：复杂类型注解实战
```python
# 复杂类型注解
from __future__ import annotations
from typing import Callable, TypeVar, Any
from collections.abc import Sequence, Iterator

print("===复杂类型注解实战===")

# 1. Callable 注解：表示可调用对象
def apply_twice(func: Callable[[int], int], value: int) -> int:
    """将函数应用两次"""
    return func(func(value))

def double(x: int) -> int:
    return x * 2

print(f"apply_twice(double, 3) = {apply_twice(double, 3)}")  # 12

# 2. TypeVar：泛型类型变量
T = TypeVar("T")

def first_element(items: Sequence[T]) -> Optional[T]:
    """获取序列第一个元素"""
    return items[0] if items else None

print(f"\n第一个整数: {first_element([1, 2, 3])}")
print(f"第一个字符串: {first_element(['a', 'b', 'c'])}")
print(f"空序列: {first_element([])}")

# 3. 类的类型注解
class BankAccount:
    """银行账户类（带完整类型注解）"""

    def __init__(self, owner: str, balance: float = 0.0) -> None:
        self.owner: str = owner
        self.balance: float = balance
        self._transactions: list[dict[str, Any]] = []

    def deposit(self, amount: float) -> BankAccount:
        """存款，返回 self 支持链式调用"""
        if amount <= 0:
            raise ValueError(f"存款金额必须为正数，收到: {amount}")
        self.balance += amount
        self._transactions.append({"type": "deposit", "amount": amount})
        return self

    def withdraw(self, amount: float) -> BankAccount:
        """取款"""
        if amount <= 0:
            raise ValueError(f"取款金额必须为正数，收到: {amount}")
        if amount > self.balance:
            raise ValueError(f"余额不足：当前 {self.balance}，取款 {amount}")
        self.balance -= amount
        self._transactions.append({"type": "withdraw", "amount": amount})
        return self

    def get_history(self) -> list[dict[str, Any]]:
        """获取交易历史"""
        return self._transactions.copy()

    def __repr__(self) -> str:
        return f"BankAccount(owner={self.owner!r}, balance={self.balance:.2f})"

# 演示
print("\n===银行账户演示===")
account = BankAccount("张三", 1000.0)
account.deposit(500.0).deposit(200.0).withdraw(300.0)
print(account)
print(f"交易记录: {account.get_history()}")
```

### 代码说明

**案例1代码解释**：
1. `from __future__ import annotations`：让注解延迟求值，避免 Python 3.9 以下版本的兼容问题
2. `Optional[str]`：等价于 `Union[str, None]`，表示参数可以是字符串或 None
3. `Union[int, str]`：接受整数或字符串两种类型，Python 3.10+ 可写成 `int | str`
4. `-> str`：函数返回类型注解，`-> None` 表示无返回值

**案例2代码解释**：
1. `Callable[[int], int]`：表示接收一个 int 参数并返回 int 的可调用对象
2. `TypeVar("T")`：定义泛型变量，让函数对多种类型都适用且保持类型安全
3. 类方法的 `-> BankAccount`：返回 self 时注解为类名，支持链式调用
4. 实例变量也可以在 `__init__` 中用 `self.attr: 类型 = 值` 注解

---

## 2. dataclasses 装饰器

### 知识点解析

**概念定义**：`dataclasses` 是 Python 3.7+ 的内置装饰器，专门用于创建"数据类"——主要用来存储数据的类。它自动生成 `__init__`、`__repr__`、`__eq__` 等常用方法，省去了大量样板代码。就像让 Python 自动帮你建造仓库的货架，你只需要说明放什么货物，它帮你安排好一切。

**核心规则**：
1. 使用 `@dataclass` 装饰器，字段用类型注解声明
2. 有默认值的字段必须在无默认值的字段之后
3. 可变默认值（如列表）必须用 `field(default_factory=...)` 而不能直接写 `= []`
4. `frozen=True` 创建不可变数据类（类似命名元组，但更强大）
5. `__post_init__` 方法在 `__init__` 之后自动调用，可做额外初始化或验证

**常见易错点**：
1. 直接写 `tags: list = []` 会报 `ValueError: mutable default is not allowed`，必须用 `field(default_factory=list)`
2. 继承时父类的带默认值字段不能在子类的无默认值字段之前
3. `frozen=True` 的实例尝试修改字段会报 `FrozenInstanceError`
4. 把 `dataclass` 与普通类混用继承时注意 MRO 顺序

### 实战案例

#### 案例1：数据类基础用法
```python
# dataclasses 基础
from dataclasses import dataclass, field, asdict, astuple
from typing import Optional
import json

print("===dataclasses 基础===")

@dataclass
class Point:
    """二维坐标点"""
    x: float
    y: float

    def distance_to(self, other: Point) -> float:
        """计算到另一个点的距离"""
        return ((self.x - other.x) ** 2 + (self.y - other.y) ** 2) ** 0.5

@dataclass
class Student:
    """学生数据类"""
    name: str
    student_id: str
    age: int
    scores: list[float] = field(default_factory=list)   # 可变默认值用 field
    grade: Optional[str] = None                          # 可选字段默认 None

    def __post_init__(self) -> None:
        """初始化后验证数据"""
        if self.age < 0 or self.age > 150:
            raise ValueError(f"年龄无效: {self.age}")
        if not self.student_id.startswith("S"):
            self.student_id = "S" + self.student_id  # 自动格式化

    @property
    def average_score(self) -> Optional[float]:
        """计算平均分"""
        if not self.scores:
            return None
        return sum(self.scores) / len(self.scores)

    def add_score(self, score: float) -> None:
        """添加成绩"""
        if not 0 <= score <= 100:
            raise ValueError(f"成绩超出范围: {score}")
        self.scores.append(score)
        # 自动更新等级
        avg = self.average_score
        if avg is not None:
            if avg >= 90:
                self.grade = "优秀"
            elif avg >= 80:
                self.grade = "良好"
            elif avg >= 70:
                self.grade = "中等"
            elif avg >= 60:
                self.grade = "及格"
            else:
                self.grade = "不及格"

# 演示
print("=== Point 演示 ===")
p1 = Point(0.0, 0.0)
p2 = Point(3.0, 4.0)
print(f"p1 = {p1}")       # 自动生成的 __repr__
print(f"p2 = {p2}")
print(f"距离 = {p1.distance_to(p2)}")  # 5.0
print(f"p1 == Point(0,0): {p1 == Point(0.0, 0.0)}")  # 自动生成的 __eq__

print("\n=== Student 演示 ===")
s1 = Student(name="张三", student_id="001", age=20)
s1.add_score(85)
s1.add_score(92)
s1.add_score(78)
print(f"学生: {s1}")
print(f"平均分: {s1.average_score:.2f}")
print(f"等级: {s1.grade}")

# 转为字典（方便序列化）
student_dict = asdict(s1)
print(f"\n序列化为字典: {json.dumps(student_dict, ensure_ascii=False, indent=2)}")
```

#### 案例2：冻结数据类与继承
```python
# 冻结数据类和继承
from dataclasses import dataclass, field
from typing import ClassVar

print("===冻结数据类===")

@dataclass(frozen=True)
class Color:
    """不可变颜色类（RGB）"""
    r: int
    g: int
    b: int
    CLASS_INFO: ClassVar[str] = "RGB颜色"  # 类变量，不被 dataclass 处理

    def __post_init__(self) -> None:
        for name, val in [("r", self.r), ("g", self.g), ("b", self.b)]:
            if not 0 <= val <= 255:
                raise ValueError(f"{name} 必须在 0-255 之间，收到 {val}")

    def to_hex(self) -> str:
        """转为十六进制颜色码"""
        return f"#{self.r:02X}{self.g:02X}{self.b:02X}"

    def blend(self, other: Color, ratio: float = 0.5) -> Color:
        """混合两种颜色"""
        def mix(a: int, b: int) -> int:
            return round(a * ratio + b * (1 - ratio))
        return Color(mix(self.r, other.r), mix(self.g, other.g), mix(self.b, other.b))

red = Color(255, 0, 0)
blue = Color(0, 0, 255)
purple = red.blend(blue)
print(f"红色: {red} -> {red.to_hex()}")
print(f"蓝色: {blue} -> {blue.to_hex()}")
print(f"混合: {purple} -> {purple.to_hex()}")

# 尝试修改冻结实例
try:
    red.r = 100
except Exception as e:
    print(f"尝试修改冻结实例: {type(e).__name__}: {e}")

print("\n===数据类继承===")

@dataclass
class Animal:
    name: str
    age: int
    sound: str = "..."

    def speak(self) -> str:
        return f"{self.name} 说: {self.sound}"

@dataclass
class Dog(Animal):
    breed: str = "未知品种"
    tricks: list[str] = field(default_factory=list)
    sound: str = "汪汪"   # 覆盖父类默认值

    def learn_trick(self, trick: str) -> None:
        self.tricks.append(trick)

    def perform(self) -> str:
        if not self.tricks:
            return f"{self.name} 还没学会任何技能"
        return f"{self.name} 会表演: {', '.join(self.tricks)}"

dog = Dog(name="旺财", age=3, breed="金毛")
dog.learn_trick("握手")
dog.learn_trick("翻滚")
print(dog.speak())
print(dog.perform())
print(f"狗的信息: {dog}")
```

### 代码说明

**案例1代码解释**：
1. `@dataclass` 自动生成 `__init__`、`__repr__`、`__eq__`，无需手动编写
2. `field(default_factory=list)` 是可变默认值的正确写法，每次创建实例时都会调用 `list()` 生成新列表
3. `__post_init__` 在自动生成的 `__init__` 末尾被调用，适合做参数校验和格式化
4. `asdict()` 将数据类递归转换为字典，方便 JSON 序列化

**案例2代码解释**：
1. `frozen=True` 使实例不可修改，尝试赋值会抛出 `FrozenInstanceError`，冻结实例可哈希（hashable）
2. `ClassVar[str]` 声明类变量，dataclass 不会把它当作字段处理
3. 子类继承时，子类中可以覆盖父类字段的默认值（如 `sound: str = "汪汪"`）
4. 继承 dataclass 时，父类所有有默认值的字段在子类无默认值字段之前，这可能导致排列问题，此时可用 `field(default=...)` 或 `kw_only=True`（Python 3.10+）

---

## 3. Python 3.10+ 新类型语法

### 知识点解析

**概念定义**：Python 3.10 引入了两个重要特性：`match/case` 结构模式匹配，以及 `X | Y` 联合类型语法糖。这些特性让代码更简洁、表达力更强。`match/case` 就像增强版的 `switch`，不仅能匹配值，还能匹配数据结构和类型。

**核心规则**：
1. `X | Y` 替代 `Union[X, Y]`，要求 Python 3.10+，注解中使用加 `from __future__ import annotations` 可在低版本中写法兼容
2. `match` 语句从上到下匹配第一个符合的 `case`，匹配到后不会继续（不需要 break）
3. `case _` 是通配符，相当于 `default`
4. 结构模式匹配支持匹配序列、映射（字典）、类实例等复杂结构
5. `|` 在 `case` 中也可以组合多个模式：`case "yes" | "y":`

**常见易错点**：
1. `match` 的 subject 是表达式，不是语句，可以是任意值
2. `case [x, y]` 匹配长度为2的序列并解包，不同于列表相等性比较
3. 模式中的 `.` 访问不被视为捕获变量（如 `case Status.OK` 是字面量，`case x` 是捕获变量）
4. Python 3.10 以下运行 `match` 语法会报 `SyntaxError`

### 实战案例

#### 案例1：match/case 模式匹配
```python
# Python 3.10+ match/case 演示
# （以下代码需要 Python 3.10+）
import sys

print("===match/case 模式匹配===")
print(f"Python 版本: {sys.version}")

def describe_number(n: int) -> str:
    """用 match/case 描述数字"""
    match n:
        case 0:
            return "零"
        case 1 | 2 | 3:
            return "很小的正整数"
        case x if x < 0:
            return f"负数: {x}"
        case x if x > 1000:
            return f"大数: {x}"
        case x:
            return f"普通正整数: {x}"

for num in [0, 2, -5, 1500, 42]:
    print(f"describe_number({num}) = {describe_number(num)}")

# 匹配序列（列表/元组）
def process_command(command: list) -> str:
    """解析命令列表"""
    match command:
        case []:
            return "空命令"
        case ["quit"]:
            return "退出程序"
        case ["go", direction]:
            return f"向 {direction} 走"
        case ["go", direction, steps]:
            return f"向 {direction} 走 {steps} 步"
        case ["attack", target, *weapons]:
            return f"用 {', '.join(weapons)} 攻击 {target}"
        case _:
            return f"未知命令: {command}"

print("\n===命令解析===")
for cmd in [[], ["quit"], ["go", "北"], ["go", "东", 3], ["attack", "龙", "剑", "魔法"]]:
    print(f"{cmd!r:35} -> {process_command(cmd)}")

# 匹配字典
def handle_event(event: dict) -> str:
    """处理事件字典"""
    match event:
        case {"type": "click", "button": btn, "x": x, "y": y}:
            return f"鼠标点击: 按钮={btn}, 位置=({x},{y})"
        case {"type": "keypress", "key": key}:
            return f"键盘按键: {key}"
        case {"type": "error", "message": msg}:
            return f"错误: {msg}"
        case {"type": t}:
            return f"未知事件类型: {t}"
        case _:
            return "无效事件"

print("\n===事件处理===")
events = [
    {"type": "click", "button": "left", "x": 100, "y": 200},
    {"type": "keypress", "key": "Enter"},
    {"type": "error", "message": "网络超时"},
    {"type": "scroll"},
]
for evt in events:
    print(handle_event(evt))
```

#### 案例2：新联合类型语法与类型守卫
```python
# Python 3.10+ 联合类型语法
from __future__ import annotations  # 兼容旧版 Python 的注解写法

print("===联合类型语法对比===")

# 旧写法（所有 Python 3.5+ 都支持）
from typing import Union, Optional

def old_style(value: Union[int, float, str]) -> Optional[str]:
    if isinstance(value, (int, float)):
        return f"数字: {value}"
    return None

# 新写法（Python 3.10+ 运行时，或用 from __future__ import annotations 的注解）
def new_style(value: int | float | str) -> str | None:
    if isinstance(value, (int, float)):
        return f"数字: {value}"
    return None

for v in [42, 3.14, "hello"]:
    print(f"old_style({v!r}) = {old_style(v)}")
    print(f"new_style({v!r}) = {new_style(v)}")
    print()

# 类型守卫（isinstance 缩窄类型）
def process_value(value: int | str | list[int]) -> str:
    """演示 isinstance 作为类型守卫"""
    if isinstance(value, int):
        # 在此分支，value 类型被缩窄为 int
        return f"整数的两倍: {value * 2}"
    elif isinstance(value, str):
        # 在此分支，value 类型被缩窄为 str
        return f"大写字符串: {value.upper()}"
    else:
        # 在此分支，value 类型被缩窄为 list[int]
        return f"列表求和: {sum(value)}"

print("===类型守卫演示===")
for val in [10, "hello", [1, 2, 3, 4, 5]]:
    print(f"process_value({val!r}) = {process_value(val)}")
```

### 代码说明

**案例1代码解释**：
1. `case x if x < 0` 使用"守卫"（guard）条件，相当于 `case x: if x < 0:` 的组合
2. `case [a, b, *rest]` 匹配序列并将剩余部分捕获到 `rest`（星号模式）
3. `case {"type": "click", ...}` 只要字典包含这些键值对就匹配，不要求字典恰好只有这些键
4. `case _` 是通配符，不绑定变量，相当于 `else`

**案例2代码解释**：
1. `from __future__ import annotations` 让注解以字符串形式存储，避免运行时求值，所以 `int | str` 在注解中是安全的，即使在 Python 3.9 以下
2. 在实际运行逻辑中（不是注解），`isinstance(value, int)` 是最可靠的类型检查方式
3. mypy 和 pyright 等工具能理解 `isinstance` 的类型缩窄，在 `if isinstance(x, int):` 块内会把 x 视为 int

---

## 4. 代码质量工具

### 知识点解析

**概念定义**：代码质量工具是一组帮助我们写出更好代码的辅助程序，分为：**静态类型检查器**（如 mypy，运行前检查类型错误）、**代码格式化工具**（如 black，自动整理代码风格）、**代码风格检查工具**（如 pylint/flake8，检查 PEP8 规范和潜在问题）。就像写文章时的语法检查器、排版工具和内容审查员。

**核心规则**：
1. **mypy**：静态类型检查，安装：`pip install mypy`，运行：`mypy your_file.py`
2. **black**：自动代码格式化，安装：`pip install black`，运行：`black your_file.py`
3. **pylint**：综合代码检查，安装：`pip install pylint`，运行：`pylint your_file.py`
4. **flake8**：轻量级 PEP8 检查，安装：`pip install flake8`，运行：`flake8 your_file.py`
5. 推荐配置：在项目根目录添加 `pyproject.toml` 或 `.pylintrc` 统一配置

**常见易错点**：
1. mypy 默认宽松，`--strict` 模式才开启所有检查（推荐新项目使用）
2. black 的风格无需讨论，它是"无妥协"格式化工具，遵守即可，不要与它争论
3. pylint 分数不是绝对的，某些警告（如 `too-few-public-methods`）可以用 `# pylint: disable=xxx` 在必要时忽略
4. 类型注解不完整时 mypy 可能无法发现所有问题，`Any` 类型会跳过类型检查

### 实战案例

#### 案例1：mypy 类型检查示例
```python
# mypy 类型检查示例（展示有类型注解时能发现的问题）
from __future__ import annotations
from typing import Optional

print("===类型安全的代码===")

# 好的代码：类型注解完整，mypy 能全面检查
def safe_divide(a: float, b: float) -> Optional[float]:
    """安全除法：除数为0时返回 None"""
    if b == 0:
        return None
    return a / b

def format_result(result: Optional[float]) -> str:
    """格式化结果，处理 None 值"""
    if result is None:
        return "计算错误（除数为零）"
    return f"结果: {result:.4f}"

# 类型安全的使用方式
for a, b in [(10, 3), (10, 0), (7, 2)]:
    r = safe_divide(a, b)
    print(f"{a} / {b} = {format_result(r)}")

# 演示类型不匹配（运行时不报错，但 mypy 会警告）
def add_numbers(x: int, y: int) -> int:
    return x + y

print(f"\n正确使用: {add_numbers(3, 5)}")
# 下面这行运行不报错，但 mypy --strict 会报错：
# add_numbers("3", "5")  # mypy: Argument 1 to "add_numbers" has incompatible type "str"; expected "int"

# 完善的 API 设计（带类型注解）
class UserRegistry:
    """用户注册表（带类型注解的完整类）"""

    def __init__(self) -> None:
        self._users: dict[int, str] = {}
        self._next_id: int = 1

    def register(self, name: str) -> int:
        """注册用户，返回用户ID"""
        if not name.strip():
            raise ValueError("用户名不能为空")
        user_id = self._next_id
        self._users[user_id] = name
        self._next_id += 1
        return user_id

    def get_name(self, user_id: int) -> Optional[str]:
        """根据ID获取用户名"""
        return self._users.get(user_id)

    def list_users(self) -> list[tuple[int, str]]:
        """列出所有用户"""
        return list(self._users.items())

registry = UserRegistry()
id1 = registry.register("张三")
id2 = registry.register("李四")
print(f"\n注册用户 -> ID: {id1}, {id2}")
print(f"ID={id1} 的用户: {registry.get_name(id1)}")
print(f"所有用户: {registry.list_users()}")
```

#### 案例2：PEP8 规范与 pylint 配置
```python
# PEP8 规范演示：对比不规范与规范的写法
print("===PEP8 规范示例===")

# ❌ 不规范的代码（展示常见问题）
# （以下代码是反例，实际不运行这些不规范版本）
bad_code_example = """
# 问题1: 变量名不清晰，命名不规范
x=1  # 运算符周围无空格
y   =   2  # 多余空格

# 问题2: 函数名不遵循 snake_case
def MyFunction():pass  # 函数体在同一行

# 问题3: 行过长（超过79字符）
very_long_variable_name_that_is_way_too_long = some_function(argument_one, argument_two, argument_three)

# 问题4: 导入顺序混乱
import os, sys  # 多个导入在一行
"""

# ✅ 规范的代码
# 1. 命名规范
user_name = "张三"          # 变量：snake_case
MAX_RETRY_COUNT = 3          # 常量：UPPER_CASE
class UserAccount:           # 类名：PascalCase
    pass


def calculate_total_price(  # 函数：snake_case
    base_price: float,
    tax_rate: float = 0.13,
    discount: float = 0.0,
) -> float:
    """计算含税折扣后的总价。

    Args:
        base_price: 基础价格（必须为正数）
        tax_rate: 税率，默认13%
        discount: 折扣（0表示无折扣，0.1表示9折）

    Returns:
        计算后的总价

    Raises:
        ValueError: base_price 为负数时
    """
    if base_price < 0:
        raise ValueError(f"价格不能为负: {base_price}")
    discounted = base_price * (1 - discount)
    return discounted * (1 + tax_rate)


# 2. 适当的空行（类之间2行，方法之间1行）
import os    # 标准库
import json  # 标准库

# 演示规范代码
prices = [100.0, 250.0, 89.5]
for price in prices:
    total = calculate_total_price(price, discount=0.1)
    print(f"基础价: {price:.2f} -> 含税折后: {total:.2f}")

# 3. pyproject.toml 配置示例（注释说明）
config_example = """
# pyproject.toml 推荐配置

[tool.mypy]
python_version = "3.10"
strict = true
ignore_missing_imports = true

[tool.black]
line-length = 88
target-version = ["py310"]

[tool.pylint.messages_control]
disable = ["missing-module-docstring"]

[tool.flake8]
max-line-length = 88
extend-ignore = ["E203", "W503"]
"""
print(f"\n推荐的 pyproject.toml 配置片段:\n{config_example}")
```

### 代码说明

**案例1代码解释**：
1. 类型注解完整的代码让 mypy 能在运行前发现类型错误，如传入字符串给 `int` 参数
2. `Optional[float]` 的返回类型迫使调用者在使用结果前处理 None 的情况，避免 `NoneType has no attribute` 错误
3. 类的实例变量在 `__init__` 中完整注解，mypy 在访问不存在的属性时会警告

**案例2代码解释**：
1. PEP8 的核心原则：可读性高于简洁，空格让代码呼吸，命名让代码自文档化
2. 函数参数过多时，每个参数占一行（尾随逗号），方便 git diff 查看变更
3. 工具配置集中在 `pyproject.toml`，避免多个配置文件散落各处
4. mypy `strict` 模式等价于开启所有严格检查标志，新项目推荐从一开始使用

---

## 5. 知识点小结

| 特性 | Python版本 | 用途 |
|------|-----------|------|
| 基础类型注解 | 3.5+ | 变量和函数参数/返回值注解 |
| `Optional[T]` | 3.5+ | 可为 None 的类型 |
| `Union[X, Y]` | 3.5+ | 多种可能类型 |
| `dataclass` | 3.7+ | 自动生成数据类方法 |
| `frozen=True` | 3.7+ | 不可变数据类 |
| 内置泛型 `list[int]` | 3.9+ | 不需要 `from typing import List` |
| `X \| Y` 联合类型 | 3.10+ | `Union[X,Y]` 的语法糖 |
| `match/case` | 3.10+ | 结构模式匹配 |
| `kw_only=True` (dataclass) | 3.10+ | 字段仅关键字传入 |

**学习建议**：
1. 新项目从第一行代码就加类型注解，比后期补注解容易得多
2. 配合 IDE（PyCharm/VS Code）实时类型检查，随写随看
3. 先熟悉 `Optional`、`Union`、`list[T]`、`dict[K, V]`，足以覆盖80%的场景
4. `dataclass` 能替代大部分简单数据结构类，优先使用
5. 在 CI 流水线中加入 `mypy --strict` 检查，保持代码质量
