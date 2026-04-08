"""
Python 数据处理进阶 - 示例代码
覆盖知识点：pandas 数据清洗、分组聚合、matplotlib/seaborn 可视化、完整分析流程

安装依赖：
    pip install pandas matplotlib seaborn openpyxl numpy
"""

import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import os

# ============================================================
# 0. 全局设置
# ============================================================
# 中文字体设置（Windows）
matplotlib.rcParams["font.sans-serif"] = ["SimHei", "Microsoft YaHei"]
matplotlib.rcParams["axes.unicode_minus"] = False  # 解决负号显示问题

# ============================================================
# 1. pandas 数据清洗深入
# ============================================================
print("=" * 60)
print("1. pandas 数据清洗深入")
print("=" * 60)

# --- 1.1 创建"脏"数据（模拟真实场景的常见问题）---
data = {
    "订单号": [
        "ORD-001", "ORD-002", "ORD-003", "ORD-004", "ORD-005",
        "ORD-005", "ORD-006", "ORD-007", "ORD-008", "ORD-009", "ORD-010",
    ],
    "客户": [
        "张三", "李四", "王五", "张三", "赵六",
        "赵六", "钱七", "tom", "李四", np.nan, "孙八",
    ],
    "商品": [
        "Python书", "键盘", "鼠标", "Python书", "显示器",
        "显示器", "笔记本", "python书", "鼠标", "耳机", "键盘",
    ],
    "数量": [2, 1, 3, 2, 1, 1, -5, 2, "3", 5, 0],
    "单价": [89.9, 399.0, 99.0, 89.9, 1299.0, 1299.0, 15.5, 89.9, 99.0, "299", 399.0],
    "日期": [
        "2024-01-15", "2024-01-16", "2024/01/17", "2024-01-15",
        "2024-01-18", "2024-01-18", "2024-01-19", "2024-01-20",
        "2024-01-17", "2024-01-21", "abc",
    ],
    "城市": [
        "北京", "上海", "北京", "北京", "广州",
        "广州", "深圳", "beijing", "上海", "杭州", "成都",
    ],
}

df = pd.DataFrame(data)
print("\n原始数据（脏数据）:")
print(df.to_string())
print(f"\n数据形状: {df.shape}")

# --- 1.2 数据质量报告 ---
print("\n--- 数据质量报告 ---")
print(f"缺失值统计:\n{df.isna().sum()}")
print(f"\n重复行数: {df.duplicated().sum()}")
print(f"\n各列数据类型:\n{df.dtypes}")

# --- 1.3 清洗流程 ---
print("\n--- 清洗步骤 ---")

# 步骤1：去重（按订单号去重，保留第一条）
df_clean = df.drop_duplicates(subset=["订单号"], keep="first")
print(f"步骤1 去重: {len(df)} -> {len(df_clean)} 行")

# 步骤2：处理缺失值（关键字段缺失则删除整行）
before = len(df_clean)
df_clean = df_clean.dropna(subset=["客户"])
print(f"步骤2 去除缺失客户: {before} -> {len(df_clean)} 行")

# 步骤3：类型转换（errors="coerce" 遇到无法转换的设为 NaN）
df_clean["数量"] = pd.to_numeric(df_clean["数量"], errors="coerce")
df_clean["单价"] = pd.to_numeric(df_clean["单价"], errors="coerce")
df_clean["日期"] = pd.to_datetime(df_clean["日期"], errors="coerce")
print(f"步骤3 类型转换后:\n{df_clean.dtypes}")

# 步骤4：处理异常值
invalid_qty = df_clean[(df_clean["数量"] <= 0) | df_clean["数量"].isna()]
print(f"\n步骤4 无效数量行: {len(invalid_qty)}（数量 <= 0 或非数字）")
df_clean = df_clean[(df_clean["数量"] > 0) & df_clean["数量"].notna()]
df_clean = df_clean[df_clean["单价"] > 0]

# 步骤5：日期缺失处理
df_clean = df_clean.dropna(subset=["日期"])
print(f"步骤5 清洗后剩余: {len(df_clean)} 行")

# 步骤6：字符串标准化
df_clean["客户"] = df_clean["客户"].str.strip()
df_clean["城市"] = df_clean["城市"].str.strip().str.title()  # "beijing" -> "Beijing"
df_clean["商品"] = df_clean["商品"].str.strip().str.title()

# 步骤7：计算衍生列
df_clean["金额"] = df_clean["数量"] * df_clean["单价"]
df_clean["月份"] = df_clean["日期"].dt.strftime("%Y-%m")

df_clean = df_clean.reset_index(drop=True)
print("\n清洗后数据:")
print(df_clean.to_string())


# ============================================================
# 2. 分组聚合与数据透视
# ============================================================
print("\n" + "=" * 60)
print("2. 分组聚合与数据透视")
print("=" * 60)

# 使用模拟的清洗后数据进行聚合分析
agg_data = {
    "月份": ["2024-01"] * 5 + ["2024-02"] * 5,
    "城市": ["北京", "上海", "北京", "广州", "上海", "北京", "上海", "广州", "深圳", "北京"],
    "商品": ["Python书", "键盘", "鼠标", "显示器", "鼠标", "键盘", "Python书", "显示器", "笔记本", "鼠标"],
    "金额": [179.8, 399.0, 297.0, 1299.0, 198.0, 399.0, 89.9, 1299.0, 77.5, 198.0],
}
df_agg = pd.DataFrame(agg_data)

# --- 2.1 按月份统计 ---
monthly = df_agg.groupby("月份").agg(
    订单数=("金额", "count"),
    总金额=("金额", "sum"),
    平均金额=("金额", "mean"),
    最大单笔=("金额", "max"),
).round(2)
print("\n月度统计:")
print(monthly.to_string())

# --- 2.2 按城市统计 ---
city_stats = df_agg.groupby("城市")["金额"].agg(["sum", "mean", "count"]).round(2)
city_stats.columns = ["总金额", "平均金额", "订单数"]
city_stats = city_stats.sort_values("总金额", ascending=False)
print("\n城市统计（按总金额降序）:")
print(city_stats.to_string())

# --- 2.3 数据透视表 ---
pivot = df_agg.pivot_table(
    values="金额", index="城市", columns="月份",
    aggfunc=["sum", "count"], fill_value=0,
)
print("\n数据透视表（城市 × 月份）:")
print(pivot.to_string())

# --- 2.4 多级分组 + 排名 ---
multi = df_agg.groupby(["月份", "城市"]).agg(
    总金额=("金额", "sum"),
    订单数=("金额", "count"),
).round(2).reset_index()
print("\n多级分组（月份 × 城市）:")
print(multi.to_string())

df_agg["城市排名"] = (
    df_agg.groupby("月份")["金额"]
    .rank(ascending=False, method="dense")
    .astype(int)
)
print("\n加排名列:")
print(df_agg.to_string())


# ============================================================
# 3. merge/join 合并数据
# ============================================================
print("\n" + "=" * 60)
print("3. merge/join 合并数据")
print("=" * 60)

# 模拟用户信息表
users = pd.DataFrame({
    "用户ID": [1, 2, 3, 4, 5],
    "姓名": ["张三", "李四", "王五", "赵六", "钱七"],
    "城市": ["北京", "上海", "北京", "广州", "深圳"],
})

# 模拟订单表
orders = pd.DataFrame({
    "订单号": ["O001", "O002", "O003", "O004"],
    "用户ID": [1, 2, 1, 6],  # 用户ID=6不存在（测试左连接）
    "金额": [100, 200, 150, 300],
})

# 内连接（只保留两表都有的）
inner = pd.merge(users, orders, on="用户ID", how="inner")
print("\n内连接 (inner join):")
print(inner.to_string())

# 左连接（保留左表全部）
left = pd.merge(users, orders, on="用户ID", how="left")
print("\n左连接 (left join):")
print(left.to_string())

# 右连接（保留右表全部）
right = pd.merge(users, orders, on="用户ID", how="right")
print("\n右连接 (right join):")
print(right.to_string())


# ============================================================
# 4. matplotlib 进阶可视化
# ============================================================
print("\n" + "=" * 60)
print("4. matplotlib 进阶可视化")
print("=" * 60)

# 创建多子图仪表板
fig, axes = plt.subplots(2, 2, figsize=(12, 8))
fig.suptitle("销售数据分析仪表板", fontsize=16, fontweight="bold")

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
for bar, val in zip(bars, values):
    ax2.text(
        bar.get_x() + bar.get_width() / 2, bar.get_height() + 50,
        f"¥{val}", ha="center", fontsize=10,
    )

# 子图3：饼图（占比）
ax3 = axes[1, 0]
wedges, texts, autotexts = ax3.pie(
    values, labels=categories, colors=colors, autopct="%1.1f%%",
    startangle=90, pctdistance=0.75,
    wedgeprops={"linewidth": 2, "edgecolor": "white"},
)
ax3.set_title("品类销售占比")

# 子图4：散点图（相关性）
ax4 = axes[1, 1]
np.random.seed(42)
x_data = np.random.normal(50, 15, 100)
y_data = x_data * 0.8 + np.random.normal(10, 8, 100)
scatter = ax4.scatter(
    x_data, y_data, c=x_data, cmap="coolwarm", alpha=0.7, edgecolors="white",
)
ax4.set_title("广告投入与销售额关系")
ax4.set_xlabel("广告投入（万元）")
ax4.set_ylabel("销售额（万元）")
fig.colorbar(scatter, ax=ax4, label="投入金额")
ax4.grid(True, alpha=0.3)

plt.tight_layout()
output_path = os.path.join(os.path.dirname(__file__), "sales_dashboard.png")
plt.savefig(output_path, dpi=150, bbox_inches="tight")
print(f"\n图表已保存: {output_path}")
plt.close()


# ============================================================
# 5. seaborn 统计图表（需要安装 seaborn）
# ============================================================
print("\n" + "=" * 60)
print("5. seaborn 统计图表")
print("=" * 60)

try:
    import seaborn as sns

    np.random.seed(42)
    n = 200
    df_sns = pd.DataFrame({
        "城市": np.random.choice(["北京", "上海", "广州", "深圳", "杭州"], n),
        "月份": np.random.choice(["1月", "2月", "3月", "4月"], n),
        "品类": np.random.choice(["电子", "图书", "服装"], n),
        "销售额": np.random.lognormal(6, 0.8, n),
        "利润率": np.random.normal(0.15, 0.05, n),
        "满意度": np.random.normal(4.2, 0.6, n).clip(1, 5),
    })

    fig, axes = plt.subplots(2, 2, figsize=(12, 8))
    fig.suptitle("seaborn 统计图表", fontsize=16, fontweight="bold")

    # 箱线图（分布 + 异常值）
    ax1 = axes[0, 0]
    sns.boxplot(data=df_sns, x="城市", y="销售额", ax=ax1, palette="Set2")
    ax1.set_title("各城市销售额分布（箱线图）")

    # 热力图（相关性矩阵）
    ax2 = axes[0, 1]
    numeric_df = df_sns[["销售额", "利润率", "满意度"]]
    corr = numeric_df.corr()
    sns.heatmap(corr, annot=True, cmap="RdYlBu_r", ax=ax2, fmt=".2f", vmin=-1, vmax=1)
    ax2.set_title("数值变量相关性（热力图）")

    # 分组柱状图
    ax3 = axes[1, 0]
    sns.barplot(data=df_sns, x="品类", y="销售额", hue="城市", ax=ax3, palette="Set1")
    ax3.set_title("各品类城市销售额对比")
    ax3.legend(bbox_to_anchor=(1.05, 1), loc="upper left", fontsize=8)

    # 直方图 + KDE 密度曲线
    ax4 = axes[1, 1]
    sns.histplot(data=df_sns, x="销售额", kde=True, bins=25, color="#4ECDC4", ax=ax4)
    ax4.set_title("销售额分布（直方图 + 密度曲线）")

    plt.tight_layout()
    sns_path = os.path.join(os.path.dirname(__file__), "seaborn_stats.png")
    plt.savefig(sns_path, dpi=150, bbox_inches="tight")
    print(f"图表已保存: {sns_path}")
    plt.close()

except ImportError:
    print("\n⚠️ seaborn 未安装，跳过统计图表示例")
    print("安装命令: pip install seaborn")


# ============================================================
# 6. Excel 读写（openpyxl）
# ============================================================
print("\n" + "=" * 60)
print("6. Excel 读写（openpyxl）")
print("=" * 60)

try:
    # 导出 DataFrame 到 Excel
    excel_path = os.path.join(os.path.dirname(__file__), "sales_data.xlsx")
    with pd.ExcelWriter(excel_path, engine="openpyxl") as writer:
        df_clean.to_excel(writer, sheet_name="清洗后数据", index=False)
        monthly.to_excel(writer, sheet_name="月度统计")
        city_stats.to_excel(writer, sheet_name="城市统计")
    print(f"Excel 文件已保存: {excel_path}")

    # 从 Excel 读取
    df_read = pd.read_excel(excel_path, sheet_name="清洗后数据")
    print(f"\n从 Excel 读取数据，形状: {df_read.shape}")
    print(df_read.head().to_string())

except ImportError:
    print("\n⚠️ openpyxl 未安装，跳过 Excel 读写示例")
    print("安装命令: pip install openpyxl")


# ============================================================
# 7. 完整分析流程总结
# ============================================================
print("\n" + "=" * 60)
print("7. 完整数据分析流程总结")
print("=" * 60)

print("""
标准数据分析流程：

  1. 加载数据    → pd.read_csv() / pd.read_excel() / pd.read_sql()
  2. 初步探索    → df.head() / df.info() / df.describe()
  3. 数据清洗    → 缺失值、重复值、类型转换、异常值
  4. 特征工程    → 衍生列、分类编码、标准化
  5. 分析洞察    → 分组聚合、透视表、相关性分析
  6. 可视化      → matplotlib / seaborn
  7. 导出报告    → df.to_csv() / df.to_excel()

常用安装命令：
  pip install pandas matplotlib seaborn openpyxl numpy
""")

print("✅ 所有示例运行完毕！")
