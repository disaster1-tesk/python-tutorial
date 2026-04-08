# Python NLP 与大语言模型

## 1. 文本预处理

### 知识点解析

**概念定义**：NLP（Natural Language Processing，自然语言处理）是让计算机理解、生成和处理人类语言的技术。文本预处理是所有 NLP 任务的第一步。

**核心概念**：
- **分词（Tokenization）**：将文本切分为词、子词或字符
- **清洗（Cleaning）**：去除噪声：特殊字符、HTML标签、停用词
- **标准化（Normalization）**：大小写转换、词干提取（Stemming）、词形还原（Lemmatization）
- **文本向量化**：将文本转换为数值表示

**核心规则**：
1. 中文分词需要专门的工具：jieba（简单）、pkuseg（准确）、HanLP（功能全）
2. 子词分词（BPE/WordPiece）是大模型标准：平衡词汇表大小和语义粒度
3. 停用词过滤需谨慎——某些任务（情感分析）中"不"、"没"等停用词很重要
4. 正则表达式是文本清洗的利器：`re.sub(r'[^\w\s]', '', text)`

### 实战案例

#### 案例1：中文文本预处理
```python
import re
import jieba
import jieba.posseg as pseg

# ========== 中文分词 ==========
text = "自然语言处理是人工智能领域的一个重要方向"
words = jieba.lcut(text)
print(f"分词结果: {words}")
# ['自然语言', '处理', '是', '人工智能', '领域', '的', '一个', '重要', '方向']

# ========== 带词性标注 ==========
for word, flag in pseg.cut(text):
    print(f"  {word} ({flag})")

# ========== 自定义词典 ==========
jieba.add_word("大语言模型")
jieba.load_userdict("custom_dict.txt")  # 从文件加载

# ========== 文本清洗 ==========
def clean_text(text: str) -> str:
    """文本清洗流水线"""
    # 去除HTML标签
    text = re.sub(r'<[^>]+>', '', text)
    # 去除URL
    text = re.sub(r'https?://\S+', '', text)
    # 去除特殊字符（保留中文、英文、数字）
    text = re.sub(r'[^\w\s\u4e00-\u9fff]', '', text)
    # 去除多余空白
    text = re.sub(r'\s+', ' ', text).strip()
    # 转小写
    text = text.lower()
    return text

# ========== 停用词过滤 ==========
def remove_stopwords(words, stopwords_path='stopwords.txt'):
    """去除停用词"""
    try:
        with open(stopwords_path, 'r', encoding='utf-8') as f:
            stopwords = set(line.strip() for line in f)
    except FileNotFoundError:
        stopwords = {'的', '了', '是', '在', '我', '有', '和', '就', '不', '人', '都', '一'}

    return [w for w in words if w not in stopwords and len(w) > 0]
```

#### 案例2：词频统计与 TF-IDF
```python
from collections import Counter
import math

def tf_idf(documents):
    """手动实现 TF-IDF"""
    vocab = set()
    for doc in documents:
        vocab.update(doc)
    vocab = sorted(vocab)
    vocab_index = {w: i for i, w in enumerate(vocab)}

    n_docs = len(documents)
    n_vocab = len(vocab)

    # 计算IDF
    idf = np.zeros(n_vocab)
    for i, word in enumerate(vocab):
        doc_count = sum(1 for doc in documents if word in doc)
        idf[i] = math.log(n_docs / (1 + doc_count)) + 1

    # 计算TF-IDF
    tfidf_matrix = np.zeros((n_docs, n_vocab))
    for doc_idx, doc in enumerate(documents):
        word_count = Counter(doc)
        total = len(doc)
        for word, count in word_count.items():
            tf = count / total
            tfidf_matrix[doc_idx, vocab_index[word]] = tf * idf[vocab_index[word]]

    return tfidf_matrix, vocab

# 使用示例
docs = [
    ["自然", "语言", "处理", "很有", "趣"],
    ["深度", "学习", "改变", "了", "自然", "语言", "处理"],
    ["机器", "学习", "和", "深度", "学习", "都是", "人工智能"],
]
matrix, vocab = tf_idf(docs)
```

---

## 2. 词嵌入（Word Embedding）

### 知识点解析

**核心概念**：
- **Word2Vec**：CBOW（上下文预测中心词）和 Skip-gram（中心词预测上下文）
- **GloVe**：基于全局词共现矩阵的词向量
- **FastText**：考虑子词（subword）信息，能处理未登录词（OOV）
- **上下文相关嵌入**：ELMo、BERT 等动态词向量，同一词在不同语境有不同向量

**核心规则**：
1. 词向量的维度通常是 100-300 维
2. 语义相近的词在向量空间中距离近：`cosine_similarity(king-man+woman, queen) ≈ 1`
3. 预训练词向量可以直接加载使用，无需从头训练
4. 静态词向量（Word2Vec）vs 动态词向量（BERT）：后者效果更好但计算量大

---

## 3. HuggingFace Transformers 生态

### 知识点解析

**概念定义**：HuggingFace 是当前 AI 领域最重要的开源社区之一，其 Transformers 库提供了数万个预训练模型的统一接口。

**核心概念**：
- **Pipeline**：一行代码调用预训练模型（分类、生成、问答、翻译等）
- **AutoModel/AutoTokenizer**：自动加载对应架构的模型和分词器
- **Model Hub**：模型仓库，搜索、下载、分享预训练模型
- **Datasets**：数据集库，一行代码加载公共数据集
- **Trainer API**：训练、评估、推理的高层接口

**核心规则**：
1. 基本用法：`pipeline("task", model="model_name")` 即可使用
2. 分词器与模型必须匹配：同一模型的 tokenizer 和 model 一起使用
3. `return_tensors="pt"` 返回 PyTorch Tensor，`padding=True` 对齐序列长度
4. 模型微调时设置 `requires_grad=False` 冻结不需要训练的层

### 实战案例

#### 案例1：Pipeline 快速使用
```python
from transformers import pipeline

# ========== 文本分类 ==========
classifier = pipeline("sentiment-analysis", model="uer/roberta-base-finetuned-jd-binary-chinese")
result = classifier("这个产品质量非常好，推荐购买！")
print(f"情感分析: {result}")
# [{'label': 'positive', 'score': 0.98}]

# ========== 文本生成 ==========
generator = pipeline("text-generation", model="uer/gpt2-chinese-cluecorpussmall")
result = generator("人工智能的未来是", max_length=50, num_return_sequences=1)
print(f"文本生成: {result[0]['generated_text']}")

# ========== 命名实体识别 ==========
ner = pipeline("ner", model="uer/roberta-base-finetuned-cluener2020-chinese")
result = ner("张三在北京清华大学学习计算机科学")
for entity in result:
    print(f"  实体: {entity['word']}, 类型: {entity['entity']}, 置信度: {entity['score']:.4f}")

# ========== 问答系统 ==========
qa = pipeline("question-answering", model="uer/roberta-base-finetuned-dureader-robust")
result = qa(question="什么是深度学习？", context="深度学习是机器学习的一个分支，它使用多层神经网络来模拟人脑的学习过程。")
print(f"答案: {result['answer']}")

# ========== 文本摘要 ==========
summarizer = pipeline("summarization", model="uer/pegasus-base-chinese")
result = summarizer("长文本...", max_length=50, min_length=10)
print(f"摘要: {result[0]['summary_text']}")
```

#### 案例2：AutoModel 微调
```python
from transformers import AutoTokenizer, AutoModelForSequenceClassification, Trainer, TrainingArguments
from datasets import load_dataset

# ========== 加载模型和分词器 ==========
model_name = "bert-base-chinese"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name, num_labels=2)

# ========== 数据预处理 ==========
def tokenize_function(examples):
    return tokenizer(examples["text"], padding="max_length", truncation=True, max_length=128)

dataset = load_dataset("csv", data_files={"train": "train.csv", "test": "test.csv"})
tokenized_dataset = dataset.map(tokenize_function, batched=True)

# ========== 训练配置 ==========
training_args = TrainingArguments(
    output_dir="./results",
    num_train_epochs=3,
    per_device_train_batch_size=16,
    per_device_eval_batch_size=32,
    learning_rate=2e-5,
    weight_decay=0.01,
    evaluation_strategy="epoch",
    save_strategy="epoch",
    load_best_model_at_end=True,
    logging_steps=100,
)

# ========== 训练 ==========
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_dataset["train"],
    eval_dataset=tokenized_dataset["test"],
)

trainer.train()

# ========== 保存模型 ==========
trainer.save_model("./my-finetuned-model")
tokenizer.save_pretrained("./my-finetuned-model")
```

---

## 4. 大语言模型（LLM）应用

### 知识点解析

**概念定义**：大语言模型（Large Language Model）是基于 Transformer Decoder 架构、在海量文本上预训练的生成式模型。代表模型包括 GPT 系列、LLaMA、ChatGLM、Qwen 等。

**核心概念**：
- **预训练 + 微调**：在海量文本上预训练语言能力，在任务数据上微调特定能力
- **Prompt Engineering**：通过设计输入提示来引导模型输出
- **RAG（检索增强生成）**：结合外部知识库检索 + LLM 生成
- **Fine-tuning**：全参数微调、LoRA/QLoRA（参数高效微调）
- **Token**：模型处理文本的基本单位，不同模型有不同的分词方式

**核心规则**：
1. LLM 是生成式模型：输入 prompt，自回归地逐个 token 生成输出
2. `temperature` 控制随机性：0=确定性，1=正常，>1=更随机
3. `max_tokens` 控制生成长度，`top_p` 控制核采样范围
4. LoRA 微调：只训练低秩适配器（通常 <1% 参数），显存需求大幅降低
5. RAG 流程：用户问题 → 检索相关文档 → 拼接为 prompt → LLM 生成回答

### 实战案例

#### 案例1：OpenAI API / 兼容接口调用
```python
# 使用 OpenAI 兼容的 API（适用于各种国产大模型）
from openai import OpenAI

client = OpenAI(
    api_key="your-api-key",
    base_url="https://api.example.com/v1"  # 替换为实际的 API 地址
)

# ========== 基本对话 ==========
response = client.chat.completions.create(
    model="your-model-name",
    messages=[
        {"role": "system", "content": "你是一个有帮助的助手。"},
        {"role": "user", "content": "用Python写一个快速排序。"},
    ],
    temperature=0.7,
    max_tokens=1024,
)
print(response.choices[0].message.content)

# ========== 流式输出 ==========
stream = client.chat.completions.create(
    model="your-model-name",
    messages=[{"role": "user", "content": "解释什么是RAG"}],
    stream=True,
)
for chunk in stream:
    if chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end="", flush=True)
```

#### 案例2：RAG 检索增强生成
```python
"""
RAG（Retrieval-Augmented Generation）核心流程：
1. 文档分块（Chunking）
2. 向量化嵌入（Embedding）
3. 向量存储与检索
4. Prompt 组装
5. LLM 生成
"""

import numpy as np
from typing import List

# ========== 第1步：文档分块 ==========
def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50) -> List[str]:
    """将长文本按字符数分块，带重叠"""
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size - overlap
    return chunks

# ========== 第2步：计算文本相似度 ==========
def cosine_similarity(vec_a, vec_b):
    """余弦相似度"""
    return np.dot(vec_a, vec_b) / (np.linalg.norm(vec_a) * np.linalg.norm(vec_b))

# ========== 第3步：简化版向量检索 ==========
class SimpleVectorStore:
    """简化版向量数据库"""

    def __init__(self):
        self.documents = []
        self.embeddings = []

    def add(self, doc: str, embedding: np.ndarray):
        self.documents.append(doc)
        self.embeddings.append(embedding)

    def search(self, query_embedding: np.ndarray, top_k: int = 3) -> List[tuple]:
        """检索最相关的文档"""
        scores = [
            (doc, cosine_similarity(query_embedding, emb))
            for doc, emb in zip(self.documents, self.embeddings)
        ]
        return sorted(scores, key=lambda x: x[1], reverse=True)[:top_k]

# ========== 第4步：组装 RAG Prompt ==========
def build_rag_prompt(query: str, retrieved_docs: List[str]) -> str:
    """组装带检索结果的 Prompt"""
    context = "\n\n".join([f"【参考资料{i+1}】\n{doc}" for i, doc in enumerate(retrieved_docs)])

    prompt = f"""请根据以下参考资料回答用户问题。如果资料中没有相关信息，请如实告知。

{context}

用户问题：{query}

请给出准确、完整的回答："""
    return prompt

# ========== 第5步：完整 RAG 流程 ==========
def rag_pipeline(query: str, vector_store: SimpleVectorStore, llm_client):
    """完整的 RAG 流程"""
    # 1. 查询向量化（实际中用 embedding 模型）
    query_embedding = np.random.randn(768)  # 模拟

    # 2. 检索相关文档
    results = vector_store.search(query_embedding, top_k=3)
    retrieved_docs = [doc for doc, score in results]

    # 3. 组装 prompt
    prompt = build_rag_prompt(query, retrieved_docs)

    # 4. 调用 LLM 生成
    response = llm_client.chat.completions.create(
        model="your-model",
        messages=[{"role": "user", "content": prompt}],
    )

    return response.choices[0].message.content
```

#### 案例3：Prompt Engineering 技巧
```python
# ========== 1. 零样本（Zero-shot）==========
prompt_zero_shot = """请将以下英文翻译为中文：
Hello, how are you?"""

# ========== 2. 少样本（Few-shot）==========
prompt_few_shot = """请判断以下评论的情感倾向。

评论：这个手机很好用 → 正面
评论：质量太差了，退货 → 负面
评论：一般般吧，还行 → 中性
评论：超出预期，非常满意！→"""

# ========== 3. 角色扮演 ==========
prompt_role = """你是一位资深的Python架构师，拥有10年大型项目经验。
请为我设计一个电商系统的用户认证模块，要求：
1. 支持JWT和OAuth2.0
2. 包含密码加密和防暴力破解
3. 给出完整的代码结构和关键实现"""

# ========== 4. 思维链（Chain-of-Thought）==========
prompt_cot = """请一步步思考并解决以下问题：

一个水池有两个进水管和一个出水管。A管单独注满需要6小时，B管单独注满需要8小时，
出水管单独排空需要12小时。如果三管同时打开，多久能注满水池？

请一步步展示你的推理过程。"""

# ========== 5. 结构化输出 ==========
prompt_structured = """请从以下文本中提取信息，以JSON格式输出：
{
  "name": "人名",
  "age": "年龄",
  "skills": ["技能列表"],
  "education": "学历"
}

文本：张三今年28岁，毕业于北京大学计算机系，擅长Python、Java和深度学习。"""

# ========== 6. 系统提示词最佳实践 ==========
system_prompt = """## 角色
你是一个专业的技术文档助手。

## 规则
1. 回答要准确、简洁、有代码示例
2. 不确定的信息要明确标注
3. 优先使用 Python 代码示例
4. 按Markdown格式组织回答

## 输出格式
- 使用标题层级组织内容
- 代码使用代码块并标注语言
- 重要概念加粗显示"""
```

---

## 5. LangChain 框架

### 知识点解析

**概念定义**：LangChain 是构建 LLM 应用的框架，提供链式调用、Agent、记忆、工具集成等抽象。

**核心概念**：
- **Chain**：将多个操作串联为工作流
- **Agent**：让 LLM 自主决定使用哪些工具
- **Memory**：对话历史的记忆管理
- **Tool**：让 LLM 调用外部工具（搜索、计算、数据库查询等）

### 实战案例

```python
# LangChain 基本用法（概念示例）
"""
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# 1. 创建 LLM
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

# 2. 创建 Prompt 模板
prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个Python编程专家。"),
    ("user", "{input}")
])

# 3. 创建 Chain
chain = prompt | llm | StrOutputParser()

# 4. 调用
result = chain.invoke({"input": "解释什么是装饰器"})
print(result)

# ========== LangChain Agent ==========
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain.tools import tool

@tool
def search_web(query: str) -> str:
    \"\"\"搜索网络获取最新信息\"\"\"
    # 实际接入搜索API
    return f"搜索结果: {query}"

@tool
def calculate(expression: str) -> str:
    \"\"\"计算数学表达式\"\"\"
    try:
        return str(eval(expression))
    except:
        return "计算错误"

tools = [search_web, calculate]
agent = create_tool_calling_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools)
"""
```

---

## 6. 向量数据库

### 知识点解析

**核心概念**：
- **向量数据库**：存储和检索高维向量的专用数据库
- **Embedding 模型**：将文本转换为向量表示
- **相似度检索**：ANN（近似最近邻）算法快速搜索

**常用工具**：
1. **ChromaDB**：轻量级，适合开发和小规模应用
2. **FAISS**：Meta 开源，纯计算库，性能极高
3. **Milvus**：分布式，适合大规模生产环境
4. **Weaviate**：自带向量化和混合搜索
5. **Pinecone**：全托管云服务

```python
# ChromaDB 示例
"""
import chromadb
from chromadb.utils import embedding_functions

# 创建客户端
client = chromadb.PersistentClient(path="./chroma_db")

# 使用嵌入函数
embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
)

# 创建集合
collection = client.get_or_create_collection(
    name="documents",
    embedding_function=embedding_fn
)

# 添加文档
collection.add(
    documents=["Python是一种解释型编程语言", "Java是一种编译型编程语言"],
    ids=["doc1", "doc2"],
    metadatas=[{"source": "wiki"}, {"source": "wiki"}]
)

# 查询
results = collection.query(
    query_texts=["什么是Python"],
    n_results=2
)
"""
```

## 学习建议

1. **先学文本预处理**：分词、清洗、向量化是所有 NLP 任务的基础
2. **HuggingFace 是必备工具**：Pipeline 快速体验，AutoModel 深度使用
3. **掌握 Prompt Engineering**：不用训练模型就能大幅提升效果
4. **RAG 是当前最实用的 LLM 应用方式**：学会检索+生成的组合
5. **关注国产大模型**：ChatGLM、Qwen、DeepSeek、Kimi 等都有很好的中文支持
6. **向量数据库是 AI 应用的基础设施**：理解 Embedding + 检索的原理
