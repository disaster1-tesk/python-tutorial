"""
Python 数据库操作完整示例
演示内容：
1. sqlite3：连接、CRUD、参数化查询、事务、聚合查询
2. SQLAlchemy ORM：模型定义、Session、关系映射、查询
3. 数据库最佳实践：连接池、防SQL注入、上下文管理器
"""

import sqlite3
import os
from contextlib import contextmanager
from datetime import datetime, date
from typing import Optional, Generator

print("=" * 60)
print("Python 数据库操作完整示例")
print("=" * 60)

# ============================================================
# 1. sqlite3 基础：CRUD 操作
# ============================================================
print("\n【1. sqlite3 基础 CRUD】")


@contextmanager
def get_db_connection(db_path: str = ":memory:") -> Generator[sqlite3.Connection, None, None]:
    """数据库连接上下文管理器：保证连接正确关闭"""
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row  # 支持列名访问
    conn.execute("PRAGMA foreign_keys = ON")
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def setup_tables(conn: sqlite3.Connection) -> None:
    """创建表结构"""
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS departments (
            id   INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE
        );

        CREATE TABLE IF NOT EXISTS employees (
            id            INTEGER PRIMARY KEY AUTOINCREMENT,
            name          TEXT NOT NULL,
            age           INTEGER NOT NULL CHECK(age > 0),
            salary        REAL NOT NULL CHECK(salary >= 0),
            email         TEXT UNIQUE,
            department_id INTEGER REFERENCES departments(id),
            hire_date     DATE DEFAULT (date('now'))
        );

        CREATE INDEX IF NOT EXISTS idx_emp_dept ON employees(department_id);
    """)


with get_db_connection() as conn:
    setup_tables(conn)

    # INSERT：参数化查询（防SQL注入）
    conn.execute("INSERT INTO departments (name) VALUES (?)", ("研发部",))
    conn.execute("INSERT INTO departments (name) VALUES (?)", ("产品部",))
    conn.execute("INSERT INTO departments (name) VALUES (?)", ("运营部",))

    # executemany 批量插入（比循环快）
    employees_data = [
        ("张三", 28, 15000.0, "zhang@example.com", 1),
        ("李四", 32, 18000.0, "li@example.com", 1),
        ("王五", 25, 12000.0, "wang@example.com", 2),
        ("赵六", 35, 22000.0, "zhao@example.com", 2),
        ("钱七", 27, 9500.0, "qian@example.com", 3),
        ("孙八", 30, 16000.0, "sun@example.com", 1),
    ]
    conn.executemany(
        "INSERT INTO employees (name, age, salary, email, department_id) VALUES (?, ?, ?, ?, ?)",
        employees_data,
    )
    print(f"插入了 {conn.total_changes} 条记录")

    # SELECT：基础查询
    print("\n所有员工:")
    rows = conn.execute("""
        SELECT e.name, e.age, e.salary, d.name as dept
        FROM employees e
        LEFT JOIN departments d ON e.department_id = d.id
        ORDER BY e.salary DESC
    """).fetchall()
    for row in rows:
        print(f"  {row['name']:4} {row['age']}岁  ¥{row['salary']:>8,.0f}  [{row['dept']}]")

    # SELECT：条件查询（参数化）
    dept_filter = "研发部"
    dev_employees = conn.execute("""
        SELECT e.name, e.salary FROM employees e
        JOIN departments d ON e.department_id = d.id
        WHERE d.name = ?
    """, (dept_filter,)).fetchall()
    print(f"\n{dept_filter}员工: {[r['name'] for r in dev_employees]}")

    # UPDATE
    updated = conn.execute(
        "UPDATE employees SET salary = salary * 1.1 WHERE department_id = 1"
    ).rowcount
    print(f"\n研发部涨薪10%，影响 {updated} 条记录")

    # 验证更新
    for row in conn.execute("SELECT name, salary FROM employees WHERE department_id = 1"):
        print(f"  {row['name']}: ¥{row['salary']:,.0f}")

    # DELETE
    deleted = conn.execute(
        "DELETE FROM employees WHERE name = ?", ("钱七",)
    ).rowcount
    print(f"\n删除钱七，影响 {deleted} 条")

    # 聚合查询：GROUP BY + HAVING
    print("\n各部门薪资统计（平均薪资>12000）:")
    for row in conn.execute("""
        SELECT d.name, COUNT(e.id) as headcount,
               ROUND(AVG(e.salary), 2) as avg_salary,
               MAX(e.salary) as max_salary
        FROM departments d
        LEFT JOIN employees e ON d.id = e.department_id
        GROUP BY d.id
        HAVING avg_salary > 12000
        ORDER BY avg_salary DESC
    """):
        print(f"  {row['name']:4}: {row['headcount']}人, "
              f"均薪¥{row['avg_salary']:,.0f}, 最高¥{row['max_salary']:,.0f}")

# ============================================================
# 2. 事务处理
# ============================================================
print("\n【2. 事务处理（原子性保证）】")


def transfer_funds(db_path: str, from_id: int, to_id: int, amount: float) -> bool:
    """
    转账操作（事务保证原子性）
    - 成功：扣款和加款同时提交
    - 失败：两个操作同时回滚
    """
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row

    try:
        with conn:  # with 语句：成功 commit，异常 rollback
            # 检查余额
            sender = conn.execute(
                "SELECT balance FROM accounts WHERE id = ?", (from_id,)
            ).fetchone()
            if not sender or sender["balance"] < amount:
                raise ValueError(f"余额不足（现有 {sender['balance'] if sender else 0}）")

            conn.execute(
                "UPDATE accounts SET balance = balance - ? WHERE id = ?",
                (amount, from_id),
            )
            conn.execute(
                "UPDATE accounts SET balance = balance + ? WHERE id = ?",
                (amount, to_id),
            )
            return True
    except ValueError as e:
        print(f"  转账失败: {e}")
        return False
    finally:
        conn.close()


# 创建并演示转账
with get_db_connection() as conn:
    conn.execute("CREATE TABLE accounts (id INTEGER PRIMARY KEY, owner TEXT, balance REAL)")
    conn.execute("INSERT INTO accounts VALUES (1, '张三', 1000.0)")
    conn.execute("INSERT INTO accounts VALUES (2, '李四', 500.0)")

    def show_balances(conn: sqlite3.Connection) -> None:
        for row in conn.execute("SELECT owner, balance FROM accounts"):
            print(f"  {row['owner']}: ¥{row['balance']:.2f}")

    print("初始余额:")
    show_balances(conn)

# 对独立连接演示事务（使用文件数据库）
import tempfile
with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as f:
    db_file = f.name

# 重建账户表
conn = sqlite3.connect(db_file)
conn.execute("CREATE TABLE accounts (id INTEGER PRIMARY KEY, owner TEXT, balance REAL)")
conn.execute("INSERT INTO accounts VALUES (1, '张三', 1000.0)")
conn.execute("INSERT INTO accounts VALUES (2, '李四', 500.0)")
conn.commit()
conn.close()

# 成功转账
print("\n张三 -> 李四 转账 300 元:")
transfer_funds(db_file, 1, 2, 300.0)

conn = sqlite3.connect(db_file)
conn.row_factory = sqlite3.Row
for row in conn.execute("SELECT owner, balance FROM accounts"):
    print(f"  {row['owner']}: ¥{row['balance']:.2f}")
conn.close()

# 失败转账（余额不足）
print("\n张三 -> 李四 转账 5000 元（余额不足）:")
transfer_funds(db_file, 1, 2, 5000.0)

conn = sqlite3.connect(db_file)
conn.row_factory = sqlite3.Row
print("转账失败后余额（不变）:")
for row in conn.execute("SELECT owner, balance FROM accounts"):
    print(f"  {row['owner']}: ¥{row['balance']:.2f}")
conn.close()
os.unlink(db_file)  # 清理临时文件

# ============================================================
# 3. SQLAlchemy ORM
# ============================================================
print("\n【3. SQLAlchemy ORM】")

try:
    from sqlalchemy import (
        create_engine, Column, Integer, String, Float,
        DateTime, ForeignKey, func, select
    )
    from sqlalchemy.orm import DeclarativeBase, Session, relationship

    class Base(DeclarativeBase):
        pass

    class Category(Base):
        __tablename__ = "categories"
        id       = Column(Integer, primary_key=True)
        name     = Column(String(50), unique=True, nullable=False)
        products = relationship("Product", back_populates="category")

        def __repr__(self) -> str:
            return f"Category({self.name!r})"

    class Product(Base):
        __tablename__ = "products"
        id          = Column(Integer, primary_key=True)
        name        = Column(String(100), nullable=False)
        price       = Column(Float, nullable=False)
        stock       = Column(Integer, default=0)
        category_id = Column(Integer, ForeignKey("categories.id"))
        category    = relationship("Category", back_populates="products")

        def __repr__(self) -> str:
            return f"Product({self.name!r}, ¥{self.price})"

    # 创建引擎（echo=False 不打印SQL）
    engine = create_engine("sqlite:///:memory:", echo=False)
    Base.metadata.create_all(engine)

    # 插入数据
    with Session(engine) as session:
        categories = [
            Category(name="图书"),
            Category(name="电子产品"),
            Category(name="文具"),
        ]
        session.add_all(categories)
        session.flush()  # 获取自增 ID

        products = [
            Product(name="Python编程书", price=89.9, stock=100, category=categories[0]),
            Product(name="数据结构书", price=79.5, stock=50, category=categories[0]),
            Product(name="机械键盘", price=399.0, stock=30, category=categories[1]),
            Product(name="无线鼠标", price=129.0, stock=80, category=categories[1]),
            Product(name="笔记本", price=15.5, stock=500, category=categories[2]),
        ]
        session.add_all(products)
        session.commit()
    print("ORM 数据插入完成")

    # 查询操作
    with Session(engine) as session:
        # 基础查询
        all_products = session.query(Product).order_by(Product.price.desc()).all()
        print("\n商品列表（按价格降序）:")
        for p in all_products:
            cat = p.category.name if p.category else "无分类"
            print(f"  {p.name:15} ¥{p.price:>7.2f}  库存:{p.stock:>4}  [{cat}]")

        # 条件过滤
        expensive = session.query(Product).filter(Product.price > 100).all()
        print(f"\n价格>100的商品: {[p.name for p in expensive]}")

        # 关联查询
        books = (
            session.query(Product)
            .join(Category)
            .filter(Category.name == "图书")
            .all()
        )
        print(f"图书类商品: {[p.name for p in books]}")

        # 聚合查询
        print("\n各分类统计:")
        stats = (
            session.query(
                Category.name,
                func.count(Product.id).label("count"),
                func.avg(Product.price).label("avg_price"),
                func.sum(Product.stock).label("total_stock"),
            )
            .join(Product)
            .group_by(Category.id)
            .all()
        )
        for cat_name, count, avg_price, total_stock in stats:
            print(f"  {cat_name:6}: {count}款商品, 均价¥{avg_price:.2f}, 总库存{total_stock}")

    # 更新和删除
    with Session(engine) as session:
        # 单个更新
        product = session.query(Product).filter_by(name="Python编程书").first()
        if product:
            product.price = 79.9  # 直接修改属性
            session.commit()
            print(f"\nPython编程书更新后价格: ¥{product.price}")

        # 批量更新（图书全部打9折）
        updated = (
            session.query(Product)
            .filter(Product.category.has(Category.name == "图书"))
            .update({"price": Product.price * 0.9}, synchronize_session="fetch")
        )
        session.commit()
        print(f"图书打9折，更新了 {updated} 条记录")

        # 验证
        for p in session.query(Product).join(Category).filter(Category.name == "图书"):
            print(f"  {p.name}: ¥{p.price:.2f}")

except ImportError:
    print("提示: 请安装 SQLAlchemy: pip install sqlalchemy")
    print("（未安装时跳过ORM演示）")

# ============================================================
# 4. 防SQL注入演示
# ============================================================
print("\n【4. 防SQL注入演示（重要！）】")

with get_db_connection() as conn:
    conn.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT, password TEXT)")
    conn.execute("INSERT INTO users VALUES (1, 'admin', 'secret123')")
    conn.execute("INSERT INTO users VALUES (2, '张三', 'mypassword')")

    # ✅ 正确方式：参数化查询
    def safe_login(conn: sqlite3.Connection, username: str, password: str) -> bool:
        result = conn.execute(
            "SELECT id FROM users WHERE name = ? AND password = ?",
            (username, password),  # ? 占位符，安全！
        ).fetchone()
        return result is not None

    # ❌ 危险方式（仅作反面教材，实际代码千万不要这样写）
    def unsafe_login(conn: sqlite3.Connection, username: str, password: str) -> bool:
        # 拼接SQL字符串 -> SQL注入漏洞！
        sql = f"SELECT id FROM users WHERE name = '{username}' AND password = '{password}'"
        result = conn.execute(sql).fetchone()
        return result is not None

    # 正常登录
    print(f"正常登录 admin: {safe_login(conn, 'admin', 'secret123')}")

    # SQL注入攻击字符串
    attack = "' OR '1'='1"
    print(f"\n[安全] 注入攻击字符串: {safe_login(conn, attack, attack)}")
    print(f"[危险] 注入攻击字符串: {unsafe_login(conn, attack, attack)}  ← 被SQL注入！")
    print("结论: 永远使用 ? 占位符，绝对不要拼接 SQL 字符串！")

# ============================================================
# 5. 最佳实践总结
# ============================================================
print("\n【5. 数据库操作最佳实践】")
tips = [
    "✓ 永远使用 ? 占位符，杜绝SQL注入",
    "✓ 使用上下文管理器确保连接正确关闭",
    "✓ 批量操作用 executemany，比循环快得多",
    "✓ 事务保证原子性：with conn: 自动 commit/rollback",
    "✓ conn.row_factory = sqlite3.Row 支持列名访问",
    "✓ SQLAlchemy 生产环境配置连接池参数",
    "✓ ORM关系查询注意懒加载，Session关闭后不能访问关联属性",
    "✓ 复杂查询不要怕写原生SQL，ORM.execute() 支持",
]
for tip in tips:
    print(f"  {tip}")
