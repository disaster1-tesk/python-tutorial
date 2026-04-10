# 提示工程示例代码

# ========== 1. 基础提示词 ==========
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-3.5-turbo")

# 不好的提示词
bad_prompt = "写一首诗"
response = llm.invoke(bad_prompt)
print("=== 不好的提示词结果 ===")
print(response.content[:100])

# 好的提示词
good_prompt = """请写一首关于春天的七言绝句，要求：
1. 描绘春天的景色
2. 押韵工整
3. 意境优美
"""
response = llm.invoke(good_prompt)
print("\n=== 好的提示词结果 ===")
print(response.content)


# ========== 2. 角色扮演提示词 ==========
role_prompt = """你是一位资深的Python工程师，有10年的开发经验。
你的风格是：
1. 代码简洁规范
2. 注重性能优化
3. 善用类型注解

请用Python实现一个快速排序算法："""

response = llm.invoke(role_prompt)
print("\n=== 角色扮演提示词 ===")
print(response.content[:500])


# ========== 3. Few-shot 提示 ==========
few_shot_prompt = """对以下文本进行情感分析（positive/negative/neutral），只输出情感标签。

示例：
文本: 这个产品太棒了，非常满意！
情感: positive

文本: 体验很差，不推荐购买
情感: negative

文本: 还可以，一般般吧
情感: neutral

请分析：
文本: 刚刚入手了这款手机，拍照效果超级棒，满意！
情感:"""

response = llm.invoke(few_shot_prompt)
print("\n=== Few-shot 情感分析 ===")
print(response.content)


# ========== 4. Chain-of-Thought 提示 ==========
cot_prompt = """请一步步计算以下问题，并展示推理过程。

问题：小明有50个苹果，小红比小明多15个，小华比小红少10个。小华有多少个苹果？

推理过程："""

response = llm.invoke(cot_prompt)
print("\n=== Chain-of-Thought 推理 ===")
print(response.content)


# ========== 5. 结构化输出提示 ==========
json_prompt = """请将以下信息提取为JSON格式：
{"name": "string", "company": "string", "position": "string"}

文本：王五，腾讯公司，高级工程师

输出JSON："""

response = llm.invoke(json_prompt)
print("\n=== JSON 结构化输出 ===")
print(response.content)


# ========== 6. 分步提示链 ==========
# 步骤1：提取关键信息
step1_prompt = """从以下文本中提取关键实体（人物、地点、组织）：
文本：马云于1999年在杭州创立了阿里巴巴
实体："""

# 步骤2：生成内容
step2_prompt = """基于以下实体生成介绍：
实体：["马云", "杭州", "阿里巴巴"]
生成一段50字的介绍："""

print("\n=== 分步提示链演示 ===")
print("步骤1: 提取实体")
response1 = llm.invoke(step1_prompt)
print(response1.content)

print("\n步骤2: 生成内容")
response2 = llm.invoke(step2_prompt)
print(response2.content)


# ========== 7. 约束提示 ==========
constraint_prompt = """请生成一句话介绍Python，要求：
1. 不超过30字
2. 不能包含"非常"
3. 要提到"简单"和"强大"

回答："""

response = llm.invoke(constraint_prompt)
print("\n=== 约束提示 ===")
print(response.content)


# ========== 8. 输出格式控制 ==========
# Markdown 格式
md_prompt = """用Markdown表格对比 Python 和 Java：
| 特性 | Python | Java |"""

response = llm.invoke(md_prompt)
print("\n=== Markdown 格式 ===")
print(response.content)


# 使用分隔符
delimiter_prompt = """请分别用【】和（）输出两个内容：

【Python的主要特点】
（）Java的主要特点
"""

response = llm.invoke(delimiter_prompt)
print("\n=== 分隔符使用 ===")
print(response.content)


print("\n" + "="*50)
print("提示工程示例完成")