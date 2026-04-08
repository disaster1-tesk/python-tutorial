"""
Python AI/ML 基础完整示例
演示内容：
1. NumPy：数组操作、广播、向量化计算
2. Pandas：DataFrame 创建、数据清洗、分组聚合
3. Scikit-learn：分类、回归、聚类完整流程
4. 特征工程：标准化、编码、降维
5. 模型评估：交叉验证、学习曲线分析
"""

import numpy as np

print("=" * 60)
print("Python AI/ML 基础完整示例")
print("=" * 60)

# ============================================================
# 1. NumPy 核心操作
# ============================================================
print("\n【1. NumPy 数组操作】")

# 数组创建
arr = np.array([1, 2, 3, 4, 5])
matrix = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
print(f"  一维数组: {arr}, shape={arr.shape}, dtype={arr.dtype}")
print(f"  二维数组:\n{matrix}")
print(f"  shape={matrix.shape}, ndim={matrix.ndim}")

# 特殊数组
print(f"\n  全零数组: {np.zeros((2, 3))}")
print(f"  全一数组: {np.ones((2, 2))}")
print(f"  单位矩阵:\n{np.eye(3)}")
print(f"  等差数组: {np.arange(0, 1, 0.2)}")
print(f"  等分数组: {np.linspace(0, 1, 5)}")
print(f"  随机数组: {np.random.randn(3, 3).round(2)}")

# 形状操作
print(f"\n  reshape(3,2): {arr.reshape(3, 2).tolist()}")
print(f"  转置:\n{matrix.T}")
print(f"  展平: {matrix.flatten()}")
print(f"  增加维度: shape {np.expand_dims(arr, axis=1).shape}")

# 数学运算
a = np.array([1, 2, 3])
b = np.array([4, 5, 6])
print(f"\n  a={a}, b={b}")
print(f"  元素乘法 a*b: {a * b}")
print(f"  点积 a@b: {a @ b}")
print(f"  外积:\n{np.outer(a, b)}")

# 矩阵运算
m1 = np.array([[1, 2], [3, 4]])
m2 = np.array([[5, 6], [7, 8]])
print(f"\n  矩阵乘法 m1@m2:\n{m1 @ m2}")
print(f"  逆矩阵:\n{np.linalg.inv(m1).round(2)}")
print(f"  行列式: {np.linalg.det(m1):.0f}")
print(f"  特征值: {np.linalg.eigvals(m1).round(2)}")

# 统计运算
data = np.array([12, 15, 18, 22, 25, 28, 30, 35, 40, 45])
print(f"\n  数据: {data}")
print(f"  均值: {data.mean():.1f}")
print(f"  中位数: {np.median(data):.1f}")
print(f"  标准差: {data.std():.2f}")
print(f"  最大值: {data.max()}, 最小值: {data.min()}")
print(f"  最大值索引: {data.argmax()}")
print(f"  求和: {data.sum()}, 累积和: {data.cumsum()}")

# 广播
mat = np.array([[1], [2], [3]])   # shape (3, 1)
vec = np.array([10, 20, 30])       # shape (3,)
print(f"\n  广播 (3,1) + (3,) -> (3,3):\n{mat + vec}")

# 布尔索引
scores = np.array([85, 42, 91, 67, 78, 95, 33, 88])
print(f"\n  成绩: {scores}")
print(f"  >=80: {scores[scores >= 80]}")
print(f"  前3名: {scores[np.argsort(scores)[-3:]]}")
print(f"  排名: {np.argsort(np.argsort(-scores)) + 1}")

# ============================================================
# 2. Pandas 数据处理（模拟实现核心概念）
# ============================================================
print("\n\n【2. Pandas DataFrame 核心概念】")


class SimpleDataFrame:
    """简化版 DataFrame——演示核心概念"""

    def __init__(self, data: dict):
        self.columns = list(data.keys())
        self.data = []
        n_rows = len(data[self.columns[0]])
        for i in range(n_rows):
            row = {col: data[col][i] for col in self.columns}
            self.data.append(row)

    def __repr__(self):
        lines = [str(self.columns)]
        for row in self.data:
            lines.append([str(row[col]) for col in self.columns])
        return str(lines)

    def filter(self, condition):
        """类似 df[df['col'] > value]"""
        return [row for row in self.data if condition(row)]

    def groupby(self, key):
        """类似 df.groupby('col')"""
        groups = {}
        for row in self.data:
            k = row[key]
            groups.setdefault(k, []).append(row)
        return groups

    def sort_values(self, key, ascending=True):
        return sorted(self.data, key=lambda x: x[key], reverse=not ascending)


# 创建数据
df = SimpleDataFrame({
    '姓名': ['张三', '李四', '王五', '赵六', '张三', '李四', '王五', '赵六'],
    '科目': ['数学', '数学', '数学', '数学', '英语', '英语', '英语', '英语'],
    '成绩': [85, 92, 78, 60, 95, 88, 72, 83],
    '班级': ['A', 'A', 'B', 'A', 'B', 'B', 'A', 'B']
})

# 过滤
high_scores = df.filter(lambda r: r['成绩'] >= 85)
print(f"  成绩>=85: {len(high_scores)} 条")
for r in high_scores:
    print(f"    {r['姓名']} - {r['科目']}: {r['成绩']}")

# 分组聚合
groups = df.groupby('姓名')
print(f"\n  按姓名分组:")
for name, rows in groups.items():
    avg = sum(r['成绩'] for r in rows) / len(rows)
    print(f"    {name}: 平均分={avg:.1f}, 考试次数={len(rows)}")

# 排序
top3 = df.sort_values('成绩', ascending=False)[:3]
print(f"\n  成绩前3:")
for r in top3:
    print(f"    {r['姓名']} - {r['科目']}: {r['成绩']}")

# ============================================================
# 3. Scikit-learn 风格的模型训练（模拟）
# ============================================================
print("\n\n【3. 机器学习模型训练流程】")


# 线性回归实现
class LinearRegression:
    """简化版线性回归（梯度下降法）"""

    def __init__(self, learning_rate=0.01, n_iterations=1000):
        self.lr = learning_rate
        self.n_iter = n_iterations
        self.weights = None
        self.bias = None

    def fit(self, X, y):
        n_samples, n_features = X.shape
        self.weights = np.zeros(n_features)
        self.bias = 0.0

        for _ in range(self.n_iter):
            y_pred = X @ self.weights + self.bias
            error = y_pred - y

            self.weights -= self.lr * (2 / n_samples) * (X.T @ error)
            self.bias -= self.lr * (2 / n_samples) * error.sum()

    def predict(self, X):
        return X @ self.weights + self.bias

    def score(self, X, y):
        """R² 分数"""
        y_pred = self.predict(X)
        ss_res = np.sum((y - y_pred) ** 2)
        ss_tot = np.sum((y - y.mean()) ** 2)
        return 1 - (ss_res / ss_tot)


# KNN 分类器实现
class KNNClassifier:
    """简化版 KNN 分类器"""

    def __init__(self, k=3):
        self.k = k
        self.X_train = None
        self.y_train = None

    def fit(self, X, y):
        self.X_train = X
        self.y_train = y

    def predict(self, X):
        predictions = []
        for x in X:
            # 计算距离
            distances = np.sqrt(np.sum((self.X_train - x) ** 2, axis=1))
            # 找最近的k个
            k_indices = np.argsort(distances)[:self.k]
            k_labels = self.y_train[k_indices]
            # 多数投票
            unique, counts = np.unique(k_labels, return_counts=True)
            predictions.append(unique[np.argmax(counts)])
        return np.array(predictions)

    def score(self, X, y):
        y_pred = self.predict(X)
        return np.mean(y_pred == y)


# 生成模拟数据
np.random.seed(42)

# 回归数据：y = 3x1 + 5x2 + 10 + noise
X_reg = np.random.randn(200, 2)
y_reg = 3 * X_reg[:, 0] + 5 * X_reg[:, 1] + 10 + np.random.randn(200) * 0.5

# 分类数据：两个簇
X_cls_0 = np.random.randn(50, 2) + np.array([-2, -2])
X_cls_1 = np.random.randn(50, 2) + np.array([2, 2])
X_cls = np.vstack([X_cls_0, X_cls_1])
y_cls = np.array([0] * 50 + [1] * 50)

# 拆分训练集和测试集
def train_test_split(X, y, test_size=0.2):
    n = len(X)
    indices = np.random.permutation(n)
    split = int(n * (1 - test_size))
    return X[indices[:split]], X[indices[split:]], y[indices[:split]], y[indices[split:]]

# ====== 回归任务 ======
print("  --- 线性回归 ---")
X_train, X_test, y_train, y_test = train_test_split(X_reg, y_reg)

lr = LinearRegression(learning_rate=0.01, n_iterations=1000)
lr.fit(X_train, y_train)
y_pred = lr.predict(X_test)

mse = np.mean((y_test - y_pred) ** 2)
r2 = lr.score(X_test, y_test)
print(f"  权重: {lr.weights.round(4)}")
print(f"  偏置: {lr.bias:.4f}")
print(f"  MSE:  {mse:.4f}")
print(f"  R²:   {r2:.4f}")

# ====== 分类任务 ======
print("\n  --- KNN 分类 ---")
X_train, X_test, y_train, y_test = train_test_split(X_cls, y_cls)

for k in [1, 3, 5, 7]:
    knn = KNNClassifier(k=k)
    knn.fit(X_train, y_train)
    accuracy = knn.score(X_test, y_test)
    print(f"  K={k}: 准确率={accuracy:.2%}")

# ============================================================
# 4. 特征工程
# ============================================================
print("\n\n【4. 特征工程】")

# 标准化
data = np.array([[10, 200], [20, 300], [30, 100], [40, 500], [50, 400]])

# 手动标准化
mean = data.mean(axis=0)
std = data.std(axis=0)
standardized = (data - mean) / std
print(f"  原始数据均值: {mean}")
print(f"  标准化后均值: {standardized.mean(axis=0).round(4)} (≈0)")
print(f"  标准化后标准差: {standardized.std(axis=0).round(4)} (≈1)")

# Min-Max 归一化
data_min = data.min(axis=0)
data_max = data.max(axis=0)
normalized = (data - data_min) / (data_max - data_min)
print(f"\n  归一化范围: [{normalized.min():.2f}, {normalized.max():.2f}]")

# 独热编码
categories = np.array(['红', '蓝', '绿', '红', '蓝', '绿'])
unique_cats = np.unique(categories)
one_hot = np.zeros((len(categories), len(unique_cats)))
for i, cat in enumerate(categories):
    one_hot[i, np.where(unique_cats == cat)[0][0]] = 1
print(f"\n  类别: {categories.tolist()}")
print(f"  独热编码:\n{one_hot.astype(int)}")

# ============================================================
# 5. K-Means 聚类
# ============================================================
print("\n\n【5. K-Means 聚类算法】")


class KMeansClustering:
    """简化版 K-Means 聚类"""

    def __init__(self, k=3, max_iterations=100):
        self.k = k
        self.max_iter = max_iterations
        self.centroids = None

    def fit(self, X):
        # 随机选择初始中心点
        indices = np.random.choice(len(X), self.k, replace=False)
        self.centroids = X[indices].copy()

        for iteration in range(self.max_iter):
            # 分配簇
            distances = np.zeros((len(X), self.k))
            for i, c in enumerate(self.centroids):
                distances[:, i] = np.sqrt(np.sum((X - c) ** 2, axis=1))
            labels = np.argmin(distances, axis=1)

            # 更新中心点
            new_centroids = np.zeros_like(self.centroids)
            for i in range(self.k):
                members = X[labels == i]
                if len(members) > 0:
                    new_centroids[i] = members.mean(axis=0)

            # 收敛检查
            if np.allclose(self.centroids, new_centroids):
                print(f"  在第 {iteration + 1} 次迭代后收敛")
                break
            self.centroids = new_centroids

        return labels

    def predict(self, X):
        distances = np.zeros((len(X), self.k))
        for i, c in enumerate(self.centroids):
            distances[:, i] = np.sqrt(np.sum((X - c) ** 2, axis=1))
        return np.argmin(distances, axis=1)


# 生成3个簇的数据
cluster1 = np.random.randn(30, 2) + np.array([0, 0])
cluster2 = np.random.randn(30, 2) + np.array([5, 5])
cluster3 = np.random.randn(30, 2) + np.array([0, 5])
X_clusters = np.vstack([cluster1, cluster2, cluster3])

kmeans = KMeansClustering(k=3, max_iterations=100)
labels = kmeans.fit(X_clusters)

print(f"  聚类中心:\n{kmeans.centroids.round(2)}")
print(f"  各簇样本数: {np.bincount(labels)}")

# 肘部法则
print("\n  肘部法则（寻找最优K值）:")
for k in range(2, 7):
    km = KMeansClustering(k=k)
    labels_k = km.fit(X_clusters)
    # 计算惯性（所有样本到其簇中心的距离之和）
    inertia = sum(
        np.sum((X_clusters[labels_k == i] - km.centroids[i]) ** 2)
        for i in range(k)
    )
    print(f"    K={k}: 惯性={inertia:.2f}")

# ============================================================
# 6. 交叉验证
# ============================================================
print("\n\n【6. 交叉验证】")


class CrossValidator:
    """简化版 K-Fold 交叉验证"""

    @staticmethod
    def kfold_split(n_samples, k=5):
        """生成 K-Fold 索引"""
        indices = np.arange(n_samples)
        np.random.shuffle(indices)
        fold_sizes = np.full(k, n_samples // k)
        fold_sizes[:n_samples % k] += 1

        current = 0
        for fold_size in fold_sizes:
            val_idx = indices[current:current + fold_size]
            train_idx = np.concatenate([indices[:current], indices[current + fold_size:]])
            yield train_idx, val_idx
            current += fold_size


# 5折交叉验证评估KNN
knn = KNNClassifier(k=3)
scores = []

for fold, (train_idx, val_idx) in enumerate(CrossValidator.kfold_split(len(X_cls), k=5)):
    X_tr, X_val = X_cls[train_idx], X_cls[val_idx]
    y_tr, y_val = y_cls[train_idx], y_cls[val_idx]
    knn.fit(X_tr, y_tr)
    acc = knn.score(X_val, y_val)
    scores.append(acc)
    print(f"  Fold {fold + 1}: 准确率={acc:.2%}")

print(f"  平均准确率: {np.mean(scores):.2%} ± {np.std(scores):.2%}")

print("\n" + "=" * 60)
print("AI/ML 基础示例运行完毕！")
print("=" * 60)
