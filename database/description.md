# Python 数据库操作

## 1. sqlite3 内置模块

### 知识点解析

**概念定义**：SQLite 是 Python 内置支持的轻量级关系型数据库，无需安装额外服务，数据存在单个文件中。`sqlite3` 模块是 Python 标准库的一部分，非常适合本地应用、原型开发和学习数据库操作。

**核心规则**：
1. 连接数据库：`conn = sqlite3.connect("db.sqlite3")`，`:memory:` 表示内存数据库
2. 游标执行 SQL：`cursor = conn.cursor(); cursor.execute(sql)`
3. 参数化查询防 SQL 注入：`cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))`，**永远不要用字符串拼接构造 SQL**
4. 增删改后必须 `conn.commit()` 才真正写入，或用 `with conn:` 自动提交/回滚
5. 用完记得 `conn.close()`，或用 `with sqlite3.connect() as conn:`（注意：`with` 只管事务不管关闭）

**常见易错点**：
1. 用 f-string 或 `%` 格式化拼接 SQL 参数——会导致 SQL 注入漏洞，必须用 `?` 占位符
2. 忘记 `commit()` 导致修改丢失（重启后数据消失）
3. 在 `fetchone()` 返回 `None` 时直接访问字段会报 `TypeError`
4. 多线程共享同一 `Connection` 对象可能报错，每个线程应有自己的连接
5. `executemany` 比循环调用 `execute` 批量插入效率高得多

### 实战案例

#### 案例1：学生管理系统（CRUD）
```python
# sqlite3 CRUD 操作
import sqlite3
from contextlib import contextmanager

print("===SQLite3 学生管理系统===")

# 数据库上下文管理器（确保连接和事务安全）
@contextmanager
def get_db(db_path: str = ":memory:"):
    """数据库连接上下文管理器"""
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row  # 让查询结果支持列名访问：row["name"]
    conn.execute("PRAGMA foreign_keys = ON")  # 启用外键约束
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()

def init_database(conn: sqlite3.Connection) -> None:
    """初始化数据库表"""
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS classes (
            id      INTEGER PRIMARY KEY AUTOINCREMENT,
            name    TEXT NOT NULL UNIQUE,
            teacher TEXT NOT NULL
        );
        
        CREATE TABLE IF NOT EXISTS students (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            name       TEXT NOT NULL,
            age        INTEGER NOT NULL CHECK(age > 0 AND age < 150),
            email      TEXT UNIQUE,
            class_id   INTEGER REFERENCES classes(id),
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        );
        
        CREATE INDEX IF NOT EXISTS idx_students_class ON students(class_id);
    """)
    print("数据库初始化完成")

def insert_sample_data(conn: sqlite3.Connection) -> None:
    """批量插入样本数据（演示 executemany）"""
    classes = [("Python班", "李老师"), ("Java班", "王老师"), ("AI班", "张老师")]
    conn.executemany(
        "INSERT OR IGNORE INTO classes (name, teacher) VALUES (?, ?)",
        classes
    )
    
    students = [
        ("张三", 20, "zhang@example.com", 1),
        ("李四", 22, "li@example.com", 1),
        ("王五", 21, "wang@example.com", 2),
        ("赵六", 23, "zhao@example.com", 3),
        ("钱七", 20, "qian@example.com", 1),
    ]
    conn.executemany(
        "INSERT OR IGNORE INTO students (name, age, email, class_id) VALUES (?, ?, ?, ?)",
        students
    )
    print(f"插入了 {conn.total_changes} 条记录")

def get_student(conn: sqlite3.Connection, student_id: int) -> sqlite3.Row | None:
    """查询单个学生（参数化查询，防SQL注入）"""
    return conn.execute(
        """
        SELECT s.id, s.name, s.age, s.email, c.name as class_name
        FROM students s
        LEFT JOIN classes c ON s.class_id = c.id
        WHERE s.id = ?
        """,
        (student_id,)
    ).fetchone()

def search_students(conn: sqlite3.Connection, keyword: str) -> list:
    """模糊搜索学生"""
    return conn.execute(
        "SELECT * FROM students WHERE name LIKE ? OR email LIKE ?",
        (f"%{keyword}%", f"%{keyword}%")
    ).fetchall()

def update_student_age(conn: sqlite3.Connection, student_id: int, new_age: int) -> int:
    """更新学生年龄，返回受影响行数"""
    cursor = conn.execute(
        "UPDATE students SET age = ? WHERE id = ?",
        (new_age, student_id)
    )
    return cursor.rowcount

def delete_student(conn: sqlite3.Connection, student_id: int) -> int:
    """删除学生，返回受影响行数"""
    cursor = conn.execute("DELETE FROM students WHERE id = ?", (student_id,))
    return cursor.rowcount

# 演示所有操作
with get_db(":memory:") as conn:
    init_database(conn)
    insert_sample_data(conn)
    
    # 查询全部
    print("\n所有学生:")
    for row in conn.execute("SELECT s.id, s.name, s.age, c.name as class FROM students s LEFT JOIN classes c ON s.class_id=c.id"):
        print(f"  [{row['id']}] {row['name']}, {row['age']}岁, {row['class']}")
    
    # 查询单个（row_factory 支持列名访问）
    student = get_student(conn, 1)
    if student:
        print(f"\n查询学生ID=1: {student['name']}，班级: {student['class_name']}")
    
    # 搜索
    results = search_students(conn, "三")
    print(f"\n搜索'三'的结果: {[r['name'] for r in results]}")
    
    # 更新
    affected = update_student_age(conn, 1, 25)
    print(f"\n更新ID=1的年龄，影响行数: {affected}")
    
    # 验证更新
    student = get_student(conn, 1)
    print(f"更新后年龄: {student['age']}")
    
    # 删除
    affected = delete_student(conn, 5)
    print(f"\n删除ID=5，影响行数: {affected}")
    
    total = conn.execute("SELECT COUNT(*) FROM students").fetchone()[0]
    print(f"剩余学生数: {total}")
```

#### 案例2：事务与高级查询
```python
# 事务处理
import sqlite3

print("\n===事务处理与聚合查询===")

def demonstrate_transactions():
    """演示事务的原子性"""
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    
    # 建表
    conn.execute("""
        CREATE TABLE accounts (
            id      INTEGER PRIMARY KEY,
            owner   TEXT NOT NULL,
            balance REAL NOT NULL CHECK(balance >= 0)
        )
    """)
    conn.execute("INSERT INTO accounts VALUES (1, '张三', 1000.0)")
    conn.execute("INSERT INTO accounts VALUES (2, '李四', 500.0)")
    conn.commit()
    
    def transfer(conn, from_id: int, to_id: int, amount: float) -> bool:
        """转账（事务保证原子性）"""
        try:
            with conn:  # with 语句：成功则 commit，失败则 rollback
                # 检查余额
                balance = conn.execute(
                    "SELECT balance FROM accounts WHERE id = ?", (from_id,)
                ).fetchone()[0]
                
                if balance < amount:
                    raise ValueError(f"余额不足（现有 {balance}，转账 {amount}）")
                
                conn.execute(
                    "UPDATE accounts SET balance = balance - ? WHERE id = ?",
                    (amount, from_id)
                )
                conn.execute(
                    "UPDATE accounts SET balance = balance + ? WHERE id = ?",
                    (amount, to_id)
                )
            return True
        except ValueError as e:
            print(f"  转账失败: {e}")
            return False
    
    def show_balances(conn):
        for row in conn.execute("SELECT owner, balance FROM accounts"):
            print(f"  {row['owner']}: ¥{row['balance']:.2f}")
    
    print("初始余额:")
    show_balances(conn)
    
    # 成功转账
    print("\n张三向李四转账 300 元:")
    transfer(conn, 1, 2, 300)
    show_balances(conn)
    
    # 失败转账（余额不足）
    print("\n张三向李四转账 5000 元（余额不足）:")
    transfer(conn, 1, 2, 5000)
    show_balances(conn)  # 余额不变，事务回滚了
    
    conn.close()

demonstrate_transactions()

# 聚合查询示例
def aggregation_demo():
    """聚合查询：GROUP BY、HAVING、子查询"""
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    
    conn.executescript("""
        CREATE TABLE orders (
            id          INTEGER PRIMARY KEY,
            customer    TEXT,
            product     TEXT,
            quantity    INTEGER,
            unit_price  REAL,
            order_date  DATE
        );
        INSERT INTO orders VALUES (1,'张三','Python书',2,89.9,'2024-01-01');
        INSERT INTO orders VALUES (2,'李四','键盘',1,399.0,'2024-01-02');
        INSERT INTO orders VALUES (3,'张三','鼠标',1,99.0,'2024-01-03');
        INSERT INTO orders VALUES (4,'王五','Python书',3,89.9,'2024-01-04');
        INSERT INTO orders VALUES (5,'李四','显示器',1,1299.0,'2024-01-05');
        INSERT INTO orders VALUES (6,'张三','键盘',1,399.0,'2024-01-06');
    """)
    
    print("\n===聚合查询===")
    
    # 按客户统计总消费
    print("各客户总消费:")
    for row in conn.execute("""
        SELECT customer, 
               COUNT(*) as order_count,
               SUM(quantity * unit_price) as total_amount
        FROM orders
        GROUP BY customer
        ORDER BY total_amount DESC
    """):
        print(f"  {row['customer']}: {row['order_count']}单，合计 ¥{row['total_amount']:.2f}")
    
    # HAVING 过滤
    print("\n消费超过500元的客户:")
    for row in conn.execute("""
        SELECT customer, SUM(quantity * unit_price) as total
        FROM orders
        GROUP BY customer
        HAVING total > 500
    """):
        print(f"  {row['customer']}: ¥{row['total']:.2f}")
    
    conn.close()

aggregation_demo()
```

### 代码说明

**案例1代码解释**：
1. `conn.row_factory = sqlite3.Row`：让查询结果变成类字典对象，可用 `row["列名"]` 访问
2. `?` 占位符是防 SQL 注入的正确方式——永远不要用 f-string 拼接 SQL
3. `executemany(sql, list_of_tuples)` 批量操作比循环 `execute` 快很多
4. `conn.total_changes` 返回连接建立以来所有 SQL 修改的总行数

**案例2代码解释**：
1. `with conn:` 作为事务上下文：代码块成功则 commit，抛出异常则 rollback
2. `CHECK(balance >= 0)` 是数据库层面的约束，比应用层检查更可靠
3. 事务保证了转账操作的原子性——要么全成功，要么全回滚，不会出现扣款成功但加款失败的情况
4. `GROUP BY` 分组后 `HAVING` 筛选（WHERE 在分组前过滤，HAVING 在分组后过滤）

---

## 2. SQLAlchemy ORM

### 知识点解析

**概念定义**：ORM（对象关系映射）是一种将数据库表映射为 Python 类、将表的行映射为类实例的技术。SQLAlchemy 是 Python 最流行的 ORM，让我们用 Python 对象来操作数据库而不用写 SQL。就像有个翻译官，把"Python语言"自动翻译成"SQL语言"。

**SQLAlchemy 两层 API**：
- **Core**：接近原始 SQL，性能好，适合复杂查询
- **ORM**：面向对象，代码直观，适合 CRUD 业务

**核心规则**：
1. 定义模型：继承 `Base = declarative_base()` 的类
2. 创建表：`Base.metadata.create_all(engine)`
3. 操作数据：通过 `Session` 进行，`session.add()`、`session.query()`、`session.commit()`
4. SQLAlchemy 2.0+ 推荐使用 `Session` 上下文管理器和新风格查询 `select(Model)`

**常见易错点**：
1. 未调用 `session.commit()` 导致修改不持久化
2. Session 未关闭导致连接泄漏，应使用 `with Session() as session:` 或 `try/finally`
3. 懒加载问题：在 Session 关闭后访问关联属性会报 `DetachedInstanceError`
4. 安装：`pip install sqlalchemy`（Core 功能），连接 MySQL 还需 `pip install pymysql`

### 实战案例

#### 案例1：SQLAlchemy ORM 基础
```python
# SQLAlchemy ORM 示例
# 安装：pip install sqlalchemy
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey, func
from sqlalchemy.orm import DeclarativeBase, Session, relationship
from datetime import datetime

print("===SQLAlchemy ORM===")

# 1. 定义基类
class Base(DeclarativeBase):
    pass

# 2. 定义模型（映射数据库表）
class Department(Base):
    __tablename__ = "departments"
    
    id   = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)
    
    # 关系：一个部门对应多个员工
    employees = relationship("Employee", back_populates="department")
    
    def __repr__(self) -> str:
        return f"Department(id={self.id}, name={self.name!r})"

class Employee(Base):
    __tablename__ = "employees"
    
    id            = Column(Integer, primary_key=True)
    name          = Column(String(50), nullable=False)
    salary        = Column(Float, nullable=False)
    hire_date     = Column(DateTime, default=datetime.now)
    department_id = Column(Integer, ForeignKey("departments.id"))
    
    # 关系：多个员工对应一个部门
    department = relationship("Department", back_populates="employees")
    
    def __repr__(self) -> str:
        return f"Employee(id={self.id}, name={self.name!r}, salary={self.salary})"

# 3. 创建引擎和表
engine = create_engine(
    "sqlite:///:memory:",
    echo=False,   # True 时打印 SQL，调试时很有用
)
Base.metadata.create_all(engine)
print("数据库表创建完成")

# 4. 插入数据
with Session(engine) as session:
    # 创建部门
    depts = [
        Department(name="研发部"),
        Department(name="产品部"),
        Department(name="运营部"),
    ]
    session.add_all(depts)
    session.flush()  # flush 但不 commit，先获取 id
    
    # 创建员工
    employees = [
        Employee(name="张三", salary=15000, department=depts[0]),
        Employee(name="李四", salary=18000, department=depts[0]),
        Employee(name="王五", salary=12000, department=depts[1]),
        Employee(name="赵六", salary=20000, department=depts[1]),
        Employee(name="钱七", salary=10000, department=depts[2]),
    ]
    session.add_all(employees)
    session.commit()
    print("样本数据插入完成")

# 5. 查询操作
print("\n=== ORM 查询 ===")
with Session(engine) as session:
    # 查询全部
    all_emp = session.query(Employee).all()
    print(f"全部员工: {[e.name for e in all_emp]}")
    
    # 条件查询
    rich = session.query(Employee).filter(Employee.salary >= 15000).all()
    print(f"\n薪资>=15000的员工: {[e.name for e in rich]}")
    
    # 关联查询（访问关系属性）
    print("\n员工与部门:")
    for emp in session.query(Employee).all():
        dept_name = emp.department.name if emp.department else "无部门"
        print(f"  {emp.name}: {dept_name}, ¥{emp.salary:,.0f}")
    
    # 聚合查询
    print("\n各部门薪资统计:")
    stats = (
        session.query(
            Department.name,
            func.count(Employee.id).label("count"),
            func.avg(Employee.salary).label("avg_salary"),
        )
        .join(Employee)
        .group_by(Department.id)
        .all()
    )
    for dept_name, count, avg_sal in stats:
        print(f"  {dept_name}: {count}人, 平均薪资 ¥{avg_sal:,.0f}")

# 6. 更新和删除
print("\n=== 更新和删除 ===")
with Session(engine) as session:
    # 更新
    emp = session.query(Employee).filter_by(name="张三").first()
    if emp:
        emp.salary = 17000  # 直接修改属性
        session.commit()
        print(f"张三薪资更新为: ¥{emp.salary:,.0f}")
    
    # 批量更新
    session.query(Employee).filter(
        Employee.department.has(Department.name == "运营部")
    ).update({"salary": Employee.salary * 1.1})
    session.commit()
    
    # 查询验证
    ops = session.query(Employee).join(Department).filter(Department.name == "运营部").all()
    for e in ops:
        print(f"运营部 {e.name} 调薪后: ¥{e.salary:,.0f}")
    
    # 删除
    emp_to_del = session.query(Employee).filter_by(name="钱七").first()
    if emp_to_del:
        session.delete(emp_to_del)
        session.commit()
        print(f"已删除: 钱七")
    
    remaining = session.query(func.count(Employee.id)).scalar()
    print(f"剩余员工数: {remaining}")
```

### 代码说明

**案例1代码解释**：
1. `DeclarativeBase`（SQLAlchemy 2.0+）是定义模型的基类，`__tablename__` 指定对应的数据库表名
2. `relationship("Employee", back_populates="department")` 定义双向关系，`back_populates` 必须在两端都声明
3. `session.flush()` 将变更发送到数据库但不提交事务，可用于在 commit 前获取自增 ID
4. `filter_by(name="张三")` 等于号精确匹配；`filter(Model.salary >= 15000)` 支持比较运算符
5. `func.count()`、`func.avg()` 等对应 SQL 聚合函数，`label("别名")` 设置结果列别名

---

## 3. 连接池与最佳实践

### 知识点解析

**概念定义**：数据库连接池是一组预先建立的数据库连接，应用需要时从池中取一个，用完还回去，避免频繁建立/断开连接的开销。就像公司的公务车，多人共用，用完还回停车场。

**SQLAlchemy 内置连接池**（无需额外配置）：
- `create_engine(url, pool_size=5, max_overflow=10, pool_timeout=30, pool_recycle=3600)`
- `pool_size`：池中保持的连接数
- `max_overflow`：超出 pool_size 的临时连接数
- `pool_recycle`：连接生存时间（秒），避免数据库断开过期连接

**最佳实践总结**：
1. 永远用参数化查询（`?` 或 `:param`），绝对不拼接 SQL 字符串
2. `with Session() as session:` 确保 Session 正确关闭
3. 只在需要时 `commit`，长事务持有连接会阻塞其他操作
4. 生产环境用 `pool_recycle` 定期重建连接，避免数据库侧连接超时断开
5. 异步场景用 `AsyncSession` + `create_async_engine`

---

## 4. 知识点小结

| 场景 | 推荐方案 |
|------|---------|
| 本地轻量应用、学习、原型 | sqlite3 内置模块 |
| 业务系统、需要 ORM | SQLAlchemy ORM |
| 高性能、复杂查询 | SQLAlchemy Core |
| 异步 Web 应用 | SQLAlchemy AsyncSession + aiomysql/aiosqlite |
| 大数据 ETL | 直接使用 pandas + SQLAlchemy |

**安装命令**：
```bash
pip install sqlalchemy          # SQLAlchemy（包含 SQLite 支持）
pip install pymysql             # MySQL 连接驱动
pip install psycopg2-binary     # PostgreSQL 连接驱动
pip install aiosqlite           # 异步 SQLite
pip install aiomysql            # 异步 MySQL
```

**学习建议**：
1. 先熟练掌握 sqlite3，理解 SQL 基础（SELECT/INSERT/UPDATE/DELETE/JOIN/GROUP BY）
2. 再学习 SQLAlchemy ORM，用 Python 对象方式操作数据库
3. 复杂查询和性能优化时，不要怕写原生 SQL，ORM 允许执行原始 SQL
4. 生产环境一定要配置连接池参数，避免连接泄漏和超时问题
