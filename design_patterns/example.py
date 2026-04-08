"""
Python 设计模式完整示例
演示内容：
1. 创建型：单例（Singleton）、工厂方法（Factory Method）
2. 结构型：装饰器（Decorator）、代理（Proxy）、适配器（Adapter）
3. 行为型：观察者（Observer）、策略（Strategy）、命令（Command）
4. Python 惯用法 vs GoF 传统模式对比
"""

from __future__ import annotations

import threading
import functools
import time
from abc import ABC, abstractmethod
from typing import Callable, Any

print("=" * 60)
print("Python 设计模式完整示例")
print("=" * 60)

# ============================================================
# 1. 单例模式（Singleton）
# ============================================================
print("\n【1. 单例模式】")


class DatabaseConnection:
    """线程安全的数据库连接单例"""
    _instance: DatabaseConnection | None = None
    _lock = threading.Lock()

    def __new__(cls, host: str = "localhost", port: int = 5432) -> DatabaseConnection:
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    instance = super().__new__(cls)
                    instance.host = host
                    instance.port = port
                    instance._connected = False
                    cls._instance = instance
        return cls._instance

    def connect(self) -> None:
        if not self._connected:
            print(f"  连接数据库: {self.host}:{self.port}")
            self._connected = True

    def execute(self, sql: str) -> str:
        if not self._connected:
            self.connect()
        return f"执行SQL: {sql}"

    def __repr__(self) -> str:
        return f"DB(id={id(self)}, host={self.host})"


db1 = DatabaseConnection("prod.db.com", 5432)
db2 = DatabaseConnection("other.com", 3306)  # 参数被忽略，返回已有实例
print(f"db1 is db2: {db1 is db2}")  # True
print(f"db1: {db1}")
print(f"db2: {db2}")  # 与db1相同
print(db2.execute("SELECT * FROM users"))


# Python 最简单的单例：模块级变量（天然单例）
class AppConfig:
    """应用配置（模块级单例）"""
    def __init__(self) -> None:
        self.settings: dict[str, Any] = {
            "debug": False,
            "version": "1.0.0",
            "max_connections": 100,
        }

    def get(self, key: str, default: Any = None) -> Any:
        return self.settings.get(key, default)

    def set(self, key: str, value: Any) -> None:
        self.settings[key] = value


# 模块级单例（在实际项目中，这个实例会在模块导入时创建一次）
_config = AppConfig()

def get_config() -> AppConfig:
    """获取全局配置（推荐的Python单例方式）"""
    return _config


cfg = get_config()
cfg.set("debug", True)
cfg2 = get_config()
print(f"\n配置单例: {cfg is cfg2}")
print(f"debug: {cfg2.get('debug')}")

# ============================================================
# 2. 工厂方法模式（Factory Method）
# ============================================================
print("\n【2. 工厂方法模式】")


class Logger(ABC):
    """日志器基类（产品接口）"""
    @abstractmethod
    def log(self, level: str, message: str) -> None:
        pass

    def info(self, msg: str) -> None:
        self.log("INFO", msg)

    def error(self, msg: str) -> None:
        self.log("ERROR", msg)


class ConsoleLogger(Logger):
    def log(self, level: str, message: str) -> None:
        colors = {"INFO": "\033[32m", "ERROR": "\033[31m", "RESET": "\033[0m"}
        color = colors.get(level, "")
        reset = colors["RESET"]
        print(f"  {color}[{level}]{reset} {message}")


class FileLogger(Logger):
    def __init__(self, filename: str) -> None:
        self.filename = filename

    def log(self, level: str, message: str) -> None:
        print(f"  [FILE:{self.filename}] [{level}] {message}")


class JsonLogger(Logger):
    def log(self, level: str, message: str) -> None:
        import json
        entry = {"level": level, "message": message, "ts": time.strftime("%H:%M:%S")}
        print(f"  [JSON] {json.dumps(entry, ensure_ascii=False)}")


# 工厂：字典注册表（Python风格，符合开闭原则）
class LoggerFactory:
    _registry: dict[str, Callable[..., Logger]] = {
        "console": lambda **kw: ConsoleLogger(),
        "file": lambda **kw: FileLogger(kw.get("filename", "app.log")),
        "json": lambda **kw: JsonLogger(),
    }

    @classmethod
    def create(cls, logger_type: str, **kwargs: Any) -> Logger:
        creator = cls._registry.get(logger_type)
        if not creator:
            raise ValueError(f"未知日志类型: {logger_type}（可用: {list(cls._registry)}）")
        return creator(**kwargs)

    @classmethod
    def register(cls, name: str, creator: Callable[..., Logger]) -> None:
        """扩展点：注册新类型（开闭原则：对扩展开放，对修改关闭）"""
        cls._registry[name] = creator


# 演示
for logger_type in ["console", "file", "json"]:
    logger = LoggerFactory.create(logger_type, filename="app.log")
    logger.info(f"应用启动（{logger_type}日志器）")
    logger.error("发现一个错误")

# 扩展：注册新类型，无需修改工厂
class SilentLogger(Logger):
    def log(self, level: str, message: str) -> None:
        pass  # 静默，用于测试


LoggerFactory.register("silent", lambda **kw: SilentLogger())
test_logger = LoggerFactory.create("silent")
test_logger.error("这条错误被静默了")
print("  [SILENT] 日志已静默（无输出）")

# ============================================================
# 3. 装饰器模式（Python @decorator 风格）
# ============================================================
print("\n【3. 装饰器模式（Python风格）】")


def timer(func: Callable) -> Callable:
    """计时装饰器"""
    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        print(f"  [TIMER] {func.__name__} 耗时 {elapsed*1000:.2f}ms")
        return result
    return wrapper


def cache_result(max_size: int = 64) -> Callable:
    """LRU缓存装饰器（带参数）"""
    def decorator(func: Callable) -> Callable:
        _cache: dict = {}
        _order: list = []

        @functools.wraps(func)
        def wrapper(*args: Any) -> Any:
            if args in _cache:
                print(f"  [CACHE] 命中: {func.__name__}{args}")
                return _cache[args]
            result = func(*args)
            _cache[args] = result
            _order.append(args)
            if len(_order) > max_size:
                oldest = _order.pop(0)
                del _cache[oldest]
            return result

        wrapper.cache_info = lambda: f"缓存大小: {len(_cache)}/{max_size}"
        return wrapper
    return decorator


def validate_types(**type_map: type) -> Callable:
    """类型验证装饰器（运行时类型检查）"""
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            import inspect
            sig = inspect.signature(func)
            bound = sig.bind(*args, **kwargs)
            for param_name, expected_type in type_map.items():
                if param_name in bound.arguments:
                    val = bound.arguments[param_name]
                    if not isinstance(val, expected_type):
                        raise TypeError(
                            f"{func.__name__}: 参数 '{param_name}' "
                            f"期望 {expected_type.__name__}，收到 {type(val).__name__}"
                        )
            return func(*args, **kwargs)
        return wrapper
    return decorator


# 叠加多个装饰器
@timer
@cache_result(max_size=10)
def compute_fibonacci(n: int) -> int:
    """计算斐波那契数（演示缓存效果）"""
    if n <= 1:
        return n
    return compute_fibonacci(n - 1) + compute_fibonacci(n - 2)


@validate_types(name=str, age=int, score=float)
def create_student_record(name: str, age: int, score: float) -> dict:
    return {"name": name, "age": age, "score": score}


print("斐波那契（带缓存+计时）:")
print(f"  fib(10) = {compute_fibonacci(10)}")
print(f"  fib(10) = {compute_fibonacci(10)}")  # 缓存命中
print(f"  {compute_fibonacci.cache_info()}")

print("\n类型验证装饰器:")
try:
    record = create_student_record("张三", 20, 95.5)
    print(f"  成功: {record}")
    create_student_record("李四", "二十", 88.0)  # 类型错误
except TypeError as e:
    print(f"  类型错误: {e}")

# ============================================================
# 4. 代理模式（Proxy）
# ============================================================
print("\n【4. 代理模式】")


class HeavyResource:
    """重量级资源（创建开销大）"""
    def __init__(self, name: str) -> None:
        print(f"  [资源] 加载 {name}（耗时操作...）")
        self.name = name
        self.data = f"{name} 的数据"

    def get_data(self) -> str:
        return self.data


class LazyProxy:
    """懒加载代理（延迟创建真实对象）"""
    def __init__(self, resource_name: str) -> None:
        self._resource_name = resource_name
        self._resource: HeavyResource | None = None

    def __getattr__(self, name: str) -> Any:
        if self._resource is None:
            self._resource = HeavyResource(self._resource_name)
        return getattr(self._resource, name)


# 代理只在真正需要时才创建资源
proxy = LazyProxy("大型配置文件")
print("代理创建完毕（资源尚未加载）")
data = proxy.get_data()  # 此时才加载
print(f"  获取数据: {data}")
data2 = proxy.get_data()  # 已加载，直接获取
print(f"  再次获取: {data2}")

# ============================================================
# 5. 观察者模式（Observer）
# ============================================================
print("\n【5. 观察者模式（事件系统）】")


class EventBus:
    """事件总线（解耦发布者和订阅者）"""

    def __init__(self) -> None:
        self._subscribers: dict[str, list[Callable]] = {}

    def subscribe(self, event: str, callback: Callable) -> None:
        self._subscribers.setdefault(event, []).append(callback)

    def unsubscribe(self, event: str, callback: Callable) -> None:
        if event in self._subscribers:
            self._subscribers[event] = [
                cb for cb in self._subscribers[event] if cb != callback
            ]

    def publish(self, event: str, **data: Any) -> None:
        for callback in self._subscribers.get(event, []):
            callback(**data)


# 创建事件总线
bus = EventBus()

# 订阅者（观察者）
def send_email_notification(user_id: int, order_id: str, amount: float) -> None:
    print(f"  [邮件] 用户{user_id}，订单{order_id}已支付 ¥{amount:.2f}")

def update_inventory(order_id: str, **kwargs: Any) -> None:
    print(f"  [库存] 处理订单{order_id}的库存扣减")

def generate_invoice(user_id: int, order_id: str, amount: float) -> None:
    print(f"  [发票] 为用户{user_id}生成订单{order_id}的发票（¥{amount:.2f}）")

def log_transaction(**data: Any) -> None:
    print(f"  [日志] 记录交易事件: {data}")


# 注册订阅者
bus.subscribe("order_paid", send_email_notification)
bus.subscribe("order_paid", update_inventory)
bus.subscribe("order_paid", generate_invoice)
bus.subscribe("order_paid", log_transaction)

# 发布事件（触发所有订阅者）
print("发布订单支付事件:")
bus.publish("order_paid", user_id=1001, order_id="ORD-2024001", amount=299.0)

# 取消订阅
print("\n取消邮件通知，再次发布:")
bus.unsubscribe("order_paid", send_email_notification)
bus.publish("order_paid", user_id=1002, order_id="ORD-2024002", amount=159.5)

# ============================================================
# 6. 策略模式（Strategy）
# ============================================================
print("\n【6. 策略模式（函数即策略）】")

# Python函数是一等公民，策略可以直接是函数
SortStrategy = Callable[[list], list]


def bubble_sort(arr: list) -> list:
    """冒泡排序（稳定，复杂度O(n²)）"""
    arr = arr.copy()
    for i in range(len(arr)):
        for j in range(len(arr) - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr


def python_sort(arr: list) -> list:
    """Python内置Timsort（最快，适合一般场景）"""
    return sorted(arr)


def reverse_sort(arr: list) -> list:
    """逆序排序"""
    return sorted(arr, reverse=True)


class DataProcessor:
    """数据处理器：可在运行时切换排序策略"""

    def __init__(self, sort_strategy: SortStrategy = python_sort) -> None:
        self.sort_strategy = sort_strategy

    def process(self, data: list) -> list:
        return self.sort_strategy(data)


data = [64, 34, 25, 12, 22, 11, 90]
processor = DataProcessor()

for strategy, name in [
    (bubble_sort, "冒泡排序"),
    (python_sort, "Python内置"),
    (reverse_sort, "逆序排序"),
]:
    processor.sort_strategy = strategy
    result = processor.process(data)
    print(f"  {name:12}: {result}")

# ============================================================
# 7. 命令模式（Command）
# ============================================================
print("\n【7. 命令模式（支持撤销）】")


class TextEditor:
    """简单文本编辑器（支持命令+撤销）"""

    def __init__(self) -> None:
        self._text = ""
        self._history: list[tuple[Callable, Callable]] = []  # (do, undo)

    def execute(self, do_fn: Callable, undo_fn: Callable) -> None:
        do_fn()
        self._history.append((do_fn, undo_fn))

    def undo(self) -> bool:
        if not self._history:
            return False
        _, undo_fn = self._history.pop()
        undo_fn()
        return True

    @property
    def text(self) -> str:
        return self._text

    def append(self, content: str) -> None:
        """追加文本（带撤销）"""
        old_text = self._text

        def do() -> None:
            self._text += content

        def undo() -> None:
            self._text = old_text

        self.execute(do, undo)

    def replace(self, old: str, new: str) -> None:
        """替换文本（带撤销）"""
        old_text = self._text

        def do() -> None:
            self._text = self._text.replace(old, new)

        def undo() -> None:
            self._text = old_text

        self.execute(do, undo)


editor = TextEditor()
editor.append("Hello")
editor.append(", World")
editor.append("!")
print(f"初始文本: {editor.text!r}")

editor.replace("World", "Python")
print(f"替换后: {editor.text!r}")

editor.undo()
print(f"撤销替换: {editor.text!r}")

editor.undo()
editor.undo()
print(f"撤销2次: {editor.text!r}")

# ============================================================
# 8. 设计模式总结
# ============================================================
print("\n【8. 设计模式总结】")
summary = [
    ("单例", "全局唯一实例", "Python模块级变量最简洁"),
    ("工厂方法", "解耦对象创建", "字典注册表实现扩展点"),
    ("装饰器", "动态增加功能", "@decorator语法，叠加使用"),
    ("代理", "控制对象访问", "__getattr__ 实现透明代理"),
    ("观察者", "事件驱动通知", "EventBus解耦发布者/订阅者"),
    ("策略", "算法族可切换", "函数作为策略，运行时替换"),
    ("命令", "请求封装为对象", "支持撤销的do/undo函数对"),
]
print(f"  {'模式':8} {'用途':20} {'Python风格实现'}")
print("  " + "-" * 60)
for name, purpose, impl in summary:
    print(f"  {name:8} {purpose:20} {impl}")
