# MCP (Model Context Protocol) 协议示例代码

"""
MCP协议示例代码
展示MCP的核心概念和实现
"""

# ============================================================
# 1. MCP架构示例
# ============================================================

class MCPHost:
    """
    MCP主机类
    负责管理AI应用和MCP客户端
    """
    
    def __init__(self, name: str):
        self.name = name
        self.clients = []
        print(f"🖥️  主机 '{name}' 已启动")
    
    def add_client(self, client):
        """添加MCP客户端"""
        self.clients.append(client)
        print(f"➕ 添加客户端: {client.name}")
    
    def request(self, prompt: str):
        """
        处理用户请求
        
        参数:
            prompt: 用户输入的提示
        """
        print(f"\n📝 用户请求: {prompt}")
        
        # 模拟AI判断需要使用工具
        needs_tool = self._analyze_needs_tool(prompt)
        
        if needs_tool:
            print("🔧 需要使用外部工具...")
            # 协调客户端调用工具
            for client in self.clients:
                result = client.call_tool(needs_tool)
                if result:
                    return f"✅ 处理完成: {result}"
        
        return "📄 常规响应"
    
    def _analyze_needs_tool(self, prompt: str) -> str:
        """分析是否需要使用工具"""
        keywords = ["计算", "文件", "查询", "天气", "搜索"]
        for keyword in keywords:
            if keyword in prompt:
                return keyword
        return None


class MCPClient:
    """
    MCP客户端类
    负责与MCP服务器通信
    """
    
    def __init__(self, name: str):
        self.name = name
        self.servers = []
        print(f"📡 客户端 '{name}' 已初始化")
    
    def connect_server(self, server):
        """连接MCP服务器"""
        self.servers.append(server)
        print(f"🔗 已连接到服务器: {server.name}")
    
    def list_tools(self):
        """列出所有可用工具"""
        tools = []
        for server in self.servers:
            tools.extend(server.list_tools())
        return tools
    
    def call_tool(self, tool_name: str, **kwargs):
        """调用指定工具"""
        for server in self.servers:
            tool = server.get_tool(tool_name)
            if tool:
                return server.execute_tool(tool_name, **kwargs)
        return None


class MCPServer:
    """
    MCP服务器类
    提供工具、资源、提示模板
    """
    
    def __init__(self, name: str):
        self.name = name
        self.tools = {}
        self.resources = {}
        self.prompts = {}
        print(f"🖥️  MCP服务器 '{name}' 已启动")
    
    def register_tool(self, name: str, description: str, handler):
        """注册工具"""
        self.tools[name] = {
            "name": name,
            "description": description,
            "handler": handler
        }
        print(f"🔧 注册工具: {name}")
    
    def list_tools(self):
        """列出所有可用工具"""
        return [
            {
                "name": name,
                "description": info["description"]
            }
            for name, info in self.tools.items()
        ]
    
    def get_tool(self, name: str):
        """获取指定工具"""
        return self.tools.get(name)
    
    def execute_tool(self, name: str, **kwargs):
        """执行工具"""
        tool = self.tools.get(name)
        if tool:
            return tool["handler"](**kwargs)
        return None
    
    def register_resource(self, uri: str, name: str, content: str):
        """注册资源"""
        self.resources[uri] = {
            "name": name,
            "content": content
        }
        print(f"📄 注册资源: {uri}")
    
    def read_resource(self, uri: str):
        """读取资源"""
        resource = self.resources.get(uri)
        if resource:
            return resource["content"]
        return None


# 测试MCP架构
def test_mcp_architecture():
    """测试MCP架构"""
    print("\n" + "=" * 50)
    print("测试1: MCP架构")
    print("=" * 50)
    
    # 创建架构组件
    host = MCPHost("Claude Desktop")
    client = MCPClient("MCP Client")
    server = MCPServer("File System Server")
    
    # 建立连接
    host.add_client(client)
    client.connect_server(server)
    
    # 注册工具
    def read_file_handler(path: str) -> str:
        return f"文件 {path} 的内容..."
    
    server.register_tool("read_file", "读取文件内容", read_file_handler)
    server.register_resource("file:///test.txt", "测试文件", "Hello MCP!")
    
    # 处理请求
    result = host.request("请读取 test.txt 文件")
    print(f"\n结果: {result}")
    
    # 列出工具
    print(f"\n可用工具: {client.list_tools()}")


# ============================================================
# 2. JSON-RPC消息示例
# ============================================================

import json


class JSONRPCMessage:
    """JSON-RPC消息处理类"""
    
    @staticmethod
    def create_request(method: str, params: dict = None, req_id: int = 1) -> dict:
        """创建JSON-RPC请求"""
        request = {
            "jsonrpc": "2.0",
            "id": req_id,
            "method": method
        }
        if params:
            request["params"] = params
        return request
    
    @staticmethod
    def create_response(result: Any, req_id: int = 1) -> dict:
        """创建JSON-RPC响应"""
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": result
        }
    
    @staticmethod
    def create_error(code: int, message: str, req_id: int = 1) -> dict:
        """创建JSON-RPC错误响应"""
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "error": {
                "code": code,
                "message": message
            }
        }
    
    @staticmethod
    def parse_message(message: dict) -> str:
        """解析JSON-RPC消息"""
        if "method" in message:
            return "request"
        elif "error" in message:
            return "error"
        elif "result" in message:
            return "response"
        return "unknown"


# 错误代码常量
JSONRPC_ERRORS = {
    -32700: "Parse error - 解析错误",
    -32600: "Invalid Request - 无效请求",
    -32601: "Method not found - 方法未找到",
    -32602: "Invalid params - 无效参数",
    -32603: "Internal error - 内部错误"
}


def test_jsonrpc_messages():
    """测试JSON-RPC消息"""
    print("\n" + "=" * 50)
    print("测试2: JSON-RPC消息")
    print("=" * 50)
    
    # 创建工具列表请求
    request = JSONRPCMessage.create_request("tools/list")
    print("\n请求消息:")
    print(json.dumps(request, indent=2, ensure_ascii=False))
    
    # 创建工具调用请求
    call_request = JSONRPCMessage.create_request(
        "tools/call",
        params={
            "name": "read_file",
            "arguments": {"path": "/home/user/test.txt"}
        },
        req_id=2
    )
    print("\n工具调用请求:")
    print(json.dumps(call_request, indent=2, ensure_ascii=False))
    
    # 创建成功响应
    response = JSONRPCMessage.create_response(
        {"content": [{"type": "text", "text": "文件内容..."}]},
        req_id=2
    )
    print("\n成功响应:")
    print(json.dumps(response, indent=2, ensure_ascii=False))
    
    # 创建错误响应
    error = JSONRPCMessage.create_error(
        -32601,
        "Method not found",
        req_id=3
    )
    print("\n错误响应:")
    print(json.dumps(error, indent=2, ensure_ascii=False))


# ============================================================
# 3. MCP工具定义示例
# ============================================================

from typing import Any


class ToolDefinition:
    """MCP工具定义类"""
    
    def __init__(self, name: str, description: str, input_schema: dict):
        self.name = name
        self.description = description
        self.input_schema = input_schema
    
    def to_dict(self) -> dict:
        """转换为MCP工具格式"""
        return {
            "name": self.name,
            "description": self.description,
            "inputSchema": self.input_schema
        }
    
    @staticmethod
    def from_dict(data: dict) -> 'ToolDefinition':
        """从字典创建工具定义"""
        return ToolDefinition(
            name=data["name"],
            description=data["description"],
            input_schema=data["inputSchema"]
        )
    
    def validate_params(self, params: dict) -> tuple[bool, str]:
        """验证参数"""
        required = self.input_schema.get("required", [])
        for param in required:
            if param not in params:
                return False, f"缺少必需参数: {param}"
        
        properties = self.input_schema.get("properties", {})
        for key, value in params.items():
            if key in properties:
                expected_type = properties[key].get("type")
                if not self._check_type(value, expected_type):
                    return False, f"参数 {key} 类型错误，需要 {expected_type}"
        
        return True, "参数有效"
    
    def _check_type(self, value: Any, expected_type: str) -> bool:
        """检查类型"""
        type_map = {
            "string": str,
            "number": (int, float),
            "integer": int,
            "boolean": bool,
            "object": dict,
            "array": list
        }
        expected = type_map.get(expected_type)
        if expected:
            return isinstance(value, expected)
        return True


class ToolRegistry:
    """MCP工具注册表"""
    
    def __init__(self):
        self.tools: dict[str, ToolDefinition] = {}
        self.handlers: dict[str, callable] = {}
    
    def register(self, tool_def: ToolDefinition, handler: callable):
        """注册工具"""
        self.tools[tool_def.name] = tool_def
        self.handlers[tool_def.name] = handler
        print(f"✅ 注册工具: {tool_def.name}")
    
    def get_tool(self, name: str) -> ToolDefinition | None:
        """获取工具定义"""
        return self.tools.get(name)
    
    def call(self, name: str, params: dict) -> Any:
        """调用工具"""
        tool = self.tools.get(name)
        if not tool:
            raise ValueError(f"工具不存在: {name}")
        
        # 验证参数
        valid, message = tool.validate_params(params)
        if not valid:
            raise ValueError(message)
        
        # 执行处理函数
        handler = self.handlers.get(name)
        if handler:
            return handler(**params)
        
        return None
    
    def list_tools(self) -> list[dict]:
        """列出所有工具"""
        return [tool.to_dict() for tool in self.tools.values()]


def test_tool_system():
    """测试工具系统"""
    print("\n" + "=" * 50)
    print("测试3: MCP工具系统")
    print("=" * 50)
    
    # 创建工具注册表
    registry = ToolRegistry()
    
    # 定义工具
    bmi_tool = ToolDefinition(
        name="calculate_bmi",
        description="根据身高体重计算BMI指数",
        input_schema={
            "type": "object",
            "properties": {
                "height_cm": {
                    "type": "number",
                    "description": "身高（厘米）"
                },
                "weight_kg": {
                    "type": "number",
                    "description": "体重（公斤）"
                }
            },
            "required": ["height_cm", "weight_kg"]
        }
    )
    
    # 定义处理函数
    def calculate_bmi_handler(height_cm: float, weight_kg: float) -> dict:
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
        
        return {"bmi": round(bmi, 2), "status": status}
    
    # 注册工具
    registry.register(bmi_tool, calculate_bmi_handler)
    
    # 调用工具
    result = registry.call("calculate_bmi", {"height_cm": 175, "weight_kg": 70})
    print(f"\nBMI计算结果: {result}")
    
    # 列出工具
    print(f"\n已注册工具: {registry.list_tools()}")


# ============================================================
# 4. MCP资源系统示例
# ============================================================

class Resource:
    """MCP资源类"""
    
    def __init__(self, uri: str, name: str, content: str, mime_type: str = "text/plain"):
        self.uri = uri
        self.name = name
        self.content = content
        self.mime_type = mime_type
    
    def to_dict(self) -> dict:
        """转换为MCP资源格式"""
        return {
            "uri": self.uri,
            "name": self.name,
            "mimeType": self.mime_type
        }


class ResourceManager:
    """MCP资源管理器"""
    
    def __init__(self):
        self.resources: dict[str, Resource] = {}
    
    def register(self, resource: Resource):
        """注册资源"""
        self.resources[resource.uri] = resource
        print(f"✅ 注册资源: {resource.uri}")
    
    def list(self) -> list[dict]:
        """列出所有资源"""
        return [r.to_dict() for r in self.resources.values()]
    
    def read(self, uri: str) -> str | None:
        """读取资源内容"""
        resource = self.resources.get(uri)
        if resource:
            return resource.content
        return None


def test_resource_system():
    """测试资源系统"""
    print("\n" + "=" * 50)
    print("测试4: MCP资源系统")
    print("=" * 50)
    
    # 创建资源管理器
    manager = ResourceManager()
    
    # 注册资源
    config_resource = Resource(
        uri="config://app/settings",
        name="应用配置",
        content='{"theme": "dark", "language": "zh-CN"}',
        mime_type="application/json"
    )
    manager.register(config_resource)
    
    doc_resource = Resource(
        uri="file:///docs/readme.txt",
        name="README文档",
        content="这是MCP协议学习教程"
    )
    manager.register(doc_resource)
    
    # 列出资源
    print(f"\n可用资源: {manager.list()}")
    
    # 读取资源
    content = manager.read("config://app/settings")
    print(f"\n读取配置: {content}")


# ============================================================
# 5. MCP提示模板示例
# ============================================================

class PromptTemplate:
    """MCP提示模板类"""
    
    def __init__(self, name: str, description: str, template: str, arguments: dict = None):
        self.name = name
        self.description = description
        self.template = template
        self.arguments = arguments or {}
    
    def render(self, **kwargs) -> str:
        """渲染提示模板"""
        return self.template.format(**kwargs)
    
    def to_dict(self) -> dict:
        """转换为MCP提示模板格式"""
        result = {
            "name": self.name,
            "description": self.description
        }
        if self.arguments:
            result["arguments"] = self.arguments
        return result


class PromptManager:
    """MCP提示模板管理器"""
    
    def __init__(self):
        self.prompts: dict[str, PromptTemplate] = {}
    
    def register(self, prompt: PromptTemplate):
        """注册提示模板"""
        self.prompts[prompt.name] = prompt
        print(f"✅ 注册提示模板: {prompt.name}")
    
    def list(self) -> list[dict]:
        """列出所有提示模板"""
        return [p.to_dict() for p in self.prompts.values()]
    
    def get(self, name: str, **kwargs) -> str | None:
        """获取渲染后的提示"""
        prompt = self.prompts.get(name)
        if prompt:
            return prompt.render(**kwargs)
        return None


def test_prompt_system():
    """测试提示模板系统"""
    print("\n" + "=" * 50)
    print("测试5: MCP提示模板系统")
    print("=" * 50)
    
    # 创建提示管理器
    manager = PromptManager()
    
    # 注册代码审查模板
    code_review = PromptTemplate(
        name="code_review",
        description="请求代码审查",
        template="""
请审查以下{{language}}代码：

```{{language}}
{{code}}
```

请指出：
1. 代码风格问题
2. 潜在的性能问题
3. 可能的安全风险
4. 改进建议
        """,
        arguments={
            "language": {"type": "string", "description": "编程语言"},
            "code": {"type": "string", "description": "要审查的代码"}
        }
    )
    manager.register(code_review)
    
    # 注册文档生成模板
    doc_gen = PromptTemplate(
        name="generate_doc",
        description="生成API文档",
        template="""
请为以下API生成文档：

端点: {{endpoint}}
方法: {{method}}
描述: {{description}}

请包含：
1. 功能说明
2. 参数说明
3. 返回值说明
4. 示例
        """
    )
    manager.register(doc_gen)
    
    # 列出提示模板
    print(f"\n可用提示模板: {manager.list()}")
    
    # 渲染提示
    rendered = manager.get(
        "code_review",
        language="Python",
        code="def hello(): print('Hello World')"
    )
    print(f"\n渲染后的提示:\n{rendered}")


# ============================================================
# 6. 完整MCP会话示例
# ============================================================

class MCPSession:
    """完整的MCP会话模拟"""
    
    def __init__(self):
        self.client = MCPClient("MainClient")
        self.server = MCPServer("DemoServer")
        self.client.connect_server(self.server)
        
        # 注册演示工具
        self._register_demo_tools()
        
        # 注册演示资源
        self._register_demo_resources()
        
        # 注册演示提示
        self._register_demo_prompts()
    
    def _register_demo_tools(self):
        """注册演示工具"""
        
        def calculator(expression: str) -> str:
            """计算器工具"""
            try:
                result = eval(expression)
                return str(result)
            except Exception as e:
                return f"错误: {str(e)}"
        
        self.server.register_tool("calculator", "简单计算器", calculator)
    
    def _register_demo_resources(self):
        """注册演示资源"""
        self.server.register_resource(
            "config://demo/settings",
            "演示配置",
            '{"version": "1.0", "debug": true}'
        )
    
    def _register_demo_prompts(self):
        """注册演示提示"""
        pass  # 提示模板需要单独的管理器
    
    def initialize(self) -> dict:
        """初始化会话"""
        print("\n🔄 MCP会话初始化...")
        
        # 发送初始化请求
        request = JSONRPCMessage.create_request(
            "initialize",
            params={
                "protocolVersion": "2024-11-05",
                "capabilities": {
                    "tools": {},
                    "resources": {},
                    "prompts": {}
                },
                "clientInfo": {
                    "name": "demo-client",
                    "version": "1.0.0"
                }
            }
        )
        
        # 模拟响应
        response = {
            "protocolVersion": "2024-11-05",
            "capabilities": {
                "tools": {},
                "resources": {},
                "prompts": {}
            },
            "serverInfo": {
                "name": "demo-server",
                "version": "1.0.0"
            }
        }
        
        print("✅ 初始化完成")
        return response
    
    def list_tools(self) -> list[dict]:
        """列出工具"""
        request = JSONRPCMessage.create_request("tools/list")
        return self.server.list_tools()
    
    def call_tool(self, name: str, arguments: dict) -> Any:
        """调用工具"""
        request = JSONRPCMessage.create_request(
            "tools/call",
            params={"name": name, "arguments": arguments},
            req_id=2
        )
        
        result = self.server.execute_tool(name, **arguments)
        
        response = JSONRPCMessage.create_response(
            {"content": [{"type": "text", "text": str(result)}]},
            req_id=2
        )
        
        return response


def test_full_session():
    """测试完整MCP会话"""
    print("\n" + "=" * 50)
    print("测试6: 完整MCP会话")
    print("=" * 50)
    
    # 创建会话
    session = MCPSession()
    
    # 初始化
    init_result = session.initialize()
    print(f"初始化结果: {init_result['serverInfo']}")
    
    # 列出工具
    tools = session.list_tools()
    print(f"\n可用工具: {tools}")
    
    # 调用工具
    result = session.call_tool("calculator", {"expression": "2 + 3 * 4"})
    print(f"\n计算结果: {result}")


# ============================================================
# 主函数
# ============================================================

if __name__ == "__main__":
    from typing import Any
    
    print("=" * 60)
    print("MCP (Model Context Protocol) 协议示例")
    print("=" * 60)
    
    # 运行所有测试
    test_mcp_architecture()
    test_jsonrpc_messages()
    test_tool_system()
    test_resource_system()
    test_prompt_system()
    test_full_session()
    
    print("\n" + "=" * 60)
    print("所有测试完成!")
    print("=" * 60)
