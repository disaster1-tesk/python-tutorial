"""
Python 计算机视觉完整示例
演示内容：
1. 图像基础操作（NumPy模拟）
2. 图像滤波（卷积、模糊、边缘检测）
3. 颜色空间转换
4. 形态学操作
5. 轮廓检测
6. 特征提取概念
7. 深度学习视觉任务概览
"""

import numpy as np

print("=" * 60)
print("Python 计算机视觉完整示例")
print("=" * 60)

# ============================================================
# 1. 图像基础操作（NumPy模拟）
# ============================================================
print("\n【1. 图像基础操作】")

# 创建模拟图像（8x8灰度图）
image_8x8 = np.array([
    [50, 50, 50, 50, 50, 50, 50, 50],
    [50, 200, 200, 200, 200, 200, 200, 50],
    [50, 200, 100, 100, 100, 100, 200, 50],
    [50, 200, 100, 255, 255, 100, 200, 50],
    [50, 200, 100, 255, 255, 100, 200, 50],
    [50, 200, 100, 100, 100, 100, 200, 50],
    [50, 200, 200, 200, 200, 200, 200, 50],
    [50, 50, 50, 50, 50, 50, 50, 50],
], dtype=np.uint8)

print(f"  模拟图像 (8x8):")
for row in image_8x8:
    print(f"    {row}")

# 创建彩色图像（BGR格式）
color_image = np.zeros((8, 8, 3), dtype=np.uint8)
color_image[2:6, 2:6, 0] = 255    # B通道
color_image[2:6, 2:6, 1] = 0      # G通道
color_image[2:6, 2:6, 2] = 0      # R通道
print(f"\n  彩色图像 shape: {color_image.shape} (H, W, C)")
print(f"  中心像素 BGR: {color_image[4, 4]}")

# 图像缩放（最近邻插值）
def resize_nearest(img, new_h, new_w):
    """最近邻插值缩放"""
    h, w = img.shape[:2]
    if img.ndim == 3:
        result = np.zeros((new_h, new_w, img.shape[2]), dtype=img.dtype)
    else:
        result = np.zeros((new_h, new_w), dtype=img.dtype)

    for i in range(new_h):
        for j in range(new_w):
            src_i = int(i * h / new_h)
            src_j = int(j * w / new_w)
            result[i, j] = img[src_i, src_j]

    return result


resized = resize_nearest(image_8x8, 4, 4)
print(f"\n  缩放 8x8 → 4x4:")
for row in resized:
    print(f"    {row}")

# ROI裁剪
roi = image_8x8[2:6, 2:6]
print(f"\n  ROI 裁剪 [2:6, 2:6]:")
for row in roi:
    print(f"    {row}")

# 图像翻转
flip_h = np.fliplr(image_8x8)
flip_v = np.flipud(image_8x8)
print(f"\n  水平翻转: {flip_h.shape}, 垂直翻转: {flip_v.shape}")

# ============================================================
# 2. 图像滤波
# ============================================================
print("\n\n【2. 图像滤波操作】")


def convolve2d(image, kernel, padding=0):
    """2D卷积"""
    h, w = image.shape
    kh, kw = kernel.shape

    if padding > 0:
        padded = np.zeros((h + 2 * padding, w + 2 * padding), dtype=np.float64)
        padded[padding:padding + h, padding:padding + w] = image
    else:
        padded = image.astype(np.float64)

    out_h = padded.shape[0] - kh + 1
    out_w = padded.shape[1] - kw + 1
    output = np.zeros((out_h, out_w))

    for i in range(out_h):
        for j in range(out_w):
            region = padded[i:i + kh, j:j + kw]
            output[i, j] = np.sum(region * kernel)

    return output


# 创建一个更大的测试图像
np.random.seed(42)
test_image = np.random.rand(10, 10) * 255
test_image[2:8, 2:8] = 200  # 添加亮区域
test_image = test_image.astype(np.uint8)

# ========== 均值滤波 ==========
mean_kernel = np.ones((3, 3)) / 9
mean_filtered = convolve2d(test_image, mean_kernel)
print(f"  均值滤波 (3x3) 示例值: {mean_filtered[3:5, 3:5].round(0).astype(int).tolist()}")

# ========== 高斯滤波 ==========
gaussian_kernel = np.array([
    [1, 2, 1],
    [2, 4, 2],
    [1, 2, 1]
], dtype=np.float64) / 16

gaussian_filtered = convolve2d(test_image, gaussian_kernel)
print(f"  高斯滤波 (3x3) 示例值: {gaussian_filtered[3:5, 3:5].round(0).astype(int).tolist()}")

# ========== 锐化滤波 ==========
sharpen_kernel = np.array([
    [0, -1, 0],
    [-1, 5, -1],
    [0, -1, 0]
], dtype=np.float64)

sharpened = convolve2d(test_image, sharpen_kernel)
print(f"  锐化滤波 示例值: {sharpened[3:5, 3:5].round(0).astype(int).tolist()}")

# ========== 边缘检测 ==========
# Sobel 水平边缘
sobel_x = np.array([
    [-1, 0, 1],
    [-2, 0, 2],
    [-1, 0, 1]
], dtype=np.float64)

# Sobel 垂直边缘
sobel_y = np.array([
    [-1, -2, -1],
    [0, 0, 0],
    [1, 2, 1]
], dtype=np.float64)

# Laplacian
laplacian_kernel = np.array([
    [0, 1, 0],
    [1, -4, 1],
    [0, 1, 0]
], dtype=np.float64)

# 边缘图
edge_x = np.abs(convolve2d(test_image, sobel_x))
edge_y = np.abs(convolve2d(test_image, sobel_y))
edges = np.sqrt(edge_x ** 2 + edge_y ** 2)
edge_threshold = edges > edges.mean() * 1.5

print(f"\n  Sobel边缘检测:")
print(f"  边缘像素数: {edge_threshold.sum()} (总 {edge_threshold.size})")
print(f"  边缘强度最大值: {edges.max():.1f}")
print(f"  边缘强度均值: {edges.mean():.1f}")

# ============================================================
# 3. 颜色空间
# ============================================================
print("\n\n【3. 颜色空间转换】")


def rgb_to_hsv(r, g, b):
    """RGB → HSV 转换"""
    r, g, b = r / 255.0, g / 255.0, b / 255.0
    cmax = max(r, g, b)
    cmin = min(r, g, b)
    delta = cmax - cmin

    # Hue
    if delta == 0:
        h = 0
    elif cmax == r:
        h = 60 * (((g - b) / delta) % 6)
    elif cmax == g:
        h = 60 * (((b - r) / delta) + 2)
    else:
        h = 60 * (((r - g) / delta) + 4)

    # Saturation
    s = 0 if cmax == 0 else delta / cmax

    # Value
    v = cmax

    return h, s, v


# 测试各种颜色
test_colors = {
    "红色": (255, 0, 0),
    "绿色": (0, 255, 0),
    "蓝色": (0, 0, 255),
    "黄色": (255, 255, 0),
    "青色": (0, 255, 255),
    "白色": (255, 255, 255),
    "黑色": (0, 0, 0),
    "灰色": (128, 128, 128),
}

print(f"  {'颜色':6s} {'RGB':20s} {'H':6s} {'S':6s} {'V':6s}")
print(f"  {'-'*6} {'-'*20} {'-'*6} {'-'*6} {'-'*6}")
for name, (r, g, b) in test_colors.items():
    h, s, v = rgb_to_hsv(r, g, b)
    print(f"  {name:6s} ({r:3d},{g:3d},{b:3d})        {h:5.1f} {s:5.3f} {v:5.3f}")

# ============================================================
# 4. 形态学操作
# ============================================================
print("\n\n【4. 形态学操作】")


def erode(binary_image, kernel_size=3):
    """腐蚀操作"""
    h, w = binary_image.shape
    result = np.zeros_like(binary_image)
    pad = kernel_size // 2

    padded = np.zeros((h + 2 * pad, w + 2 * pad))
    padded[pad:pad + h, pad:pad + w] = binary_image

    for i in range(h):
        for j in range(w):
            region = padded[i:i + kernel_size, j:j + kernel_size]
            result[i, j] = region.min()  # 腐蚀：取最小值

    return result


def dilate(binary_image, kernel_size=3):
    """膨胀操作"""
    h, w = binary_image.shape
    result = np.zeros_like(binary_image)
    pad = kernel_size // 2

    padded = np.zeros((h + 2 * pad, w + 2 * pad))
    padded[pad:pad + h, pad:pad + w] = binary_image

    for i in range(h):
        for j in range(w):
            region = padded[i:i + kernel_size, j:j + kernel_size]
            result[i, j] = region.max()  # 膨胀：取最大值

    return result


# 创建二值图像
binary = np.zeros((10, 10), dtype=np.uint8)
binary[2:8, 2:8] = 255  # 白色方块
binary[3, 5] = 0          # 加一个小黑点（噪声）
binary[5, 3] = 0          # 加一个小黑点

print(f"  原始二值图 (有噪声):")
for row in binary:
    print(f"    {''.join(['#' if v > 0 else '.' for v in row])}")

# 闭运算（先膨胀后腐蚀，填充小洞）
closed = erode(dilate(binary, 3), 3)
print(f"\n  闭运算后 (小洞被填充):")
for row in closed:
    print(f"    {''.join(['#' if v > 0 else '.' for v in row])}")

# 开运算（先腐蚀后膨胀，去除小噪点）
noisy = binary.copy()
noisy[0, 0] = 255  # 加一个孤立白点
opened = dilate(erode(noisy, 3), 3)
print(f"\n  开运算后 (孤立噪点被去除):")
for row in opened:
    print(f"    {''.join(['#' if v > 0 else '.' for v in row])}")

# ============================================================
# 5. 直方图与阈值分割
# ============================================================
print("\n\n【5. 直方图与阈值分割】")

# 模拟灰度直方图
gray_values = np.random.randint(50, 200, size=500)
gray_values = np.concatenate([gray_values, np.random.randint(0, 30, size=100)])  # 暗像素
gray_values = np.concatenate([gray_values, np.random.randint(220, 256, size=100)])  # 亮像素

# 计算直方图
hist, bin_edges = np.histogram(gray_values, bins=256, range=(0, 256))

# Otsu 阈值（简化版）
best_threshold = 0
best_variance = 0

for t in range(1, 256):
    w0 = np.sum(gray_values <= t)
    w1 = np.sum(gray_values > t)

    if w0 == 0 or w1 == 0:
        continue

    mu0 = np.mean(gray_values[gray_values <= t])
    mu1 = np.mean(gray_values[gray_values > t])

    between_variance = w0 * w1 * (mu0 - mu1) ** 2
    if between_variance > best_variance:
        best_variance = between_variance
        best_threshold = t

print(f"  灰度范围: [{gray_values.min()}, {gray_values.max()}]")
print(f"  均值: {gray_values.mean():.1f}")
print(f"  Otsu最佳阈值: {best_threshold}")
print(f"  暗像素(<=阈值): {np.sum(gray_values <= best_threshold)}")
print(f"  亮像素(>阈值): {np.sum(gray_values > best_threshold)}")

# ============================================================
# 6. 特征提取概念
# ============================================================
print("\n\n【6. 图像特征提取概念】")


def compute_image_features(image):
    """计算基本图像特征"""
    features = {}

    # 1. 像素统计特征
    features['mean'] = np.mean(image)
    features['std'] = np.std(image)
    features['min'] = np.min(image)
    features['max'] = np.max(image)
    features['median'] = np.median(image)

    # 2. 直方图特征（256维压缩到8维）
    hist, _ = np.histogram(image, bins=8, range=(0, 256))
    hist = hist / hist.sum()  # 归一化
    features['histogram'] = hist.tolist()

    # 3. 纹理特征（灰度共生矩阵简化版）
    # 水平相邻像素差
    h_diff = np.mean(np.abs(np.diff(image, axis=1)))
    v_diff = np.mean(np.abs(np.diff(image, axis=0)))
    features['texture_h'] = h_diff
    features['texture_v'] = v_diff

    # 4. 形状特征（如果图像是二值图）
    binary = (image > np.median(image)).astype(np.uint8)
    features['white_ratio'] = np.sum(binary) / binary.size
    features['center_of_mass'] = (
        int(np.average(np.arange(image.shape[0]), weights=binary.sum(axis=1))),
        int(np.average(np.arange(image.shape[1]), weights=binary.sum(axis=0)))
    )

    return features


features = compute_image_features(image_8x8)
print(f"  图像特征提取结果:")
print(f"    均值: {features['mean']:.1f}")
print(f"    标准差: {features['std']:.1f}")
print(f"    最小/最大: {features['min']}/{features['max']}")
print(f"    中位数: {features['median']:.1f}")
print(f"    白色比例: {features['white_ratio']:.2%}")
print(f"    质心: {features['center_of_mass']}")
print(f"    纹理(水平): {features['texture_h']:.1f}")
print(f"    纹理(垂直): {features['texture_v']:.1f}")
print(f"    直方图(8bin): {[f'{v:.2f}' for v in features['histogram']]}")

# ============================================================
# 7. 深度学习视觉任务概览
# ============================================================
print("\n\n【7. 深度学习视觉任务概览】")

tasks = [
    {
        "任务": "图像分类",
        "输入": "一张图片",
        "输出": "类别标签（如：猫、狗、汽车）",
        "常用模型": "ResNet, EfficientNet, ViT, ConvNeXt",
        "典型精度": "Top-1 准确率 > 85%",
        "应用场景": "相册分类、内容审核、医疗影像"
    },
    {
        "任务": "目标检测",
        "输入": "一张图片",
        "输出": "多个 [类别, 置信度, 边界框]",
        "常用模型": "YOLOv8, Faster R-CNN, DETR",
        "典型精度": "mAP > 50%",
        "应用场景": "自动驾驶、安防监控、工业质检"
    },
    {
        "任务": "语义分割",
        "输入": "一张图片",
        "输出": "每个像素的类别标签",
        "常用模型": "U-Net, DeepLabV3, SegFormer",
        "典型精度": "mIoU > 70%",
        "应用场景": "医学图像分割、自动驾驶道路检测"
    },
    {
        "任务": "实例分割",
        "输入": "一张图片",
        "输出": "每个物体的像素级掩码+类别",
        "常用模型": "Mask R-CNN, YOLOv8-Seg, SAM",
        "典型精度": "mask AP > 40%",
        "应用场景": "精细目标分割、图像编辑"
    },
    {
        "任务": "图像生成",
        "输入": "文本描述/噪声",
        "输出": "生成的图片",
        "常用模型": "Stable Diffusion, DALL-E, GAN",
        "典型精度": "FID < 20",
        "应用场景": "AI绘画、数据增强、创意设计"
    },
]

print(f"  {'任务':8s} {'常用模型':30s} {'应用场景':25s}")
print(f"  {'-'*8} {'-'*30} {'-'*25}")
for task in tasks:
    print(f"  {task['任务']:8s} {task['常用模型']:30s} {task['应用场景']:25s}")

# 常用评估指标
print(f"\n  常用评估指标:")
metrics = [
    ("Accuracy", "分类准确率 = 预测正确数 / 总数"),
    ("Precision", "精确率 = TP / (TP + FP)"),
    ("Recall", "召回率 = TP / (TP + FN)"),
    ("F1-Score", "F1 = 2 * Precision * Recall / (Precision + Recall)"),
    ("IoU", "交并比 = 交集面积 / 并集面积"),
    ("mAP", "平均精度均值，目标检测核心指标"),
    ("mIoU", "平均IoU，语义分割核心指标"),
    ("PSNR", "峰值信噪比，图像质量评估"),
    ("SSIM", "结构相似性，图像质量评估"),
]
for name, desc in metrics:
    print(f"    {name:10s}: {desc}")

print("\n" + "=" * 60)
print("计算机视觉示例运行完毕！")
print("=" * 60)
