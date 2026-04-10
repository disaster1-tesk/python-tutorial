# RAG 架构设计

## 1. RAG 基础概念

### 知识点解析

**概念定义**：RAG（Retrieval Augmented Generation，检索增强生成）是一种结合了信息检索和文本生成的技术架构。它通过从外部知识库中检索相关信息，来增强 LLM 的回答质量和准确性。

**核心价值**：
- **解决知识过时问题**：可以更新知识库而不需要重新训练模型
- **减少幻觉**：提供真实依据，减少模型编造答案
- **扩展知识范围**：让模型访问私有或专业领域知识
- **提高可解释性**：可以追溯答案来源

**核心流程**：
1. **索引阶段**：将文档切分为块，转换为向量，存储到向量数据库
2. **检索阶段**：根据用户问题检索最相关的文档块
3. **生成阶段**：将检索到的内容作为上下文，生成答案

**核心规则**：
1. 文档质量直接影响 RAG 效果
2. 块大小要合理（通常 500-1000 tokens）
3. 检索结果的相关性至关重要
4. 上下文窗口有限，需要筛选最重要内容

**常见易错点**：
1. 文档切分不合理导致关键信息被切断
2. 检索结果太多或太少
3. 提示词没有有效利用检索内容
4. 忽略来源验证和结果排序

### 实战案例

#### 案例1：基础 RAG 流程
```python
# ========== 完整 RAG 流程示例 ==========

# 1. 文档加载
from langchain_community.document_loaders import TextLoader

loader = TextLoader("knowledge.txt")
documents = loader.load()

# 2. 文档切分
from langchain.text_splitter import CharacterTextSplitter

splitter = CharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)
splits = splitter.split_documents(documents)

# 3. 向量化
from langchain_openai import OpenAIEmbeddings

embeddings = OpenAIEmbeddings()
vectorstore.add_documents(splits)

# 4. 检索
query = "什么是Python？"
retrieved_docs = vectorstore.similarity_search(query, k=3)

# 5. 生成
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

llm = ChatOpenAI(model="gpt-3.5-turbo")
prompt = ChatPromptTemplate.from_template(
    """基于以下文档回答问题。
如果文档中没有相关信息，请说明不知道。

文档：
{docs}

问题：{question}

回答："""
)

context = "\n\n".join([doc.page_content for doc in retrieved_docs])
answer = llm.invoke(prompt.format(docs=context, question=query))
print(answer.content)
```

---

## 2. 文档处理与索引优化

### 知识点解析

**核心概念**：
- **文档加载器**：从不同来源加载文档
- **文本切分器**：将文档切分为小块
- **向量化**：将文本转换为向量
- **索引策略**：优化检索效率

**核心规则**：
1. 根据文档类型选择合适的加载器
2. 块大小根据内容和检索需求调整
3. 重叠部分可以避免关键信息被切断
4. 元数据可以用于过滤和排序

### 实战案例

#### 案例1：多种文档格式处理
```python
from langchain_community.document_loaders import (
    TextLoader,           # TXT
    PyPDFLoader,         # PDF
    CSVLoader,           # CSV
    UnstructuredHTMLLoader,  # HTML
    DocxLoader          # Word
)

# PDF 文档
pdf_loader = PyPDFLoader("document.pdf")
pdf_docs = pdf_loader.load()

# Word 文档
docx_loader = DocxLoader("document.docx")
docx_docs = docx_loader.load()

# HTML 网页
html_loader = UnstructuredHTMLLoader("page.html")
html_docs = html_loader.load()
```

#### 案例2：智能文本切分
```python
from langchain.text_splitter import (
    CharacterTextSplitter,
    RecursiveCharacterTextSplitter,
    MarkdownTextSplitter,
    PythonCodeTextSplitter
)

# 通用文本
char_splitter = CharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)

# 递归切分（更智能）
recursive_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50,
    separators=["\n\n", "\n", " ", ""]
)

# Markdown 文档
markdown_splitter = MarkdownTextSplitter(
    chunk_size=500
)

# Python 代码
code_splitter = PythonCodeTextSplitter(
    chunk_size=200
)

# 根据内容类型选择合适的切分器
def get_splitter(file_type: str):
    splitters = {
        "txt": RecursiveCharacterTextSplitter(chunk_size=500),
        "md": MarkdownTextSplitter(chunk_size=500),
        "py": PythonCodeTextSplitter(chunk_size=200),
    }
    return splitters.get(file_type, RecursiveCharacterTextSplitter())
```

---

## 3. 检索策略优化

### 知识点解析

**核心概念**：
- **相似度度量**：余弦相似度、欧氏距离、点积
- **Top-K 检索**：返回最相似的 K 个结果
- **重排序**：对初步结果进行二次排序
- **混合检索**：结合关键词和向量检索

**核心规则**：
1. 根据场景选择相似度度量
2. K 值要合理，太少可能遗漏，太多可能引入噪声
3. 可以在检索后进行重排序
4. 混合检索可以提高召回率

### 实战案例

#### 案例1：优化检索参数
```python
# 基础检索
basic_results = vectorstore.similarity_search(query, k=3)

# 带分数的检索
scored_results = vectorstore.similarity_search_with_score(query, k=5)

# 过滤检索（基于元数据）
filtered_results = vectorstore.similarity_search(
    query,
    k=3,
    filter={"source": "important_doc"}
)

# 最大边际相关性检索（MMR）- 避免结果过于相似
mmr_results = vectorstore.max_marginal_relevance_search(
    query,
    k=3,
    fetch_k=10  # 从更多候选中选取多样性结果
)

print("=== 检索结果示例 ===")
for doc, score in scored_results:
    print(f"内容: {doc.page_content[:50]}...")
    print(f"相似度: {1-score:.4f}\n")
```

#### 案例2：重排序
```python
from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import CrossEncoderReranker
from langchain.cross_encoders import CrossEncoder

# 使用交叉编码器重排序
cross_encoder = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")

# 先进行向量检索
base_retriever = vectorstore.as_retriever(search_kwargs={"k": 10})

# 添加重排序
compressor = CrossEncoderReranker(
    model=cross_encoder,
    top_n=3
)

compression_retriever = ContextualCompressionRetriever(
    base_compressor=compressor,
    base_retriever=base_retriever
)

# 使用重排序后的检索器
results = compression_retriever.invoke("什么是Python？")
```

---

## 4. 生成优化

### 知识点解析

**核心概念**：
- **上下文压缩**：压缩检索到的文档
- **Stuff 文档链**：将所有文档塞入上下文
- **Map-Reduce**：先处理每个文档，再合并结果
- **Refine**：迭代优化答案

**核心规则**：
1. 根据文档数量和长度选择合适的链类型
2. 提示词要明确指示如何利用上下文
3. 可以添加来源标注增强可信度
4. 需要处理上下文超出限制的情况

### 实战案例

#### 案例1：不同类型的生成链
```python
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import (
    create_stuff_documents_chain,
    create_map_reduce_documents_chain
)

llm = ChatOpenAI(model="gpt-3.5-turbo")

# 方式1：Stuff（适合少量文档）
stuff_chain = create_stuff_documents_chain(llm, prompt)
rag_chain = create_retrieval_chain(retriever, stuff_chain)

# 方式2：Map-Reduce（适合大量文档）
map_prompt = ChatPromptTemplate.from_template(
    """总结以下文档的要点：
{doc}
要点："""
)
map_chain = create_map_reduce_documents_chain(llm, map_prompt)

reduce_prompt = ChatPromptTemplate.from_template(
    """合并以下要点，给出最终答案：
{docs}

最终答案："""
)
reduce_chain = create_stuff_documents_chain(llm, reduce_prompt)
map_reduce_rag = create_retrieval_chain(retriever, map_chain | reduce_chain)
```

#### 案例2：带来源标注的生成
```python
def generate_with_sources(query: str, retrieved_docs: list) -> dict:
    """生成带来源标注的答案"""
    
    # 构建上下文和来源
    context_parts = []
    sources = []
    
    for i, doc in enumerate(retrieved_docs):
        context_parts.append(f"[文档{i+1}] {doc.page_content}")
        source = doc.metadata.get("source", "未知来源")
        sources.append(f"文档{i+1}: {source}")
    
    context = "\n\n".join(context_parts)
    
    # 生成答案
    prompt = f"""基于以下文档回答问题。如果文档中没有相关信息，请说明不知道。

{context}

问题：{query}

回答时，请标注信息来源，例如【文档1】。"""

    answer = llm.invoke(prompt).content
    
    return {
        "answer": answer,
        "sources": sources
    }

result = generate_with_sources("Python有什么特点？", retrieved_docs)
print(result["answer"])
print("\n来源:", result["sources"])
```

---

## 5. RAG 架构变体

### 知识点解析

**核心概念**：
- **Parent Document RAG**：先检索小块，再检索完整文档
- **Self-RAG**：检索后自我评估相关性
- **HyDE**：假设性文档嵌入
- **Graph RAG**：图结构知识增强

### 实战案例

#### 案例1：Parent Document RAG
```python
from langchain.retrievers import ParentDocumentRetriever
from langchain.text_splitter import RecursiveCharacterTextSplitter

# 切分为小块
child_splitter = RecursiveCharacterTextSplitter(chunk_size=200)

# 切分为大块（父文档）
parent_splitter = RecursiveCharacterTextSplitter(chunk_size=1000)

# 创建检索器
retriever = ParentDocumentRetriever(
    vectorstore=vectorstore,
    docstore=InMemoryStore(),
    child_splitter=child_splitter,
    parent_splitter=parent_splitter
)

# 检索时会先找小块，再找到对应的父文档
results = retriever.invoke("Python基础")
```

---

## 6. RAG 最佳实践

### 性能优化技巧

1. **索引优化**
   - 定期更新索引
   - 清理无效数据
   - 监控索引大小

2. **检索优化**
   - 调整 K 值
   - 使用元数据过滤
   - 结合多种检索方式

3. **生成优化**
   - 优化提示词
   - 添加来源标注
   - 处理长上下文

4. **成本控制**
   - 使用更小的模型处理简单任务
   - 批量处理
   - 缓存常用结果

### 评估与监控

1. **检索质量指标**：召回率、精确率
2. **生成质量指标**：相关性、完整性
3. **系统性能指标**：延迟、吞吐量
4. **用户反馈**：满意度、重复查询率