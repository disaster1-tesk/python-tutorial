# Python 深度学习

## 1. PyTorch 基础

### 知识点解析

**概念定义**：PyTorch 是 Meta（原 Facebook）开源的深度学习框架，以动态计算图和 Pythonic 的设计风格著称。是目前学术界和工业界最流行的深度学习框架之一。

**核心概念**：
- **Tensor（张量）**：PyTorch 的核心数据结构，类似 NumPy 数组但支持 GPU 加速
- **自动微分（Autograd）**：自动计算梯度，`requires_grad=True` 开启追踪
- **计算图**：前向传播构建图，反向传播计算梯度
- **nn.Module**：所有神经网络模块的基类
- **DataLoader**：批量数据加载器，支持自动分批、打乱、多进程

**核心规则**：
1. 张量创建：`torch.tensor()`、`torch.zeros()`、`torch.randn()`，支持 `.to('cuda')` 转移到 GPU
2. 自动求导：前向计算 → `loss.backward()` → 参数 `.grad` 获取梯度
3. 模型定义：继承 `nn.Module`，实现 `__init__()` 和 `forward()`
4. 训练循环：清零梯度 `optimizer.zero_grad()` → 前向 `output = model(x)` → 计算损失 `loss = criterion(output, y)` → 反向 `loss.backward()` → 更新 `optimizer.step()`
5. `model.eval()` / `model.train()` 切换推理/训练模式（影响 Dropout 和 BatchNorm）

**常见易错点**：
1. 忘记 `optimizer.zero_grad()` 导致梯度累积
2. Tensor 和 NumPy 之间的转换：`.numpy()` 要求 Tensor 在 CPU 上且无梯度
3. `torch.no_grad()` 在推理时使用，节省内存并避免不必要的梯度计算
4. 形状不匹配是最常见的错误：注意 `(batch_size, channels, height, width)` 的顺序
5. `squeeze()` 删除长度为1的维度，`unsqueeze()` 增加维度

### 实战案例

#### 案例1：PyTorch 基础操作
```python
import torch
import torch.nn as nn
import torch.optim as optim

# ========== Tensor 操作 ==========
# 创建张量
t = torch.tensor([1, 2, 3, 4], dtype=torch.float32)
mat = torch.randn(3, 3)           # 标准正态分布
zeros = torch.zeros(2, 3)
ones = torch.ones(2, 3)
eye = torch.eye(3)

# GPU 支持
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
t_gpu = t.to(device)

# Tensor 与 NumPy 互转
import numpy as np
arr = np.array([1, 2, 3])
t_from_np = torch.from_numpy(arr)   # NumPy -> Tensor
t_to_np = t_from_np.numpy()         # Tensor -> NumPy

# 数学运算
a = torch.tensor([1.0, 2.0, 3.0])
b = torch.tensor([4.0, 5.0, 6.0])
print(f"元素乘: {a * b}")
print(f"点积: {torch.dot(a, b)}")
print(f"矩阵乘: {torch.matmul(a, b)}")

# ========== 自动微分 ==========
x = torch.tensor(2.0, requires_grad=True)
y = x ** 2 + 3 * x + 1     # y = x² + 3x + 1
y.backward()                 # 自动求导
print(f"dy/dx at x=2: {x.grad}")  # 2*2 + 3 = 7

# 多个变量
w = torch.tensor([1.0, 2.0], requires_grad=True)
b = torch.tensor(0.5, requires_grad=True)
x_input = torch.tensor([3.0, 4.0])
y = torch.dot(w, x_input) + b    # y = 1*3 + 2*4 + 0.5 = 12.5
y.backward()
print(f"dy/dw: {w.grad}")  # [3, 4]
print(f"dy/db: {b.grad}")  # 1.0
```

---

## 2. 神经网络基础

### 知识点解析

**核心概念**：
- **全连接层（Linear）**：`y = xW^T + b`，每个输入连接每个输出
- **激活函数**：ReLU、Sigmoid、Tanh、GELU，引入非线性
- **损失函数**：MSE（回归）、CrossEntropy（分类）、BCE（二分类）
- **优化器**：SGD、Adam、AdamW，更新参数的规则
- **正则化**：Dropout、BatchNorm、L2正则化，防止过拟合

### 实战案例

#### 案例1：多层感知机（MLP）实现
```python
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset

# ========== 定义模型 ==========
class MLP(nn.Module):
    """多层感知机：3层全连接网络"""

    def __init__(self, input_dim, hidden_dim, output_dim, dropout_rate=0.3):
        super().__init__()
        self.network = nn.Sequential(
            nn.Linear(input_dim, hidden_dim),
            nn.BatchNorm1d(hidden_dim),      # 批归一化
            nn.ReLU(),                        # 激活函数
            nn.Dropout(dropout_rate),          # Dropout 正则化

            nn.Linear(hidden_dim, hidden_dim // 2),
            nn.BatchNorm1d(hidden_dim // 2),
            nn.ReLU(),
            nn.Dropout(dropout_rate),

            nn.Linear(hidden_dim // 2, output_dim),
        )

    def forward(self, x):
        return self.network(x)

# ========== 创建模型 ==========
model = MLP(input_dim=784, hidden_dim=256, output_dim=10)
print(f"模型参数量: {sum(p.numel() for p in model.parameters()):,}")

# ========== 生成模拟数据（类似MNIST） ==========
X_train = torch.randn(1000, 784)           # 1000张28x28图片
y_train = torch.randint(0, 10, (1000,))    # 10分类
X_test = torch.randn(200, 784)
y_test = torch.randint(0, 10, (200,))

# 创建 DataLoader
train_dataset = TensorDataset(X_train, y_train)
train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)

# ========== 训练配置 ==========
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001, weight_decay=1e-4)
scheduler = optim.lr_scheduler.StepLR(optimizer, step_size=5, gamma=0.5)

# ========== 训练循环 ==========
num_epochs = 10
for epoch in range(num_epochs):
    model.train()
    total_loss = 0
    correct = 0
    total = 0

    for batch_X, batch_y in train_loader:
        # 1. 清零梯度
        optimizer.zero_grad()

        # 2. 前向传播
        outputs = model(batch_X)

        # 3. 计算损失
        loss = criterion(outputs, batch_y)

        # 4. 反向传播
        loss.backward()

        # 5. 更新参数
        optimizer.step()

        total_loss += loss.item()
        _, predicted = outputs.max(1)
        correct += predicted.eq(batch_y).sum().item()
        total += batch_y.size(0)

    scheduler.step()

    # 评估
    model.eval()
    with torch.no_grad():
        test_outputs = model(X_test)
        test_loss = criterion(test_outputs, y_test)
        _, test_pred = test_outputs.max(1)
        test_acc = test_pred.eq(y_test).sum().item() / len(y_test)

    avg_loss = total_loss / len(train_loader)
    train_acc = correct / total
    print(f"Epoch {epoch+1:2d} | Loss: {avg_loss:.4f} | "
          f"Train Acc: {train_acc:.2%} | Test Acc: {test_acc:.2%} | "
          f"LR: {scheduler.get_last_lr()[0]:.6f}")
```

---

## 3. 卷积神经网络（CNN）

### 知识点解析

**概念定义**：CNN 是处理图像数据的核心架构，通过卷积核提取空间特征。在图像分类、目标检测、语义分割等任务中表现出色。

**核心概念**：
- **卷积层（Conv2d）**：滑动窗口提取局部特征，参数 `in_channels`、`out_channels`、`kernel_size`
- **池化层（MaxPool2d）**：降采样，减少计算量，提取最显著特征
- **特征图（Feature Map）**：卷积层的输出，每个通道代表一种特征
- **感受野（Receptive Field）**：每个输出像素对应的输入区域大小

**核心规则**：
1. 图像张量形状：`(batch_size, channels, height, width)`，PyTorch 使用 NCHW 格式
2. 卷积后尺寸计算：`output = (input - kernel + 2*padding) / stride + 1`
3. 典型 CNN 结构：`Conv → BN → ReLU → Pool → ... → Flatten → Linear`
4. 迁移学习：用预训练模型（ResNet、VGG、EfficientNet）作为特征提取器，微调最后一层

### 实战案例

#### 案例1：CNN 图像分类
```python
class SimpleCNN(nn.Module):
    """简单CNN：适用于CIFAR-10等小图片分类"""

    def __init__(self, num_classes=10):
        super().__init__()
        self.features = nn.Sequential(
            # 卷积块1: 3x32x32 -> 32x16x16
            nn.Conv2d(3, 32, kernel_size=3, padding=1),
            nn.BatchNorm2d(32),
            nn.ReLU(),
            nn.MaxPool2d(2, 2),

            # 卷积块2: 32x16x16 -> 64x8x8
            nn.Conv2d(32, 64, kernel_size=3, padding=1),
            nn.BatchNorm2d(64),
            nn.ReLU(),
            nn.MaxPool2d(2, 2),

            # 卷积块3: 64x8x8 -> 128x4x4
            nn.Conv2d(64, 128, kernel_size=3, padding=1),
            nn.BatchNorm2d(128),
            nn.ReLU(),
            nn.MaxPool2d(2, 2),
        )

        self.classifier = nn.Sequential(
            nn.Flatten(),
            nn.Linear(128 * 4 * 4, 256),
            nn.ReLU(),
            nn.Dropout(0.5),
            nn.Linear(256, num_classes),
        )

    def forward(self, x):
        x = self.features(x)
        x = self.classifier(x)
        return x

# 模拟前向传播
model = SimpleCNN(num_classes=10)
dummy_input = torch.randn(4, 3, 32, 32)  # batch=4, 3通道, 32x32
output = model(dummy_input)
print(f"输入: {dummy_input.shape} -> 输出: {output.shape}")
```

#### 案例2：迁移学习（ResNet）
```python
import torchvision.models as models

# 加载预训练 ResNet18
resnet = models.resnet18(pretrained=True)

# 冻结所有卷积层
for param in resnet.parameters():
    param.requires_grad = False

# 替换最后的全连接层
num_features = resnet.fc.in_features  # 512
resnet.fc = nn.Linear(num_features, 10)  # 10分类

# 只训练最后全连接层
optimizer = optim.Adam(resnet.fc.parameters(), lr=0.001)

print(f"可训练参数: {sum(p.numel() for p in resnet.parameters() if p.requires_grad):,}")
print(f"冻结参数: {sum(p.numel() for p in resnet.parameters() if not p.requires_grad):,}")
```

---

## 4. 循环神经网络（RNN/LSTM/GRU）

### 知识点解析

**核心概念**：
- **RNN**：处理序列数据，隐藏状态传递历史信息
- **LSTM**：长短期记忆网络，通过门控机制解决梯度消失问题
- **GRU**：门控循环单元，LSTM 的简化版本，参数更少
- **序列到序列**：编码器-解码器架构，用于机器翻译、文本摘要

**核心规则**：
1. RNN 输入形状：`(batch_size, seq_len, input_size)`
2. LSTM 返回：`output`（每步输出）和 `(h_n, c_n)`（最终隐藏状态和细胞状态）
3. 双向 RNN：同时从前向后和从后向前处理序列，捕获双向上下文
4. 词嵌入（Embedding）：将离散的词ID映射为连续向量

### 实战案例

#### 案例1：LSTM 文本分类
```python
class LSTMClassifier(nn.Module):
    """LSTM 文本情感分类"""

    def __init__(self, vocab_size, embed_dim, hidden_dim, num_classes, num_layers=2):
        super().__init__()
        self.embedding = nn.Embedding(vocab_size, embed_dim, padding_idx=0)
        self.lstm = nn.LSTM(
            embed_dim, hidden_dim,
            num_layers=num_layers,
            batch_first=True,
            bidirectional=True,
            dropout=0.3
        )
        self.classifier = nn.Sequential(
            nn.Linear(hidden_dim * 2, 128),  # *2 因为双向
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(128, num_classes),
        )

    def forward(self, x):
        # x: (batch, seq_len) 词ID序列
        embedded = self.embedding(x)          # (batch, seq_len, embed_dim)
        lstm_out, (hidden, cell) = self.lstm(embedded)

        # 取最后一个时间步的输出（拼接双向）
        hidden_cat = torch.cat((hidden[-2], hidden[-1]), dim=1)  # (batch, hidden*2)
        return self.classifier(hidden_cat)

# 模拟数据
model = LSTMClassifier(vocab_size=10000, embed_dim=128, hidden_dim=64, num_classes=2)
dummy_input = torch.randint(0, 10000, (8, 50))  # batch=8, 序列长度=50
output = model(dummy_input)
print(f"输入: {dummy_input.shape} -> 输出: {output.shape}")
```

---

## 5. Transformer 架构

### 知识点解析

**概念定义**：Transformer 是目前 AI 领域最重要的架构，完全基于自注意力机制（Self-Attention），摒弃了循环和卷积结构。是 GPT、BERT、ViT 等大模型的基础。

**核心概念**：
- **自注意力（Self-Attention）**：`Attention(Q,K,V) = softmax(QK^T/√d_k)V`，每个位置关注序列中所有位置
- **多头注意力（Multi-Head Attention）**：将注意力分成多个"头"，并行计算后拼接
- **位置编码（Positional Encoding）**：因为 Transformer 没有循环结构，需要显式编码位置信息
- **前馈网络（FFN）**：每个 Transformer 层中的两层全连接网络
- **残差连接 + LayerNorm**：`x + Sublayer(LayerNorm(x))`，稳定训练

**核心规则**：
1. 自注意力复杂度为 O(n²)，n 为序列长度——长序列计算开销大
2. 编码器（Encoder）：双向注意力，用于理解（如 BERT）
3. 解码器（Decoder）：因果注意力（只能看前面的token），用于生成（如 GPT）
4. 学习率预热（Warmup）+ 余弦衰减是 Transformer 训练的标准策略

### 实战案例

#### 案例1：手写 Transformer 编码器层
```python
class SelfAttention(nn.Module):
    """多头自注意力"""

    def __init__(self, embed_dim, num_heads):
        super().__init__()
        assert embed_dim % num_heads == 0
        self.num_heads = num_heads
        self.head_dim = embed_dim // num_heads

        self.W_q = nn.Linear(embed_dim, embed_dim)
        self.W_k = nn.Linear(embed_dim, embed_dim)
        self.W_v = nn.Linear(embed_dim, embed_dim)
        self.W_o = nn.Linear(embed_dim, embed_dim)

    def forward(self, x, mask=None):
        batch_size, seq_len, _ = x.shape

        # 计算Q, K, V
        Q = self.W_q(x)  # (batch, seq, embed)
        K = self.W_k(x)
        V = self.W_v(x)

        # 分割多头: (batch, num_heads, seq, head_dim)
        Q = Q.view(batch_size, seq_len, self.num_heads, self.head_dim).transpose(1, 2)
        K = K.view(batch_size, seq_len, self.num_heads, self.head_dim).transpose(1, 2)
        V = V.view(batch_size, seq_len, self.num_heads, self.head_dim).transpose(1, 2)

        # 注意力分数: (batch, heads, seq, seq)
        scores = torch.matmul(Q, K.transpose(-2, -1)) / (self.head_dim ** 0.5)

        if mask is not None:
            scores = scores.masked_fill(mask == 0, float('-inf'))

        attn_weights = torch.softmax(scores, dim=-1)

        # 加权求和
        attn_output = torch.matmul(attn_weights, V)  # (batch, heads, seq, head_dim)

        # 合并多头
        attn_output = attn_output.transpose(1, 2).contiguous()
        attn_output = attn_output.view(batch_size, seq_len, -1)

        return self.W_o(attn_output)


class TransformerEncoderLayer(nn.Module):
    """Transformer 编码器层"""

    def __init__(self, embed_dim, num_heads, ff_dim, dropout=0.1):
        super().__init__()
        self.attention = SelfAttention(embed_dim, num_heads)
        self.ffn = nn.Sequential(
            nn.Linear(embed_dim, ff_dim),
            nn.GELU(),
            nn.Dropout(dropout),
            nn.Linear(ff_dim, embed_dim),
            nn.Dropout(dropout),
        )
        self.norm1 = nn.LayerNorm(embed_dim)
        self.norm2 = nn.LayerNorm(embed_dim)
        self.dropout = nn.Dropout(dropout)

    def forward(self, x, mask=None):
        # 自注意力 + 残差连接
        attn_out = self.attention(self.norm1(x), mask)
        x = x + self.dropout(attn_out)

        # 前馈网络 + 残差连接
        ffn_out = self.ffn(self.norm2(x))
        x = x + ffn_out

        return x


class TransformerEncoder(nn.Module):
    """完整 Transformer 编码器"""

    def __init__(self, vocab_size, embed_dim, num_heads, ff_dim,
                 num_layers, max_len, dropout=0.1):
        super().__init__()
        self.token_embedding = nn.Embedding(vocab_size, embed_dim)
        self.position_embedding = nn.Embedding(max_len, embed_dim)

        self.layers = nn.ModuleList([
            TransformerEncoderLayer(embed_dim, num_heads, ff_dim, dropout)
            for _ in range(num_layers)
        ])
        self.final_norm = nn.LayerNorm(embed_dim)

    def forward(self, x, mask=None):
        batch_size, seq_len = x.shape
        positions = torch.arange(seq_len, device=x.device).unsqueeze(0).expand(batch_size, -1)

        x = self.token_embedding(x) + self.position_embedding(positions)

        for layer in self.layers:
            x = layer(x, mask)

        return self.final_norm(x)
```

---

## 6. 训练技巧与最佳实践

### 知识点解析

**核心概念**：
- **学习率调度**：Warmup、Cosine Decay、ReduceLROnPlateau
- **梯度裁剪**：`torch.nn.utils.clip_grad_norm_()`，防止梯度爆炸
- **混合精度训练**：`torch.cuda.amp`，使用 FP16 加速训练、减少显存
- **早停（Early Stopping）**：验证集性能不再提升时停止训练
- **模型保存与加载**：`torch.save()`、`torch.load()`，保存/恢复模型权重

### 实战案例

```python
# ========== 混合精度训练 ==========
from torch.cuda.amp import autocast, GradScaler

scaler = GradScaler()

for batch_X, batch_y in train_loader:
    optimizer.zero_grad()

    with autocast():  # 自动混合精度
        outputs = model(batch_X)
        loss = criterion(outputs, batch_y)

    scaler.scale(loss).backward()          # 缩放梯度
    scaler.unscale_(optimizer)             # 反缩放（梯度裁剪前）
    torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
    scaler.step(optimizer)                 # 更新参数
    scaler.update()                        # 更新缩放因子

# ========== 模型保存与加载 ==========
# 保存模型
torch.save({
    'model_state_dict': model.state_dict(),
    'optimizer_state_dict': optimizer.state_dict(),
    'epoch': epoch,
    'loss': loss,
}, 'checkpoint.pth')

# 加载模型
checkpoint = torch.load('checkpoint.pth')
model.load_state_dict(checkpoint['model_state_dict'])
optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
```

## 学习建议

1. **先 PyTorch 再 TensorFlow**：PyTorch 更 Pythonic，调试更方便，社区增长更快
2. **从 MLP 开始**：先理解全连接网络，再学 CNN（图像）和 RNN（序列）
3. **手写一次反向传播**：理解 autograd 的原理，但不建议在生产中手动计算梯度
4. **重视数据处理**：80% 的时间在处理数据，20% 在训练模型
5. **GPU 是必需的**：深度学习训练没有 GPU 基本不现实（至少需要 8GB 显存）
6. **先跑通再优化**：先用小数据、简单模型验证流程，再扩大规模
