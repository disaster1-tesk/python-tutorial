"""
Python 类型注解与代码质量示例
演示内容：
1. 基础类型注解（变量、函数参数、返回值）
2. typing 模块（Optional、Union、Callable、TypeVar）
3. dataclasses 装饰器
4. Python 3.10+ 新语法（match/case、X|Y联合类型）
5. 代码质量工具使用指南
"""

from __future__ import annotations

import sys
import json
from dataclasses import dataclass, field, asdict
from typing import Optional, Union, Callable, TypeVar, Any, ClassVar

print("=" * 60)
print("Python 类型注解与代码质量完整示例")
print("=" * 60)

# ============================================================
# 1. 基础类型注解
# ============================================================
print("\n【1. 基础类型注解】")

# 变量注解
name: str = "张三"
age: int = 25
score: float = 98.5
is_active: bool = True
tags: list[str] = ["Python", "类型注解"]
scores_map: dict[str, float] = {"数学": 95.0, "英语": 88.5}
coords: tuple[float, float] = (39.9, 116.4)

print(f"变量注解示例: name={name!r}, age={age}, score={score}")


# 函数参数与返回值注解
def greet(name: str, age: int, greeting: Optional[str] = None) -> str:
    """生成问候语，greeting 为 None 时使用默认值"""
    if greeting is None:
        greeting = "你好"
    return f"{greeting}，{name}！你今年 {age} 岁了。"


print(greet("李四", 30))
print(greet("王五", 25, "嗨"))


# Optional 和 Union 的实际用法
def find_user(user_id: int) -> Optional[dict[str, str]]:
    """查找用户，不存在返回 None"""
    db = {1: {"name": "张三", "role": "admin"}, 2: {"name": "李四", "role": "user"}}
    return db.get(user_id)


user = find_user(1)
if user is not None:
    print(f"找到用户: {user['name']}（{user['role']}）")

missing = find_user(99)
print(f"未找到用户: {missing is None}")


def process_id(user_id: Union[int, str]) -> str:
    """接受 int 或 str 两种 ID 格式"""
    return f"ID: {str(user_id).zfill(8)}"


print(process_id(42))
print(process_id("U00123"))

# ============================================================
# 2. 高级类型：Callable 和 TypeVar
# ============================================================
print("\n【2. 高级类型：Callable 和 TypeVar】")

T = TypeVar("T")


def apply_twice(func: Callable[[int], int], value: int) -> int:
    """将函数连续应用两次"""
    return func(func(value))


def double(x: int) -> int:
    return x * 2


def square(x: int) -> int:
    return x * x


print(f"apply_twice(double, 3)  = {apply_twice(double, 3)}")   # 12
print(f"apply_twice(square, 2)  = {apply_twice(square, 2)}")   # 16


def first_or_default(items: list[T], default: T) -> T:
    """返回列表第一个元素，空列表返回默认值（泛型）"""
    return items[0] if items else default


print(f"first_or_default([1,2,3], 0)   = {first_or_default([1, 2, 3], 0)}")
print(f"first_or_default([], 0)         = {first_or_default([], 0)}")
print(f"first_or_default(['a','b'], '') = {first_or_default(['a', 'b'], '')}")
print(f"first_or_default([], 'N/A')     = {first_or_default([], 'N/A')}")

# ============================================================
# 3. dataclasses 装饰器
# ============================================================
print("\n【3. dataclasses 装饰器】")


@dataclass
class Student:
    """学生数据类：自动生成 __init__、__repr__、__eq__"""
    name: str
    student_id: str
    age: int
    scores: list[float] = field(default_factory=list)  # 可变默认值
    grade: Optional[str] = None

    def __post_init__(self) -> None:
        """初始化后自动验证"""
        if not 0 < self.age < 150:
            raise ValueError(f"年龄无效: {self.age}")
        # 格式化学号
        if not self.student_id.startswith("S"):
            # dataclass frozen=False 时可以修改字段
            object.__setattr__(self, "student_id", "S" + self.student_id)

    @property
    def average_score(self) -> Optional[float]:
        return sum(self.scores) / len(self.scores) if self.scores else None

    def add_score(self, score: float) -> None:
        if not 0 <= score <= 100:
            raise ValueError(f"成绩超出范围: {score}")
        self.scores.append(score)
        avg = self.average_score
        if avg is not None:
            thresholds = [(90, "优秀"), (80, "良好"), (70, "中等"), (60, "及格")]
            self.grade = next(
                (g for threshold, g in thresholds if avg >= threshold),
                "不及格",
            )


# 演示 dataclass 自动生成的方法
s1 = Student(name="张三", student_id="001", age=20)
s2 = Student(name="李四", student_id="S002", age=22)
print(f"s1 = {s1}")         # 自动生成的 __repr__
print(f"s1 == s2: {s1 == s2}")   # 自动生成的 __eq__

s1.add_score(88)
s1.add_score(95)
s1.add_score(82)
print(f"平均分: {s1.average_score:.2f}")
print(f"等级: {s1.grade}")

# asdict 用于序列化
student_dict = asdict(s1)
print(f"序列化: {json.dumps(student_dict, ensure_ascii=False)}")


# 不可变数据类
@dataclass(frozen=True)
class Color:
    """不可变 RGB 颜色类"""
    r: int
    g: int
    b: int
    DESCRIPTION: ClassVar[str] = "RGB颜色"

    def __post_init__(self) -> None:
        for name_val, val in [("r", self.r), ("g", self.g), ("b", self.b)]:
            if not 0 <= val <= 255:
                raise ValueError(f"{name_val} 超出范围: {val}")

    def to_hex(self) -> str:
        return f"#{self.r:02X}{self.g:02X}{self.b:02X}"

    def blend(self, other: Color) -> Color:
        return Color(
            (self.r + other.r) // 2,
            (self.g + other.g) // 2,
            (self.b + other.b) // 2,
        )


red = Color(255, 0, 0)
blue = Color(0, 0, 255)
purple = red.blend(blue)
print(f"\n颜色混合: {red.to_hex()} + {blue.to_hex()} = {purple.to_hex()}")

# 冻结实例不可修改
try:
    red.r = 100  # type: ignore[misc]
except Exception as e:
    print(f"尝试修改冻结实例: {type(e).__name__}")

# ============================================================
# 4. Python 3.10+ 新语法
# ============================================================
print("\n【4. Python 3.10+ 新语法】")


def describe_type(value: Any) -> str:
    """类型描述（Python 3.10+ match/case）"""
    if sys.version_info >= (3, 10):
        # Python 3.10+ 可以使用 match/case
        # 由于语法兼容性，这里用字符串形式展示，实际运行用 isinstance 替代
        pass

    # 兼容写法（所有版本都支持）
    if isinstance(value, bool):
        return f"布尔值: {value}"
    elif isinstance(value, int):
        return f"整数: {value}"
    elif isinstance(value, float):
        return f"浮点数: {value:.2f}"
    elif isinstance(value, str):
        return f"字符串: {value!r}"
    elif isinstance(value, list):
        return f"列表（{len(value)}个元素）"
    elif isinstance(value, dict):
        return f"字典（{len(value)}个键）"
    else:
        return f"其他类型: {type(value).__name__}"


test_values: list[Any] = [True, 42, 3.14, "hello", [1, 2, 3], {"a": 1}]
for v in test_values:
    print(f"  {describe_type(v)}")

# Python 3.10+ X|Y 联合类型（注解中使用，配合 __future__.annotations）
def new_union_example(value: int | str | None) -> str:
    """Python 3.10+ 联合类型语法（在注解中有效，因为有 __future__.annotations）"""
    if value is None:
        return "空值"
    if isinstance(value, int):
        return f"整数: {value}"
    return f"字符串: {value}"


print(f"\n联合类型: {new_union_example(42)}")
print(f"联合类型: {new_union_example('hello')}")
print(f"联合类型: {new_union_example(None)}")

# ============================================================
# 5. 实战：带完整类型注解的库存管理系统
# ============================================================
print("\n【5. 实战：带类型注解的库存管理系统】")


@dataclass
class Product:
    """商品数据类"""
    product_id: str
    name: str
    price: float
    stock: int = 0
    category: str = "未分类"

    def __post_init__(self) -> None:
        if self.price < 0:
            raise ValueError(f"价格不能为负: {self.price}")
        if self.stock < 0:
            raise ValueError(f"库存不能为负: {self.stock}")


class Inventory:
    """库存管理系统（带完整类型注解）"""

    def __init__(self) -> None:
        self._products: dict[str, Product] = {}

    def add_product(self, product: Product) -> None:
        """添加商品"""
        if product.product_id in self._products:
            raise ValueError(f"商品ID已存在: {product.product_id}")
        self._products[product.product_id] = product
        print(f"✓ 添加商品: {product.name}（ID: {product.product_id}）")

    def restock(self, product_id: str, quantity: int) -> None:
        """补充库存"""
        if product_id not in self._products:
            raise KeyError(f"商品不存在: {product_id}")
        if quantity <= 0:
            raise ValueError(f"补货数量必须为正数: {quantity}")
        self._products[product_id].stock += quantity

    def sell(self, product_id: str, quantity: int) -> float:
        """销售商品，返回总金额"""
        product = self._products.get(product_id)
        if product is None:
            raise KeyError(f"商品不存在: {product_id}")
        if product.stock < quantity:
            raise ValueError(f"库存不足: 现有 {product.stock}，需要 {quantity}")
        product.stock -= quantity
        return product.price * quantity

    def get_low_stock(self, threshold: int = 10) -> list[Product]:
        """获取低库存商品列表"""
        return [p for p in self._products.values() if p.stock < threshold]

    def search_by_category(self, category: str) -> list[Product]:
        """按分类搜索商品"""
        return [p for p in self._products.values() if p.category == category]

    def total_value(self) -> float:
        """计算库存总价值"""
        return sum(p.price * p.stock for p in self._products.values())


# 使用库存系统
inventory = Inventory()

# 添加商品
products = [
    Product("P001", "Python编程书", 89.9, 50, "图书"),
    Product("P002", "机械键盘", 399.0, 8, "电子产品"),
    Product("P003", "笔记本", 15.5, 200, "文具"),
    Product("P004", "鼠标", 99.0, 5, "电子产品"),
]
for p in products:
    inventory.add_product(p)

# 销售
revenue = inventory.sell("P001", 3)
print(f"销售3本书，收入: ¥{revenue:.2f}")

# 补货
inventory.restock("P002", 20)

# 查询低库存
print("\n低库存商品（< 10）:")
for p in inventory.get_low_stock(10):
    print(f"  {p.name}: {p.stock} 件（¥{p.price}）")

# 按分类查询
print("\n电子产品:")
for p in inventory.search_by_category("电子产品"):
    print(f"  {p.name}: {p.stock} 件")

print(f"\n库存总价值: ¥{inventory.total_value():.2f}")

# ============================================================
# 6. 类型注解最佳实践总结
# ============================================================
print("\n【6. 最佳实践总结】")
tips = [
    "✓ 新项目从第一行就加类型注解，养成习惯",
    "✓ Optional[T] 用于可能为 None 的值，不要省略",
    "✓ dataclass 替代只存储数据的简单类",
    "✓ field(default_factory=list) 代替 = []",
    "✓ from __future__ import annotations 兼容旧版写法",
    "✓ 在 CI 中加入 mypy --strict 保证类型安全",
    "✓ black 自动格式化，不与它争论风格",
]
for tip in tips:
    print(f"  {tip}")
