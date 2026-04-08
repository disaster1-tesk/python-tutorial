"""
Python 并发编程完整示例
演示内容：
1. GIL 与并发模型对比（多线程 vs 多进程 vs asyncio）
2. threading：基础线程、Lock锁、线程池
3. multiprocessing：进程池、Queue进程间通信
4. asyncio：协程基础、并发 gather、超时控制、异步生成器
5. 混合使用：run_in_executor
"""

import threading
import multiprocessing
import asyncio
import time
import random
import os
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, as_completed
from contextlib import asynccontextmanager

print("=" * 60)
print("Python 并发编程完整示例")
print("=" * 60)

# ============================================================
# 1. 多线程基础
# ============================================================
print("\n【1. 多线程基础】")


def worker(name: str, duration: float) -> str:
    """线程工作函数：模拟I/O等待"""
    print(f"  [{threading.current_thread().name}] {name} 开始")
    time.sleep(duration)
    print(f"  [{threading.current_thread().name}] {name} 完成 ({duration:.1f}s)")
    return f"{name}结果"


# 顺序执行 vs 多线程并发
print("--- 顺序执行 ---")
start = time.time()
worker("任务A", 0.3)
worker("任务B", 0.3)
worker("任务C", 0.3)
print(f"顺序耗时: {time.time()-start:.2f}s\n")

print("--- 多线程并发 ---")
start = time.time()
threads = [
    threading.Thread(target=worker, args=(f"任务{n}", 0.3), name=f"T-{n}")
    for n in ["A", "B", "C"]
]
for t in threads:
    t.start()
for t in threads:
    t.join()
print(f"多线程耗时: {time.time()-start:.2f}s")

# ============================================================
# 2. Lock 锁：保护共享数据
# ============================================================
print("\n【2. Lock 锁保护共享数据】")

# 演示竞态条件
counter = 0
lock = threading.Lock()


def increment_no_lock(n: int) -> None:
    """无锁版本（有竞态条件）"""
    global counter
    for _ in range(n):
        val = counter
        time.sleep(0)  # 模拟线程切换时机
        counter = val + 1


def increment_with_lock(n: int) -> None:
    """有锁版本（线程安全）"""
    global counter
    for _ in range(n):
        with lock:
            counter += 1


# 测试有锁版本
counter = 0
safe_threads = [threading.Thread(target=increment_with_lock, args=(500,)) for _ in range(5)]
for t in safe_threads:
    t.start()
for t in safe_threads:
    t.join()
print(f"有锁计数器结果: {counter}（期望: 2500）")


# RLock 演示（可重入锁）
class BankAccount:
    """线程安全的银行账户"""

    def __init__(self, owner: str, balance: float) -> None:
        self.owner = owner
        self.balance = balance
        self._lock = threading.RLock()  # 可重入锁，同一线程可多次获取

    def deposit(self, amount: float) -> None:
        with self._lock:
            self.balance += amount

    def withdraw(self, amount: float) -> bool:
        with self._lock:
            if self.balance >= amount:
                self.balance -= amount
                return True
            return False

    def transfer_to(self, other: "BankAccount", amount: float) -> bool:
        """转账（持锁的情况下调用其他需锁的方法）"""
        with self._lock:  # RLock允许同一线程再次获取（普通Lock会死锁）
            if self.withdraw(amount):
                other.deposit(amount)
                return True
            return False


account_a = BankAccount("张三", 1000.0)
account_b = BankAccount("李四", 500.0)


def do_transfers():
    for _ in range(10):
        account_a.transfer_to(account_b, 50.0)


def do_reverse_transfers():
    for _ in range(10):
        account_b.transfer_to(account_a, 30.0)


t1 = threading.Thread(target=do_transfers)
t2 = threading.Thread(target=do_reverse_transfers)
t1.start()
t2.start()
t1.join()
t2.join()
print(f"转账后余额: {account_a.owner}={account_a.balance:.0f}, {account_b.owner}={account_b.balance:.0f}")

# ============================================================
# 3. 线程池 ThreadPoolExecutor
# ============================================================
print("\n【3. 线程池 ThreadPoolExecutor】")


def simulate_request(url: str) -> dict:
    """模拟HTTP请求"""
    delay = random.uniform(0.2, 0.8)
    time.sleep(delay)
    return {
        "url": url,
        "status": 200 if random.random() > 0.1 else 500,
        "duration": delay,
    }


urls = [f"https://api.example.com/data/{i}" for i in range(1, 9)]

start = time.time()
success = []
failures = []

with ThreadPoolExecutor(max_workers=4, thread_name_prefix="HTTP") as executor:
    future_to_url = {executor.submit(simulate_request, url): url for url in urls}
    for future in as_completed(future_to_url):
        url = future_to_url[future]
        try:
            result = future.result()
            status = result["status"]
            if status == 200:
                success.append(url)
                print(f"  ✓ {url.split('/')[-1]:8} -> {status} ({result['duration']:.2f}s)")
            else:
                failures.append(url)
                print(f"  ✗ {url.split('/')[-1]:8} -> {status}")
        except Exception as e:
            failures.append(url)
            print(f"  ✗ 异常: {e}")

print(f"完成: {len(success)}成功, {len(failures)}失败, 耗时 {time.time()-start:.2f}s")

# ============================================================
# 4. 多进程 ProcessPoolExecutor（CPU密集型）
# ============================================================
print("\n【4. 多进程 CPU密集型计算】")


def is_prime(n: int) -> bool:
    """判断质数（纯CPU计算）"""
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


def count_primes(start: int, end: int) -> tuple[int, int]:
    """计算范围内的质数数量，返回 (count, pid)"""
    count = sum(1 for n in range(start, end) if is_prime(n))
    return count, os.getpid()


if __name__ == "__main__":
    N = 100_000
    num_cores = min(multiprocessing.cpu_count(), 4)

    # 单进程基准
    start = time.time()
    single_count = sum(1 for n in range(2, N) if is_prime(n))
    single_time = time.time() - start
    print(f"单进程: 1~{N}内质数={single_count}, 耗时={single_time:.3f}s")

    # 多进程
    chunk = N // num_cores
    ranges = [(i * chunk + 2, (i + 1) * chunk + 2) for i in range(num_cores)]
    ranges[-1] = (ranges[-1][0], N)

    start = time.time()
    with ProcessPoolExecutor(max_workers=num_cores) as executor:
        futures = [executor.submit(count_primes, s, e) for s, e in ranges]
        results = [f.result() for f in futures]
    multi_time = time.time() - start

    multi_count = sum(r[0] for r in results)
    print(f"多进程({num_cores}核): 1~{N}内质数={multi_count}, 耗时={multi_time:.3f}s")
    print(f"加速比: {single_time/multi_time:.2f}x")

    # ============================================================
    # 5. asyncio 异步编程
    # ============================================================
    print("\n【5. asyncio 异步编程】")

    async def async_fetch(name: str, delay: float) -> str:
        """模拟异步HTTP请求"""
        print(f"  [{name}] 发起请求...")
        await asyncio.sleep(delay)  # 主动让出控制权
        print(f"  [{name}] 响应完成 ({delay:.1f}s)")
        return f"{name}: {random.randint(1, 100)}"

    async def sequential_demo() -> None:
        """顺序执行（慢）"""
        print("--- asyncio 顺序执行 ---")
        start = time.time()
        r1 = await async_fetch("API-1", 0.5)
        r2 = await async_fetch("API-2", 0.8)
        r3 = await async_fetch("API-3", 0.3)
        print(f"结果: {[r1, r2, r3]}, 耗时: {time.time()-start:.2f}s")

    async def concurrent_demo() -> None:
        """并发执行（快）"""
        print("\n--- asyncio 并发执行 ---")
        start = time.time()
        results = await asyncio.gather(
            async_fetch("API-1", 0.5),
            async_fetch("API-2", 0.8),
            async_fetch("API-3", 0.3),
        )
        print(f"结果: {results}, 耗时: {time.time()-start:.2f}s")

    asyncio.run(sequential_demo())
    asyncio.run(concurrent_demo())

    # asyncio Task 和超时
    async def task_and_timeout_demo() -> None:
        print("\n--- Task 和超时控制 ---")

        async def quick_task(n: int) -> int:
            await asyncio.sleep(0.1 * n)
            return n * n

        # 创建多个 Task
        tasks = [asyncio.create_task(quick_task(i), name=f"task-{i}") for i in range(1, 6)]
        results = await asyncio.gather(*tasks)
        print(f"Task 结果: {results}")

        # 超时控制
        async def slow_task() -> str:
            await asyncio.sleep(10)
            return "永远不会到达"

        try:
            result = await asyncio.wait_for(slow_task(), timeout=0.5)
        except asyncio.TimeoutError:
            print("超时控制: 0.5s 超时取消")

        # gather 容错（return_exceptions=True）
        async def maybe_fail(name: str, fail: bool) -> str:
            await asyncio.sleep(0.05)
            if fail:
                raise ValueError(f"{name} 失败")
            return f"{name} 成功"

        results_with_errors = await asyncio.gather(
            maybe_fail("A", False),
            maybe_fail("B", True),
            maybe_fail("C", False),
            return_exceptions=True,
        )
        for name, res in zip(["A", "B", "C"], results_with_errors):
            if isinstance(res, Exception):
                print(f"  任务{name}: ✗ {res}")
            else:
                print(f"  任务{name}: ✓ {res}")

    asyncio.run(task_and_timeout_demo())

    # ============================================================
    # 6. 混合：asyncio + 阻塞函数
    # ============================================================
    print("\n【6. asyncio 中运行阻塞函数 (run_in_executor)】")

    def blocking_operation(name: str, delay: float) -> str:
        """旧式阻塞函数（无法直接用 await）"""
        time.sleep(delay)  # 阻塞调用
        return f"{name} 完成"

    async def mixed_demo() -> None:
        loop = asyncio.get_event_loop()

        # 将阻塞函数放入线程池执行，不阻塞事件循环
        results = await asyncio.gather(
            loop.run_in_executor(None, blocking_operation, "阻塞任务A", 0.5),
            loop.run_in_executor(None, blocking_operation, "阻塞任务B", 0.3),
            async_fetch("异步任务C", 0.4),
        )
        for r in results:
            print(f"  {r}")

    asyncio.run(mixed_demo())

    # ============================================================
    # 7. 异步生成器
    # ============================================================
    print("\n【7. 异步生成器与异步上下文管理器】")

    async def async_data_stream(items: list, delay: float = 0.1):
        """异步数据流生成器"""
        for item in items:
            await asyncio.sleep(delay)
            yield item

    @asynccontextmanager
    async def timer_context(name: str):
        """异步计时上下文管理器"""
        start = time.time()
        print(f"  [{name}] 开始")
        try:
            yield
        finally:
            elapsed = time.time() - start
            print(f"  [{name}] 结束，耗时 {elapsed:.3f}s")

    async def advanced_async_demo() -> None:
        # 异步 for 循环
        print("异步数据流:")
        data = [1, 4, 9, 16, 25]
        async for item in async_data_stream(data, 0.05):
            print(f"  收到: {item}", end="")
        print()

        # 异步上下文管理器
        async with timer_context("数据处理"):
            await asyncio.sleep(0.2)  # 模拟处理

    asyncio.run(advanced_async_demo())

    # ============================================================
    # 8. 总结
    # ============================================================
    print("\n【8. 并发模型选择总结】")
    guide = [
        "I/O密集型（网络/磁盘）        → threading 或 asyncio",
        "CPU密集型（大量计算）          → multiprocessing",
        "高并发连接（1000+）            → asyncio",
        "需要使用阻塞库                → ThreadPoolExecutor",
        "计算密集 + 简单并行            → ProcessPoolExecutor",
        "混合场景（async + 阻塞库）     → run_in_executor",
    ]
    for g in guide:
        print(f"  {g}")
