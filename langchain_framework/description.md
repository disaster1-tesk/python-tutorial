# LangChain AI框架

## 1. LangChain 基础入门

### 知识点解析

**概念定义**：LangChain 是一个用于构建基于大语言模型（LLM）应用的开发框架，它提供了抽象层和工具来简化与 LLMs 的交互，使开发者能够快速构建 AI 应用。

**核心概念**：
- **LLM Chain**：将多个 LLM 调用串联起来的链式结构
- **Prompt Template**：可复用的提示词模板
- **Memory**：为对话添加记忆功能
- **Agents**：使 LLM 能够自主决策和执行行动
- **Document Loader**：加载各种格式的文档
- **Output Parser**：解析 LLM 输出为结构化数据

**核心规则**：
1. LangChain 的核心组件：Model I/O、Retrieval、Memory、Chains、Agents
2. 使用 `ChatOpenAI` 或 `OpenAI` 与 GPT 模型交互
3. `LCEL`（LangChain Expression Language）是新版 API，更简洁
4. `Runnable` 接口统一了所有组件的调用方式

**常见易错点**：
1. 环境变量需要设置 `OPENAI_API_KEY`
2. 使用 `ChatOpenAI` 而不是 `OpenAI` 来进行聊天
3. 提示词模板中使用 `{}` 作为占位符
4. `stuff` 类型的 Chain 会将所有文档一次性输入，可能超出上下文限制

### 实战案例

#### 案例1：基础 LLM 调用
```python
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage

# 初始化 Chat 模型
llm = ChatOpenAI(
    model="gpt-3.5-turbo",
    temperature=0.7,
    max_tokens=1000,
    openai_api_key="your-api-key"  # 建议使用环境变量
)

# 同步调用
response = llm.invoke("What is Python?")
print(response.content)

# 批量调用
responses = llm.batch([
    "What is Python?",
    "What is Java?",
    "What is Go?"
])
for r in responses:
    print(r.content)
```

#### 案例2：使用提示词模板
```python
from langchain.prompts import ChatPromptTemplate

# 创建提示词模板
template = ChatPromptTemplate.from_template(
    "请用{language}编程语言编写一个简单的{hello_type}程序"
)

# 生成提示词
prompt = template.invoke({
    "language": "Python",
    "hello_type": "Hello World"
})

# 调用 LLM
response = llm.invoke(prompt)
print(response.content)
```

#### 案例3：输出结构化数据
```python
from langchain.output_parsers import StructuredOutputParser, ResponseSchema

# 定义输出结构
response_schemas = [
    ResponseSchema(name="language", description="编程语言名称"),
    ResponseSchema(name="difficulty", description="难度等级 beginner/intermediate/advanced"),
    ResponseSchema(name="uses", description="主要应用场景")
]

output_parser = StructuredOutputParser.from_response_schemas(response_schemas)

# 创建带格式说明的提示词
template = ChatPromptTemplate.from_template(
    """请根据以下信息回答：
主题: {topic}
{format_instructions}
"""
)

# 格式化输出说明
format_instructions = output_parser.get_format_instructions()
prompt = template.invoke({"topic": "Python", "format_instructions": format_instructions})

# 获取结构化输出
response = llm.invoke(prompt)
result = output_parser.parse(response.content)
print(result)  # {'language': 'Python', 'difficulty': 'intermediate', 'uses': 'Web开发、数据科学等'}
```

---

## 2. LangChain Chain 链式调用

### 知识点解析

**概念定义**：Chain 是 LangChain 的核心组件，用于将多个组件串联起来，形成完整的工作流程。LCEL（LangChain Expression Language）提供了更简洁的链式调用语法。

**核心概念**：
- **LCEL**：使用 `|` 操作符串联组件
- **Runnable 接口**：所有组件都实现此接口，统一调用方式
- **RunnableSequence**：串联的执行序列
- **Parallel**：并行执行多个任务

**核心规则**：
1. 使用 `|` 操作符串联 LLM、Prompt、OutputParser
2. `.invoke()` 是同步调用，`.stream()` 是流式调用
3. 可以给链中的组件添加名称，便于调试
4. 支持绑定运行时参数到组件

**常见易错点**：
1. 链式调用返回的是 `Runnable`，需要调用 `.invoke()` 执行
2. 中间步骤的输出需要匹配下一步的输入格式
3. 并行执行使用 `RunnableParallel` 或字典语法

### 实战案例

#### 案例1：基础链式调用
```python
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

llm = ChatOpenAI(model="gpt-3.5-turbo")

# 使用 LCEL 语法构建链
prompt = ChatPromptTemplate.from_template(
    "请用一句话介绍 {topic}，不超过50字"
)
chain = prompt | llm

# 执行链
result = chain.invoke({"topic": "Python"})
print(result.content)
```

#### 案例2：带输出解析的链
```python
from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers import StructuredOutputParser, ResponseSchema

llm = ChatOpenAI(model="gpt-3.5-turbo")

# 定义输出结构
schemas = [
    ResponseSchema(name="definition", description="概念定义"),
    ResponseSchema(name="example", description="一个例子")
]
parser = StructuredOutputParser.from_response_schemas(schemas)

# 构建链
prompt = ChatPromptTemplate.from_template(
    "请解释以下概念：{concept}\n{format_instructions}"
)
chain = prompt | llm | parser

# 执行
result = chain.invoke({
    "concept": "递归",
    "format_instructions": parser.get_format_instructions()
})
print(result)  # {'definition': '...', 'example': '...'}
```

#### 案例3：并行执行
```python
from langchain.runnables import RunnableParallel

llm = ChatOpenAI(model="gpt-3.5-turbo")

# 创建多个提示词
prompt1 = ChatPromptTemplate.from_template("用一句话介绍{prompt1}")
prompt2 = ChatPromptTemplate.from_template("用一句话介绍{prompt2}")

# 并行执行
parallel = RunnableParallel({
    "topic1": prompt1 | llm,
    "topic2": prompt2 | llm
})

result = parallel.invoke({
    "prompt1": "Python",
    "prompt2": "JavaScript"
})
print(result["topic1"].content)
print(result["topic2"].content)
```

---

## 3. LangChain Memory 记忆组件

### 知识点解析

**概念定义**：Memory 组件为 LangChain 应用提供持久化和管理对话历史的能力，使 AI 能够记住之前的上下文，实现多轮对话。

**核心概念**：
- **ConversationBufferMemory**：存储完整的对话历史
- **ConversationSummaryMemory**：存储对话摘要，节省 token
- **EntityMemory**：提取并存储实体信息
- **BufferWindowMemory**：只保留最近 N 轮对话

**核心规则**：
1. 在 Chain 中使用 `.with_context()` 或 `RunnableWithMessageHistory`
2. Memory 需要保存提示词模板中的历史消息
3. 不同类型的 Memory 适用于不同场景
4. 需要提供 `session_id` 来区分不同的对话

**常见易错点**：
1. 默认的 Memory 不会自动添加到提示词中
2. 需要在提示词中添加 `{history}` 占位符
3. 长期对话需要考虑 token 限制，优先使用 SummaryMemory

### 实战案例

#### 案例1：基础对话记忆
```python
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.memory import ConversationBufferMemory
from langchain.chains import LLMChain

llm = ChatOpenAI(model="gpt-3.5-turbo")

# 创建记忆组件
memory = ConversationBufferMemory(
    memory_key="history",
    return_messages=True
)

# 创建提示词模板
prompt = ChatPromptTemplate.from_template(
    """你是一个助手。以下是对话历史：
{history}

用户: {input}
助手:"""
)

# 创建带记忆的链
chain = LLMChain(
    llm=llm,
    prompt=prompt,
    memory=memory
)

# 多轮对话
response1 = chain.invoke({"input": "我叫张三"})
print(response1["text"])

response2 = chain.invoke({"input": "我叫什么名字？"})
print(response2["text"])  # 应该能回答"张三"
```

#### 案例2：使用摘要记忆
```python
from langchain.memory import ConversationSummaryMemory

llm = ChatOpenAI(model="gpt-3.5-turbo")

# 使用摘要记忆，节省 token
memory = ConversationSummaryMemory(
    llm=llm,
    memory_key="history",
    return_messages=True
)

prompt = ChatPromptTemplate.from_template(
    """对话历史：
{history}

用户: {input}
助手:"""
)

chain = LLMChain(llm=llm, prompt=prompt, memory=memory)

# 多次对话后，历史会被压缩为摘要
for i in range(5):
    chain.invoke({"input": f"这是第{i+1}次对话"})
    print(f"--- 第{i+1}轮完成 ---")
```

---

## 4. LangChain Agents 智能代理

### 知识点解析

**概念定义**：Agents 是 LangChain 中使 LLM 能够自主决策、调用工具、完成复杂任务的组件。Agent 可以根据 LLM 的输出动态选择和执行行动。

**核心概念**：
- **Tool**：Agent 可以调用的工具（搜索、计算、文件操作等）
- **AgentExecutor**：执行 Agent 的运行时
- **ReAct**：推理+行动的 Agent 模式
- **Self-Ask**：带有追问能力的 Agent

**核心规则**：
1. Agent 通过 LLM 判断应该使用哪个工具
2. 工具需要注册到 Agent 中
3. AgentExecutor 会循环执行直到完成或达到最大轮数
4. 可以自定义 Agent 类型来控制决策逻辑

**常见易错点**：
1. 工具的描述会影响 Agent 的选择
2. Agent 可能陷入循环，需要设置最大轮数
3. 某些工具需要安装额外的依赖

### 实战案例

#### 案例1：基础 Agent
```python
from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.tools import Tool

llm = ChatOpenAI(model="gpt-3.5-turbo")

# 定义工具
def search_function(query: str) -> str:
    """模拟搜索功能"""
    return f"搜索结果：关于{query}的信息..."

tools = [
    Tool.from_function(
        func=search_function,
        name="search",
        description="用于搜索信息。当需要查找具体信息时使用。"
    )
]

# 创建 Agent
prompt = ChatPromptTemplate.from_template(
    """你是一个助手。你可以使用工具来完成任务。
可用工具：search

问题：{input}
思考过程：{agent_scratchpad}"""
)

agent = create_openai_functions_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# 执行
result = agent_executor.invoke({"input": "Python的创始人是谁？"})
print(result["output"])
```

#### 案例2：使用内置 Agent 类型
```python
from langchain.agents import create_json_agent, create_conversational_agent
from langchain.agents.agent_toolkits import create_python_agent
from langchain_experimental.tools import PythonREPLTool

# 创建 Python Agent
llm = ChatOpenAI(model="gpt-3.5-turbo")

# Python Agent 可以执行代码
agent_executor = create_python_agent(
    llm=llm,
    tool=PythonREPLTool(),
    verbose=True
)

result = agent_executor.invoke(
    "请计算1到100的和，然后乘以2"
)
print(result["output"])
```

---

## 5. LlamaIndex 向量化知识库

### 知识点解析

**概念定义**：LlamaIndex 是另一个流行的 LLM 应用框架，专注于构建知识库和检索增强生成（RAG）。它提供了更专业的文档处理和索引能力。

**核心概念**：
- **Data Connector**：从各种数据源加载数据
- **Index**：将文档转换为可检索的结构
- **Query Engine**：执行检索和生成答案
- **Retriever**：决定如何检索相关文档
- **Node**：索引中的基本单元

**核心规则**：
1. LlamaIndex 更专注于索引和检索
2. 支持多种索引类型：Vector、List、Tree、Keyword
3. 可以与 LangChain 集成使用
4. 支持自定义节点解析器

**常见易错点**：
1. 文档需要先解析为节点才能索引
2. 不同的索引类型适用于不同查询场景
3. 检索结果需要通过 LLM 生成答案

### 实战案例

#### 案例1：构建简单知识库
```python
from llama_index import Document, VectorStoreIndex
from llama_index.llms import OpenAI

# 创建文档
documents = [
    Document(text="Python是一种高级编程语言。"),
    Document(text="Python支持多种编程范式。"),
    Document(text="人工智能是计算机科学的一个分支。")
]

# 创建索引
index = VectorStoreIndex.from_documents(documents)

# 创建查询引擎
query_engine = index.as_query_engine()

# 查询
response = query_engine.query("什么是Python？")
print(response)
```

#### 案例2：高级索引和检索
```python
from llama_index import Document, VectorStoreIndex, StorageContext
from llama_index.vector_stores import ChromaVectorStore
import chromadb

# 使用 Chroma 作为向量存储
chroma_client = chromadb.PersistentClient(path="./chroma_db")
chroma_collection = chroma_client.create_collection("my_docs")

vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
storage_context = StorageContext.from_defaults(vector_store=vector_store)

# 从文档创建索引
documents = [Document(text="...") for ...]
index = VectorStoreIndex.from_documents(
    documents,
    storage_context=storage_context
)

# 自定义检索
retriever = index.as_retriever(
    similarity_top_k=3,
    filters=None
)

# 检索
nodes = retriever.retrieve("查询内容")
for node in nodes:
    print(node.text, node.score)
```

#### 案例3：与 LangChain 集成
```python
from llama_index import VectorStoreIndex
from llama_index.llms import LangChainLLM
from langchain_openai import OpenAI
from langchain.chains import RetrievalQA

# 创建 LlamaIndex 索引
index = VectorStoreIndex.from_documents(documents)

# 获取检索器
retriever = index.as_retriever()

# 创建 LangChain QA 链
llm = OpenAI(model="gpt-3.5-turbo")
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=retriever
)

# 查询
result = qa_chain.invoke("我的问题")
print(result["result"])
```

---

## 6. 综合实战：构建 RAG 应用

### 实战案例

```python
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings

# ========== 1. 加载文档 ==========
loader = TextLoader("document.txt")
documents = loader.load()

# ========== 2. 分割文档 ==========
text_splitter = CharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)
splits = text_splitter.split_documents(documents)

# ========== 3. 创建向量存储 ==========
vectorstore = FAISS.from_documents(
    documents=splits,
    embedding=OpenAIEmbeddings()
)

# ========== 4. 创建检索器 ==========
retriever = vectorstore.as_retriever()

# ========== 5. 创建 QA 链 ==========
llm = ChatOpenAI(model="gpt-3.5-turbo")

system_prompt = """你是一个专业的问答助手。
使用以下上下文来回答用户的问题。
如果无法从上下文中找到答案，请明确告知。

Context:
{context}"""

prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    ("human", "{input}")
])

question_answer_chain = create_stuff_documents_chain(llm, prompt)
rag_chain = create_retrieval_chain(retriever, question_answer_chain)

# ========== 6. 执行查询 ==========
result = rag_chain.invoke({"input": "你的问题是什么？"})
print(result["answer"])
```

---

## 7. 常见问题和最佳实践

### 常见问题

1. **API 密钥问题**
   - 确保设置 `OPENAI_API_KEY` 环境变量
   - 或在初始化时显式传递 `openai_api_key`

2. **Token 限制**
   - 使用摘要记忆减少历史记录
   - 文档分割避免超过上下文限制
   - 使用 `max_tokens` 限制输出长度

3. **响应速度**
   - 考虑使用流式响应 `.stream()`
   - 批量处理减少 API 调用
   - 缓存常用结果

### 最佳实践

1. **提示词工程**
   - 使用结构化提示词模板
   - 提供清晰的指令和示例
   - 分离系统提示和用户输入

2. **错误处理**
   - 添加重试机制
   - 设置超时
   - 优雅降级

3. **性能优化**
   - 合理选择检索策略
   - 使用缓存
   - 异步处理

4. **安全性**
   - 不在代码中硬编码 API 密钥
   - 验证用户输入
   - 限制输出长度