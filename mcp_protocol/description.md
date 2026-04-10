# MCP (Model Context Protocol) 协议

---

## 学习目标

完成本章节学习后，你将能够：

| 目标 | 描述 | 重要性 |
|------|------|--------|
| 理解MCP协议 | 掌握MCP的定义、架构和核心概念 | ⭐⭐⭐ 必备 |
| 理解协议原理 | 理解MCP的通信机制和JSON-RPC交互 | ⭐⭐⭐ 必备 |
| 掌握工具定义 | 学会在MCP中定义和使用工具 | ⭐⭐⭐ 必备 |
| 掌握资源管理 | 理解MCP中资源的概念和使用方法 | ⭐⭐ 重要 |
| 理解提示模板 | 掌握MCP提示模板的使用场景 | ⭐⭐ 重要 |
| 理解协议生态 | 了解MCP的生态系统和发展趋势 | ⭐ 了解 |

---

## 预习检查

在开始学习之前，请尝试回答以下问题：

1. 什么是MCP？它解决了什么问题？
2. MCP协议与传统的API调用有什么不同？
3. MCP协议的核心组件有哪些？
4. 为什么说MCP是AI Agent的"USB接口"？

如果你对以上问题还有疑惑，不用担心，通过本章节的学习，你会找到答案！

---

## 章节概览

```
┌─────────────────────────────────────────────────────────┐
│              MCP (Model Context Protocol)                │
├─────────────────────────────────────────────────────────┤
│  1. MCP简介      │ AI与外部世界交互的新标准              │
│  2. 架构解析      │ 主机、客户端、服务器的三角关系       │
│  3. 通信机制      │ JSON-RPC消息格式与通信流程           │
│  4. 工具系统      │ AI调用外部工具的标准化方式           │
│  5. 资源系统      │ 让AI访问外部数据的统一接口           │
│  6. 提示模板      │ 标准化AI交互模式的利器               │
│  7. 生态发展      │ MCP的现状与未来趋势                  │
└─────────────────────────────────────────────────────────┘
```

---

## 1. MCP简介

### 知识点解析

**概念定义**：MCP（Model Context Protocol，模型上下文协议）是由Anthropic公司于2024年推出的开放标准协议，旨在为AI模型提供与外部世界交互的标准化方式。它的设计灵感来源于USB协议——正如USB让各种设备能够统一连接到计算机，MCP让各种外部工具和数据源能够统一连接到AI Agent。

**核心价值**：

1. **统一接口**：过去每个AI应用都需要为不同的外部工具编写专门的集成代码，MCP提供了统一的通信标准
2. **可扩展性**：添加新的外部工具只需要实现MCP服务器，不需要修改AI应用本身
3. **安全性**：协议内置了权限控制和审计机制，确保AI只能访问被授权的资源
4. **互操作性**：不同厂商开发的AI应用和MCP服务器可以互相协作

**MCP解决的问题**：

在没有MCP的时代，AI应用与外部系统集成面临巨大挑战：
- 每个工具都需要专门的API集成代码
- 不同的AI模型可能使用不同的集成方式
- 工具调用缺乏标准化，导致维护困难
- 安全性难以保证

MCP的出现彻底改变了这一局面，让AI能够安全、标准地访问外部世界。

### MCP vs 传统API：核心区别

| 对比项 | 传统API调用 | MCP协议 |
|--------|-------------|---------|
| 交互模式 | 请求-响应 | 双向、持续连接 |
| 工具发现 | 需要文档 | 自动发现可用工具 |
| 调用方式 | 硬编码 | 动态调用 |
| 状态管理 | 无状态 | 有状态会话 |
| 标准化程度 | 厂商自定义 | 开放统一标准 |

### 常见错误详解

**错误1：混淆MCP和API**
```python
# ❌ 错误理解
# MCP也是一种HTTP API

# ✅ 正确理解
# MCP是基于JSON-RPC的协议，不等同于传统HTTP API
# MCP更像是一个"连接层"，让AI能够动态发现和调用各种工具
```

**错误2：认为MCP只适用于Claude**
```python
# ❌ 错误理解
# 只有Claude AI才能使用MCP

# ✅ 正确理解
# MCP是一个开放协议，任何AI模型都可以实现
# 已经有多个项目支持MCP，包括OpenAI、OpenRouter等
```

**错误3：低估MCP的安全性**
```python
# ❌ 错误理解
# MCP不安全，不应该用于生产环境

# ✅ 正确理解
# MCP协议内置了安全机制
# - 工具调用需要明确授权
# - 资源访问可以限制范围
# - 可以集成OAuth等认证机制
```

---

## 2. MCP架构解析

### 知识点解析

**三层架构**：MCP采用客户端-服务器架构，包含三个核心角色：

```
┌─────────────────────────────────────────────────────────┐
│                        主机 (Host)                       │
│                   AI应用（如Claude Desktop）            │
├─────────────────────────────────────────────────────────┤
│                    MCP客户端 (Client)                    │
│                  负责与MCP服务器通信                      │
├─────────────────────────────────────────────────────────┤
│                   MCP服务器 (Server)                      │
│              提供工具、资源、提示模板                     │
└─────────────────────────────────────────────────────────┘
```

**主机（Host）**：通常是AI应用程序，负责：
- 管理用户交互
- 协调MCP客户端
- 处理AI模型的请求和响应

**MCP客户端**：作为主机和服务器之间的桥梁，负责：
- 建立与MCP服务器的连接
- 发送请求和接收响应
- 管理会话状态

**MCP服务器**：提供具体的功能扩展，负责：
- 暴露可用的工具（Tools）
- 提供可访问的资源（Resources）
- 定义提示模板（Prompts）

### 通信流程

```
用户请求 ──→ 主机 ──→ MCP客户端 ──→ MCP服务器
                ↑                    │
                │                    ↓
                └────── 响应 ←───────┘
```

**具体流程**：
1. 用户向AI应用发出请求
2. AI应用判断需要使用外部工具
3. MCP客户端向MCP服务器发送工具调用请求
4. MCP服务器执行相应操作
5. 结果返回给MCP客户端
6. 主机将结果整合到AI响应中
7. 最终响应呈现给用户

### 常见错误详解

**错误1：混淆客户端和服务器角色**
```python
# ❌ 错误理解
# 我开发的MCP服务器需要包含客户端代码

# ✅ 正确理解
# MCP服务器只需要实现服务端的职责
# 客户端由AI应用（如Claude Desktop）提供
```

**错误2：一个应用只能连接一个MCP服务器**
```python
# ❌ 错误理解
# 主机只能连接一个MCP服务器

# ✅ 正确理解
# 主机可以同时连接多个MCP服务器
# 每个服务器提供不同的功能扩展
# AI会根据需求选择合适的服务器调用
```

---

## 3. MCP通信机制

### 知识点解析

**JSON-RPC基础**：MCP使用JSON-RPC 2.0作为通信协议。JSON-RPC是一种轻量级的远程过程调用协议，使用JSON格式编码数据。

**消息类型**：

MCP协议定义了三种主要的请求/响应类型：

1. **请求/响应（Request/Response）**：用于工具调用等需要响应的操作
2. **通知（Notification）**：用于不需要响应的消息，如日志
3. **请求批量（Batch）**：用于批量处理多个请求

**核心方法**：

| 方法 | 方向 | 用途 |
|------|------|------|
| `initialize` | 客户端→服务器 | 建立连接，交换能力 |
| `initialized` | 服务器→客户端 | 确认连接建立 |
| `tools/list` | 客户端→服务器 | 获取可用工具列表 |
| `tools/call` | 客户端→服务器 | 调用指定工具 |
| `resources/list` | 客户端→服务器 | 获取可用资源列表 |
| `resources/read` | 客户端→服务器 | 读取资源内容 |
| `prompts/list` | 客户端→服务器 | 获取可用提示模板 |
| `prompts/get` | 客户端→服务器 | 获取提示模板内容 |

### JSON-RPC消息示例

**工具列表请求**：
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/list",
  "params": {}
}
```

**工具列表响应**：
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "tools": [
      {
        "name": "filesystem_read",
        "description": "读取文件内容",
        "inputSchema": {
          "type": "object",
          "properties": {
            "path": {
              "type": "string",
              "description": "要读取的文件路径"
            }
          },
          "required": ["path"]
        }
      }
    ]
  }
}
```

**工具调用请求**：
```json
{
  "jsonrpc": "2.0",
  "id": 2,
  "method": "tools/call",
  "params": {
    "name": "filesystem_read",
    "arguments": {
      "path": "/home/user/doc.txt"
    }
  }
}
```

**工具调用响应**：
```json
{
  "jsonrpc": "2.0",
  "id": 2,
  "result": {
    "content": [
      {
        "type": "text",
        "text": "文件内容..."
      }
    ]
  }
}
```

### 常见错误详解

**错误1：忽略JSON-RPC版本号**
```python
# ❌ 错误示例
{
  "method": "tools/list"
  # 缺少jsonrpc版本号
}

# ✅ 正确示例
{
  "jsonrpc": "2.0",
  "method": "tools/list"
}
```

**错误2：请求ID使用不当**
```python
# ❌ 错误示例
# 同一会话中重复使用相同的ID

# ✅ 正确示例
# 每个请求使用递增的ID
# 响应中的ID必须与请求ID匹配
```

---

## 4. 工具系统（Tools）

### 知识点解析

**概念定义**：工具（Tools）是MCP中最核心的功能，它允许AI模型调用外部函数来执行特定任务。通过工具系统，AI可以突破语言模型的固有局限，执行计算、访问文件系统、调用外部API等操作。

**工具定义结构**：

每个MCP工具都包含以下核心属性：

```json
{
  "name": "tool_name",
  "description": "工具的功能描述",
  "inputSchema": {
    "type": "object",
    "properties": {
      "param1": {
        "type": "string",
        "description": "参数描述"
      }
    },
    "required": ["param1"]
  }
}
```

**工具类型**：MCP工具可以是任何可执行的函数，常见类型包括：

1. **文件系统工具**：读取、写入、删除文件
2. **网络工具**：发送HTTP请求、获取网页内容
3. **数据库工具**：查询、更新数据库
4. **计算工具**：执行复杂计算、数据处理
5. **自定义工具**：根据业务需求定制

### 工具调用流程

```
AI决定需要工具 ──→ 查询可用工具 ──→ 选择工具 ──→ 执行调用
                                                        │
                                                        ↓
                                              返回结果给AI ──→ 生成最终响应
```

### 最佳实践

**1. 工具命名要清晰**
```python
# ❌ 差的工具名
def do_something(x, y):
    pass

# ✅ 好的工具名
def calculate_average(numbers):
    """计算一组数字的平均值"""
    pass
```

**2. 工具描述要详细**
```python
# ❌ 简单描述
def send_email(to, subject, body):
    """发送邮件"""

# ✅ 详细描述
def send_email(to, subject, body):
    """
    发送电子邮件
    
    参数:
        to (str): 收件人邮箱地址
        subject (str): 邮件主题
        body (str): 邮件正文内容
    
    返回:
        dict: 包含发送状态的字典
    
    示例:
        >>> send_email("user@example.com", "Hello", "Hi there!")
        {"status": "success", "message_id": "abc123"}
    """
```

**3. 参数要类型明确**
```python
# ❌ 模糊的参数类型
def process(data):
    pass

# ✅ 明确的参数类型和约束
def process_user_data(user_id: int, options: dict = None):
    """
    处理用户数据
    
    参数:
        user_id: 用户ID，必须为正整数
        options: 可选配置字典
    """
```

### 自测题

1. MCP工具的核心属性有哪些？
2. 工具的inputSchema主要用于什么目的？
3. 如何设计一个好的工具描述？

---

## 5. 资源系统（Resources）

### 知识点解析

**概念定义**：资源（Resources）是MCP中用于让AI访问外部数据的一种机制。与工具不同，资源更像是"只读"的数据源，AI可以通过资源获取信息，但不会执行任何操作。

**资源与工具的区别**：

| 特性 | 工具 (Tools) | 资源 (Resources) |
|------|-------------|------------------|
| 操作类型 | 执行操作 | 获取数据 |
| 副作用 | 可以有 | 无 |
| 调用方式 | AI主动调用 | AI主动请求 |
| 数据流向 | 双向 | 单向（只读） |
| 典型用途 | 执行计算、修改数据 | 查看文件、查询状态 |

**资源URI**：每个资源都有一个唯一的URI，格式如下：

```
scheme://host/path
```

例如：
- `file:///home/user/documents/report.txt`
- `database:///users/active`
- `config://app/settings`

### 资源注册与访问

**资源列表**：
```json
{
  "resources": [
    {
      "uri": "file:///config/app.json",
      "name": "app_config",
      "description": "应用程序配置文件",
      "mimeType": "application/json"
    }
  ]
}
```

**资源读取**：
```json
{
  "method": "resources/read",
  "params": {
    "uri": "file:///config/app.json"
  }
}
```

### 常见使用场景

1. **配置文件访问**：让AI读取应用配置
2. **文档检索**：让AI搜索和读取文档
3. **数据库查询**：让AI查询数据库状态
4. **API文档**：让AI访问API文档
5. **日志分析**：让AI读取系统日志

---

## 6. 提示模板（Prompts）

### 知识点解析

**概念定义**：提示模板（Prompts）是MCP中用于标准化AI交互模式的机制。它允许开发者预定义常用的提示模式，AI可以根据需要调用这些模板，确保交互的一致性。

**提示模板的价值**：

1. **标准化**：确保相同场景下AI行为一致
2. **复用性**：避免重复编写相似的提示词
3. **可维护性**：集中管理提示词，便于更新
4. **参数化**：支持动态参数，灵活适应不同场景

### 提示模板结构

```json
{
  "name": "code_review",
  "description": "请求代码审查",
  "arguments": {
    "type": "object",
    "properties": {
      "language": {
        "type": "string",
        "description": "编程语言"
      },
      "code": {
        "type": "string",
        "description": "要审查的代码"
      }
    },
    "required": ["code"]
  }
}
```

**模板内容示例**：
```
请审查以下{{language}}代码：

{{code}}

请指出：
1. 代码风格问题
2. 潜在的性能问题
3. 可能的安全风险
4. 改进建议
```

### 常见使用场景

1. **代码审查**：标准化代码审查流程
2. **文档生成**：生成特定格式的文档
3. **数据分析**：标准化数据分析报告
4. **测试生成**：生成单元测试用例

---

## 7. MCP生态系统

### 知识点解析

**发展现状**：MCP协议推出后，迅速获得了业界的广泛支持。主要进展包括：

1. **官方服务器**：Anthropic官方提供了多个MCP服务器实现
2. **社区贡献**：开源社区贡献了大量MCP服务器
3. **集成支持**：多个AI应用开始支持MCP协议
4. **工具链完善**：开发工具、测试工具逐渐完善

**官方MCP服务器**：

| 服务器 | 功能 |
|--------|------|
| filesystem | 文件系统操作 |
| postgres | PostgreSQL数据库 |
| sqlite | SQLite数据库 |
| github | GitHub API集成 |
| slack | Slack消息发送 |

**社区MCP服务器**：

| 服务器 | 功能 |
|--------|------|
| Puppeteer | 浏览器自动化 |
| Git | Git操作 |
| AWS | AWS服务集成 |
| Azure | Azure云服务 |

### MCP的优势与挑战

**优势**：
1. 开放标准，社区驱动
2. 简单易用，实现成本低
3. 安全机制完善
4. 生态发展迅速

**挑战**：
1. 协议相对较新
2. 某些场景下的性能优化
3. 多语言SDK的完善程度
4. 企业级功能的成熟度

### 未来发展趋势

1. **更丰富的工具生态**：更多官方和社区工具
2. **更好的性能**：优化通信效率
3. **企业级特性**：加强安全和审计功能
4. **标准化扩展**：更多协议扩展
5. **跨平台支持**：更好的移动端支持

---

## 实战案例

### 案例1：MCP架构示意图

```python
"""
MCP架构示意图
展示主机、客户端、服务器的关系
"""

# MCP架构中的角色
MCP_ROLES = {
    "Host": {
        "description": "AI应用程序（如Claude Desktop）",
        "responsibilities": [
            "管理用户交互",
            "协调MCP客户端",
            "处理AI模型请求"
        ]
    },
    "Client": {
        "description": "MCP客户端组件",
        "responsibilities": [
            "与服务器建立连接",
            "发送请求和接收响应",
            "管理会话状态"
        ]
    },
    "Server": {
        "description": "MCP服务器",
        "responsibilities": [
            "提供工具(tools)",
            "提供资源(resources)",
            "提供提示模板(prompts)"
        ]
    }
}

# 打印架构信息
for role, info in MCP_ROLES.items():
    print(f"\n{role}:")
    print(f"  描述: {info['description']}")
    print(f"  职责:")
    for resp in info['responsibilities']:
        print(f"    - {resp}")
```

### 案例2：MCP工具定义示例

```python
"""
MCP工具定义示例
展示如何定义一个MCP工具
"""

# MCP工具定义
def define_mcp_tool():
    """定义一个简单的MCP工具"""
    
    tool = {
        "name": "calculate_bmi",
        "description": "根据身高体重计算BMI指数",
        "inputSchema": {
            "type": "object",
            "properties": {
                "height_cm": {
                    "type": "number",
                    "description": "身高（厘米）",
                    "minimum": 50,
                    "maximum": 300
                },
                "weight_kg": {
                    "type": "number",
                    "description": "体重（公斤）",
                    "minimum": 10,
                    "maximum": 500
                }
            },
            "required": ["height_cm", "weight_kg"]
        }
    }
    
    return tool


def execute_bmi_calculation(height_cm: float, weight_kg: float) -> dict:
    """
    执行BMI计算
    
    参数:
        height_cm: 身高（厘米）
        weight_kg: 体重（公斤）
    
    返回:
        dict: 包含BMI值和健康建议
    """
    # BMI公式：体重(kg) / 身高(m)的平方
    height_m = height_cm / 100
    bmi = weight_kg / (height_m ** 2)
    
    # 根据BMI值返回健康建议
    if bmi < 18.5:
        status = "偏瘦"
        suggestion = "建议适当增加营养摄入"
    elif bmi < 24:
        status = "正常"
        suggestion = "继续保持健康生活方式"
    elif bmi < 28:
        status = "偏胖"
        suggestion = "建议适当增加运动量"
    else:
        status = "肥胖"
        suggestion = "建议咨询医生制定健康计划"
    
    return {
        "bmi": round(bmi, 2),
        "status": status,
        "suggestion": suggestion
    }


# 测试工具
tool = define_mcp_tool()
result = execute_bmi_calculation(175, 70)

print(f"工具定义: {tool['name']}")
print(f"BMI计算结果: {result}")
```

### 案例3：JSON-RPC消息构建

```python
"""
JSON-RPC消息构建示例
展示MCP协议的消息格式
"""

import json
from typing import Any


def create_jsonrpc_request(method: str, params: dict = None, req_id: int = 1) -> dict:
    """
    创建JSON-RPC请求消息
    
    参数:
        method: 方法名
        params: 请求参数
        req_id: 请求ID
    
    返回:
        dict: JSON-RPC请求消息
    """
    request = {
        "jsonrpc": "2.0",
        "id": req_id,
        "method": method
    }
    
    if params:
        request["params"] = params
    
    return request


def create_jsonrpc_response(result: Any, req_id: int = 1) -> dict:
    """
    创建JSON-RPC响应消息
    
    参数:
        result: 处理结果
        req_id: 请求ID
    
    返回:
        dict: JSON-RPC响应消息
    """
    return {
        "jsonrpc": "2.0",
        "id": req_id,
        "result": result
    }


def create_jsonrpc_error(code: int, message: str, req_id: int = 1) -> dict:
    """
    创建JSON-RPC错误响应
    
    参数:
        code: 错误代码
        message: 错误消息
        req_id: 请求ID
    
    返回:
        dict: JSON-RPC错误响应
    """
    return {
        "jsonrpc": "2.0",
        "id": req_id,
        "error": {
            "code": code,
            "message": message
        }
    }


# 测试消息构建

# 1. 工具列表请求
list_tools_request = create_jsonrpc_request("tools/list")
print("工具列表请求:")
print(json.dumps(list_tools_request, indent=2, ensure_ascii=False))

# 2. 工具调用请求
tool_call_request = create_jsonrpc_request(
    "tools/call",
    params={
        "name": "calculate_bmi",
        "arguments": {
            "height_cm": 175,
            "weight_kg": 70
        }
    },
    req_id=2
)
print("\n工具调用请求:")
print(json.dumps(tool_call_request, indent=2, ensure_ascii=False))

# 3. 响应示例
tool_call_response = create_jsonrpc_response(
    result={
        "content": [
            {
                "type": "text",
                "text": "BMI: 22.86, 正常"
            }
        ]
    },
    req_id=2
)
print("\n工具调用响应:")
print(json.dumps(tool_call_response, indent=2, ensure_ascii=False))

# 4. 错误响应示例
error_response = create_jsonrpc_error(
    code=-32601,
    message="Method not found",
    req_id=3
)
print("\n错误响应:")
print(json.dumps(error_response, indent=2, ensure_ascii=False))
```

### 代码说明

**案例1代码解释**：
1. 定义了MCP架构中的三个核心角色
2. 每个角色有不同的职责描述
3. 帮助理解MCP的整体架构

**案例2代码解释**：
1. 定义了BMI计算工具的结构
2. 实现了工具的执行逻辑
3. 包含输入验证和结果解释

**案例3代码解释**：
1. 展示了JSON-RPC消息的构建方法
2. 包含请求、响应、错误三种消息类型
3. 符合MCP协议的规范要求

---

## 本章小结

本章我们学习了MCP（Model Context Protocol）协议的核心概念：

1. **MCP简介**：理解了什么MCP，它解决了什么问题，为什么被称为AI的"USB接口"
2. **架构解析**：掌握了主机、客户端、服务器的三层架构
3. **通信机制**：理解了JSON-RPC协议和MCP的核心方法
4. **工具系统**：学会了如何定义和使用MCP工具
5. **资源系统**：理解了资源与工具的区别和应用场景
6. **提示模板**：掌握了提示模板的使用方式
7. **生态发展**：了解了MCP的现状和未来趋势

MCP作为新兴的AI交互协议，正在快速发展。掌握这些核心概念，将帮助你在AI应用开发中更好地利用MCP的能力。
