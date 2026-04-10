# AI 模型微调 (Fine-tuning)

## 1. 微调基础概念

### 知识点解析

**概念定义**：模型微调（Fine-tuning）是指在预训练模型的基础上，使用特定领域的数据进行进一步训练，使模型适应特定任务或领域的技术。

**为什么需要微调**：
- **领域适配**：通用模型在专业领域表现不佳
- **任务定制**：针对特定任务优化模型
- **成本效益**：比从头训练更省资源
- **数据效率**：少量数据即可达到好效果

**核心概念**：
- **预训练模型**：在大规模数据上训练的模型
- **全参数微调**：更新所有参数
- **LoRA/QLoRA**：只更新少量参数
- **Adapter**：插入小型适配器模块

**核心规则**：
1. 质量高的微调数据是关键
2. 学习率通常比预训练时小
3. 训练轮数不宜过多，避免过拟合
4. 评估指标要选择与任务相关的

**常见易错点**：
1. 数据量不足或质量不高
2. 学习率设置不当
3. 过拟合而不自知
4. 没有保留验证集

### 实战案例

#### 案例1：使用 LoRA 微调 LLM
```python
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import LoraConfig, get_peft_model, TaskType

# 加载基础模型
model_name = "gpt2"
model = AutoModelForCausalLM.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)

# 配置 LoRA
lora_config = LoraConfig(
    r=8,  # LoRA 秩
    lora_alpha=16,
    target_modules=["q_proj", "v_proj"],  # 目标层
    lora_dropout=0.05,
    bias="none",
    task_type=TaskType.CAUSAL_LM
)

# 应用 LoRA
model = get_peft_model(model, lora_config)
model.print_trainable_parameters()
# 输出：trainable params: 835,040 || all params: 124,878,080 || trainable%: 0.67
```

---

## 2. 数据准备

### 知识点解析

**数据格式**：
- **Instruction Format**：指令-输入-输出格式
- **Conversational Format**：对话格式
- **JSONL**：每行一个 JSON 对象

**数据清洗**：
- 去除重复数据
- 修正错误标注
- 控制数据质量
- 数据增强

**核心规则**：
1. 数据量：根据任务复杂度，通常 100-10000 条
2. 质量 > 数量：高质量小数据集优于低质量大数据集
3. 多样性：覆盖各种场景
4. 格式统一：符合模型训练格式要求

**常见易错点**：
1. 数据格式不符合要求
2. 数据分布不均匀
3. 没有划分训练/验证/测试集
4. 敏感信息未处理

### 实战案例

#### 案例1：准备微调数据
```python
import json

# Instruction 格式
instruction_data = [
    {
        "instruction": "把下面句子翻译成英文",
        "input": "今天天气很好",
        "output": "The weather is nice today."
    },
    {
        "instruction": "总结以下文章",
        "input": "长文章内容...",
        "output": "简短摘要..."
    }
]

# 转换为训练格式
def format_data(item):
    return f"""Instruction: {item['instruction']}
Input: {item['input']}
Output: {item['output']}"""

# 保存为 JSONL
with open("train.jsonl", "w", encoding="utf-8") as f:
    for item in instruction_data:
        f.write(json.dumps(item, ensure_ascii=False) + "\n")

print(f"已准备 {len(instruction_data)} 条训练数据")
```

#### 案例2：数据增强
```python
# 回译增强
def back_translate(text: str) -> list:
    """回译增强：翻译成其他语言再翻译回中文"""
    # 模拟回译过程
    en = f"[EN] {text}"
    fr = f"[FR] {en}"
    zh_back = fr.replace("[FR] ", "").replace("[EN] ", "")
    return [zh_back]

# 同义词替换
def synonym_replace(text: str) -> list:
    """同义词替换增强"""
    replacements = {
        "很好": ["不错", "非常好", "相当好"],
        "今天": ["今日", "本日"]
    }
    results = [text]
    for key, values in replacements.items():
        if key in text:
            for v in values:
                results.append(text.replace(key, v))
    return results

# 测试
text = "今天天气很好"
augmented = synonym_replace(text)
print(f"原始: {text}")
print(f"增强后: {augmented}")
```

---

## 3. 微调训练

### 知识点解析

**训练参数**：
- **Learning Rate**：通常 1e-5 到 1e-4
- **Batch Size**：根据显存调整，通常 4-32
- **Epochs**：3-10 个 epoch
- **Warmup**：学习率预热比例

**训练技巧**：
1. 使用梯度累积处理大 batch
2. 启用 bf16/fp16 加速
3. 使用 DeepSpeed/ZeRO 节省显存
4. 定期保存检查点

**核心规则**：
1. 监控训练损失和验证损失
2. 早停策略防止过拟合
3. 使用评价指标监控模型质量
4. 训练后评估模型性能

### 实战案例

#### 案例1：使用 Transformers 训练
```python
from transformers import Trainer, TrainingArguments
from datasets import Dataset

# 准备数据
train_data = [
    {"text": f"Instruction: 翻译\nInput: 你好\nOutput: Hello"},
    {"text": f"Instruction: 总结\nInput: 文章内容\nOutput: 摘要"},
]

dataset = Dataset.from_list(train_data)

# 配置训练参数
training_args = TrainingArguments(
    output_dir="./output",
    num_train_epochs=3,
    per_device_train_batch_size=4,
    learning_rate=1e-4,
    warmup_steps=100,
    logging_steps=10,
    save_steps=500,
    eval_strategy="steps",
    save_total_limit=2,
)

# 创建 Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=dataset,
)

# 开始训练
trainer.train()
```

#### 案例2：使用 QLoRA 微调
```python
from transformers import AutoModelForCausalLM, TrainingArguments
from peft import LoraConfig, get_peft_model
from bitsandbytes import BitsAndBytesConfig

# 4-bit 量化配置
bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_compute_dtype="float16",
    bnb_4bit_use_double_quant=True,
    bnb_4bit_quant_type="nf4"
)

# 加载量化模型
model = AutoModelForCausalLM.from_pretrained(
    "facebook/opt-1.3b",
    quantization_config=bnb_config
)

# LoRA 配置
lora_config = LoraConfig(
    r=16,
    lora_alpha=32,
    target_modules=["q_proj", "k_proj", "v_proj", "o_proj"],
    lora_dropout=0.05,
    bias="none",
    task_type="CAUSAL_LM"
)

# 应用 LoRA
model = get_peft_model(model, lora_config)

# 训练
# ... (与上面类似)
```

---

## 4. 模型评估与部署

### 知识点解析

**评估指标**：
- **Perplexity**：语言模型困惑度
- **BLEU/ROUGE**：文本生成质量
- **准确率/F1**：分类任务
- **人工评估**：主观质量

**部署方式**：
- **HuggingFace Transformers**：本地部署
- **vLLM**：高吞吐量推理
- **Ollama**：本地大模型运行
- **API 服务**：FastAPI/Flask

**核心规则**：
1. 评估要全面：自动指标 + 人工评估
2. 部署要考虑性能优化
3. 监控模型在生产环境的表现
4. 定期收集反馈数据进行迭代

### 实战案例

#### 案例1：模型评估
```python
from datasets import load_metric
from transformers import EvalPrediction

# 加载指标
bleu = load_metric("bleu")

# 评估函数
def compute_metrics(eval_pred: EvalPrediction):
    predictions = eval_pred.predictions
    labels = eval_pred.label_ids
    
    # 解码
    decoded_preds = tokenizer.batch_decode(predictions, skip_special_tokens=True)
    decoded_labels = tokenizer.batch_decode(labels, skip_special_tokens=True)
    
    # 计算 BLEU
    result = bleu.compute(
        predictions=[p.split() for p in decoded_preds],
        references=[[l.split()] for l in decoded_labels]
    )
    
    return {"bleu": result["bleu"]}

# 评估
trainer = Trainer(
    model=model,
    eval_dataset=eval_dataset,
    compute_metrics=compute_metrics
)

metrics = trainer.evaluate()
print(metrics)
```

#### 案例2：模型导出与部署
```python
# 合并 LoRA 权重
from peft import PeftModel

# 加载基础模型
base_model = AutoModelForCausalLM.from_pretrained("gpt2")
# 加载 LoRA
peft_model = PeftModel.from_pretrained(base_model, "./lora_output")
# 合并
merged_model = peft_model.merge_and_unload()

# 保存
merged_model.save_pretrained("./final_model")
tokenizer.save_pretrained("./final_model")

# 使用模型
from transformers import pipeline

pipe = pipeline("text-generation", model="./final_model", tokenizer=tokenizer)
result = pipe("Once upon a time")
print(result[0]["generated_text"])
```

---

## 5. 微调最佳实践

### 数据准备技巧

1. **数据质量**
   - 人工审核关键数据
   - 自动检测异常值
   - 多样性检查

2. **数据量估算**
   - 简单任务：100-500 条
   - 中等任务：500-2000 条
   - 复杂任务：2000-10000 条

### 训练技巧

1. **学习率**
   - 建议从 1e-5 开始
   - 可使用 cosine schedule
   - 配合 warmup

2. **防止过拟合**
   - 早停机制
   - 验证集评估
   - 正则化

### 部署优化

1. **量化**
   - INT8 量化
   - INT4 量化
   - GPTQ/AWQ

2. **推理优化**
   - 批量推理
   - KV Cache
   - 连续批处理