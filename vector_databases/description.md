# 向量数据库

## 1. 向量数据库基础

### 知识点解析

**概念定义**：向量数据库是专门用于存储和检索高维向量数据的数据库系统。在 AI 应用中，文本、图像、音频等数据会被转换为向量嵌入（Embedding），向量数据库能够高效地完成相似性搜索。

**核心概念**：
- **向量嵌入（Embedding）**：将原始数据（文本、图像等）转换为固定维度的数值向量
- **相似度度量**：常用的度量方式包括余弦相似度（Cosine Similarity）、欧氏距离（Euclidean Distance）、点积（Dot Product）
- **索引算法**：HNSW、IVF、PQ 等用于加速向量检索
- **向量维度**：嵌入向量的维度，通常由 embedding 模型决定

**核心规则**：
1. 向量数据库的核心操作：增删改查（CRUD）和相似性搜索
2. 选择合适的 embedding 模型直接影响搜索质量
3. 向量维度越高，存储和计算成本越大
4. 索引类型影响搜索速度和精度

**常见易错点**：
1. 相似性搜索返回的是相似度最高的结果，而非精确匹配
2. 不同 embedding 模型生成的向量不能混用
3. 向量数据库不支持直接用作文本搜索，需要先转为向量
4. 批量写入比逐条写入效率高得多

### 实战案例

#### 案例1：使用 Chroma 向量数据库
```python
import chromadb
from chromadb.config import Settings

# 初始化客户端
client = chromadb.PersistentClient(
    path="./chroma_data",
    settings=Settings(anonymized_telemetry=False)
)

# 创建或获取集合
collection = client.get_or_create_collection(
    name="my_documents",
    metadata={"description": "文档向量库"}
)

# 添加向量数据
documents = [
    "Python是一种高级编程语言",
    "Java是一种面向对象编程语言",
    "人工智能是计算机科学的一个分支"
]

# 生成向量（实际使用 embedding 模型）
import numpy as np
embeddings = []
for i, doc in enumerate(documents):
    # 简单的模拟向量，实际使用 OpenAI 或其他 embedding 模型
    embedding = np.random.rand(1536).tolist()
    embeddings.append(embedding)

collection.add(
    ids=[str(i) for i in range(len(documents))],
    documents=documents,
    embeddings=embeddings
)

# 相似性搜索
query = "编程语言"
query_embedding = np.random.rand(1536).tolist()

results = collection.query(
    query_embeddings=[query_embedding],
    n_results=2
)

print("搜索结果:")
for i, doc in enumerate(results["documents"][0]):
    print(f"  {i+1}. {doc}")
```

#### 案例2：使用 FAISS 向量数据库
```python
import numpy as np
from faiss import IndexFlatIP, IndexIVFFlat

# 创建向量数据 (1000个向量，维度为128)
d = 128  # 向量维度
n = 1000  # 向量数量
vectors = np.random.rand(n, d).astype('float32')

# 归一化（用于余弦相似度）
norms = np.linalg.norm(vectors, axis=1, keepdims=True)
vectors = vectors / norms

# 创建索引
index = IndexFlatIP(d)  # 内积索引

# 添加向量
index.add(vectors)

# 搜索
query = np.random.rand(1, d).astype('float32')
query = query / np.linalg.norm(query)

k = 5  # 返回前5个最相似的结果
distances, indices = index.search(query, k)

print("搜索结果:")
print("索引:", indices)
print("距离:", distances)
```

---

## 2. Chroma 实战

### 知识点解析

**概念定义**：Chroma 是一个开源的嵌入式向量数据库，专为 AI 应用设计，简化了向量存储和检索的流程。

**核心概念**：
- **Client**：连接向量数据库的客户端
- **Collection**：存储向量和相关数据的集合
- **Embedding Function**：将文本转换为向量的函数

**核心规则**：
1. Chroma 支持多种 embedding 函数，默认使用 sentence-transformers
2. 可以持久化到本地文件系统
3. 支持过滤和元数据搜索

### 实战案例

#### 案例1：完整 RAG 流程
```python
import chromadb
from chromadb.config import Settings

# ========== 1. 初始化 ==========
client = chromadb.PersistentClient(path="./chroma_db")

# ========== 2. 创建集合 ==========
collection = client.get_or_create_collection(
    name="knowledge_base",
    metadata={"hnsw:space": "cosine"}  # 使用余弦相似度
)

# ========== 3. 添加文档 ==========
# 模拟文档
docs = [
    "Python的环境管理工具包括virtualenv、conda、pipenv等",
    "pip是Python的官方包管理工具",
    "conda既可以管理Python包，也可以管理其他语言的包",
    "Docker是一种容器化技术，用于应用部署",
    "Kubernetes是容器编排平台，用于管理容器集群"
]

# 模拟 embeddings
import numpy as np
embeddings = [np.random.rand(1536).tolist() for _ in docs]

collection.add(
    ids=[str(i) for i in range(len(docs))],
    documents=docs,
    embeddings=embeddings,
    metadatas=[{"id": i} for i in range(len(docs))]
)

# ========== 4. 搜索 ==========
query = "Python包管理工具"
query_embedding = np.random.rand(1536).tolist()

results = collection.query(
    query_embeddings=[query_embedding],
    n_results=3
)

print("查询:", query)
print("\n检索结果:")
for i, (doc, distance) in enumerate(zip(
    results["documents"][0],
    results["distances"][0]
)):
    print(f"{i+1}. {doc} (相似度: {1-distance:.4f})")

# ========== 5. 删除操作 ==========
# 删除指定ID的文档
# collection.delete(ids=["0"])

# 清空集合
# collection.delete(where={})
```

---

## 3. Pinecone 向量数据库

### 知识点解析

**概念定义**：Pinecone 是一个云原生的向量数据库服务，提供托管的向量存储和检索服务，适合大规模生产环境。

**核心概念**：
- **Index**：向量索引，核心存储单元
- **Namespace**：用于隔离索引内的数据
- **Upsert**：更新或插入操作
- **Serverless/Managed**：托管服务模式

**核心规则**：
1. Pinecone 是云服务，需要 API 密钥
2. 支持多种索引类型：pod-based 和 serverless
3. 付费版支持更多高级功能

### 实战案例

#### 案例1：Pinecone 基础操作
```python
from pinecone import Pinecone, ServerlessSpec
import time

# ========== 1. 初始化 ==========
pc = Pinecone(api_key="your-api-key")

# ========== 2. 创建索引 ==========
index_name = "my-index"

# 检查索引是否存在，不存在则创建
if index_name not in pc.list_indexes().names():
    pc.create_index(
        name=index_name,
        dimension=1536,
        metric="cosine",
        spec=ServerlessSpec(
            cloud="aws",
            region="us-west-2"
        )
    )
    # 等待索引就绪
    while not pc.describe_index(index_name).status['ready']:
        time.sleep(1)

# ========== 3. 连接索引 ==========
index = pc.Index(index_name)

# ========== 4. 插入向量 ==========
import numpy as np

vectors = []
for i in range(10):
    vector = np.random.rand(1536).tolist()
    vectors.append({
        "id": f"vec-{i}",
        "values": vector,
        "metadata": {"index": i}
    })

index.upsert(vectors=vectors, namespace="ns1")

# ========== 5. 查询 ==========
query_vector = np.random.rand(1536).tolist()
results = index.query(
    vector=query_vector,
    top_k=3,
    namespace="ns1",
    include_metadata=True
)

print("查询结果:")
for match in results['matches']:
    print(f"ID: {match['id']}, Score: {match['score']}, Metadata: {match['metadata']}")
```

---

## 4. 向量检索高级技巧

### 知识点解析

**核心概念**：
- **Hybrid Search**：结合关键词和向量搜索
- **Filtering**：基于元数据过滤搜索结果
- **Re-ranking**：对初步结果进行重排序

**核心规则**：
1. 元数据过滤可以缩小搜索范围，提高精度
2. 分层检索：第一层快速筛选，第二层精细排序
3. 批量操作比单条操作效率高

### 实战案例

#### 案例1：带过滤的搜索
```python
import chromadb

client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_or_create_collection("products")

# 添加产品数据
products = [
    {"id": "1", "name": "iPhone 15", "category": "手机", "price": 5999},
    {"id": "2", "name": "MacBook Pro", "category": "电脑", "price": 14999},
    {"id": "3", "name": "iPad Pro", "category": "平板", "price": 4999},
    {"id": "4", "name": "AirPods Pro", "category": "耳机", "price": 1899},
    {"id": "5", "name": "iPhone SE", "category": "手机", "price": 3499},
]

import numpy as np
for p in products:
    # 模拟向量
    collection.add(
        ids=[p["id"]],
        documents=[p["name"]],
        embeddings=[np.random.rand(1536).tolist()],
        metadatas=[{"category": p["category"], "price": p["price"]}]
    )

# 搜索：价格小于5000的电子产品
query_embedding = np.random.rand(1536).tolist()

results = collection.query(
    query_embeddings=[query_embedding],
    n_results=5,
    where={"price": {"$lt": 5000}},  # 价格小于5000
    include=["documents", "metadatas", "distances"]
)

print("筛选结果（价格 < 5000）:")
for doc, meta, dist in zip(
    results["documents"][0],
    results["metadatas"][0],
    results["distances"][0]
):
    print(f"  {doc} - {meta['category']} - ¥{meta['price']}")
```

---

## 5. 最佳实践与性能优化

### 最佳实践

1. **Embedding 模型选择**
   - 英文：text-embedding-ada-002、sentence-transformers
   - 中文：text-embedding-3-small、中文 RoBERTa

2. **索引优化**
   - 定期清理无效数据
   - 使用合适的索引参数
   - 监控查询延迟

3. **成本控制**
   - 使用批量操作
   - 选择合适的向量维度
   - 利用过滤减少搜索空间