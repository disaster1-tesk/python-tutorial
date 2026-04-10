"""
Python 教程 Web 平台 - 模块配置
包含24个知识模块的定义
"""

# ==================== 模块定义 ====================

MODULES = [
    # 基础阶段
    {"id": "base_syntax", "name": "Python基础语法", "icon": "📖", "category": "基础阶段", "order": 1},
    {"id": "data_types", "name": "数据类型", "icon": "🔢", "category": "基础阶段", "order": 2},
    {"id": "control_flow", "name": "控制流", "icon": "🔀", "category": "基础阶段", "order": 3},
    {"id": "functions", "name": "函数", "icon": "⚡", "category": "基础阶段", "order": 4},
    {"id": "classes_objects", "name": "类和对象", "icon": "🎯", "category": "基础阶段", "order": 5},
    {"id": "exception_handling", "name": "异常处理", "icon": "⚠️", "category": "基础阶段", "order": 6},
    {"id": "file_operations", "name": "文件操作", "icon": "📁", "category": "基础阶段", "order": 7},
    {"id": "modules_packages", "name": "模块和包", "icon": "📦", "category": "基础阶段", "order": 8},
    
    # 进阶阶段
    {"id": "advanced_features", "name": "高级特性", "icon": "🚀", "category": "进阶阶段", "order": 9},
    {"id": "type_hints", "name": "类型提示", "icon": "🔍", "category": "进阶阶段", "order": 10},
    {"id": "concurrency", "name": "并发编程", "icon": "🧵", "category": "进阶阶段", "order": 11},
    {"id": "standard_library", "name": "标准库", "icon": "📚", "category": "进阶阶段", "order": 12},
    {"id": "third_party_libraries", "name": "第三方库", "icon": "🔧", "category": "进阶阶段", "order": 13},
    
    # 应用阶段
    {"id": "database", "name": "数据库操作", "icon": "🗄️", "category": "应用阶段", "order": 14},
    {"id": "design_patterns", "name": "设计模式", "icon": "🏗️", "category": "应用阶段", "order": 15},
    {"id": "networking", "name": "网络编程", "icon": "🌐", "category": "应用阶段", "order": 16},
    {"id": "data_processing", "name": "数据处理", "icon": "📊", "category": "应用阶段", "order": 17},
    {"id": "web_development", "name": "Web开发", "icon": "🌍", "category": "应用阶段", "order": 18},
    
    # AI/ML
    {"id": "ai_ml_basics", "name": "AI/ML基础", "icon": "🤖", "category": "AI/机器学习", "order": 19},
    {"id": "deep_learning", "name": "深度学习", "icon": "🧠", "category": "AI/机器学习", "order": 20},
    {"id": "nlp_and_llm", "name": "NLP与大模型", "icon": "💬", "category": "AI/机器学习", "order": 21},
    {"id": "cv_computer_vision", "name": "计算机视觉", "icon": "👁️", "category": "AI/机器学习", "order": 22},
    
    # 工程化
    {"id": "unit_testing", "name": "单元测试", "icon": "🧪", "category": "工程化", "order": 23},
    {"id": "debugging", "name": "调试与优化", "icon": "🔧", "category": "工程化", "order": 24},
    
    # AI应用开发
    {"id": "langchain_framework", "name": "LangChain框架", "icon": "⛓️", "category": "AI应用开发", "order": 25},
    {"id": "vector_databases", "name": "向量数据库", "icon": "🔐", "category": "AI应用开发", "order": 26},
    {"id": "prompt_engineering", "name": "提示工程", "icon": "📝", "category": "AI应用开发", "order": 27},
    {"id": "ai_agent", "name": "AI Agent", "icon": "🤖", "category": "AI应用开发", "order": 28},
    {"id": "rag_architecture", "name": "RAG架构", "icon": "📚", "category": "AI应用开发", "order": 29},
    {"id": "model_finetuning", "name": "模型微调", "icon": "🎛️", "category": "AI应用开发", "order": 30},
    {"id": "multimodal_ai", "name": "多模态AI", "icon": "🎨", "category": "AI应用开发", "order": 31},
    
    # MCP/Skills
    {"id": "mcp_protocol", "name": "MCP协议", "icon": "🔗", "category": "MCP/Skills", "order": 32},
    {"id": "mcp_server", "name": "MCP Server", "icon": "🖥️", "category": "MCP/Skills", "order": 33},
    {"id": "custom_skill", "name": "自定义Skill", "icon": "🛠️", "category": "MCP/Skills", "order": 34},
    {"id": "enterprise_mcp", "name": "企业级MCP", "icon": "🏢", "category": "MCP/Skills", "order": 35},
    {"id": "mcp_security", "name": "MCP安全认证", "icon": "🔒", "category": "MCP/Skills", "order": 36},
    {"id": "multi_agent", "name": "多Agent协作", "icon": "👥", "category": "MCP/Skills", "order": 37},
]

# 模块分类
MODULE_CATEGORIES = [
    "基础阶段",
    "进阶阶段",
    "应用阶段", 
    "AI/机器学习",
    "工程化",
    "AI应用开发",
    "MCP/Skills",
]

# 学习路径依赖（模块ID -> 依赖模块ID列表）
MODULE_DEPENDENCIES = {
    "base_syntax": [],
    "data_types": ["base_syntax"],
    "control_flow": ["base_syntax", "data_types"],
    "functions": ["base_syntax", "data_types", "control_flow"],
    "classes_objects": ["base_syntax", "data_types", "control_flow", "functions"],
    "exception_handling": ["base_syntax", "control_flow"],
    "file_operations": ["base_syntax", "exception_handling"],
    "modules_packages": ["base_syntax"],
    "advanced_features": ["classes_objects"],
    "type_hints": ["functions"],
    "concurrency": ["functions", "exception_handling"],
    "standard_library": ["base_syntax"],
    "third_party_libraries": ["standard_library"],
    "database": ["exception_handling", "file_operations"],
    "design_patterns": ["classes_objects", "advanced_features"],
    "networking": ["exception_handling"],
    "data_processing": ["standard_library", "third_party_libraries"],
    "web_development": ["networking", "third_party_libraries"],
    "ai_ml_basics": ["data_processing", "statistics"],
    "deep_learning": ["ai_ml_basics"],
    "nlp_and_llm": ["ai_ml_basics", "deep_learning"],
    "cv_computer_vision": ["ai_ml_basics", "deep_learning"],
    "unit_testing": ["exception_handling", "functions"],
    "debugging": ["unit_testing"],
    
    # AI应用开发
    "langchain_framework": ["nlp_and_llm", "ai_ml_basics"],
    "vector_databases": ["ai_ml_basics"],
    "prompt_engineering": ["nlp_and_llm"],
    "ai_agent": ["langchain_framework"],
    "rag_architecture": ["nlp_and_llm", "vector_databases"],
    "model_finetuning": ["ai_ml_basics", "deep_learning"],
    "multimodal_ai": ["nlp_and_llm", "cv_computer_vision"],
}

# 应用信息
APP_NAME = "Python 教程学习平台"
APP_ICON = "🐍"
APP_VERSION = "3.0.0"
APP_PORT = 8502


def get_module_info(module_id: str) -> dict:
    """获取模块信息"""
    for m in MODULES:
        if m['id'] == module_id:
            return m
    return None


def get_category_modules(category: str) -> list:
    """获取分类下的模块"""
    return [m for m in MODULES if m['category'] == category]


def get_module_dependencies(module_id: str) -> list:
    """获取模块的依赖"""
    return MODULE_DEPENDENCIES.get(module_id, [])


def get_learning_path() -> list:
    """获取推荐学习路径（按顺序）"""
    path = []
    added = set()
    
    for order in range(1, 25):
        for m in MODULES:
            if m['order'] == order and m['id'] not in added:
                path.append(m)
                added.add(m['id'])
                break
    
    return path
