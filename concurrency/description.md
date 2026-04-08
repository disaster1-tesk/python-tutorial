# Python 并发编程

## 1. GIL 与并发模型概述

### 知识点解析

**概念定义**：并发是指多个任务在同一时间段内交替执行，并行是多个任务真正同时执行。Python 的并发编程有三种主要模型：**多线程**（threading）、**多进程**（multiprocessing）、**异步 I/O**（asyncio）。

**GIL（全局解释器锁）**：CPython（官方 Python）有一把全局锁，同一时刻只允许一个线程执行 Python 字节码。就像一间办公室只有一把钥匙，多个员工（线程）轮流拿钥匙干活——虽然他们都在"工作"，但同一时刻只有一人在真正执行 Python 代码。

**三种模型适用场景对比**：

| 模型 | 适用场景 | GIL影响 | 资源开销 |
|------|---------|--------|---------|
| 多线程（threading） | I/O 密集型（网络请求、文件读写） | 有GIL，但I/O时会释放 | 低 |
| 多进程（multiprocessing） | CPU 密集型（计算、图像处理） | 每个进程独立GIL | 高 |
| 异步（asyncio） | 高并发 I/O（大量网络请求） | 单线程，无GIL问题 | 极低 |

**核心规则**：
1. I/O 密集型任务（等待网络/磁盘）→ 多线程或异步，GIL 在等待时会释放
2. CPU 密集型任务（大量计算）→ 多进程绕过 GIL
3. 需要处理成千上万并发连接 → asyncio 效率最高
4. 第三方库（如 numpy）内部操作期间会释放 GIL，可用多线程加速

**常见易错点**：
1. 认为多线程能加速 CPU 密集型任务——受 GIL 限制，效果往往不如单线程
2. 多进程中传递不可 pickle 的对象（如 lambda、本地函数）会报错
3. 在 asyncio 中调用阻塞函数（如 `time.sleep`）会阻塞整个事件循环，应用 `asyncio.sleep`
4. 忘记给多线程共享数据加锁，导致竞态条件（race condition）

---

## 2. 多线程（threading）

### 知识点解析

**概念定义**：线程是进程内的执行单元，共享进程的内存空间。多线程就像一个公司里多个员工共用同一套办公设备，协作完成工作。

**核心规则**：
1. 使用 `threading.Thread(target=func, args=(...))` 创建线程
2. `thread.start()` 启动线程，`thread.join()` 等待线程结束
3. `threading.Lock()` 创建互斥锁，`lock.acquire()` + `lock.release()` 或 `with lock:` 保护共享数据
4. `ThreadPoolExecutor` 是线程池的推荐用法，比手动管理线程更简洁
5. `threading.local()` 创建线程本地变量，每个线程有独立副本

**常见易错点**：
1. 不加锁修改共享变量导致结果不确定（竞态条件）
2. 死锁：两个线程互相等待对方释放锁
3. 线程数量过多导致频繁上下文切换，性能下降
4. 在线程函数中捕获异常，否则异常会被静默丢弃

### 实战案例

#### 案例1：线程基础与锁
```python
# 多线程基础
import threading
import time

print("===多线程基础===")

# 1. 简单线程创建
def worker(name: str, duration: float) -> None:
    """模拟耗时工作的线程函数"""
    print(f"[{threading.current_thread().name}] {name} 开始工作")
    time.sleep(duration)  # 模拟 I/O 等待
    print(f"[{threading.current_thread().name}] {name} 完成工作（{duration}s）")

# 顺序执行（对比用）
start = time.time()
print("\n--- 顺序执行 ---")
worker("任务A", 0.5)
worker("任务B", 0.5)
worker("任务C", 0.5)
print(f"顺序执行总耗时: {time.time()-start:.2f}s")

# 多线程并发执行
start = time.time()
print("\n--- 多线程执行 ---")
threads = [
    threading.Thread(target=worker, args=("任务A", 0.5), name="Thread-A"),
    threading.Thread(target=worker, args=("任务B", 0.5), name="Thread-B"),
    threading.Thread(target=worker, args=("任务C", 0.5), name="Thread-C"),
]
for t in threads:
    t.start()
for t in threads:
    t.join()  # 等待所有线程完成
print(f"多线程执行总耗时: {time.time()-start:.2f}s")

# 2. 竞态条件演示与 Lock 解决
print("\n===Lock 锁保护共享数据===")

counter_unsafe = 0
counter_safe = 0
lock = threading.Lock()

def increment_unsafe(n: int) -> None:
    """不安全的计数（没有锁保护）"""
    global counter_unsafe
    for _ in range(n):
        # 这三步不是原子操作，可能被其他线程打断
        val = counter_unsafe
        time.sleep(0)  # 模拟线程切换
        counter_unsafe = val + 1

def increment_safe(n: int) -> None:
    """安全的计数（有锁保护）"""
    global counter_safe
    for _ in range(n):
        with lock:  # 推荐用 with 语句，自动释放锁
            counter_safe += 1

# 测试不安全版本
counter_unsafe = 0
unsafe_threads = [threading.Thread(target=increment_unsafe, args=(1000,)) for _ in range(5)]
for t in unsafe_threads:
    t.start()
for t in unsafe_threads:
    t.join()
print(f"不安全计数结果: {counter_unsafe}（期望: 5000，实际可能不同）")

# 测试安全版本
counter_safe = 0
safe_threads = [threading.Thread(target=increment_safe, args=(1000,)) for _ in range(5)]
for t in safe_threads:
    t.start()
for t in safe_threads:
    t.join()
print(f"安全计数结果: {counter_safe}（期望: 5000）")
```

#### 案例2：线程池并发下载模拟
```python
# 线程池实战：模拟并发下载
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading
import time
import random

print("===线程池并发任务===")

def download_file(url: str) -> dict:
    """
    模拟文件下载
    
    Args:
        url: 文件URL
        
    Returns:
        包含下载结果的字典
    """
    start_time = time.time()
    # 模拟网络延迟（0.5-2秒随机）
    delay = random.uniform(0.5, 2.0)
    time.sleep(delay)
    
    # 模拟偶尔失败
    if random.random() < 0.1:  # 10%概率失败
        raise ConnectionError(f"下载失败: {url}")
    
    size_kb = random.randint(100, 5000)
    return {
        "url": url,
        "size_kb": size_kb,
        "duration": time.time() - start_time,
        "thread": threading.current_thread().name,
    }

# 待下载的URL列表
urls = [f"https://example.com/file_{i}.zip" for i in range(1, 11)]

print(f"待下载文件数: {len(urls)}")

# 顺序下载（参考时间）
print("\n--- 模拟顺序下载（不实际运行，仅估算）---")
print(f"顺序下载预计耗时: {len(urls) * 1.25:.0f}s（平均每个1.25s）")

# 线程池并发下载
print("\n--- 线程池并发下载（max_workers=4）---")
start = time.time()
results = []
errors = []

with ThreadPoolExecutor(max_workers=4, thread_name_prefix="Downloader") as executor:
    # 提交所有任务，返回 future 字典
    future_to_url = {executor.submit(download_file, url): url for url in urls}
    
    for future in as_completed(future_to_url):
        url = future_to_url[future]
        try:
            result = future.result()
            results.append(result)
            print(f"  ✓ {result['url'].split('/')[-1]:15} "
                  f"{result['size_kb']:>5}KB  "
                  f"{result['duration']:.2f}s  "
                  f"[{result['thread']}]")
        except ConnectionError as e:
            errors.append(str(e))
            print(f"  ✗ {str(e)}")

total_time = time.time() - start
total_size = sum(r["size_kb"] for r in results)

print(f"\n下载完成:")
print(f"  成功: {len(results)}/{len(urls)} 个文件")
print(f"  总大小: {total_size} KB")
print(f"  总耗时: {total_time:.2f}s")
if errors:
    print(f"  失败: {errors}")
```

### 代码说明

**案例1代码解释**：
1. `threading.Thread(target=func, args=(...))`：创建线程，target是线程函数，args是其参数元组
2. `t.join()`：主线程等待子线程结束，缺少 join 可能导致主程序在子线程未完成时退出
3. `with lock:`：推荐用上下文管理器，即使函数抛出异常也能保证锁被释放
4. 竞态条件的本质：`val = counter` → `time.sleep(0)` → `counter = val + 1` 三步之间可能被其他线程插入

**案例2代码解释**：
1. `ThreadPoolExecutor(max_workers=4)` 创建最多4个工作线程的线程池
2. `executor.submit(func, arg)` 提交任务，立即返回 `Future` 对象
3. `as_completed(futures)` 按完成顺序迭代，哪个先完成先处理哪个
4. `future.result()` 获取结果，如果任务抛出异常，这里会重新抛出

---

## 3. 多进程（multiprocessing）

### 知识点解析

**概念定义**：多进程是创建多个独立的 Python 进程，每个进程有自己独立的内存空间和 Python 解释器（以及 GIL），因此可以真正并行执行 CPU 密集型计算。就像公司开了多个独立部门，每个部门都有自己的办公室和设备。

**核心规则**：
1. `multiprocessing.Process(target=func, args=(...))` 创建进程
2. 进程间通信必须通过 `Queue`、`Pipe`、共享内存（`Value`/`Array`）或管理器（`Manager`）
3. `ProcessPoolExecutor` 是进程池的推荐用法（来自 `concurrent.futures`）
4. Windows 下多进程代码必须放在 `if __name__ == '__main__':` 保护块中（避免递归 spawn）
5. 传递给进程的对象必须可 pickle（lambda、局部函数、文件对象等不可 pickle）

**常见易错点**：
1. 进程间不共享全局变量——子进程修改的变量不影响父进程
2. Windows 下忘记 `if __name__ == '__main__':` 导致无限递归创建进程
3. 传入不可 pickle 的对象（lambda、类方法的 self 包含不可序列化的属性）
4. 进程池任务数量远多于核心数时，过多的进程创建开销反而比串行慢

### 实战案例

#### 案例1：多进程 CPU 密集型计算
```python
# 多进程 CPU 密集型计算
import multiprocessing
import time
import os

print("===多进程 CPU 密集型计算===")

def is_prime(n: int) -> bool:
    """判断是否为质数（CPU密集型）"""
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    for i in range(3, int(n**0.5) + 1, 2):
        if n % i == 0:
            return False
    return True

def count_primes_in_range(start: int, end: int) -> int:
    """计算范围内质数数量"""
    return sum(1 for n in range(start, end) if is_prime(n))

def count_primes_worker(args: tuple) -> tuple:
    """进程工作函数（包装为元组参数，方便 starmap）"""
    start, end = args
    count = count_primes_in_range(start, end)
    pid = os.getpid()
    return (start, end, count, pid)

if __name__ == '__main__':
    N = 200_000  # 计算 1 到 200000 之间的质数数量
    
    # 单进程版本
    start_time = time.time()
    single_result = count_primes_in_range(2, N)
    single_time = time.time() - start_time
    print(f"单进程: 1~{N} 内质数数量 = {single_result}，耗时 {single_time:.3f}s")
    
    # 多进程版本（分段计算）
    num_cores = multiprocessing.cpu_count()
    print(f"\nCPU 核心数: {num_cores}")
    
    # 将范围分割成多份
    chunk_size = N // num_cores
    ranges = [(i * chunk_size + 2, (i + 1) * chunk_size + 2) for i in range(num_cores)]
    ranges[-1] = (ranges[-1][0], N)  # 最后一个范围到N
    
    start_time = time.time()
    with multiprocessing.Pool(processes=num_cores) as pool:
        results = pool.map(count_primes_worker, ranges)
    multi_time = time.time() - start_time
    
    multi_result = sum(r[2] for r in results)
    print(f"多进程: 1~{N} 内质数数量 = {multi_result}，耗时 {multi_time:.3f}s")
    print(f"加速比: {single_time / multi_time:.2f}x")
    print("\n各进程工作情况:")
    for start, end, count, pid in results:
        print(f"  PID {pid}: 范围 {start:>7}-{end:>7}，质数数量 {count}")
```

#### 案例2：进程间通信（Queue + Pipe）
```python
# 进程间通信
import multiprocessing
import time
import random

print("===进程间通信：生产者-消费者模式===")

def producer(queue: multiprocessing.Queue, num_items: int) -> None:
    """生产者进程：生产数据放入队列"""
    for i in range(num_items):
        item = {
            "id": i,
            "value": random.randint(1, 100),
            "producer_pid": os.getpid(),
        }
        queue.put(item)
        print(f"[生产者 PID={os.getpid()}] 生产: {item['id']}={item['value']}")
        time.sleep(random.uniform(0.05, 0.15))
    queue.put(None)  # 发送结束信号
    print(f"[生产者] 生产完成")

def consumer(queue: multiprocessing.Queue, result_queue: multiprocessing.Queue) -> None:
    """消费者进程：从队列消费数据"""
    total = 0
    count = 0
    while True:
        item = queue.get()
        if item is None:  # 收到结束信号
            break
        processed_value = item["value"] * 2  # 模拟处理
        total += processed_value
        count += 1
        print(f"[消费者 PID={os.getpid()}] 处理: {item['id']}={item['value']} -> {processed_value}")
        time.sleep(random.uniform(0.01, 0.1))
    
    result_queue.put({"count": count, "total": total})
    print(f"[消费者] 处理完成，共处理 {count} 条")

if __name__ == '__main__':
    import os
    queue = multiprocessing.Queue(maxsize=5)  # 有界队列
    result_queue = multiprocessing.Queue()
    
    p_producer = multiprocessing.Process(target=producer, args=(queue, 8))
    p_consumer = multiprocessing.Process(target=consumer, args=(queue, result_queue))
    
    p_producer.start()
    p_consumer.start()
    
    p_producer.join()
    p_consumer.join()
    
    result = result_queue.get()
    print(f"\n消费者汇总: 处理了 {result['count']} 条，合计值 {result['total']}")
```

### 代码说明

**案例1代码解释**：
1. `multiprocessing.Pool(processes=n)` 创建n个工作进程的进程池
2. `pool.map(func, iterable)` 将任务分发到进程池，阻塞直到所有结果返回
3. 进程池任务函数接收的参数必须可 pickle；lambda 不可 pickle，用模块级普通函数
4. `if __name__ == '__main__':` 在 Windows 下是必须的，防止 spawn 方式创建进程时递归导入

**案例2代码解释**：
1. `multiprocessing.Queue` 是进程安全的队列，底层通过 socket/pipe 实现
2. `queue.put(None)` 是常见的"毒丸"（poison pill）模式，通知消费者没有更多数据
3. 生产者-消费者模式解耦了数据生产和处理，适合数据流水线场景
4. 与 `threading.Queue` 不同，`multiprocessing.Queue` 会序列化（pickle）数据

---

## 4. asyncio 异步编程深入

### 知识点解析

**概念定义**：asyncio 是 Python 的异步 I/O 框架，基于**事件循环**（event loop）和**协程**（coroutine）。协程是可以暂停和恢复的函数，在等待 I/O 时主动让出控制权，让其他协程执行。就像一个服务员同时服务多张桌子——去厨房拿菜（I/O等待）期间，去其他桌子点单，而不是站在那儿傻等。

**核心概念**：
- `async def`：定义协程函数
- `await`：在协程中等待另一个协程或可等待对象
- `asyncio.run(coro())`：运行顶层协程，启动事件循环
- `asyncio.create_task(coro())`：将协程包装为 Task，调度到事件循环并发执行
- `asyncio.gather(*coros)`：并发运行多个协程，等待所有完成

**核心规则**：
1. `await` 只能在 `async def` 函数内使用
2. `asyncio.sleep()` 替代 `time.sleep()`，前者主动让出控制权，后者阻塞整个线程
3. 普通的阻塞 I/O（如 `requests.get`）会阻塞事件循环，应使用异步库（如 `aiohttp`）
4. 使用 `asyncio.gather` 并发运行，而不是逐个 `await`
5. `asyncio.wait_for(coro, timeout=...)` 设置超时

**常见易错点**：
1. 在事件循环中调用 `time.sleep()`（阻塞）而不是 `asyncio.sleep()`（让出控制权）
2. `async for` 和 `async with` 用于异步迭代器和异步上下文管理器，不能用普通 `for`/`with`
3. 创建 Task 后没有 await，协程可能没有执行就被垃圾回收
4. 在非异步环境中直接调用协程函数，返回的是协程对象而非结果

### 实战案例

#### 案例1：asyncio 核心用法
```python
# asyncio 核心用法
import asyncio
import time

print("===asyncio 核心用法===")

# 1. 基础协程：顺序 vs 并发
async def fetch_data(name: str, delay: float) -> str:
    """模拟异步 I/O 操作（如网络请求）"""
    print(f"[{name}] 开始获取数据...")
    await asyncio.sleep(delay)  # 模拟网络等待（主动让出控制权）
    result = f"{name}的数据（耗时{delay}s）"
    print(f"[{name}] 数据获取完成")
    return result

async def run_sequential():
    """顺序执行"""
    start = time.time()
    r1 = await fetch_data("API-1", 1.0)
    r2 = await fetch_data("API-2", 1.5)
    r3 = await fetch_data("API-3", 0.8)
    print(f"顺序执行耗时: {time.time()-start:.2f}s")
    return [r1, r2, r3]

async def run_concurrent():
    """并发执行"""
    start = time.time()
    results = await asyncio.gather(
        fetch_data("API-1", 1.0),
        fetch_data("API-2", 1.5),
        fetch_data("API-3", 0.8),
    )
    print(f"并发执行耗时: {time.time()-start:.2f}s")
    return results

print("--- 顺序执行 ---")
asyncio.run(run_sequential())

print("\n--- 并发执行 ---")
asyncio.run(run_concurrent())

# 2. Task 独立调度
async def task_demo():
    """Task 演示"""
    async def sub_task(name: str, n: int) -> int:
        total = 0
        for i in range(n):
            await asyncio.sleep(0)  # 让出控制权，允许其他任务运行
            total += i
        return total
    
    # create_task 立即调度，不等待
    task1 = asyncio.create_task(sub_task("计算A", 5), name="task-A")
    task2 = asyncio.create_task(sub_task("计算B", 3), name="task-B")
    task3 = asyncio.create_task(sub_task("计算C", 4), name="task-C")
    
    # 等待所有 Task 完成
    results = await asyncio.gather(task1, task2, task3)
    print(f"\nTask 结果: A={results[0]}, B={results[1]}, C={results[2]}")

asyncio.run(task_demo())

# 3. 超时控制
async def timeout_demo():
    """超时控制"""
    print("\n===超时控制===")
    
    async def slow_operation() -> str:
        await asyncio.sleep(5)  # 模拟耗时5秒的操作
        return "完成"
    
    try:
        # 设置2秒超时
        result = await asyncio.wait_for(slow_operation(), timeout=2.0)
        print(f"结果: {result}")
    except asyncio.TimeoutError:
        print("操作超时（2秒内未完成）")

asyncio.run(timeout_demo())
```

#### 案例2：异步上下文管理器与异步生成器
```python
# 异步高级特性
import asyncio
from contextlib import asynccontextmanager

print("===异步上下文管理器===")

class AsyncDatabaseConnection:
    """模拟异步数据库连接"""
    
    def __init__(self, host: str) -> None:
        self.host = host
        self.connected = False
    
    async def __aenter__(self):
        """异步进入：连接数据库"""
        print(f"  正在连接 {self.host}...")
        await asyncio.sleep(0.1)  # 模拟连接耗时
        self.connected = True
        print(f"  已连接 {self.host}")
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """异步退出：关闭连接"""
        await asyncio.sleep(0.05)  # 模拟关闭耗时
        self.connected = False
        print(f"  已断开 {self.host}")
        return False
    
    async def query(self, sql: str) -> list:
        """执行查询"""
        if not self.connected:
            raise RuntimeError("未连接数据库")
        await asyncio.sleep(0.05)
        return [{"id": i, "data": f"{sql}_result_{i}"} for i in range(3)]

# 使用异步上下文管理器
async def database_demo():
    async with AsyncDatabaseConnection("localhost:5432") as conn:
        results = await conn.query("SELECT * FROM users")
        print(f"  查询结果: {len(results)} 条记录")

asyncio.run(database_demo())

# @asynccontextmanager 装饰器方式
@asynccontextmanager
async def managed_resource(name: str):
    """异步上下文管理器装饰器方式"""
    print(f"  获取资源: {name}")
    await asyncio.sleep(0.05)
    try:
        yield f"Resource({name})"  # 这个值被 as 子句接收
    finally:
        print(f"  释放资源: {name}")
        await asyncio.sleep(0.02)

async def resource_demo():
    async with managed_resource("文件锁") as res:
        print(f"  使用: {res}")

asyncio.run(resource_demo())

# 异步生成器
print("\n===异步生成器===")

async def async_range(n: int, delay: float = 0.1):
    """异步生成器：带延迟地生成数字"""
    for i in range(n):
        await asyncio.sleep(delay)
        yield i

async def async_generator_demo():
    print("异步生成数字（带0.1s延迟）:")
    result = []
    async for num in async_range(5, 0.1):
        result.append(num)
        print(f"  收到: {num}")
    print(f"所有数字: {result}")

asyncio.run(async_generator_demo())

# 并发任务的错误处理
print("\n===并发任务的错误处理===")

async def risky_task(name: str, should_fail: bool) -> str:
    await asyncio.sleep(0.1)
    if should_fail:
        raise ValueError(f"任务 {name} 失败了")
    return f"任务 {name} 成功"

async def handle_concurrent_errors():
    """gather 的错误处理"""
    # return_exceptions=True：让失败的 Task 返回异常而不是引发
    results = await asyncio.gather(
        risky_task("A", False),
        risky_task("B", True),   # 这个会失败
        risky_task("C", False),
        risky_task("D", True),   # 这个也会失败
        return_exceptions=True,  # 关键参数
    )
    for i, result in enumerate(results):
        if isinstance(result, Exception):
            print(f"  任务{['A','B','C','D'][i]} 失败: {result}")
        else:
            print(f"  任务{['A','B','C','D'][i]}: {result}")

asyncio.run(handle_concurrent_errors())
```

### 代码说明

**案例1代码解释**：
1. `await asyncio.sleep(delay)` 让当前协程暂停，事件循环可以运行其他协程
2. `asyncio.gather(c1, c2, c3)` 同时调度三个协程，总耗时约等于最慢的那个
3. `asyncio.create_task(coro)` 立即调度到事件循环（不等待），需要 await 或 gather 等待结果
4. `asyncio.wait_for(coro, timeout=n)` 超时后取消协程并抛出 `asyncio.TimeoutError`

**案例2代码解释**：
1. `__aenter__`/`__aexit__` 是异步版本的上下文管理器协议，必须是 `async def`
2. `@asynccontextmanager` 简化异步上下文管理器的写法，`yield` 前是进入代码，`yield` 后是退出代码
3. `async for` 用于异步迭代器（实现了 `__aiter__`/`__anext__` 的对象，或 `async def` 生成器）
4. `gather(return_exceptions=True)` 是并发任务容错的推荐方式，避免一个任务失败取消所有其他任务

---

## 5. 并发模型选择指南

### 综合对比

```
任务类型判断流程：

是否是 CPU 密集型？（大量计算，如图像处理、机器学习推理）
  └─ 是 → 使用 multiprocessing（绕过GIL）
  └─ 否（I/O密集型）
       ├─ 并发连接数是否很大（100+）？
       │    └─ 是 → asyncio（最高效，适合服务器）
       │    └─ 否（10-50个任务）→ ThreadPoolExecutor（简单，兼容性好）
       └─ 是否需要与阻塞的第三方库兼容？
            └─ 是 → ThreadPoolExecutor（可用 run_in_executor 桥接）
            └─ 否 → asyncio（首选）
```

### 关键选择原则

| 场景 | 推荐方案 | 原因 |
|------|---------|------|
| Web 爬虫（大量URL） | asyncio + aiohttp | 高并发 I/O，单线程无锁 |
| 数据处理管道 | multiprocessing.Pool | 纯计算，充分利用多核 |
| 文件批量处理 | ThreadPoolExecutor | I/O 等待，线程简单 |
| 实时聊天服务器 | asyncio | 大量长连接，事件驱动 |
| 调用阻塞第三方库 | loop.run_in_executor | 将阻塞操作放入线程池 |

### 混合使用：在 asyncio 中运行阻塞代码

```python
import asyncio
import time

async def main_with_blocking():
    """在 asyncio 中运行阻塞函数（run_in_executor）"""
    loop = asyncio.get_event_loop()
    
    def blocking_io():
        """模拟阻塞的 I/O 操作（如旧版同步库）"""
        time.sleep(1)
        return "阻塞操作完成"
    
    # 在默认的线程池执行器中运行阻塞函数
    result = await loop.run_in_executor(None, blocking_io)
    print(f"run_in_executor 结果: {result}")

asyncio.run(main_with_blocking())
```

---

## 6. 知识点小结

**三种并发模型对比**：
- `threading`：适合 I/O 密集，共享内存，需要锁
- `multiprocessing`：绕过 GIL，适合 CPU 密集，进程间通信有开销
- `asyncio`：最高效的 I/O 并发，单线程无锁，但需要全异步生态

**GIL 核心理解**：
- GIL 只是 CPython 的实现细节，Jython/PyPy 没有 GIL
- 纯 Python 计算受 GIL 限制，多线程无法加速
- C 扩展（numpy、pandas 核心计算）通常会释放 GIL，可以多线程
- 使用 `multiprocessing` 是绕过 GIL 的标准方式

**最佳实践**：
1. 优先使用 `concurrent.futures`（`ThreadPoolExecutor`/`ProcessPoolExecutor`），比手动管理线程/进程更安全
2. asyncio 任务出错不要沉默——用 `return_exceptions=True` 或显式处理
3. 多进程代码用 `if __name__ == '__main__':` 保护，Windows 必须
4. 不要在 asyncio 中调用同步阻塞代码，用 `run_in_executor` 桥接
