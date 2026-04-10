# AI 模型微调示例代码

# ========== 1. 准备微调数据 ==========
import json

print("=== 准备微调数据 ===\n")

# 模拟训练数据
train_data = [
    {
        "instruction": "把下面的中文翻译成英文",
        "input": "今天天气很好",
        "output": "The weather is nice today."
    },
    {
        "instruction": "把下面的中文翻译成英文",
        "input": "我喜欢学习Python",
        "output": "I like learning Python."
    },
    {
        "instruction": "回答这个问题",
        "input": "Python的创始人是谁？",
        "output": "Python的创始人是Guido van Rossum。"
    },
    {
        "instruction": "解释这个术语",
        "input": "什么是机器学习？",
        "output": "机器学习是人工智能的一个分支，让计算机通过数据学习并改进。"
    },
]

# 转换为训练格式
def format_for_training(data: list) -> list:
    formatted = []
    for item in data:
        text = f"""Below is an instruction that describes a task, paired with an input that provides further context. Write a response that appropriately completes the request.

### Instruction:
{item['instruction']}

### Input:
{item['input']}

### Response:
{item['output']}"""
        formatted.append({"text": text})
    return formatted

formatted_data = format_for_training(train_data)
print(f"准备 {len(formatted_data)} 条数据")
print(f"示例：\n{formatted_data[0]['text'][:200]}...")

# 保存为 JSONL
with open("train_data.jsonl", "w", encoding="utf-8") as f:
    for item in formatted_data:
        f.write(json.dumps(item, ensure_ascii=False) + "\n")

print("\n数据已保存到 train_data.jsonl")


# ========== 2. LoRA 微调配置 ==========
print("\n" + "="*50)
print("=== LoRA 微调配置示例 ===\n")

# LoRA 配置参数说明
lora_config = {
    "r": 8,                    # LoRA 秩，决定低秩矩阵的维度
    "lora_alpha": 16,          # LoRA 缩放因子
    "target_modules": [        # 要应用 LoRA 的模块
        "q_proj",              # Query 投影
        "v_proj",              # Value 投影
        "k_proj",              # Key 投影
        "o_proj"               # Output 投影
    ],
    "lora_dropout": 0.05,      # Dropout 概率
    "bias": "none",            # 是否训练 bias
    "task_type": "CAUSAL_LM"   # 任务类型
}

print("LoRA 配置：")
for k, v in lora_config.items():
    print(f"  {k}: {v}")

# 计算参数量
print("\n参数量对比（示例）：")
print(f"  基础模型参数量: 124,878,080")
print(f"  LoRA 训练参数量: ~835,040 (0.67%)")


# ========== 3. 训练参数配置 ==========
print("\n" + "="*50)
print("=== 训练参数配置 ===\n")

training_config = {
    "output_dir": "./results",
    "num_train_epochs": 3,
    "per_device_train_batch_size": 4,
    "learning_rate": 1e-4,
    "warmup_steps": 100,
    "logging_steps": 10,
    "save_steps": 500,
    "eval_steps": 500,
    "save_total_limit": 2,
    "fp16": True,              # 使用混合精度
    "gradient_accumulation_steps": 4,  # 梯度累积
}

print("训练参数：")
for k, v in training_config.items():
    print(f"  {k}: {v}")


# ========== 4. 模拟训练过程 ==========
print("\n" + "="*50)
print("=== 模拟训练过程 ===\n")

# 模拟训练日志
import random

epochs = 3
steps_per_epoch = 10

for epoch in range(1, epochs + 1):
    print(f"Epoch {epoch}/{epochs}")
    for step in range(1, steps_per_epoch + 1):
        loss = random.uniform(0.5, 2.0) * (0.8 ** (epoch - 1))  # 损失递减
        
        if step % 5 == 0:
            print(f"  Step {step}: loss = {loss:.4f}, lr = {1e-4:.2e}")
    
    # 验证
    val_loss = random.uniform(0.3, 1.0)
    print(f"  Validation loss: {val_loss:.4f}")
    print()


# ========== 5. 模型评估 ==========
print("="*50)
print("=== 模型评估 ===\n")

# 评估指标
def evaluate_model(predictions: list, references: list) -> dict:
    """模拟评估函数"""
    
    # 准确率
    correct = sum(1 for p, r in zip(predictions, references) if p == r)
    accuracy = correct / len(predictions) if predictions else 0
    
    # BLEU（简化模拟）
    bleu_score = random.uniform(0.3, 0.8)
    
    return {
        "accuracy": accuracy,
        "bleu": bleu_score,
        "perplexity": random.uniform(1.5, 3.0)
    }

# 模拟预测
test_predictions = [
    "The weather is nice today.",
    "I like learning Python.",
    "Guido van Rossum created Python."
]

test_references = [
    "The weather is nice today.",
    "I like learning Python.",
    "Python was created by Guido van Rossum."
]

results = evaluate_model(test_predictions, test_references)

print("评估结果：")
print(f"  准确率: {results['accuracy']:.2%}")
print(f"  BLEU: {results['bleu']:.2f}")
print(f"  Perplexity: {results['perplexity']:.2f}")


# ========== 6. 模型导出与部署 ==========
print("\n" + "="*50)
print("=== 模型导出示例 ===\n")

# 模型导出步骤
export_steps = [
    "1. 合并 LoRA 权重到基础模型",
    "2. 保存模型权重和配置文件",
    "3. 保存 tokenizer",
    "4. 量化模型（可选）",
    "5. 导出为适合部署的格式"
]

for step in export_steps:
    print(f"  {step}")

print("\n部署方式：")
print("  - HuggingFace Transformers")
print("  - vLLM (高吞吐量)")
print("  - Ollama (本地运行)")
print("  - FastAPI 服务")


# ========== 7. 模型量化示例 ==========
print("\n" + "="*50)
print("=== 模型量化示例 ===\n")

quantization_types = {
    "FP16": "16位浮点，精度高，显存减半",
    "INT8": "8位整数，精度略有下降，显存降至1/4",
    "INT4": "4位整数，精度明显下降，显存降至1/8"
}

print("量化类型对比：")
for qtype, desc in quantization_types.items():
    print(f"  {qtype}: {desc}")

print("\n量化命令示例（使用 bitsandbytes）：")
print("  quantization_config = BitsAndBytesConfig(")
print("      load_in_4bit=True,")
print("      bnb_4bit_compute_dtype='float16'")
print("  )")


print("\n" + "="*50)
print("AI 模型微调示例完成")