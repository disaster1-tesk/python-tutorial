# Python文件操作知识点

## 1. 文件操作基础和open()函数

### 知识点解析

**概念定义**：文件操作就像我们对纸质文件的处理过程，可以打开文件查看内容（读取），可以在文件上写字（写入），也可以在文件末尾添加新内容（追加）。Python提供了简单易用的工具让我们能方便地操作计算机中的文件。

**核心规则**：
1. 使用`open()`函数打开文件，需要指定文件名和操作模式
2. 操作完成后必须关闭文件，推荐使用`with`语句自动管理
3. 文本文件需要指定编码格式，通常使用`utf-8`
4. 常见操作模式有：`r`(读取)、`w`(写入)、`a`(追加)

**常见易错点**：
1. 忘记关闭文件导致资源泄露
2. 没有指定编码格式导致中文乱码
3. 使用写入模式时意外覆盖重要文件
4. 文件路径写错导致找不到文件

### 实战案例

#### 案例1：个人记账本
```python
# 个人记账本
print("===个人记账本===")

import datetime
from pathlib import Path

# 创建账本文件管理器
class ExpenseTracker:
    """个人记账本"""
    
    def __init__(self, filename="expense_log.txt"):
        """
        初始化记账本
        
        参数:
            filename (str): 账本文件名
        """
        self.filename = filename
        # 确保账本文件存在
        Path(self.filename).touch(exist_ok=True)
    
    def add_expense(self, item, amount):
        """
        添加支出记录
        
        参数:
            item (str): 支出项目
            amount (float): 支出金额
        """
        # 获取当前时间
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # 准备记录内容
        record = f"[{timestamp}] {item}: ¥{amount:.2f}\n"
        
        # 使用with语句安全地写入文件
        try:
            with open(self.filename, "a", encoding="utf-8") as file:
                file.write(record)
            print(f"已记录支出: {item} ¥{amount:.2f}")
        except Exception as e:
            print(f"记录支出失败: {e}")
    
    def show_expenses(self, limit=None):
        """
        显示支出记录
        
        参数:
            limit (int): 显示记录数限制，None表示显示所有
        """
        try:
            with open(self.filename, "r", encoding="utf-8") as file:
                lines = file.readlines()
            
            if not lines:
                print("暂无支出记录")
                return
            
            print(f"\n=== 最近支出记录 ===")
            # 如果指定了限制，只显示最近的几条记录
            display_lines = lines[-limit:] if limit else lines
            
            total = 0
            for line in display_lines:
                print(f"  {line.strip()}")
                # 从记录中提取金额
                try:
                    amount_str = line.split("¥")[-1]
                    amount = float(amount_str)
                    total += amount
                except (IndexError, ValueError):
                    pass  # 忽略格式不正确的记录
            
            print(f"总计支出: ¥{total:.2f}")
            
        except FileNotFoundError:
            print("账本文件不存在")
        except Exception as e:
            print(f"读取支出记录失败: {e}")
    
    def clear_expenses(self):
        """清空所有支出记录"""
        try:
            with open(self.filename, "w", encoding="utf-8") as file:
                file.write("")  # 写入空内容清空文件
            print("已清空所有支出记录")
        except Exception as e:
            print(f"清空记录失败: {e}")

# 使用记账本
print("创建记账本:")
tracker = ExpenseTracker("my_expenses.txt")

# 添加支出记录
print("\n添加支出记录:")
tracker.add_expense("早餐", 15.5)
tracker.add_expense("午餐", 25.0)
tracker.add_expense("地铁", 6.0)
tracker.add_expense("书籍", 59.8)
tracker.add_expense("电影票", 45.0)

# 查看支出记录
print("\n查看支出记录:")
tracker.show_expenses()

# 只查看最近3条记录
print("\n查看最近3条记录:")
tracker.show_expenses(limit=3)

# 清空记录
print("\n清空记录:")
tracker.clear_expenses()

# 再次查看（应该没有记录了）
print("\n清空后查看:")
tracker.show_expenses()
```

#### 案例2：配置文件管理器
```python
# 配置文件管理器
print("\n===配置文件管理器===")

import json

class ConfigManager:
    """配置文件管理器"""
    
    def __init__(self, config_file="app_config.json"):
        """
        初始化配置管理器
        
        参数:
            config_file (str): 配置文件名
        """
        self.config_file = config_file
        self.config = self._load_default_config()
        self.load_config()
    
    def _load_default_config(self):
        """加载默认配置"""
        return {
            "app_name": "我的应用程序",
            "version": "1.0.0",
            "debug": False,
            "max_users": 100,
            "features": ["用户管理", "数据统计", "报表生成"],
            "database": {
                "host": "localhost",
                "port": 5432,
                "name": "myapp_db"
            }
        }
    
    def load_config(self):
        """从文件加载配置"""
        try:
            with open(self.config_file, "r", encoding="utf-8") as file:
                loaded_config = json.load(file)
            
            # 合并默认配置和加载的配置
            self.config.update(loaded_config)
            print(f"配置已从 {self.config_file} 加载")
            
        except FileNotFoundError:
            print(f"配置文件 {self.config_file} 不存在，使用默认配置")
            self.save_config()  # 创建默认配置文件
        except json.JSONDecodeError as e:
            print(f"配置文件格式错误: {e}，使用默认配置")
        except Exception as e:
            print(f"加载配置时发生错误: {e}，使用默认配置")
    
    def save_config(self):
        """保存配置到文件"""
        try:
            with open(self.config_file, "w", encoding="utf-8") as file:
                json.dump(self.config, file, ensure_ascii=False, indent=2)
            print(f"配置已保存到 {self.config_file}")
        except Exception as e:
            print(f"保存配置失败: {e}")
    
    def get(self, key, default=None):
        """
        获取配置项的值
        
        参数:
            key (str): 配置项键名
            default: 默认值
            
        返回:
            配置项的值
        """
        return self.config.get(key, default)
    
    def set(self, key, value):
        """
        设置配置项的值
        
        参数:
            key (str): 配置项键名
            value: 配置项值
        """
        self.config[key] = value
        print(f"配置项 '{key}' 已设置为 '{value}'")
    
    def show_config(self):
        """显示当前配置"""
        print(f"\n=== 当前配置 ({self.config_file}) ===")
        print(json.dumps(self.config, ensure_ascii=False, indent=2))

# 使用配置管理器
print("创建配置管理器:")
config_manager = ConfigManager("my_app_config.json")

# 显示默认配置
print("\n默认配置:")
config_manager.show_config()

# 修改配置
print("\n修改配置:")
config_manager.set("app_name", "超级记账本")
config_manager.set("debug", True)
config_manager.set("max_users", 200)

# 添加新的配置项
config_manager.set("theme", "dark")
config_manager.set("language", "zh-CN")

# 保存配置
print("\n保存配置:")
config_manager.save_config()

# 重新加载配置
print("\n重新加载配置:")
new_manager = ConfigManager("my_app_config.json")
new_manager.show_config()

# 获取特定配置项
print(f"\n应用名称: {new_manager.get('app_name')}")
print(f"调试模式: {new_manager.get('debug')}")
print(f"数据库主机: {new_manager.get('database', {}).get('host', '未设置')}")
```

### 代码说明

**案例1代码解释**：
1. `with open(self.filename, "a", encoding="utf-8") as file:`：使用with语句以追加模式打开文件，确保自动关闭
2. `file.write(record)`：向文件写入支出记录
3. `with open(self.filename, "r", encoding="utf-8") as file:`：以读取模式打开文件
4. `lines = file.readlines()`：读取所有行到列表中

如果忘记使用with语句，需要手动调用`file.close()`，如果中间发生异常可能导致文件未正确关闭，造成资源泄露。

**案例2代码解释**：
1. `json.dump(self.config, file, ensure_ascii=False, indent=2)`：将配置字典保存为格式化的JSON文件
2. `loaded_config = json.load(file)`：从JSON文件加载配置
3. `self.config.update(loaded_config)`：用加载的配置更新默认配置
4. `Path(self.filename).touch(exist_ok=True)`：确保文件存在

如果在保存JSON文件时不使用`ensure_ascii=False`，中文会被转换为Unicode编码，不利于人工阅读。

## 2. 文件读取和写入方法

### 知识点解析

**概念定义**：文件读取就像看书一样，可以一次看完一本书（read），也可以一次看一页（readline），或者快速浏览所有页面（readlines）。文件写入就像在空白纸上写字，可以一个字一个字地写（write），也可以一次写很多行（writelines）。

**核心规则**：
1. `read()`读取整个文件或指定字数
2. `readline()`每次读取一行
3. `readlines()`读取所有行并返回列表
4. `write()`写入字符串，`writelines()`写入字符串列表

**常见易错点**：
1. 读取大文件时一次性使用`read()`导致内存不足
2. 忘记在写入后添加换行符`\n`
3. 使用`writelines()`时列表元素没有换行符
4. 混淆文本模式和二进制模式

### 实战案例

#### 案例1：学生成绩统计系统
```python
# 学生成绩统计系统
print("===学生成绩统计系统===")

# 创建学生成绩文件
def create_sample_data():
    """创建示例成绩数据"""
    sample_data = """张三,数学,85
张三,英语,92
张三,物理,78
李四,数学,90
李四,英语,88
李四,物理,85
王五,数学,78
王五,英语,85
王五,物理,90
赵六,数学,92
赵六,英语,87
赵六,物理,88"""
    
    try:
        with open("student_scores.txt", "w", encoding="utf-8") as file:
            file.write(sample_data)
        print("示例成绩数据已创建")
    except Exception as e:
        print(f"创建示例数据失败: {e}")

# 创建示例数据
create_sample_data()

class ScoreAnalyzer:
    """成绩分析器"""
    
    def __init__(self, filename):
        """
        初始化成绩分析器
        
        参数:
            filename (str): 成绩文件名
        """
        self.filename = filename
        self.scores = []
        self.load_scores()
    
    def load_scores(self):
        """加载成绩数据"""
        try:
            with open(self.filename, "r", encoding="utf-8") as file:
                # 方法1: 使用readlines()逐行读取
                lines = file.readlines()
                
                for line in lines:
                    line = line.strip()  # 去除首尾空白字符
                    if line:  # 跳过空行
                        try:
                            name, subject, score = line.split(",")
                            self.scores.append({
                                "name": name,
                                "subject": subject,
                                "score": int(score)
                            })
                        except ValueError:
                            print(f"跳过格式错误的行: {line}")
            
            print(f"成功加载 {len(self.scores)} 条成绩记录")
            
        except FileNotFoundError:
            print(f"成绩文件 {self.filename} 不存在")
        except Exception as e:
            print(f"加载成绩数据失败: {e}")
    
    def get_student_scores(self, student_name):
        """
        获取指定学生的成绩
        
        参数:
            student_name (str): 学生姓名
            
        返回:
            list: 学生成绩列表
        """
        return [score for score in self.scores if score["name"] == student_name]
    
    def get_subject_scores(self, subject):
        """
        获取指定科目的成绩
        
        参数:
            subject (str): 科目名称
            
        返回:
            list: 科目成绩列表
        """
        return [score for score in self.scores if score["subject"] == subject]
    
    def calculate_student_average(self, student_name):
        """
        计算学生平均分
        
        参数:
            student_name (str): 学生姓名
            
        返回:
            float: 平均分
        """
        student_scores = self.get_student_scores(student_name)
        if not student_scores:
            return 0
        
        total = sum(score["score"] for score in student_scores)
        return total / len(student_scores)
    
    def calculate_subject_average(self, subject):
        """
        计算科目平均分
        
        参数:
            subject (str): 科目名称
            
        返回:
            float: 平均分
        """
        subject_scores = self.get_subject_scores(subject)
        if not subject_scores:
            return 0
        
        total = sum(score["score"] for score in subject_scores)
        return total / len(subject_scores)
    
    def get_top_students(self):
        """获取各科第一名学生"""
        subjects = set(score["subject"] for score in self.scores)
        top_students = {}
        
        for subject in subjects:
            subject_scores = self.get_subject_scores(subject)
            if subject_scores:
                # 按分数降序排列
                subject_scores.sort(key=lambda x: x["score"], reverse=True)
                top_students[subject] = subject_scores[0]
        
        return top_students
    
    def generate_report(self):
        """生成成绩报告"""
        print(f"\n=== 成绩分析报告 ===")
        
        # 按学生统计
        print("\n1. 学生成绩统计:")
        students = set(score["name"] for score in self.scores)
        for student in students:
            average = self.calculate_student_average(student)
            print(f"  {student}: 平均分 {average:.1f}")
        
        # 按科目统计
        print("\n2. 科目成绩统计:")
        subjects = set(score["subject"] for score in self.scores)
        for subject in subjects:
            average = self.calculate_subject_average(subject)
            print(f"  {subject}: 平均分 {average:.1f}")
        
        # 各科第一名
        print("\n3. 各科第一名:")
        top_students = self.get_top_students()
        for subject, score_info in top_students.items():
            print(f"  {subject}: {score_info['name']} ({score_info['score']}分)")

# 使用成绩分析器
print("\n创建成绩分析器:")
analyzer = ScoreAnalyzer("student_scores.txt")

# 生成成绩报告
analyzer.generate_report()

# 查询特定学生成绩
print("\n=== 查询张三的成绩 ===")
zhang_san_scores = analyzer.get_student_scores("张三")
for score in zhang_san_scores:
    print(f"  {score['subject']}: {score['score']}分")

# 查询特定科目成绩
print("\n=== 查询数学成绩 ===")
math_scores = analyzer.get_subject_scores("数学")
for score in math_scores:
    print(f"  {score['name']}: {score['score']}分")
```

#### 案例2：日志文件分析器
```python
# 日志文件分析器
print("\n===日志文件分析器===")

import datetime
import random
from collections import defaultdict

# 创建示例日志文件
def create_sample_logs():
    """创建示例日志数据"""
    log_levels = ["INFO", "WARNING", "ERROR"]
    messages = [
        "用户登录成功",
        "数据保存完成",
        "发送邮件成功",
        "文件上传完成",
        "数据库连接成功",
        "内存使用过高",
        "磁盘空间不足",
        "网络连接超时",
        "数据库查询失败",
        "权限验证失败"
    ]
    
    try:
        with open("app.log", "w", encoding="utf-8") as file:
            # 生成100条日志记录
            start_time = datetime.datetime.now() - datetime.timedelta(hours=24)
            
            for i in range(100):
                # 随机生成时间（在过去24小时内）
                log_time = start_time + datetime.timedelta(
                    minutes=random.randint(0, 24*60)
                )
                
                # 随机选择日志级别和消息
                level = random.choice(log_levels)
                message = random.choice(messages)
                
                # 写入日志记录
                log_entry = f"[{log_time.strftime('%Y-%m-%d %H:%M:%S')}] {level}: {message}\n"
                file.write(log_entry)
        
        print("示例日志数据已创建")
        
    except Exception as e:
        print(f"创建示例日志失败: {e}")

# 创建示例日志
create_sample_logs()

class LogAnalyzer:
    """日志分析器"""
    
    def __init__(self, log_file="app.log"):
        """
        初始化日志分析器
        
        参数:
            log_file (str): 日志文件名
        """
        self.log_file = log_file
        self.logs = []
        self.load_logs()
    
    def load_logs(self):
        """加载日志数据"""
        try:
            with open(self.log_file, "r", encoding="utf-8") as file:
                # 方法2: 使用逐行读取（适合大文件）
                line_number = 0
                for line in file:
                    line_number += 1
                    line = line.strip()
                    if line:
                        try:
                            # 解析日志格式: [时间] 级别: 消息
                            parts = line.split(" ", 3)  # 最多分割成4部分
                            if len(parts) >= 4 and parts[0].startswith("[") and parts[2].endswith(":"):
                                timestamp_str = parts[0][1:-1]  # 去除方括号
                                level = parts[1][:-1]  # 去除冒号
                                message = parts[3]
                                
                                # 解析时间戳
                                timestamp = datetime.datetime.strptime(
                                    timestamp_str, 
                                    "%Y-%m-%d %H:%M:%S"
                                )
                                
                                self.logs.append({
                                    "timestamp": timestamp,
                                    "level": level,
                                    "message": message,
                                    "line_number": line_number
                                })
                            else:
                                print(f"跳过格式不正确的日志行 {line_number}: {line}")
                        except (ValueError, IndexError) as e:
                            print(f"解析日志行 {line_number} 失败: {e}")
            
            print(f"成功加载 {len(self.logs)} 条日志记录")
            
        except FileNotFoundError:
            print(f"日志文件 {self.log_file} 不存在")
        except Exception as e:
            print(f"加载日志数据失败: {e}")
    
    def filter_logs(self, level=None, keyword=None, hours=None):
        """
        过滤日志记录
        
        参数:
            level (str): 日志级别过滤
            keyword (str): 关键词过滤
            hours (int): 时间范围过滤（最近几小时）
            
        返回:
            list: 过滤后的日志记录
        """
        filtered_logs = self.logs.copy()
        
        # 按级别过滤
        if level:
            filtered_logs = [log for log in filtered_logs if log["level"] == level]
        
        # 按关键词过滤
        if keyword:
            filtered_logs = [log for log in filtered_logs if keyword in log["message"]]
        
        # 按时间范围过滤
        if hours:
            time_threshold = datetime.datetime.now() - datetime.timedelta(hours=hours)
            filtered_logs = [log for log in filtered_logs if log["timestamp"] >= time_threshold]
        
        return filtered_logs
    
    def get_log_statistics(self):
        """获取日志统计信息"""
        if not self.logs:
            return {}
        
        # 统计各级别日志数量
        level_counts = defaultdict(int)
        for log in self.logs:
            level_counts[log["level"]] += 1
        
        # 统计错误类型
        error_messages = defaultdict(int)
        for log in self.logs:
            if log["level"] in ["ERROR", "WARNING"]:
                error_messages[log["message"]] += 1
        
        # 时间分布统计
        hour_counts = defaultdict(int)
        for log in self.logs:
            hour = log["timestamp"].hour
            hour_counts[hour] += 1
        
        return {
            "total_logs": len(self.logs),
            "level_counts": dict(level_counts),
            "top_errors": dict(sorted(error_messages.items(), key=lambda x: x[1], reverse=True)[:5]),
            "hourly_distribution": dict(hour_counts)
        }
    
    def show_recent_logs(self, count=10):
        """
        显示最近的日志记录
        
        参数:
            count (int): 显示记录数
        """
        if not self.logs:
            print("没有日志记录")
            return
        
        # 按时间排序
        sorted_logs = sorted(self.logs, key=lambda x: x["timestamp"], reverse=True)
        
        print(f"\n=== 最近 {min(count, len(sorted_logs))} 条日志记录 ===")
        for log in sorted_logs[:count]:
            print(f"[{log['timestamp'].strftime('%Y-%m-%d %H:%M:%S')}] {log['level']}: {log['message']}")
    
    def generate_report(self):
        """生成日志分析报告"""
        stats = self.get_log_statistics()
        if not stats:
            print("没有日志数据可分析")
            return
        
        print(f"\n=== 日志分析报告 ===")
        print(f"总日志数: {stats['total_logs']}")
        
        print(f"\n各级别日志数量:")
        for level, count in stats['level_counts'].items():
            percentage = (count / stats['total_logs']) * 100
            print(f"  {level}: {count} ({percentage:.1f}%)")
        
        if stats['top_errors']:
            print(f"\n最常见的错误/警告:")
            for message, count in list(stats['top_errors'].items())[:3]:
                print(f"  {message}: {count} 次")
        
        print(f"\n小时分布（最近24小时）:")
        for hour in range(24):
            count = stats['hourly_distribution'].get(hour, 0)
            bar = "█" * (count // 2)  # 简单的条形图
            print(f"  {hour:02d}:00 - {hour:02d}:59 |{bar} {count}")

# 使用日志分析器
print("\n创建日志分析器:")
log_analyzer = LogAnalyzer("app.log")

# 显示最近日志
log_analyzer.show_recent_logs(5)

# 过滤错误日志
print("\n=== 过滤错误日志 ===")
error_logs = log_analyzer.filter_logs(level="ERROR")
print(f"找到 {len(error_logs)} 条错误日志")

# 过滤包含特定关键词的日志
print("\n=== 过滤包含'数据库'的日志 ===")
db_logs = log_analyzer.filter_logs(keyword="数据库")
print(f"找到 {len(db_logs)} 条相关日志")
for log in db_logs[:3]:  # 只显示前3条
    print(f"  [{log['timestamp'].strftime('%Y-%m-%d %H:%M:%S')}] {log['level']}: {log['message']}")

# 生成分析报告
log_analyzer.generate_report()
```

### 代码说明

**案例1代码解释**：
1. `lines = file.readlines()`：一次性读取所有行到内存（适合小文件）
2. `for line in file:`：逐行读取文件（适合大文件，节省内存）
3. `line.split(",")`：按逗号分割字符串获取各字段
4. `file.write(sample_data)`：一次性写入所有数据

如果成绩文件非常大（比如有几万条记录），使用`readlines()`会占用大量内存，这时应该使用逐行读取的方式。

**案例2代码解释**：
1. `file.write(log_entry)`：逐行写入日志记录
2. `line.split(" ", 3)`：按空格分割，最多分成4部分
3. `datetime.datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")`：解析时间字符串
4. `defaultdict(int)`：使用默认字典统计数量

如果忘记在写入日志时添加`\n`换行符，所有日志记录会出现在同一行，难以阅读。

## 3. with语句和上下文管理器

### 知识点解析

**概念定义**：with语句就像一个智能的文件管理员，当我们需要操作文件时，它会帮我们打开文件，操作完成后自动帮我们关闭文件，即使在操作过程中出现意外情况也会确保文件被正确关闭。

**核心规则**：
1. 使用`with open(...) as file:`语法自动管理文件
2. 进入with块时自动调用`__enter__`方法
3. 退出with块时自动调用`__exit__`方法
4. 即使发生异常，也会确保资源被正确清理

**常见易错点**：
1. 忘记使用with语句，手动管理文件开关
2. 在with块外部访问文件对象
3. 在`__exit__`方法中错误地抑制异常
4. 不理解上下文管理器的工作原理

### 实战案例

#### 案例1：安全的文件备份工具
```python
# 安全的文件备份工具
print("===安全的文件备份工具===")

import shutil
import os
from pathlib import Path
from contextlib import contextmanager
import datetime

# 自定义上下文管理器
@contextmanager
def safe_file_backup(filename):
    """
    安全文件备份上下文管理器
    在修改文件前自动创建备份，如果操作失败则恢复备份
    
    参数:
        filename (str): 要操作的文件名
    """
    backup_filename = None
    file_handle = None
    
    try:
        print(f"准备操作文件: {filename}")
        
        # 如果原文件存在，创建备份
        if os.path.exists(filename):
            # 生成备份文件名
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            name, ext = os.path.splitext(filename)
            backup_filename = f"{name}_{timestamp}{ext}"
            
            # 创建备份
            shutil.copy2(filename, backup_filename)
            print(f"已创建备份: {backup_filename}")
        
        # 打开原文件进行操作
        file_handle = open(filename, "w", encoding="utf-8")
        print(f"已打开文件: {filename}")
        
        # yield语句将文件句柄传递给with块
        yield file_handle
        
        # 如果执行到这里，说明操作成功
        print("文件操作成功完成")
        
    except Exception as e:
        # 如果发生异常，恢复备份
        print(f"文件操作失败: {e}")
        if backup_filename and os.path.exists(backup_filename):
            shutil.copy2(backup_filename, filename)
            print(f"已从备份恢复文件: {filename}")
        raise  # 重新抛出异常
    else:
        # 操作成功，可以删除备份
        if backup_filename and os.path.exists(backup_filename):
            os.remove(backup_filename)
            print(f"操作成功，已删除备份: {backup_filename}")
    finally:
        # 确保文件被关闭
        if file_handle and not file_handle.closed:
            file_handle.close()
            print("文件已关闭")

# 文件操作类
class FileManager:
    """文件管理器"""
    
    @staticmethod
    def create_document(filename, title, content):
        """
        创建文档
        
        参数:
            filename (str): 文件名
            title (str): 文档标题
            content (str): 文档内容
        """
        document = f"""====================
{title}
====================

{content}

文档创建时间: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
"""
        
        # 使用自定义上下文管理器安全地创建文件
        with safe_file_backup(filename) as file:
            file.write(document)
            # 模拟可能的处理时间
            import time
            time.sleep(0.1)
        
        print(f"文档已创建: {filename}")
    
    @staticmethod
    def append_to_document(filename, new_content):
        """
        向文档追加内容
        
        参数:
            filename (str): 文件名
            new_content (str): 新内容
        """
        # 先读取原内容
        try:
            with open(filename, "r", encoding="utf-8") as file:
                original_content = file.read()
        except FileNotFoundError:
            original_content = ""
        
        # 准备新内容
        updated_content = original_content + f"\n--- 追加内容 ---\n{new_content}\n"
        
        # 使用自定义上下文管理器安全地更新文件
        with safe_file_backup(filename) as file:
            file.write(updated_content)
        
        print(f"内容已追加到: {filename}")

# 使用文件备份工具
print("创建文档:")
try:
    FileManager.create_document(
        "my_document.txt",
        "我的第一份文档",
        "这是文档的主要内容。\n包含多行文本。\n用于演示文件操作。"
    )
    
    # 显示创建的文档
    print("\n文档内容:")
    with open("my_document.txt", "r", encoding="utf-8") as file:
        print(file.read())
        
except Exception as e:
    print(f"创建文档失败: {e}")

print("\n追加内容:")
try:
    FileManager.append_to_document(
        "my_document.txt",
        "这是后来追加的内容。\n增加了更多详细信息。"
    )
    
    # 显示更新后的文档
    print("\n更新后的文档内容:")
    with open("my_document.txt", "r", encoding="utf-8") as file:
        print(file.read())
        
except Exception as e:
    print(f"追加内容失败: {e}")

# 演示异常恢复
print("\n===演示异常恢复===")
try:
    with safe_file_backup("test_file.txt") as file:
        file.write("这是测试内容\n")
        # 模拟操作失败
        raise ValueError("模拟操作失败")
except ValueError as e:
    print(f"捕获到异常: {e}")
    
# 检查文件状态
if os.path.exists("test_file.txt"):
    print("原文件仍然存在")
    with open("test_file.txt", "r", encoding="utf-8") as file:
        print(f"文件内容: {file.read()}")
else:
    print("文件已被删除")
```

#### 案例2：多文件操作管理器
```python
# 多文件操作管理器
print("\n===多文件操作管理器===")

from contextlib import ExitStack
import csv
import json

class MultiFileManager:
    """多文件操作管理器"""
    
    def __init__(self):
        self.exit_stack = ExitStack()
    
    def __enter__(self):
        """进入上下文"""
        self.exit_stack.__enter__()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """退出上下文"""
        return self.exit_stack.__exit__(exc_type, exc_val, exc_tb)
    
    def open_file(self, filename, mode="r", encoding="utf-8"):
        """
        打开文件并添加到管理器
        
        参数:
            filename (str): 文件名
            mode (str): 打开模式
            encoding (str): 编码格式
            
        返回:
            文件对象
        """
        file = open(filename, mode, encoding=encoding)
        # 使用exit_stack管理文件，确保正确关闭
        return self.exit_stack.enter_context(file)
    
    def process_data_files(self, input_file, output_file, log_file):
        """
        处理数据文件
        
        参数:
            input_file (str): 输入文件名
            output_file (str): 输出文件名
            log_file (str): 日志文件名
        """
        try:
            # 同时打开多个文件
            input_f = self.open_file(input_file, "r")
            output_f = self.open_file(output_file, "w")
            log_f = self.open_file(log_file, "a")
            
            # 记录开始处理
            log_f.write(f"[{datetime.datetime.now()}] 开始处理 {input_file}\n")
            
            # 读取输入数据
            data = input_f.read()
            print(f"读取到 {len(data)} 个字符")
            
            # 处理数据（转换为大写）
            processed_data = data.upper()
            
            # 写入输出文件
            output_f.write(processed_data)
            
            # 记录完成处理
            log_f.write(f"[{datetime.datetime.now()}] 处理完成，输出到 {output_file}\n")
            
            print(f"数据已处理并保存到 {output_file}")
            
        except Exception as e:
            # 记录错误
            if 'log_f' in locals():
                log_f.write(f"[{datetime.datetime.now()}] 处理失败: {e}\n")
            raise

# 创建示例输入文件
def create_sample_input():
    """创建示例输入文件"""
    sample_text = """hello world
this is a sample text file
used for demonstrating multi-file operations
it contains multiple lines of text
for processing and transformation"""
    
    with open("input.txt", "w", encoding="utf-8") as file:
        file.write(sample_text)
    print("示例输入文件已创建")

# 创建示例输入文件
create_sample_input()

# 使用多文件管理器
print("使用多文件管理器:")
try:
    with MultiFileManager() as manager:
        manager.process_data_files("input.txt", "output.txt", "processing.log")
        
        # 验证结果
        print("\n处理结果:")
        with open("output.txt", "r", encoding="utf-8") as file:
            print(file.read())
            
        print("\n日志内容:")
        with open("processing.log", "r", encoding="utf-8") as file:
            print(file.read())
            
except Exception as e:
    print(f"处理失败: {e}")

# 演示多个文件的原子操作
print("\n===演示原子操作===")

def atomic_file_operations():
    """演示原子文件操作"""
    files_to_create = ["file1.txt", "file2.txt", "file3.txt"]
    
    try:
        with ExitStack() as stack:
            # 同时打开所有文件
            files = []
            for filename in files_to_create:
                file = stack.enter_context(open(filename, "w", encoding="utf-8"))
                files.append(file)
            
            # 向所有文件写入内容
            for i, file in enumerate(files):
                file.write(f"这是 {files_to_create[i]} 的内容\n")
                print(f"已写入 {files_to_create[i]}")
            
            # 模拟在操作中途发生错误
            # raise IOError("模拟磁盘写入错误")
            
            print("所有文件操作成功完成")
            
    except Exception as e:
        print(f"操作失败: {e}")
        print("由于使用了ExitStack，所有文件都会被正确关闭")

# 执行原子操作演示
atomic_file_operations()

# 检查文件是否都已正确创建和关闭
print("\n检查创建的文件:")
for filename in ["file1.txt", "file2.txt", "file3.txt"]:
    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as file:
            print(f"{filename}: {file.read().strip()}")
        # 清理文件
        os.remove(filename)
```

### 代码说明

**案例1代码解释**：
1. `@contextmanager`：将函数转换为上下文管理器
2. `yield file_handle`：将文件句柄传递给with块
3. `shutil.copy2(filename, backup_filename)`：创建文件备份
4. `try...except...else...finally`：确保正确的异常处理和资源清理

如果在`safe_file_backup`上下文管理器中忘记关闭文件，可能导致文件锁未释放，影响其他程序访问该文件。

**案例2代码解释**：
1. `ExitStack()`：管理多个上下文管理器
2. `self.exit_stack.enter_context(file)`：将文件添加到退出栈
3. `with ExitStack() as stack:`：自动管理多个资源的清理
4. `stack.enter_context(open(filename, "w", encoding="utf-8"))`：安全地打开文件

如果手动管理多个文件的开关，需要在多个地方处理异常和关闭操作，代码复杂且容易出错。

## 4. 文件和目录操作

### 知识点解析

**概念定义**：文件和目录操作就像管理现实中的文件夹和文件一样，我们可以创建新的文件夹（目录），查看文件夹里有什么文件，移动文件到不同文件夹，或者删除不需要的文件和文件夹。

**核心规则**：
1. 使用`os`模块进行基本文件和目录操作
2. 使用`pathlib`模块进行现代化的路径操作
3. 操作前检查文件或目录是否存在
4. 注意区分文件和目录的不同操作方法

**常见易错点**：
1. 删除重要文件或目录前没有确认
2. 路径分隔符在不同系统上不一致
3. 没有权限访问某些目录或文件
4. 递归操作时意外删除了重要文件

### 实战案例

#### 案例1：个人文档管理系统
```python
# 个人文档管理系统
print("===个人文档管理系统===")

import os
from pathlib import Path
import shutil
from datetime import datetime

class DocumentManager:
    """个人文档管理系统"""
    
    def __init__(self, base_directory="my_documents"):
        """
        初始化文档管理系统
        
        参数:
            base_directory (str): 基础文档目录
        """
        self.base_directory = Path(base_directory)
        self.create_directory(self.base_directory)
        print(f"文档管理系统已初始化: {self.base_directory}")
    
    def create_directory(self, directory_path):
        """
        创建目录
        
        参数:
            directory_path (Path): 目录路径
        """
        try:
            directory_path.mkdir(parents=True, exist_ok=True)
            print(f"目录已创建或已存在: {directory_path}")
        except Exception as e:
            print(f"创建目录失败 {directory_path}: {e}")
    
    def create_document(self, category, filename, content=""):
        """
        创建文档
        
        参数:
            category (str): 文档分类
            filename (str): 文件名
            content (str): 文档内容
        """
        # 创建分类目录
        category_dir = self.base_directory / category
        self.create_directory(category_dir)
        
        # 创建文档路径
        document_path = category_dir / filename
        
        try:
            # 写入文档内容
            with open(document_path, "w", encoding="utf-8") as file:
                file.write(content)
            print(f"文档已创建: {document_path}")
            return document_path
        except Exception as e:
            print(f"创建文档失败 {document_path}: {e}")
            return None
    
    def list_documents(self, category=None):
        """
        列出文档
        
        参数:
            category (str): 文档分类，None表示所有分类
        """
        if category:
            category_dir = self.base_directory / category
            if not category_dir.exists():
                print(f"分类 {category} 不存在")
                return
            
            print(f"\n=== {category} 分类下的文档 ===")
            for item in category_dir.iterdir():
                if item.is_file():
                    stat = item.stat()
                    size = stat.st_size
                    modified = datetime.fromtimestamp(stat.st_mtime)
                    print(f"  {item.name} ({size} 字节, 修改时间: {modified.strftime('%Y-%m-%d %H:%M')})")
        else:
            print(f"\n=== 所有文档分类 ===")
            for item in self.base_directory.iterdir():
                if item.is_dir():
                    file_count = len([f for f in item.iterdir() if f.is_file()])
                    print(f"  {item.name} ({file_count} 个文件)")
    
    def search_documents(self, keyword):
        """
        搜索文档
        
        参数:
            keyword (str): 搜索关键词
        """
        print(f"\n=== 搜索包含 '{keyword}' 的文档 ===")
        found_count = 0
        
        # 遍历所有文档
        for root, dirs, files in os.walk(self.base_directory):
            for file in files:
                if file.endswith(('.txt', '.md', '.py')):  # 只搜索特定类型文件
                    file_path = Path(root) / file
                    try:
                        with open(file_path, "r", encoding="utf-8") as f:
                            content = f.read()
                            if keyword.lower() in content.lower():
                                print(f"  找到: {file_path}")
                                found_count += 1
                    except Exception as e:
                        print(f"  无法读取 {file_path}: {e}")
        
        print(f"总共找到 {found_count} 个匹配的文档")
    
    def move_document(self, source_category, filename, target_category):
        """
        移动文档
        
        参数:
            source_category (str): 源分类
            filename (str): 文件名
            target_category (str): 目标分类
        """
        source_path = self.base_directory / source_category / filename
        target_path = self.base_directory / target_category / filename
        
        if not source_path.exists():
            print(f"源文件不存在: {source_path}")
            return False
        
        # 创建目标目录
        self.create_directory(target_path.parent)
        
        try:
            # 移动文件
            shutil.move(str(source_path), str(target_path))
            print(f"文档已移动: {source_path} -> {target_path}")
            return True
        except Exception as e:
            print(f"移动文档失败: {e}")
            return False
    
    def delete_document(self, category, filename):
        """
        删除文档
        
        参数:
            category (str): 文档分类
            filename (str): 文件名
        """
        document_path = self.base_directory / category / filename
        
        if not document_path.exists():
            print(f"文件不存在: {document_path}")
            return False
        
        try:
            document_path.unlink()  # 删除文件
            print(f"文档已删除: {document_path}")
            return True
        except Exception as e:
            print(f"删除文档失败: {e}")
            return False
    
    def get_storage_info(self):
        """获取存储信息"""
        total_files = 0
        total_size = 0
        categories = {}
        
        for item in self.base_directory.iterdir():
            if item.is_dir():
                file_count = 0
                category_size = 0
                
                for file in item.iterdir():
                    if file.is_file():
                        file_count += 1
                        try:
                            category_size += file.stat().st_size
                        except:
                            pass
                
                categories[item.name] = {
                    "files": file_count,
                    "size": category_size
                }
                total_files += file_count
                total_size += category_size
        
        print(f"\n=== 存储信息 ===")
        print(f"总文件数: {total_files}")
        print(f"总大小: {total_size} 字节 ({total_size / 1024:.1f} KB)")
        print(f"分类详情:")
        for category, info in categories.items():
            print(f"  {category}: {info['files']} 个文件, {info['size']} 字节")

# 使用文档管理系统
print("创建文档管理系统:")
doc_manager = DocumentManager("personal_docs")

# 创建示例文档
print("\n创建示例文档:")
doc1 = doc_manager.create_document(
    "工作", 
    "项目计划.txt", 
    "项目名称: 文档管理系统\n开始时间: 2023-01-01\n结束时间: 2023-12-31\n负责人: 张三"
)

doc2 = doc_manager.create_document(
    "学习", 
    "Python笔记.txt", 
    "Python基础知识\n1. 变量和数据类型\n2. 控制流\n3. 函数\n4. 文件操作"
)

doc3 = doc_manager.create_document(
    "生活", 
    "购物清单.txt", 
    "购物清单:\n- 苹果\n- 牛奶\n- 面包\n- 鸡蛋"
)

# 列出所有文档
doc_manager.list_documents()

# 列出特定分类的文档
doc_manager.list_documents("工作")

# 搜索文档
doc_manager.search_documents("Python")

# 移动文档
doc_manager.move_document("生活", "购物清单.txt", "工作")

# 再次列出文档查看移动结果
print("\n移动文档后:")
doc_manager.list_documents()

# 获取存储信息
doc_manager.get_storage_info()

# 删除文档
doc_manager.delete_document("学习", "Python笔记.txt")

# 再次获取存储信息
doc_manager.get_storage_info()
```

#### 案例2：文件同步工具
```python
# 文件同步工具
print("\n===文件同步工具===")

import hashlib
import shutil
from pathlib import Path

class FileSyncer:
    """文件同步工具"""
    
    def __init__(self):
        self.sync_log = []
    
    def calculate_file_hash(self, file_path):
        """
        计算文件的MD5哈希值
        
        参数:
            file_path (Path): 文件路径
            
        返回:
            str: 文件的MD5哈希值
        """
        hash_md5 = hashlib.md5()
        try:
            with open(file_path, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_md5.update(chunk)
            return hash_md5.hexdigest()
        except Exception as e:
            print(f"计算文件哈希失败 {file_path}: {e}")
            return None
    
    def compare_directories(self, source_dir, target_dir):
        """
        比较两个目录的文件
        
        参数:
            source_dir (str): 源目录
            target_dir (str): 目标目录
            
        返回:
            dict: 比较结果
        """
        source_path = Path(source_dir)
        target_path = Path(target_dir)
        
        if not source_path.exists():
            print(f"源目录不存在: {source_path}")
            return None
        
        # 确保目标目录存在
        target_path.mkdir(parents=True, exist_ok=True)
        
        # 收集源目录文件信息
        source_files = {}
        for file_path in source_path.rglob("*"):
            if file_path.is_file():
                relative_path = file_path.relative_to(source_path)
                file_hash = self.calculate_file_hash(file_path)
                if file_hash:
                    source_files[str(relative_path)] = {
                        "path": file_path,
                        "hash": file_hash,
                        "size": file_path.stat().st_size
                    }
        
        # 收集目标目录文件信息
        target_files = {}
        for file_path in target_path.rglob("*"):
            if file_path.is_file():
                relative_path = file_path.relative_to(target_path)
                file_hash = self.calculate_file_hash(file_path)
                if file_hash:
                    target_files[str(relative_path)] = {
                        "path": file_path,
                        "hash": file_hash,
                        "size": file_path.stat().st_size
                    }
        
        # 比较文件
        to_copy = []      # 需要复制的文件
        to_update = []    # 需要更新的文件
        to_delete = []    # 需要删除的文件
        
        # 检查源目录中的文件
        for rel_path, source_info in source_files.items():
            if rel_path not in target_files:
                # 文件在源目录但不在目标目录，需要复制
                to_copy.append((source_info["path"], rel_path))
            else:
                # 文件在两个目录都存在，比较哈希值
                target_info = target_files[rel_path]
                if source_info["hash"] != target_info["hash"]:
                    # 文件内容不同，需要更新
                    to_update.append((source_info["path"], rel_path))
        
        # 检查目标目录中多余的文件
        for rel_path, target_info in target_files.items():
            if rel_path not in source_files:
                # 文件在目标目录但不在源目录，需要删除
                to_delete.append((target_info["path"], rel_path))
        
        return {
            "to_copy": to_copy,
            "to_update": to_update,
            "to_delete": to_delete,
            "source_files": source_files,
            "target_files": target_files
        }
    
    def sync_directories(self, source_dir, target_dir, delete_extra=False):
        """
        同步两个目录
        
        参数:
            source_dir (str): 源目录
            target_dir (str): 目标目录
            delete_extra (bool): 是否删除目标目录中多余的文件
        """
        print(f"开始同步: {source_dir} -> {target_dir}")
        
        comparison = self.compare_directories(source_dir, target_dir)
        if not comparison:
            print("目录比较失败")
            return
        
        source_path = Path(source_dir)
        target_path = Path(target_dir)
        
        # 复制新文件
        for source_file, rel_path in comparison["to_copy"]:
            target_file = target_path / rel_path
            # 确保目标目录存在
            target_file.parent.mkdir(parents=True, exist_ok=True)
            
            try:
                shutil.copy2(str(source_file), str(target_file))
                print(f"  复制: {rel_path}")
                self.sync_log.append(f"复制: {rel_path}")
            except Exception as e:
                print(f"  复制失败 {rel_path}: {e}")
        
        # 更新已修改的文件
        for source_file, rel_path in comparison["to_update"]:
            target_file = target_path / rel_path
            try:
                shutil.copy2(str(source_file), str(target_file))
                print(f"  更新: {rel_path}")
                self.sync_log.append(f"更新: {rel_path}")
            except Exception as e:
                print(f"  更新失败 {rel_path}: {e}")
        
        # 删除多余的文件
        if delete_extra:
            for target_file, rel_path in comparison["to_delete"]:
                try:
                    target_file.unlink()
                    print(f"  删除: {rel_path}")
                    self.sync_log.append(f"删除: {rel_path}")
                except Exception as e:
                    print(f"  删除失败 {rel_path}: {e}")
        
        print("同步完成")
    
    def show_sync_log(self):
        """显示同步日志"""
        if not self.sync_log:
            print("暂无同步记录")
            return
        
        print(f"\n=== 同步日志 ({len(self.sync_log)} 条记录) ===")
        for entry in self.sync_log:
            print(f"  {entry}")

# 创建测试目录和文件
def create_test_directories():
    """创建测试目录和文件"""
    # 创建源目录结构
    source_dirs = ["source/docs", "source/images", "source/code"]
    for dir_path in source_dirs:
        Path(dir_path).mkdir(parents=True, exist_ok=True)
    
    # 创建源文件
    test_files = {
        "source/readme.txt": "这是 readme 文件",
        "source/docs/guide.md": "# 使用指南\n详细说明如何使用本系统",
        "source/docs/api.md": "# API 文档\n接口说明文档",
        "source/images/logo.png": "fake png content",  # 模拟图片文件
        "source/code/script.py": "print('Hello, World!')",
    }
    
    for file_path, content in test_files.items():
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
    
    print("测试源目录和文件已创建")
    
    # 创建目标目录（初始为空）
    Path("target").mkdir(exist_ok=True)
    print("测试目标目录已创建")

# 创建测试环境
create_test_directories()

# 使用文件同步工具
print("\n使用文件同步工具:")
syncer = FileSyncer()

# 首次同步
syncer.sync_directories("source", "target")

# 显示同步后的目标目录结构
print("\n同步后的目标目录:")
for root, dirs, files in os.walk("target"):
    level = root.replace("target", "").count(os.sep)
    indent = " " * 2 * level
    print(f"{indent}{os.path.basename(root)}/")
    subindent = " " * 2 * (level + 1)
    for file in files:
        print(f"{subindent}{file}")

# 修改源文件
print("\n修改源文件:")
with open("source/docs/guide.md", "a", encoding="utf-8") as f:
    f.write("\n\n## 新增章节\n这是新增的内容")

# 添加新文件
print("添加新文件:")
with open("source/new_file.txt", "w", encoding="utf-8") as f:
    f.write("这是新增的文件")

# 再次同步
syncer.sync_directories("source", "target")

# 显示同步日志
syncer.show_sync_log()

# 演示删除多余文件
print("\n=== 演示删除多余文件 ===")

# 在目标目录添加一个额外文件
extra_file = Path("target/extra.txt")
extra_file.write_text("这是目标目录的额外文件")

print("在目标目录添加了额外文件")
print("同步时不删除额外文件:")
syncer.sync_directories("source", "target", delete_extra=False)

print("\n同步时删除额外文件:")
syncer.sync_directories("source", "target", delete_extra=True)

# 检查额外文件是否被删除
if not extra_file.exists():
    print("额外文件已成功删除")
else:
    print("额外文件仍然存在")
```

### 代码说明

**案例1代码解释**：
1. `Path(base_directory)`：使用pathlib创建路径对象
2. `directory_path.mkdir(parents=True, exist_ok=True)`：创建目录，自动创建父目录
3. `file_path.unlink()`：删除文件
4. `shutil.move(str(source_path), str(target_path))`：移动文件

如果在创建目录时忘记使用`parents=True`，当父目录不存在时会报错。

**案例2代码解释**：
1. `hashlib.md5()`：创建MD5哈希对象
2. `source_path.rglob("*")`：递归查找所有文件
3. `file_path.relative_to(source_path)`：获取相对路径
4. `shutil.copy2(str(source_file), str(target_file))`：复制文件并保持元数据

如果在计算大文件哈希时一次性读取整个文件，会占用大量内存，因此使用分块读取的方式。

## 5. 实际应用场景和最佳实践

### 知识点解析

**概念定义**：实际应用场景就是把学到的文件操作知识用到实际工作中，比如制作一个可以管理个人文件的小工具，或者处理大量数据的脚本。最佳实践就是经验丰富的程序员总结出来的做事情最有效、最安全的方法。

**核心规则**：
1. 始终使用with语句管理文件资源
2. 明确指定文件编码格式
3. 操作前检查文件是否存在
4. 处理可能的异常情况
5. 对于大文件使用流式处理

**常见易错点**：
1. 在生产环境中忘记处理异常
2. 不考虑文件权限和磁盘空间
3. 没有备份重要文件就直接修改
4. 忽视性能问题，处理大文件时内存不足
5. 跨平台时没有考虑路径分隔符差异

### 实战案例

#### 案例1：个人密码管理器
```python
# 个人密码管理器
print("===个人密码管理器===")

import json
import hashlib
import os
from pathlib import Path
import getpass

class PasswordManager:
    """个人密码管理器"""
    
    def __init__(self, data_file="passwords.json"):
        """
        初始化密码管理器
        
        参数:
            data_file (str): 密码数据文件
        """
        self.data_file = Path(data_file)
        self.passwords = {}
        self.master_password_hash = None
        self.load_data()
    
    def _hash_password(self, password):
        """
        哈希密码
        
        参数:
            password (str): 原始密码
            
        返回:
            str: 哈希后的密码
        """
        return hashlib.sha256(password.encode()).hexdigest()
    
    def set_master_password(self):
        """设置主密码"""
        if self.master_password_hash:
            print("主密码已设置")
            return
        
        while True:
            password = getpass.getpass("请设置主密码: ")
            if len(password) < 6:
                print("密码长度至少6位")
                continue
            
            confirm = getpass.getpass("请确认主密码: ")
            if password != confirm:
                print("两次输入的密码不一致")
                continue
            
            self.master_password_hash = self._hash_password(password)
            self.save_data()
            print("主密码设置成功")
            break
    
    def verify_master_password(self):
        """
        验证主密码
        
        返回:
            bool: 验证是否成功
        """
        if not self.master_password_hash:
            print("请先设置主密码")
            return False
        
        password = getpass.getpass("请输入主密码: ")
        if self._hash_password(password) == self.master_password_hash:
            return True
        else:
            print("密码错误")
            return False
    
    def add_password(self, service, username, password):
        """
        添加密码
        
        参数:
            service (str): 服务名称
            username (str): 用户名
            password (str): 密码
        """
        if not self.verify_master_password():
            return
        
        # 加密存储密码（简单示例，实际应用中应使用更安全的方法）
        encrypted_password = self._hash_password(password)[:16]  # 简单截取
        
        self.passwords[service] = {
            "username": username,
            "password": encrypted_password,
            "created_at": __import__('datetime').datetime.now().isoformat()
        }
        
        self.save_data()
        print(f"密码已添加: {service}")
    
    def get_password(self, service):
        """
        获取密码
        
        参数:
            service (str): 服务名称
            
        返回:
            dict: 密码信息
        """
        if not self.verify_master_password():
            return None
        
        return self.passwords.get(service)
    
    def list_services(self):
        """列出所有服务"""
        if not self.verify_master_password():
            return
        
        if not self.passwords:
            print("暂无保存的密码")
            return
        
        print("\n=== 保存的密码服务 ===")
        for service in self.passwords:
            print(f"  - {service}")
    
    def delete_password(self, service):
        """
        删除密码
        
        参数:
            service (str): 服务名称
        """
        if not self.verify_master_password():
            return
        
        if service in self.passwords:
            del self.passwords[service]
            self.save_data()
            print(f"密码已删除: {service}")
        else:
            print(f"未找到服务: {service}")
    
    def load_data(self):
        """加载数据"""
        try:
            if self.data_file.exists():
                with open(self.data_file, "r", encoding="utf-8") as file:
                    data = json.load(file)
                    self.passwords = data.get("passwords", {})
                    self.master_password_hash = data.get("master_password_hash")
                print("密码数据已加载")
            else:
                print("密码数据文件不存在，将创建新文件")
        except Exception as e:
            print(f"加载数据失败: {e}")
            self.passwords = {}
            self.master_password_hash = None
    
    def save_data(self):
        """保存数据"""
        try:
            data = {
                "passwords": self.passwords,
                "master_password_hash": self.master_password_hash
            }
            
            # 确保目录存在
            self.data_file.parent.mkdir(parents=True, exist_ok=True)
            
            with open(self.data_file, "w", encoding="utf-8") as file:
                json.dump(data, file, ensure_ascii=False, indent=2)
            print("密码数据已保存")
        except Exception as e:
            print(f"保存数据失败: {e}")

# 使用密码管理器
print("创建密码管理器:")
pm = PasswordManager("my_passwords.json")

# 设置主密码
print("\n设置主密码:")
pm.set_master_password()

# 添加密码
print("\n添加密码:")
pm.add_password("gmail", "user@gmail.com", "mygmailpassword")
pm.add_password("github", "github_user", "mygithubpassword")
pm.add_password("bank", "bank_user", "mybankpassword")

# 列出服务
print("\n列出服务:")
pm.list_services()

# 获取密码
print("\n获取密码:")
gmail_info = pm.get_password("gmail")
if gmail_info:
    print(f"Gmail 用户名: {gmail_info['username']}")
    print(f"创建时间: {gmail_info['created_at']}")

# 删除密码
print("\n删除密码:")
pm.delete_password("bank")

# 再次列出服务
print("\n删除后列出服务:")
pm.list_services()

# 演示密码错误的情况
print("\n=== 演示密码错误 ===")
# 创建新的实例来测试
pm_test = PasswordManager("my_passwords.json")
# 尝试错误的主密码
# 这里我们不会实际输入错误密码，只是说明会有验证过程
```

#### 案例2：数据备份和恢复工具
```python
# 数据备份和恢复工具
print("\n===数据备份和恢复工具===")

import zipfile
import os
from pathlib import Path
from datetime import datetime
import shutil

class BackupManager:
    """数据备份和恢复工具"""
    
    def __init__(self, backup_dir="backups"):
        """
        初始化备份管理器
        
        参数:
            backup_dir (str): 备份目录
        """
        self.backup_dir = Path(backup_dir)
        self.backup_dir.mkdir(exist_ok=True)
        print(f"备份管理器已初始化: {self.backup_dir}")
    
    def create_backup(self, source_dir, backup_name=None):
        """
        创建备份
        
        参数:
            source_dir (str): 源目录
            backup_name (str): 备份名称，None表示自动生成
            
        返回:
            str: 备份文件路径
        """
        source_path = Path(source_dir)
        if not source_path.exists():
            print(f"源目录不存在: {source_path}")
            return None
        
        # 生成备份文件名
        if not backup_name:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_name = f"backup_{timestamp}"
        
        backup_file = self.backup_dir / f"{backup_name}.zip"
        
        try:
            print(f"正在创建备份: {backup_file}")
            
            with zipfile.ZipFile(backup_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for root, dirs, files in os.walk(source_path):
                    for file in files:
                        file_path = Path(root) / file
                        # 计算相对路径
                        arcname = file_path.relative_to(source_path.parent)
                        zipf.write(file_path, arcname)
                        print(f"  已添加: {arcname}")
            
            print(f"备份创建成功: {backup_file}")
            return str(backup_file)
            
        except Exception as e:
            print(f"创建备份失败: {e}")
            return None
    
    def restore_backup(self, backup_file, target_dir):
        """
        恢复备份
        
        参数:
            backup_file (str): 备份文件路径
            target_dir (str): 目标目录
        """
        backup_path = Path(backup_file)
        target_path = Path(target_dir)
        
        if not backup_path.exists():
            print(f"备份文件不存在: {backup_path}")
            return False
        
        try:
            print(f"正在恢复备份: {backup_file} -> {target_dir}")
            
            # 确保目标目录存在
            target_path.mkdir(parents=True, exist_ok=True)
            
            with zipfile.ZipFile(backup_path, 'r') as zipf:
                zipf.extractall(target_path)
                print("备份恢复成功")
                return True
                
        except Exception as e:
            print(f"恢复备份失败: {e}")
            return False
    
    def list_backups(self):
        """列出所有备份"""
        backups = list(self.backup_dir.glob("*.zip"))
        if not backups:
            print("暂无备份文件")
            return
        
        print(f"\n=== 备份文件列表 ({len(backups)} 个) ===")
        for backup in sorted(backups, key=lambda x: x.stat().st_mtime, reverse=True):
            stat = backup.stat()
            size = stat.st_size
            modified = datetime.fromtimestamp(stat.st_mtime)
            print(f"  {backup.name} ({size} 字节, {modified.strftime('%Y-%m-%d %H:%M')})")
    
    def delete_backup(self, backup_name):
        """
        删除备份
        
        参数:
            backup_name (str): 备份文件名（不含路径和扩展名）
        """
        backup_file = self.backup_dir / f"{backup_name}.zip"
        if backup_file.exists():
            try:
                backup_file.unlink()
                print(f"备份已删除: {backup_file}")
            except Exception as e:
                print(f"删除备份失败: {e}")
        else:
            print(f"备份文件不存在: {backup_file}")

# 创建测试数据
def create_test_data():
    """创建测试数据"""
    test_dirs = ["test_data/docs", "test_data/images", "test_data/code"]
    for dir_path in test_dirs:
        Path(dir_path).mkdir(parents=True, exist_ok=True)
    
    test_files = {
        "test_data/readme.txt": "这是测试数据的 readme 文件",
        "test_data/docs/guide.md": "# 测试指南\n测试说明文档",
        "test_data/images/test.png": "fake image content",
        "test_data/code/test.py": "print('Hello, Test!')",
    }
    
    for file_path, content in test_files.items():
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
    
    print("测试数据已创建")

# 创建测试数据
create_test_data()

# 使用备份管理器
print("\n使用备份管理器:")
backup_manager = BackupManager("my_backups")

# 创建备份
print("\n创建备份:")
backup1 = backup_manager.create_backup("test_data", "test_backup_1")
backup2 = backup_manager.create_backup("test_data")  # 自动生成名称

# 列出备份
backup_manager.list_backups()

# 恢复备份
print("\n恢复备份:")
# 先删除原始数据
shutil.rmtree("test_data", ignore_errors=True)
print("已删除原始数据")

# 恢复第一个备份
backup_manager.restore_backup(backup1, "restored_data")

# 验证恢复结果
print("\n恢复后的目录结构:")
for root, dirs, files in os.walk("restored_data"):
    level = root.replace("restored_data", "").count(os.sep)
    indent = " " * 2 * level
    print(f"{indent}{os.path.basename(root)}/")
    subindent = " " * 2 * (level + 1)
    for file in files:
        print(f"{subindent}{file}")

# 删除备份
print("\n删除备份:")
backup_manager.delete_backup("test_backup_1")

# 再次列出备份
backup_manager.list_backups()

# 清理测试文件
shutil.rmtree("test_data", ignore_errors=True)
shutil.rmtree("restored_data", ignore_errors=True)
shutil.rmtree("my_backups", ignore_errors=True)

print("\n=== 最佳实践总结 ===")
print("文件操作最佳实践:")
print("1. 始终使用 with 语句管理文件资源")
print("2. 明确指定文件编码格式")
print("3. 操作前检查文件是否存在")
print("4. 处理可能的异常情况")
print("5. 对于大文件使用流式处理")
print("6. 重要文件操作前创建备份")
print("7. 使用 pathlib 进行现代化路径操作")
print("8. 定期清理临时文件和备份")
```

### 代码说明

**案例1代码解释**：
1. `getpass.getpass("请输入密码: ")`：隐藏用户输入的密码
2. `hashlib.sha256(password.encode()).hexdigest()`：使用SHA256哈希密码
3. `json.dump(data, file, ensure_ascii=False, indent=2)`：格式化保存JSON数据
4. `self.data_file.parent.mkdir(parents=True, exist_ok=True)`：确保目录存在

如果在实际应用中直接存储密码的哈希值，应该使用加盐哈希(salted hash)以增加安全性。

**案例2代码解释**：
1. `zipfile.ZipFile(backup_file, 'w', zipfile.ZIP_DEFLATED)`：创建ZIP文件
2. `file_path.relative_to(source_path.parent)`：计算文件的相对路径
3. `zipf.extractall(target_path)`：解压所有文件
4. `shutil.rmtree("test_data", ignore_errors=True)`：删除整个目录树

如果备份的文件非常大，应该考虑分卷压缩或者增量备份以节省存储空间。

这些实战案例展示了文件操作在实际应用中的各种场景，包括数据持久化、配置管理、日志记录、文件同步和备份恢复等。通过这些例子，可以更好地理解如何在实际项目中正确和安全地使用Python的文件操作功能。

