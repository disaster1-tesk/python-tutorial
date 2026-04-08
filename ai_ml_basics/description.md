# Python AI/ML 基础

## 1. NumPy 科学计算

### 知识点解析

**概念定义**：NumPy（Numerical Python）是 Python 科学计算的基础库，提供高性能的多维数组对象和丰富的数学函数。几乎所有 AI/ML 框架（TensorFlow、PyTorch、scikit-learn）都基于或兼容 NumPy。

**核心概念**：
- **ndarray**：N 维数组，同类型元素的网格，是 NumPy 的核心数据结构
- **广播（Broadcasting）**：不同形状数组之间运算的自动扩展规则
- **向量化运算**：避免 Python 循环，用 C 层级的批量运算提升性能
- **索引与切片**：高级索引、布尔索引、花式索引
- **轴（axis）**：多维数组操作的方向，axis=0 按列，axis=1 按行

**核心规则**：
1. 创建数组：`np.array()`、`np.zeros()`、`np.ones()`、`np.arange()`、`np.linspace()`
2. 形状操作：`reshape()`、`T`（转置）、`flatten()`、`np.expand_dims()`
3. 数学运算：`+` `-` `*` `/` 是元素级运算，`@` 或 `np.dot()` 是矩阵乘法
4. 聚合：`sum()`、`mean()`、`std()`、`max()`、`argmax()`，通过 `axis` 控制方向
5. 布尔索引：`arr[arr > 0]` 提取满足条件的元素

**常见易错点**：
1. `reshape(-1)` 自动推断维度，但元素总数必须匹配
2. `np.array([1, 2, 3])` 的 shape 是 `(3,)` 而不是 `(3, 1)`——注意一维数组的形状
3. `*` 是元素乘法，矩阵乘法用 `@`（Python 3.5+）或 `np.dot()`
4. 浮点数比较用 `np.allclose()` 或 `np.isclose()`，不要用 `==`
5. `arr[[1, 3]]` 是花式索引（返回副本），`arr[1:3]` 是切片（返回视图）

### 实战案例

#### 案例1：NumPy 核心操作
```python
import numpy as np

# ========== 数组创建 ==========
arr1d = np.array([1, 2, 3, 4, 5])
arr2d = np.array([[1, 2, 3], [4, 5, 6]])      # shape (2, 3)
zeros = np.zeros((3, 4))                        # 3行4列全0
ones = np.ones((2, 3))                          # 全1
random = np.random.randn(3, 3)                  # 标准正态分布
eye = np.eye(3)                                 # 单位矩阵
arange = np.arange(0, 1, 0.1)                  # [0, 0.1, 0.2, ..., 0.9]

# ========== 形状操作 ==========
arr = np.arange(12)                              # [0, 1, ..., 11]
reshaped = arr.reshape(3, 4)                     # 3行4列
reshaped_t = reshaped.T                          # 转置：4行3列
flattened = reshaped.flatten()                   # 展平为一维
expanded = np.expand_dims(arr1d, axis=1)         # (5,) -> (5, 1)

# ========== 数学运算 ==========
a = np.array([1, 2, 3])
b = np.array([4, 5, 6])

element_mul = a * b           # [4, 10, 18]  元素乘法
dot_product = a @ b           # 32            点积（内积）
outer_product = np.outer(a, b)                # 外积

# 矩阵运算
mat_a = np.array([[1, 2], [3, 4]])
mat_b = np.array([[5, 6], [7, 8]])
mat_mul = mat_a @ mat_b                     # 矩阵乘法
mat_inv = np.linalg.inv(mat_a)              # 逆矩阵
det = np.linalg.det(mat_a)                  # 行列式

# ========== 统计运算 ==========
data = np.random.randn(100, 3)  # 100个样本，3个特征

print(f"均值（每列）: {data.mean(axis=0)}")        # shape (3,)
print(f"标准差（每行）: {data.std(axis=1)[:5]}")    # shape (100,)
print(f"最大值索引: {data.argmax(axis=1)[:5]}")      # 每行最大值的位置

# ========== 布尔索引与过滤 ==========
scores = np.array([85, 92, 78, 95, 60, 88])
passed = scores[scores >= 80]                        # [85, 92, 95, 88]
top_3 = scores[np.argsort(scores)[-3:]]              # 排序后取前3

# ========== 广播 ==========
mat = np.array([[1, 2, 3], [4, 5, 6]])    # (2, 3)
row_vec = np.array([10, 20, 30])            # (3,)
result = mat + row_vec                      # (2,3)+(3,) -> (2,3) 自动广播
# 结果: [[11, 22, 33], [14, 25, 36]]
```

---

## 2. Pandas 数据处理

### 知识点解析

**概念定义**：Pandas 是 Python 数据分析和处理的核心库，提供 DataFrame（二维表格）和 Series（一维序列）两种数据结构。

**核心概念**：
- **DataFrame**：二维表格数据，类似 Excel 表格或 SQL 表
- **Series**：一维数组，带标签索引
- **索引（Index）**：行标签和列标签，支持层级索引
- **分组聚合**：`groupby()` + 聚合函数，类似 SQL 的 GROUP BY
- **时间序列**：DatetimeIndex，支持时间范围、重采样、移动窗口

**核心规则**：
1. `df.loc[row_label, col_label]` 基于标签索引，`df.iloc[row_pos, col_pos]` 基于位置索引
2. `df.query()` 用字符串表达式过滤，`df[df['col'] > value]` 用布尔索引过滤
3. `groupby().agg()` 同时应用多个聚合函数
4. `pd.merge()` 合并表（类似 SQL JOIN），`pd.concat()` 拼接表
5. 缺失值处理：`fillna()` 填充、`dropna()` 删除、`isna()` 检测

### 实战案例

#### 案例1：数据分析完整流程
```python
import pandas as pd
import numpy as np

# ========== 创建数据 ==========
data = {
    '姓名': ['张三', '李四', '王五', '赵六', '张三', '李四', '王五'],
    '科目': ['数学', '数学', '数学', '数学', '英语', '英语', '英语'],
    '成绩': [85, 92, 78, None, 95, 88, 72],
    '班级': ['A', 'A', 'B', 'A', 'B', 'B', 'A']
}
df = pd.DataFrame(data)

# ========== 数据清洗 ==========
# 处理缺失值
df['成绩'] = df['成绩'].fillna(df['成绩'].mean())

# ========== 分组聚合 ==========
# 每人的平均成绩
avg_by_student = df.groupby('姓名')['成绩'].agg(['mean', 'max', 'min', 'count'])
print(avg_by_student)

# 每个班级每个科目的平均成绩
pivot = df.pivot_table(values='成绩', index='班级', columns='科目', aggfunc='mean')
print(pivot)

# ========== 数据筛选 ==========
# 成绩大于80的记录
good_scores = df[df['成绩'] > 80]

# ========== 排序 ==========
top_students = df.sort_values('成绩', ascending=False).head(5)
```

---

## 3. Scikit-learn 传统机器学习

### 知识点解析

**概念定义**：Scikit-learn 是 Python 最流行的传统机器学习库，提供分类、回归、聚类、降维、模型选择等完整工具链。

**核心概念**：
- **监督学习**：有标签数据训练，包括分类（Classification）和回归（Regression）
- **无监督学习**：无标签数据，包括聚类（Clustering）和降维（Dimensionality Reduction）
- **特征工程**：数据预处理、特征选择、特征提取
- **模型评估**：交叉验证、指标计算、超参数调优
- **Pipeline**：将预处理和模型训练串联为工作流

**核心规则**：
1. 所有模型的 API 统一：`fit(X, y)` 训练、`predict(X)` 预测、`score(X, y)` 评估
2. 数据拆分：`train_test_split(X, y, test_size=0.2)`，训练集80%，测试集20%
3. 预处理：数值特征用 `StandardScaler` 标准化，类别特征用 `OneHotEncoder` 编码
4. 分类评估指标：accuracy（准确率）、precision（精确率）、recall（召回率）、F1-score
5. 回归评估指标：MSE、RMSE、R²（决定系数）
6. 防止过拟合：交叉验证、正则化、early stopping

**常见易错点**：
1. 预处理只用 `fit_transform()` 在训练集上，测试集只用 `transform()`
2. `train_test_split` 要设置 `random_state` 保证可复现
3. 类别不平衡时 accuracy 有误导性，看 precision/recall/F1
4. 特征缩放对 SVM、KNN、神经网络很重要，对决策树类不需要
5. 数据泄露：在拆分之前做预处理会泄露测试集信息

### 实战案例

#### 案例1：分类任务完整流程
```python
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.svm import SVC
from sklearn.metrics import (classification_report, confusion_matrix,
                               accuracy_score, roc_auc_score)
from sklearn.pipeline import Pipeline
import numpy as np

# ========== 1. 生成模拟数据 ==========
X, y = make_classification(
    n_samples=1000, n_features=20, n_informative=10,
    n_redundant=5, random_state=42
)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# ========== 2. 构建Pipeline ==========
# Pipeline = 预处理 + 模型，确保训练和测试用同样的预处理
pipeline = Pipeline([
    ('scaler', StandardScaler()),
    ('classifier', LogisticRegression(max_iter=1000))
])

# ========== 3. 训练与评估 ==========
pipeline.fit(X_train, y_train)
y_pred = pipeline.predict(X_test)

print(f"准确率: {accuracy_score(y_test, y_pred):.4f}")
print(f"分类报告:\n{classification_report(y_test, y_pred)}")

# ========== 4. 交叉验证 ==========
cv_scores = cross_val_score(pipeline, X_train, y_train, cv=5)
print(f"5折交叉验证: {cv_scores.mean():.4f} ± {cv_scores.std():.4f}")

# ========== 5. 超参数调优 ==========
param_grid = {
    'classifier__C': [0.1, 1, 10],
    'classifier__penalty': ['l2'],
}
grid_search = GridSearchCV(pipeline, param_grid, cv=5, scoring='f1')
grid_search.fit(X_train, y_train)
print(f"最佳参数: {grid_search.best_params_}")
print(f"最佳F1: {grid_search.best_score_:.4f}")

# ========== 6. 多模型对比 ==========
models = {
    'Logistic Regression': LogisticRegression(max_iter=1000),
    'Random Forest': RandomForestClassifier(n_estimators=100),
    'Gradient Boosting': GradientBoostingClassifier(n_estimators=100),
    'SVM': SVC(),
}

for name, model in models.items():
    pipe = Pipeline([('scaler', StandardScaler()), ('clf', model)])
    scores = cross_val_score(pipe, X_train, y_train, cv=5, scoring='accuracy')
    print(f"{name:25s}: {scores.mean():.4f} ± {scores.std():.4f}")
```

#### 案例2：回归任务
```python
from sklearn.datasets import make_regression
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error

# 生成回归数据
X, y = make_regression(n_samples=500, n_features=10, noise=15, random_state=42)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 训练模型
model = LinearRegression()
model.fit(X_train, y_train)
y_pred = model.predict(X_test)

print(f"MSE:  {mean_squared_error(y_test, y_pred):.2f}")
print(f"RMSE: {np.sqrt(mean_squared_error(y_test, y_pred)):.2f}")
print(f"MAE:  {mean_absolute_error(y_test, y_pred):.2f}")
print(f"R²:   {r2_score(y_test, y_pred):.4f}")

# 正则化回归
ridge = Ridge(alpha=1.0)
lasso = Lasso(alpha=1.0)

for name, model in [('Ridge', ridge), ('Lasso', lasso)]:
    model.fit(X_train, y_train)
    score = r2_score(y_test, model.predict(X_test))
    print(f"{name} R²: {score:.4f}")
```

---

## 4. 数据预处理与特征工程

### 知识点解析

**核心概念**：
- **标准化（StandardScaler）**：将特征转换为均值0、标准差1的分布
- **归一化（MinMaxScaler）**：将特征缩放到 [0, 1] 范围
- **独热编码（OneHotEncoder）**：将类别特征转换为二进制向量
- **标签编码（LabelEncoder）**：将类别标签转换为整数
- **特征选择**：选择最有信息量的特征
- **降维（PCA）**：主成分分析，减少特征维度

### 实战案例

```python
from sklearn.preprocessing import StandardScaler, MinMaxScaler, OneHotEncoder, LabelEncoder
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.decomposition import PCA
import numpy as np

# ========== 数值特征处理 ==========
numeric_data = np.array([[100, 200], [150, 250], [200, 300]])

# 标准化：均值0，标准差1
scaler = StandardScaler()
standardized = scaler.fit_transform(numeric_data)

# 归一化：缩放到[0,1]
minmax = MinMaxScaler()
normalized = minmax.fit_transform(numeric_data)

# ========== 类别特征处理 ==========
categories = ['红色', '蓝色', '绿色', '红色', '蓝色']

# 独热编码
encoder = OneHotEncoder(sparse_output=False)
one_hot = encoder.fit_transform(np.array(categories).reshape(-1, 1))
print(f"独热编码:\n{one_hot}")

# 标签编码
label_enc = LabelEncoder()
labels = label_enc.fit_transform(categories)
print(f"标签编码: {labels}")  # [2, 1, 0, 2, 1]

# ========== 特征选择 ==========
X, y = make_classification(n_samples=100, n_features=20, n_informative=5, random_state=42)
selector = SelectKBest(f_classif, k=5)
X_selected = selector.fit_transform(X, y)
print(f"原始特征数: {X.shape[1]}, 选择后: {X_selected.shape[1]}")

# ========== PCA 降维 ==========
pca = PCA(n_components=0.95)  # 保留95%方差
X_pca = pca.fit_transform(X)
print(f"原始维度: {X.shape[1]}, PCA后: {X_pca.shape[1]}, 方差解释: {pca.explained_variance_ratio_.sum():.2%}")
```

---

## 5. 模型评估与调优

### 知识点解析

**核心概念**：
- **过拟合 vs 欠拟合**：过拟合=训练好测试差，欠拟合=训练和测试都差
- **偏差-方差权衡**：模型复杂度的平衡
- **交叉验证**：K-Fold、Stratified K-Fold
- **学习曲线**：随训练数据量变化的性能曲线
- **网格搜索 vs 随机搜索**：超参数优化策略

### 实战案例

```python
from sklearn.model_selection import learning_curve, validation_curve
import matplotlib.pyplot as plt

# 学习曲线：诊断过拟合/欠拟合
train_sizes, train_scores, test_scores = learning_curve(
    pipeline, X_train, y_train, cv=5,
    train_sizes=np.linspace(0.1, 1.0, 10),
    scoring='accuracy'
)

# 分析：
# - 如果训练分高、测试分低 → 过拟合（增加数据、减少复杂度、正则化）
# - 如果训练分和测试分都低 → 欠拟合（增加特征、增加模型复杂度）
# - 如果两者都高且接近 → 理想状态
```

---

## 6. 无监督学习

### 知识点解析

**核心概念**：
- **K-Means 聚类**：基于距离的划分聚类算法
- **DBSCAN**：基于密度的聚类，能发现任意形状的簇
- **层次聚类**：构建聚类树（树状图）
- **PCA**：主成分分析，线性降维
- **t-SNE**：非线性降维，常用于高维数据可视化

### 实战案例

```python
from sklearn.cluster import KMeans, DBSCAN
from sklearn.metrics import silhouette_score

# K-Means 聚类
kmeans = KMeans(n_clusters=3, random_state=42)
labels = kmeans.fit_predict(X)

# 轮廓系数评估（越接近1越好）
score = silhouette_score(X, labels)
print(f"轮廓系数: {score:.4f}")

# 肘部法则选择最优K值
inertias = []
for k in range(2, 10):
    km = KMeans(n_clusters=k, random_state=42)
    km.fit(X)
    inertias.append(km.inertia_)
# 画图找"拐点"即最优K
```

## 学习建议

1. **NumPy 是基础中的基础**：AI/ML 的所有计算都基于矩阵运算，NumPy 必须熟练
2. **Pandas 用于数据探索**：拿到数据先用 Pandas 看看长什么样（`df.head()`、`df.describe()`、`df.info()`）
3. **Scikit-learn 入门 ML 的最佳选择**：API 统一、文档完善、社区活跃
4. **掌握 Pipeline**：将预处理和模型打包，避免数据泄露，代码更整洁
5. **先跑通 Baseline 再优化**：先用简单模型建立基准，再逐步优化
6. **重视特征工程**：好的特征比复杂模型更重要
