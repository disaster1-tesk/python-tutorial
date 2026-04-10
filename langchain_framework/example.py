# LangChain 示例代码

# ========== 1. 基础 LLM 调用 ==========
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage

# 初始化 Chat 模型
llm = ChatOpenAI(
    model="gpt-3.5-turbo",
    temperature=0.7,
    max_tokens=1000,
    openai_api_key="your-api-key"
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

# ========== 2. 使用提示词模板 ==========
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

# ========== 3. 输出结构化数据 ==========
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
print(result)


# ========== 4. LCEL 链式调用 ==========
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


# ========== 5. 对话记忆 ==========
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
print(response2["text"])


# ========== 6. Agent 工具调用 ==========
from langchain.agents import AgentExecutor, create_openai_functions_agent
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


# ========== 7. RAG 完整示例 ==========
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings

# 模拟文档内容
documents = [
    "Python是一种高级编程语言，由Guido van Rossum创建。",
    "Python支持多种编程范式，包括面向对象、函数式和过程式编程。",
    "人工智能是计算机科学的一个分支，致力于开发智能机器。",
    "机器学习是人工智能的一个子领域，专注于从数据中学习。",
    "深度学习是机器学习的一个分支，使用神经网络模型。"
]

# 分割文档
text_splitter = CharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)

from langchain.docstore.document import Document
docs = [Document(page_content=text) for text in documents]
splits = text_splitter.split_documents(docs)

# 创建向量存储（使用模拟嵌入）
print("创建向量索引...")
# 注意：实际使用时需要真实的 OpenAI API Key
# vectorstore = FAISS.from_documents(
#     documents=splits,
#     embedding=OpenAIEmbeddings()
# )
# retriever = vectorstore.as_retriever()

# 模拟检索结果
print("\n=== RAG 应用演示 ===")
print("用户问题: 什么是Python?")
print("检索到的相关内容:")
for doc in splits[:2]:
    print(f"  - {doc.page_content}")

print("\nLLM生成的回答:")
print("Python是一种高级编程语言，由Guido van Rossum创建。它支持多种编程范式，")
print("广泛应用于Web开发、数据科学、人工智能等领域。")


print("\n" + "="*50)
print("LangChain 示例完成")