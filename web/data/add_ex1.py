import json

with open('exercises.json', 'r', encoding='utf-8') as f:
    exercises = json.load(f)

batch1 = [
    # ---- langchain_framework ----
    {"id": "ex_langchain_001", "module": "langchain_framework", "title": "LangChain 安装与基础", "difficulty": "easy", "points": 10,
     "description": "使用 LangChain 创建一个简单的提示模板并格式化",
     "starter_code": "from langchain.prompts import PromptTemplate\n\n# 创建提示模板\ntemplate = \"请用中文介绍 {topic}\"\n# 创建 PromptTemplate 对象\n# 格式化模板",
     "solution": "from langchain.prompts import PromptTemplate\n\ntemplate = \"请用中文介绍 {topic}\"\nprompt = PromptTemplate(template=template, input_variables=[\"topic\"])\nresult = prompt.format(topic=\"Python 编程\")\nprint(result)",
     "tags": ["LangChain", "PromptTemplate"]},

    {"id": "ex_langchain_002", "module": "langchain_framework", "title": "消息类型使用", "difficulty": "easy", "points": 10,
     "description": "使用 LangChain 的消息类型构建对话",
     "starter_code": "from langchain.schema import HumanMessage, AIMessage, SystemMessage\n\n# 创建一组对话消息\nmessages = [\n    # system 消息\n    # human 消息\n    # ai 消息\n]\nfor msg in messages:\n    print(type(msg).__name__, ':', msg.content)",
     "solution": "from langchain.schema import HumanMessage, AIMessage, SystemMessage\n\nmessages = [\n    SystemMessage(content='你是一个 Python 教学助手'),\n    HumanMessage(content='什么是列表推导式？'),\n    AIMessage(content='列表推导式是一种简洁的构建列表的语法。')\n]\nfor msg in messages:\n    print(type(msg).__name__, ':', msg.content)",
     "tags": ["LangChain", "消息"]},

    {"id": "ex_langchain_003", "module": "langchain_framework", "title": "OutputParser 使用", "difficulty": "medium", "points": 15,
     "description": "使用 StrOutputParser 解析模型输出",
     "starter_code": "# 模拟 LangChain 输出解析器的用法\nclass MockModel:\n    def invoke(self, prompt):\n        return type('obj', (object,), {'content': f'回答: {prompt}'})()\n\nclass StrOutputParser:\n    def invoke(self, model_output):\n        # 提取内容\n        pass\n\n# 组合使用",
     "solution": "class MockModel:\n    def invoke(self, prompt):\n        return type('obj', (object,), {'content': f'回答: {prompt}'})()\n\nclass StrOutputParser:\n    def invoke(self, model_output):\n        return model_output.content\n\nmodel = MockModel()\nparser = StrOutputParser()\n\nresult = model.invoke('Python 是什么？')\noutput = parser.invoke(result)\nprint(output)",
     "tags": ["LangChain", "OutputParser"]},

    {"id": "ex_langchain_004", "module": "langchain_framework", "title": "Chain 链接", "difficulty": "medium", "points": 15,
     "description": "实现一个简单的 Chain，将提示模板和模型链接起来",
     "starter_code": "# 模拟 LangChain Chain\nclass SimpleChain:\n    def __init__(self, prompt, model):\n        self.prompt = prompt\n        self.model = model\n    \n    def invoke(self, inputs):\n        # 格式化提示并调用模型\n        pass",
     "solution": "class MockPrompt:\n    def __init__(self, template):\n        self.template = template\n    def format(self, **kwargs):\n        result = self.template\n        for k, v in kwargs.items():\n            result = result.replace('{' + k + '}', str(v))\n        return result\n\nclass MockModel:\n    def invoke(self, text):\n        return f'[模型回答] {text}'\n\nclass SimpleChain:\n    def __init__(self, prompt, model):\n        self.prompt = prompt\n        self.model = model\n    \n    def invoke(self, inputs):\n        formatted = self.prompt.format(**inputs)\n        return self.model.invoke(formatted)\n\nchain = SimpleChain(\n    MockPrompt('请介绍{topic}'),\n    MockModel()\n)\nresult = chain.invoke({'topic': 'Python'})\nprint(result)",
     "tags": ["LangChain", "Chain"]},

    {"id": "ex_langchain_005", "module": "langchain_framework", "title": "Memory 记忆", "difficulty": "medium", "points": 15,
     "description": "实现对话记忆功能，保存并加载历史对话",
     "starter_code": "class ConversationMemory:\n    def __init__(self):\n        self.history = []\n    \n    def add(self, role, content):\n        # 添加消息\n        pass\n    \n    def get_history(self):\n        # 返回历史\n        pass\n    \n    def clear(self):\n        # 清空历史\n        pass",
     "solution": "class ConversationMemory:\n    def __init__(self):\n        self.history = []\n    \n    def add(self, role, content):\n        self.history.append({'role': role, 'content': content})\n    \n    def get_history(self):\n        return self.history\n    \n    def get_context(self):\n        return '\\n'.join([f\"{m['role']}: {m['content']}\" for m in self.history])\n    \n    def clear(self):\n        self.history = []\n\nmemory = ConversationMemory()\nmemory.add('user', '你好，介绍一下 Python')\nmemory.add('assistant', 'Python 是一种高级编程语言')\nmemory.add('user', '它有什么特点？')\n\nprint('对话历史:')\nprint(memory.get_context())\nprint('\\n历史条数:', len(memory.get_history()))",
     "tags": ["LangChain", "Memory"]},

    {"id": "ex_langchain_006", "module": "langchain_framework", "title": "工具定义", "difficulty": "medium", "points": 15,
     "description": "定义 LangChain 格式的工具函数",
     "starter_code": "# 定义工具类\nclass Tool:\n    def __init__(self, name, description, func):\n        self.name = name\n        self.description = description\n        self.func = func\n    \n    def run(self, input_str):\n        # 调用工具\n        pass",
     "solution": "class Tool:\n    def __init__(self, name, description, func):\n        self.name = name\n        self.description = description\n        self.func = func\n    \n    def run(self, input_str):\n        return self.func(input_str)\n\n# 定义工具\ndef search_tool(query):\n    return f'搜索结果: {query}'\n\ndef calc_tool(expr):\n    try:\n        return str(eval(expr))\n    except:\n        return '计算错误'\n\ntools = [\n    Tool('search', '搜索信息', search_tool),\n    Tool('calculator', '数学计算', calc_tool),\n]\n\n# 使用工具\nfor tool in tools:\n    print(f'工具: {tool.name}')\n    print(f'  描述: {tool.description}')\n\nprint(tools[0].run('Python 教程'))\nprint(tools[1].run('2 + 3 * 4'))",
     "tags": ["LangChain", "Tools"]},

    {"id": "ex_langchain_007", "module": "langchain_framework", "title": "文档分割器", "difficulty": "medium", "points": 15,
     "description": "实现文本分块功能，模拟 LangChain 的 TextSplitter",
     "starter_code": "class TextSplitter:\n    def __init__(self, chunk_size=100, overlap=20):\n        self.chunk_size = chunk_size\n        self.overlap = overlap\n    \n    def split(self, text):\n        # 分割文本\n        pass",
     "solution": "class TextSplitter:\n    def __init__(self, chunk_size=100, overlap=20):\n        self.chunk_size = chunk_size\n        self.overlap = overlap\n    \n    def split(self, text):\n        chunks = []\n        start = 0\n        while start < len(text):\n            end = start + self.chunk_size\n            chunk = text[start:end]\n            chunks.append(chunk)\n            start = end - self.overlap\n        return chunks\n\ntext = 'Python 是一种广泛使用的高级编程语言。它以简洁易读的语法著称，支持多种编程范式，包括面向对象、函数式和过程式编程。Python 有丰富的标准库和第三方库生态系统。' * 5\n\nsplitter = TextSplitter(chunk_size=50, overlap=10)\nchunks = splitter.split(text)\nprint(f'原始文本长度: {len(text)}')\nprint(f'分块数量: {len(chunks)}')\nprint(f'第一块: {chunks[0]}')",
     "tags": ["LangChain", "TextSplitter"]},

    {"id": "ex_langchain_008", "module": "langchain_framework", "title": "LCEL 管道模拟", "difficulty": "hard", "points": 20,
     "description": "模拟 LangChain LCEL 的管道语法（| 操作符）",
     "starter_code": "# 实现支持 | 操作符的组件\nclass Runnable:\n    def invoke(self, input):\n        raise NotImplementedError\n    \n    def __or__(self, other):\n        # 实现管道操作\n        pass",
     "solution": "class Runnable:\n    def invoke(self, input):\n        raise NotImplementedError\n    \n    def __or__(self, other):\n        return RunnableSequence(self, other)\n\nclass RunnableSequence(Runnable):\n    def __init__(self, first, second):\n        self.first = first\n        self.second = second\n    \n    def invoke(self, input):\n        return self.second.invoke(self.first.invoke(input))\n\nclass PromptTemplate(Runnable):\n    def __init__(self, template):\n        self.template = template\n    def invoke(self, inputs):\n        result = self.template\n        for k, v in inputs.items():\n            result = result.replace('{' + k + '}', str(v))\n        return result\n\nclass MockLLM(Runnable):\n    def invoke(self, prompt):\n        return f'[LLM 回答]: {prompt[:30]}...'\n\nclass StrParser(Runnable):\n    def invoke(self, text):\n        return text.strip()\n\n# 使用 LCEL 管道\nchain = PromptTemplate('请介绍 {topic}') | MockLLM() | StrParser()\nresult = chain.invoke({'topic': 'Python'})\nprint(result)",
     "tags": ["LangChain", "LCEL"]},

    {"id": "ex_langchain_009", "module": "langchain_framework", "title": "文档加载模拟", "difficulty": "medium", "points": 15,
     "description": "实现文档加载器，从文本生成文档对象",
     "starter_code": "class Document:\n    def __init__(self, page_content, metadata=None):\n        self.page_content = page_content\n        self.metadata = metadata or {}\n\nclass TextLoader:\n    def __init__(self, text):\n        self.text = text\n    \n    def load(self):\n        # 返回 Document 列表\n        pass",
     "solution": "class Document:\n    def __init__(self, page_content, metadata=None):\n        self.page_content = page_content\n        self.metadata = metadata or {}\n    def __repr__(self):\n        return f'Document(content={self.page_content[:30]}..., meta={self.metadata})'\n\nclass TextLoader:\n    def __init__(self, text, source='text'):\n        self.text = text\n        self.source = source\n    \n    def load(self):\n        paragraphs = [p.strip() for p in self.text.split('\\n\\n') if p.strip()]\n        return [\n            Document(\n                page_content=para,\n                metadata={'source': self.source, 'index': i}\n            )\n            for i, para in enumerate(paragraphs)\n        ]\n\ntext = '''\nPython 是一种编程语言。\n\nPython 易于学习和使用。\n\nPython 有丰富的库生态系统。\n'''\n\nloader = TextLoader(text, source='intro.txt')\ndocs = loader.load()\nfor doc in docs:\n    print(doc)",
     "tags": ["LangChain", "文档加载"]},

    {"id": "ex_langchain_010", "module": "langchain_framework", "title": "RetrievalQA 模拟", "difficulty": "hard", "points": 20,
     "description": "模拟 LangChain RetrievalQA 的完整流程",
     "starter_code": "# 模拟检索问答流程\nclass VectorStore:\n    def __init__(self, docs):\n        self.docs = docs\n    \n    def similarity_search(self, query, k=2):\n        # 简单关键词匹配\n        pass\n\nclass RetrievalQA:\n    def __init__(self, retriever, llm):\n        self.retriever = retriever\n        self.llm = llm\n    \n    def invoke(self, question):\n        # 检索+生成\n        pass",
     "solution": "class Document:\n    def __init__(self, content):\n        self.page_content = content\n\nclass VectorStore:\n    def __init__(self, docs):\n        self.docs = docs\n    \n    def similarity_search(self, query, k=2):\n        scored = [(doc, sum(1 for w in query.split() if w in doc.page_content)) for doc in self.docs]\n        scored.sort(key=lambda x: x[1], reverse=True)\n        return [doc for doc, _ in scored[:k]]\n\nclass MockLLM:\n    def invoke(self, prompt):\n        return f'基于上下文，回答是：{prompt[:50]}'\n\nclass RetrievalQA:\n    def __init__(self, retriever, llm):\n        self.retriever = retriever\n        self.llm = llm\n    \n    def invoke(self, question):\n        docs = self.retriever.similarity_search(question)\n        context = '\\n'.join([d.page_content for d in docs])\n        prompt = f'上下文: {context}\\n问题: {question}'\n        return self.llm.invoke(prompt)\n\ndocs = [\n    Document('Python 是一种高级编程语言，由 Guido van Rossum 创建'),\n    Document('Python 支持面向对象、函数式和过程式编程'),\n    Document('Java 是一种静态类型的编程语言'),\n]\n\nvs = VectorStore(docs)\nqa = RetrievalQA(vs, MockLLM())\nanswer = qa.invoke('Python 是什么？')\nprint(answer)",
     "tags": ["LangChain", "RAG", "RetrievalQA"]},

    # ---- vector_databases ----
    {"id": "ex_vector_001", "module": "vector_databases", "title": "向量创建与表示", "difficulty": "easy", "points": 10,
     "description": "创建和操作基本向量，计算向量的模长",
     "starter_code": "import math\n\ndef vector_magnitude(v):\n    # 计算向量的模长\n    pass\n\ndef normalize(v):\n    # 归一化向量\n    pass\n\nv = [3, 4]\nprint('模长:', vector_magnitude(v))\nprint('归一化:', normalize(v))",
     "solution": "import math\n\ndef vector_magnitude(v):\n    return math.sqrt(sum(x**2 for x in v))\n\ndef normalize(v):\n    mag = vector_magnitude(v)\n    return [x / mag for x in v]\n\nv = [3, 4]\nprint('模长:', vector_magnitude(v))  # 5.0\nprint('归一化:', normalize(v))  # [0.6, 0.8]",
     "tags": ["向量", "基础"]},

    {"id": "ex_vector_002", "module": "vector_databases", "title": "余弦相似度", "difficulty": "easy", "points": 10,
     "description": "实现余弦相似度计算函数",
     "starter_code": "import math\n\ndef cosine_similarity(v1, v2):\n    # 计算余弦相似度\n    pass\n\nv1 = [1, 2, 3]\nv2 = [1, 2, 4]\nprint('相似度:', cosine_similarity(v1, v2))",
     "solution": "import math\n\ndef dot_product(v1, v2):\n    return sum(a * b for a, b in zip(v1, v2))\n\ndef magnitude(v):\n    return math.sqrt(sum(x**2 for x in v))\n\ndef cosine_similarity(v1, v2):\n    dot = dot_product(v1, v2)\n    mag1 = magnitude(v1)\n    mag2 = magnitude(v2)\n    if mag1 == 0 or mag2 == 0:\n        return 0\n    return dot / (mag1 * mag2)\n\nv1 = [1, 2, 3]\nv2 = [1, 2, 4]\nprint(f'相似度: {cosine_similarity(v1, v2):.4f}')\n\n# 相同向量\nprint(f'自身相似度: {cosine_similarity(v1, v1):.4f}')",
     "tags": ["向量", "余弦相似度"]},

    {"id": "ex_vector_003", "module": "vector_databases", "title": "欧氏距离", "difficulty": "easy", "points": 10,
     "description": "实现欧氏距离和曼哈顿距离",
     "starter_code": "import math\n\ndef euclidean_distance(v1, v2):\n    # 欧氏距离\n    pass\n\ndef manhattan_distance(v1, v2):\n    # 曼哈顿距离\n    pass\n\nv1 = [0, 0]\nv2 = [3, 4]",
     "solution": "import math\n\ndef euclidean_distance(v1, v2):\n    return math.sqrt(sum((a - b)**2 for a, b in zip(v1, v2)))\n\ndef manhattan_distance(v1, v2):\n    return sum(abs(a - b) for a, b in zip(v1, v2))\n\nv1 = [0, 0]\nv2 = [3, 4]\nprint(f'欧氏距离: {euclidean_distance(v1, v2):.2f}')  # 5.0\nprint(f'曼哈顿距离: {manhattan_distance(v1, v2)}')  # 7",
     "tags": ["向量", "距离"]},

    {"id": "ex_vector_004", "module": "vector_databases", "title": "简单向量索引", "difficulty": "medium", "points": 15,
     "description": "实现一个简单的向量索引，支持添加和搜索",
     "starter_code": "import math\n\nclass SimpleVectorIndex:\n    def __init__(self):\n        self.vectors = {}\n    \n    def add(self, id, vector, metadata=None):\n        # 添加向量\n        pass\n    \n    def search(self, query_vector, k=3):\n        # 搜索最相似的 k 个向量\n        pass",
     "solution": "import math\n\ndef cosine_sim(v1, v2):\n    dot = sum(a*b for a, b in zip(v1, v2))\n    m1 = math.sqrt(sum(x**2 for x in v1))\n    m2 = math.sqrt(sum(x**2 for x in v2))\n    return dot / (m1 * m2) if m1 and m2 else 0\n\nclass SimpleVectorIndex:\n    def __init__(self):\n        self.vectors = {}\n    \n    def add(self, id, vector, metadata=None):\n        self.vectors[id] = {'vector': vector, 'metadata': metadata or {}}\n    \n    def search(self, query_vector, k=3):\n        scores = []\n        for id, item in self.vectors.items():\n            sim = cosine_sim(query_vector, item['vector'])\n            scores.append((id, sim, item['metadata']))\n        scores.sort(key=lambda x: x[1], reverse=True)\n        return scores[:k]\n\nindex = SimpleVectorIndex()\nindex.add('python', [1, 0, 0], {'text': 'Python 编程语言'})\nindex.add('java', [0.8, 0.2, 0], {'text': 'Java 编程语言'})\nindex.add('ml', [0, 0.8, 0.6], {'text': '机器学习'})\nindex.add('dl', [0, 0.6, 0.8], {'text': '深度学习'})\n\nresults = index.search([0, 0.7, 0.7], k=2)\nfor id, score, meta in results:\n    print(f'{id}: {score:.3f} - {meta[\"text\"]}')",
     "tags": ["向量索引", "搜索"]},

    {"id": "ex_vector_005", "module": "vector_databases", "title": "简单词向量", "difficulty": "medium", "points": 15,
     "description": "实现简单的词袋模型向量化",
     "starter_code": "def vectorize(texts):\n    # 词袋模型向量化\n    pass\n\ntexts = ['Python 是编程语言', 'Java 是编程语言', 'Python 用于机器学习']",
     "solution": "from collections import Counter\n\ndef build_vocab(texts):\n    vocab = set()\n    for text in texts:\n        vocab.update(text.split())\n    return sorted(vocab)\n\ndef vectorize(text, vocab):\n    counter = Counter(text.split())\n    return [counter.get(word, 0) for word in vocab]\n\ntexts = ['Python 是 编程语言', 'Java 是 编程语言', 'Python 用于 机器学习']\nvocab = build_vocab(texts)\nprint('词汇表:', vocab)\n\nfor text in texts:\n    vec = vectorize(text, vocab)\n    print(f'{text} -> {vec}')",
     "tags": ["词向量", "词袋模型"]},

    {"id": "ex_vector_006", "module": "vector_databases", "title": "KNN 搜索", "difficulty": "medium", "points": 15,
     "description": "实现 K 近邻搜索算法",
     "starter_code": "def knn_search(query, vectors, k=3):\n    # 找到 query 的 K 个最近邻\n    pass",
     "solution": "import math\n\ndef euclidean_dist(v1, v2):\n    return math.sqrt(sum((a-b)**2 for a, b in zip(v1, v2)))\n\ndef knn_search(query, vectors, k=3):\n    distances = [(label, euclidean_dist(query, vec)) for label, vec in vectors]\n    distances.sort(key=lambda x: x[1])\n    return distances[:k]\n\n# 测试数据\nvectors = [\n    ('苹果', [1, 0, 0]),\n    ('香蕉', [0.9, 0.1, 0]),\n    ('狗', [0, 1, 0]),\n    ('猫', [0, 0.9, 0.1]),\n    ('汽车', [0, 0, 1]),\n]\n\nquery = [0.95, 0.05, 0]  # 接近苹果的向量\nresults = knn_search(query, vectors, k=2)\nprint('最近邻:')\nfor label, dist in results:\n    print(f'  {label}: {dist:.3f}')",
     "tags": ["KNN", "搜索"]},

    {"id": "ex_vector_007", "module": "vector_databases", "title": "向量数据库操作", "difficulty": "hard", "points": 20,
     "description": "实现一个带持久化的向量数据库",
     "starter_code": "import json\n\nclass VectorDB:\n    def __init__(self):\n        self.data = []\n    \n    def insert(self, id, vector, payload):\n        pass\n    \n    def search(self, query, top_k=5):\n        pass\n    \n    def delete(self, id):\n        pass\n    \n    def save(self, path):\n        pass\n    \n    def load(self, path):\n        pass",
     "solution": "import json\nimport math\n\ndef cosine_sim(v1, v2):\n    dot = sum(a*b for a, b in zip(v1, v2))\n    m1 = math.sqrt(sum(x**2 for x in v1)) or 1\n    m2 = math.sqrt(sum(x**2 for x in v2)) or 1\n    return dot / (m1 * m2)\n\nclass VectorDB:\n    def __init__(self):\n        self.data = []\n    \n    def insert(self, id, vector, payload):\n        self.data.append({'id': id, 'vector': vector, 'payload': payload})\n    \n    def search(self, query, top_k=5):\n        scored = [(item, cosine_sim(query, item['vector'])) for item in self.data]\n        scored.sort(key=lambda x: x[1], reverse=True)\n        return [(item['id'], score, item['payload']) for item, score in scored[:top_k]]\n    \n    def delete(self, id):\n        self.data = [item for item in self.data if item['id'] != id]\n    \n    def save(self, path):\n        with open(path, 'w', encoding='utf-8') as f:\n            json.dump(self.data, f)\n    \n    def load(self, path):\n        with open(path, 'r', encoding='utf-8') as f:\n            self.data = json.load(f)\n\n# 测试\ndb = VectorDB()\ndb.insert('doc1', [1, 0, 0], {'text': 'Python 文档'})\ndb.insert('doc2', [0, 1, 0], {'text': 'Java 文档'})\ndb.insert('doc3', [0.8, 0.2, 0], {'text': 'Python 教程'})\n\nresults = db.search([1, 0, 0], top_k=2)\nfor id, score, payload in results:\n    print(f'{id}: {score:.3f} {payload[\"text\"]}')",
     "tags": ["向量数据库", "持久化"]},

    # ---- prompt_engineering ----
    {"id": "ex_prompt_001", "module": "prompt_engineering", "title": "角色提示", "difficulty": "easy", "points": 10,
     "description": "编写有效的角色提示（System Prompt）",
     "starter_code": "def create_system_prompt(role, expertise, style):\n    # 构建角色提示\n    pass\n\nprompt = create_system_prompt('Python 导师', ['算法', '数据结构'], '专业友好')\nprint(prompt)",
     "solution": "def create_system_prompt(role, expertise, style):\n    expertise_str = ', '.join(expertise)\n    return f\"\"\"你是一位专业的{role}。\n你的专业领域包括：{expertise_str}。\n你的回答风格：{style}。\n当遇到你不确定的问题时，请坦诚说明。\n请始终给出清晰、有条理的回答。\"\"\"\n\nprompt = create_system_prompt('Python 导师', ['算法', '数据结构'], '专业友好')\nprint(prompt)",
     "tags": ["提示工程", "角色提示"]},

    {"id": "ex_prompt_002", "module": "prompt_engineering", "title": "Few-shot 示例", "difficulty": "easy", "points": 10,
     "description": "构建 Few-shot 提示，通过示例引导模型输出",
     "starter_code": "def build_few_shot_prompt(task, examples, query):\n    # 构建 few-shot 提示\n    pass\n\nexamples = [\n    ('Python 是什么？', 'Python 是一种高级编程语言，以简洁著称。'),\n    ('Java 是什么？', 'Java 是一种面向对象的编程语言，一次编写到处运行。')\n]\n\nprompt = build_few_shot_prompt('请介绍编程语言', examples, 'JavaScript 是什么？')\nprint(prompt)",
     "solution": "def build_few_shot_prompt(task, examples, query):\n    prompt = f'任务：{task}\\n\\n示例：\\n'\n    for i, (q, a) in enumerate(examples, 1):\n        prompt += f'问：{q}\\n答：{a}\\n\\n'\n    prompt += f'现在回答以下问题：\\n问：{query}\\n答：'\n    return prompt\n\nexamples = [\n    ('Python 是什么？', 'Python 是一种高级编程语言，以简洁著称。'),\n    ('Java 是什么？', 'Java 是一种面向对象的编程语言，一次编写到处运行。')\n]\n\nprompt = build_few_shot_prompt('请介绍编程语言', examples, 'JavaScript 是什么？')\nprint(prompt)",
     "tags": ["Few-shot", "提示"]},

    {"id": "ex_prompt_003", "module": "prompt_engineering", "title": "CoT 提示", "difficulty": "medium", "points": 15,
     "description": "构建 Chain of Thought 提示，引导逐步推理",
     "starter_code": "def cot_prompt(problem, steps_hint=None):\n    # 构建 CoT 提示\n    pass\n\nproblem = '一个班级有 30 名学生，其中 60% 是女生，女生中有 40% 喜欢数学，请问喜欢数学的女生有多少人？'\nprompt = cot_prompt(problem)\nprint(prompt)",
     "solution": "def cot_prompt(problem, steps_hint=None):\n    prompt = f'请一步步思考以下问题：\\n\\n{problem}\\n\\n'\n    if steps_hint:\n        prompt += '解题步骤提示：\\n'\n        for i, hint in enumerate(steps_hint, 1):\n            prompt += f'{i}. {hint}\\n'\n        prompt += '\\n'\n    prompt += '让我一步步来解：\\n步骤1：'\n    return prompt\n\nproblem = '一个班级有 30 名学生，其中 60% 是女生，女生中有 40% 喜欢数学，喜欢数学的女生有多少人？'\nhints = ['先计算女生总数', '再计算喜欢数学的女生', '得出答案']\nprompt = cot_prompt(problem, hints)\nprint(prompt)",
     "tags": ["CoT", "推理"]},

    {"id": "ex_prompt_004", "module": "prompt_engineering", "title": "输出格式控制", "difficulty": "medium", "points": 15,
     "description": "编写提示控制模型输出的格式（JSON/Markdown等）",
     "starter_code": "def format_prompt(task, output_format):\n    # 构建要求特定格式输出的提示\n    pass\n\nprompt = format_prompt('分析 Python 的优缺点', 'json')\nprint(prompt)",
     "solution": "def format_prompt(task, output_format):\n    format_instructions = {\n        'json': '请以 JSON 格式输出，包含 advantages 和 disadvantages 两个数组字段。',\n        'markdown': '请以 Markdown 格式输出，使用 ## 标题和 - 列表。',\n        'table': '请以 Markdown 表格格式输出，包含 方面、优点、缺点 三列。',\n        'list': '请以编号列表格式输出，清晰列举各点。'\n    }\n    instruction = format_instructions.get(output_format, '请结构化输出。')\n    return f'{task}\\n\\n输出要求：{instruction}\\n\\n输出：'\n\nprompt = format_prompt('分析 Python 的优缺点', 'json')\nprint(prompt)\n\nprompt2 = format_prompt('比较 Python 和 Java', 'table')\nprint(prompt2)",
     "tags": ["格式控制", "提示"]},

    {"id": "ex_prompt_005", "module": "prompt_engineering", "title": "提示模板库", "difficulty": "medium", "points": 15,
     "description": "构建可复用的提示模板库",
     "starter_code": "class PromptLibrary:\n    def __init__(self):\n        self.templates = {}\n    \n    def register(self, name, template):\n        pass\n    \n    def render(self, name, **kwargs):\n        pass\n    \n    def list_templates(self):\n        pass",
     "solution": "class PromptLibrary:\n    def __init__(self):\n        self.templates = {}\n    \n    def register(self, name, template, description=''):\n        self.templates[name] = {'template': template, 'desc': description}\n    \n    def render(self, name, **kwargs):\n        if name not in self.templates:\n            raise ValueError(f'模板不存在: {name}')\n        tpl = self.templates[name]['template']\n        return tpl.format(**kwargs)\n    \n    def list_templates(self):\n        return [(name, info['desc']) for name, info in self.templates.items()]\n\nlibrary = PromptLibrary()\n\nlibrary.register('code_review', '请审查以下 {language} 代码，指出问题和改进建议：\\n```{language}\\n{code}\\n```', '代码审查')\nlibrary.register('translate', '请将以下文本翻译成{target_lang}，保持原意：\\n{text}', '文本翻译')\nlibrary.register('summarize', '请用{max_words}字以内总结以下内容：\\n{content}', '文本摘要')\n\nprint('模板列表:')\nfor name, desc in library.list_templates():\n    print(f'  {name}: {desc}')\n\nprint()\nprint(library.render('translate', target_lang='英文', text='Python 是一种高级编程语言'))",
     "tags": ["提示模板", "复用"]}
]

exercises.extend(batch1)

with open('exercises.json', 'w', encoding='utf-8') as f:
    json.dump(exercises, f, ensure_ascii=False, indent=2)

print(f'已添加 {len(batch1)} 道练习题，总计: {len(exercises)}')
