# 自定义 Skill 开发

---

## 学习目标

完成本章节学习后，你将能够：

| 目标 | 描述 | 重要性 |
|------|------|--------|
| 理解Skill概念 | 掌握Skill的定义和在AI系统中的作用 | ⭐⭐⭐ 必备 |
| 掌握Skill结构 | 理解Skill的组成文件和结构规范 | ⭐⭐⭐ 必备 |
| 开发基础Skill | 能够创建和配置一个简单的自定义Skill | ⭐⭐⭐ 必备 |
| 实现Skill能力 | 学会定义Skill的tools、workflows等 | ⭐⭐⭐ 必备 |
| 测试与调试 | 掌握Skill的测试和调试技巧 | ⭐⭐ 重要 |
| 发布与分享 | 学会将Skill打包和分享 | ⭐⭐ 重要 |

---

## 预习检查

在开始学习之前，请尝试回答以下问题：

1. 什么是Skill？它与传统的插件有什么区别？
2. Skill的主要组成结构是什么？
3. 如何创建一个自定义Skill？
4. Skill如何与AI系统进行交互？

如果你对以上问题还有疑惑，不用担心，通过本章节的学习，你会找到答案！

---

## 章节概览

```
┌─────────────────────────────────────────────────────────┐
│                 自定义 Skill 开发                           │
├─────────────────────────────────────────────────────────┤
│  1. Skill简介    │ AI能力的可扩展单元                      │
│  2. 结构规范      │ Skill的文件结构和配置                   │
│  3. 基础开发      │ 从零创建第一个Skill                      │
│  4. 能力定义      │ 定义Tools、Workflows等                  │
│  5. 工作流        │ 创建自动化工作流                          │
│  6. 测试调试      │ Skill的测试和调试                        │
│  7. 发布分享      │ Skill的打包和发布                        │
└─────────────────────────────────────────────────────────┘
```

---

## 1. Skill简介

### 知识点解析

**概念定义**：Skill（技能）是一种扩展AI系统能力的标准化方式。它将特定领域的功能封装为可重用的单元，让AI能够调用这些能力来完成任务。与传统的API或插件相比，Skill更强调"能力"而非"接口"，是一种更高层次的抽象。

**Skill的价值**：

1. **模块化**：将复杂功能封装为独立单元
2. **可复用**：一次开发，多处使用
3. **可组合**：多个Skill可以协同工作
4. **可扩展**：方便添加新能力

**Skill vs MCP**：

| 特性 | Skill | MCP |
|------|-------|-----|
| 抽象层次 | 能力单元 | 协议标准 |
| 使用场景 | AI能力扩展 | AI与外部系统交互 |
| 实现方式 | 定义能力清单 | 实现服务器接口 |
| 灵活性 | 高 | 高 |
| 复杂度 | 中等 | 较高 |

**Skill的典型应用**：

1. **文档处理**：PDF解析、Word文档编辑、PPT制作
2. **数据分析**：Excel处理、数据可视化、报表生成
3. **媒体生成**：图片生成、视频编辑、音频处理
4. **网络操作**：网页抓取、API调用、浏览器自动化

---

## 2. Skill结构规范

### 知识点解析

**目录结构**：

一个标准的Skill通常包含以下文件：

```
my_skill/
├── SKILL.md              # Skill配置文件（必需）
├── README.md             # 使用说明（可选）
├── requirements.txt      # 依赖列表（可选）
├── tools/               # 工具脚本目录
│   ├── __init__.py
│   ├── tool1.py
│   └── tool2.py
├── workflows/           # 工作流目录
│   └── workflow1.py
└── assets/              # 资源文件
    └── icon.png
```

### SKILL.md 结构

**必需字段**：

```yaml
---
name: my_skill           # Skill名称（英文唯一标识）
title: 我的技能           # 显示标题（中文）
description: 技能描述      # 简短描述
version: 1.0.0           # 版本号
author: 作者名            # 作者
location: manager       # 位置（manager/plugin）
trigger: 触发关键词      # 触发条件
---
```

**能力定义**：

```yaml
capabilities:
  tools:
    - name: tool_name
      description: 工具描述
      script: tools/tool.py
      function: handle_tool
      
  workflows:
    - name: workflow_name
      description: 工作流描述
      script: workflows/workflow.py
```

### 示例配置

```yaml
---
name: document_processor
title: 文档处理
description: 处理PDF、Word、PPT等文档
version: 1.0.0
author: MCP Team
location: plugin
trigger: 文档|处理|转换
---

# 能力定义
capabilities:
  tools:
    - name: pdf_to_text
      description: 将PDF转换为文本
      script: tools/pdf_processor.py
      function: extract_text
      
    - name: word_editor
      description: 编辑Word文档
      script: tools/word_editor.py
      function: edit_document
      
    - name: ppt_generator
      description: 生成PPT演示文稿
      script: tools/ppt_generator.py
      function: create_presentation
      
  workflows:
    - name: document_pipeline
      description: 文档处理流水线
      script: workflows/pipeline.py
```

---

## 3. 基础Skill开发

### 知识点解析

**开发流程**：

1. 创建Skill目录结构
2. 编写SKILL.md配置文件
3. 实现工具脚本
4. 添加依赖说明
5. 测试和调试

### 第一步：创建目录结构

```bash
# 创建Skill目录
mkdir -p my_skill/{tools,workflows,assets}

# 创建必需文件
touch my_skill/SKILL.md
touch my_skill/README.md
touch my_skill/requirements.txt
touch my_skill/tools/__init__.py
```

### 第二步：编写SKILL.md

```yaml
---
name: hello_skill
title: 打招呼技能
description: 一个简单的打招呼Skill示例
version: 1.0.0
author: YourName
location: plugin
trigger: 打招呼|hello|问候
---

capabilities:
  tools:
    - name: greet
      description: 向用户打招呼
      script: tools/greet.py
      function: greet_user
      
    - name: farewell
      description: 说再见
      script: tools/greet.py
      function: say_goodbye
```

### 第三步：实现工具脚本

```python
# tools/greet.py

def greet_user(name: str = "朋友") -> str:
    """
    向用户打招呼
    
    参数:
        name: 用户名称，默认"朋友"
    
    返回:
        str: 问候语
    """
    greetings = [
        f"你好，{name}！很高兴见到你！",
        f"嗨，{name}！今天过得怎么样？",
        f"{name}，欢迎回来！"
    ]
    return "\n".join(greetings)


def say_goodbye(name: str = "朋友") -> str:
    """
    说再见
    
    参数:
        name: 用户名称，默认"朋友"
    
    返回:
        str: 告别语
    """
    farewells = [
        f"再见，{name}！后会有期！",
        f"{name}，下次见！",
        f"祝你好运，{name}！"
    ]
    return "\n".join(farewells)
```

### 第四步：添加依赖

```txt
# requirements.txt
# 此Skill不需要额外依赖
# 如果需要，添加如下：
# pdfplumber>=0.10.0
# python-docx>=1.0.0
```

---

## 4. 能力定义

### 知识点解析

**Tools定义**：

每个Tool是一个可执行的函数，AI可以通过调用它来完成任务。

**Tool结构要求**：

1. **函数名**：清晰表达功能
2. **文档字符串**：详细说明用途、参数、返回值
3. **类型注解**：明确的参数和返回值类型
4. **错误处理**：适当的异常处理

**Tool示例**：

```python
# tools/data_processor.py
import json
from typing import Any


def process_csv(file_path: str, encoding: str = "utf-8") -> dict:
    """
    处理CSV文件，返回JSON数据
    
    参数:
        file_path: CSV文件路径
        encoding: 文件编码，默认utf-8
    
    返回:
        dict: 包含行数据的字典
    """
    try:
        import csv
        
        with open(file_path, 'r', encoding=encoding) as f:
            reader = csv.DictReader(f)
            rows = list(reader)
        
        return {
            "success": True,
            "row_count": len(rows),
            "data": rows[:10],  # 返回前10行预览
            "headers": list(rows[0].keys()) if rows else []
        }
    except FileNotFoundError:
        return {"success": False, "error": f"文件不存在: {file_path}"}
    except Exception as e:
        return {"success": False, "error": str(e)}


def calculate_stats(numbers: list) -> dict:
    """
    计算数字列表的统计信息
    
    参数:
        numbers: 数字列表
    
    返回:
        dict: 统计结果
    """
    if not numbers:
        return {"error": "列表为空"}
    
    import statistics
    
    return {
        "count": len(numbers),
        "sum": sum(numbers),
        "mean": statistics.mean(numbers),
        "median": statistics.median(numbers),
        "min": min(numbers),
        "max": max(numbers),
        "stdev": statistics.stdev(numbers) if len(numbers) > 1 else 0
    }


def format_json(data: Any, indent: int = 2) -> str:
    """
    格式化JSON数据
    
    参数:
        data: 任意JSON兼容数据
        indent: 缩进空格数
    
    返回:
        str: 格式化后的JSON字符串
    """
    return json.dumps(data, indent=indent, ensure_ascii=False)
```

### Skill注册机制

```python
# skill_registry.py

class SkillRegistry:
    """Skill注册中心"""
    
    def __init__(self):
        self.skills = {}
        self.tools = {}
    
    def register_skill(self, skill_info: dict):
        """注册Skill"""
        name = skill_info["name"]
        self.skills[name] = skill_info
        print(f"✅ 注册Skill: {name}")
    
    def register_tool(self, skill_name: str, tool: callable):
        """注册Tool"""
        tool_name = f"{skill_name}.{tool.__name__}"
        self.tools[tool_name] = tool
        print(f"✅ 注册Tool: {tool_name}")
    
    def get_tool(self, tool_name: str) -> callable:
        """获取Tool"""
        return self.tools.get(tool_name)
    
    def list_tools(self) -> list:
        """列出所有Tool"""
        return list(self.tools.keys())


# 全局注册表
registry = SkillRegistry()
```

---

## 5. 工作流

### 知识点解析

**Workflow概念**：工作流（Workflow）是由多个Tool按照特定顺序组成的自动化流程。它可以将复杂任务分解为多个步骤，并自动串联执行。

**工作流场景**：

1. **数据处理流水线**：读取→处理→转换→输出
2. **文档生成流程**：收集数据→生成内容→格式化→保存
3. **多步骤任务**：验证→处理→验证→完成

**工作流实现**：

```python
# workflows/document_pipeline.py
from typing import Any


class DocumentPipeline:
    """文档处理工作流"""
    
    def __init__(self):
        self.steps = []
    
    def add_step(self, name: str, tool: callable, params: dict = None):
        """添加步骤"""
        self.steps.append({
            "name": name,
            "tool": tool,
            "params": params or {}
        })
        print(f"➕ 添加步骤: {name}")
    
    def execute(self, initial_data: Any) -> dict:
        """执行工作流"""
        results = {
            "steps": [],
            "final_result": None
        }
        
        current_data = initial_data
        
        for step in self.steps:
            print(f"\n🔄 执行步骤: {step['name']}")
            
            try:
                # 合并参数
                params = {**step["params"], **({"data": current_data})}
                
                # 执行工具
                result = step["tool"](**params)
                
                results["steps"].append({
                    "name": step["name"],
                    "success": True,
                    "result": result
                })
                
                current_data = result
                
            except Exception as e:
                results["steps"].append({
                    "name": step["name"],
                    "success": False,
                    "error": str(e)
                })
                results["final_result"] = {"error": str(e)}
                return results
        
        results["final_result"] = current_data
        return results


def create_document_pipeline(data: dict) -> dict:
    """
    创建文档处理工作流
    
    参数:
        data: 初始数据
    
    返回:
        dict: 处理结果
    """
    pipeline = DocumentPipeline()
    
    # 添加步骤
    pipeline.add_step("数据验证", validate_data)
    pipeline.add_step("数据转换", transform_data)
    pipeline.add_step("内容生成", generate_content)
    pipeline.add_step("格式处理", format_output)
    
    # 执行
    return pipeline.execute(data)


def validate_data(data: dict) -> dict:
    """验证数据"""
    errors = []
    
    if "title" not in data:
        errors.append("缺少标题")
    if "content" not in data:
        errors.append("缺少内容")
    
    if errors:
        raise ValueError(f"数据验证失败: {', '.join(errors)}")
    
    return {"valid": True, "data": data}


def transform_data(data: dict) -> dict:
    """转换数据"""
    transformed = data.copy()
    transformed["title"] = transformed["title"].strip()
    transformed["content"] = transformed["content"].strip()
    return transformed


def generate_content(data: dict) -> dict:
    """生成内容"""
    return {
        **data,
        "generated_at": "2024-01-01",
        "word_count": len(data.get("content", "").split())
    }


def format_output(data: dict) -> dict:
    """格式化输出"""
    return {
        "document": {
            "title": data["title"],
            "content": data["content"],
            "metadata": {
                "generated_at": data.get("generated_at"),
                "word_count": data.get("word_count")
            }
        }
    }
```

---

## 6. 测试与调试

### 知识点解析

**测试策略**：

1. **单元测试**：测试每个Tool函数
2. **集成测试**：测试Tool之间的协作
3. **端到端测试**：测试完整的工作流

**测试框架**：

```python
# test_skill.py
import unittest
from tools.greet import greet_user, say_goodbye
from tools.data_processor import calculate_stats


class TestGreetSkill(unittest.TestCase):
    """打招呼Skill测试"""
    
    def test_greet_user_default(self):
        """测试默认打招呼"""
        result = greet_user()
        self.assertIn("朋友", result)
    
    def test_greet_user_custom_name(self):
        """测试自定义名字"""
        result = greet_user("张三")
        self.assertIn("张三", result)
    
    def test_say_goodbye(self):
        """测试告别"""
        result = say_goodbye()
        self.assertIn("再见", result)


class TestDataProcessor(unittest.TestCase):
    """数据处理Tool测试"""
    
    def test_calculate_stats_basic(self):
        """测试基本统计"""
        numbers = [1, 2, 3, 4, 5]
        result = calculate_stats(numbers)
        
        self.assertEqual(result["count"], 5)
        self.assertEqual(result["sum"], 15)
        self.assertEqual(result["mean"], 3)
        self.assertEqual(result["min"], 1)
        self.assertEqual(result["max"], 5)
    
    def test_calculate_stats_empty(self):
        """测试空列表"""
        result = calculate_stats([])
        self.assertIn("error", result)
    
    def test_calculate_stats_single(self):
        """测试单元素"""
        result = calculate_stats([10])
        self.assertEqual(result["mean"], 10)


if __name__ == "__main__":
    unittest.main()
```

**调试技巧**：

1. **日志输出**：在关键位置添加print语句
2. **参数检查**：使用assert验证参数
3. **异常捕获**：详细记录错误信息
4. **逐步执行**：分步骤测试工作流

```python
# 调试示例
def debug_tool(param: dict) -> dict:
    """带调试的工具"""
    print(f"🔍 输入参数: {param}")
    
    try:
        # 验证参数
        assert "key" in param, "缺少必需的key参数"
        
        # 执行逻辑
        result = process(param)
        
        print(f"✅ 结果: {result}")
        return result
        
    except AssertionError as e:
        print(f"⚠️  验证错误: {e}")
        raise
    except Exception as e:
        print(f"❌ 执行错误: {e}")
        raise
```

---

## 7. 发布与分享

### 知识点解析

**发布流程**：

1. 整理目录结构
2. 编写README文档
3. 创建requirements.txt
4. 测试兼容性
5. 打包发布

**README模板**：

```markdown
# Skill名称

简要描述这个Skill能做什么。

## 功能列表

- 功能1：描述
- 功能2：描述
- 功能3：描述

## 使用方法

### 安装

```bash
# 复制到Skill目录
```

### 使用

```
触发词: xxx
```

## 示例

### 示例1

输入：
```

输出：
```

## 依赖

- python >= 3.10
- package1 >= 1.0.0
- package2 >= 2.0.0

## 版本历史

- 1.0.0: 初始版本
```

**打包方式**：

```bash
# 方式1：直接复制
cp -r my_skill/ ~/.workbuddy/skills/

# 方式2：创建ZIP包
zip -r my_skill.zip my_skill/
```

---

## 实战案例

### 案例1：完整的Skill实现

```python
"""
完整Skill示例：数据处理Skill
"""

# 目录结构：
# data_processor/
# ├── SKILL.md
# ├── tools/
# │   ├── __init__.py
# │   ├── processor.py
# │   └── converter.py
# └── workflows/
#     ├── __init__.py
#     └── pipeline.py


# ============================================================
# SKILL.md 内容
# ============================================================

SKILL_CONTENT = '''
---
name: data_processor
title: 数据处理专家
description: 提供数据处理、转换和分析能力
version: 1.0.0
author: MCP Team
location: plugin
trigger: 数据|处理|转换|分析
---

capabilities:
  tools:
    - name: process_csv
      description: 处理CSV文件，返回JSON数据
      script: tools/processor.py
      function: process_csv
      
    - name: process_excel
      description: 处理Excel文件
      script: tools/processor.py
      function: process_excel
      
    - name: convert_format
      description: 转换数据格式
      script: tools/converter.py
      function: convert_format
      
    - name: analyze_data
      description: 分析数据统计信息
      script: tools/converter.py
      function: analyze_data
      
  workflows:
    - name: data_pipeline
      description: 完整的数据处理流水线
      script: workflows/pipeline.py
'''


# ============================================================
# tools/processor.py
# ============================================================

import csv
import json
from typing import Any


def process_csv(file_path: str, encoding: str = "utf-8") -> str:
    """
    处理CSV文件
    
    参数:
        file_path: CSV文件路径
        encoding: 文件编码
    
    返回:
        str: JSON格式的处理结果
    """
    try:
        with open(file_path, 'r', encoding=encoding) as f:
            reader = csv.DictReader(f)
            rows = list(reader)
        
        return json.dumps({
            "success": True,
            "row_count": len(rows),
            "preview": rows[:5],
            "headers": list(rows[0].keys()) if rows else []
        }, indent=2, ensure_ascii=False)
        
    except FileNotFoundError:
        return json.dumps({"success": False, "error": f"文件不存在: {file_path}"})
    except Exception as e:
        return json.dumps({"success": False, "error": str(e)})


def process_excel(file_path: str, sheet_name: str = None) -> str:
    """
    处理Excel文件
    
    参数:
        file_path: Excel文件路径
        sheet_name: 工作表名称
    
    返回:
        str: JSON格式的处理结果
    """
    # 简化版本，实际需要openpyxl
    return json.dumps({
        "success": True,
        "message": "Excel处理功能",
        "file": file_path,
        "sheet": sheet_name or "默认工作表"
    })


# ============================================================
# tools/converter.py
# ============================================================

import json
from typing import Any


def convert_format(data: Any, target_format: str = "json") -> str:
    """
    转换数据格式
    
    参数:
        data: 输入数据（支持dict、list、str）
        target_format: 目标格式（json、csv、xml）
    
    返回:
        str: 转换后的数据
    """
    # 先转换为Python对象
    if isinstance(data, str):
        try:
            data = json.loads(data)
        except json.JSONDecodeError:
            return json.dumps({"error": "无效的JSON字符串"})
    
    # 转换为目标格式
    if target_format == "json":
        return json.dumps(data, indent=2, ensure_ascii=False)
    elif target_format == "csv":
        if isinstance(data, list) and data:
            headers = list(data[0].keys())
            lines = [",".join(headers)]
            for item in data:
                lines.append(",".join(str(item.get(h, "")) for h in headers))
            return "\n".join(lines)
        return ""
    else:
        return json.dumps({"error": f"不支持的目标格式: {target_format}"})


def analyze_data(data: Any) -> str:
    """
    分析数据统计信息
    
    参数:
        data: 输入数据（dict或list）
    
    返回:
        str: 统计分析结果
    """
    try:
        if isinstance(data, str):
            data = json.loads(data)
        
        if isinstance(data, dict):
            # 分析字典
            result = {
                "type": "object",
                "key_count": len(data.keys()),
                "keys": list(data.keys())
            }
        elif isinstance(data, list):
            # 分析列表
            if data and isinstance(data[0], dict):
                result = {
                    "type": "array_of_objects",
                    "item_count": len(data),
                    "fields": list(data[0].keys()) if data else []
                }
            else:
                result = {
                    "type": "array",
                    "item_count": len(data),
                    "sample": data[:3]
                }
        else:
            result = {"type": "primitive", "value": str(data)}
        
        return json.dumps(result, indent=2, ensure_ascii=False)
        
    except Exception as e:
        return json.dumps({"error": str(e)})


# ============================================================
# workflows/pipeline.py
# ============================================================

import json


def data_pipeline(file_path: str) -> str:
    """
    完整的数据处理流水线
    
    参数:
        file_path: 数据文件路径
    
    返回:
        str: 处理结果
    """
    results = []
    
    # 步骤1：读取文件
    results.append({"step": "read", "status": "processing"})
    
    # 这里简化处理，实际需要调用processor
    data = {"message": f"已读取文件: {file_path}"}
    results.append({"step": "read", "status": "success", "data": data})
    
    # 步骤2：转换格式
    results.append({"step": "convert", "status": "processing"})
    converted = json.dumps(data)
    results.append({"step": "convert", "status": "success", "result": converted})
    
    # 步骤3：分析数据
    results.append({"step": "analyze", "status": "processing"})
    analysis = {"total_records": 1, "fields": 1}
    results.append({"step": "analyze", "status": "success", "result": analysis})
    
    return json.dumps({
        "pipeline_status": "completed",
        "steps": results,
        "final_result": analysis
    }, indent=2, ensure_ascii=False)


# ============================================================
# 测试代码
# ============================================================

def test_skill():
    """测试数据处理Skill"""
    print("\n" + "=" * 50)
    print("测试数据处理Skill")
    print("=" * 50)
    
    # 测试数据转换
    test_data = [
        {"name": "张三", "age": 25},
        {"name": "李四", "age": 30}
    ]
    
    print("\n测试 convert_format:")
    json_result = convert_format(test_data, "json")
    print(json_result[:200])
    
    csv_result = convert_format(test_data, "csv")
    print(csv_result)
    
    # 测试数据分析
    print("\n测试 analyze_data:")
    analysis = analyze_data(test_data)
    print(analysis)
    
    # 测试工作流
    print("\n测试 data_pipeline:")
    pipeline_result = data_pipeline("test.csv")
    print(pipeline_result)


if __name__ == "__main__":
    test_skill()
```

---

## 本章小结

本章我们学习了自定义Skill的开发：

1. **Skill简介**：理解了Skill的概念、价值和与MCP的区别
2. **结构规范**：掌握了Skill的目录结构和配置文件格式
3. **基础开发**：学会了创建第一个Skill的完整流程
4. **能力定义**：掌握了Tools的定义和实现方法
5. **工作流**：学会了创建自动化工作流
6. **测试调试**：掌握了单元测试和调试技巧
7. **发布分享**：学会了打包和分享Skill

通过这些内容，你已经具备了独立开发自定义Skill的能力，可以根据业务需求创建各种AI能力扩展。
