# Python 数据处理进阶

## 1. pandas 数据清洗深入

### 知识点解析

**概念定义**：数据清洗是数据分析中最耗时但也最重要的环节（通常占60-80%的时间）。现实世界的数据往往是不完整的（缺失值）、不一致的（格式错误）、有噪声的（异常值）。pandas 提供了强大的数据清洗工具。

**核心规则**：
1. 缺失值处理：`isna()/isnull()` 检测、`fillna()` 填充、`dropna()` 删除
2. 重复值处理：`duplicated()` 检测、`drop_duplicates()` 去重
3. 类型转换：`astype()`、`pd.to_numeric()`、`pd.to_datetime()`
4. 字符串处理：`.str` 访问器（`str.lower()`、`str.contains()`、`str.extract()`）
5. 分组聚合：`groupby()` + `agg()`，支持多种聚合函数

**常见易错点**：
1. `fillna()` 默认不修改原 DataFrame，要用 `inplace=True` 或重新赋值
2. `pd.to_numeric(errors="coerce")` 将无法转换的值设为 NaN，而不是报错
3. `groupby` 后直接取列是 Series，用 `reset_index()` 转回 DataFrame
4. 链式操作注意方法返回的是 Series 还是 DataFrame，避免类型混乱
5. 安装：`pip install pandas`

### 实战案例

#### 案例1：销售数据清洗全流程
```python
# 安装: pip install pandas
import pandas as pd
import numpy as np

print("===pandas 数据清洗深入===")

# 1. 创建"脏"数据（模拟真实场景的常见问题）
data = {
    "订单号": ["ORD-001", "ORD-002", "ORD-003", "ORD-004", "ORD-005",
               "ORD-005", "ORD-006", "ORD-007", "ORD-008", "ORD-009", "ORD-010"],
    "客户":   ["张三", "李四", "王五", "张三", "赵六",
               "赵六", "钱七", "tom", "李四", np.nan, "孙八"],
    "商品":   ["Python书", "键盘", "鼠标", "Python书", "显示器",
               "显示器", "笔记本", "python书", "鼠标", "耳机", "键盘"],
    "数量":   [2, 1, 3, 2, 1, 1, -5, 2, "3", 5, 0],
    "单价":   [89.9, 399.0, 99.0, 89.9, 1299.0, 1299.0, 15.5, 89.9, 99.0, "299", 399.0],
    "日期":   ["2024-01-15", "2024-01-16", "2024/01/17", "2024-01-15",
               "2024-01-18", "2024-01-18", "2024-01-19", "2024-01-20",
               "2024-01-17", "2024-01-21", "abc"],
    "城市":   ["北京", "上海", "北京", "北京", "广州",
               "广州", "深圳", "beijing", "上海", "杭州", "成都"],
}

df = pd.DataFrame(data)
print("原始数据（脏数据）:")
print(df.to_string())
print(f"\n数据形状: {df.shape}")

# 2. 检测数据质量
print("\n===数据质量报告===")
print(f"缺失值统计:\n{df.isna().sum()}")
print(f"重复行数: {df.duplicated().sum()}")
print(f"各列数据类型:\n{df.dtypes}")

# 3. 数据清洗流程
print("\n===清洗步骤===")

# 步骤1：去重（保留第一条）
df_clean = df.drop_duplicates(subset=["订单号"], keep="first")
print(f"去重后: {len(df)} -> {len(df_clean)} 行")

# 步骤2：处理缺失值
df_clean = df_clean.dropna(subset=["客户"])  # 关键字段缺失则删除整行
print(f"去除缺失客户后: {len(df_clean)} 行")

# 步骤3：类型转换（errors="coerce" 遇到无法转换的设为NaN）
df_clean["数量"] = pd.to_numeric(df_clean["数量"], errors="coerce")
df_clean["单价"] = pd.to_numeric(df_clean["单价"], errors="coerce")
df_clean["日期"] = pd.to_datetime(df_clean["日期"], errors="coerce")
print(f"类型转换后:\n{df_clean.dtypes}")

# 步骤4：处理异常值
# 数量不能为负数或0
invalid_qty = df_clean[(df_clean["数量"] <= 0) | df_clean["数量"].isna()]
print(f"无效数量行: {len(invalid_qty)}（数量<=0或非数字）")
df_clean = df_clean[(df_clean["数量"] > 0) & df_clean["数量"].notna()]

# 单价合理性检查
df_clean = df_clean[df_clean["单价"] > 0]
print(f"去除无效数量和单价后: {len(df_clean)} 行")

# 步骤5：日期缺失处理
df_clean = df_clean.dropna(subset=["日期"])
print(f"去除无效日期后: {len(df_clean)} 行")

# 步骤6：字符串标准化（统一大小写、去空格）
df_clean["客户"] = df_clean["客户"].str.strip()
df_clean["城市"] = df_clean["城市"].str.strip().str.title()  # "beijing" -> "Beijing"
df_clean["商品"] = df_clean["商品"].str.strip().str.title()  # "python书" -> "Python书"

# 步骤7：计算衍生列
df_clean["金额"] = df_clean["数量"] * df_clean["单价"]
df_clean["月份"] = df_clean["日期"].dt.strftime("%Y-%m")

# 重置索引
df_clean = df_clean.reset_index(drop=True)

print("\n清洗后数据:")
print(df_clean.to_string())
```

#### 案例2：分组聚合与数据透视
```python
# 分组聚合
import pandas as pd
import numpy as np

print("\n===分组聚合===")

# 假设 df_clean 已经清洗好（这里用模拟数据）
data = {
    "月份": ["2024-01"] * 5 + ["2024-02"] * 5,
    "城市": ["北京", "上海", "北京", "广州", "上海", "北京", "上海", "广州", "深圳", "北京"],
    "商品": ["Python书", "键盘", "鼠标", "显示器", "鼠标", "键盘", "Python书", "显示器", "笔记本", "鼠标"],
    "金额": [179.8, 399.0, 297.0, 1299.0, 198.0, 399.0, 89.9, 1299.0, 77.5, 198.0],
}
df = pd.DataFrame(data)

# 按月份统计
monthly = df.groupby("月份").agg(
    订单数=("金额", "count"),
    总金额=("金额", "sum"),
    平均金额=("金额", "mean"),
    最大单笔=("金额", "max"),
).round(2)
print("月度统计:")
print(monthly.to_string())

# 按城市统计
city_stats = df.groupby("城市")["金额"].agg(["sum", "mean", "count"]).round(2)
city_stats.columns = ["总金额", "平均金额", "订单数"]
city_stats = city_stats.sort_values("总金额", ascending=False)
print("\n城市统计:")
print(city_stats.to_string())

# 数据透视表
pivot = df.pivot_table(
    values="金额", index="城市", columns="月份",
    aggfunc=["sum", "count"], fill_value=0
)
print("\n数据透视表（城市 x 月份）:")
print(pivot.to_string())

# 多级分组
multi = df.groupby(["月份", "城市"]).agg(
    总金额=("金额", "sum"),
    订单数=("金额", "count"),
).round(2).reset_index()
print("\n多级分组:")
print(multi.to_string())

# 排名
df["城市排名"] = df.groupby("月份")["金额"].rank(ascending=False, method="dense").astype(int)
print("\n加排名列:")
print(df.to_string())
```

### 代码说明

**案例1代码解释**：
1. `drop_duplicates(subset=["订单号"])` 按订单号去重，`keep="first"` 保留第一条
2. `pd.to_numeric(errors="coerce")` 将非数字转为 NaN（如 "3" → 3.0，"abc" → NaN）
3. `pd.to_datetime(errors="coerce")` 解析日期，格式不统一的也能处理
4. `.str.title()` 将字符串转为首字母大写形式（"beijing" → "Beijing"）
5. 每步清洗操作建议单独打印检查，不要一次性做太多操作导致难以排查

**案例2代码解释**：
1. `groupby("列名").agg(新列名=("源列", "函数"))` 是新版语法，比旧版更清晰
2. `pivot_table()` 生成二维交叉表，类似 Excel 的数据透视表
3. `rank(method="dense")` 密集排名（1,1,2,3,3,4），不跳过排名
4. `reset_index()` 将 groupby 的结果索引转回普通列

---

## 2. 数据可视化进阶

### 知识点解析

**概念定义**：数据可视化是将数据转化为图形的过程，帮助人直观发现数据中的规律、趋势和异常。Python 主要用 `matplotlib`（基础绘图）和 `seaborn`（统计图表）。

**核心规则**：
1. matplotlib 图表结构：Figure（画布）→ Axes（坐标系）→ 各种 plot
2. `fig, axes = plt.subplots(nrows, ncols)` 创建多子图
3. seaborn 基于 matplotlib，提供更美观的统计图表
4. 中文显示：`plt.rcParams["font.sans-serif"] = ["SimHei"]` 或 `plt.rcParams["font.family"]`
5. 安装：`pip install matplotlib seaborn`

**常见易错点**：
1. matplotlib 中文显示为方块——需要设置中文字体
2. 子图布局重叠——用 `plt.tight_layout()` 或调整 `figsize`
3. seaborn 的 `hue` 参数分组后图例位置不佳——用 `plt.legend(bbox_to_anchor=...)`
4. 保存图片分辨率不够——用 `dpi=150` 或更高

### 实战案例

#### 案例3：matplotlib 进阶图表
```python
# 安装: pip install matplotlib
import matplotlib.pyplot as plt
import matplotlib
import numpy as np

print("===matplotlib 进阶可视化===")

# 中文字体设置（Windows）
matplotlib.rcParams["font.sans-serif"] = ["SimHei", "Microsoft YaHei"]
matplotlib.rcParams["axes.unicode_minus"] = False  # 解决负号显示问题

# 创建多子图
fig, axes = plt.subplots(2, 2, figsize=(12, 8))
fig.suptitle("销售数据分析仪表板", fontsize=16, fontweight="bold")

# 数据
months = ["1月", "2月", "3月", "4月", "5月", "6月"]
sales_a = [120, 150, 180, 200, 170, 220]
sales_b = [80, 95, 110, 130, 120, 150]
categories = ["电子", "图书", "文具", "服装", "食品"]
values = [3500, 2800, 1500, 4200, 2100]
colors = ["#FF6B6B", "#4ECDC4", "#45B7D1", "#FFA07A", "#98D8C8"]

# 子图1：折线图（趋势）
ax1 = axes[0, 0]
ax1.plot(months, sales_a, "o-", color="#FF6B6B", linewidth=2, label="产品A", markersize=8)
ax1.plot(months, sales_b, "s--", color="#4ECDC4", linewidth=2, label="产品B", markersize=8)
ax1.fill_between(months, sales_a, alpha=0.1, color="#FF6B6B")
ax1.fill_between(months, sales_b, alpha=0.1, color="#4ECDC4")
ax1.set_title("月度销售趋势")
ax1.set_ylabel("销售额（万元）")
ax1.legend()
ax1.grid(True, alpha=0.3)

# 子图2：柱状图（对比）
ax2 = axes[0, 1]
x = np.arange(len(categories))
bars = ax2.bar(x, values, color=colors, width=0.6, edgecolor="white", linewidth=1.5)
ax2.set_xticks(x)
ax2.set_xticklabels(categories)
ax2.set_title("各品类销售额")
ax2.set_ylabel("销售额（万元）")
# 在柱子上显示数值
for bar, val in zip(bars, values):
    ax2.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 50,
             f"¥{val}", ha="center", fontsize=10)

# 子图3：饼图（占比）
ax3 = axes[1, 0]
wedges, texts, autotexts = ax3.pie(
    values, labels=categories, colors=colors, autopct="%1.1f%%",
    startangle=90, pctdistance=0.75, wedgeprops={"linewidth": 2, "edgecolor": "white"}
)
ax3.set_title("品类销售占比")

# 子图4：散点图（相关性）
ax4 = axes[1, 1]
np.random.seed(42)
x_data = np.random.normal(50, 15, 100)
y_data = x_data * 0.8 + np.random.normal(10, 8, 100)
scatter = ax4.scatter(x_data, y_data, c=x_data, cmap="coolwarm", alpha=0.7, edgecolors="white")
ax4.set_title("广告投入与销售额关系")
ax4.set_xlabel("广告投入（万元）")
ax4.set_ylabel("销售额（万元）")
fig.colorbar(scatter, ax=ax4, label="投入金额")
ax4.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig("sales_dashboard.png", dpi=150, bbox_inches="tight")
print("图表已保存: sales_dashboard.png")
plt.close()
```

#### 案例4：seaborn 统计图表
```python
# 安装: pip install seaborn
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib
import pandas as pd
import numpy as np

print("\n===seaborn 统计图表===")

matplotlib.rcParams["font.sans-serif"] = ["SimHei", "Microsoft YaHei"]
matplotlib.rcParams["axes.unicode_minus"] = False

# 生成模拟数据
np.random.seed(42)
n = 200
df = pd.DataFrame({
    "城市": np.random.choice(["北京", "上海", "广州", "深圳", "杭州"], n),
    "月份": np.random.choice(["1月", "2月", "3月", "4月"], n),
    "品类": np.random.choice(["电子", "图书", "服装"], n),
    "销售额": np.random.lognormal(6, 0.8, n),
    "利润率": np.random.normal(0.15, 0.05, n),
    "满意度": np.random.normal(4.2, 0.6, n).clip(1, 5),
})

# seaborn 图表集合
fig, axes = plt.subplots(2, 2, figsize=(12, 8))
fig.suptitle("seaborn 统计图表", fontsize=16, fontweight="bold")

# 1. 箱线图（分布+异常值）
ax1 = axes[0, 0]
sns.boxplot(data=df, x="城市", y="销售额", ax=ax1, palette="Set2")
ax1.set_title("各城市销售额分布（箱线图）")

# 2. 热力图（相关性矩阵）
ax2 = axes[0, 1]
numeric_df = df[["销售额", "利润率", "满意度"]]
corr = numeric_df.corr()
sns.heatmap(corr, annot=True, cmap="RdYlBu_r", ax=ax2, fmt=".2f", vmin=-1, vmax=1)
ax2.set_title("数值变量相关性（热力图）")

# 3. 分组柱状图
ax3 = axes[1, 0]
sns.barplot(data=df, x="品类", y="销售额", hue="城市", ax=ax3, palette="Set1")
ax3.set_title("各品类城市销售额对比")
ax3.legend(bbox_to_anchor=(1.05, 1), loc="upper left", fontsize=8)

# 4. 直方图+KDE密度曲线
ax4 = axes[1, 1]
sns.histplot(data=df, x="销售额", kde=True, bins=25, color="#4ECDC4", ax=ax4)
ax4.set_title("销售额分布（直方图+密度曲线）")

plt.tight_layout()
plt.savefig("seaborn_stats.png", dpi=150, bbox_inches="tight")
print("图表已保存: seaborn_stats.png")
plt.close()
```

### 代码说明

**案例3代码解释**：
1. `fig, axes = plt.subplots(2, 2)` 创建 2x2 的子图网格，`axes[0,0]` 是左上角
2. `ax.fill_between()` 在折线下方填充颜色，增强视觉效果
3. `plt.tight_layout()` 自动调整子图间距避免标签重叠
4. `plt.savefig(dpi=150)` 保存为高分辨率图片

**案例4代码解释**：
1. `sns.boxplot()` 箱线图展示数据分布的中位数、四分位、异常值
2. `sns.heatmap()` 热力图用颜色编码矩阵值，适合相关性分析
3. `sns.barplot(hue="城市")` 按 hue 分组，自动计算均值和置信区间
4. `sns.histplot(kde=True)` 直方图叠加核密度估计曲线

---

## 3. 完整数据分析流程

### 流程模板

```
1. 加载数据 → pd.read_csv() / pd.read_excel() / pd.read_sql()
2. 初步探索 → df.head() / df.info() / df.describe()
3. 数据清洗 → 缺失值、重复值、类型转换、异常值
4. 特征工程 → 衍生列、分类编码、标准化
5. 分析洞察 → 分组聚合、透视表、相关性分析
6. 可视化 → matplotlib / seaborn
7. 导出报告 → df.to_csv() / df.to_excel()
```

---

## 4. 知识点小结

| 操作 | pandas 方法 | 说明 |
|------|-----------|------|
| 检测缺失值 | `df.isna().sum()` | 统计每列缺失数量 |
| 填充缺失值 | `df.fillna(value)` | 填充指定值 |
| 删除缺失行 | `df.dropna(subset=[...])` | 按指定列删除 |
| 去重 | `df.drop_duplicates()` | 删除完全相同的行 |
| 类型转换 | `pd.to_numeric(errors="coerce")` | 容错转换 |
| 分组聚合 | `df.groupby().agg()` | 灵活聚合 |
| 数据透视 | `df.pivot_table()` | 二维交叉表 |
| 排名 | `df.groupby().rank()` | 分组内排名 |

**安装命令**：
```bash
pip install pandas matplotlib seaborn openpyxl
```

**学习建议**：
1. 先掌握 pandas 基础操作（选列、过滤、排序），再学高级用法
2. 数据清洗是核心技能——花时间练习处理各种脏数据
3. 可视化不需要做得很漂亮，重点是"用图表讲故事"
4. `openpyxl` 是读写 Excel 的推荐库（`pip install openpyxl`）
