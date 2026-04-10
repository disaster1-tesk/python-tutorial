# 向量数据库示例代码

# ========== 1. Chroma 基础操作 ==========
import chromadb
from chromadb.config import Settings

# 初始化客户端
client = chromadb.PersistentClient(
    path="./chroma_data",
    settings=Settings(anonymized_telemetry=False)
)

# 创建集合
collection = client.get_or_create_collection("demo")

# 添加数据
import numpy as np

documents = [
    "Python是一种高级编程语言",
    "Java是一种面向对象编程语言",
    "人工智能是计算机科学的一个分支",
    "机器学习是人工智能的子领域",
    "深度学习使用神经网络模型"
]

# 模拟 embeddings（实际使用 embedding 模型）
for i, doc in enumerate(documents):
    embedding = np.random.rand(1536).tolist()
    collection.add(
        ids=[str(i)],
        documents=[doc],
        embeddings=[embedding]
    )

# 相似性搜索
query_embedding = np.random.rand(1536).tolist()
results = collection.query(
    query_embeddings=[query_embedding],
    n_results=3
)

print("=== Chroma 向量搜索 ===")
for doc in results["documents"][0]:
    print(f"  - {doc}")

# ========== 2. 带元数据的向量搜索 ==========
import chromadb

client = chromadb.PersistentClient(path="./product_db")
collection = client.get_or_create_collection("products")

# 添加带元数据的产品
products = [
    {"id": "1", "name": "iPhone 15", "category": "手机", "price": 5999},
    {"id": "2", "name": "MacBook Pro", "category": "电脑", "price": 14999},
    {"id": "3", "name": "iPad Pro", "category": "平板", "price": 4999},
]

for p in products:
    collection.add(
        ids=[p["id"]],
        documents=[p["name"]],
        embeddings=[np.random.rand(1536).tolist()],
        metadatas=[{"category": p["category"], "price": p["price"]}]
    )

# 带过滤的搜索
results = collection.query(
    query_embeddings=[np.random.rand(1536).tolist()],
    n_results=5,
    where={"price": {"$lt": 6000}},
    include=["documents", "metadatas"]
)

print("\n=== 带过滤的搜索（价格 < 6000）===")
for doc, meta in zip(results["documents"][0], results["metadatas"][0]):
    print(f"  {doc} - ¥{meta['price']}")


# ========== 3. FAISS 基础操作 ==========
import numpy as np
from faiss import IndexFlatIP, IndexIVFFlat

# 创建测试数据
d = 128  # 向量维度
n = 1000  # 向量数量
vectors = np.random.rand(n, d).astype('float32')

# 归一化（余弦相似度）
norms = np.linalg.norm(vectors, axis=1, keepdims=True)
vectors = vectors / norms

# 创建索引
index = IndexFlatIP(d)
index.add(vectors)

# 搜索
query = np.random.rand(1, d).astype('float32')
query = query / np.linalg.norm(query)

k = 5
distances, indices = index.search(query, k)

print(f"\n=== FAISS 搜索 ===")
print(f"找到 {k} 个最相似的结果")
print(f"索引: {indices}")
print(f"相似度: {distances}")


# ========== 4. 批量操作 ==========
import chromadb

client = chromadb.PersistentClient(path="./batch_demo")
collection = client.get_or_create_collection("batch_test")

# 批量添加数据
n = 100
ids = [str(i) for i in range(n)]
documents = [f"文档 {i}" for i in range(n)]
embeddings = [np.random.rand(1536).tolist() for _ in range(n)]

# 批量添加（推荐）
collection.add(ids=ids, documents=documents, embeddings=embeddings)

print(f"\n=== 批量操作 ===")
print(f"已添加 {n} 条数据")

# 批量查询
query_embeddings = [np.random.rand(1536).tolist() for _ in range(5)]
results = collection.query(
    query_embeddings=query_embeddings,
    n_results=3
)

print(f"批量查询完成，返回 {len(results['ids'])} 组结果")


# ========== 5. 删除和更新 ==========
import chromadb

client = chromadb.PersistentClient(path="./update_demo")
collection = client.get_or_create_collection("update_test")

# 添加数据
collection.add(
    ids=["1", "2", "3"],
    documents=["文档A", "文档B", "文档C"],
    embeddings=[np.random.rand(1536).tolist() for _ in range(3)]
)

print("\n=== 删除和更新操作 ===")

# 删除指定ID
collection.delete(ids=["1"])
print("已删除 ID=1")

# 按条件删除
collection.delete(where={"category": "test"})

# 清空集合
# collection.delete(where={})

print("向量数据库操作示例完成")


print("\n" + "="*50)
print("向量数据库示例完成")