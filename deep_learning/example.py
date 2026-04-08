"""
Python 深度学习完整示例
演示内容：
1. PyTorch Tensor 操作与自动微分
2. 神经网络：全连接、激活函数、损失函数
3. CNN：卷积、池化、迁移学习概念
4. RNN/LSTM：序列数据处理
5. Transformer：自注意力机制（简化实现）
6. 训练流程：完整训练循环、评估、保存
"""

import numpy as np

print("=" * 60)
print("Python 深度学习完整示例")
print("=" * 60)

# ============================================================
# 1. 模拟张量（Tensor）操作
# ============================================================
print("\n【1. 张量（Tensor）操作】")


class Tensor:
    """简化版 Tensor——演示自动微分原理"""

    def __init__(self, data, requires_grad=False):
        self.data = np.array(data, dtype=np.float64)
        self.requires_grad = requires_grad
        self.grad = None
        self._backward = lambda: None
        self._prev = set()

    def __repr__(self):
        return f"Tensor({self.data}, grad={self.grad})"

    @property
    def shape(self):
        return self.data.shape

    def __add__(self, other):
        other = other if isinstance(other, Tensor) else Tensor(other)
        out = Tensor(self.data + other.data, requires_grad=self.requires_grad or other.requires_grad)

        def _backward():
            if self.requires_grad:
                self.grad = self.grad + out.grad * np.ones_like(self.data) if self.grad is not None else out.grad * np.ones_like(self.data)
            if other.requires_grad:
                other.grad = other.grad + out.grad * np.ones_like(other.data) if other.grad is not None else out.grad * np.ones_like(other.data)

        out._backward = _backward
        out._prev = {self, other}
        return out

    def __mul__(self, other):
        other = other if isinstance(other, Tensor) else Tensor(other)
        out = Tensor(self.data * other.data, requires_grad=self.requires_grad or other.requires_grad)

        def _backward():
            if self.requires_grad:
                self.grad = self.grad + out.grad * other.data if self.grad is not None else out.grad * other.data
            if other.requires_grad:
                other.grad = other.grad + out.grad * self.data if other.grad is not None else out.grad * self.data

        out._backward = _backward
        out._prev = {self, other}
        return out

    def __neg__(self):
        return self * (-1)

    def __sub__(self, other):
        return self + (-other)

    def __pow__(self, n):
        out = Tensor(self.data ** n, requires_grad=self.requires_grad)

        def _backward():
            if self.requires_grad:
                self.grad = self.grad + out.grad * n * (self.data ** (n - 1)) if self.grad is not None else out.grad * n * (self.data ** (n - 1))

        out._backward = _backward
        out._prev = {self}
        return out

    def sum(self):
        out = Tensor(np.array([self.data.sum()]), requires_grad=self.requires_grad)

        def _backward():
            if self.requires_grad:
                self.grad = self.grad + out.grad * np.ones_like(self.data) if self.grad is not None else out.grad * np.ones_like(self.data)

        out._backward = _backward
        out._prev = {self}
        return out

    def backward(self):
        # 拓扑排序
        topo = []
        visited = set()

        def build_topo(v):
            if v not in visited:
                visited.add(v)
                for child in v._prev:
                    build_topo(child)
                topo.append(v)

        build_topo(self)
        self.grad = np.ones_like(self.data)

        for v in reversed(topo):
            v._backward()


# 基本运算
a = Tensor([2.0], requires_grad=True)
b = Tensor([3.0], requires_grad=True)
c = a * b + a ** 2       # c = 2*3 + 2^2 = 10
print(f"  a={a.data}, b={b.data}")
print(f"  c = a*b + a^2 = {c.data}")

c.backward()
print(f"  dc/da = {a.grad} (应为 3 + 2*2 = 7)")
print(f"  dc/db = {b.grad} (应为 2)")

# 复杂计算图
x = Tensor([1.5], requires_grad=True)
y = Tensor([2.0], requires_grad=True)
z = (x * y + x ** 3).sum()
print(f"\n  z = x*y + x^3 = {z.data}")
z.backward()
print(f"  dz/dx = {x.grad} (应为 y + 3x^2 = 2 + 3*2.25 = 8.75)")
print(f"  dz/dy = {y.grad} (应为 x = 1.5)")

# ============================================================
# 2. 神经网络层（从零实现）
# ============================================================
print("\n\n【2. 神经网络层实现】")


class Linear:
    """全连接层: y = xW^T + b"""

    def __init__(self, in_features, out_features):
        # Xavier 初始化
        limit = np.sqrt(6 / (in_features + out_features))
        self.W = np.random.uniform(-limit, limit, (out_features, in_features))
        self.b = np.zeros(out_features)
        self.dW = None
        self.db = None
        self._input = None

    def forward(self, x):
        self._input = x
        return x @ self.W.T + self.b

    def backward(self, grad_output):
        self.dW = grad_output.T @ self._input
        self.db = grad_output.sum(axis=0)
        return grad_output @ self.W


class ReLU:
    """ReLU 激活函数"""

    def __init__(self):
        self._mask = None

    def forward(self, x):
        self._mask = (x > 0)
        return x * self._mask

    def backward(self, grad_output):
        return grad_output * self._mask


class Sigmoid:
    """Sigmoid 激活函数"""

    def __init__(self):
        self._output = None

    def forward(self, x):
        self._output = 1 / (1 + np.exp(-np.clip(x, -500, 500)))
        return self._output

    def backward(self, grad_output):
        return grad_output * self._output * (1 - self._output)


class Sequential:
    """模型容器"""

    def __init__(self, *layers):
        self.layers = layers

    def forward(self, x):
        for layer in self.layers:
            x = layer.forward(x)
        return x

    def backward(self, grad):
        for layer in reversed(self.layers):
            grad = layer.backward(grad)
        return grad

    def parameters(self):
        params = []
        for layer in self.layers:
            if hasattr(layer, 'W'):
                params.append(('W', layer))
                params.append(('b', layer))
        return params


# 构建模型
np.random.seed(42)
model = Sequential(
    Linear(2, 16),
    ReLU(),
    Linear(16, 8),
    ReLU(),
    Linear(8, 1),
    Sigmoid(),
)

# 生成数据（XOR问题）
X_data = np.array([[0, 0], [0, 1], [1, 0], [1, 1]], dtype=np.float64)
y_data = np.array([[0], [1], [1], [0]], dtype=np.float64)

print(f"  模型结构: 2 → 16 (ReLU) → 8 (ReLU) → 1 (Sigmoid)")
print(f"  训练 XOR 问题: {X_data.tolist()} → {y_data.flatten().tolist()}")

# 训练
lr = 0.5
for epoch in range(500):
    # 前向传播
    output = model.forward(X_data)

    # 二元交叉熵损失
    loss = -np.mean(y_data * np.log(output + 1e-8) + (1 - y_data) * np.log(1 - output + 1e-8))

    # 反向传播
    grad = (output - y_data) / (output * (1 - output) + 1e-8) / len(y_data)
    model.backward(grad)

    # 梯度下降
    for name, layer in model.parameters():
        if name == 'W':
            layer.W -= lr * layer.dW
        else:
            layer.b -= lr * layer.db

    if (epoch + 1) % 100 == 0:
        predictions = (output > 0.5).astype(int)
        accuracy = np.mean(predictions == y_data)
        print(f"  Epoch {epoch+1:3d} | Loss: {loss:.4f} | Acc: {accuracy:.0%} | Pred: {predictions.flatten().tolist()}")

# ============================================================
# 3. CNN 概念演示
# ============================================================
print("\n\n【3. CNN 卷积操作演示】")


def conv2d(input_matrix, kernel, stride=1, padding=0):
    """
    简化版 2D 卷积
    input_matrix: (H, W)
    kernel: (kH, kW)
    """
    H, W = input_matrix.shape
    kH, kW = kernel.shape

    # 填充
    if padding > 0:
        padded = np.zeros((H + 2 * padding, W + 2 * padding))
        padded[padding:padding + H, padding:padding + W] = input_matrix
    else:
        padded = input_matrix

    pH, pW = padded.shape
    out_H = (pH - kH) // stride + 1
    out_W = (pW - kW) // stride + 1
    output = np.zeros((out_H, out_W))

    for i in range(out_H):
        for j in range(out_W):
            region = padded[i * stride:i * stride + kH, j * stride:j * stride + kW]
            output[i, j] = np.sum(region * kernel)

    return output


def max_pool2d(input_matrix, pool_size=2):
    """简化版最大池化"""
    H, W = input_matrix.shape
    out_H = H // pool_size
    out_W = W // pool_size
    output = np.zeros((out_H, out_W))

    for i in range(out_H):
        for j in range(out_W):
            region = input_matrix[i * pool_size:(i + 1) * pool_size,
                                  j * pool_size:(j + 1) * pool_size]
            output[i, j] = region.max()

    return output


# 示例图像（5x5）
image = np.array([
    [1, 2, 0, 1, 3],
    [0, 1, 2, 3, 1],
    [1, 3, 1, 0, 2],
    [2, 0, 3, 1, 1],
    [3, 1, 0, 2, 0],
], dtype=np.float64)

# 边缘检测卷积核
edge_kernel = np.array([
    [-1, -1, -1],
    [-1,  8, -1],
    [-1, -1, -1],
], dtype=np.float64)

# 模糊卷积核
blur_kernel = np.ones((3, 3)) / 9

print(f"  输入图像 (5x5):")
print(f"  {image.tolist()}")

# 卷积
conv_result = conv2d(image, edge_kernel, padding=1)
print(f"\n  边缘检测结果 (5x5, padding=1):")
print(f"  {conv_result.round(1).tolist()}")

# 池化
conv_no_pad = conv2d(image, blur_kernel, padding=0)  # 3x3
pooled = max_pool2d(conv_no_pad, pool_size=2)  # 需要3x3+ 才能池化
print(f"\n  模糊卷积 (3x3): {conv_no_pad.round(2).tolist()}")

# 更大的图像演示池化
large_image = np.random.rand(6, 6)
pooled_large = max_pool2d(large_image, pool_size=2)
print(f"\n  6x6 图像 → 2x2 最大池化: {pooled_large.shape}")

# ============================================================
# 4. 自注意力机制（简化）
# ============================================================
print("\n\n【4. 自注意力机制（Self-Attention）】")


def self_attention(Q, K, V):
    """
    缩放点积注意力
    Q, K, V: (seq_len, d_k)
    Attention(Q,K,V) = softmax(QK^T / sqrt(d_k)) * V
    """
    d_k = Q.shape[-1]

    # 1. 注意力分数: QK^T / sqrt(d_k)
    scores = Q @ K.T / np.sqrt(d_k)

    # 2. Softmax
    exp_scores = np.exp(scores - scores.max(axis=-1, keepdims=True))  # 数值稳定
    attention_weights = exp_scores / exp_scores.sum(axis=-1, keepdims=True)

    # 3. 加权求和
    output = attention_weights @ V

    return output, attention_weights


# 示例：4个词，每个词用3维向量表示
words = ["我", "喜欢", "深度", "学习"]
Q = np.array([
    [1.0, 0.2, 0.1],
    [0.1, 1.0, 0.3],
    [0.2, 0.1, 1.0],
    [0.3, 0.2, 0.8],
])
K = Q.copy()
V = np.array([
    [0.9, 0.1, 0.2],
    [0.2, 0.8, 0.3],
    [0.1, 0.3, 0.9],
    [0.4, 0.1, 0.7],
])

output, attn_weights = self_attention(Q, K, V)

print(f"  输入词: {words}")
print(f"  注意力权重矩阵:")
for i, word in enumerate(words):
    weights_str = " ".join([f"{w:.3f}" for w in attn_weights[i]])
    print(f"    '{word}' 关注: [{weights_str}]")
print(f"  注意力输出:")
for i, word in enumerate(words):
    print(f"    '{word}' → {output[i].round(3)}")

# ============================================================
# 5. 位置编码
# ============================================================
print("\n\n【5. 位置编码（Positional Encoding）】")


def positional_encoding(max_len, d_model):
    """正弦-余弦位置编码"""
    pe = np.zeros((max_len, d_model))
    for pos in range(max_len):
        for i in range(0, d_model, 2):
            pe[pos, i] = np.sin(pos / (10000 ** (i / d_model)))
            if i + 1 < d_model:
                pe[pos, i + 1] = np.cos(pos / (10000 ** (i / d_model)))
    return pe


pe = positional_encoding(max_len=10, d_model=8)
print(f"  位置编码矩阵 (10x8):")
print(f"  行=位置, 列=维度")
for pos in range(min(5, 10)):
    print(f"  pos={pos}: {pe[pos].round(3).tolist()}")

# ============================================================
# 6. 训练流程总结
# ============================================================
print("\n\n【6. PyTorch 训练流程模板】")

training_template = """
# PyTorch 标准训练流程
import torch
import torch.nn as nn
import torch.optim as optim

# 1. 定义模型
class MyModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.layer1 = nn.Linear(784, 256)
        self.layer2 = nn.Linear(256, 10)

    def forward(self, x):
        x = torch.relu(self.layer1(x))
        return self.layer2(x)

model = MyModel()

# 2. 定义损失函数和优化器
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

# 3. 训练循环
for epoch in range(num_epochs):
    model.train()
    for batch_X, batch_y in train_loader:
        optimizer.zero_grad()           # 清零梯度
        outputs = model(batch_X)        # 前向传播
        loss = criterion(outputs, batch_y)  # 计算损失
        loss.backward()                 # 反向传播
        optimizer.step()                # 更新参数

    # 4. 评估
    model.eval()
    with torch.no_grad():
        correct = 0
        for batch_X, batch_y in test_loader:
            outputs = model(batch_X)
            _, predicted = outputs.max(1)
            correct += predicted.eq(batch_y).sum().item()
        print(f"Accuracy: {correct / len(test_dataset):.2%}")
"""
print(training_template)

print("\n" + "=" * 60)
print("深度学习示例运行完毕！")
print("=" * 60)
