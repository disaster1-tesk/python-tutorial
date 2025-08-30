# Python标准库使用知识点

## 1. os和sys模块 - 系统操作基础

### 知识点解析

**概念定义**：os模块就像Python与操作系统的"翻译官"，帮助Python程序与计算机系统进行交流，比如查看文件、创建文件夹、获取系统信息等。sys模块则是Python程序的"自我认知工具"，可以获取程序的运行参数、Python版本等信息。

**核心规则**：
1. os模块用于与操作系统交互，处理文件和目录
2. sys模块用于与Python解释器交互，处理程序参数和系统信息
3. 使用os.path进行跨平台路径操作
4. 使用sys.argv获取命令行参数

**常见易错点**：
1. 忘记处理文件或目录不存在的情况
2. 硬编码路径分隔符导致跨平台兼容性问题
3. 不检查命令行参数数量导致索引越界
4. 忘记处理环境变量不存在的情况

### 实战案例

#### 案例1：系统信息查看器
```python
# 系统信息查看器
print("===系统信息查看器===")

import os
import sys
from datetime import datetime

class SystemInfoViewer:
    """系统信息查看器"""
    
    def __init__(self):
        """初始化系统信息查看器"""
        print("系统信息查看器已启动")
    
    def show_current_directory_info(self):
        """显示当前目录信息"""
        print("\n=== 当前目录信息 ===")
        
        # 获取当前工作目录
        current_dir = os.getcwd()
        print(f"当前目录: {current_dir}")
        
        # 列出当前目录内容
        try:
            items = os.listdir(current_dir)
            print(f"目录项数: {len(items)}")
            
            # 分类统计文件和目录
            files = []
            directories = []
            
            for item in items:
                item_path = os.path.join(current_dir, item)
                if os.path.isfile(item_path):
                    files.append(item)
                elif os.path.isdir(item_path):
                    directories.append(item)
            
            print(f"文件数量: {len(files)}")
            print(f"目录数量: {len(directories)}")
            
            # 显示前5个文件和目录
            if files:
                print("文件示例 (前5个):")
                for file in files[:5]:
                    print(f"  文件: {file}")
            
            if directories:
                print("目录示例 (前5个):")
                for directory in directories[:5]:
                    print(f"  目录: {directory}")
                    
        except PermissionError:
            print("没有权限访问当前目录")
        except Exception as e:
            print(f"获取目录信息时出错: {e}")
    
    def show_environment_info(self):
        """显示环境信息"""
        print("\n=== 环境信息 ===")
        
        # 显示Python版本
        print(f"Python版本: {sys.version}")
        print(f"Python可执行文件路径: {sys.executable}")
        
        # 显示平台信息
        print(f"操作系统平台: {sys.platform}")
        
        # 显示命令行参数
        print(f"命令行参数: {sys.argv}")
        
        # 显示环境变量
        print("\n重要环境变量:")
        important_vars = ["HOME", "PATH", "USER", "USERNAME", "PWD"]
        for var in important_vars:
            value = os.environ.get(var, "未设置")
            if var == "PATH":
                # PATH变量通常很长，只显示前100个字符
                value = value[:100] + "..." if len(value) > 100 else value
            print(f"  {var}: {value}")
    
    def show_system_paths(self):
        """显示系统路径"""
        print("\n=== Python模块搜索路径 ===")
        
        # 显示模块搜索路径
        print("模块搜索路径 (前10个):")
        for i, path in enumerate(sys.path[:10]):
            if path:  # 跳过空路径
                print(f"  {i+1}. {path}")
            else:
                print(f"  {i+1}. (当前目录)")
        
        # 如果路径超过10个，显示总数
        if len(sys.path) > 10:
            print(f"  ... 还有 {len(sys.path) - 10} 个路径")
    
    def create_test_structure(self):
        """创建测试目录结构"""
        print("\n=== 创建测试目录结构 ===")
        
        # 创建测试目录
        test_dirs = ["test_project", "test_project/docs", "test_project/src", "test_project/tests"]
        for directory in test_dirs:
            try:
                os.makedirs(directory, exist_ok=True)
                print(f"已创建目录: {directory}")
            except Exception as e:
                print(f"创建目录 {directory} 时出错: {e}")
        
        # 创建测试文件
        test_files = {
            "test_project/README.md": "# 测试项目\n这是一个测试项目",
            "test_project/docs/intro.txt": "项目介绍文档",
            "test_project/src/main.py": "print('Hello, World!')",
            "test_project/tests/test_main.py": "def test_example():\n    assert True"
        }
        
        for file_path, content in test_files.items():
            try:
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(content)
                print(f"已创建文件: {file_path}")
            except Exception as e:
                print(f"创建文件 {file_path} 时出错: {e}")
    
    def cleanup_test_structure(self):
        """清理测试目录结构"""
        print("\n=== 清理测试目录结构 ===")
        
        import shutil
        try:
            if os.path.exists("test_project"):
                shutil.rmtree("test_project")
                print("已清理测试目录结构")
            else:
                print("测试目录不存在")
        except Exception as e:
            print(f"清理测试目录时出错: {e}")

# 使用系统信息查看器
print("创建系统信息查看器:")
viewer = SystemInfoViewer()

# 显示当前目录信息
viewer.show_current_directory_info()

# 显示环境信息
viewer.show_environment_info()

# 显示系统路径
viewer.show_system_paths()

# 创建并清理测试结构
viewer.create_test_structure()
viewer.cleanup_test_structure()
```

#### 案例2：文件目录管理工具
```python
# 文件目录管理工具
print("\n===文件目录管理工具===")

import os
import sys
from pathlib import Path
import shutil

class FileManager:
    """文件目录管理工具"""
    
    def __init__(self):
        """初始化文件管理工具"""
        print("文件目录管理工具已启动")
    
    def create_directory(self, path):
        """
        创建目录
        
        参数:
            path (str): 目录路径
        """
        try:
            Path(path).mkdir(parents=True, exist_ok=True)
            print(f"目录已创建: {path}")
            return True
        except Exception as e:
            print(f"创建目录 {path} 失败: {e}")
            return False
    
    def remove_directory(self, path):
        """
        删除目录
        
        参数:
            path (str): 目录路径
        """
        try:
            if os.path.exists(path):
                if os.path.isdir(path):
                    shutil.rmtree(path)
                    print(f"目录已删除: {path}")
                else:
                    print(f"路径 {path} 不是目录")
            else:
                print(f"目录不存在: {path}")
            return True
        except Exception as e:
            print(f"删除目录 {path} 失败: {e}")
            return False
    
    def copy_file(self, src, dst):
        """
        复制文件
        
        参数:
            src (str): 源文件路径
            dst (str): 目标文件路径
        """
        try:
            shutil.copy2(src, dst)
            print(f"文件已复制: {src} -> {dst}")
            return True
        except Exception as e:
            print(f"复制文件 {src} -> {dst} 失败: {e}")
            return False
    
    def move_file(self, src, dst):
        """
        移动文件
        
        参数:
            src (str): 源文件路径
            dst (str): 目标文件路径
        """
        try:
            shutil.move(src, dst)
            print(f"文件已移动: {src} -> {dst}")
            return True
        except Exception as e:
            print(f"移动文件 {src} -> {dst} 失败: {e}")
            return False
    
    def list_directory_tree(self, path, level=0):
        """
        列出目录树结构
        
        参数:
            path (str): 目录路径
            level (int): 缩进级别
        """
        try:
            path_obj = Path(path)
            if not path_obj.exists():
                print(f"路径不存在: {path}")
                return
            
            indent = "  " * level
            print(f"{indent}{path_obj.name}/")
            
            if path_obj.is_dir():
                for item in path_obj.iterdir():
                    if item.is_dir():
                        self.list_directory_tree(str(item), level + 1)
                    else:
                        print(f"{'  ' * (level + 1)}{item.name}")
        except Exception as e:
            print(f"列出目录树 {path} 失败: {e}")
    
    def search_files(self, directory, pattern):
        """
        搜索文件
        
        参数:
            directory (str): 搜索目录
            pattern (str): 文件名模式
        """
        try:
            found_files = []
            directory_path = Path(directory)
            
            if not directory_path.exists():
                print(f"目录不存在: {directory}")
                return found_files
            
            # 递归搜索文件
            for file_path in directory_path.rglob(pattern):
                if file_path.is_file():
                    found_files.append(str(file_path))
            
            return found_files
        except Exception as e:
            print(f"搜索文件失败: {e}")
            return []
    
    def get_file_info(self, file_path):
        """
        获取文件信息
        
        参数:
            file_path (str): 文件路径
        """
        try:
            path_obj = Path(file_path)
            if not path_obj.exists():
                print(f"文件不存在: {file_path}")
                return None
            
            stat = path_obj.stat()
            info = {
                "路径": str(path_obj),
                "大小": f"{stat.st_size} 字节",
                "创建时间": datetime.fromtimestamp(stat.st_ctime).strftime("%Y-%m-%d %H:%M:%S"),
                "修改时间": datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M:%S"),
                "是否为文件": path_obj.is_file(),
                "是否为目录": path_obj.is_dir()
            }
            
            return info
        except Exception as e:
            print(f"获取文件信息 {file_path} 失败: {e}")
            return None

# 使用文件管理工具
print("创建文件管理工具:")
file_manager = FileManager()

# 创建测试目录结构
print("\n创建测试结构:")
file_manager.create_directory("project")
file_manager.create_directory("project/src")
file_manager.create_directory("project/docs")
file_manager.create_directory("project/tests")

# 创建测试文件
test_files = {
    "project/README.md": "# 项目说明\n这是项目说明文件",
    "project/src/main.py": "def main():\n    print('Hello, World!')\n\nif __name__ == '__main__':\n    main()",
    "project/src/utils.py": "def utility_function():\n    return '这是一个工具函数'",
    "project/docs/guide.md": "# 使用指南\n详细使用说明",
    "project/tests/test_main.py": "def test_main():\n    assert True"
}

for file_path, content in test_files.items():
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"已创建文件: {file_path}")
    except Exception as e:
        print(f"创建文件 {file_path} 失败: {e}")

# 显示目录树
print("\n项目目录树:")
file_manager.list_directory_tree("project")

# 搜索文件
print("\n搜索Python文件:")
py_files = file_manager.search_files("project", "*.py")
for file in py_files:
    print(f"  找到: {file}")

# 获取文件信息
print("\n文件信息:")
info = file_manager.get_file_info("project/src/main.py")
if info:
    for key, value in info.items():
        print(f"  {key}: {value}")

# 复制和移动文件
print("\n文件操作:")
file_manager.copy_file("project/README.md", "project/README_COPY.md")
file_manager.move_file("project/docs/guide.md", "project/GUIDE.md")

# 显示更新后的目录树
print("\n更新后的目录树:")
file_manager.list_directory_tree("project")

# 清理测试文件
import shutil
shutil.rmtree("project", ignore_errors=True)
```

### 代码说明

**案例1代码解释**：
1. `os.getcwd()`：获取当前工作目录
2. `os.listdir(current_dir)`：列出目录中的所有项目
3. `sys.version`：获取Python版本信息
4. `os.environ.get(var, "未设置")`：安全地获取环境变量

如果直接访问`os.environ[var]`而变量不存在，会抛出KeyError异常，使用get方法可以避免这个问题。

**案例2代码解释**：
1. `Path(path).mkdir(parents=True, exist_ok=True)`：创建目录，自动创建父目录
2. `shutil.rmtree(path)`：递归删除目录及其内容
3. `path_obj.iterdir()`：遍历目录中的项目
4. `path_obj.rglob(pattern)`：递归搜索匹配模式的文件

如果忘记使用`parents=True`参数，当父目录不存在时会抛出FileNotFoundError异常。

## 2. datetime和time模块 - 时间日期处理

### 知识点解析

**概念定义**：datetime模块就像一个"时间魔法师"，可以帮我们处理各种与时间相关的问题，比如获取当前时间、计算时间差、格式化时间显示等。time模块则更底层，提供了时间访问和转换的基本功能。

**核心规则**：
1. datetime模块提供日期时间的高级操作
2. time模块提供底层时间功能
3. 使用strftime()格式化时间，strptime()解析时间字符串
4. timedelta用于时间计算

**常见易错点**：
1. 混淆datetime对象和字符串表示
2. 时区处理不当导致时间错误
3. 忘记处理时间解析异常
4. 时间计算时忽略闰秒等特殊情况

### 实战案例

#### 案例1：个人时间管理器
```python
# 个人时间管理器
print("===个人时间管理器===")

from datetime import datetime, date, time, timedelta
import time as time_module  # 为了避免与datetime.time冲突

class TimeManager:
    """个人时间管理器"""
    
    def __init__(self):
        """初始化时间管理器"""
        self.events = []
        print("个人时间管理器已启动")
    
    def add_event(self, name, event_datetime, duration_hours=1):
        """
        添加事件
        
        参数:
            name (str): 事件名称
            event_datetime (datetime): 事件时间
            duration_hours (int): 持续时间（小时）
        """
        event = {
            "name": name,
            "datetime": event_datetime,
            "duration": timedelta(hours=duration_hours),
            "created_at": datetime.now()
        }
        
        self.events.append(event)
        print(f"已添加事件: {name} 在 {event_datetime.strftime('%Y-%m-%d %H:%M')}")
    
    def show_upcoming_events(self, days=7):
        """
        显示即将到来的事件
        
        参数:
            days (int): 显示未来几天的事件
        """
        print(f"\n=== 未来 {days} 天的事件 ===")
        
        now = datetime.now()
        future_limit = now + timedelta(days=days)
        
        upcoming_events = [
            event for event in self.events
            if now <= event["datetime"] <= future_limit
        ]
        
        if not upcoming_events:
            print("暂无即将到来的事件")
            return
        
        # 按时间排序
        upcoming_events.sort(key=lambda x: x["datetime"])
        
        for event in upcoming_events:
            time_str = event["datetime"].strftime("%Y-%m-%d %H:%M")
            print(f"  {time_str}: {event['name']}")
    
    def show_events_on_date(self, target_date):
        """
        显示指定日期的事件
        
        参数:
            target_date (date): 目标日期
        """
        print(f"\n=== {target_date.strftime('%Y年%m月%d日')} 的事件 ===")
        
        date_events = [
            event for event in self.events
            if event["datetime"].date() == target_date
        ]
        
        if not date_events:
            print("当天没有事件安排")
            return
        
        # 按时间排序
        date_events.sort(key=lambda x: x["datetime"])
        
        for event in date_events:
            time_str = event["datetime"].strftime("%H:%M")
            end_time = event["datetime"] + event["duration"]
            end_time_str = end_time.strftime("%H:%M")
            print(f"  {time_str}-{end_time_str}: {event['name']}")
    
    def calculate_time_until_event(self, event_name):
        """
        计算距离事件的时间
        
        参数:
            event_name (str): 事件名称
        """
        print(f"\n=== 距离 '{event_name}' 的时间 ===")
        
        for event in self.events:
            if event["name"] == event_name:
                now = datetime.now()
                if event["datetime"] > now:
                    time_diff = event["datetime"] - now
                    days = time_diff.days
                    hours, remainder = divmod(time_diff.seconds, 3600)
                    minutes, _ = divmod(remainder, 60)
                    
                    print(f"距离 {event_name} 还有 {days} 天 {hours} 小时 {minutes} 分钟")
                elif event["datetime"] < now:
                    time_diff = now - event["datetime"]
                    days = time_diff.days
                    print(f"{event_name} 已经过了 {days} 天")
                else:
                    print(f"{event_name} 正在进行中")
                return
        
        print(f"未找到事件: {event_name}")
    
    def show_current_time_info(self):
        """显示当前时间信息"""
        print("\n=== 当前时间信息 ===")
        
        now = datetime.now()
        print(f"当前时间: {now.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"星期: {now.strftime('%A')}")
        print(f"月份: {now.strftime('%B')}")
        print(f"一年中的第 {now.timetuple().tm_yday} 天")
        print(f"一周中的第 {now.weekday() + 1} 天")
        
        # 显示时间戳
        timestamp = time_module.time()
        print(f"时间戳: {timestamp}")
    
    def format_time_examples(self):
        """显示时间格式化示例"""
        print("\n=== 时间格式化示例 ===")
        
        sample_time = datetime(2023, 12, 25, 14, 30, 45)
        formats = [
            ("%Y-%m-%d %H:%M:%S", "标准格式"),
            ("%Y年%m月%d日 %H时%M分%S秒", "中文格式"),
            ("%A, %B %d, %Y", "英文格式"),
            ("%Y-%m-%d", "日期格式"),
            ("%H:%M:%S", "时间格式"),
            ("%Y-%m-%d %I:%M %p", "12小时制格式")
        ]
        
        for format_str, description in formats:
            formatted = sample_time.strftime(format_str)
            print(f"  {description}: {formatted}")
    
    def parse_time_examples(self):
        """显示时间解析示例"""
        print("\n=== 时间解析示例 ===")
        
        time_strings = [
            ("2023-12-25 14:30:45", "%Y-%m-%d %H:%M:%S"),
            ("25/12/2023", "%d/%m/%Y"),
            ("Dec 25, 2023", "%b %d, %Y"),
            ("2023-12-25", "%Y-%m-%d")
        ]
        
        for time_str, format_str in time_strings:
            try:
                parsed = datetime.strptime(time_str, format_str)
                print(f"  '{time_str}' -> {parsed}")
            except ValueError as e:
                print(f"  '{time_str}' 解析失败: {e}")

# 使用时间管理器
print("创建时间管理器:")
time_manager = TimeManager()

# 显示当前时间信息
time_manager.show_current_time_info()

# 显示格式化示例
time_manager.format_time_examples()

# 显示解析示例
time_manager.parse_time_examples()

# 添加示例事件
now = datetime.now()
time_manager.add_event("团队会议", now + timedelta(days=1, hours=2), 2)
time_manager.add_event("项目截止", now + timedelta(days=3), 1)
time_manager.add_event("生日聚会", now + timedelta(days=7, hours=18), 3)
time_manager.add_event("年度总结", date(2024, 1, 15), 2)

# 显示即将到来的事件
time_manager.show_upcoming_events(10)

# 显示指定日期的事件
tomorrow = (now + timedelta(days=1)).date()
time_manager.show_events_on_date(tomorrow)

# 计算距离事件的时间
time_manager.calculate_time_until_event("团队会议")
```

#### 案例2：工作时间计算器
```python
# 工作时间计算器
print("\n===工作时间计算器===")

from datetime import datetime, timedelta, time
import json

class WorkTimeCalculator:
    """工作时间计算器"""
    
    def __init__(self):
        """初始化工作时间计算器"""
        self.work_records = []
        print("工作时间计算器已启动")
    
    def start_work(self, task_name):
        """
        开始工作
        
        参数:
            task_name (str): 任务名称
        """
        start_time = datetime.now()
        record = {
            "task_name": task_name,
            "start_time": start_time,
            "end_time": None,
            "duration": None
        }
        
        self.work_records.append(record)
        print(f"开始工作: {task_name} (开始时间: {start_time.strftime('%H:%M:%S')})")
    
    def end_work(self):
        """结束当前工作"""
        if not self.work_records:
            print("没有正在进行的工作")
            return
        
        # 找到最后一个未结束的工作
        current_work = None
        for record in reversed(self.work_records):
            if record["end_time"] is None:
                current_work = record
                break
        
        if current_work is None:
            print("没有正在进行的工作")
            return
        
        end_time = datetime.now()
        current_work["end_time"] = end_time
        current_work["duration"] = end_time - current_work["start_time"]
        
        duration_str = str(current_work["duration"]).split('.')[0]  # 移除微秒部分
        print(f"结束工作: {current_work['task_name']} (结束时间: {end_time.strftime('%H:%M:%S')}, 持续时间: {duration_str})")
    
    def get_daily_summary(self, target_date=None):
        """
        获取每日工作摘要
        
        参数:
            target_date (date): 目标日期，默认为今天
        """
        if target_date is None:
            target_date = datetime.now().date()
        
        print(f"\n=== {target_date.strftime('%Y年%m月%d日')} 工作摘要 ===")
        
        # 筛选指定日期的工作记录
        daily_records = [
            record for record in self.work_records
            if record["start_time"].date() == target_date and record["duration"] is not None
        ]
        
        if not daily_records:
            print("当天没有完成的工作记录")
            return
        
        total_duration = timedelta()
        print("工作记录:")
        for record in daily_records:
            duration_str = str(record["duration"]).split('.')[0]
            start_str = record["start_time"].strftime('%H:%M')
            end_str = record["end_time"].strftime('%H:%M')
            print(f"  {record['task_name']}: {start_str}-{end_str} ({duration_str})")
            total_duration += record["duration"]
        
        total_hours = total_duration.total_seconds() / 3600
        print(f"\n总工作时间: {str(total_duration).split('.')[0]} ({total_hours:.2f} 小时)")
    
    def get_weekly_summary(self, weeks_ago=0):
        """
        获取周工作摘要
        
        参数:
            weeks_ago (int): 几周前，默认为本周
        """
        today = datetime.now().date()
        # 计算周一日期
        monday = today - timedelta(days=today.weekday()) - timedelta(weeks=weeks_ago)
        sunday = monday + timedelta(days=6)
        
        print(f"\n=== {monday.strftime('%Y年%m月%d日')}-{sunday.strftime('%m月%d日')} 周工作摘要 ===")
        
        # 筛选本周的工作记录
        weekly_records = [
            record for record in self.work_records
            if monday <= record["start_time"].date() <= sunday and record["duration"] is not None
        ]
        
        if not weekly_records:
            print("本周没有完成的工作记录")
            return
        
        # 按日期分组
        daily_totals = {}
        task_totals = {}
        
        for record in weekly_records:
            record_date = record["start_time"].date()
            if record_date not in daily_totals:
                daily_totals[record_date] = timedelta()
            daily_totals[record_date] += record["duration"]
            
            task_name = record["task_name"]
            if task_name not in task_totals:
                task_totals[task_name] = timedelta()
            task_totals[task_name] += record["duration"]
        
        # 显示每日总计
        print("每日工作时间:")
        for date_key in sorted(daily_totals.keys()):
            duration = daily_totals[date_key]
            hours = duration.total_seconds() / 3600
            print(f"  {date_key.strftime('%m月%d日')}: {str(duration).split('.')[0]} ({hours:.2f} 小时)")
        
        # 显示任务总计
        print("\n任务时间分布:")
        sorted_tasks = sorted(task_totals.items(), key=lambda x: x[1], reverse=True)
        total_week_duration = sum(task_totals.values(), timedelta())
        total_week_hours = total_week_duration.total_seconds() / 3600
        
        for task_name, duration in sorted_tasks:
            hours = duration.total_seconds() / 3600
            percentage = (hours / total_week_hours) * 100 if total_week_hours > 0 else 0
            print(f"  {task_name}: {str(duration).split('.')[0]} ({hours:.2f} 小时, {percentage:.1f}%)")
        
        print(f"\n本周总工作时间: {str(total_week_duration).split('.')[0]} ({total_week_hours:.2f} 小时)")
    
    def export_records(self, filename):
        """
        导出工作记录
        
        参数:
            filename (str): 导出文件名
        """
        export_data = []
        for record in self.work_records:
            export_record = {
                "task_name": record["task_name"],
                "start_time": record["start_time"].isoformat() if record["start_time"] else None,
                "end_time": record["end_time"].isoformat() if record["end_time"] else None,
                "duration_seconds": record["duration"].total_seconds() if record["duration"] else None
            }
            export_data.append(export_record)
        
        try:
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(export_data, f, ensure_ascii=False, indent=2)
            print(f"工作记录已导出到: {filename}")
        except Exception as e:
            print(f"导出记录失败: {e}")
    
    def import_records(self, filename):
        """
        导入工作记录
        
        参数:
            filename (str): 导入文件名
        """
        try:
            with open(filename, "r", encoding="utf-8") as f:
                import_data = json.load(f)
            
            self.work_records = []
            for record_data in import_data:
                record = {
                    "task_name": record_data["task_name"],
                    "start_time": datetime.fromisoformat(record_data["start_time"]) if record_data["start_time"] else None,
                    "end_time": datetime.fromisoformat(record_data["end_time"]) if record_data["end_time"] else None,
                    "duration": timedelta(seconds=record_data["duration_seconds"]) if record_data["duration_seconds"] else None
                }
                self.work_records.append(record)
            
            print(f"工作记录已从 {filename} 导入")
        except Exception as e:
            print(f"导入记录失败: {e}")

# 使用工作时间计算器
print("创建工作时间计算器:")
work_calculator = WorkTimeCalculator()

# 模拟工作记录
print("\n模拟工作记录:")
work_calculator.start_work("编写代码")
# 模拟工作1小时
import time
time.sleep(1)  # 实际使用中这里会是实际工作时间
work_calculator.end_work()

work_calculator.start_work("代码审查")
time.sleep(1)
work_calculator.end_work()

work_calculator.start_work("会议")
time.sleep(1)
work_calculator.end_work()

# 获取每日摘要
work_calculator.get_daily_summary()

# 获取周摘要
work_calculator.get_weekly_summary()

# 导出记录
work_calculator.export_records("work_records.json")

# 创建新的计算器并导入记录
print("\n导入记录测试:")
new_calculator = WorkTimeCalculator()
new_calculator.import_records("work_records.json")
new_calculator.get_daily_summary()

# 清理文件
import os
if os.path.exists("work_records.json"):
    os.remove("work_records.json")
```

### 代码说明

**案例1代码解释**：
1. `datetime.now()`：获取当前日期时间
2. `timedelta(days=1, hours=2)`：创建时间差对象
3. `strftime('%Y-%m-%d %H:%M:%S')`：格式化时间显示
4. `strptime(time_str, format_str)`：解析时间字符串

如果时间字符串格式与指定格式不匹配，strptime会抛出ValueError异常。

**案例2代码解释**：
1. `datetime.fromisoformat(record_data["start_time"])`：解析ISO格式的时间字符串
2. `duration.total_seconds()`：将时间差转换为秒数
3. `timedelta(seconds=record_data["duration_seconds"])`：从秒数创建时间差对象
4. `divmod(time_diff.seconds, 3600)`：计算小时和剩余秒数

如果忘记处理未结束的工作记录，在计算时间时会出现NoneType错误。

## 3. math和random模块 - 数学计算和随机数

### 知识点解析

**概念定义**：math模块就像一个"科学计算器"，提供了各种数学函数，如三角函数、对数函数、幂函数等。random模块则像一个"随机数生成器"，可以生成各种随机数，用于模拟、游戏或加密等场景。

**核心规则**：
1. math模块提供数学常数和函数
2. random模块提供随机数生成功能
3. 使用math.radians()和math.degrees()进行角度转换
4. 使用random.seed()设置随机种子以获得可重现的结果

**常见易错点**：
1. 忘记角度和弧度的转换导致三角函数计算错误
2. 对负数开平方或对数导致数学域错误
3. 不设置随机种子导致结果无法重现
4. 误用random.randint()和random.randrange()的参数

### 实战案例

#### 案例1：科学计算器
```python
# 科学计算器
print("===科学计算器===")

import math
import random

class ScientificCalculator:
    """科学计算器"""
    
    def __init__(self):
        """初始化科学计算器"""
        print("科学计算器已启动")
    
    def basic_operations(self, a, b):
        """
        基本运算
        
        参数:
            a (float): 第一个数
            b (float): 第二个数
        """
        print(f"\n=== 基本运算 ({a}, {b}) ===")
        print(f"加法: {a} + {b} = {a + b}")
        print(f"减法: {a} - {b} = {a - b}")
        print(f"乘法: {a} * {b} = {a * b}")
        
        if b != 0:
            print(f"除法: {a} / {b} = {a / b}")
            print(f"取余: {a} % {b} = {a % b}")
            print(f"整除: {a} // {b} = {a // b}")
        else:
            print("除法: 除数不能为零")
        
        print(f"幂运算: {a} ** {b} = {a ** b}")
    
    def math_functions(self, x):
        """
        数学函数
        
        参数:
            x (float): 输入值
        """
        print(f"\n=== 数学函数 (x = {x}) ===")
        
        # 基本函数
        print(f"绝对值: abs({x}) = {abs(x)}")
        print(f"向上取整: math.ceil({x}) = {math.ceil(x)}")
        print(f"向下取整: math.floor({x}) = {math.floor(x)}")
        
        # 幂和对数函数
        if x > 0:
            print(f"平方根: math.sqrt({x}) = {math.sqrt(x):.6f}")
            print(f"自然对数: math.log({x}) = {math.log(x):.6f}")
            print(f"以10为底的对数: math.log10({x}) = {math.log10(x):.6f}")
        elif x == 0:
            print("平方根: 0")
            print("自然对数: 负无穷")
            print("以10为底的对数: 负无穷")
        else:
            print("平方根: 未定义（负数）")
            print("自然对数: 未定义（负数）")
            print("以10为底的对数: 未定义（负数）")
        
        print(f"e的x次方: math.exp({x}) = {math.exp(x):.6f}")
        print(f"x的平方: math.pow({x}, 2) = {math.pow(x, 2):.6f}")
        
        # 三角函数（需要将角度转换为弧度）
        rad = math.radians(x)
        print(f"角度转弧度: math.radians({x}) = {rad:.6f}")
        print(f"sin({x}°) = {math.sin(rad):.6f}")
        print(f"cos({x}°) = {math.cos(rad):.6f}")
        print(f"tan({x}°) = {math.tan(rad):.6f}")
        
        # 反三角函数
        if -1 <= x <= 1:
            print(f"arcsin({x}) = {math.degrees(math.asin(x)):.2f}°")
            print(f"arccos({x}) = {math.degrees(math.acos(x)):.2f}°")
        print(f"arctan({x}) = {math.degrees(math.atan(x)):.2f}°")
    
    def constants_and_advanced_functions(self):
        """常数和高级函数"""
        print(f"\n=== 数学常数 ===")
        print(f"圆周率 π: {math.pi:.10f}")
        print(f"自然常数 e: {math.e:.10f}")
        print(f"2π (τ): {math.tau:.10f}")
        print(f"正无穷: {math.inf}")
        print(f"负无穷: {-math.inf}")
        print(f"非数字: {math.nan}")
        
        print(f"\n=== 高级函数 ===")
        print(f"最大公约数 gcd(48, 18): {math.gcd(48, 18)}")
        print(f"阶乘 5!: {math.factorial(5)}")
        
        # 误差函数
        print(f"误差函数 erf(1): {math.erf(1):.6f}")
        
        # 伽马函数
        print(f"伽马函数 gamma(5): {math.gamma(5):.6f}")
        
        # 双曲函数
        print(f"双曲正弦 sinh(1): {math.sinh(1):.6f}")
        print(f"双曲余弦 cosh(1): {math.cosh(1):.6f}")
        print(f"双曲正切 tanh(1): {math.tanh(1):.6f}")
    
    def statistics_functions(self, numbers):
        """
        统计函数
        
        参数:
            numbers (list): 数字列表
        """
        if not numbers:
            print("数字列表为空")
            return
        
        print(f"\n=== 统计函数 ({numbers}) ===")
        print(f"求和: {sum(numbers)}")
        print(f"平均值: {sum(numbers) / len(numbers):.2f}")
        print(f"最大值: {max(numbers)}")
        print(f"最小值: {min(numbers)}")
        
        # 方差和标准差
        mean = sum(numbers) / len(numbers)
        variance = sum((x - mean) ** 2 for x in numbers) / len(numbers)
        std_dev = math.sqrt(variance)
        print(f"方差: {variance:.2f}")
        print(f"标准差: {std_dev:.2f}")
        
        # 中位数
        sorted_numbers = sorted(numbers)
        n = len(sorted_numbers)
        if n % 2 == 0:
            median = (sorted_numbers[n//2 - 1] + sorted_numbers[n//2]) / 2
        else:
            median = sorted_numbers[n//2]
        print(f"中位数: {median}")

# 使用科学计算器
print("创建科学计算器:")
calculator = ScientificCalculator()

# 基本运算
calculator.basic_operations(10, 3)

# 数学函数
calculator.math_functions(30)

# 常数和高级函数
calculator.constants_and_advanced_functions()

# 统计函数
calculator.statistics_functions([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
```

#### 案例2：概率统计模拟器
```python
# 概率统计模拟器
print("\n===概率统计模拟器===")

import random
import math
from collections import Counter

class ProbabilitySimulator:
    """概率统计模拟器"""
    
    def __init__(self):
        """初始化概率统计模拟器"""
        print("概率统计模拟器已启动")
    
    def coin_flip_simulation(self, num_flips=1000):
        """
        抛硬币模拟
        
        参数:
            num_flips (int): 抛硬币次数
        """
        print(f"\n=== 抛硬币模拟 ({num_flips} 次) ===")
        
        # 设置随机种子以获得可重现的结果
        random.seed(42)
        
        results = []
        for _ in range(num_flips):
            # 0表示反面，1表示正面
            flip = random.randint(0, 1)
            results.append("正面" if flip == 1 else "反面")
        
        # 统计结果
        counter = Counter(results)
        heads_count = counter["正面"]
        tails_count = counter["反面"]
        
        print(f"正面次数: {heads_count} ({heads_count/num_flips*100:.1f}%)")
        print(f"反面次数: {tails_count} ({tails_count/num_flips*100:.1f}%)")
        
        # 计算与理论值的偏差
        expected = num_flips / 2
        heads_deviation = abs(heads_count - expected) / expected * 100
        print(f"正面偏差: {heads_deviation:.1f}%")
    
    def dice_roll_simulation(self, num_rolls=1000, num_dice=2):
        """
        骰子投掷模拟
        
        参数:
            num_rolls (int): 投掷次数
            num_dice (int): 骰子数量
        """
        print(f"\n=== {num_dice}个骰子投掷模拟 ({num_rolls} 次) ===")
        
        random.seed(42)
        
        results = []
        for _ in range(num_rolls):
            # 投掷多个骰子并求和
            roll_sum = sum(random.randint(1, 6) for _ in range(num_dice))
            results.append(roll_sum)
        
        # 统计结果
        counter = Counter(results)
        total_possible_outcomes = 6 ** num_dice
        
        print("点数分布:")
        for point in sorted(counter.keys()):
            count = counter[point]
            probability = count / num_rolls * 100
            theoretical_prob = self._theoretical_dice_probability(point, num_dice) * 100
            print(f"  {point}点: {count}次 ({probability:.1f}%) [理论: {theoretical_prob:.1f}%]")
    
    def _theoretical_dice_probability(self, target_sum, num_dice):
        """
        计算骰子点数和的理论概率
        
        参数:
            target_sum (int): 目标点数和
            num_dice (int): 骰子数量
            
        返回:
            float: 理论概率
        """
        # 这是一个简化的计算方法，适用于少量骰子
        if num_dice == 1:
            return 1/6 if 1 <= target_sum <= 6 else 0
        elif num_dice == 2:
            # 对于两个骰子，点数和的概率分布是已知的
            if 2 <= target_sum <= 7:
                return (target_sum - 1) / 36
            elif 8 <= target_sum <= 12:
                return (13 - target_sum) / 36
            else:
                return 0
        else:
            # 对于更多骰子，使用近似计算
            return 1 / (6 ** num_dice)  # 简化处理
    
    def normal_distribution_simulation(self, sample_size=10000):
        """
        正态分布模拟（使用中心极限定理）
        
        参数:
            sample_size (int): 样本大小
        """
        print(f"\n=== 正态分布模拟 ({sample_size} 个样本) ===")
        
        random.seed(42)
        
        # 使用中心极限定理生成近似正态分布的数据
        # 通过求多个均匀分布随机数的平均值来近似正态分布
        samples = []
        for _ in range(sample_size):
            # 生成12个均匀分布的随机数并求和，减去6得到近似标准正态分布
            uniform_sum = sum(random.random() for _ in range(12))
            standard_normal = uniform_sum - 6
            samples.append(standard_normal)
        
        # 计算统计信息
        mean = sum(samples) / len(samples)
        variance = sum((x - mean) ** 2 for x in samples) / len(samples)
        std_dev = math.sqrt(variance)
        
        print(f"样本均值: {mean:.4f} (理论值: 0)")
        print(f"样本标准差: {std_dev:.4f} (理论值: 1)")
        
        # 分组统计
        print("\n分布情况:")
        min_val = min(samples)
        max_val = max(samples)
        interval = (max_val - min_val) / 10
        
        for i in range(10):
            lower = min_val + i * interval
            upper = min_val + (i + 1) * interval
            count = sum(1 for x in samples if lower <= x < upper)
            if i == 9:  # 最后一个区间包含上界
                count = sum(1 for x in samples if lower <= x <= upper)
            
            percentage = count / len(samples) * 100
            print(f"  [{lower:5.2f}, {upper:5.2f}): {count:4d} ({percentage:4.1f}%)")
    
    def random_sampling(self, population, sample_size):
        """
        随机抽样
        
        参数:
            population (list): 总体
            sample_size (int): 样本大小
        """
        print(f"\n=== 随机抽样 ===")
        print(f"总体大小: {len(population)}")
        print(f"样本大小: {sample_size}")
        
        if sample_size > len(population):
            print("样本大小不能超过总体大小")
            return
        
        # 不重复抽样
        sample_without_replacement = random.sample(population, sample_size)
        print(f"不重复抽样: {sample_without_replacement}")
        
        # 重复抽样
        sample_with_replacement = [random.choice(population) for _ in range(sample_size)]
        print(f"重复抽样: {sample_with_replacement}")
        
        # 随机打乱
        shuffled_population = population.copy()
        random.shuffle(shuffled_population)
        print(f"随机打乱前5个: {shuffled_population[:5]}")
    
    def monte_carlo_pi_estimation(self, num_points=1000000):
        """
        蒙特卡洛方法估算π值
        
        参数:
            num_points (int): 随机点数量
        """
        print(f"\n=== 蒙特卡洛估算π值 ({num_points} 个点) ===")
        
        random.seed(42)
        
        points_inside_circle = 0
        
        for _ in range(num_points):
            # 在单位正方形内生成随机点
            x = random.uniform(-1, 1)
            y = random.uniform(-1, 1)
            
            # 检查点是否在单位圆内
            if x**2 + y**2 <= 1:
                points_inside_circle += 1
        
        # 根据蒙特卡洛方法，π ≈ 4 * (圆内点数 / 总点数)
        estimated_pi = 4 * points_inside_circle / num_points
        error = abs(estimated_pi - math.pi) / math.pi * 100
        
        print(f"估算的π值: {estimated_pi:.6f}")
        print(f"真实π值: {math.pi:.6f}")
        print(f"误差: {error:.4f}%")

# 使用概率统计模拟器
print("创建概率统计模拟器:")
simulator = ProbabilitySimulator()

# 抛硬币模拟
simulator.coin_flip_simulation(1000)

# 骰子投掷模拟
simulator.dice_roll_simulation(1000, 2)

# 正态分布模拟
simulator.normal_distribution_simulation(10000)

# 随机抽样
population = list(range(1, 101))  # 1到100的数字
simulator.random_sampling(population, 10)

# 蒙特卡洛估算π值
simulator.monte_carlo_pi_estimation(100000)
```

### 代码说明

**案例1代码解释**：
1. `math.sqrt(x)`：计算平方根
2. `math.sin(math.radians(x))`：先将角度转换为弧度再计算正弦值
3. `math.factorial(5)`：计算阶乘
4. `sum((x - mean) ** 2 for x in numbers) / len(numbers)`：计算方差

如果对负数调用math.sqrt()，会抛出ValueError异常。

**案例2代码解释**：
1. `random.randint(0, 1)`：生成0或1的随机整数
2. `random.sample(population, sample_size)`：不重复随机抽样
3. `random.uniform(-1, 1)`：生成指定范围内的随机浮点数
4. `random.seed(42)`：设置随机种子以获得可重现的结果

如果sample_size大于总体大小，random.sample()会抛出ValueError异常。

## 4. json和re模块 - 数据处理和文本匹配

### 知识点解析

**概念定义**：json模块就像一个"数据翻译官"，可以将Python对象转换为JSON格式的文本，也可以将JSON文本转换为Python对象，便于数据存储和传输。re模块则像一个"文本侦探"，可以使用正则表达式在文本中查找、替换特定模式的内容。

**核心规则**：
1. json模块用于JSON数据的序列化和反序列化
2. re模块用于正则表达式匹配和文本处理
3. 使用json.dumps()和json.loads()处理字符串
4. 使用json.dump()和json.load()处理文件

**常见易错点**：
1. 忘记处理JSON解析异常
2. 正则表达式写错导致匹配不到预期内容
3. 不使用原始字符串(r"")导致转义字符问题
4. 忘记指定编码格式导致中文乱码

### 实战案例

#### 案例1：数据序列化管理器
```python
# 数据序列化管理器
print("===数据序列化管理器===")

import json
import re
from datetime import datetime

class DataSerializationManager:
    """数据序列化管理器"""
    
    def __init__(self):
        """初始化数据序列化管理器"""
        print("数据序列化管理器已启动")
    
    def serialize_to_json(self, data, filename=None):
        """
        序列化数据到JSON
        
        参数:
            data: 要序列化的数据
            filename (str): 保存文件名，如果为None则返回字符串
            
        返回:
            str or bool: JSON字符串或保存成功与否
        """
        try:
            if filename:
                with open(filename, "w", encoding="utf-8") as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
                print(f"数据已保存到: {filename}")
                return True
            else:
                json_string = json.dumps(data, ensure_ascii=False, indent=2)
                return json_string
        except Exception as e:
            print(f"序列化数据失败: {e}")
            return False if filename else None
    
    def deserialize_from_json(self, source):
        """
        从JSON反序列化数据
        
        参数:
            source (str): JSON字符串或文件名
            
        返回:
            object: 反序列化的数据
        """
        try:
            # 判断是文件名还是JSON字符串
            if source.endswith('.json') and len(source) > 5:
                # 假设是文件名
                with open(source, "r", encoding="utf-8") as f:
                    data = json.load(f)
                print(f"数据已从 {source} 加载")
            else:
                # 假设是JSON字符串
                data = json.loads(source)
            return data
        except FileNotFoundError:
            print(f"文件未找到: {source}")
            return None
        except json.JSONDecodeError as e:
            print(f"JSON解析错误: {e}")
            return None
        except Exception as e:
            print(f"反序列化数据失败: {e}")
            return None
    
    def create_sample_data(self):
        """创建示例数据"""
        return {
            "用户信息": {
                "姓名": "张三",
                "年龄": 28,
                "邮箱": "zhangsan@example.com",
                "电话": "13812345678",
                "地址": {
                    "省份": "北京市",
                    "城市": "北京市",
                    "详细地址": "朝阳区某某街道123号"
                },
                "兴趣爱好": ["阅读", "游泳", "编程"]
            },
            "订单信息": [
                {
                    "订单号": "ORD202312001",
                    "商品": "笔记本电脑",
                    "价格": 5999.00,
                    "数量": 1,
                    "状态": "已发货"
                },
                {
                    "订单号": "ORD202312002",
                    "商品": "无线鼠标",
                    "价格": 99.00,
                    "数量": 2,
                    "状态": "已付款"
                }
            ],
            "系统信息": {
                "创建时间": datetime.now().isoformat(),
                "版本": "1.0.0",
                "启用": True
            }
        }
    
    def validate_json_format(self, json_string):
        """
        验证JSON格式
        
        参数:
            json_string (str): JSON字符串
            
        返回:
            bool: 格式是否正确
        """
        try:
            json.loads(json_string)
            return True
        except json.JSONDecodeError:
            return False
    
    def format_json_string(self, json_string):
        """
        格式化JSON字符串
        
        参数:
            json_string (str): JSON字符串
            
        返回:
            str: 格式化后的JSON字符串
        """
        try:
            data = json.loads(json_string)
            return json.dumps(data, ensure_ascii=False, indent=2)
        except json.JSONDecodeError as e:
            print(f"JSON格式错误: {e}")
            return None

# 使用数据序列化管理器
print("创建数据序列化管理器:")
manager = DataSerializationManager()

# 创建示例数据
sample_data = manager.create_sample_data()
print("创建示例数据完成")

# 序列化到JSON字符串
print("\n序列化到JSON字符串:")
json_string = manager.serialize_to_json(sample_data)
if json_string:
    print("序列化成功:")
    print(json_string[:200] + "..." if len(json_string) > 200 else json_string)

# 保存到文件
print("\n保存到文件:")
manager.serialize_to_json(sample_data, "sample_data.json")

# 从文件加载
print("\n从文件加载:")
loaded_data = manager.deserialize_from_json("sample_data.json")
if loaded_data:
    print("加载成功，用户姓名:", loaded_data["用户信息"]["姓名"])

# 验证JSON格式
print("\n验证JSON格式:")
valid_json = '{"姓名": "李四", "年龄": 25}'
invalid_json = '{"姓名": "李四", "年龄": 25'  # 缺少闭合括号

print(f"有效JSON: {manager.validate_json_format(valid_json)}")
print(f"无效JSON: {manager.validate_json_format(invalid_json)}")

# 格式化JSON字符串
print("\n格式化JSON字符串:")
messy_json = '{"姓名":"王五","年龄":30,"城市":"上海"}'
formatted_json = manager.format_json_string(messy_json)
if formatted_json:
    print("格式化后:")
    print(formatted_json)

# 清理文件
import os
if os.path.exists("sample_data.json"):
    os.remove("sample_data.json")
```

#### 案例2：文本处理和信息提取器
```python
# 文本处理和信息提取器
print("\n===文本处理和信息提取器===")

import re
import json

class TextProcessor:
    """文本处理和信息提取器"""
    
    def __init__(self):
        """初始化文本处理器"""
        print("文本处理和信息提取器已启动")
    
    def extract_emails(self, text):
        """
        提取邮箱地址
        
        参数:
            text (str): 文本内容
            
        返回:
            list: 邮箱地址列表
        """
        # 邮箱正则表达式
        email_pattern = r'\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b'
        emails = re.findall(email_pattern, text)
        return emails
    
    def extract_phone_numbers(self, text):
        """
        提取电话号码
        
        参数:
            text (str): 文本内容
            
        返回:
            list: 电话号码列表
        """
        # 中国手机号正则表达式
        phone_pattern = r'\b1[3-9]\d{9}\b'
        phones = re.findall(phone_pattern, text)
        return phones
    
    def extract_urls(self, text):
        """
        提取URL链接
        
        参数:
            text (str): 文本内容
            
        返回:
            list: URL列表
        """
        # URL正则表达式
        url_pattern = r'https?://(?:[-\w.])+(?:[:\d]+)?(?:/(?:[\w/_.])*(?:\?(?:[\w&=%.])*)?(?:#(?:[\w.])*)?)?'
        urls = re.findall(url_pattern, text)
        return urls
    
    def mask_sensitive_info(self, text):
        """
        遮蔽敏感信息
        
        参数:
            text (str): 文本内容
            
        返回:
            str: 遮蔽后的文本
        """
        # 遮蔽手机号
        text = re.sub(r'\b(1[3-9]\d)(\d{4})(\d{4})\b', r'\1****\3', text)
        
        # 遮蔽邮箱（保留@前第一个字符和@后域名）
        text = re.sub(r'\b([a-zA-Z0-9])[a-zA-Z0-9._%+-]*@([a-zA-Z0-9.-]+\.[a-zA-Z]{2,})\b', r'\1***@\2', text)
        
        # 遮蔽身份证号
        text = re.sub(r'\b(\d{4})\d{10}(\d{4})\b', r'\1**********\2', text)
        
        return text
    
    def find_keywords(self, text, keywords):
        """
        查找关键词
        
        参数:
            text (str): 文本内容
            keywords (list): 关键词列表
            
        返回:
            dict: 关键词及其出现次数
        """
        result = {}
        for keyword in keywords:
            # 使用单词边界确保精确匹配
            pattern = r'\b' + re.escape(keyword) + r'\b'
            matches = re.findall(pattern, text, re.IGNORECASE)
            result[keyword] = len(matches)
        return result
    
    def replace_text(self, text, pattern, replacement, ignore_case=False):
        """
        替换文本
        
        参数:
            text (str): 原文本
            pattern (str): 要替换的模式
            replacement (str): 替换内容
            ignore_case (bool): 是否忽略大小写
            
        返回:
            str: 替换后的文本
        """
        flags = re.IGNORECASE if ignore_case else 0
        return re.sub(pattern, replacement, text, flags=flags)
    
    def split_text(self, text, delimiter_pattern):
        """
        分割文本
        
        参数:
            text (str): 文本内容
            delimiter_pattern (str): 分隔符模式
            
        返回:
            list: 分割后的文本列表
        """
        return re.split(delimiter_pattern, text)
    
    def validate_input(self, text, pattern_type):
        """
        验证输入格式
        
        参数:
            text (str): 要验证的文本
            pattern_type (str): 验证类型 (email, phone, id_card, ip)
            
        返回:
            bool: 是否符合格式
        """
        patterns = {
            "email": r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$',
            "phone": r'^1[3-9]\d{9}$',
            "id_card": r'^\d{17}[\dXx]$',
            "ip": r'^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$'
        }
        
        if pattern_type in patterns:
            return bool(re.match(patterns[pattern_type], text))
        else:
            raise ValueError(f"不支持的验证类型: {pattern_type}")

# 使用文本处理器
print("创建文本处理器:")
processor = TextProcessor()

# 测试文本
test_text = """
联系我们：
邮箱：support@example.com 或 admin@test.org
电话：13812345678，客服热线：400-123-4567
网站：https://www.example.com 或 http://test.org:8080/page?id=123
地址：北京市朝阳区某某街道123号
身份证号：110101199001011234
IP地址：192.168.1.1

重要通知：所有用户必须在2023年12月31日前完成信息更新。
关键词包括：用户、信息、更新、完成、必须。
"""

# 提取邮箱
print("提取邮箱:")
emails = processor.extract_emails(test_text)
for email in emails:
    print(f"  {email}")

# 提取电话号码
print("\n提取电话号码:")
phones = processor.extract_phone_numbers(test_text)
for phone in phones:
    print(f"  {phone}")

# 提取URL
print("\n提取URL:")
urls = processor.extract_urls(test_text)
for url in urls:
    print(f"  {url}")

# 遮蔽敏感信息
print("\n遮蔽敏感信息:")
masked_text = processor.mask_sensitive_info(test_text)
print(masked_text)

# 查找关键词
print("\n查找关键词:")
keywords = ["用户", "信息", "更新", "完成", "必须"]
keyword_counts = processor.find_keywords(test_text, keywords)
for keyword, count in keyword_counts.items():
    print(f"  '{keyword}': {count} 次")

# 替换文本
print("\n替换文本:")
replaced_text = processor.replace_text(test_text, r"2023年12月31日", "2024年1月31日")
print("替换日期后:")
print(replaced_text.split('\n')[-3])  # 只显示最后一行

# 分割文本
print("\n分割文本:")
sentences = processor.split_text(test_text, r'[。！？]')
print(f"分割成 {len(sentences)} 句话，前3句:")
for i, sentence in enumerate(sentences[:3]):
    print(f"  {i+1}. {sentence.strip()}")

# 验证输入格式
print("\n验证输入格式:")
test_inputs = [
    ("test@example.com", "email"),
    ("13812345678", "phone"),
    ("110101199001011234", "id_card"),
    ("192.168.1.1", "ip"),
    ("invalid-email", "email"),
    ("12345", "phone")
]

for input_text, input_type in test_inputs:
    is_valid = processor.validate_input(input_text, input_type)
    print(f"  {input_text} ({input_type}): {'有效' if is_valid else '无效'}")
```

### 代码说明

**案例1代码解释**：
1. `json.dumps(data, ensure_ascii=False, indent=2)`：将Python对象序列化为格式化的JSON字符串
2. `json.loads(json_string)`：将JSON字符串反序列化为Python对象
3. `json.dump(data, f, ensure_ascii=False, indent=2)`：将数据直接写入文件
4. `json.load(f)`：从文件直接读取并反序列化

如果JSON字符串格式不正确，json.loads()会抛出JSONDecodeError异常。

**案例2代码解释**：
1. `re.findall(pattern, text)`：查找所有匹配的文本
2. `re.sub(pattern, replacement, text)`：替换匹配的文本
3. `re.split(delimiter_pattern, text)`：按模式分割文本
4. `re.escape(keyword)`：转义特殊字符以进行字面量匹配

如果正则表达式中有特殊字符没有正确转义，可能会导致匹配结果不符合预期。

## 5. collections和pathlib模块 - 高级数据结构和路径操作

### 知识点解析

**概念定义**：collections模块就像一个"高级工具箱"，提供了比内置数据类型更强大的容器类，如计数器、默认字典、命名元组等。pathlib模块则像一个"现代化的路径专家"，以面向对象的方式处理文件系统路径，比传统的os.path更加直观和易用。

**核心规则**：
1. collections模块提供高性能的容器数据类型
2. pathlib模块提供面向对象的文件系统路径操作
3. Counter用于统计元素出现次数
4. Path对象提供丰富的路径操作方法

**常见易错点**：
1. 忘记collections中的容器类型是不可变的还是可变的
2. 混用os.path和pathlib导致代码不一致
3. 不处理路径不存在的情况
4. 忘记指定文件编码导致中文乱码

### 实战案例

#### 案例1：数据分析工具
```python
# 数据分析工具
print("===数据分析工具===")

from collections import Counter, defaultdict, namedtuple, deque
from pathlib import Path
import json

class DataAnalyzer:
    """数据分析工具"""
    
    def __init__(self):
        """初始化数据分析工具"""
        print("数据分析工具已启动")
    
    def analyze_text_frequency(self, text):
        """
        分析文本词频
        
        参数:
            text (str): 要分析的文本
            
        返回:
            Counter: 词频统计
        """
        # 简单的分词（按空格和标点符号分割）
        import re
        words = re.findall(r'\b[a-zA-Z]+\b', text.lower())
        
        # 使用Counter统计词频
        word_counter = Counter(words)
        return word_counter
    
    def analyze_character_frequency(self, text):
        """
        分析字符频率
        
        参数:
            text (str): 要分析的文本
            
        返回:
            Counter: 字符频率统计
        """
        # 过滤掉空格和换行符
        characters = [char for char in text if char not in ' \n\t']
        char_counter = Counter(characters)
        return char_counter
    
    def get_most_common_words(self, text, n=10):
        """
        获取最常见的单词
        
        参数:
            text (str): 文本内容
            n (int): 返回前n个最常见的单词
            
        返回:
            list: 最常见的单词及其频率
        """
        word_counter = self.analyze_text_frequency(text)
        return word_counter.most_common(n)
    
    def group_data_by_category(self, data):
        """
        按类别分组数据
        
        参数:
            data (list): 包含字典的列表，每个字典应有'category'键
            
        返回:
            defaultdict: 按类别分组的数据
        """
        # 使用defaultdict自动创建空列表
        grouped_data = defaultdict(list)
        
        for item in data:
            category = item.get('category', 'unknown')
            grouped_data[category].append(item)
        
        return grouped_data
    
    def create_data_structure(self):
        """创建数据结构示例"""
        # 使用namedtuple创建结构化数据
        Person = namedtuple('Person', ['name', 'age', 'city', 'occupation'])
        
        people = [
            Person('张三', 28, '北京', '工程师'),
            Person('李四', 32, '上海', '设计师'),
            Person('王五', 25, '北京', '工程师'),
            Person('赵六', 30, '广州', '产品经理'),
            Person('钱七', 28, '上海', '设计师')
        ]
        
        return people
    
    def analyze_people_data(self, people):
        """
        分析人员数据
        
        参数:
            people (list): namedtuple人员列表
        """
        print("\n=== 人员数据分析 ===")
        
        # 统计职业分布
        occupations = [person.occupation for person in people]
        occupation_counter = Counter(occupations)
        print("职业分布:")
        for occupation, count in occupation_counter.items():
            print(f"  {occupation}: {count}人")
        
        # 统计城市分布
        cities = [person.city for person in people]
        city_counter = Counter(cities)
        print("\n城市分布:")
        for city, count in city_counter.items():
            print(f"  {city}: {count}人")
        
        # 统计年龄分布
        ages = [person.age for person in people]
        age_counter = Counter(ages)
        print("\n年龄分布:")
        for age, count in sorted(age_counter.items()):
            print(f"  {age}岁: {count}人")
    
    def demonstrate_deque_usage(self):
        """演示deque的使用"""
        print("\n=== deque使用演示 ===")
        
        # 创建deque
        dq = deque([1, 2, 3, 4, 5])
        print(f"初始deque: {dq}")
        
        # 两端添加元素
        dq.append(6)        # 右端添加
        dq.appendleft(0)    # 左端添加
        print(f"添加元素后: {dq}")
        
        # 两端删除元素
        popped_right = dq.pop()      # 右端弹出
        popped_left = dq.popleft()   # 左端弹出
        print(f"弹出元素: {popped_right}(右), {popped_left}(左)")
        print(f"弹出后: {dq}")
        
        # 限制deque大小
        limited_dq = deque(maxlen=3)
        for i in range(6):
            limited_dq.append(i)
            print(f"添加{i}后: {limited_dq} (最大长度: {limited_dq.maxlen})")

# 使用数据分析工具
print("创建数据分析工具:")
analyzer = DataAnalyzer()

# 分析文本词频
sample_text = """
Python is a powerful programming language. Python is easy to learn and Python is widely used.
Many developers love Python because Python is versatile and Python has a great community.
Data science, web development, automation, and artificial intelligence all use Python.
Python's syntax is clean and readable, making Python a great choice for beginners.
"""

print("分析文本词频:")
word_freq = analyzer.get_most_common_words(sample_text, 5)
for word, count in word_freq:
    print(f"  {word}: {count}次")

# 分析字符频率
print("\n分析字符频率:")
char_freq = analyzer.analyze_character_frequency("hello world")
for char, count in char_freq.most_common(5):
    print(f"  '{char}': {count}次")

# 按类别分组数据
sample_data = [
    {'name': '项目A', 'category': '技术', 'priority': '高'},
    {'name': '项目B', 'category': '市场', 'priority': '中'},
    {'name': '项目C', 'category': '技术', 'priority': '低'},
    {'name': '项目D', 'category': '运营', 'priority': '高'},
    {'name': '项目E', 'category': '技术', 'priority': '中'}
]

print("\n按类别分组数据:")
grouped = analyzer.group_data_by_category(sample_data)
for category, items in grouped.items():
    print(f"  {category}类别 ({len(items)}项):")
    for item in items:
        print(f"    - {item['name']} (优先级: {item['priority']})")

# 创建和分析人员数据
people = analyzer.create_data_structure()
analyzer.analyze_people_data(people)

# 演示deque使用
analyzer.demonstrate_deque_usage()
```

#### 案例2：文件系统分析器
```python
# 文件系统分析器
print("\n===文件系统分析器===")

from collections import Counter, defaultdict
from pathlib import Path
import os

class FileSystemAnalyzer:
    """文件系统分析器"""
    
    def __init__(self):
        """初始化文件系统分析器"""
        print("文件系统分析器已启动")
    
    def analyze_directory(self, directory_path):
        """
        分析目录结构
        
        参数:
            directory_path (str): 目录路径
            
        返回:
            dict: 分析结果
        """
        directory = Path(directory_path)
        if not directory.exists():
            print(f"目录不存在: {directory_path}")
            return None
        
        if not directory.is_dir():
            print(f"路径不是目录: {directory_path}")
            return None
        
        print(f"开始分析目录: {directory_path}")
        
        # 统计信息
        file_count = 0
        dir_count = 0
        extension_counter = Counter()
        size_counter = Counter()
        size_distribution = defaultdict(int)
        
        try:
            # 递归遍历目录
            for item in directory.rglob('*'):
                if item.is_file():
                    file_count += 1
                    
                    # 统计文件扩展名
                    extension = item.suffix.lower() if item.suffix else '[无扩展名]'
                    extension_counter[extension] += 1
                    
                    # 统计文件大小
                    try:
                        size = item.stat().st_size
                        # 按大小分类
                        if size < 1024:  # < 1KB
                            size_category = '< 1KB'
                        elif size < 1024 * 1024:  # < 1MB
                            size_category = '1KB - 1MB'
                        elif size < 10 * 1024 * 1024:  # < 10MB
                            size_category = '1MB - 10MB'
                        elif size < 100 * 1024 * 1024:  # < 100MB
                            size_category = '10MB - 100MB'
                        else:  # >= 100MB
                            size_category = '>= 100MB'
                        
                        size_distribution[size_category] += 1
                        
                    except OSError:
                        pass  # 忽略无法访问的文件
                        
                elif item.is_dir():
                    dir_count += 1
            
            # 构建分析结果
            analysis = {
                'total_files': file_count,
                'total_directories': dir_count,
                'extensions': dict(extension_counter.most_common()),
                'size_distribution': dict(size_distribution),
                'largest_files': self._get_largest_files(directory, 5)
            }
            
            return analysis
            
        except Exception as e:
            print(f"分析目录时出错: {e}")
            return None
    
    def _get_largest_files(self, directory, count):
        """
        获取最大的文件
        
        参数:
            directory (Path): 目录路径
            count (int): 返回文件数量
            
        返回:
            list: 最大文件列表
        """
        files_with_size = []
        
        for item in directory.rglob('*'):
            if item.is_file():
                try:
                    size = item.stat().st_size
                    files_with_size.append((str(item), size))
                except OSError:
                    pass
        
        # 按大小排序并返回前count个
        files_with_size.sort(key=lambda x: x[1], reverse=True)
        return files_with_size[:count]
    
    def show_analysis_report(self, analysis):
        """
        显示分析报告
        
        参数:
            analysis (dict): 分析结果
        """
        if not analysis:
            print("没有分析数据")
            return
        
        print("\n=== 文件系统分析报告 ===")
        print(f"总文件数: {analysis['total_files']}")
        print(f"总目录数: {analysis['total_directories']}")
        
        # 显示文件扩展名统计
        if analysis['extensions']:
            print("\n文件类型统计 (前10种):")
            for extension, count in list(analysis['extensions'].items())[:10]:
                print(f"  {extension}: {count}个")
        
        # 显示文件大小分布
        if analysis['size_distribution']:
            print("\n文件大小分布:")
            for size_range, count in analysis['size_distribution'].items():
                print(f"  {size_range}: {count}个")
        
        # 显示最大的文件
        if analysis['largest_files']:
            print("\n最大的5个文件:")
            for file_path, size in analysis['largest_files']:
                # 格式化文件大小
                if size < 1024:
                    size_str = f"{size}B"
                elif size < 1024 * 1024:
                    size_str = f"{size/1024:.1f}KB"
                elif size < 1024 * 1024 * 1024:
                    size_str = f"{size/(1024*1024):.1f}MB"
                else:
                    size_str = f"{size/(1024*1024*1024):.1f}GB"
                
                print(f"  {size_str}: {file_path}")
    
    def create_sample_structure(self):
        """创建示例目录结构"""
        print("\n=== 创建示例目录结构 ===")
        
        # 创建测试目录结构
        structure = {
            "test_project": {
                "src": {
                    "main.py": "print('Hello, World!')",
                    "utils.py": "def helper():\n    return 'Helper function'",
                    "config.py": "CONFIG = {'debug': True}"
                },
                "docs": {
                    "README.md": "# Test Project\nThis is a test project.",
                    "guide.txt": "User guide content",
                    "api.md": "# API Documentation\nAPI details here."
                },
                "data": {
                    "users.json": '[{"name": "张三", "age": 25}]',
                    "config.xml": '<config><debug>true</debug></config>',
                    "large_file.txt": "Large file content. " * 1000  # 创建大文件
                },
                "tests": {
                    "test_main.py": "def test_main():\n    assert True",
                    "test_utils.py": "def test_utils():\n    assert True"
                }
            }
        }
        
        self._create_structure(structure)
        print("示例目录结构创建完成")
    
    def _create_structure(self, structure, base_path="."):
        """递归创建目录结构"""
        for name, content in structure.items():
            path = Path(base_path) / name
            if isinstance(content, dict):
                # 创建目录
                path.mkdir(exist_ok=True)
                # 递归创建子结构
                self._create_structure(content, path)
            else:
                # 创建文件
                with open(path, "w", encoding="utf-8") as f:
                    f.write(content)
    
    def cleanup_sample_structure(self):
        """清理示例目录结构"""
        print("\n=== 清理示例目录结构 ===")
        import shutil
        try:
            if Path("test_project").exists():
                shutil.rmtree("test_project")
                print("示例目录结构已清理")
            else:
                print("示例目录不存在")
        except Exception as e:
            print(f"清理目录时出错: {e}")

# 使用文件系统分析器
print("创建文件系统分析器:")
fs_analyzer = FileSystemAnalyzer()

# 创建示例结构
fs_analyzer.create_sample_structure()

# 分析目录
analysis = fs_analyzer.analyze_directory("test_project")

# 显示分析报告
fs_analyzer.show_analysis_report(analysis)

# 清理示例结构
fs_analyzer.cleanup_sample_structure()
```

### 代码说明

**案例1代码解释**：
1. `Counter(words)`：统计单词出现次数
2. `defaultdict(list)`：自动创建空列表的字典
3. `namedtuple('Person', ['name', 'age', 'city', 'occupation'])`：创建命名元组
4. `deque([1, 2, 3], maxlen=3)`：创建有限长度的双端队列

如果向namedtuple实例尝试赋值，会抛出AttributeError异常，因为namedtuple是不可变的。

**案例2代码解释**：
1. `Path(directory_path)`：创建Path对象
2. `directory.rglob('*')`：递归遍历目录中的所有项目
3. `item.stat().st_size`：获取文件大小
4. `item.suffix.lower()`：获取文件扩展名并转换为小写

如果目录中包含权限受限的文件，item.stat()可能会抛出OSError异常。

这些实战案例展示了Python标准库中常用模块的实际应用场景，包括系统操作、时间处理、数学计算、数据序列化、文本处理和高级数据结构等。通过这些例子，可以更好地理解如何在实际项目中使用这些模块来解决具体问题。

