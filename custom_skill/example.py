# 自定义 Skill 开发示例代码

"""
自定义 Skill 示例代码
展示Skill的开发、测试和调试
"""

import json
import os
from typing import Any

# ============================================================
# 1. Skill基础架构
# ============================================================


class SkillBase:
    """Skill基础类"""
    
    def __init__(self, name: str, title: str, description: str):
        self.name = name
        self.title = title
        self.description = description
        self.tools = {}
        self.workflows = {}
    
    def register_tool(self, name: str, func: callable, description: str = ""):
        """注册工具"""
        self.tools[name] = {
            "function": func,
            "description": description
        }
        print(f"🔧 注册工具: {self.name}.{name}")
    
    def register_workflow(self, name: str, func: callable, description: str = ""):
        """注册工作流"""
        self.workflows[name] = {
            "function": func,
            "description": description
        }
        print(f"🔄 注册工作流: {self.name}.{name}")
    
    def get_tool(self, name: str):
        """获取工具"""
        return self.tools.get(name)
    
    def list_tools(self) -> list:
        """列出所有工具"""
        return [
            {"name": name, "description": info["description"]}
            for name, info in self.tools.items()
        ]


class SkillRegistry:
    """Skill注册中心"""
    
    def __init__(self):
        self.skills = {}
        print("📋 Skill注册中心已创建")
    
    def register(self, skill: SkillBase):
        """注册Skill"""
        self.skills[skill.name] = skill
        print(f"✅ 注册Skill: {skill.title}")
    
    def get_skill(self, name: str) -> SkillBase:
        """获取Skill"""
        return self.skills.get(name)
    
    def list_skills(self) -> list:
        """列出所有Skill"""
        return [
            {
                "name": s.name,
                "title": s.title,
                "description": s.description,
                "tool_count": len(s.tools),
                "workflow_count": len(s.workflows)
            }
            for s in self.skills.values()
        ]


def test_skill_architecture():
    """测试Skill架构"""
    print("\n" + "=" * 50)
    print("示例1: Skill基础架构")
    print("=" * 50)
    
    # 创建注册中心
    registry = SkillRegistry()
    
    # 创建Skill
    hello_skill = SkillBase(
        name="hello_skill",
        title="打招呼技能",
        description="提供打招呼和告别功能"
    )
    
    # 定义工具函数
    def greet(name: str = "朋友") -> str:
        """打招呼"""
        return f"你好，{name}！欢迎使用Skill系统！"
    
    def farewell(name: str = "朋友") -> str:
        """告别"""
        return f"再见，{name}！后会有期！"
    
    # 注册工具
    hello_skill.register_tool("greet", greet, "向用户打招呼")
    hello_skill.register_tool("farewell", farewell, "说再见")
    
    # 注册到注册中心
    registry.register(hello_skill)
    
    # 列出所有Skill
    print("\n已注册的Skill:")
    for skill in registry.list_skills():
        print(f"  - {skill['title']} ({skill['name']})")
        print(f"    工具: {skill['tool_count']}个")
        print(f"    描述: {skill['description']}")
    
    # 调用工具
    print("\n调用工具:")
    tool = hello_skill.get_tool("greet")
    if tool:
        result = tool["function"](name="张三")
        print(f"  greet('张三'): {result}")


# ============================================================
# 2. 数据处理Skill
# ============================================================


class DataProcessorSkill(SkillBase):
    """数据处理Skill"""
    
    def __init__(self):
        super().__init__(
            name="data_processor",
            title="数据处理专家",
            description="提供数据处理、转换和分析能力"
        )
        self._register_tools()
    
    def _register_tools(self):
        """注册数据处理工具"""
        
        def process_csv(file_path: str) -> str:
            """处理CSV文件"""
            try:
                import csv
                with open(file_path, 'r', encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    rows = list(reader)
                return json.dumps({
                    "success": True,
                    "row_count": len(rows),
                    "headers": list(rows[0].keys()) if rows else [],
                    "preview": rows[:3]
                }, ensure_ascii=False)
            except Exception as e:
                return json.dumps({"success": False, "error": str(e)})
        
        def process_json(json_str: str) -> str:
            """处理JSON数据"""
            try:
                data = json.loads(json_str)
                return json.dumps({
                    "success": True,
                    "type": type(data).__name__,
                    "size": len(data) if isinstance(data, (list, dict)) else 1
                }, ensure_ascii=False)
            except Exception as e:
                return json.dumps({"success": False, "error": str(e)})
        
        def convert_to_csv(data: list) -> str:
            """转换为CSV格式"""
            if not data or not isinstance(data, list):
                return "错误: 数据为空或不是列表"
            
            if not data:
                return ""
            
            headers = list(data[0].keys())
            lines = [",".join(headers)]
            
            for item in data:
                lines.append(",".join(str(item.get(h, "")) for h in headers))
            
            return "\n".join(lines)
        
        def analyze_numbers(numbers: list) -> dict:
            """分析数字列表"""
            if not numbers:
                return {"error": "数字列表为空"}
            
            return {
                "count": len(numbers),
                "sum": sum(numbers),
                "mean": sum(numbers) / len(numbers),
                "min": min(numbers),
                "max": max(numbers),
                "sorted": sorted(numbers)
            }
        
        # 注册工具
        self.register_tool("process_csv", process_csv, "读取并处理CSV文件")
        self.register_tool("process_json", process_json, "解析并处理JSON数据")
        self.register_tool("convert_csv", convert_to_csv, "将数据转换为CSV格式")
        self.register_tool("analyze_numbers", analyze_numbers, "分析数字列表统计信息")


def test_data_processor():
    """测试数据处理Skill"""
    print("\n" + "=" * 50)
    print("示例2: 数据处理Skill")
    print("=" * 50)
    
    # 创建Skill
    skill = DataProcessorSkill()
    
    # 测试JSON处理
    print("\n测试 process_json:")
    result = skill.tools["process_json"]["function"](
        '{"name": "张三", "age": 25}'
    )
    print(f"  结果: {result}")
    
    # 测试CSV转换
    print("\n测试 convert_to_csv:")
    test_data = [
        {"name": "张三", "age": 25},
        {"name": "李四", "age": 30}
    ]
    result = skill.tools["convert_csv"]["function"](test_data)
    print(f"  结果:\n{result}")
    
    # 测试数字分析
    print("\n测试 analyze_numbers:")
    result = skill.tools["analyze_numbers"]["function"]([10, 20, 30, 40, 50])
    print(f"  结果: {result}")


# ============================================================
# 3. 文件处理Skill
# ============================================================


class FileProcessorSkill(SkillBase):
    """文件处理Skill"""
    
    def __init__(self):
        super().__init__(
            name="file_processor",
            title="文件处理专家",
            description="提供文件读取、写入和管理能力"
        )
        self._register_tools()
    
    def _register_tools(self):
        """注册文件处理工具"""
        
        def read_text(file_path: str, encoding: str = "utf-8") -> str:
            """读取文本文件"""
            try:
                with open(file_path, 'r', encoding=encoding) as f:
                    content = f.read()
                return json.dumps({
                    "success": True,
                    "path": file_path,
                    "length": len(content),
                    "preview": content[:200]
                }, ensure_ascii=False)
            except Exception as e:
                return json.dumps({"success": False, "error": str(e)})
        
        def write_text(file_path: str, content: str, encoding: str = "utf-8") -> str:
            """写入文本文件"""
            try:
                os.makedirs(os.path.dirname(file_path), exist_ok=True)
                with open(file_path, 'w', encoding=encoding) as f:
                    f.write(content)
                return json.dumps({
                    "success": True,
                    "path": file_path,
                    "bytes_written": len(content)
                }, ensure_ascii=False)
            except Exception as e:
                return json.dumps({"success": False, "error": str(e)})
        
        def list_files(directory: str = ".", pattern: str = "*") -> str:
            """列出目录文件"""
            import fnmatch
            try:
                files = []
                for name in os.listdir(directory):
                    if fnmatch.fnmatch(name, pattern):
                        files.append(name)
                return json.dumps({
                    "success": True,
                    "directory": directory,
                    "count": len(files),
                    "files": files
                }, ensure_ascii=False)
            except Exception as e:
                return json.dumps({"success": False, "error": str(e)})
        
        def get_file_info(file_path: str) -> str:
            """获取文件信息"""
            try:
                stat = os.stat(file_path)
                return json.dumps({
                    "success": True,
                    "path": file_path,
                    "size": stat.st_size,
                    "modified": stat.st_mtime,
                    "is_file": os.path.isfile(file_path),
                    "is_dir": os.path.isdir(file_path)
                }, ensure_ascii=False)
            except Exception as e:
                return json.dumps({"success": False, "error": str(e)})
        
        def search_in_file(file_path: str, keyword: str) -> str:
            """在文件中搜索关键字"""
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                
                matches = []
                for i, line in enumerate(lines, 1):
                    if keyword in line:
                        matches.append({
                            "line": i,
                            "content": line.strip()
                        })
                
                return json.dumps({
                    "success": True,
                    "keyword": keyword,
                    "matches": len(matches),
                    "results": matches[:10]
                }, ensure_ascii=False)
            except Exception as e:
                return json.dumps({"success": False, "error": str(e)})
        
        # 注册工具
        self.register_tool("read_text", read_text, "读取文本文件")
        self.register_tool("write_text", write_text, "写入文本文件")
        self.register_tool("list_files", list_files, "列出目录文件")
        self.register_tool("file_info", get_file_info, "获取文件信息")
        self.register_tool("search", search_in_file, "在文件中搜索关键字")


def test_file_processor():
    """测试文件处理Skill"""
    print("\n" + "=" * 50)
    print("示例3: 文件处理Skill")
    print("=" * 50)
    
    # 创建Skill
    skill = FileProcessorSkill()
    
    # 列出当前目录文件
    print("\n测试 list_files:")
    result = skill.tools["list_files"]["function"](".", "*.py")
    print(f"  结果: {result[:300]}...")
    
    # 获取当前文件信息
    print("\n测试 file_info:")
    result = skill.tools["file_info"]["function"]("custom_skill.py")
    print(f"  结果: {result}")


# ============================================================
# 4. 工作流实现
# ============================================================


class WorkflowEngine:
    """工作流引擎"""
    
    def __init__(self, name: str):
        self.name = name
        self.steps = []
    
    def add_step(self, name: str, func: callable, params: dict = None):
        """添加步骤"""
        self.steps.append({
            "name": name,
            "func": func,
            "params": params or {}
        })
        print(f"  ➕ 步骤: {name}")
    
    def execute(self, initial_data: Any = None) -> dict:
        """执行工作流"""
        results = {
            "workflow": self.name,
            "status": "running",
            "steps": [],
            "final_result": None
        }
        
        current_data = initial_data
        
        for i, step in enumerate(self.steps):
            print(f"\n🔄 执行步骤 {i+1}/{len(self.steps)}: {step['name']}")
            
            try:
                # 准备参数
                params = step["params"].copy()
                if current_data is not None:
                    params["input_data"] = current_data
                
                # 执行
                result = step["func"](**params)
                
                results["steps"].append({
                    "name": step["name"],
                    "status": "success",
                    "result": str(result)[:100]
                })
                
                current_data = result
                
            except Exception as e:
                results["steps"].append({
                    "name": step["name"],
                    "status": "error",
                    "error": str(e)
                })
                results["status"] = "failed"
                results["final_result"] = {"error": str(e)}
                return results
        
        results["status"] = "completed"
        results["final_result"] = current_data
        return results


def create_data_processing_workflow():
    """创建数据处理工作流"""
    print("\n" + "=" * 50)
    print("示例4: 工作流引擎")
    print("=" * 50)
    
    # 定义工作流步骤
    def step_load_data(**kwargs):
        """加载数据"""
        data = kwargs.get("input_data", {})
        print(f"    加载数据: {len(data)} 条记录")
        return {**data, "loaded": True}
    
    def step_validate(**kwargs):
        """验证数据"""
        data = kwargs.get("input_data", {})
        print(f"    验证: 检查数据完整性")
        if not data.get("loaded"):
            raise ValueError("数据未加载")
        return {**data, "validated": True}
    
    def step_transform(**kwargs):
        """转换数据"""
        data = kwargs.get("input_data", {})
        print(f"    转换: 处理数据格式")
        transformed = {
            **data,
            "transformed": True,
            "timestamp": "2024-01-01"
        }
        return transformed
    
    def step_save(**kwargs):
        """保存结果"""
        data = kwargs.get("input_data", {})
        print(f"    保存: 处理完成")
        return {**data, "saved": True, "status": "completed"}
    
    # 创建工作流
    workflow = WorkflowEngine("data_processing")
    workflow.add_step("加载数据", step_load_data)
    workflow.add_step("验证数据", step_validate)
    workflow.add_step("转换数据", step_transform)
    workflow.add_step("保存结果", step_save)
    
    # 执行工作流
    print("\n开始执行工作流:")
    result = workflow.execute({"test": "data"})
    
    print(f"\n工作流状态: {result['status']}")
    print(f"步骤数: {len(result['steps'])}")
    print(f"最终结果: {result['final_result']}")


# ============================================================
# 5. Skill测试框架
# ============================================================


class SkillTester:
    """Skill测试框架"""
    
    def __init__(self, skill: SkillBase):
        self.skill = skill
        self.results = []
    
    def test_tool(self, tool_name: str, input_data: Any, expected_contains: str = None) -> bool:
        """测试工具"""
        print(f"\n🧪 测试工具: {tool_name}")
        print(f"   输入: {input_data}")
        
        tool = self.skill.get_tool(tool_name)
        if not tool:
            print(f"   ❌ 工具不存在")
            self.results.append(False)
            return False
        
        try:
            result = tool["function"](**input_data)
            print(f"   输出: {str(result)[:100]}...")
            
            if expected_contains and expected_contains not in str(result):
                print(f"   ⚠️  结果不包含预期内容")
                self.results.append(False)
                return False
            
            print(f"   ✅ 通过")
            self.results.append(True)
            return True
            
        except Exception as e:
            print(f"   ❌ 错误: {str(e)}")
            self.results.append(False)
            return False
    
    def test_all_tools(self, test_cases: dict) -> dict:
        """测试所有工具"""
        print("\n" + "=" * 50)
        print(f"测试Skill: {self.skill.title}")
        print("=" * 50)
        
        for tool_name, test_data in test_cases.items():
            self.test_tool(
                tool_name,
                test_data.get("input", {}),
                test_data.get("expected")
            )
        
        passed = sum(self.results)
        total = len(self.results)
        
        return {
            "skill": self.skill.name,
            "passed": passed,
            "total": total,
            "success_rate": f"{passed/total*100:.1f}%"
        }


def test_skill_framework():
    """测试Skill测试框架"""
    print("\n" + "=" * 50)
    print("示例5: Skill测试框架")
    print("=" * 50)
    
    # 创建测试Skill
    test_skill = SkillBase("test_skill", "测试技能", "用于测试的Skill")
    
    # 注册测试工具
    def echo(message: str) -> str:
        return f"回显: {message}"
    
    def add(a: int, b: int) -> str:
        return str(a + b)
    
    test_skill.register_tool("echo", echo, "回显消息")
    test_skill.register_tool("add", add, "加法计算")
    
    # 创建测试器
    tester = SkillTester(test_skill)
    
    # 定义测试用例
    test_cases = {
        "echo": {
            "input": {"message": "Hello"},
            "expected": "Hello"
        },
        "add": {
            "input": {"a": 5, "b": 3},
            "expected": "8"
        }
    }
    
    # 运行测试
    result = tester.test_all_tools(test_cases)
    
    print(f"\n测试结果: {result['passed']}/{result['total']} 通过")
    print(f"成功率: {result['success_rate']}")


# ============================================================
# 6. 完整Skill实现示例
# ============================================================


class CalculatorSkill(SkillBase):
    """计算器Skill - 完整示例"""
    
    def __init__(self):
        super().__init__(
            name="calculator",
            title="智能计算器",
            description="提供各种数学计算功能"
        )
        self._register_tools()
        self._register_workflows()
    
    def _register_tools(self):
        """注册计算工具"""
        
        def basic_calc(expression: str) -> str:
            """基础计算"""
            try:
                result = eval(expression)
                return json.dumps({
                    "expression": expression,
                    "result": result,
                    "type": type(result).__name__
                }, ensure_ascii=False)
            except Exception as e:
                return json.dumps({"error": str(e)})
        
        def calculate_bmi(height_cm: float, weight_kg: float) -> str:
            """计算BMI"""
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
            
            return json.dumps({
                "height": height_cm,
                "weight": weight_kg,
                "bmi": round(bmi, 2),
                "status": status
            }, ensure_ascii=False)
        
        def calculate_percentage(value: float, total: float) -> str:
            """计算百分比"""
            if total == 0:
                return json.dumps({"error": "总数不能为0"})
            
            percentage = (value / total) * 100
            return json.dumps({
                "value": value,
                "total": total,
                "percentage": round(percentage, 2),
                "formatted": f"{percentage:.2f}%"
            }, ensure_ascii=False)
        
        def format_currency(amount: float, currency: str = "CNY") -> str:
            """货币格式化"""
            symbols = {
                "CNY": "¥",
                "USD": "$",
                "EUR": "€",
                "GBP": "£"
            }
            symbol = symbols.get(currency, currency)
            return json.dumps({
                "amount": amount,
                "currency": currency,
                "formatted": f"{symbol}{amount:,.2f}"
            }, ensure_ascii=False)
        
        # 注册工具
        self.register_tool("basic_calc", basic_calc, "基础数学计算")
        self.register_tool("bmi", calculate_bmi, "计算BMI指数")
        self.register_tool("percentage", calculate_percentage, "计算百分比")
        self.register_tool("currency", format_currency, "货币格式化")
    
    def _register_workflows(self):
        """注册工作流"""
        
        def financial_analysis(**kwargs) -> str:
            """财务分析工作流"""
            amount = kwargs.get("amount", 0)
            rate = kwargs.get("rate", 0)
            years = kwargs.get("years", 1)
            
            # 计算复利
            future_value = amount * (1 + rate / 100) ** years
            interest = future_value - amount
            
            return json.dumps({
                "principal": amount,
                "rate": rate,
                "years": years,
                "future_value": round(future_value, 2),
                "interest": round(interest, 2)
            }, ensure_ascii=False)
        
        self.register_workflow("financial_analysis", financial_analysis, "财务复利分析")


def test_complete_skill():
    """测试完整Skill"""
    print("\n" + "=" * 50)
    print("示例6: 完整Calculator Skill")
    print("=" * 50)
    
    # 创建Skill
    calc = CalculatorSkill()
    
    # 测试工具
    print("\n工具列表:")
    for tool in calc.list_tools():
        print(f"  - {tool['name']}: {tool['description']}")
    
    # 测试BMI计算
    print("\n测试BMI计算:")
    result = calc.tools["bmi"]["function"](175, 70)
    print(f"  输入: 身高175cm, 体重70kg")
    print(f"  输出: {result}")
    
    # 测试百分比
    print("\n测试百分比:")
    result = calc.tools["percentage"]["function"](25, 200)
    print(f"  输入: 25 / 200")
    print(f"  输出: {result}")
    
    # 测试货币格式化
    print("\n测试货币格式化:")
    result = calc.tools["currency"]["function"](12345.67, "CNY")
    print(f"  输入: 12345.67 CNY")
    print(f"  输出: {result}")
    
    # 测试工作流
    print("\n测试财务分析工作流:")
    workflow = calc.workflows["financial_analysis"]
    result = workflow["function"](amount=10000, rate=5, years=10)
    print(f"  输入: 本金10000, 利率5%, 10年")
    print(f"  输出: {result}")


# ============================================================
# 7. Skill配置生成
# ============================================================


def generate_skill_config(skill: SkillBase) -> str:
    """生成SKILL.md配置"""
    
    config = f"""---
name: {skill.name}
title: {skill.title}
description: {skill.description}
version: 1.0.0
author: MCP Team
location: plugin
---

capabilities:
  tools:
"""
    
    for name, info in skill.tools.items():
        config += f"""    - name: {name}
      description: {info['description']}
      script: tools/{name}.py
      function: {name}
      
"""
    
    config += "  workflows:\n"
    
    for name, info in skill.workflows.items():
        config += f"""    - name: {name}
      description: {info['description']}
      script: workflows/{name}.py
      
"""
    
    return config


def test_config_generation():
    """测试配置生成"""
    print("\n" + "=" * 50)
    print("示例7: Skill配置生成")
    print("=" * 50)
    
    # 创建Skill
    calc = CalculatorSkill()
    
    # 生成配置
    config = generate_skill_config(calc)
    
    print("\n生成的SKILL.md:")
    print(config)


# ============================================================
# 主函数
# ============================================================

if __name__ == "__main__":
    print("=" * 60)
    print("自定义 Skill 开发示例")
    print("=" * 60)
    
    # 运行所有示例
    test_skill_architecture()
    test_data_processor()
    test_file_processor()
    create_data_processing_workflow()
    test_skill_framework()
    test_complete_skill()
    test_config_generation()
    
    print("\n" + "=" * 60)
    print("所有示例完成!")
    print("=" * 60)
