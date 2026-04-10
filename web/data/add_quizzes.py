import json

with open('quizzes.json', 'r', encoding='utf-8') as f:
    quizzes = json.load(f)

new_quizzes = [
    # langchain_framework (006-010)
    {'id': 'quiz_langchain_006', 'module_id': 'langchain_framework', 'type': '选择', 'question': 'LangChain 中 Chain 的作用是？', 'options': ['仅存储数据', '连接多个组件形成处理流水线', '仅处理HTTP请求', '仅数据库操作'], 'answer': 'B', 'explanation': 'Chain 用于将多个组件串联成工作流。'},
    {'id': 'quiz_langchain_007', 'module_id': 'langchain_framework', 'type': '选择', 'question': '以下哪个是 LangChain 常用的输出解析器？', 'options': ['JSONOutputParser', 'CSVParser', 'XMLParser', 'HTMLParser'], 'answer': 'A', 'explanation': 'JSONOutputParser 将模型输出解析为 JSON。'},
    {'id': 'quiz_langchain_008', 'module_id': 'langchain_framework', 'type': '选择', 'question': 'LangChain Agent 的核心特点是？', 'options': ['完全确定性的', '能自主决策使用哪些工具', '只能顺序执行', '不支持工具调用'], 'answer': 'B', 'explanation': 'Agent 能自主决定使用哪些工具。'},
    {'id': 'quiz_langchain_009', 'module_id': 'langchain_framework', 'type': '选择', 'question': 'VectorStore 在 LangChain 中的作用是？', 'options': ['存储图片', '存储和检索向量嵌入', '仅缓存数据', '处理音频'], 'answer': 'B', 'explanation': 'VectorStore 用于存储向量嵌入并支持相似性搜索。'},
    {'id': 'quiz_langchain_010', 'module_id': 'langchain_framework', 'type': '选择', 'question': '以下哪个不是 LangChain 的 Memory 类型？', 'options': ['ConversationBufferMemory', 'ConversationSummaryMemory', 'EntityMemory', 'ImageMemory'], 'answer': 'D', 'explanation': 'LangChain 有多种 Memory，但没有 ImageMemory。'},

    # vector_databases (006-010)
    {'id': 'quiz_vector_006', 'module_id': 'vector_databases', 'type': '选择', 'question': '向量归一化的作用是？', 'options': ['增加向量长度', '将向量长度统一为1，便于余弦相似度计算', '减少维度', '增加噪声'], 'answer': 'B', 'explanation': '归一化后余弦相似度等于点积。'},
    {'id': 'quiz_vector_007', 'module_id': 'vector_databases', 'type': '选择', 'question': 'HNSW 算法的特点是？', 'options': ['单层索引', '多层图结构，高效近似搜索', '仅支持精确查询', '内存占用极大'], 'answer': 'B', 'explanation': 'HNSW 使用分层图结构，在搜索效率和精度间取得平衡。'},
    {'id': 'quiz_vector_008', 'module_id': 'vector_databases', 'type': '选择', 'question': 'Faiss 的全称是？', 'options': ['Fast Artificial Index', 'Facebook AI Search', 'Facebook AI Similarity Search', 'Fast AI Similarity System'], 'answer': 'C', 'explanation': 'Faiss = Facebook AI Similarity Search。'},
    {'id': 'quiz_vector_009', 'module_id': 'vector_databases', 'type': '选择', 'question': '向量聚类的常用方法是？', 'options': ['仅 K-Means', 'K-Means, DBSCAN, 层次聚类', '仅排序', '仅过滤'], 'answer': 'B', 'explanation': '可以使用多种聚类算法处理向量数据。'},
    {'id': 'quiz_vector_010', 'module_id': 'vector_databases', 'type': '选择', 'question': '向量数据库与传统数据库的关系是？', 'options': ['完全替代', '互补关系，向量作为新型数据类型', '毫无关系', '就是传统数据库'], 'answer': 'B', 'explanation': '向量数据库是传统数据库的补充。'},

    # prompt_engineering (006-010)
    {'id': 'quiz_prompt_006', 'module_id': 'prompt_engineering', 'type': '选择', 'question': 'Zero-shot 提示的特点是？', 'options': ['需要大量示例', '不需要任何示例即可完成任务', '必须训练模型', '只能处理简单任务'], 'answer': 'B', 'explanation': 'Zero-shot 不需要示例，利用预学知识完成任务。'},
    {'id': 'quiz_prompt_007', 'module_id': 'prompt_engineering', 'type': '选择', 'question': 'Self-Consistency 自洽性的核心思想是？', 'options': ['只生成一次', '生成多个推理路径，选择最一致的答案', '随机生成', '仅使用第一个答案'], 'answer': 'B', 'explanation': '通过多数投票选择最一致的推理结果。'},
    {'id': 'quiz_prompt_008', 'module_id': 'prompt_engineering', 'type': '选择', 'question': 'Tree of Thoughts (ToT) 拓展了什么？', 'options': ['单链推理', '树状多分支推理探索', '仅顺序执行', '单一路径'], 'answer': 'B', 'explanation': 'ToT 让模型在多个推理分支中探索。'},
    {'id': 'quiz_prompt_009', 'module_id': 'prompt_engineering', 'type': '选择', 'question': 'Prompt Tuning 与 Prompt Engineering 的区别是？', 'options': ['完全相同', 'Prompt Tuning 通过梯度调整提示嵌入', '前者需要训练', '后者需要GPU'], 'answer': 'B', 'explanation': 'Prompt Tuning 是参数高效的微调方法。'},
    {'id': 'quiz_prompt_010', 'module_id': 'prompt_engineering', 'type': '选择', 'question': 'System Prompt 的作用是？', 'options': ['限制用户输入', '设定模型角色和行为规则', '仅日志记录', '加密通信'], 'answer': 'B', 'explanation': 'System Prompt 定义模型的整体行为。'},

    # rag_architecture (006-010)
    {'id': 'quiz_rag_006', 'module_id': 'rag_architecture', 'type': '选择', 'question': '向量检索在 RAG 中的典型流程是？', 'options': ['仅存储', '文档->分块->向量化->存储->查询->检索', '直接查询', '仅排序'], 'answer': 'B', 'explanation': '完整的向量检索流程包括文档处理、向量化、存储和检索。'},
    {'id': 'quiz_rag_007', 'module_id': 'rag_architecture', 'type': '选择', 'question': 'RAG 中文档分块的目的是？', 'options': ['增加数据量', '将长文档拆分为适合的片段，便于向量化', '减少存储', '仅用于显示'], 'answer': 'B', 'explanation': '合理的分块确保检索内容既相关又完整。'},
    {'id': 'quiz_rag_008', 'module_id': 'rag_architecture', 'type': '选择', 'question': 'HyDE 的原理是？', 'options': ['直接检索', '让模型生成假设文档再检索', '仅排序', '过滤结果'], 'answer': 'B', 'explanation': 'HyDE 先让模型生成假设答案，再用假设答案去检索。'},
    {'id': 'quiz_rag_009', 'module_id': 'rag_architecture', 'type': '选择', 'question': 'RAG 评估的常用指标是？', 'options': ['仅准确率', '上下文相关性、答案准确性、忠实度', '仅速度', '仅成本'], 'answer': 'B', 'explanation': 'RAG 评估需综合考虑检索质量和生成质量。'},
    {'id': 'quiz_rag_010', 'module_id': 'rag_architecture', 'type': '选择', 'question': 'RAG 与微调的选择依据是？', 'options': ['总是用RAG', '需要频繁更新知识用RAG，需要模型适配特定风格用微调', '仅看成本', '仅看速度'], 'answer': 'B', 'explanation': 'RAG 适合动态知识，微调适合固定任务风格。'},

    # model_finetuning (006-010)
    {'id': 'quiz_finetune_006', 'module_id': 'model_finetuning', 'type': '选择', 'question': 'QLoRA 的特点是？', 'options': ['需要全参数训练', '4-bit量化+LoRA，大幅降低显存', '无法量化', '仅支持CPU'], 'answer': 'B', 'explanation': 'QLoRA 通过量化大幅降低显存。'},
    {'id': 'quiz_finetune_007', 'module_id': 'model_finetuning', 'type': '选择', 'question': 'PEFT 的全称是？', 'options': ['Python Extra Fine Tuning', 'Parameter-Efficient Fine-Tuning', 'Pre-Training Extra Fine Tune', 'Prompt Efficient Fine Tuning'], 'answer': 'B', 'explanation': 'PEFT = Parameter-Efficient Fine-Tuning。'},
    {'id': 'quiz_finetune_008', 'module_id': 'model_finetuning', 'type': '选择', 'question': 'Adapter 的作用是？', 'options': ['增加模型参数', '在模型层间插入小型模块进行微调', '减少参数', '仅推理'], 'answer': 'B', 'explanation': 'Adapter 在层间插入小型模块。'},
    {'id': 'quiz_finetune_009', 'module_id': 'model_finetuning', 'type': '选择', 'question': 'Instruction Tuning 的目的是？', 'options': ['仅语言建模', '让模型理解并遵循自然语言指令', '仅生成文本', '仅分类'], 'answer': 'B', 'explanation': 'Instruction Tuning 提升模型指令遵循能力。'},
    {'id': 'quiz_finetune_010', 'module_id': 'model_finetuning', 'type': '选择', 'question': 'RLHF 的全称是？', 'options': ['Reinforcement Learning High Frequency', 'Reinforcement Learning from Human Feedback', 'Rapid Learning High Feature', 'Recursive Learning from History'], 'answer': 'B', 'explanation': 'RLHF = Reinforcement Learning from Human Feedback。'},

    # multimodal_ai (006-010)
    {'id': 'quiz_multimodal_006', 'module_id': 'multimodal_ai', 'type': '选择', 'question': 'BLIP 模型主要用于？', 'options': ['仅文本处理', '图像-文本理解和生成', '仅语音识别', '仅视频处理'], 'answer': 'B', 'explanation': 'BLIP 用于引导式图像-文本理解与生成。'},
    {'id': 'quiz_multimodal_007', 'module_id': 'multimodal_ai', 'type': '选择', 'question': 'Flamingo 模型的特点是？', 'options': ['仅处理图像', '少样本多模态学习', '仅单模态', '不支持few-shot'], 'answer': 'B', 'explanation': 'Flamingo 能在少样本下学习多模态任务。'},
    {'id': 'quiz_multimodal_008', 'module_id': 'multimodal_ai', 'type': '选择', 'question': 'AudioLM 用于？', 'options': ['图像生成', '音频生成和续写', '文本处理', '视频处理'], 'answer': 'B', 'explanation': 'AudioLM 是音频生成模型。'},
    {'id': 'quiz_multimodal_009', 'module_id': 'multimodal_ai', 'type': '选择', 'question': '多模态融合的常用方法是？', 'options': ['仅早融合', '早融合、晚融合、中间融合', '仅晚融合', '仅拼接'], 'answer': 'B', 'explanation': '多模态融合可在不同阶段进行。'},
    {'id': 'quiz_multimodal_010', 'module_id': 'multimodal_ai', 'type': '选择', 'question': '视频理解模型通常处理哪些信息？', 'options': ['仅画面', '画面、音频、时序信息', '仅音频', '仅文本'], 'answer': 'B', 'explanation': '视频理解需综合处理视觉、听觉和时序信息。'},

    # enterprise_mcp (006-010)
    {'id': 'quiz_enterprise_mcp_006', 'module_id': 'enterprise_mcp', 'type': '选择', 'question': 'MCP 网关的主要作用是？', 'options': ['仅日志记录', '统一入口、负载均衡、认证授权', '仅存储', '仅显示'], 'answer': 'B', 'explanation': 'MCP 网关是系统的统一入口。'},
    {'id': 'quiz_enterprise_mcp_007', 'module_id': 'enterprise_mcp', 'type': '选择', 'question': '容器化部署 MCP 的优势是？', 'options': ['无优势', '环境一致、快速伸缩、易于运维', '成本更高', '无法伸缩'], 'answer': 'B', 'explanation': 'Docker/K8s 提供标准化部署。'},
    {'id': 'quiz_enterprise_mcp_008', 'module_id': 'enterprise_mcp', 'type': '选择', 'question': '服务发现在 MCP 集群中的作用是？', 'options': ['仅日志', '自动发现和管理服务实例', '仅存储', '仅监控'], 'answer': 'B', 'explanation': '服务发现让系统自动感知可用的 MCP 实例。'},
    {'id': 'quiz_enterprise_mcp_009', 'module_id': 'enterprise_mcp', 'type': '选择', 'question': 'MCP 多租户架构需要考虑？', 'options': ['仅性能', '资源隔离、权限管理、数据隔离、计费', '仅存储', '仅显示'], 'answer': 'B', 'explanation': '多租户需保证租户间的隔离。'},
    {'id': 'quiz_enterprise_mcp_010', 'module_id': 'enterprise_mcp', 'type': '选择', 'question': '灰度发布 MCP 服务的目的是？', 'options': ['立即全量', '逐步放量、降低风险、快速回滚', '增加成本', '减少功能'], 'answer': 'B', 'explanation': '灰度发布通过逐步放量控制新版本风险。'},

    # mcp_security (006-010)
    {'id': 'quiz_mcp_security_006', 'module_id': 'mcp_security', 'type': '选择', 'question': 'MCP 工具调用审计应记录？', 'options': ['仅时间', '调用者、工具名、参数、结果、时间', '仅参数', '仅结果'], 'answer': 'B', 'explanation': '完整审计需记录完整调用上下文。'},
    {'id': 'quiz_mcp_security_007', 'module_id': 'mcp_security', 'type': '选择', 'question': 'Rate Limiting 在 MCP 中的作用是？', 'options': ['无作用', '防止滥用、保护后端资源', '增加延迟', '减少功能'], 'answer': 'B', 'explanation': '限流防止单个用户过度消耗资源。'},
    {'id': 'quiz_mcp_security_008', 'module_id': 'mcp_security', 'type': '选择', 'question': 'MCP 敏感数据脱敏策略包括？', 'options': ['仅日志', '输入脱敏、输出脱敏、日志脱敏', '仅存储', '仅显示'], 'answer': 'B', 'explanation': '数据全流程都需要脱敏。'},
    {'id': 'quiz_mcp_security_009', 'module_id': 'mcp_security', 'type': '选择', 'question': 'MCP 密钥轮换的最佳实践是？', 'options': ['永不更换', '定期自动轮换、立即撤销泄露密钥', '手动更换', '仅首次设置'], 'answer': 'B', 'explanation': '自动化轮换降低密钥泄露风险。'},
    {'id': 'quiz_mcp_security_010', 'module_id': 'mcp_security', 'type': '选择', 'question': '零信任架构在 MCP 中的体现是？', 'options': ['仅防火墙内', '永不信任、始终验证、最小权限', '仅内网', '仅VPN'], 'answer': 'B', 'explanation': '零信任要求每次访问都经过验证。'}
]

quizzes.extend(new_quizzes)

with open('quizzes.json', 'w', encoding='utf-8') as f:
    json.dump(quizzes, f, ensure_ascii=False, indent=2)

print(f'已添加 {len(new_quizzes)} 道测验题，总计: {len(quizzes)}')
