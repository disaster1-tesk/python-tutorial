"""
Python NLP 与大语言模型完整示例
演示内容：
1. 文本预处理：分词、清洗、停用词
2. 词频统计与 TF-IDF
3. 文本相似度计算
4. 自注意力机制演示
5. 简化版文本生成（RNN风格）
6. RAG 概念演示
7. Prompt Engineering 模板
"""

import numpy as np
import re
from collections import Counter
import math
import random

print("=" * 60)
print("Python NLP 与大语言模型完整示例")
print("=" * 60)

# ============================================================
# 1. 文本预处理
# ============================================================
print("\n【1. 文本预处理】")


# 简单中文分词（基于最大匹配算法）
class SimpleChineseTokenizer:
    """基于前向最大匹配的中文分词器"""

    def __init__(self, dict_path=None):
        self.dictionary = set()
        self.max_word_len = 5
        self._init_dictionary()

    def _init_dictionary(self):
        """初始化词典"""
        # 常用词汇
        words = [
            "自然", "自然语言", "语言", "处理", "人工", "智能", "人工智能",
            "机器", "学习", "机器学习", "深度", "深度学习", "神经网络",
            "大语言", "大语言模型", "模型", "训练", "数据", "文本",
            "向量", "嵌入", "注意力", "机制", "生成", "预训练", "微调",
            "重要", "一个", "方向", "技术", "应用", "开发", "领域",
            "中国", "北京", "大学", "研究", "科学", "计算机", "工程",
        ]
        self.dictionary = set(words)
        self.max_word_len = max(len(w) for w in self.dictionary)

    def cut(self, text: str) -> list:
        """前向最大匹配分词"""
        words = []
        i = 0
        while i < len(text):
            matched = False
            for length in range(min(self.max_word_len, len(text) - i), 1, -1):
                word = text[i:i + length]
                if word in self.dictionary:
                    words.append(word)
                    i += length
                    matched = True
                    break
            if not matched:
                words.append(text[i])
                i += 1
        return words


tokenizer = SimpleChineseTokenizer()

text1 = "自然语言处理是人工智能领域的一个重要方向"
text2 = "深度学习改变了自然语言处理的研究方向"
text3 = "大语言模型是人工智能的最新应用"

for text in [text1, text2, text3]:
    words = tokenizer.cut(text)
    print(f"  {text}")
    print(f"  → {words}")

# 文本清洗
def clean_text(text: str) -> str:
    """文本清洗"""
    text = re.sub(r'<[^>]+>', '', text)         # 去HTML标签
    text = re.sub(r'https?://\S+', '', text)     # 去URL
    text = re.sub(r'[^\w\s\u4e00-\u9fff]', '', text)  # 去特殊字符
    text = re.sub(r'\s+', ' ', text).strip()     # 去多余空白
    return text


dirty_text = "自然语言处理(NLP)是<a href='#'>AI</a>的核心技术！详见 https://example.com"
cleaned = clean_text(dirty_text)
print(f"\n  原文: {dirty_text}")
print(f"  清洗: {cleaned}")

# ============================================================
# 2. 词频统计与 TF-IDF
# ============================================================
print("\n\n【2. 词频统计与 TF-IDF】")

# 构建文档集
documents = [
    tokenizer.cut("自然语言处理是人工智能领域的一个重要方向"),
    tokenizer.cut("深度学习改变了自然语言处理的研究方向"),
    tokenizer.cut("大语言模型是人工智能的最新应用技术"),
    tokenizer.cut("机器学习和深度学习都是人工智能的研究方向"),
]

print(f"  文档集: {len(documents)} 篇文档")

# 词频统计
all_words = [w for doc in documents for w in doc]
word_freq = Counter(all_words)
print(f"\n  词频 Top 10:")
for word, count in word_freq.most_common(10):
    print(f"    {word}: {count}")

# TF-IDF 计算
vocab = sorted(set(all_words))
vocab_index = {w: i for i, w in enumerate(vocab)}
n_docs = len(documents)
n_vocab = len(vocab)

# IDF: log(N / (1 + df))
idf = np.zeros(n_vocab)
for i, word in enumerate(vocab):
    df = sum(1 for doc in documents if word in doc)
    idf[i] = math.log(n_docs / (1 + df)) + 1

# TF-IDF 矩阵
tfidf_matrix = np.zeros((n_docs, n_vocab))
for doc_idx, doc in enumerate(documents):
    word_count = Counter(doc)
    total = len(doc)
    for word, count in word_count.items():
        tf = count / total
        tfidf_matrix[doc_idx, vocab_index[word]] = tf * idf[vocab_index[word]]

# 找每篇文档的关键词
print(f"\n  各文档关键词 (TF-IDF Top 3):")
for doc_idx, doc in enumerate(documents):
    doc_tfidf = tfidf_matrix[doc_idx]
    top_indices = doc_tfidf.argsort()[-3:][::-1]
    keywords = [(vocab[i], doc_tfidf[i].round(3)) for i in top_indices if doc_tfidf[i] > 0]
    print(f"    文档{doc_idx + 1}: {keywords}")

# ============================================================
# 3. 文本相似度
# ============================================================
print("\n\n【3. 文本相似度计算】")


def cosine_similarity(vec_a, vec_b):
    """余弦相似度"""
    norm_a = np.linalg.norm(vec_a)
    norm_b = np.linalg.norm(vec_b)
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return np.dot(vec_a, vec_b) / (norm_a * norm_b)


def jaccard_similarity(set_a, set_b):
    """Jaccard 相似度"""
    intersection = len(set_a & set_b)
    union = len(set_a | set_b)
    return intersection / union if union > 0 else 0.0


print("  文档间 TF-IDF 余弦相似度:")
for i in range(n_docs):
    for j in range(i + 1, n_docs):
        sim = cosine_similarity(tfidf_matrix[i], tfidf_matrix[j])
        print(f"    文档{i+1} vs 文档{j+1}: {sim:.4f}")

print("\n  文档间 Jaccard 相似度:")
for i in range(n_docs):
    for j in range(i + 1, n_docs):
        sim = jaccard_similarity(set(documents[i]), set(documents[j]))
        print(f"    文档{i+1} vs 文档{j+1}: {sim:.4f}")

# ============================================================
# 4. 自注意力机制（文本场景）
# ============================================================
print("\n\n【4. 自注意力机制在文本中的应用】")


def softmax(x):
    """数值稳定的 Softmax"""
    exp_x = np.exp(x - np.max(x, axis=-1, keepdims=True))
    return exp_x / exp_x.sum(axis=-1, keepdims=True)


def scaled_dot_product_attention(Q, K, V, mask=None):
    """缩放点积注意力"""
    d_k = Q.shape[-1]
    scores = Q @ K.T / np.sqrt(d_k)

    if mask is not None:
        scores = scores + mask * (-1e9)

    attn_weights = softmax(scores)
    output = attn_weights @ V

    return output, attn_weights


# 示例：句子 "我 喜欢 深度 学习"
words = ["我", "喜欢", "深度", "学习"]
d_model = 4  # 嵌入维度

# 模拟词嵌入
embeddings = {
    "我": np.array([0.8, 0.1, 0.3, 0.2]),
    "喜欢": np.array([0.2, 0.9, 0.1, 0.5]),
    "深度": np.array([0.3, 0.2, 0.8, 0.4]),
    "学习": np.array([0.1, 0.3, 0.7, 0.9]),
}

X = np.array([embeddings[w] for w in words])  # (4, 4)

# 自注意力
output, attn_weights = scaled_dot_product_attention(X, X, X)

print(f"  输入词: {words}")
print(f"  注意力权重:")
for i, word in enumerate(words):
    attn_str = " ".join([f"{words[j]}:{attn_weights[i,j]:.3f}" for j in range(len(words))])
    print(f"    '{word}' 关注 → {attn_str}")

# 因果掩码（用于文本生成）
print(f"\n  因果掩码（生成模式，只能看前面的词）:")
seq_len = len(words)
causal_mask = np.triu(np.ones((seq_len, seq_len)), k=1)
_, causal_attn = scaled_dot_product_attention(X, X, X, mask=causal_mask)
for i, word in enumerate(words):
    attn_str = " ".join([
        f"{words[j]}:{causal_attn[i,j]:.3f}" if j <= i else f"{words[j]}:---"
        for j in range(len(words))
    ])
    print(f"    '{word}' 关注 → {attn_str}")

# ============================================================
# 5. 简化版文本生成
# ============================================================
print("\n\n【5. 简化版文本生成（N-gram语言模型）】")


class NGramLanguageModel:
    """N-gram 语言模型"""

    def __init__(self, n=2):
        self.n = n
        self.ngram_counts = Counter()
        self.context_counts = Counter()
        self.vocabulary = set()

    def train(self, corpus: list):
        """训练"""
        for sentence in corpus:
            tokens = list(sentence)
            self.vocabulary.update(tokens)

            for i in range(len(tokens) - self.n + 1):
                ngram = tuple(tokens[i:i + self.n])
                context = tuple(tokens[i:i + self.n - 1])
                self.ngram_counts[ngram] += 1
                self.context_counts[context] += 1

    def predict_next(self, context: tuple, top_k=3):
        """预测下一个词"""
        candidates = {}
        for ngram, count in self.ngram_counts.items():
            if ngram[:-1] == context:
                prob = count / self.context_counts[context]
                candidates[ngram[-1]] = prob

        sorted_candidates = sorted(candidates.items(), key=lambda x: x[1], reverse=True)
        return sorted_candidates[:top_k]

    def generate(self, start: str, max_length=20):
        """生成文本"""
        result = list(start)
        context = tuple(result[-(self.n - 1):])

        for _ in range(max_length - len(result)):
            predictions = self.predict_next(context)
            if not predictions:
                break
            # 带随机性的选择
            words, probs = zip(*predictions)
            next_word = random.choices(words, weights=probs, k=1)[0]
            result.append(next_word)
            context = tuple(result[-(self.n - 1):])

        return "".join(result)


# 训练语料
corpus = [
    "自然语言处理是人工智能的重要方向",
    "深度学习改变了人工智能的研究方向",
    "大语言模型是深度学习的最新应用",
    "人工智能的发展推动了大语言模型的进步",
    "自然语言处理需要深度学习的技术",
    "大语言模型需要大量的训练数据",
    "深度学习是人工智能的核心技术",
    "自然语言处理是大语言模型的基础",
]

model = NGramLanguageModel(n=3)
model.train(corpus)

# 预测
print(f"  词汇表大小: {len(model.vocabulary)}")
print(f"  N-gram 数量: {len(model.ngram_counts)}")

# 生成文本
random.seed(42)
print(f"\n  文本生成:")
for start in ["自然语言", "深度学习", "大语言"]:
    generated = model.generate(start, max_length=15)
    print(f"    '{start}' → '{generated}'")

# ============================================================
# 6. RAG 概念演示
# ============================================================
print("\n\n【6. RAG（检索增强生成）概念演示】")


class SimpleRAG:
    """简化版 RAG 系统"""

    def __init__(self):
        self.knowledge_base = []

    def add_document(self, doc: str, metadata: dict = None):
        """添加文档到知识库"""
        self.knowledge_base.append({
            "text": doc,
            "metadata": metadata or {},
            "tokens": tokenizer.cut(doc),
        })

    def retrieve(self, query: str, top_k: int = 2) -> list:
        """检索相关文档（基于词重叠）"""
        query_tokens = set(tokenizer.cut(query))

        scored_docs = []
        for doc in self.knowledge_base:
            doc_tokens = set(doc["tokens"])
            # Jaccard 相似度
            sim = jaccard_similarity(query_tokens, doc_tokens)
            scored_docs.append((doc, sim))

        scored_docs.sort(key=lambda x: x[1], reverse=True)
        return scored_docs[:top_k]

    def generate_answer(self, query: str) -> str:
        """生成回答"""
        retrieved = self.retrieve(query, top_k=2)
        context = "\n".join([f"[资料{i+1}] {doc['text']}" for i, (doc, _) in enumerate(retrieved)])

        prompt = f"""基于以下资料回答问题：

{context}

问题：{query}

回答："""

        # 模拟 LLM 回答（实际中调用 LLM API）
        print(f"  构建的 Prompt:")
        for line in prompt.split('\n'):
            print(f"    {line}")

        return f"根据检索到的资料，关于'{query}'的答案是综合以上信息得出的结论。"


# 创建知识库
rag = SimpleRAG()
rag.add_document("Python是一种解释型编程语言，由Guido van Rossum于1991年发布", {"source": "wiki"})
rag.add_document("PyTorch是Meta开发的深度学习框架，支持动态计算图", {"source": "docs"})
rag.add_document("Transformers架构由Google在2017年提出，是GPT和Bert的基础", {"source": "paper"})
rag.add_document("大语言模型通常基于Transformer Decoder架构，通过自回归方式生成文本", {"source": "tutorial"})

# 检索
print(f"  知识库文档数: {len(rag.knowledge_base)}")
query = "什么是Transformers架构"
retrieved = rag.retrieve(query)
print(f"\n  查询: '{query}'")
print(f"  检索结果:")
for doc, score in retrieved:
    print(f"    [{score:.2%}] {doc['text'][:50]}... (来源: {doc['metadata'].get('source', 'N/A')})")

print(f"\n  生成回答:")
rag.generate_answer(query)

# ============================================================
# 7. Prompt Engineering 模板
# ============================================================
print("\n\n【7. Prompt Engineering 技巧总结】")

prompt_techniques = [
    ("零样本（Zero-shot）", "直接给出任务描述，不加示例"),
    ("少样本（Few-shot）", "提供2-5个输入-输出示例"),
    ("角色扮演（Role-play）", "设定AI的身份和专业背景"),
    ("思维链（Chain-of-Thought）", "要求逐步推理，展示思考过程"),
    ("结构化输出", "指定输出格式（JSON/Markdown/表格）"),
    ("自我反思", "让AI检查和修正自己的回答"),
    ("多轮对话", "通过上下文维持对话连贯性"),
]

print(f"  {'技巧':25s} {'说明':35s}")
print(f"  {'-'*25} {'-'*35}")
for name, desc in prompt_techniques:
    print(f"  {name:25s} {desc}")

# Prompt 组装示例
system_prompt = """你是一位专业的 Python 技术讲师。

## 规则
1. 回答简洁准确，包含代码示例
2. 使用中文回答
3. 代码使用Markdown代码块格式

## 输出格式
- 先给出核心概念解释
- 再给出代码示例
- 最后给出注意事项"""

user_prompt = "请解释Python中的装饰器是什么"

full_prompt = f"System: {system_prompt}\n\nUser: {user_prompt}"
print(f"\n  完整 Prompt 示例:")
print(f"  {full_prompt}")

print("\n" + "=" * 60)
print("NLP 与大语言模型示例运行完毕！")
print("=" * 60)
