# Python 计算机视觉

## 1. OpenCV 图像处理基础

### 知识点解析

**概念定义**：OpenCV（Open Source Computer Vision Library）是最流行的计算机视觉库，提供图像读取、处理、分析等功能。支持 Python、C++ 等语言，拥有超过 2500 个优化算法。

**核心概念**：
- **像素与坐标系**：图像是二维矩阵，`(x, y)` 是列-行坐标，原点在左上角
- **颜色空间**：BGR（OpenCV默认）、RGB、HSV、灰度
- **图像属性**：shape（高, 宽, 通道）、dtype（数据类型）、size（总像素数）
- **ROI（Region of Interest）**：感兴趣区域，通过切片选取图像的局部

**核心规则**：
1. 读取：`cv2.imread(path, flags)`，flags: `0`=灰度, `1`=彩色, `-1`=含alpha
2. 显示：`cv2.imshow('title', img)` + `cv2.waitKey(0)` + `cv2.destroyAllWindows()`
3. 颜色转换：`cv2.cvtColor(img, cv2.COLOR_BGR2RGB)`，BGR → RGB
4. 图像 = NumPy 数组：可以直接用 NumPy 进行像素级操作
5. 保存：`cv2.imwrite(path, img)`，注意文件格式和压缩参数

**常见易错点**：
1. OpenCV 默认使用 BGR 而非 RGB——用 `matplotlib` 显示前要先转 RGB
2. `cv2.resize(src, (width, height))` 注意是 (宽, 高)，不是 (高, 宽)
3. 坐标系：`img[y, x]` 是 (行, 列) 即 (高, 宽)
4. 图像数据类型必须是 `uint8`（0-255）或 `float32`（0.0-1.0），注意归一化
5. `waitKey()` 必须调用，否则窗口无法正常显示和关闭

### 实战案例

#### 案例1：图像读取与基本操作
```python
import cv2
import numpy as np

# ========== 读取与保存 ==========
img = cv2.imread('photo.jpg')                    # BGR格式
img_gray = cv2.imread('photo.jpg', 0)            # 灰度图
cv2.imwrite('photo_gray.jpg', img_gray)

# ========== 图像属性 ==========
print(f"形状: {img.shape}")       # (height, width, channels) 如 (1080, 1920, 3)
print(f"尺寸: {img.size}")        # 总像素数
print(f"类型: {img.dtype}")       # uint8

# ========== 颜色转换 ==========
img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)           # BGR → RGB
img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)           # BGR → HSV
img_lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)           # BGR → LAB

# ========== 缩放 ==========
img_resized = cv2.resize(img, (640, 480))                # 指定尺寸
img_scaled = cv2.resize(img, None, fx=0.5, fy=0.5)       # 缩放50%
img_large = cv2.resize(img, None, fx=2.0, fy=2.0,
                        interpolation=cv2.INTER_CUBIC)    # 放大用三次插值

# ========== 裁剪（ROI）==========
face_roi = img[100:300, 200:400]      # [y1:y2, x1:x2]
img[100:300, 200:400] = face_roi      # 将ROI粘贴回其他位置

# ========== 翻转与旋转 ==========
img_flip_h = cv2.flip(img, 1)         # 水平翻转
img_flip_v = cv2.flip(img, 0)         # 垂直翻转
img_rotated = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)  # 顺时针90度

# 任意角度旋转（需计算旋转矩阵）
h, w = img.shape[:2]
center = (w // 2, h // 2)
M = cv2.getRotationMatrix2D(center, 45, 1.0)  # 中心, 角度, 缩放
img_rotated = cv2.warpAffine(img, M, (w, h))
```

---

## 2. 图像滤波与增强

### 知识点解析

**核心概念**：
- **卷积滤波**：用卷积核对图像进行局部运算，实现模糊、锐化、边缘检测
- **高斯模糊**：用高斯分布的卷积核模糊图像，去除噪声
- **中值滤波**：用中值代替均值，对椒盐噪声效果好
- **边缘检测**：Sobel、Canny、Laplacian 算子
- **直方图**：像素值分布的统计图，用于亮度/对比度调整

### 实战案例

#### 案例1：常用滤波操作
```python
# ========== 高斯模糊 ==========
img_blur = cv2.GaussianBlur(img, (5, 5), 0)         # 5x5高斯核
img_blur_large = cv2.GaussianBlur(img, (15, 15), 0)  # 更强模糊

# ========== 中值滤波（去椒盐噪声）==========
img_median = cv2.medianBlur(img, 5)                   # 5x5中值

# ========== 双边滤波（保边去噪）==========
img_bilateral = cv2.bilateralFilter(img, 9, 75, 75)  # 保边滤波

# ========== 边缘检测 ==========
# Canny 边缘检测（最常用）
edges = cv2.Canny(img, 100, 200)  # 低阈值, 高阈值

# Sobel 边缘
sobel_x = cv2.Sobel(img_gray, cv2.CV_64F, 1, 0, ksize=3)  # 水平边缘
sobel_y = cv2.Sobel(img_gray, cv2.CV_64F, 0, 1, ksize=3)  # 垂直边缘
sobel = np.abs(sobel_x) + np.abs(sobel_y)

# Laplacian 边缘
laplacian = cv2.Laplacian(img_gray, cv2.CV_64F)

# ========== 形态学操作 ==========
kernel = np.ones((5, 5), np.uint8)

# 腐蚀（白色区域变小）
img_erosion = cv2.erode(img, kernel, iterations=1)

# 膨胀（白色区域变大）
img_dilation = cv2.dilate(img, kernel, iterations=1)

# 开运算（先腐蚀后膨胀，去小白点噪声）
img_opening = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)

# 闭运算（先膨胀后腐蚀，填小白洞）
img_closing = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)

# ========== 直方图操作 ==========
# 计算直方图
hist = cv2.calcHist([img_gray], [0], None, [256], [0, 256])

# 直方图均衡化（增强对比度）
img_equalized = cv2.equalizeHist(img_gray)

# CLAHE（自适应直方图均衡化，效果更好）
clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
img_clahe = clahe.apply(img_gray)

# ========== 亮度与对比度调整 ==========
# alpha: 对比度(1.0-3.0), beta: 亮度(0-100)
alpha = 1.5
beta = 30
img_adjusted = cv2.convertScaleAbs(img, alpha=alpha, beta=beta)
```

---

## 3. 图像分割与特征检测

### 知识点解析

**核心概念**：
- **阈值分割**：将图像分为前景和背景
- **轮廓检测**：找到图像中物体的边界
- **特征点检测**：SIFT、ORB、Harris 角点检测
- **模板匹配**：在图像中查找特定图案
- **颜色分割**：基于 HSV 颜色空间提取特定颜色区域

### 实战案例

#### 案例1：阈值分割与轮廓检测
```python
# ========== 阈值分割 ==========
# 全局阈值
_, thresh_binary = cv2.threshold(img_gray, 127, 255, cv2.THRESH_BINARY)
_, thresh_otsu = cv2.threshold(img_gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

# 自适应阈值（光照不均时更好）
thresh_adaptive = cv2.adaptiveThreshold(
    img_gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
    cv2.THRESH_BINARY, 11, 2
)

# ========== 轮廓检测 ==========
contours, hierarchy = cv2.findContours(
    thresh_binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
)

# 绘制轮廓
img_contours = img.copy()
cv2.drawContours(img_contours, contours, -1, (0, 255, 0), 2)

# 轮廓属性
for i, contour in enumerate(contours):
    area = cv2.contourArea(contour)           # 面积
    perimeter = cv2.arcLength(contour, True)   # 周长

    # 最小外接矩形
    x, y, w, h = cv2.boundingRect(contour)
    cv2.rectangle(img_contours, (x, y), (x+w, y+h), (255, 0, 0), 2)

    # 最小外接圆
    (cx, cy), radius = cv2.minEnclosingCircle(contour)

    # 轮廓近似（简化多边形）
    epsilon = 0.02 * perimeter
    approx = cv2.approxPolyDP(contour, epsilon, True)

    # 凸包
    hull = cv2.convexHull(contour)
```

#### 案例2：颜色分割（HSV空间）
```python
# ========== 基于颜色提取物体 ==========
img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

# 定义颜色范围（以红色为例）
# 红色在HSV中分布在 [0,10] 和 [170,180] 两个区间
lower_red1 = np.array([0, 100, 100])
upper_red1 = np.array([10, 255, 255])
lower_red2 = np.array([170, 100, 100])
upper_red2 = np.array([180, 255, 255])

# 创建掩码
mask1 = cv2.inRange(img_hsv, lower_red1, upper_red1)
mask2 = cv2.inRange(img_hsv, lower_red2, upper_red2)
mask = mask1 | mask2

# 提取红色区域
result = cv2.bitwise_and(img, img, mask=mask)
```

---

## 4. PIL/Pillow 图像处理

### 知识点解析

**概念定义**：Pillow（PIL）是 Python 最常用的图像处理库，API 比 OpenCV 更简洁，适合基本图像操作。

**核心概念**：
- **Image 对象**：Pillow 的核心类，代表一张图像
- **ImageDraw**：在图像上绘制形状和文字
- **ImageFont**：加载字体文件
- **ImageFilter**：图像滤镜（模糊、锐化、边缘增强等）
- **ImageEnhance**：图像增强（亮度、对比度、色彩、锐度）

**OpenCV vs Pillow 选择**：
- OpenCV：计算机视觉算法（目标检测、特征提取）、实时处理、矩阵运算
- Pillow：基本图像操作（裁剪、缩放、旋转、格式转换）、简单绘图、批量处理

### 实战案例

```python
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance

# ========== 基本操作 ==========
img = Image.open('photo.jpg')
print(f"大小: {img.size}")     # (width, height)
print(f"模式: {img.mode}")     # RGB, RGBA, L, CMYK

# 裁剪
cropped = img.crop((100, 50, 400, 300))  # (left, top, right, bottom)

# 缩放
resized = img.resize((640, 480))
thumbnail = img.copy()
thumbnail.thumbnail((200, 200))  # 等比缩放，不超过指定大小

# 旋转
rotated = img.rotate(45, expand=True)  # expand=True 避免裁剪

# 格式转换
img_rgb = img.convert('RGB')
img_gray = img.convert('L')

# ========== 滤镜 ==========
blurred = img.filter(ImageFilter.GaussianBlur(radius=5))
sharpened = img.filter(ImageFilter.SHARPEN)
edge_enhanced = img.filter(ImageFilter.EDGE_ENHANCE)

# ========== 增强效果 ==========
enhancer_brightness = ImageEnhance.Brightness(img)
brightened = enhancer_brightness.enhance(1.5)  # 1.5倍亮度

enhancer_contrast = ImageEnhance.Contrast(img)
contrasted = enhancer_contrast.enhance(1.5)

enhancer_color = ImageEnhance.Color(img)
colorized = enhancer_color.enhance(1.5)

# ========== 绘制文字 ==========
draw = ImageDraw.Draw(img)
draw.rectangle([50, 50, 200, 100], outline='red', width=2)
draw.ellipse([100, 100, 300, 300], fill='blue')
draw.line([(0, 0), (100, 100)], fill='green', width=3)
draw.text((50, 50), "Hello PIL", fill='white')

# ========== 批量处理 ==========
from pathlib import Path

output_dir = Path('processed')
output_dir.mkdir(exist_ok=True)

for img_path in Path('images').glob('*.jpg'):
    with Image.open(img_path) as img:
        img = img.resize((640, 480))
        img = img.convert('RGB')
        img.save(output_dir / f'resized_{img_path.name}', quality=85)
```

---

## 5. 深度学习视觉任务

### 知识点解析

**核心概念**：
- **图像分类**：识别图像中的主要物体（ResNet、EfficientNet、ViT）
- **目标检测**：定位并识别图像中的多个物体（YOLO、Faster R-CNN）
- **语义分割**：像素级分类，每个像素标注类别（U-Net、DeepLab）
- **图像生成**：生成新图像（GAN、Diffusion Model、Stable Diffusion）

**核心规则**：
1. YOLO 是实时目标检测的首选：速度快、精度高
2. 预训练模型 + 微调是标准流程
3. 数据增强对训练深度学习视觉模型至关重要
4. 输入图像尺寸通常固定（224x224、416x416、512x512）
5. 理解 mAP、IoU 等评估指标

### 实战案例

#### 案例1：使用预训练模型进行图像分类
```python
import torch
import torchvision.models as models
from torchvision import transforms
from PIL import Image

# ========== 加载预训练模型 ==========
model = models.resnet50(pretrained=True)
model.eval()

# ========== 图像预处理 ==========
preprocess = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406],    # ImageNet 均值
                         std=[0.229, 0.224, 0.225]),      # ImageNet 标准差
])

# ========== 加载并预处理图像 ==========
img = Image.open('cat.jpg')
img_tensor = preprocess(img).unsqueeze(0)  # 添加 batch 维度

# ========== 预测 ==========
with torch.no_grad():
    output = model(img_tensor)

# ========== 解析结果 ==========
probabilities = torch.nn.functional.softmax(output[0], dim=0)
top5_prob, top5_indices = probabilities.topk(5)

# 加载 ImageNet 标签
with open('imagenet_classes.txt') as f:
    classes = [line.strip() for line in f.readlines()]

for prob, idx in zip(top5_prob, top5_indices):
    print(f"  {classes[idx]:30s} {prob:.2%}")
```

#### 案例2：YOLO 目标检测
```python
# 使用 ultralytics 库（YOLOv8）
from ultralytics import YOLO

# 加载预训练模型
model = YOLO('yolov8n.pt')  # nano版，速度最快

# 检测
results = model('street.jpg')

# 结果处理
for result in results:
    boxes = result.boxes  # 检测框
    for box in boxes:
        cls_id = int(box.cls[0])
        conf = float(box.conf[0])
        xyxy = box.xyxy[0].tolist()  # [x1, y1, x2, y2]
        class_name = model.names[cls_id]
        print(f"  {class_name}: 置信度={conf:.2%}, 位置={xyxy}")

# 训练自定义模型
# model = YOLO('yolov8n.pt')
# model.train(data='custom_dataset.yaml', epochs=100, imgsz=640)
```

---

## 6. 视频处理

### 知识点解析

**核心概念**：
- **视频读取**：`cv2.VideoCapture()`，逐帧读取视频
- **视频写入**：`cv2.VideoWriter()`，指定编码器和帧率
- **帧处理**：每帧是一张图像，可以应用所有图像处理技术

### 实战案例

```python
import cv2

# ========== 读取视频 ==========
cap = cv2.VideoCapture('video.mp4')

# 获取视频信息
fps = cap.get(cv2.CAP_PROP_FPS)
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
print(f"视频: {width}x{height}, {fps}fps, {total_frames}帧")

# ========== 逐帧处理 ==========
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter('output.mp4', fourcc, fps, (width, height))

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # 处理帧
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 150)

    # 写入
    out.write(cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR))

cap.release()
out.release()

# ========== 摄像头实时处理 ==========
cap = cv2.VideoCapture(0)  # 0=默认摄像头

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # 实时处理（例如人脸检测）
    # ...

    cv2.imshow('Camera', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):  # 按q退出
        break

cap.release()
cv2.destroyAllWindows()
```

## 学习建议

1. **OpenCV 和 Pillow 都要掌握**：OpenCV 做算法，Pillow 做基本操作
2. **从图像读取开始**：理解图像就是 NumPy 数组，一切操作都是矩阵运算
3. **滤波是基础**：高斯模糊、边缘检测是几乎所有视觉任务的前置步骤
4. **颜色空间很重要**：BGR/RGB 用于显示，HSV 用于颜色分割，LAB 用于颜色差异
5. **深度学习优先用预训练模型**：ResNet 分类、YOLO 检测、U-Net 分割
6. **视频 = 帧序列**：学会逐帧处理，就能做视频分析
