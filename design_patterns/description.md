# Python 设计模式

## 1. 创建型模式

### 知识点解析

**概念定义**：创建型模式关注"如何创建对象"，目标是将对象的创建与使用解耦，使代码更灵活、可扩展。常见的有：单例（Singleton）、工厂方法（Factory Method）、抽象工厂（Abstract Factory）、建造者（Builder）。

---

### 1.1 单例模式（Singleton）

**概念**：确保一个类只有一个实例，并提供全局访问点。就像全公司只有一台打印机，任何人要打印都使用同一台。

**Python 实现方式对比**：

| 方式 | 线程安全 | 代码简洁度 | 说明 |
|------|---------|----------|------|
| `__new__` 方法 | 需加锁 | 中等 | 最常见，控制实例创建 |
| 模块级变量 | ✅ 是 | 最简洁 | 利用Python模块导入机制天然单例 |
| 装饰器 | 需加锁 | 简洁 | 通用，可复用 |
| 元类 | 需加锁 | 复杂 | 最Pythonic，透明 |

**常见易错点**：
1. 单例在多线程环境下不加锁可能创建多个实例（双重检查锁定）
2. 单例难以测试（单元测试时状态共享）——可通过依赖注入规避
3. 滥用单例让代码隐式依赖全局状态，增加耦合

### 实战案例

#### 案例1：配置管理器（单例）
```python
# 单例模式：配置管理器
import threading

print("===单例模式===")

class ConfigManager:
    """线程安全的配置管理器单例"""
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:  # 双重检查锁定
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._config = {}
                    cls._instance._initialized = False
        return cls._instance

    def initialize(self, config: dict) -> None:
        """初始化配置（只执行一次）"""
        if not self._initialized:
            self._config.update(config)
            self._initialized = True
            print(f"配置初始化: {list(config.keys())}")
        else:
            print("配置已初始化，跳过")

    def get(self, key: str, default=None):
        return self._config.get(key, default)

    def set(self, key: str, value) -> None:
        self._config[key] = value

    def __repr__(self) -> str:
        return f"ConfigManager(id={id(self)}, keys={list(self._config.keys())})"

# 演示
cfg1 = ConfigManager()
cfg2 = ConfigManager()
print(f"cfg1 is cfg2: {cfg1 is cfg2}")  # True，同一实例

cfg1.initialize({"db_host": "localhost", "debug": True, "port": 8080})
cfg2.initialize({"other": "value"})  # 已初始化，跳过

print(f"db_host: {cfg2.get('db_host')}")  # 从同一实例读取
cfg1.set("version", "1.0.0")
print(f"version (via cfg2): {cfg2.get('version')}")  # cfg2 也能读到

# 装饰器方式的单例
def singleton(cls):
    """单例装饰器"""
    instances = {}
    _lock = threading.Lock()
    def get_instance(*args, **kwargs):
        if cls not in instances:
            with _lock:
                if cls not in instances:
                    instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return get_instance

@singleton
class DatabasePool:
    def __init__(self, size: int = 5):
        self.size = size
        print(f"创建数据库连接池（size={size}）")

pool1 = DatabasePool(5)
pool2 = DatabasePool(10)  # 不会再创建，返回已有实例
print(f"pool1 is pool2: {pool1 is pool2}")
print(f"pool size: {pool2.size}")  # 还是5，因为只创建了一次
```

---

### 1.2 工厂模式（Factory）

**概念**：定义创建对象的接口，但让子类决定实例化哪个类。工厂方法让类的实例化延迟到子类中进行。就像汽车工厂——下单说要什么车型，工厂帮你生产，你不需要知道车怎么造的。

**简单工厂 vs 工厂方法 vs 抽象工厂**：
- **简单工厂**：一个函数/类根据参数创建不同对象（严格来说不是设计模式）
- **工厂方法**：定义接口，每个子类实现自己的创建逻辑
- **抽象工厂**：创建一族相关对象，保证产品系列的一致性

### 实战案例

#### 案例2：通知系统（工厂 + 策略）
```python
# 工厂模式：通知系统
from abc import ABC, abstractmethod

print("\n===工厂模式：通知系统===")

class Notification(ABC):
    """通知基类（产品接口）"""
    @abstractmethod
    def send(self, recipient: str, message: str) -> bool:
        pass
    
    @abstractmethod
    def get_type(self) -> str:
        pass

class EmailNotification(Notification):
    def __init__(self, smtp_host: str):
        self.smtp_host = smtp_host
    
    def send(self, recipient: str, message: str) -> bool:
        print(f"[邮件] {self.smtp_host} -> {recipient}: {message[:30]}...")
        return True
    
    def get_type(self) -> str:
        return "email"

class SMSNotification(Notification):
    def __init__(self, api_key: str):
        self.api_key = api_key
    
    def send(self, recipient: str, message: str) -> bool:
        print(f"[短信] API:{self.api_key[:4]}**** -> {recipient}: {message[:20]}...")
        return True
    
    def get_type(self) -> str:
        return "sms"

class PushNotification(Notification):
    def send(self, recipient: str, message: str) -> bool:
        print(f"[推送] -> {recipient}: {message[:25]}...")
        return True
    
    def get_type(self) -> str:
        return "push"

# 工厂类
class NotificationFactory:
    """通知工厂：根据类型创建通知对象"""
    _creators = {
        "email": lambda config: EmailNotification(config.get("smtp_host", "smtp.example.com")),
        "sms":   lambda config: SMSNotification(config.get("api_key", "default_key")),
        "push":  lambda config: PushNotification(),
    }
    
    @classmethod
    def create(cls, notification_type: str, config: dict = None) -> Notification:
        creator = cls._creators.get(notification_type)
        if not creator:
            raise ValueError(f"不支持的通知类型: {notification_type}")
        return creator(config or {})
    
    @classmethod
    def register(cls, type_name: str, creator) -> None:
        """扩展：注册新的通知类型（开闭原则）"""
        cls._creators[type_name] = creator

# 演示
config = {"smtp_host": "mail.myapp.com", "api_key": "sk_test_abc123"}
for ntype in ["email", "sms", "push"]:
    notifier = NotificationFactory.create(ntype, config)
    notifier.send("user@example.com", "您的订单已发货，请注意查收！")

# 扩展新的通知类型（不修改工厂代码）
class WeChatNotification(Notification):
    def send(self, recipient: str, message: str) -> bool:
        print(f"[微信] -> {recipient}: {message[:20]}...")
        return True
    def get_type(self) -> str:
        return "wechat"

NotificationFactory.register("wechat", lambda c: WeChatNotification())
wechat = NotificationFactory.create("wechat")
wechat.send("openid_12345", "消息通知")
```

---

## 2. 结构型模式

### 知识点解析

**概念定义**：结构型模式关注"如何组合对象和类"，将对象和类组合成更大的结构。常见的有：装饰器（Decorator）、代理（Proxy）、适配器（Adapter）、组合（Composite）。

---

### 2.1 装饰器模式（Decorator）

**Python 装饰器语法 vs GoF 装饰器模式对比**：

| 对比点 | Python @装饰器 | GoF 装饰器模式 |
|-------|-------------|--------------|
| 本质 | 函数包装函数 | 对象包装对象 |
| 语法 | `@decorator` 语法糖 | 继承同一接口 |
| 典型用途 | 函数功能增强（日志、缓存、权限） | 运行时动态组合功能 |
| 可组合性 | 叠加多个 `@decorator` | 链式包装多个装饰器类 |

### 实战案例

#### 案例3：缓存与权限装饰器
```python
# 装饰器模式实战
import functools
import time

print("\n===装饰器模式（Python风格）===")

def log_call(func):
    """日志装饰器"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print(f"[LOG] 调用 {func.__name__}{args}")
        result = func(*args, **kwargs)
        print(f"[LOG] {func.__name__} 返回 {result}")
        return result
    return wrapper

def cache(max_size: int = 128):
    """缓存装饰器（带参数）"""
    def decorator(func):
        _cache = {}
        @functools.wraps(func)
        def wrapper(*args):
            if args not in _cache:
                if len(_cache) >= max_size:
                    _cache.pop(next(iter(_cache)))
                _cache[args] = func(*args)
            else:
                print(f"  [CACHE] 命中缓存: {func.__name__}{args}")
            return _cache[args]
        wrapper.cache = _cache  # 暴露缓存供检查
        return wrapper
    return decorator

def retry(max_attempts: int = 3, delay: float = 0.1):
    """重试装饰器"""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts - 1:
                        raise
                    print(f"  [RETRY] {func.__name__} 失败 ({attempt+1}/{max_attempts}): {e}")
                    time.sleep(delay)
        return wrapper
    return decorator

# 叠加使用多个装饰器
@log_call
@cache(max_size=10)
def fibonacci(n: int) -> int:
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

print("斐波那契数列（带日志+缓存）:")
for i in [5, 5, 8]:  # 5会被缓存
    print(f"  fibonacci({i}) = {fibonacci(i)}")
print(f"缓存大小: {len(fibonacci.cache)}")

# GoF 装饰器模式（对象包装）
print("\n===GoF 装饰器模式（对象包装）===")

from abc import ABC, abstractmethod

class DataSource(ABC):
    @abstractmethod
    def write(self, data: str) -> None:
        pass
    
    @abstractmethod
    def read(self) -> str:
        pass

class FileDataSource(DataSource):
    """具体组件：文件数据源"""
    def __init__(self, filename: str):
        self.filename = filename
        self._data = ""
    
    def write(self, data: str) -> None:
        self._data = data
        print(f"[文件] 写入: {data[:30]}")
    
    def read(self) -> str:
        return self._data

class DataSourceDecorator(DataSource):
    """装饰器基类"""
    def __init__(self, source: DataSource):
        self._source = source
    
    def write(self, data: str) -> None:
        self._source.write(data)
    
    def read(self) -> str:
        return self._source.read()

class EncryptionDecorator(DataSourceDecorator):
    """加密装饰器"""
    def write(self, data: str) -> None:
        encrypted = data[::-1]  # 简化：反转字符串模拟加密
        print(f"[加密] {data[:20]}... -> {encrypted[:20]}...")
        super().write(encrypted)
    
    def read(self) -> str:
        data = super().read()
        return data[::-1]  # 解密

class CompressionDecorator(DataSourceDecorator):
    """压缩装饰器"""
    def write(self, data: str) -> None:
        compressed = data[::2]  # 简化：每隔一个字符模拟压缩
        print(f"[压缩] {len(data)}字节 -> {len(compressed)}字节")
        super().write(compressed)
    
    def read(self) -> str:
        return super().read()

# 链式组合：文件 -> 加密 -> 压缩
file_source = FileDataSource("data.txt")
encrypted_source = EncryptionDecorator(file_source)
compressed_encrypted_source = CompressionDecorator(encrypted_source)

original = "Hello, Python Design Patterns! 这是测试数据。"
print(f"\n原始数据: {original}")
compressed_encrypted_source.write(original)
```

---

## 3. 行为型模式

### 知识点解析

**概念定义**：行为型模式关注"对象之间如何协作、通信和分配责任"。常见的有：观察者（Observer）、策略（Strategy）、命令（Command）、模板方法（Template Method）、迭代器（Iterator）。

---

### 3.1 观察者模式（Observer）

**概念**：定义对象间的一对多依赖，当一个对象状态改变时，所有依赖者（观察者）自动收到通知。就像微博关注：粉丝（观察者）关注博主（被观察者），博主发新微博，所有粉丝都收到通知。

### 实战案例

#### 案例4：事件系统（观察者）
```python
# 观察者模式：事件系统
from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Callable

print("\n===观察者模式：事件系统===")

class EventEmitter:
    """事件发射器（Python风格的观察者模式）"""
    def __init__(self):
        self._listeners: dict[str, list[Callable]] = {}
    
    def on(self, event: str, callback: Callable) -> None:
        """注册事件监听器"""
        if event not in self._listeners:
            self._listeners[event] = []
        self._listeners[event].append(callback)
    
    def off(self, event: str, callback: Callable) -> None:
        """移除事件监听器"""
        if event in self._listeners:
            self._listeners[event] = [
                cb for cb in self._listeners[event] if cb != callback
            ]
    
    def emit(self, event: str, *args, **kwargs) -> None:
        """触发事件"""
        for callback in self._listeners.get(event, []):
            callback(*args, **kwargs)

class Stock(EventEmitter):
    """股票（被观察者）"""
    def __init__(self, symbol: str, price: float):
        super().__init__()
        self.symbol = symbol
        self._price = price
    
    @property
    def price(self) -> float:
        return self._price
    
    @price.setter
    def price(self, new_price: float) -> None:
        old_price = self._price
        self._price = new_price
        change_pct = (new_price - old_price) / old_price * 100
        self.emit("price_change", self.symbol, old_price, new_price, change_pct)
        if abs(change_pct) >= 5:
            self.emit("alert", self.symbol, change_pct)

# 监听器函数
def price_logger(symbol, old, new, change_pct):
    direction = "▲" if new > old else "▼"
    print(f"  [LOG] {symbol}: ¥{old:.2f} {direction} ¥{new:.2f} ({change_pct:+.1f}%)")

def alert_handler(symbol, change_pct):
    print(f"  ⚠️  [ALERT] {symbol} 涨跌幅超过5%: {change_pct:+.1f}%，请注意！")

def auto_trade(symbol, old, new, change_pct):
    if change_pct <= -3:
        print(f"  [交易] {symbol} 下跌{abs(change_pct):.1f}%，触发止损卖出")
    elif change_pct >= 5:
        print(f"  [交易] {symbol} 上涨{change_pct:.1f}%，获利了结")

# 注册监听器
stock = Stock("BABA", 100.0)
stock.on("price_change", price_logger)
stock.on("price_change", auto_trade)
stock.on("alert", alert_handler)

print("股价变动追踪:")
for new_price in [102.0, 98.5, 93.0, 105.5]:
    stock.price = new_price
```

---

### 3.2 策略模式（Strategy）

**概念**：定义一族算法，将每个算法封装起来，使它们可以互换。策略模式让算法的变化独立于使用它的客户端。就像导航软件提供多种路线策略：最快路线、最短路线、避开高速——用户可以随时切换。

**Python 中的策略模式**：Python 函数是一等公民，策略可以直接用函数代替，无需专门的策略类。

### 实战案例

#### 案例5：排序策略 + 优惠计算策略
```python
# 策略模式：优惠计算
from typing import Callable

print("\n===策略模式：优惠计算===")

# 1. 函数风格的策略（更Pythonic）
DiscountStrategy = Callable[[float, int], float]  # 价格, 数量 -> 折后价

def no_discount(price: float, qty: int) -> float:
    return price * qty

def bulk_discount(price: float, qty: int) -> float:
    """批量优惠：超过10件打8折"""
    total = price * qty
    return total * 0.8 if qty >= 10 else total

def vip_discount(price: float, qty: int) -> float:
    """VIP优惠：统一9折"""
    return price * qty * 0.9

def festival_discount(price: float, qty: int) -> float:
    """节日优惠：满100减20"""
    total = price * qty
    return total - (total // 100) * 20

class ShoppingCart:
    def __init__(self, discount_strategy: DiscountStrategy = no_discount):
        self._items: list[dict] = []
        self.discount_strategy = discount_strategy  # 运行时可切换
    
    def add_item(self, name: str, price: float, qty: int) -> None:
        self._items.append({"name": name, "price": price, "qty": qty})
    
    def total(self) -> float:
        return sum(
            self.discount_strategy(item["price"], item["qty"])
            for item in self._items
        )
    
    def print_bill(self, strategy_name: str) -> None:
        print(f"\n购物车（{strategy_name}）:")
        for item in self._items:
            subtotal = self.discount_strategy(item["price"], item["qty"])
            print(f"  {item['name']:10} x{item['qty']:3} = ¥{subtotal:.2f}")
        print(f"  {'合计':>10}       = ¥{self.total():.2f}")

cart = ShoppingCart()
cart.add_item("Python书", 89.9, 2)
cart.add_item("键盘", 399.0, 1)
cart.add_item("鼠标", 99.0, 12)  # 超过10件

# 切换不同优惠策略
strategies = [
    (no_discount, "无优惠"),
    (bulk_discount, "批量优惠"),
    (vip_discount, "VIP优惠"),
    (festival_discount, "节日优惠"),
]
for strategy, name in strategies:
    cart.discount_strategy = strategy  # 动态切换策略
    cart.print_bill(name)
```

---

## 4. 设计模式 vs Python 惯用法

### 对比分析

| 设计模式 | 传统GoF实现 | Python惯用法 |
|---------|-----------|-------------|
| 单例 | `__new__` + 锁 | 模块级变量（天然单例） |
| 工厂方法 | 继承+抽象方法 | 函数 / 字典映射 / `__init_subclass__` |
| 装饰器 | 类继承组合 | `@装饰器` 函数 |
| 策略 | 策略类 + 接口 | 函数作为参数（一等公民） |
| 观察者 | Observer接口 | 函数回调 / 信号槽 |
| 迭代器 | Iterator类 | 生成器函数 + `yield` |
| 命令 | Command类 | lambda 或 functools.partial |

### Python 最佳实践

**何时用设计模式，何时用 Python 惯用法**：

1. **优先使用语言特性**：Python 的装饰器、生成器、函数式编程特性已经内置了很多模式
2. **当代码复杂度值得时才用正式模式**：简单脚本不需要工厂方法
3. **开闭原则很重要**：工厂+注册表让新增功能不修改已有代码
4. **不要过度设计**：3个类能解决的问题不要变成15个类

---

## 5. 知识点小结

**创建型**（解决"怎么创建对象"）：
- **单例**：全局唯一实例；Python模块最简单
- **工厂方法**：解耦创建与使用；字典+函数是Python风格
- **建造者**：分步构造复杂对象；`dataclass` + `Builder`方法链

**结构型**（解决"怎么组合对象"）：
- **装饰器**：动态增加功能；Python `@decorator` 语法天然支持
- **代理**：控制对象访问；`__getattr__` 实现透明代理
- **适配器**：接口转换；继承或组合

**行为型**（解决"对象怎么协作"）：
- **观察者**：事件驱动；回调函数 / 信号槽
- **策略**：算法族可切换；函数作为参数
- **命令**：请求封装为对象；`functools.partial` / 函数对象
- **模板方法**：骨架+钩子；抽象基类（`abc.ABC`）
