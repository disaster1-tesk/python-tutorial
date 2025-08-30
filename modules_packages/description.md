# Python模块和包知识点

## 1. 模块的概念和导入方式

### 知识点解析

**概念定义**：模块就像一个工具箱，里面装着相关的工具（函数、变量、类等）。我们可以把常用的代码放进模块里，需要时再拿出来使用，这样就不需要每次都重新写一遍。包则像是一个大工具箱，里面可以放很多小工具箱（模块）。

**核心规则**：
1. 模块是包含Python代码的.py文件
2. 使用`import`语句导入模块
3. 使用`from...import`语句导入模块中的特定内容
4. 每个模块都有独立的命名空间，避免命名冲突

**常见易错点**：
1. 忘记模块文件的.py扩展名
2. 模块名与Python关键字或内置函数名冲突
3. 循环导入问题（两个模块互相导入）
4. 导入路径错误导致模块找不到

### 实战案例

#### 案例1：学生成绩管理模块
```python
# 学生成绩管理模块
print("===学生成绩管理模块===")

# 创建学生成绩工具模块 (student_utils.py)
# 注意：在实际项目中，这应该是一个单独的.py文件

# 模拟 student_utils.py 模块内容
student_utils_module = '''
"""学生成绩工具模块"""

# 模块常量
VERSION = "1.0.0"
AUTHOR = "成绩管理系统"

# 模块级变量
student_records = {}  # 存储所有学生成绩

def add_student(name, scores):
    """
    添加学生成绩记录
    
    参数:
        name (str): 学生姓名
        scores (list): 成绩列表
    """
    if not isinstance(scores, list):
        raise ValueError("成绩必须是列表格式")
    
    student_records[name] = scores
    print(f"已添加学生 {name} 的成绩记录")

def get_average(name):
    """
    计算学生平均分
    
    参数:
        name (str): 学生姓名
        
    返回:
        float: 平均分
    """
    if name not in student_records:
        raise ValueError(f"未找到学生 {name}")
    
    scores = student_records[name]
    if not scores:
        return 0
    
    return sum(scores) / len(scores)

def get_ranking():
    """
    获取学生成绩排名
    
    返回:
        list: 按平均分排序的学生列表
    """
    ranking = []
    for name, scores in student_records.items():
        average = get_average(name)
        ranking.append((name, average))
    
    # 按平均分降序排列
    ranking.sort(key=lambda x: x[1], reverse=True)
    return ranking

def show_all_records():
    """显示所有成绩记录"""
    if not student_records:
        print("暂无成绩记录")
        return
    
    print("\\n=== 所有成绩记录 ===")
    for name, scores in student_records.items():
        average = get_average(name)
        print(f"{name}: {scores} (平均分: {average:.2f})")

# 模块初始化代码
print(f"学生成绩工具模块 v{VERSION} 已加载")
'''

# 将模块内容写入文件
with open("student_utils.py", "w", encoding="utf-8") as f:
    f.write(student_utils_module)

# 使用模块 (main.py)
print("使用学生成绩管理模块:")

# 方法1: 导入整个模块
import student_utils

# 添加学生成绩
student_utils.add_student("张三", [85, 92, 78, 90])
student_utils.add_student("李四", [78, 85, 88, 82])
student_utils.add_student("王五", [92, 95, 89, 94])

# 计算平均分
zhangsan_avg = student_utils.get_average("张三")
print(f"张三的平均分: {zhangsan_avg:.2f}")

# 显示所有记录
student_utils.show_all_records()

# 方法2: 导入模块并使用别名
import student_utils as stu

# 获取排名
ranking = stu.get_ranking()
print("\\n=== 学生成绩排名 ===")
for i, (name, average) in enumerate(ranking, 1):
    print(f"第{i}名: {name} (平均分: {average:.2f})")

# 方法3: 从模块中导入特定函数
from student_utils import add_student, get_average

# 添加更多学生成绩
add_student("赵六", [88, 90, 85, 87])
add_student("钱七", [95, 92, 98, 94])

# 计算新学生的平均分
zhaoliu_avg = get_average("赵六")
print(f"\\n赵六的平均分: {zhaoliu_avg:.2f}")

# 方法4: 导入模块中的所有公共对象（不推荐）
from student_utils import *

# 显示更新后的所有记录
show_all_records()

# 查看模块信息
print(f"\\n模块版本: {student_utils.VERSION}")
print(f"模块作者: {student_utils.AUTHOR}")

# 清理创建的文件
import os
os.remove("student_utils.py")
```

#### 案例2：图形绘制工具包
```python
# 图形绘制工具包
print("\\n===图形绘制工具包===")

import os

# 创建图形绘制包结构
# 创建包目录
os.makedirs("graphics/shapes", exist_ok=True)
os.makedirs("graphics/utils", exist_ok=True)

# 创建包的初始化文件
init_content = '''
"""图形绘制包"""

__version__ = "1.0.0"
__author__ = "图形工具开发者"

print("图形绘制包已初始化")
'''
with open("graphics/__init__.py", "w", encoding="utf-8") as f:
    f.write(init_content)

# 创建图形基类模块 (graphics/shapes/base.py)
base_content = '''
"""图形基类"""

class Shape:
    """图形基类"""
    
    def __init__(self, name):
        self.name = name
    
    def area(self):
        """计算面积（抽象方法）"""
        raise NotImplementedError("子类必须实现area方法")
    
    def perimeter(self):
        """计算周长（抽象方法）"""
        raise NotImplementedError("子类必须实现perimeter方法")
    
    def info(self):
        """显示图形信息"""
        return f"{self.name}: 面积={self.area():.2f}, 周长={self.perimeter():.2f}"
'''
with open("graphics/shapes/base.py", "w", encoding="utf-8") as f:
    f.write(base_content)

# 创建矩形模块 (graphics/shapes/rectangle.py)
rectangle_content = '''
"""矩形类"""

from .base import Shape

class Rectangle(Shape):
    """矩形类"""
    
    def __init__(self, width, height):
        super().__init__("矩形")
        self.width = width
        self.height = height
    
    def area(self):
        """计算矩形面积"""
        return self.width * self.height
    
    def perimeter(self):
        """计算矩形周长"""
        return 2 * (self.width + self.height)
'''
with open("graphics/shapes/rectangle.py", "w", encoding="utf-8") as f:
    f.write(rectangle_content)

# 创建圆形模块 (graphics/shapes/circle.py)
circle_content = '''
"""圆形类"""

import math
from .base import Shape

class Circle(Shape):
    """圆形类"""
    
    def __init__(self, radius):
        super().__init__("圆形")
        self.radius = radius
    
    def area(self):
        """计算圆形面积"""
        return math.pi * self.radius ** 2
    
    def perimeter(self):
        """计算圆形周长"""
        return 2 * math.pi * self.radius
'''
with open("graphics/shapes/circle.py", "w", encoding="utf-8") as f:
    f.write(circle_content)

# 创建工具模块 (graphics/utils/drawer.py)
drawer_content = '''
"""图形绘制工具"""

def draw_shape(shape):
    """
    绘制图形（模拟）
    
    参数:
        shape: 图形对象
    """
    print(f"绘制{shape.name}")
    print(f"  面积: {shape.area():.2f}")
    print(f"  周长: {shape.perimeter():.2f}")

def compare_shapes(shape1, shape2):
    """
    比较两个图形
    
    参数:
        shape1: 第一个图形
        shape2: 第二个图形
    """
    print(f"\\n比较 {shape1.name} 和 {shape2.name}:")
    area_diff = abs(shape1.area() - shape2.area())
    perimeter_diff = abs(shape1.perimeter() - shape2.perimeter())
    print(f"  面积差: {area_diff:.2f}")
    print(f"  周长差: {perimeter_diff:.2f}")
'''
with open("graphics/utils/drawer.py", "w", encoding="utf-8") as f:
    f.write(drawer_content)

# 创建包的子包初始化文件
with open("graphics/shapes/__init__.py", "w", encoding="utf-8") as f:
    f.write('"""图形形状包"""\n')
    
with open("graphics/utils/__init__.py", "w", encoding="utf-8") as f:
    f.write('"""图形工具包"""\n')

# 使用图形绘制包
print("使用图形绘制包:")

# 方法1: 导入包中的模块
import graphics.shapes.rectangle
import graphics.shapes.circle

# 创建图形对象
rect = graphics.shapes.rectangle.Rectangle(5, 3)
circle = graphics.shapes.circle.Circle(4)

# 显示图形信息
print(rect.info())
print(circle.info())

# 方法2: 使用别名导入
from graphics.shapes.rectangle import Rectangle as Rect
from graphics.shapes.circle import Circle

# 创建更多图形
rect2 = Rect(4, 6)
circle2 = Circle(3)

# 方法3: 导入子包
from graphics.utils import drawer

# 绘制图形
drawer.draw_shape(rect)
drawer.draw_shape(circle2)

# 比较图形
drawer.compare_shapes(rect, circle)

# 方法4: 相对导入（在包内部使用）
# 在实际项目中，这会在包内部的模块中使用

# 查看包信息
import graphics
print(f"\\n包版本: {graphics.__version__}")
print(f"包作者: {graphics.__author__}")

# 清理创建的文件和目录
import shutil
shutil.rmtree("graphics", ignore_errors=True)
```

### 代码说明

**案例1代码解释**：
1. `import student_utils`：导入整个模块，使用时需要加模块名前缀
2. `import student_utils as stu`：导入模块并使用别名，简化使用
3. `from student_utils import add_student, get_average`：只导入需要的函数
4. `student_utils.add_student("张三", [85, 92, 78, 90])`：调用模块中的函数

如果模块名与Python关键字冲突，如命名为`import.py`，会导致导入失败。应该使用有意义且符合Python命名规范的名称。

**案例2代码解释**：
1. `import graphics.shapes.rectangle`：导入包中的模块
2. `from graphics.shapes.rectangle import Rectangle as Rect`：从包中导入类并使用别名
3. `from graphics.utils import drawer`：导入子包中的模块
4. 包的结构：目录 + `__init__.py`文件构成包

如果忘记创建`__init__.py`文件，Python不会将目录识别为包，导致导入失败。

## 2. 标准库模块的使用

### 知识点解析

**概念定义**：标准库模块就像Python自带的工具箱，里面有各种现成的工具可以直接使用，比如处理日期时间的工具、操作文件系统的工具、进行数学计算的工具等，不需要额外安装。

**核心规则**：
1. 标准库模块随Python一起安装，无需额外安装
2. 使用`import`语句导入标准库模块
3. 常用标准库包括：os、sys、datetime、json、math、random等
4. 标准库模块经过优化，性能和稳定性较好

**常见易错点**：
1. 模块名拼写错误
2. 忘记导入需要的模块
3. 混淆模块中函数的使用方法
4. 不了解模块的具体功能，重复造轮子

### 实战案例

#### 案例1：个人日程管理器
```python
# 个人日程管理器
print("===个人日程管理器===")

# 导入标准库模块
import datetime
import json
import os
from pathlib import Path

class ScheduleManager:
    """个人日程管理器"""
    
    def __init__(self, filename="schedule.json"):
        """
        初始化日程管理器
        
        参数:
            filename (str): 日程数据文件名
        """
        self.filename = filename
        self.schedule = {}
        self.load_schedule()
    
    def add_event(self, date_str, time_str, event, location=""):
        """
        添加日程事件
        
        参数:
            date_str (str): 日期 (格式: YYYY-MM-DD)
            time_str (str): 时间 (格式: HH:MM)
            event (str): 事件描述
            location (str): 地点
        """
        try:
            # 验证日期格式
            event_date = datetime.datetime.strptime(date_str, "%Y-%m-%d")
            # 验证时间格式
            event_time = datetime.datetime.strptime(time_str, "%H:%M").time()
            
            # 创建事件
            event_key = f"{date_str} {time_str}"
            self.schedule[event_key] = {
                "date": date_str,
                "time": time_str,
                "event": event,
                "location": location,
                "created_at": datetime.datetime.now().isoformat()
            }
            
            self.save_schedule()
            print(f"已添加日程: {event_key} - {event}")
            
        except ValueError as e:
            print(f"日期或时间格式错误: {e}")
    
    def remove_event(self, date_str, time_str):
        """
        删除日程事件
        
        参数:
            date_str (str): 日期 (格式: YYYY-MM-DD)
            time_str (str): 时间 (格式: HH:MM)
        """
        event_key = f"{date_str} {time_str}"
        if event_key in self.schedule:
            event = self.schedule.pop(event_key)
            self.save_schedule()
            print(f"已删除日程: {event_key} - {event['event']}")
        else:
            print(f"未找到日程: {event_key}")
    
    def get_today_events(self):
        """获取今天的日程"""
        today = datetime.date.today().strftime("%Y-%m-%d")
        today_events = {}
        
        for key, event in self.schedule.items():
            if event["date"] == today:
                today_events[key] = event
        
        return today_events
    
    def get_upcoming_events(self, days=7):
        """
        获取未来几天的日程
        
        参数:
            days (int): 天数，默认7天
            
        返回:
            dict: 未来日程
        """
        today = datetime.date.today()
        end_date = today + datetime.timedelta(days=days)
        
        upcoming_events = {}
        for key, event in self.schedule.items():
            event_date = datetime.datetime.strptime(event["date"], "%Y-%m-%d").date()
            if today <= event_date <= end_date:
                upcoming_events[key] = event
        
        return upcoming_events
    
    def show_schedule(self, events=None):
        """
        显示日程
        
        参数:
            events (dict): 要显示的日程，None表示显示所有
        """
        if events is None:
            events = self.schedule
        
        if not events:
            print("暂无日程安排")
            return
        
        # 按日期和时间排序
        sorted_events = sorted(events.items(), key=lambda x: x[0])
        
        print("\\n=== 日程安排 ===")
        for key, event in sorted_events:
            location_info = f" (地点: {event['location']})" if event['location'] else ""
            print(f"{key}: {event['event']}{location_info}")
    
    def load_schedule(self):
        """从文件加载日程"""
        try:
            if os.path.exists(self.filename):
                with open(self.filename, "r", encoding="utf-8") as file:
                    self.schedule = json.load(file)
                print(f"日程数据已从 {self.filename} 加载")
            else:
                print("日程数据文件不存在，将创建新文件")
        except Exception as e:
            print(f"加载日程数据失败: {e}")
            self.schedule = {}
    
    def save_schedule(self):
        """保存日程到文件"""
        try:
            with open(self.filename, "w", encoding="utf-8") as file:
                json.dump(self.schedule, file, ensure_ascii=False, indent=2)
            print(f"日程数据已保存到 {self.filename}")
        except Exception as e:
            print(f"保存日程数据失败: {e}")

# 使用日程管理器
print("创建日程管理器:")
schedule_manager = ScheduleManager("my_schedule.json")

# 添加日程
print("\\n添加日程:")
today = datetime.date.today()
tomorrow = today + datetime.timedelta(days=1)
next_week = today + datetime.timedelta(days=7)

schedule_manager.add_event(today.strftime("%Y-%m-%d"), "09:00", "团队会议", "会议室A")
schedule_manager.add_event(today.strftime("%Y-%m-%d"), "14:30", "代码审查", "办公室")
schedule_manager.add_event(tomorrow.strftime("%Y-%m-%d"), "10:00", "客户拜访", "客户公司")
schedule_manager.add_event(next_week.strftime("%Y-%m-%d"), "15:00", "项目汇报", "大会议室")

# 显示所有日程
schedule_manager.show_schedule()

# 显示今日日程
print("\\n今日日程:")
today_events = schedule_manager.get_today_events()
schedule_manager.show_schedule(today_events)

# 显示未来7天日程
print("\\n未来7天日程:")
upcoming_events = schedule_manager.get_upcoming_events(7)
schedule_manager.show_schedule(upcoming_events)

# 删除日程
print("\\n删除日程:")
schedule_manager.remove_event(today.strftime("%Y-%m-%d"), "14:30")

# 再次显示今日日程
print("\\n删除后的今日日程:")
today_events = schedule_manager.get_today_events()
schedule_manager.show_schedule(today_events)

# 清理文件
if os.path.exists("my_schedule.json"):
    os.remove("my_schedule.json")
```

#### 案例2：文件统计分析工具
```python
# 文件统计分析工具
print("\\n===文件统计分析工具===")

import os
import sys
import pathlib
import hashlib
from collections import defaultdict

class FileAnalyzer:
    """文件统计分析工具"""
    
    def __init__(self):
        self.file_stats = defaultdict(int)
        self.extension_stats = defaultdict(int)
        self.size_stats = {
            "small": 0,      # < 1KB
            "medium": 0,     # 1KB - 1MB
            "large": 0,      # 1MB - 100MB
            "huge": 0        # > 100MB
        }
    
    def analyze_directory(self, directory_path, recursive=True):
        """
        分析目录中的文件
        
        参数:
            directory_path (str): 目录路径
            recursive (bool): 是否递归分析子目录
        """
        try:
            path = pathlib.Path(directory_path)
            if not path.exists():
                print(f"目录不存在: {directory_path}")
                return
            
            if not path.is_dir():
                print(f"路径不是目录: {directory_path}")
                return
            
            print(f"开始分析目录: {directory_path}")
            
            # 选择遍历方式
            if recursive:
                file_iterator = path.rglob("*")
                print("递归分析所有子目录")
            else:
                file_iterator = path.glob("*")
                print("只分析当前目录")
            
            file_count = 0
            for item in file_iterator:
                if item.is_file():
                    self._analyze_file(item)
                    file_count += 1
            
            print(f"分析完成，共处理 {file_count} 个文件")
            
        except Exception as e:
            print(f"分析目录时发生错误: {e}")
    
    def _analyze_file(self, file_path):
        """
        分析单个文件
        
        参数:
            file_path (Path): 文件路径
        """
        try:
            # 获取文件统计信息
            stat = file_path.stat()
            size = stat.st_size
            
            # 按大小分类
            if size < 1024:  # < 1KB
                self.size_stats["small"] += 1
            elif size < 1024 * 1024:  # < 1MB
                self.size_stats["medium"] += 1
            elif size < 100 * 1024 * 1024:  # < 100MB
                self.size_stats["large"] += 1
            else:  # >= 100MB
                self.size_stats["huge"] += 1
            
            # 按文件扩展名分类
            extension = file_path.suffix.lower()
            if not extension:
                extension = "[无扩展名]"
            self.extension_stats[extension] += 1
            
            # 按文件大小分类统计
            size_category = self._get_size_category(size)
            self.file_stats[size_category] += 1
            
        except Exception as e:
            print(f"分析文件 {file_path} 时发生错误: {e}")
    
    def _get_size_category(self, size):
        """
        根据文件大小获取分类
        
        参数:
            size (int): 文件大小（字节）
            
        返回:
            str: 大小分类
        """
        if size == 0:
            return "0B"
        elif size < 1024:
            return f"{size}B"
        elif size < 1024 * 1024:
            return f"{size//1024}KB"
        elif size < 1024 * 1024 * 1024:
            return f"{size//(1024*1024)}MB"
        else:
            return f"{size//(1024*1024*1024)}GB"
    
    def show_report(self):
        """显示分析报告"""
        print("\\n=== 文件分析报告 ===")
        
        # 显示文件大小分布
        print("\\n文件大小分布:")
        for category, count in self.size_stats.items():
            if count > 0:
                print(f"  {category}: {count} 个文件")
        
        # 显示文件扩展名统计
        if self.extension_stats:
            print("\\n文件类型统计:")
            # 按数量排序
            sorted_extensions = sorted(self.extension_stats.items(), 
                                     key=lambda x: x[1], reverse=True)
            for extension, count in sorted_extensions:
                print(f"  {extension}: {count} 个文件")
        
        # 显示系统信息
        print("\\n系统信息:")
        print(f"  Python版本: {sys.version}")
        print(f"  操作系统: {os.name}")
        print(f"  当前工作目录: {os.getcwd()}")
    
    def find_duplicate_files(self, directory_path):
        """
        查找重复文件（按内容哈希）
        
        参数:
            directory_path (str): 目录路径
            
        返回:
            dict: 重复文件组
        """
        print(f"\\n查找 {directory_path} 中的重复文件...")
        
        # 存储文件哈希值
        file_hashes = defaultdict(list)
        
        try:
            path = pathlib.Path(directory_path)
            for file_path in path.rglob("*"):
                if file_path.is_file():
                    # 计算文件哈希值
                    file_hash = self._calculate_file_hash(file_path)
                    if file_hash:
                        file_hashes[file_hash].append(str(file_path))
            
            # 查找重复文件（哈希值相同的文件）
            duplicates = {}
            for file_hash, file_paths in file_hashes.items():
                if len(file_paths) > 1:
                    duplicates[file_hash] = file_paths
            
            return duplicates
            
        except Exception as e:
            print(f"查找重复文件时发生错误: {e}")
            return {}
    
    def _calculate_file_hash(self, file_path):
        """
        计算文件的MD5哈希值
        
        参数:
            file_path (Path): 文件路径
            
        返回:
            str: 文件的MD5哈希值
        """
        try:
            hash_md5 = hashlib.md5()
            with open(file_path, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_md5.update(chunk)
            return hash_md5.hexdigest()
        except Exception as e:
            print(f"计算文件 {file_path} 哈希值时发生错误: {e}")
            return None

# 创建测试文件用于分析
def create_test_files():
    """创建测试文件"""
    os.makedirs("test_files", exist_ok=True)
    
    # 创建不同大小的测试文件
    test_files = {
        "test_files/small.txt": "这是小文件的内容\\n" * 10,
        "test_files/medium.txt": "这是中等文件的内容\\n" * 1000,
        "test_files/document.pdf": "%PDF-1.4 这是PDF文件的内容",
        "test_files/image.jpg": "\\xFF\\xD8\\xFF 这是JPEG文件的内容",
        "test_files/script.py": "print('Hello, World!')\\nprint('这是Python脚本')",
        "test_files/data.json": '{"name": "测试", "value": 123}\\n' * 100,
    }
    
    for file_path, content in test_files.items():
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
    
    # 创建子目录和文件
    os.makedirs("test_files/subdir", exist_ok=True)
    with open("test_files/subdir/nested.txt", "w", encoding="utf-8") as f:
        f.write("这是嵌套目录中的文件\\n" * 50)
    
    print("测试文件已创建")

# 创建测试文件
create_test_files()

# 使用文件分析工具
print("\\n使用文件分析工具:")

# 分析测试目录
analyzer = FileAnalyzer()
analyzer.analyze_directory("test_files", recursive=True)

# 显示分析报告
analyzer.show_report()

# 查找重复文件
duplicates = analyzer.find_duplicate_files("test_files")
if duplicates:
    print("\\n发现重复文件:")
    for file_hash, file_paths in duplicates.items():
        print(f"  哈希: {file_hash}")
        for file_path in file_paths:
            print(f"    {file_path}")
else:
    print("\\n未发现重复文件")

# 清理测试文件
import shutil
shutil.rmtree("test_files", ignore_errors=True)
```

### 代码说明

**案例1代码解释**：
1. `import datetime`：导入日期时间模块处理日期和时间
2. `import json`：导入JSON模块用于数据序列化
3. `datetime.datetime.strptime(date_str, "%Y-%m-%d")`：解析日期字符串
4. `json.dump(self.schedule, file, ensure_ascii=False, indent=2)`：将数据保存为格式化的JSON

如果忘记导入`json`模块就直接使用`json.dump()`，会出现`NameError`错误。

**案例2代码解释**：
1. `import pathlib`：导入现代化的路径操作模块
2. `import hashlib`：导入哈希算法模块
3. `path.rglob("*")`：递归遍历目录中的所有文件
4. `hashlib.md5()`：创建MD5哈希对象用于计算文件哈希值

如果在处理大文件时一次性读取整个文件计算哈希值，会占用大量内存，因此使用分块读取的方式。

## 3. 自定义模块和包

### 知识点解析

**概念定义**：自定义模块和包就像我们自己制作的专用工具箱，根据自己的需求制作特定的工具。模块是单个.py文件，包是包含多个模块的目录结构，可以更好地组织复杂项目。

**核心规则**：
1. 模块文件以.py结尾
2. 包是包含`__init__.py`文件的目录
3. 使用`if __name__ == "__main__":`实现模块的双重用途
4. 通过`__all__`列表控制模块的公共接口

**常见易错点**：
1. 忘记创建`__init__.py`文件导致目录不被识别为包
2. 模块间循环导入问题
3. 模块名与标准库或第三方库冲突
4. 没有正确设置模块搜索路径

### 实战案例

#### 案例1：个人财务管理包
```python
# 个人财务管理包
print("===个人财务管理包===")

import os
import shutil

# 创建财务管理包结构
finance_structure = {
    "finance": {
        "__init__.py": '''
"""个人财务管理包"""

__version__ = "1.0.0"
__author__ = "财务管理开发者"

from .account import Account
from .transaction import Transaction
from .report import generate_monthly_report

print("个人财务管理包已加载")
''',
        "account.py": '''
"""账户管理模块"""

class Account:
    """账户类"""
    
    def __init__(self, name, initial_balance=0):
        """
        初始化账户
        
        参数:
            name (str): 账户名称
            initial_balance (float): 初始余额
        """
        self.name = name
        self.balance = initial_balance
        self.transactions = []
    
    def deposit(self, amount, description="存款"):
        """
        存款
        
        参数:
            amount (float): 存款金额
            description (str): 描述
        """
        if amount <= 0:
            raise ValueError("存款金额必须大于0")
        
        self.balance += amount
        self.transactions.append({
            "type": "存款",
            "amount": amount,
            "description": description,
            "balance": self.balance
        })
        print(f"存款成功: ¥{amount:.2f}，当前余额: ¥{self.balance:.2f}")
    
    def withdraw(self, amount, description="取款"):
        """
        取款
        
        参数:
            amount (float): 取款金额
            description (str): 描述
        """
        if amount <= 0:
            raise ValueError("取款金额必须大于0")
        
        if amount > self.balance:
            raise ValueError("余额不足")
        
        self.balance -= amount
        self.transactions.append({
            "type": "取款",
            "amount": amount,
            "description": description,
            "balance": self.balance
        })
        print(f"取款成功: ¥{amount:.2f}，当前余额: ¥{self.balance:.2f}")
    
    def get_balance(self):
        """获取账户余额"""
        return self.balance
    
    def get_transaction_history(self):
        """获取交易历史"""
        return self.transactions.copy()
''',
        "transaction.py": '''
"""交易管理模块"""

from datetime import datetime

class Transaction:
    """交易类"""
    
    def __init__(self, account, transaction_type, amount, description="", category="其他"):
        """
        初始化交易
        
        参数:
            account: 关联账户
            transaction_type (str): 交易类型 (收入/支出)
            amount (float): 交易金额
            description (str): 描述
            category (str): 分类
        """
        self.account = account
        self.type = transaction_type
        self.amount = amount
        self.description = description
        self.category = category
        self.timestamp = datetime.now()
    
    def execute(self):
        """执行交易"""
        try:
            if self.type == "收入":
                self.account.deposit(self.amount, self.description)
            elif self.type == "支出":
                self.account.withdraw(self.amount, self.description)
            else:
                raise ValueError("交易类型必须是'收入'或'支出'")
            
            return True
        except ValueError as e:
            print(f"交易执行失败: {e}")
            return False
    
    def get_info(self):
        """获取交易信息"""
        return {
            "时间": self.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            "类型": self.type,
            "金额": self.amount,
            "描述": self.description,
            "分类": self.category
        }
''',
        "report.py": '''
"""报表生成模块"""

from datetime import datetime
from collections import defaultdict

def generate_monthly_report(accounts):
    """
    生成月度报告
    
    参数:
        accounts (list): 账户列表
    """
    print("\\n=== 月度财务报告 ===")
    
    total_assets = 0
    category_expenses = defaultdict(float)
    
    for account in accounts:
        print(f"\\n账户: {account.name}")
        print(f"当前余额: ¥{account.get_balance():.2f}")
        
        total_assets += account.get_balance()
        
        # 统计支出分类
        for transaction in account.get_transaction_history():
            if transaction["type"] == "取款":
                # 简单分类（实际应用中可以从描述中提取分类）
                category = "其他支出"
                category_expenses[category] += transaction["amount"]
    
    print(f"\\n总资产: ¥{total_assets:.2f}")
    
    if category_expenses:
        print("\\n支出分类统计:")
        for category, amount in category_expenses.items():
            print(f"  {category}: ¥{amount:.2f}")

def generate_transaction_report(accounts, days=30):
    """
    生成交易报告
    
    参数:
        accounts (list): 账户列表
        days (int): 报告天数
    """
    from datetime import timedelta
    
    print(f"\\n=== 最近{days}天交易报告 ===")
    
    cutoff_date = datetime.now() - timedelta(days=days)
    all_transactions = []
    
    for account in accounts:
        for transaction in account.get_transaction_history():
            # 这里简化处理，实际应该有时间戳
            all_transactions.append({
                "账户": account.name,
                "类型": transaction["type"],
                "金额": transaction["amount"],
                "描述": transaction["description"]
            })
    
    if not all_transactions:
        print("暂无交易记录")
        return
    
    # 按类型分组显示
    income_transactions = [t for t in all_transactions if t["类型"] == "存款"]
    expense_transactions = [t for t in all_transactions if t["类型"] == "取款"]
    
    print(f"\\n收入记录 ({len(income_transactions)} 笔):")
    for transaction in income_transactions:
        print(f"  [{transaction['账户']}] {transaction['描述']}: ¥{transaction['金额']:.2f}")
    
    print(f"\\n支出记录 ({len(expense_transactions)} 笔):")
    for transaction in expense_transactions:
        print(f"  [{transaction['账户']}] {transaction['描述']}: ¥{transaction['金额']:.2f}")
''',
        "utils": {
            "__init__.py": '''
"""财务工具包"""
''',
            "validators.py": '''
"""数据验证工具"""

def validate_amount(amount):
    """
    验证金额
    
    参数:
        amount: 金额
        
    返回:
        bool: 是否有效
    """
    try:
        amount = float(amount)
        return amount > 0
    except (ValueError, TypeError):
        return False

def validate_account_name(name):
    """
    验证账户名称
    
    参数:
        name (str): 账户名称
        
    返回:
        bool: 是否有效
    """
    return isinstance(name, str) and len(name.strip()) > 0
'''
        }
    }
}

# 创建包结构的辅助函数
def create_package_structure(structure, base_path="."):
    """创建包结构"""
    for name, content in structure.items():
        path = os.path.join(base_path, name)
        if isinstance(content, dict):
            # 创建目录
            os.makedirs(path, exist_ok=True)
            # 递归创建子结构
            create_package_structure(content, path)
        else:
            # 创建文件
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)

# 创建财务管理包
create_package_structure(finance_structure)
print("财务管理包结构已创建")

# 使用财务管理包
print("\\n使用财务管理包:")

# 导入包
import finance

# 创建账户
checking_account = finance.Account("储蓄账户", 5000)
credit_account = finance.Account("信用卡账户", 2000)

# 执行交易
transaction1 = finance.Transaction(checking_account, "支出", 1200, "购买笔记本电脑", "电子产品")
transaction1.execute()

transaction2 = finance.Transaction(checking_account, "收入", 8000, "工资", "收入")
transaction2.execute()

transaction3 = finance.Transaction(credit_account, "支出", 500, "餐厅用餐", "餐饮")
transaction3.execute()

# 生成报告
accounts = [checking_account, credit_account]
finance.generate_monthly_report(accounts)
finance.generate_transaction_report(accounts)

# 查看账户余额
print(f"\\n账户余额:")
print(f"储蓄账户: ¥{checking_account.get_balance():.2f}")
print(f"信用卡账户: ¥{credit_account.get_balance():.2f}")

# 查看交易历史
print(f"\\n储蓄账户交易历史:")
for transaction in checking_account.get_transaction_history():
    print(f"  {transaction['type']}: ¥{transaction['amount']:.2f} ({transaction['description']})")

# 清理创建的包
shutil.rmtree("finance", ignore_errors=True)
```

#### 案例2：文本处理工具模块
```python
# 文本处理工具模块
print("\\n===文本处理工具模块===")

# 创建文本处理模块 (text_utils.py)
text_utils_content = '''
"""文本处理工具模块"""

import re
from collections import Counter

__version__ = "1.0.0"
__all__ = ["count_words", "find_emails", "mask_sensitive_info", "TextAnalyzer"]

def count_words(text):
    """
    统计文本中的单词数量
    
    参数:
        text (str): 要统计的文本
        
    返回:
        dict: 单词计数字典
    """
    # 使用正则表达式提取单词（只包含字母和数字）
    words = re.findall(r'\\b[a-zA-Z0-9]+\\b', text.lower())
    return dict(Counter(words))

def find_emails(text):
    """
    查找文本中的邮箱地址
    
    参数:
        text (str): 要查找的文本
        
    返回:
        list: 邮箱地址列表
    """
    # 邮箱正则表达式
    email_pattern = r'\\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}\\b'
    return re.findall(email_pattern, text)

def mask_sensitive_info(text):
    """
    遮蔽敏感信息（手机号、身份证号等）
    
    参数:
        text (str): 要处理的文本
        
    返回:
        str: 处理后的文本
    """
    # 遮蔽手机号（11位数字）
    text = re.sub(r'\\b(1[3-9]\\d)(\\d{4})(\\d{4})\\b', r'\\1****\\3', text)
    
    # 遮蔽身份证号（18位数字，最后一位可能是X）
    text = re.sub(r'\\b(\\d{4})\\d{10}(\\d{3}[0-9Xx])\\b', r'\\1**********\\2', text)
    
    return text

class TextAnalyzer:
    """文本分析器"""
    
    def __init__(self, text):
        """
        初始化文本分析器
        
        参数:
            text (str): 要分析的文本
        """
        self.text = text
        self.words = re.findall(r'\\b[a-zA-Z0-9]+\\b', text.lower())
    
    def get_word_count(self):
        """获取总词数"""
        return len(self.words)
    
    def get_unique_word_count(self):
        """获取唯一词数"""
        return len(set(self.words))
    
    def get_most_common_words(self, n=5):
        """
        获取最常见的单词
        
        参数:
            n (int): 返回单词数量
            
        返回:
            list: 最常见的单词列表
        """
        word_counts = Counter(self.words)
        return word_counts.most_common(n)
    
    def get_text_stats(self):
        """获取文本统计信息"""
        stats = {
            "字符数": len(self.text),
            "单词数": self.get_word_count(),
            "唯一词数": self.get_unique_word_count(),
            "段落数": len(self.text.split('\\n\\n')),
            "句子数": len(re.split(r'[.!?]+', self.text)) - 1
        }
        return stats

# 模块的双重用途：既可以被导入，也可以直接运行
if __name__ == "__main__":
    # 当直接运行模块时执行的代码
    sample_text = """
    联系我们：请发送邮件到 support@example.com 或 admin@test.org。
    电话：13812345678，身份证号：110101199001011234。
    这是一个文本分析示例。文本分析可以帮助我们理解文本的内容和结构。
    通过分析，我们可以获得文本的各种统计信息。
    """
    
    print("文本处理工具模块演示")
    print("=" * 30)
    
    # 统计单词
    word_counts = count_words(sample_text)
    print(f"单词统计 (前5个): {dict(list(word_counts.items())[:5])}")
    
    # 查找邮箱
    emails = find_emails(sample_text)
    print(f"找到的邮箱: {emails}")
    
    # 遮蔽敏感信息
    masked_text = mask_sensitive_info(sample_text)
    print(f"遮蔽敏感信息后:\\n{masked_text}")
    
    # 文本分析
    analyzer = TextAnalyzer(sample_text)
    print(f"\\n文本统计信息: {analyzer.get_text_stats()}")
    
    common_words = analyzer.get_most_common_words(3)
    print(f"最常见的单词: {common_words}")
'''

# 创建文本处理模块文件
with open("text_utils.py", "w", encoding="utf-8") as f:
    f.write(text_utils_content)

print("文本处理模块已创建")

# 使用文本处理模块
print("\\n使用文本处理模块:")

# 导入模块
import text_utils

# 测试文本
test_text = """
亲爱的用户，您的订单已确认。订单号：ORD202312001。
请在24小时内完成支付，金额：¥299.00。
支付链接：https://payment.example.com/pay/ORD202312001
如有疑问，请联系客服：service@shop.com 或致电 400-123-4567。
您的个人信息：手机号 13800138000，身份证号 110101199001011234。
"""

# 统计单词
word_counts = text_utils.count_words(test_text)
print(f"单词统计 (前5个): {dict(list(word_counts.items())[:5])}")

# 查找邮箱
emails = text_utils.find_emails(test_text)
print(f"找到的邮箱: {emails}")

# 遮蔽敏感信息
masked_text = text_utils.mask_sensitive_info(test_text)
print(f"\\n遮蔽敏感信息后:\\n{masked_text}")

# 使用文本分析器
analyzer = text_utils.TextAnalyzer(test_text)
print(f"\\n文本统计信息: {analyzer.get_text_stats()}")

common_words = analyzer.get_most_common_words(5)
print(f"最常见的5个单词: {common_words}")

# 直接运行模块查看演示
print("\\n=== 直接运行模块演示 ===")
import subprocess
result = subprocess.run(["python", "text_utils.py"], capture_output=True, text=True, encoding="utf-8")
print(result.stdout)

# 清理文件
os.remove("text_utils.py")
```

### 代码说明

**案例1代码解释**：
1. `from .account import Account`：相对导入，从同级包导入模块
2. `__all__ = ["Account", "Transaction", "generate_monthly_report"]`：控制`from package import *`导入的内容
3. `if __name__ == "__main__":`：实现模块的双重用途（可导入也可直接运行）
4. 包的层次结构：目录 + `__init__.py`文件组成包

如果在包的`__init__.py`中没有正确导入需要的类和函数，外部就无法直接使用它们。

**案例2代码解释**：
1. `re.findall(r'\\b[a-zA-Z0-9]+\\b', text.lower())`：使用正则表达式提取单词
2. `Counter(words)`：使用计数器统计单词频率
3. `re.sub(pattern, replacement, text)`：使用正则表达式替换文本
4. `__all__`列表定义模块的公共接口

如果正则表达式写错，可能会匹配到错误的内容或者无法匹配到需要的内容。

## 4. 模块搜索路径和最佳实践

### 知识点解析

**概念定义**：模块搜索路径就像Python寻找工具箱的路线图，告诉Python到哪些地方去找我们需要的模块。最佳实践就是使用模块和包时的经验总结，帮助我们写出更清晰、更易维护的代码。

**核心规则**：
1. Python在`sys.path`列表指定的路径中搜索模块
2. 当前目录优先级最高
3. 可以通过`sys.path.append()`添加自定义搜索路径
4. 使用虚拟环境隔离项目依赖

**常见易错点**：
1. 模块路径设置错误导致模块找不到
2. 不同项目间的模块名冲突
3. 修改`sys.path`影响其他项目
4. 没有遵循模块和包的命名规范

### 实战案例

#### 案例1：模块路径管理器
```python
# 模块路径管理器
print("===模块路径管理器===")

import sys
import os
from pathlib import Path

class ModulePathManager:
    """模块路径管理器"""
    
    def __init__(self):
        self.original_path = sys.path.copy()
        print("模块路径管理器已初始化")
        self.show_current_paths()
    
    def show_current_paths(self):
        """显示当前模块搜索路径"""
        print("\\n当前模块搜索路径:")
        for i, path in enumerate(sys.path):
            if path:  # 跳过空路径
                print(f"  {i}: {path}")
            else:
                print(f"  {i}: (当前目录)")
    
    def add_path(self, path):
        """
        添加模块搜索路径
        
        参数:
            path (str): 要添加的路径
        """
        path_obj = Path(path).resolve()
        if path_obj.exists():
            path_str = str(path_obj)
            if path_str not in sys.path:
                sys.path.insert(0, path_str)  # 插入到开头，优先级更高
                print(f"已添加路径: {path_str}")
            else:
                print(f"路径已存在: {path_str}")
        else:
            print(f"路径不存在: {path}")
    
    def remove_path(self, path):
        """
        移除模块搜索路径
        
        参数:
            path (str): 要移除的路径
        """
        path_obj = Path(path).resolve()
        path_str = str(path_obj)
        if path_str in sys.path:
            sys.path.remove(path_str)
            print(f"已移除路径: {path_str}")
        else:
            print(f"路径不存在于搜索路径中: {path_str}")
    
    def find_module(self, module_name):
        """
        查找模块位置
        
        参数:
            module_name (str): 模块名
            
        返回:
            str: 模块路径或None
        """
        try:
            import importlib.util
            spec = importlib.util.find_spec(module_name)
            if spec and spec.origin:
                return spec.origin
            return None
        except Exception as e:
            print(f"查找模块 {module_name} 时出错: {e}")
            return None
    
    def restore_original_paths(self):
        """恢复原始模块搜索路径"""
        sys.path[:] = self.original_path
        print("已恢复原始模块搜索路径")
    
    def create_project_structure(self):
        """创建示例项目结构"""
        # 创建项目目录结构
        project_dirs = [
            "my_project",
            "my_project/utils",
            "my_project/models",
            "my_project/views",
            "external_libs"
        ]
        
        for directory in project_dirs:
            Path(directory).mkdir(parents=True, exist_ok=True)
        
        # 创建示例模块
        modules = {
            "my_project/__init__.py": '"""主项目包"""\nprint("主项目包已加载")',
            "my_project/utils/__init__.py": '"""工具包"""\nprint("工具包已加载")',
            "my_project/utils/helpers.py": '''
def format_currency(amount):
    return f"¥{amount:.2f}"

def validate_email(email):
    import re
    return re.match(r"[^@]+@[^@]+\\.[^@]+", email) is not None
''',
            "my_project/models/__init__.py": '"""模型包"""\nprint("模型包已加载")',
            "my_project/models/user.py": '''
class User:
    def __init__(self, name, email):
        self.name = name
        self.email = email
    
    def __str__(self):
        return f"User(name={self.name}, email={self.email})"
''',
            "external_libs/__init__.py": '"""外部库目录"""\nprint("外部库目录已加载")',
            "external_libs/custom_tool.py": '''
def custom_function():
    return "这是自定义工具函数"
'''
        }
        
        for file_path, content in modules.items():
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)
        
        print("示例项目结构已创建")

# 使用模块路径管理器
print("创建模块路径管理器:")
path_manager = ModulePathManager()

# 创建示例项目
path_manager.create_project_structure()

# 添加自定义路径
print("\\n添加自定义路径:")
path_manager.add_path("my_project")
path_manager.add_path("external_libs")

# 查看更新后的路径
path_manager.show_current_paths()

# 测试导入
print("\\n测试导入:")
try:
    # 导入项目模块
    from my_project.utils.helpers import format_currency, validate_email
    from my_project.models.user import User
    
    # 使用导入的函数和类
    amount = 1234.56
    formatted = format_currency(amount)
    print(f"格式化金额: {formatted}")
    
    email = "test@example.com"
    is_valid = validate_email(email)
    print(f"邮箱验证: {email} -> {'有效' if is_valid else '无效'}")
    
    user = User("张三", "zhangsan@example.com")
    print(f"创建用户: {user}")
    
    # 导入外部库
    from external_libs.custom_tool import custom_function
    result = custom_function()
    print(f"自定义工具函数: {result}")
    
except ImportError as e:
    print(f"导入失败: {e}")

# 查找模块位置
print("\\n查找模块位置:")
modules_to_find = ["os", "sys", "json", "my_project.utils.helpers"]
for module_name in modules_to_find:
    location = path_manager.find_module(module_name)
    if location:
        print(f"  {module_name}: {location}")
    else:
        print(f"  {module_name}: 未找到")

# 演示环境变量设置路径
print("\\n=== 环境变量设置示例 ===")
print("可以通过设置 PYTHONPATH 环境变量来添加模块搜索路径:")
print("  Linux/Mac: export PYTHONPATH=/path/to/my/modules:$PYTHONPATH")
print("  Windows: set PYTHONPATH=C:\\\\path\\\\to\\\\my\\\\modules;%PYTHONPATH%")

# 清理创建的文件和目录
import shutil
directories_to_remove = ["my_project", "external_libs"]
for directory in directories_to_remove:
    if os.path.exists(directory):
        shutil.rmtree(directory, ignore_errors=True)

# 恢复原始路径
path_manager.restore_original_paths()
```

#### 案例2：项目模块组织最佳实践
```python
# 项目模块组织最佳实践
print("\\n===项目模块组织最佳实践===")

import os
import shutil
from pathlib import Path

def demonstrate_best_practices():
    """演示模块和包的最佳实践"""
    
    # 创建示例项目结构
    project_structure = {
        "ecommerce_project": {
            "__init__.py": '''
"""电子商务项目主包"""

__version__ = "1.0.0"
__author__ = "电商项目团队"

# 控制公共接口
__all__ = ["create_app", "get_version"]

def create_app():
    """创建应用实例"""
    from .app import Application
    return Application()

def get_version():
    """获取项目版本"""
    return __version__

print(f"电子商务项目 v{__version__} 已加载")
''',
            "app.py": '''
"""应用主类"""

class Application:
    """应用主类"""
    
    def __init__(self):
        self.name = "电子商务系统"
        print(f"{self.name}应用已创建")
    
    def run(self):
        """运行应用"""
        print(f"{self.name}正在运行...")
        # 模拟应用运行
        self._initialize_components()
        self._start_server()
    
    def _initialize_components(self):
        """初始化组件"""
        print("初始化系统组件...")
        # 这里会导入其他模块
        from . import database, auth, products
        print("组件初始化完成")
    
    def _start_server(self):
        """启动服务器"""
        print("服务器已启动")
''',
            "config": {
                "__init__.py": '''
"""配置包"""

from .settings import Config
from .database import DatabaseConfig

__all__ = ["Config", "DatabaseConfig"]
''',
                "settings.py": '''
"""应用设置"""

import os

class Config:
    """应用配置"""
    
    # 基础配置
    SECRET_KEY = os.environ.get("SECRET_KEY") or "dev-secret-key"
    DEBUG = os.environ.get("DEBUG", "False").lower() == "true"
    
    # 环境相关配置
    ENV = os.environ.get("ENV", "development")
    
    @classmethod
    def init_app(cls, app):
        """初始化应用配置"""
        print(f"应用配置已初始化 (环境: {cls.ENV})")

class DevelopmentConfig(Config):
    """开发环境配置"""
    DEBUG = True
    DATABASE_URL = "sqlite:///dev.db"

class ProductionConfig(Config):
    """生产环境配置"""
    DEBUG = False
    DATABASE_URL = os.environ.get("DATABASE_URL") or "sqlite:///prod.db"

# 配置映射
config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig
}
''',
                "database.py": '''
"""数据库配置"""

class DatabaseConfig:
    """数据库配置"""
    
    def __init__(self):
        self.host = "localhost"
        self.port = 5432
        self.database = "ecommerce"
        self.username = "user"
        self.password = "password"
    
    def get_connection_string(self):
        """获取连接字符串"""
        return f"postgresql://{self.username}:{self.password}@{self.host}:{self.port}/{self.database}"
'''
            },
            "models": {
                "__init__.py": '''
"""数据模型包"""

from .user import User
from .product import Product
from .order import Order

__all__ = ["User", "Product", "Order"]
''',
                "base.py": '''
"""模型基类"""

from datetime import datetime

class BaseModel:
    """模型基类"""
    
    def __init__(self):
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
    
    def save(self):
        """保存模型"""
        self.updated_at = datetime.now()
        print(f"{self.__class__.__name__} 已保存")
    
    def delete(self):
        """删除模型"""
        print(f"{self.__class__.__name__} 已删除")
''',
                "user.py": '''
"""用户模型"""

from .base import BaseModel

class User(BaseModel):
    """用户模型"""
    
    def __init__(self, username, email):
        super().__init__()
        self.username = username
        self.email = email
        self.is_active = True
    
    def __str__(self):
        return f"User(username={self.username}, email={self.email})"
    
    def deactivate(self):
        """停用用户"""
        self.is_active = False
        self.save()
''',
                "product.py": '''
"""产品模型"""

from .base import BaseModel

class Product(BaseModel):
    """产品模型"""
    
    def __init__(self, name, price, description=""):
        super().__init__()
        self.name = name
        self.price = price
        self.description = description
        self.in_stock = True
    
    def __str__(self):
        return f"Product(name={self.name}, price={self.price})"
    
    def update_stock(self, quantity):
        """更新库存"""
        self.in_stock = quantity > 0
        self.save()
''',
                "order.py": '''
"""订单模型"""

from .base import BaseModel

class Order(BaseModel):
    """订单模型"""
    
    def __init__(self, user_id):
        super().__init__()
        self.user_id = user_id
        self.items = []
        self.status = "pending"
    
    def add_item(self, product_id, quantity):
        """添加商品"""
        self.items.append({"product_id": product_id, "quantity": quantity})
        self.updated_at = __import__('datetime').datetime.now()
    
    def complete(self):
        """完成订单"""
        self.status = "completed"
        self.save()
'''
            },
            "utils": {
                "__init__.py": '''
"""工具包"""

from .validators import validate_email, validate_phone
from .helpers import format_currency, generate_id

__all__ = ["validate_email", "validate_phone", "format_currency", "generate_id"]
''',
                "validators.py": '''
"""数据验证工具"""

import re

def validate_email(email):
    """验证邮箱格式"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_phone(phone):
    """验证手机号格式"""
    pattern = r'^1[3-9]\\d{9}$'
    return re.match(pattern, phone) is not None

def validate_password(password):
    """验证密码强度"""
    # 至少8位，包含字母和数字
    if len(password) < 8:
        return False
    if not re.search(r'[a-zA-Z]', password):
        return False
    if not re.search(r'\\d', password):
        return False
    return True
''',
                "helpers.py": '''
"""辅助工具"""

import uuid
from datetime import datetime

def format_currency(amount):
    """格式化货币"""
    return f"¥{amount:,.2f}"

def generate_id():
    """生成唯一ID"""
    return str(uuid.uuid4()).replace('-', '')[:12]

def get_timestamp():
    """获取时间戳"""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def slugify(text):
    """生成URL友好的slug"""
    import re
    # 转换为小写，替换空格为连字符，移除非字母数字字符
    slug = re.sub(r'[^\\w\\s-]', '', text.lower())
    slug = re.sub(r'[-\\s]+', '-', slug)
    return slug.strip('-')
'''
            },
            "tests": {
                "__init__.py": '"""测试包"""\n',
                "test_models.py": '''
"""模型测试"""

import unittest
from ..models.user import User
from ..models.product import Product

class TestUser(unittest.TestCase):
    """用户模型测试"""
    
    def test_user_creation(self):
        """测试用户创建"""
        user = User("张三", "zhangsan@example.com")
        self.assertEqual(user.username, "张三")
        self.assertEqual(user.email, "zhangsan@example.com")
        self.assertTrue(user.is_active)
    
    def test_user_deactivation(self):
        """测试用户停用"""
        user = User("李四", "lisi@example.com")
        user.deactivate()
        self.assertFalse(user.is_active)

class TestProduct(unittest.TestCase):
    """产品模型测试"""
    
    def test_product_creation(self):
        """测试产品创建"""
        product = Product("笔记本电脑", 5999.0, "高性能笔记本")
        self.assertEqual(product.name, "笔记本电脑")
        self.assertEqual(product.price, 5999.0)
        self.assertTrue(product.in_stock)

if __name__ == "__main__":
    unittest.main()
'''
            },
            "main.py": '''
"""项目入口点"""

import sys
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def main():
    """主函数"""
    print("启动电子商务系统...")
    
    try:
        # 导入项目包
        import ecommerce_project as app
        
        # 创建应用实例
        application = app.create_app()
        
        # 显示版本信息
        version = app.get_version()
        print(f"应用版本: {version}")
        
        # 运行应用
        application.run()
        
    except ImportError as e:
        print(f"导入模块失败: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"应用运行出错: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
''',
            "requirements.txt": '''
# 项目依赖
flask==2.3.2
sqlalchemy==2.0.15
psycopg2-binary==2.9.6
python-dotenv==1.0.0
requests==2.31.0
pillow==9.5.0
'''
        }
    }
    
    # 创建项目结构
    def create_structure(structure, base_path="."):
        for name, content in structure.items():
            path = os.path.join(base_path, name)
            if isinstance(content, dict):
                os.makedirs(path, exist_ok=True)
                create_structure(content, path)
            else:
                with open(path, "w", encoding="utf-8") as f:
                    f.write(content)
    
    create_structure(project_structure)
    print("电子商务项目结构已创建")
    
    # 展示项目结构
    print("\\n项目结构:")
    for root, dirs, files in os.walk("ecommerce_project"):
        level = root.replace("ecommerce_project", "").count(os.sep)
        indent = " " * 2 * level
        print(f"{indent}{os.path.basename(root)}/")
        subindent = " " * 2 * (level + 1)
        for file in files:
            print(f"{subindent}{file}")
    
    # 演示模块导入和使用
    print("\\n=== 演示模块使用 ===")
    
    # 临时添加项目路径
    project_path = os.path.abspath("ecommerce_project")
    if project_path not in sys.path:
        sys.path.insert(0, project_path)
    
    try:
        # 导入和使用项目模块
        from ecommerce_project import create_app, get_version
        from ecommerce_project.models.user import User
        from ecommerce_project.models.product import Product
        from ecommerce_project.utils.helpers import format_currency, generate_id
        from ecommerce_project.utils.validators import validate_email
        
        # 显示版本
        version = get_version()
        print(f"项目版本: {version}")
        
        # 创建应用
        app = create_app()
        
        # 创建用户和产品
        user = User("张三", "zhangsan@example.com")
        print(f"创建用户: {user}")
        
        product = Product("智能手机", 2999.0, "最新款智能手机")
        print(f"创建产品: {product}")
        print(f"产品价格: {format_currency(product.price)}")
        
        # 验证邮箱
        email = "test@example.com"
        is_valid = validate_email(email)
        print(f"邮箱 {email} 验证: {'有效' if is_valid else '无效'}")
        
        # 生成ID
        new_id = generate_id()
        print(f"生成ID: {new_id}")
        
    except Exception as e:
        print(f"演示过程中出错: {e}")
    
    # 最佳实践总结
    print("\\n=== 模块和包最佳实践 ===")
    best_practices = [
        "1. 使用清晰的包结构组织代码",
        "2. 每个包都包含 __init__.py 文件",
        "3. 在 __init__.py 中控制公共接口 (__all__)",
        "4. 使用相对导入处理包内模块引用",
        "5. 避免循环导入",
        "6. 遵循命名规范 (小写+下划线)",
        "7. 为模块添加文档字符串",
        "8. 使用 if __name__ == \"__main__\" 实现双重用途",
        "9. 合理设置模块搜索路径",
        "10. 使用 requirements.txt 管理依赖"
    ]
    
    for practice in best_practices:
        print(practice)
    
    # 清理创建的项目
    if os.path.exists("ecommerce_project"):
        shutil.rmtree("ecommerce_project", ignore_errors=True)

# 运行演示
demonstrate_best_practices()
```

### 代码说明

**案例1代码解释**：
1. `sys.path.insert(0, path_str)`：将路径插入到搜索路径开头，确保优先查找
2. `importlib.util.find_spec(module_name)`：查找模块的规范信息
3. `Path(path).resolve()`：获取路径的绝对路径
4. `sys.path[:] = self.original_path`：通过切片赋值恢复原始路径列表

如果直接使用`sys.path = self.original_path`，会创建新的列表对象，而不是修改原列表。

**案例2代码解释**：
1. `__all__ = ["create_app", "get_version"]`：控制模块的公共接口
2. `if __name__ == "__main__":`：实现模块的双重用途
3. 相对导入：`from . import database, auth, products`
4. 环境变量配置：`os.environ.get("SECRET_KEY") or "dev-secret-key"`

如果在包内部使用绝对导入而不是相对导入，当包名改变时需要修改多处代码。

这些实战案例展示了模块和包在实际项目中的应用，包括如何组织大型项目的结构、如何管理模块搜索路径、以及各种最佳实践。通过这些例子，可以更好地理解如何在实际开发中有效地使用Python的模块和包系统。