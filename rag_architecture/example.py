# RAG 架构示例代码

# ========== 1. 基础 RAG 流程 ==========
print("=== 基础 RAG 流程 ===\n")

# 模拟文档
documents = [
    "Python是一种高级编程语言，由Guido van Rossum创建。",
    "Python支持多种编程范式，包括面向对象、函数式和命令式编程。",
    "Python的语法简洁清晰，适合初学者学习。",
    "人工智能是计算机科学的一个分支，致力于开发智能机器。",
    "机器学习是人工智能的核心技术，让计算机从数据中学习。"
]

# 模拟文档切分（块）
chunks = []
for i, doc in enumerate(documents):
    chunks.append({
        "id": f"chunk_{i}",
        "content": doc,
        "source": f"doc_{i//2}.txt"
    })

print(f"文档切分结果：共 {len(chunks)} 个块")
for chunk in chunks:
    print(f"  - {chunk['id']}: {chunk['content'][:30]}...")

# 模拟向量化（实际使用 embedding 模型）
print("\n向量化：每个文本块转换为向量（省略）")

# 模拟向量检索
import random

def mock_search(query: str, chunks: list, k: int = 3) -> list:
    """模拟相似度搜索"""
    results = []
    for chunk in chunks:
        # 模拟相似度分数
        score = random.uniform(0.5, 1.0)
        results.append((chunk, score))
    
    # 按相似度排序，返回 top k
    results.sort(key=lambda x: x[1], reverse=True)
    return results[:k]

# 用户查询
query = "Python有什么特点？"
print(f"\n用户查询: {query}")

# 检索
retrieved = mock_search(query, chunks, k=2)
print("\n检索结果:")
for chunk, score in retrieved:
    print(f"  - {chunk['content']} (相似度: {score:.2f})")

# 模拟生成
print("\n生成答案:")
print(f"根据检索到的信息，{query}")
print("Python是一种高级编程语言，具有以下特点：")
print("1. 语法简洁清晰")
print("2. 支持多种编程范式")
print("3. 适合初学者学习")


# ========== 2. 文档切分示例 ==========
print("\n" + "="*50)
print("=== 文档切分示例 ===")

from langchain.text_splitter import RecursiveCharacterTextSplitter

# 模拟长文档
long_document = """
# Python 教程

## 第一章 简介
Python 是一种广泛使用的解释型、高级和通用的编程语言。

## 第二章 基础语法
Python 使用缩进来表示代码块，而不是使用大括号。

## 第三章 数据类型
Python 支持多种数据类型，包括数字、字符串、列表、字典等。
"""

# 创建切分器
splitter = RecursiveCharacterTextSplitter(
    chunk_size=100,
    chunk_overlap=20
)

# 切分文档
chunks = splitter.split_text(long_document)

print(f"\n切分结果：共 {len(chunks)} 个块")
for i, chunk in enumerate(chunks):
    print(f"\n块 {i+1}:")
    print(chunk[:80] + "...")


# ========== 3. 检索优化示例 ==========
print("\n" + "="*50)
print("=== 检索优化示例 ===")

# 带过滤的检索
def search_with_filter(chunks: list, query: str, k: int, source_filter: str = None) -> list:
    """带过滤的检索"""
    results = []
    for chunk in chunks:
        # 过滤
        if source_filter and chunk.get("source") != source_filter:
            continue
        
        score = random.uniform(0.5, 1.0)
        results.append((chunk, score))
    
    results.sort(key=lambda x: x[1], reverse=True)
    return results[:k]

# 添加来源信息
for chunk in chunks:
    chunk["source"] = "python_tutorial.txt"

# 测试过滤检索
print("\n过滤检索测试（仅从 python_tutorial.txt）：")
filtered_results = search_with_filter(chunks, "Python", k=2, source_filter="python_tutorial.txt")
for chunk, score in filtered_results:
    print(f"  - {chunk['content'][:40]}... (分数: {score:.2f})")


# ========== 4. 生成链示例 ==========
print("\n" + "="*50)
print("=== 生成链示例 ===")

# 模拟 LLM 生成
def mock_llm_generate(prompt: str) -> str:
    """模拟 LLM 生成"""
    if "Python" in prompt:
        return "Python是一种高级编程语言，语法简洁，易于学习。"
    elif "人工智能" in prompt:
        return "人工智能让机器具有人类智能。"
    return "根据提供的信息无法回答该问题。"

# Stuff 链：把所有上下文拼接
def stuff_generate(query: str, retrieved_chunks: list) -> str:
    context = "\n\n".join([c["content"] for c in retrieved_chunks])
    prompt = f"根据以下文档回答问题：\n\n{context}\n\n问题：{query}\n\n回答："
    return mock_llm_generate(prompt)

# Map-Reduce 链：先处理每个文档，再合并
def map_reduce_generate(query: str, chunks: list) -> str:
    # Map 阶段
    summaries = []
    for chunk in chunks:
        summary = f"文档摘要：{chunk['content'][:50]}..."
        summaries.append(summary)
    
    # Reduce 阶段
    combined = "\n".join(summaries)
    prompt = f"根据以下文档摘要回答问题：\n{combined}\n\n问题：{query}\n\n回答："
    return mock_llm_generate(prompt)

# 测试
retrieved_chunks = chunks[:3]
query = "Python是什么？"

print(f"\nStuff 链结果：")
print(f"  {stuff_generate(query, retrieved_chunks)}")

print(f"\nMap-Reduce 链结果：")
print(f"  {map_reduce_generate(query, retrieved_chunks)}")


# ========== 5. RAG 评估示例 ==========
print("\n" + "="*50)
print("=== RAG 评估指标 ===")

def evaluate_rag(query: str, retrieved_docs: list, generated_answer: str, ground_truth: str) -> dict:
    """评估 RAG 系统"""
    
    # 1. 检索指标：召回率
    relevant_docs = [d for d in retrieved_docs if "Python" in d["content"]]
    recall = len(relevant_docs) / max(len([d for d in retrieved_docs]), 1)
    
    # 2. 生成指标：答案相关性（简化模拟）
    relevance_score = random.uniform(0.7, 0.95)
    
    return {
        "recall": recall,
        "relevance": relevance_score,
        "answer_length": len(generated_answer)
    }

# 模拟评估
evaluation = evaluate_rag(
    query="Python是什么？",
    retrieved_docs=chunks[:3],
    generated_answer="Python是一种高级编程语言",
    ground_truth="Python是一种高级编程语言"
)

print("\n评估结果:")
print(f"  召回率: {evaluation['recall']:.2f}")
print(f"  相关性: {evaluation['relevance']:.2f}")
print(f"  答案长度: {evaluation['answer_length']} 字符")


print("\n" + "="*50)
print("RAG 架构示例完成")