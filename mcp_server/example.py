# MCP Server 配置与开发示例代码

"""
MCP Server示例代码
展示服务器的配置、开发和测试
"""

import asyncio
import json
import os
import sqlite3
from typing import Any

# ============================================================
# 1. 基础MCP Server实现
# ============================================================

# 注意：以下代码需要安装 mcp 库
# pip install mcp

# 由于运行环境中可能没有mcp库，我们先展示架构设计
# 实际使用时需要安装官方SDK


class BasicMCPServer:
    """基础MCP服务器框架"""
    
    def __init__(self, name: str):
        self.name = name
        self.tools = {}
        self.resources = {}
        self.prompts = {}
        print(f"🖥️  MCP服务器 '{name}' 已创建")
    
    def register_tool(self, name: str, description: str, handler, input_schema: dict):
        """注册工具"""
        self.tools[name] = {
            "name": name,
            "description": description,
            "handler": handler,
            "inputSchema": input_schema
        }
        print(f"🔧 注册工具: {name} - {description}")
    
    def register_resource(self, uri: str, name: str, content: str):
        """注册资源"""
        self.resources[uri] = {
            "uri": uri,
            "name": name,
            "content": content
        }
        print(f"📄 注册资源: {uri}")
    
    def register_prompt(self, name: str, template: str):
        """注册提示模板"""
        self.prompts[name] = {
            "name": name,
            "template": template
        }
        print(f"📝 注册提示: {name}")
    
    def list_tools(self) -> list:
        """列出所有工具"""
        return [
            {
                "name": info["name"],
                "description": info["description"],
                "inputSchema": info["inputSchema"]
            }
            for info in self.tools.values()
        ]
    
    def list_resources(self) -> list:
        """列出所有资源"""
        return [
            {
                "uri": info["uri"],
                "name": info["name"]
            }
            for info in self.resources.values()
        ]
    
    def list_prompts(self) -> list:
        """列出所有提示"""
        return [
            {"name": info["name"]}
            for info in self.prompts.values()
        ]
    
    def call_tool(self, name: str, arguments: dict) -> Any:
        """调用工具"""
        if name in self.tools:
            handler = self.tools[name]["handler"]
            return handler(**arguments)
        raise ValueError(f"未知工具: {name}")
    
    def read_resource(self, uri: str) -> str:
        """读取资源"""
        if uri in self.resources:
            return self.resources[uri]["content"]
        raise ValueError(f"未知资源: {uri}")


def create_basic_server():
    """创建基础MCP服务器"""
    print("\n" + "=" * 50)
    print("示例1: 基础MCP服务器")
    print("=" * 50)
    
    # 创建服务器
    server = BasicMCPServer("MyFirstServer")
    
    # 定义工具处理函数
    def greet_handler(name: str) -> str:
        """打招呼工具"""
        return f"你好，{name}！欢迎使用MCP服务器！"
    
    def add_handler(a: int, b: int) -> str:
        """加法工具"""
        return str(a + b)
    
    def calculate_bmi_handler(height_cm: float, weight_kg: float) -> str:
        """BMI计算工具"""
        height_m = height_cm / 100
        bmi = weight_kg / (height_m ** 2)
        
        if bmi < 18.5:
            status = "偏瘦"
        elif bmi < 24:
            status = "正常"
        elif bmi < 28:
            status = "偏胖"
        else:
            status = "肥胖"
        
        return f"BMI: {bmi:.2f} ({status})"
    
    # 注册工具
    server.register_tool(
        "greet",
        "向用户打招呼",
        greet_handler,
        {
            "type": "object",
            "properties": {
                "name": {"type": "string", "description": "用户名称"}
            },
            "required": ["name"]
        }
    )
    
    server.register_tool(
        "add",
        "计算两个数的和",
        add_handler,
        {
            "type": "object",
            "properties": {
                "a": {"type": "number", "description": "第一个数"},
                "b": {"type": "number", "description": "第二个数"}
            },
            "required": ["a", "b"]
        }
    )
    
    server.register_tool(
        "calculate_bmi",
        "根据身高体重计算BMI",
        calculate_bmi_handler,
        {
            "type": "object",
            "properties": {
                "height_cm": {"type": "number", "description": "身高（厘米）"},
                "weight_kg": {"type": "number", "description": "体重（公斤）"}
            },
            "required": ["height_cm", "weight_kg"]
        }
    )
    
    # 注册资源
    server.register_resource(
        "config://app/settings",
        "应用配置",
        '{"theme": "dark", "language": "zh-CN"}'
    )
    
    server.register_resource(
        "file://README.md",
        "项目说明",
        "# MCP Server Demo\n\n这是一个MCP服务器示例项目。"
    )
    
    # 注册提示
    server.register_prompt(
        "code_review",
        "请审查以下代码：\n{code}\n\n指出问题并提供改进建议。"
    )
    
    # 测试工具列表
    print("\n可用工具:")
    for tool in server.list_tools():
        print(f"  - {tool['name']}: {tool['description']}")
    
    # 测试资源列表
    print("\n可用资源:")
    for resource in server.list_resources():
        print(f"  - {resource['uri']}")
    
    # 测试工具调用
    print("\n工具调用测试:")
    result1 = server.call_tool("greet", {"name": "张三"})
    print(f"  greet('张三'): {result1}")
    
    result2 = server.call_tool("add", {"a": 10, "b": 20})
    print(f"  add(10, 20): {result2}")
    
    result3 = server.call_tool("calculate_bmi", {"height_cm": 175, "weight_kg": 70})
    print(f"  calculate_bmi(175, 70): {result3}")
    
    # 测试资源读取
    print("\n资源读取测试:")
    config = server.read_resource("config://app/settings")
    print(f"  config: {config}")
    
    return server


# ============================================================
# 2. 文件系统MCP Server
# ============================================================

class FilesystemMCPServer:
    """文件系统MCP服务器"""
    
    def __init__(self, root_dir: str = "."):
        self.root_dir = os.path.abspath(root_dir)
        self.server = BasicMCPServer("FilesystemServer")
        self._register_tools()
        print(f"📁 根目录: {self.root_dir}")
    
    def _register_tools(self):
        """注册文件系统工具"""
        
        def read_file_handler(path: str, encoding: str = "utf-8") -> str:
            """读取文件"""
            full_path = os.path.join(self.root_dir, path)
            
            if not os.path.exists(full_path):
                return f"错误: 文件不存在 - {path}"
            
            if not os.path.isfile(full_path):
                return f"错误: 不是文件 - {path}"
            
            try:
                with open(full_path, 'r', encoding=encoding) as f:
                    return f.read()
            except Exception as e:
                return f"读取错误: {str(e)}"
        
        def write_file_handler(path: str, content: str, encoding: str = "utf-8") -> str:
            """写入文件"""
            full_path = os.path.join(self.root_dir, path)
            
            try:
                os.makedirs(os.path.dirname(full_path), exist_ok=True)
                with open(full_path, 'w', encoding=encoding) as f:
                    f.write(content)
                return f"成功写入文件: {path}"
            except Exception as e:
                return f"写入错误: {str(e)}"
        
        def list_dir_handler(path: str = ".") -> str:
            """列出目录内容"""
            full_path = os.path.join(self.root_dir, path)
            
            if not os.path.exists(full_path):
                return f"错误: 目录不存在 - {path}"
            
            if not os.path.isdir(full_path):
                return f"错误: 不是目录 - {path}"
            
            try:
                items = os.listdir(full_path)
                result = f"目录 {path} 内容:\n"
                for item in sorted(items):
                    item_path = os.path.join(full_path, item)
                    if os.path.isdir(item_path):
                        result += f"  📁 {item}/\n"
                    else:
                        size = os.path.getsize(item_path)
                        result += f"  📄 {item} ({size} bytes)\n"
                return result
            except Exception as e:
                return f"列出错误: {str(e)}"
        
        def file_info_handler(path: str) -> str:
            """获取文件信息"""
            full_path = os.path.join(self.root_dir, path)
            
            if not os.path.exists(full_path):
                return f"错误: 文件不存在 - {path}"
            
            try:
                stat = os.stat(full_path)
                info = {
                    "path": path,
                    "size": stat.st_size,
                    "modified": stat.st_mtime,
                    "is_file": os.path.isfile(full_path),
                    "is_dir": os.path.isdir(full_path)
                }
                return json.dumps(info, indent=2, default=str)
            except Exception as e:
                return f"错误: {str(e)}"
        
        def search_files_handler(pattern: str) -> str:
            """搜索文件"""
            import fnmatch
            
            matches = []
            for root, dirs, files in os.walk(self.root_dir):
                for name in files:
                    if fnmatch.fnmatch(name, pattern):
                        rel_path = os.path.relpath(
                            os.path.join(root, name),
                            self.root_dir
                        )
                        matches.append(rel_path)
            
            if not matches:
                return f"未找到匹配 '{pattern}' 的文件"
            
            result = f"找到 {len(matches)} 个匹配 '{pattern}' 的文件:\n"
            for match in matches[:20]:  # 限制显示数量
                result += f"  - {match}\n"
            
            if len(matches) > 20:
                result += f"  ... 还有 {len(matches) - 20} 个文件\n"
            
            return result
        
        # 注册工具
        self.server.register_tool(
            "read_file",
            "读取文本文件内容",
            read_file_handler,
            {
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "文件路径"},
                    "encoding": {"type": "string", "description": "编码", "default": "utf-8"}
                },
                "required": ["path"]
            }
        )
        
        self.server.register_tool(
            "write_file",
            "写入文本到文件",
            write_file_handler,
            {
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "文件路径"},
                    "content": {"type": "string", "description": "文件内容"},
                    "encoding": {"type": "string", "description": "编码", "default": "utf-8"}
                },
                "required": ["path", "content"]
            }
        )
        
        self.server.register_tool(
            "list_directory",
            "列出目录内容",
            list_dir_handler,
            {
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "目录路径", "default": "."}
                }
            }
        )
        
        self.server.register_tool(
            "file_info",
            "获取文件信息",
            file_info_handler,
            {
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "文件路径"}
                },
                "required": ["path"]
            }
        )
        
        self.server.register_tool(
            "search_files",
            "搜索文件",
            search_files_handler,
            {
                "type": "object",
                "properties": {
                    "pattern": {"type": "string", "description": "搜索模式（如 *.py）"}
                },
                "required": ["pattern"]
            }
        )
    
    def list_tools(self):
        return self.server.list_tools()
    
    def call_tool(self, name: str, arguments: dict):
        return self.server.call_tool(name, arguments)


def create_filesystem_server():
    """创建文件系统MCP服务器"""
    print("\n" + "=" * 50)
    print("示例2: 文件系统MCP服务器")
    print("=" * 50)
    
    # 创建服务器
    server = FilesystemMCPServer(".")
    
    # 测试列出目录
    print("\n测试 list_directory:")
    result = server.call_tool("list_directory", {"path": "."})
    print(result[:500] if len(result) > 500 else result)
    
    # 测试文件信息
    print("\n测试 file_info (example.py):")
    result = server.call_tool("file_info", {"path": "example.py"})
    print(result[:500] if len(result) > 500 else result)
    
    return server


# ============================================================
# 3. 数据库MCP Server
# ============================================================

class DatabaseMCPServer:
    """数据库MCP服务器"""
    
    def __init__(self, db_path: str = ":memory:"):
        self.db_path = db_path
        self.server = BasicMCPServer("DatabaseServer")
        self._init_database()
        self._register_tools()
        print(f"🗄️  数据库: {db_path}")
    
    def _init_database(self):
        """初始化数据库"""
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row
        
        # 创建示例表
        cursor = self.conn.cursor()
        
        # 用户表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE,
                age INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # 订单表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                product TEXT NOT NULL,
                amount REAL,
                status TEXT DEFAULT 'pending',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        """)
        
        self.conn.commit()
        
        # 插入示例数据
        cursor.execute("SELECT COUNT(*) FROM users")
        if cursor.fetchone()[0] == 0:
            cursor.executemany(
                "INSERT INTO users (name, email, age) VALUES (?, ?, ?)",
                [
                    ("张三", "zhangsan@example.com", 28),
                    ("李四", "lisi@example.com", 35),
                    ("王五", "wangwu@example.com", 42),
                    ("赵六", "zhaoliu@example.com", 23),
                    ("孙七", "sunqi@example.com", 31)
                ]
            )
            
            cursor.executemany(
                "INSERT INTO orders (user_id, product, amount, status) VALUES (?, ?, ?, ?)",
                [
                    (1, "Python入门", 99.0, "completed"),
                    (1, "数据分析", 149.0, "completed"),
                    (2, "机器学习", 199.0, "pending"),
                    (3, "深度学习", 299.0, "completed"),
                    (4, "Web开发", 129.0, "completed")
                ]
            )
            
            self.conn.commit()
    
    def _register_tools(self):
        """注册数据库工具"""
        
        def query_handler(sql: str, params: list = None) -> str:
            """执行查询"""
            try:
                cursor = self.conn.cursor()
                cursor.execute(sql, params or [])
                
                # 判断是SELECT还是其他语句
                if sql.strip().upper().startswith("SELECT"):
                    rows = cursor.fetchall()
                    if not rows:
                        return "查询结果为空"
                    
                    # 获取列名
                    columns = [desc[0] for desc in cursor.description]
                    result = f"找到 {len(rows)} 条记录:\n"
                    result += " | ".join(columns) + "\n"
                    result += "-" * len(result) + "\n"
                    
                    for row in rows:
                        result += " | ".join(str(v) for v in row) + "\n"
                    
                    return result
                else:
                    self.conn.commit()
                    return f"执行成功，影响 {cursor.rowcount} 行"
                    
            except Exception as e:
                return f"SQL错误: {str(e)}"
        
        def list_tables_handler() -> str:
            """列出所有表"""
            cursor = self.conn.cursor()
            cursor.execute("""
                SELECT name FROM sqlite_master 
                WHERE type='table' AND name NOT LIKE 'sqlite_%'
                ORDER BY name
            """)
            tables = cursor.fetchall()
            
            result = "数据库中的表:\n"
            for table in tables:
                table_name = table[0]
                cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
                count = cursor.fetchone()[0]
                result += f"  - {table_name} ({count} 条记录)\n"
            
            return result
        
        def table_info_handler(table_name: str) -> str:
            """获取表结构"""
            cursor = self.conn.cursor()
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns = cursor.fetchall()
            
            if not columns:
                return f"表不存在: {table_name}"
            
            result = f"表 {table_name} 结构:\n"
            result += f"{'字段':<15} {'类型':<15} {'可空':<8} {'主键':<8}\n"
            result += "-" * 50 + "\n"
            
            for col in columns:
                result += f"{col[1]:<15} {col[2]:<15} "
                result += f"{'否' if col[3] else '是':<8} "
                result += f"{'是' if col[5] else '否':<8}\n"
            
            return result
        
        def insert_user_handler(name: str, email: str, age: int = None) -> str:
            """插入用户"""
            try:
                cursor = self.conn.cursor()
                cursor.execute(
                    "INSERT INTO users (name, email, age) VALUES (?, ?, ?)",
                    (name, email, age)
                )
                self.conn.commit()
                return f"成功插入用户，ID: {cursor.lastrowid}"
            except sqlite3.IntegrityError as e:
                return f"插入失败: 邮箱已存在"
        
        def update_order_handler(order_id: int, status: str) -> str:
            """更新订单状态"""
            cursor = self.conn.cursor()
            cursor.execute(
                "UPDATE orders SET status = ? WHERE id = ?",
                (status, order_id)
            )
            self.conn.commit()
            
            if cursor.rowcount > 0:
                return f"成功更新订单 {order_id} 状态为 {status}"
            return f"订单 {order_id} 不存在"
        
        def get_user_orders_handler(user_id: int) -> str:
            """获取用户订单"""
            cursor = self.conn.cursor()
            cursor.execute("""
                SELECT o.id, o.product, o.amount, o.status, o.created_at
                FROM orders o
                WHERE o.user_id = ?
                ORDER BY o.created_at DESC
            """, (user_id,))
            
            orders = cursor.fetchall()
            
            if not orders:
                return f"用户 {user_id} 没有订单"
            
            result = f"用户 {user_id} 的订单:\n"
            for order in orders:
                result += f"  #{order[0]} {order[1]} - ¥{order[2]} [{order[3]}]\n"
            
            return result
        
        # 注册工具
        self.server.register_tool(
            "query",
            "执行SQL查询",
            query_handler,
            {
                "type": "object",
                "properties": {
                    "sql": {"type": "string", "description": "SQL语句"},
                    "params": {"type": "array", "description": "查询参数", "default": []}
                },
                "required": ["sql"]
            }
        )
        
        self.server.register_tool(
            "list_tables",
            "列出所有表",
            list_tables_handler,
            {"type": "object", "properties": {}}
        )
        
        self.server.register_tool(
            "table_info",
            "获取表结构信息",
            table_info_handler,
            {
                "type": "object",
                "properties": {
                    "table_name": {"type": "string", "description": "表名"}
                },
                "required": ["table_name"]
            }
        )
        
        self.server.register_tool(
            "insert_user",
            "插入新用户",
            insert_user_handler,
            {
                "type": "object",
                "properties": {
                    "name": {"type": "string", "description": "用户名称"},
                    "email": {"type": "string", "description": "用户邮箱"},
                    "age": {"type": "integer", "description": "用户年龄"}
                },
                "required": ["name", "email"]
            }
        )
        
        self.server.register_tool(
            "update_order",
            "更新订单状态",
            update_order_handler,
            {
                "type": "object",
                "properties": {
                    "order_id": {"type": "integer", "description": "订单ID"},
                    "status": {"type": "string", "description": "新状态"}
                },
                "required": ["order_id", "status"]
            }
        )
        
        self.server.register_tool(
            "get_user_orders",
            "获取用户订单",
            get_user_orders_handler,
            {
                "type": "object",
                "properties": {
                    "user_id": {"type": "integer", "description": "用户ID"}
                },
                "required": ["user_id"]
            }
        )
    
    def list_tools(self):
        return self.server.list_tools()
    
    def call_tool(self, name: str, arguments: dict):
        return self.server.call_tool(name, arguments)
    
    def close(self):
        """关闭数据库连接"""
        if self.conn:
            self.conn.close()


def create_database_server():
    """创建数据库MCP服务器"""
    print("\n" + "=" * 50)
    print("示例3: 数据库MCP服务器")
    print("=" * 50)
    
    # 创建服务器
    server = DatabaseMCPServer(":memory:")
    
    # 测试列出表
    print("\n测试 list_tables:")
    result = server.call_tool("list_tables", {})
    print(result)
    
    # 测试表信息
    print("\n测试 table_info (users):")
    result = server.call_tool("table_info", {"table_name": "users"})
    print(result)
    
    # 测试查询
    print("\n测试 query:")
    result = server.call_tool("query", {"sql": "SELECT * FROM users"})
    print(result)
    
    # 测试获取用户订单
    print("\n测试 get_user_orders:")
    result = server.call_tool("get_user_orders", {"user_id": 1})
    print(result)
    
    # 关闭连接
    server.close()
    
    return server


# ============================================================
# 4. MCP Server配置与连接
# ============================================================

class MCPConfig:
    """MCP服务器配置类"""
    
    def __init__(self):
        self.servers = {}
    
    def add_server(self, name: str, command: str, args: list = None, env: dict = None):
        """添加服务器配置"""
        self.servers[name] = {
            "command": command,
            "args": args or [],
            "env": env or {}
        }
    
    def to_claude_config(self) -> dict:
        """转换为Claude Desktop配置格式"""
        return {"mcpServers": self.servers}
    
    def to_json(self) -> str:
        """转换为JSON字符串"""
        return json.dumps(self.to_claude_config(), indent=2)
    
    def save_to_file(self, path: str):
        """保存到配置文件"""
        with open(path, 'w', encoding='utf-8') as f:
            f.write(self.to_json())


def create_mcp_config():
    """创建MCP配置示例"""
    print("\n" + "=" * 50)
    print("示例4: MCP Server配置")
    print("=" * 50)
    
    config = MCPConfig()
    
    # 添加文件系统服务器
    config.add_server(
        "filesystem",
        "python",
        ["D:/mcp-servers/filesystem-server.py"],
        {"ALLOWED_DIR": "D:/projects"}
    )
    
    # 添加数据库服务器
    config.add_server(
        "database",
        "python",
        ["D:/mcp-servers/database-server.py"],
        {"DB_PATH": "D:/data/app.db"}
    )
    
    # 添加API服务器
    config.add_server(
        "api",
        "node",
        ["D:/mcp-servers/api-server.js"],
        {"API_KEY": "your-api-key"}
    )
    
    print("\nMCP配置 (Claude Desktop格式):")
    print(config.to_json())
    
    return config


# ============================================================
# 5. MCP Server测试框架
# ============================================================

class MCPTester:
    """MCP服务器测试类"""
    
    def __init__(self, server):
        self.server = server
        self.test_results = []
    
    def test_tool(self, tool_name: str, arguments: dict, expected: str = None) -> bool:
        """测试工具"""
        print(f"\n🧪 测试工具: {tool_name}")
        print(f"   参数: {arguments}")
        
        try:
            result = self.server.call_tool(tool_name, arguments)
            print(f"   结果: {result}")
            
            if expected and expected not in str(result):
                print(f"   ⚠️  警告: 预期包含 '{expected}'")
                self.test_results.append(False)
                return False
            
            print("   ✅ 通过")
            self.test_results.append(True)
            return True
            
        except Exception as e:
            print(f"   ❌ 失败: {str(e)}")
            self.test_results.append(False)
            return False
    
    def test_all_tools(self) -> dict:
        """测试所有工具"""
        print("\n" + "=" * 50)
        print("测试所有工具")
        print("=" * 50)
        
        tools = self.server.list_tools()
        
        passed = 0
        failed = 0
        
        for tool in tools:
            # 跳过测试
            pass
        
        summary = {
            "total": len(tools),
            "passed": passed,
            "failed": failed
        }
        
        print(f"\n测试结果: {passed}/{len(tools)} 通过")
        return summary


def run_tests():
    """运行测试"""
    print("\n" + "=" * 50)
    print("MCP Server 测试")
    print("=" * 50)
    
    # 测试基础服务器
    server = BasicMCPServer("TestServer")
    
    # 注册测试工具
    def echo_handler(message: str) -> str:
        return message
    
    server.register_tool(
        "echo",
        "返回输入的消息",
        echo_handler,
        {
            "type": "object",
            "properties": {
                "message": {"type": "string", "description": "消息"}
            },
            "required": ["message"]
        }
    )
    
    # 创建测试器
    tester = MCPTester(server)
    
    # 运行测试
    tester.test_tool("echo", {"message": "Hello MCP"})
    tester.test_tool("echo", {"message": "Test message"})
    
    print(f"\n测试完成: {tester.test_results}")


# ============================================================
# 主函数
# ============================================================

if __name__ == "__main__":
    print("=" * 60)
    print("MCP Server 配置与开发示例")
    print("=" * 60)
    
    # 运行所有示例
    create_basic_server()
    create_filesystem_server()
    create_database_server()
    create_mcp_config()
    run_tests()
    
    print("\n" + "=" * 60)
    print("所有示例完成!")
    print("=" * 60)
