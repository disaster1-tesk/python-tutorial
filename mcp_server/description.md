# MCP Server 配置与开发

---

## 学习目标

完成本章节学习后，你将能够：

| 目标 | 描述 | 重要性 |
|------|------|--------|
| 理解MCP Server架构 | 掌握MCP服务器的工作原理和架构 | ⭐⭐⭐ 必备 |
| 搭建开发环境 | 学会配置MCP Server开发环境 | ⭐⭐⭐ 必备 |
| 实现基础MCP Server | 能够创建并运行一个简单的MCP服务器 | ⭐⭐⭐ 必备 |
| 定义工具 | 学会在MCP Server中定义自定义工具 | ⭐⭐⭐ 必备 |
| 实现资源暴露 | 学会暴露文件和API作为MCP资源 | ⭐⭐ 重要 |
| 配置连接 | 掌握MCP Server的连接配置方法 | ⭐⭐ 重要 |
| 调试技能 | 掌握MCP Server的调试技巧 | ⭐⭐ 重要 |

---

## 预习检查

在开始学习之前，请尝试回答以下问题：

1. MCP Server和传统API服务器有什么区别？
2. 如何在本地搭建MCP Server开发环境？
3. MCP Server的核心组件有哪些？
4. 如何让AI应用连接到MCP Server？

如果你对以上问题还有疑惑，不用担心，通过本章节的学习，你会找到答案！

---

## 章节概览

```
┌─────────────────────────────────────────────────────────┐
│              MCP Server 配置与开发                         │
├─────────────────────────────────────────────────────────┤
│  1. MCP Server简介  │ 理解服务器角色与职责                 │
│  2. 开发环境搭建    │ Python环境配置与依赖安装              │
│  3. 基础服务器创建  │ 从零创建第一个MCP服务器               │
│  4. 工具开发       │ 自定义工具的实现与注册                │
│  5. 资源暴露       │ 文件系统和API资源暴露                │
│  6. 连接配置       │ 主机与服务器的连接配置                │
│  7. 调试部署       │ 开发调试与生产部署                    │
└─────────────────────────────────────────────────────────┘
```

---

## 1. MCP Server简介

### 知识点解析

**概念定义**：MCP Server是MCP协议架构中的服务端组件，负责向AI应用暴露各种能力，包括工具（Tools）、资源（Resources）和提示模板（Prompts）。它是连接AI模型与外部世界的桥梁。

**MCP Server的核心职责**：

1. **工具暴露**：提供可被AI调用的外部函数
2. **资源提供**：暴露文件、数据库、API等数据源
3. **提示模板**：提供标准化的交互模式
4. **协议处理**：处理JSON-RPC通信

**MCP Server的技术特点**：

- 基于JSON-RPC 2.0通信协议
- 支持stdio和SSE两种传输方式
- 可使用Python、TypeScript等多种语言开发
- 标准化接口，便于集成和扩展

### 常见的MCP Server类型

| 类型 | 功能 | 示例 |
|------|------|------|
| 文件系统服务器 | 文件读写操作 | `mcp-server-filesystem` |
| 数据库服务器 | 数据库查询 | `mcp-server-postgres` |
| API服务器 | 外部API集成 | `mcp-server-github` |
| 浏览器服务器 | 浏览器自动化 | `puppeteer-mcp` |
| 自定义服务器 | 业务功能封装 | 自定义开发 |

---

## 2. 开发环境搭建

### 知识点解析

**Python环境要求**：

MCP Server开发需要Python 3.10或更高版本。建议使用虚拟环境隔离项目依赖。

**核心依赖包**：

| 包名 | 作用 |
|------|------|
| `mcp` | MCP协议核心库 |
| `fastapi` | 构建HTTP API（可选） |
| `uvicorn` | ASGI服务器（可选） |
| `pydantic` | 数据验证 |

### 环境配置步骤

**步骤1：创建虚拟环境**
```bash
# 创建虚拟环境
python -m venv mcp-env

# 激活虚拟环境
# Windows:
mcp-env\Scripts\activate
# Linux/Mac:
source mcp-env/bin/activate
```

**步骤2：安装依赖**
```bash
# 安装MCP核心库
pip install mcp

# 安装开发依赖
pip install fastapi uvicorn pydantic
```

**步骤3：验证安装**
```python
# 验证MCP安装
import mcp
print(f"MCP版本: {mcp.__version__}")
```

### 常见错误详解

**错误1：Python版本过低**
```bash
# ❌ 错误
python --version  # Python 3.9

# ✅ 正确做法
# 确保Python版本 >= 3.10
python --version  # Python 3.11+
```

**错误2：依赖冲突**
```bash
# ❌ 错误
# 不同项目使用相同的全局Python环境

# ✅ 正确做法
# 使用虚拟环境隔离项目依赖
python -m venv myproject-env
```

---

## 3. 基础服务器创建

### 知识点解析

**服务器创建流程**：

使用MCP SDK创建服务器的基本步骤：

```python
from mcp.server import Server
from mcp.server.stdio import stdio_server
import asyncio

# 1. 创建服务器实例
app = Server("my-first-server")

# 2. 注册请求处理器
@app.list_tools()
async def list_tools():
    """列出可用工具"""
    return []

@app.call_tool()
async def call_tool(name: str, arguments: dict):
    """处理工具调用"""
    return "result"

# 3. 启动服务器
async def main():
    async with stdio_server() as streams:
        await app.run(
            streams[0],
            streams[1],
            app.create_initialization_options()
        )

if __name__ == "__main__":
    asyncio.run(main())
```

### 服务器结构解析

**核心组件**：

1. **Server对象**：服务器主实例，管理所有能力和请求
2. **工具列表处理器**：返回服务器提供的所有工具
3. **工具调用处理器**：处理AI的工具调用请求
4. **资源列表处理器**：返回可访问的资源
5. **提示列表处理器**：返回可用的提示模板

### 工具注册方法

**使用装饰器注册**：

```python
from mcp.server import Server
from mcp.types import Tool

app = Server("demo-server")

@app.list_tools()
async def list_tools():
    return [
        Tool(
            name="greet",
            description="向用户打招呼",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "用户名称"
                    }
                },
                "required": ["name"]
            }
        )
    ]

@app.call_tool()
async def call_tool(name: str, arguments: dict):
    if name == "greet":
        return f"你好，{arguments['name']}！"
    raise ValueError(f"未知工具: {name}")
```

---

## 4. 工具开发

### 知识点解析

**工具定义规范**：

MCP工具需要定义以下属性：

1. **name**：工具名称（唯一标识符）
2. **description**：工具功能描述（帮助AI理解何时使用）
3. **inputSchema**：输入参数模式（定义参数类型和约束）

**输入模式示例**：

```python
inputSchema = {
    "type": "object",
    "properties": {
        "param_name": {
            "type": "string",        # 参数类型
            "description": "参数描述",  # 参数说明
            "default": "默认值",      # 默认值
            "enum": ["A", "B"]       # 枚举值
        }
    },
    "required": ["param_name"],     # 必需参数
    "additionalProperties": False    # 是否允许额外参数
}
```

### 工具实现模式

**同步工具**：

```python
@app.call_tool()
async def call_tool(name: str, arguments: dict):
    """同步执行工具"""
    if name == "calculate":
        # 直接返回结果
        result = eval(arguments["expression"])
        return str(result)
```

**异步工具**：

```python
@app.call_tool()
async def call_tool(name: str, arguments: dict):
    """异步执行工具"""
    if name == "fetch_data":
        # 异步获取数据
        async with aiohttp.ClientSession() as session:
            async with session.get(arguments["url"]) as response:
                data = await response.json()
        return json.dumps(data)
```

### 工具错误处理

```python
@app.call_tool()
async def call_tool(name: str, arguments: dict):
    try:
        if name == "risky_operation":
            # 可能的失败操作
            result = risky_function(arguments)
            return result
    except ValueError as e:
        # 返回格式化的错误信息
        return f"参数错误: {str(e)}"
    except Exception as e:
        return f"执行错误: {str(e)}"
```

---

## 5. 资源暴露

### 知识点解析

**资源与工具的区别**：

- **工具**：执行操作，可能有副作用
- **资源**：提供数据，只读访问

**资源暴露方法**：

```python
from mcp.types import Resource

@app.list_resources()
async def list_resources():
    """列出可用资源"""
    return [
        Resource(
            uri="file:///config/app.json",
            name="app_config",
            description="应用程序配置文件",
            mimeType="application/json"
        ),
        Resource(
            uri="file:///docs/readme.txt",
            name="readme",
            description="项目README文档"
        )
    ]

@app.read_resource()
async def read_resource(uri: str):
    """读取资源内容"""
    if uri.startswith("file://"):
        # 读取文件
        file_path = uri.replace("file://", "")
        with open(file_path, "r") as f:
            content = f.read()
        return content
    
    raise ValueError(f"不支持的资源类型: {uri}")
```

### 动态资源

```python
@app.list_resources()
async def list_resources():
    """动态生成资源列表"""
    resources = []
    
    # 动态扫描目录中的文件
    for file in os.listdir("./docs"):
        resources.append(Resource(
            uri=f"file://./docs/{file}",
            name=file,
            description=f"文档: {file}"
        ))
    
    return resources
```

---

## 6. 连接配置

### 知识点解析

**MCP Server的连接方式**：

MCP支持两种主要的传输方式：

1. **stdio传输**：通过标准输入输出通信，适合本地进程
2. **SSE传输**：通过Server-Sent Events通信，适合远程服务

### stdio连接配置

**在Claude Desktop中配置**：

```json
{
  "mcpServers": {
    "my-server": {
      "command": "python",
      "args": ["/path/to/server.py"],
      "env": {
        "KEY": "value"
      }
    }
  }
}
```

**环境变量配置**：

```python
import os

# 读取环境变量
api_key = os.getenv("API_KEY")
db_path = os.getenv("DB_PATH", "./default.db")
```

### SSE连接配置

**使用FastAPI构建SSE服务器**：

```python
from fastapi import FastAPI
from mcp.server.sse import SseServerTransport
from starlette.requests import Request
from starlette.responses import StreamingResponse

app = FastAPI()

@app.route("/mcp", methods=["GET"])
async def mcp_sse(request: Request):
    """SSE端点"""
    transport = SseServerTransport("/messages")
    async with transport.connect() as streams:
        await app.run(
            streams[0],
            streams[1],
            app.create_initialization_options()
        )

@app.route("/messages", methods=["POST"])
async def messages(request: Request):
    """消息处理"""
    # 处理JSON-RPC消息
    pass
```

---

## 7. 调试与部署

### 知识点解析

**本地调试技巧**：

1. **日志输出**：使用print或logging记录调试信息
2. **消息追踪**：打印所有传入的JSON-RPC消息
3. **逐步测试**：先测试工具列表，再测试工具调用
4. **错误捕获**：捕获并记录所有异常

**调试代码示例**：

```python
import logging

# 配置日志
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger("mcp-server")

@app.call_tool()
async def call_tool(name: str, arguments: dict):
    logger.debug(f"调用工具: {name}")
    logger.debug(f"参数: {arguments}")
    
    try:
        result = execute_tool(name, arguments)
        logger.debug(f"结果: {result}")
        return result
    except Exception as e:
        logger.error(f"错误: {e}")
        raise
```

### 生产部署

**Docker部署示例**：

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY server.py .

CMD ["python", "server.py"]
```

**Docker Compose**：

```yaml
version: '3.8'
services:
  mcp-server:
    build: .
    environment:
      - API_KEY=${API_KEY}
      - DB_PATH=/data/app.db
    volumes:
      - ./data:/data

  claude-desktop:
    image: claude-desktop
    depends_on:
      - mcp-server
```

---

## 实战案例

### 案例1：完整的MCP Server实现

```python
"""
完整的MCP Server示例
包含工具、资源和提示模板
"""

from mcp.server import Server
from mcp.types import Tool, Resource, TextContent
from mcp.server.stdio import stdio_server
import asyncio
import json
import os


class DemoServer:
    """演示MCP服务器"""
    
    def __init__(self):
        self.server = Server("demo-mcp-server")
        self._register_handlers()
    
    def _register_handlers(self):
        """注册所有处理器"""
        
        @self.server.list_tools()
        async def list_tools():
            """列出所有工具"""
            return [
                Tool(
                    name="read_file",
                    description="读取文本文件内容",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "path": {
                                "type": "string",
                                "description": "文件路径"
                            }
                        },
                        "required": ["path"]
                    }
                ),
                Tool(
                    name="write_file",
                    description="写入文本到文件",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "path": {
                                "type": "string",
                                "description": "文件路径"
                            },
                            "content": {
                                "type": "string",
                                "description": "文件内容"
                            }
                        },
                        "required": ["path", "content"]
                    }
                ),
                Tool(
                    name="list_directory",
                    description="列出目录内容",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "path": {
                                "type": "string",
                                "description": "目录路径",
                                "default": "."
                            }
                        },
                        "required": []
                    }
                ),
                Tool(
                    name="get_system_info",
                    description="获取系统信息",
                    inputSchema={
                        "type": "object",
                        "properties": {},
                        "required": []
                    }
                )
            ]
        
        @self.server.call_tool()
        async def call_tool(name: str, arguments: dict):
            """处理工具调用"""
            
            if name == "read_file":
                path = arguments.get("path")
                try:
                    with open(path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    return [TextContent(type="text", text=content)]
                except FileNotFoundError:
                    return [TextContent(type="text", text=f"文件不存在: {path}")]
                except Exception as e:
                    return [TextContent(type="text", text=f"读取错误: {str(e)}")]
            
            elif name == "write_file":
                path = arguments.get("path")
                content = arguments.get("content")
                try:
                    with open(path, 'w', encoding='utf-8') as f:
                        f.write(content)
                    return [TextContent(type="text", text=f"成功写入文件: {path}")]
                except Exception as e:
                    return [TextContent(type="text", text=f"写入错误: {str(e)}")]
            
            elif name == "list_directory":
                path = arguments.get("path", ".")
                try:
                    files = os.listdir(path)
                    result = f"目录 {path} 内容:\n"
                    for f in files:
                        result += f"  - {f}\n"
                    return [TextContent(type="text", text=result)]
                except Exception as e:
                    return [TextContent(type="text", text=f"错误: {str(e)}")]
            
            elif name == "get_system_info":
                info = {
                    "platform": os.name,
                    "cwd": os.getcwd(),
                    "python_version": os.sys.version
                }
                return [TextContent(type="text", text=json.dumps(info, indent=2))]
            
            else:
                raise ValueError(f"未知工具: {name}")
        
        @self.server.list_resources()
        async def list_resources():
            """列出所有资源"""
            return [
                Resource(
                    uri="config://server/settings",
                    name="server_settings",
                    description="服务器配置",
                    mimeType="application/json"
                ),
                Resource(
                    uri="file://README.md",
                    name="readme",
                    description="项目README"
                )
            ]
        
        @self.server.read_resource()
        async def read_resource(uri: str):
            """读取资源"""
            if uri == "config://server/settings":
                return json.dumps({
                    "version": "1.0.0",
                    "debug": True,
                    "max_file_size": 1024 * 1024
                })
            elif uri.startswith("file://"):
                path = uri.replace("file://", "")
                with open(path, 'r', encoding='utf-8') as f:
                    return f.read()
            raise ValueError(f"未知资源: {uri}")
        
        @self.server.list_prompts()
        async def list_prompts():
            """列出所有提示模板"""
            return []
    
    async def run(self):
        """运行服务器"""
        async with stdio_server() as streams:
            await self.server.run(
                streams[0],
                streams[1],
                self.server.create_initialization_options()
            )


async def main():
    """主函数"""
    print("启动MCP演示服务器...")
    server = DemoServer()
    await server.run()


if __name__ == "__main__":
    asyncio.run(main())
```

### 案例2：数据库MCP Server

```python
"""
数据库MCP Server示例
支持SQLite数据库操作
"""

from mcp.server import Server
from mcp.types import Tool, TextContent
from mcp.server.stdio import stdio_server
import sqlite3
import asyncio
import json


class DatabaseServer:
    """数据库MCP服务器"""
    
    def __init__(self, db_path: str = ":memory:"):
        self.server = Server("database-mcp-server")
        self.db_path = db_path
        self._init_database()
        self._register_handlers()
    
    def _init_database(self):
        """初始化数据库"""
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row
        
        # 创建示例表
        cursor = self.conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        self.conn.commit()
        
        # 插入示例数据
        cursor.execute("SELECT COUNT(*) FROM users")
        if cursor.fetchone()[0] == 0:
            cursor.executemany(
                "INSERT INTO users (name, email) VALUES (?, ?)",
                [
                    ("张三", "zhangsan@example.com"),
                    ("李四", "lisi@example.com"),
                    ("王五", "wangwu@example.com")
                ]
            )
            self.conn.commit()
    
    def _register_handlers(self):
        """注册处理器"""
        
        @self.server.list_tools()
        async def list_tools():
            return [
                Tool(
                    name="query_users",
                    description="查询用户列表",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "limit": {
                                "type": "number",
                                "description": "返回数量限制",
                                "default": 10
                            }
                        },
                        "required": []
                    }
                ),
                Tool(
                    name="add_user",
                    description="添加新用户",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "name": {
                                "type": "string",
                                "description": "用户名称"
                            },
                            "email": {
                                "type": "string",
                                "description": "用户邮箱"
                            }
                        },
                        "required": ["name", "email"]
                    }
                ),
                Tool(
                    name="search_users",
                    description="搜索用户",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "keyword": {
                                "type": "string",
                                "description": "搜索关键词"
                            }
                        },
                        "required": ["keyword"]
                    }
                ),
                Tool(
                    name="get_table_info",
                    description="获取表信息",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "table_name": {
                                "type": "string",
                                "description": "表名"
                            }
                        },
                        "required": ["table_name"]
                    }
                )
            ]
        
        @self.server.call_tool()
        async def call_tool(name: str, arguments: dict):
            cursor = self.conn.cursor()
            
            if name == "query_users":
                limit = arguments.get("limit", 10)
                cursor.execute("SELECT * FROM users LIMIT ?", (limit,))
                rows = cursor.fetchall()
                
                result = "用户列表:\n"
                for row in rows:
                    result += f"  ID: {row['id']}, 姓名: {row['name']}, 邮箱: {row['email']}\n"
                
                return [TextContent(type="text", text=result)]
            
            elif name == "add_user":
                name = arguments.get("name")
                email = arguments.get("email")
                
                try:
                    cursor.execute(
                        "INSERT INTO users (name, email) VALUES (?, ?)",
                        (name, email)
                    )
                    self.conn.commit()
                    return [TextContent(type="text", text=f"成功添加用户: {name}")]
                except sqlite3.IntegrityError:
                    return [TextContent(type="text", text="错误: 邮箱已存在")]
            
            elif name == "search_users":
                keyword = arguments.get("keyword")
                cursor.execute(
                    "SELECT * FROM users WHERE name LIKE ? OR email LIKE ?",
                    (f"%{keyword}%", f"%{keyword}%")
                )
                rows = cursor.fetchall()
                
                if not rows:
                    return [TextContent(type="text", text="未找到匹配用户")]
                
                result = f"找到 {len(rows)} 个用户:\n"
                for row in rows:
                    result += f"  ID: {row['id']}, 姓名: {row['name']}, 邮箱: {row['email']}\n"
                
                return [TextContent(type="text", text=result)]
            
            elif name == "get_table_info":
                table_name = arguments.get("table_name")
                cursor.execute(f"PRAGMA table_info({table_name})")
                columns = cursor.fetchall()
                
                result = f"表 {table_name} 结构:\n"
                for col in columns:
                    result += f"  {col['name']}: {col['type']} "
                    result += "NOT NULL" if col['notnull'] else ""
                    result += " PRIMARY KEY" if col['pk'] else ""
                    result += "\n"
                
                return [TextContent(type="text", text=result)]
            
            raise ValueError(f"未知工具: {name}")
    
    async def run(self):
        async with stdio_server() as streams:
            await self.server.run(
                streams[0],
                streams[1],
                self.server.create_initialization_options()
            )


async def main():
    print("启动数据库MCP服务器...")
    db_path = os.getenv("DB_PATH", ":memory:")
    server = DatabaseServer(db_path)
    await server.run()


if __name__ == "__main__":
    import os
    asyncio.run(main())
```

### 案例3：API集成MCP Server

```python
"""
API集成MCP Server示例
展示如何集成外部API
"""

from mcp.server import Server
from mcp.types import Tool, TextContent
from mcp.server.stdio import stdio_server
import asyncio
import aiohttp
import os


class APIServer:
    """API集成MCP服务器"""
    
    def __init__(self):
        self.server = Server("api-mcp-server")
        self.session = None
        self._register_handlers()
    
    def _register_handlers():
        """注册处理器"""
        
        @self.server.list_tools()
        async def list_tools():
            return [
                Tool(
                    name="get_weather",
                    description="获取天气信息",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "city": {
                                "type": "string",
                                "description": "城市名称"
                            }
                        },
                        "required": ["city"]
                    }
                ),
                Tool(
                    name="fetch_url",
                    description="获取网页内容",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "url": {
                                "type": "string",
                                "description": "网页URL"
                            }
                        },
                        "required": ["url"]
                    }
                )
            ]
        
        @self.server.call_tool()
        async def call_tool(name: str, arguments: dict):
            if name == "get_weather":
                # 示例：实际需要API密钥
                city = arguments.get("city")
                return [TextContent(
                    type="text",
                    text=f"城市: {city}\n天气: 晴\n温度: 25°C"
                )]
            
            elif name == "fetch_url":
                url = arguments.get("url")
                try:
                    async with aiohttp.ClientSession() as session:
                        async with session.get(url) as response:
                            content = await response.text()
                            return [TextContent(
                                type="text",
                                text=f"状态: {response.status}\n内容长度: {len(content)}"
                            )]
                except Exception as e:
                    return [TextContent(type="text", text=f"错误: {str(e)}")]
            
            raise ValueError(f"未知工具: {name}")
    
    async def run(self):
        async with stdio_server() as streams:
            await self.server.run(
                streams[0],
                streams[1],
                self.server.create_initialization_options()
            )


async def main():
    print("启动API集成MCP服务器...")
    server = APIServer()
    await server.run()


if __name__ == "__main__":
    asyncio.run(main())
```

---

## 本章小结

本章我们学习了MCP Server的配置与开发：

1. **MCP Server简介**：理解了服务器的角色和职责
2. **开发环境搭建**：掌握了Python环境和依赖配置
3. **基础服务器创建**：学会了创建第一个MCP服务器
4. **工具开发**：掌握了自定义工具的实现方法
5. **资源暴露**：学会了文件和API资源的暴露
6. **连接配置**：掌握了stdio和SSE连接配置
7. **调试部署**：学会了调试技巧和Docker部署

通过这些内容，你已经具备独立开发MCP Server的能力，可以根据业务需求创建各种功能扩展。
