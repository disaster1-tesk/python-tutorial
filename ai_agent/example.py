# AI Agent 示例代码

# ========== 1. 基础 ReAct Agent ==========
from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain.prompts import ChatPromptTemplate
from langchain.tools import Tool

llm = ChatOpenAI(model="gpt-3.5-turbo")

# 定义工具
def search_wiki(query: str) -> str:
    """搜索维基百科"""
    return f"关于{query}的维基百科信息..."

def calculate(expr: str) -> str:
    """数学计算"""
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

print("=== ReAct Agent 测试 ===")
result = agent_executor.invoke({"input": "Python的创始人的出生年份是多少？"})
print(f"结果: {result['output']}\n")


# ========== 2. 简化版 AutoGPT ==========
class SimpleAutoGPT:
    def __init__(self, llm):
        self.llm = llm
        self.tasks = []
        self.completed_tasks = []
        self.results = {}
    
    def run(self, goal: str, max_iterations: int = 3):
        print(f"🎯 目标: {goal}\n")
        
        # 分解任务
        self._decompose_tasks(goal)
        
        # 循环执行
        for i in range(max_iterations):
            if not self.tasks:
                break
            print(f"--- 迭代 {i+1} ---")
            task = self.tasks.pop(0)
            result = self._execute_task(task)
            self.completed_tasks.append(task)
            self.results[task] = result
            print(f"✅ 完成: {task[:50]}\n")
        
        return self._summarize()
    
    def _decompose_tasks(self, goal: str):
        prompt = f"将以下目标分解为具体的执行步骤（最多3步）：\n目标: {goal}\n输出格式：1. 步骤1 2. 步骤2"
        response = self.llm.invoke(prompt)
        lines = response.content.split('\n')
        for line in lines:
            task = line.lstrip('1234567890.- ').strip()
            if task and len(task) > 5:
                self.tasks.append(task)
        print(f"📋 任务: {self.tasks}\n")
    
    def _execute_task(self, task: str):
        response = self.llm.invoke(f"完成以下任务：\n{task}")
        return response.content
    
    def _summarize(self):
        response = self.llm.invoke(f"总结以下任务结果：\n{self.results}")
        return response.content

print("=== AutoGPT 测试 ===")
agent = SimpleAutoGPT(llm)
result = agent.run("创建一个Python函数计算斐波那契数列")
print(result.content[:300])


# ========== 3. 多 Agent 协作 ==========
class MultiAgentSystem:
    def __init__(self, llm):
        self.llm = llm
    
    def run_task(self, task: str):
        # Agent 1: 调研
        research = self.llm.invoke(f"调研：{task}\n提供关键信息点：").content
        
        # Agent 2: 实现
        implement = self.llm.invoke(f"基于以下信息实现：\n{research}\n{task}").content
        
        # Agent 3: 审核
        review = self.llm.invoke(f"审核以下实现并给出建议：\n{implement}").content
        
        return {
            "research": research,
            "implement": implement,
            "review": review
        }

print("\n=== 多 Agent 协作测试 ===")
system = MultiAgentSystem(llm)
result = system.run_task("实现一个Python Web服务器")

print("调研结果:", result["research"][:100])
print("\n实现结果:", result["implement"][:100])
print("\n审核结果:", result["review"][:100])


# ========== 4. 带记忆的 Agent ==========
from langchain.memory import ConversationBufferMemory
from langchain.chains import LLMChain

memory = ConversationBufferMemory(memory_key="history", return_messages=True)

# 带记忆的 Agent 链
chain = LLMChain(
    llm=llm,
    prompt=ChatPromptTemplate.from_template(
        """你是智能助手。
历史记录：{history}
用户：{input}
助手："""
    ),
    memory=memory
)

print("\n=== 带记忆的 Agent 测试 ===")

# 第一轮
r1 = chain.invoke({"input": "我喜欢Python"})
print(f"用户: 我喜欢Python")
print(f"助手: {r1['text'][:100]}\n")

# 第二轮（Agent 应该记住之前的内容）
r2 = chain.invoke({"input": "我刚才说什么语言？"})
print(f"用户: 我刚才说什么语言？")
print(f"助手: {r2['text'][:100]}")


# ========== 5. 工具选择示例 ==========
def select_best_tool(query: str, tools: list) -> str:
    """根据查询选择最佳工具"""
    tool_descriptions = "\n".join([f"- {t.name}: {t.description}" for t in tools])
    prompt = f"""用户问题: {query}

可用工具：
{tool_descriptions}

请选择最合适的工具，只输出工具名称："""
    
    return llm.invoke(prompt).content.strip()

print("\n=== 工具选择测试 ===")
tools_list = [
    Tool.from_function(func=lambda x: "天气信息", name="get_weather", description="获取天气"),
    Tool.from_function(func=lambda x: "搜索结果", name="search", description="搜索信息"),
    Tool.from_function(func=lambda x: "计算结果", name="calculate", description="数学计算")
]

query = "今天北京多少度？"
best_tool = select_best_tool(query, tools_list)
print(f"问题: {query}")
print(f"选择工具: {best_tool}")


print("\n" + "="*50)
print("AI Agent 示例完成")