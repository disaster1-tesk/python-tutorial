# AI Agent 智能代理

## 1. AI Agent 基础概念

### 知识点解析

**概念定义**：AI Agent（智能代理）是一种能够自主感知环境、规划行动、执行任务并反思结果的 AI 系统。与简单的 LLM 调用不同，Agent 具有更复杂的行为模式和决策能力。

**核心概念**：
- **感知（Perception）**：Agent 通过工具或接口感知外部环境
- **规划（Planning）**：Agent 能够将复杂任务分解为子步骤
- **行动（Action）**：Agent 可以调用工具执行实际操作
- **反思（Reflection）**：Agent 能够评估行动结果并调整策略

**核心架构**：
1. **ReAct**：Reasoning + Acting，推理与行动结合
2. **Tool Use**：使用各种工具扩展能力
3. **Memory**：保持对话和任务历史
4. **Planning**：任务分解和计划执行

**核心规则**：
1. Agent = LLM + 工具 + 记忆 + 执行循环
2. 工具（Tools）是 Agent 能力的延伸
3. 迭代执行是 Agent 的核心工作方式
4. 需要设置退出条件防止无限循环

**常见易错点**：
1. 工具描述不清晰导致 Agent 选择错误工具
2. 没有设置最大迭代次数导致无限循环
3. 缺少错误处理机制导致执行失败
4. 记忆管理不当导致上下文混乱

### 实战案例

#### 案例1：基础 ReAct Agent
```python
from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain.prompts import ChatPromptTemplate
from langchain.tools import Tool

llm = ChatOpenAI(model="gpt-3.5-turbo")

# 定义工具
def search_wiki(query: str) -> str:
    """搜索维基百科（模拟）"""
    return f"关于{query}的维基百科信息..."

def calculate(expr: str) -> str:
    """数学计算（模拟）"""
    try:
        result = eval(expr)
        return str(result)
    except:
        return "计算错误"

tools = [
    Tool.from_function(
        func=search_wiki,
        name="wiki_search",
        description="当需要查找百科知识时使用此工具"
    ),
    Tool.from_function(
        func=calculate,
        name="calculator",
        description="用于数学计算，如 '2+3*5'"
    )
]

# 创建 Agent
prompt = ChatPromptTemplate.from_template(
    """你是一个智能助手，可以使用工具完成任务。

可用的工具：
- wiki_search: 搜索维基百科
- calculator: 数学计算

问题：{input}
思考过程：{agent_scratchpad}"""
)

agent = create_openai_functions_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, max_iterations=5)

# 执行
result = agent_executor.invoke({"input": "Python的创始人的出生年份是多少？"})
print(result["output"])
```

---

## 2. AutoGPT 架构

### 知识点解析

**概念定义**：AutoGPT 是一个自主运行的 AI Agent，能够根据目标自动规划、分解任务、循环执行直到完成。

**核心概念**：
- **Goal/Task**：最终要达成的目标
- **Task List**：待执行的子任务列表
- **Loop**：持续执行直到目标达成或达到限制
- **Critique**：对执行结果进行评估

**工作流程**：
1. 分析目标，分解为可执行的子任务
2. 按优先级执行任务
3. 评估执行结果
4. 根据结果更新任务列表
5. 重复直到完成或达到限制

**核心规则**：
1. 任务分解要足够细粒度
2. 每个任务完成后都要评估
3. 需要保存中间结果供后续使用
4. 设置合理的迭代上限

### 实战案例

#### 案例1：简化版 AutoGPT
```python
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

llm = ChatOpenAI(model="gpt-3.5-turbo")

class SimpleAutoGPT:
    def __init__(self, llm):
        self.llm = llm
        self.tasks = []
        self.completed_tasks = []
        self.results = {}
    
    def run(self, goal: str, max_iterations: int = 5):
        print(f"🎯 目标: {goal}\n")
        
        # 1. 分解任务
        self._decompose_tasks(goal)
        
        # 2. 循环执行
        for i in range(max_iterations):
            if not self.tasks:
                break
            
            print(f"--- 迭代 {i+1}/{max_iterations} ---")
            
            # 执行当前任务
            task = self.tasks.pop(0)
            result = self._execute_task(task)
            
            # 记录结果
            self.completed_tasks.append(task)
            self.results[task] = result
            
            print(f"✅ 完成: {task}\n")
        
        # 3. 总结结果
        return self._summarize()
    
    def _decompose_tasks(self, goal: str):
        prompt = ChatPromptTemplate.from_template(
            """将以下目标分解为具体的执行步骤（最多5步）：
目标: {goal}

输出格式：
1. 步骤1
2. 步骤2
3. ..."""
        )
        response = self.llm.invoke(prompt.invoke({"goal": goal}))
        
        # 解析任务列表
        lines = response.content.split('\n')
        for line in lines:
            if line.strip() and (line[0].isdigit() or line.startswith('-')):
                task = line.lstrip('1234567890.- ').strip()
                if task:
                    self.tasks.append(task)
        
        print(f"📋 任务列表: {self.tasks}\n")
    
    def _execute_task(self, task: str):
        prompt = ChatPromptTemplate.from_template(
            """完成以下任务：
任务: {task}

提供详细的执行结果："""
        )
        response = self.llm.invoke(prompt.invoke({"task": task}))
        return response.content
    
    def _summarize(self):
        prompt = ChatPromptTemplate.from_template(
            """根据以下任务执行结果，总结最终答案：
任务结果: {results}

目标完成情况总结："""
        )
        return self.llm.invoke(prompt.invoke({"results": self.results})).content

# 使用
agent = SimpleAutoGPT(llm)
result = agent.run("解释什么是机器学习")
print(result.content)
```

---

## 3. Claude Agent 模式

### 知识点解析

**核心概念**：
- **System Prompt**：系统级指令，定义 Agent 行为模式
- **Tool Use**：精确的函数调用和参数
- **Result Processing**：处理工具返回结果
- **Human in the Loop**：人类介入确认关键决策

**核心规则**：
1. 清晰的系统提示是基础
2. 工具定义要精确（名称、描述、参数）
3. 结果处理要完整
4. 适时让人类确认

### 实战案例

#### 案例1：Claude-style Agent
```python
from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain.prompts import ChatPromptTemplate
from langchain.tools import Tool

llm = ChatOpenAI(model="gpt-3.5-turbo")

# 模拟 Claude 的系统提示风格
system_prompt = """你是一个 Helpful AI Assistant。

工作模式：
1. 理解用户意图
2. 规划执行步骤
3. 使用工具获取信息
4. 整合信息给出答案

重要原则：
- 如果不确定，明确说明
- 复杂问题先拆解再解决
- 给出答案时说明依据"""

# 定义工具
def get_weather(city: str) -> str:
    """获取城市天气"""
    return f"{city}今天天气晴朗，25°C"

def search_code(query: str) -> str:
    """搜索代码库（模拟）"""
    return f"搜索'{query}'的结果..."

tools = [
    Tool.from_function(func=get_weather, name="get_weather", description="获取指定城市的天气"),
    Tool.from_function(func=search_code, name="search_code", description="搜索代码或技术文档"),
]

prompt = ChatPromptTemplate.from_template(
    f"""{system_prompt}

问题：{{input}}
思考：{{agent_scratchpad}}"""
)

agent = create_openai_functions_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, max_iterations=3)

result = agent_executor.invoke({"input": "北京今天天气怎么样？"})
print(result["output"])
```

---

## 4. 多 Agent 协作系统

### 知识点解析

**概念定义**：多 Agent 系统由多个具有不同职责的 Agent 组成，它们通过协作完成复杂任务。

**核心模式**：
- **Supervisor + Workers**：一个主管 Agent 协调多个执行 Agent
- **Debate**：多个 Agent 讨论并达成共识
- **Sequential**：多个 Agent 依次处理不同阶段

**核心规则**：
1. 每个 Agent 有明确的职责
2. 定义清晰的通信协议
3. 需要汇总结果的主 Agent
4. 考虑 Agent 间的依赖关系

### 实战案例

#### 案例1：Supervisor 模式
```python
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

llm = ChatOpenAI(model="gpt-3.5-turbo")

# 定义不同角色的 Agent
class RoleAgent:
    def __init__(self, role: str, expertise: str):
        self.role = role
        self.prompt = ChatPromptTemplate.from_template(
            f"""你是{role}专家。
专业领域: {expertise}
            
任务: {{task}}
            
请以{role}的角度给出专业回答："""
        )
    
    def invoke(self, task: str):
        return self.llm.invoke(self.prompt.invoke({"task": task})).content

# 创建多个 Agent
researcher = RoleAgent("研究员", "调研和信息收集")
coder = RoleAgent("程序员", "代码实现和优化")
reviewer = RoleAgent("审核员", "质量和错误检查")

# Supervisor
def supervisor_task(task: str) -> str:
    print(f"📌 任务: {task}\n")
    
    # 1. 调研阶段
    print("🔍 阶段1: 调研...")
    research_result = researcher.invoke(f"调研{task}相关的信息")
    print(f"调研结果: {research_result[:100]}...\n")
    
    # 2. 实现阶段
    print("💻 阶段2: 实现...")
    code_result = coder.invoke(f"基于以下调研结果实现：\n{research_result}")
    print(f"代码: {code_result[:100]}...\n")
    
    # 3. 审核阶段
    print("🔎 阶段3: 审核...")
    review_result = reviewer.invoke(f"审核以下实现：\n{code_result}")
    print(f"审核意见: {review_result[:100]}...\n")
    
    # 4. 总结
    return f"最终结果:\n{code_result}"

result = supervisor_task("实现一个Python Web服务器")
print(result)
```

---

## 5. Agent 最佳实践

### 设计原则

1. **工具设计**
   - 工具名称要清晰描述功能
   - 工具描述要说明使用场景
   - 参数要明确类型和含义

2. **提示词设计**
   - 系统提示定义 Agent 角色
   - 任务提示说明具体要求
   - 包含思考过程的占位符

3. **执行控制**
   - 设置合理的迭代上限
   - 添加超时机制
   - 处理异常情况

4. **结果验证**
   - 检查工具返回结果
   - 验证最终输出质量
   - 必要时进行二次确认

### 调试技巧

1. 逐步测试：先测试单步，再测试多步
2. 记录日志：追踪每一步的输入输出
3. 对比分析：比较不同提示词的效果
4. 边界测试：测试极端和异常情况

### 性能优化

1. 减少不必要的工具调用
2. 批量处理相关任务
3. 缓存常用结果
4. 适时使用缓存的思考结果