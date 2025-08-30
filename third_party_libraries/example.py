# Python第三方库使用示例

print("=== 1. requests库示例 ===")
try:
    import requests
    
    # 发送GET请求
    response = requests.get("https://httpbin.org/get")
    print(f"GET请求状态码: {response.status_code}")
    
    # 发送带参数的GET请求
    params = {"key1": "value1", "key2": "value2"}
    response = requests.get("https://httpbin.org/get", params=params)
    print(f"带参数的URL: {response.url}")
    
    # 发送POST请求
    data = {"name": "张三", "age": 25}
    response = requests.post("https://httpbin.org/post", data=data)
    print(f"POST请求响应: {response.json()['form']}")
    
    # 设置请求头
    headers = {"User-Agent": "Python Requests"}
    response = requests.get("https://httpbin.org/headers", headers=headers)
    print(f"请求头: {response.json()['headers']['User-Agent']}")
    
except ImportError:
    print("requests库未安装，请使用 'pip install requests' 安装")
except Exception as e:
    print(f"requests示例出错: {e}")

print("\n=== 2. numpy库示例 ===")
try:
    import numpy as np
    
    # 创建数组
    arr = np.array([1, 2, 3, 4, 5])
    print(f"一维数组: {arr}")
    
    # 创建二维数组
    matrix = np.array([[1, 2, 3], [4, 5, 6]])
    print(f"二维数组:\n{matrix}")
    
    # 数组运算
    print(f"数组加法: {arr + 10}")
    print(f"数组乘法: {arr * 2}")
    
    # 创建特殊数组
    zeros = np.zeros((2, 3))
    print(f"零数组:\n{zeros}")
    
    ones = np.ones((2, 2))
    print(f"一数组:\n{ones}")
    
    # 数学函数
    print(f"数组平均值: {np.mean(arr)}")
    print(f"数组标准差: {np.std(arr)}")
    
except ImportError:
    print("numpy库未安装，请使用 'pip install numpy' 安装")
except Exception as e:
    print(f"numpy示例出错: {e}")

print("\n=== 3. matplotlib库示例 ===")
try:
    import matplotlib.pyplot as plt
    import numpy as np
    
    # 准备数据
    x = np.linspace(0, 10, 100)
    y = np.sin(x)
    
    # 创建简单图表
    plt.figure(figsize=(8, 4))
    plt.plot(x, y, label="sin(x)")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.title("正弦函数图")
    plt.legend()
    plt.grid(True)
    
    # 保存图表（在实际环境中可以显示）
    plt.savefig("sin_function.png", dpi=150, bbox_inches='tight')
    print("图表已保存为sin_function.png")
    plt.close()
    
except ImportError:
    print("matplotlib库未安装，请使用 'pip install matplotlib' 安装")
except Exception as e:
    print(f"matplotlib示例出错: {e}")

print("\n=== 4. pandas库示例 ===")
try:
    import pandas as pd
    
    # 创建DataFrame
    data = {
        "姓名": ["张三", "李四", "王五"],
        "年龄": [25, 30, 35],
        "城市": ["北京", "上海", "广州"]
    }
    df = pd.DataFrame(data)
    print("DataFrame数据:")
    print(df)
    
    # 基本统计信息
    print(f"\n年龄统计信息:")
    print(df["年龄"].describe())
    
    # 数据筛选
    older_than_25 = df[df["年龄"] > 25]
    print(f"\n年龄大于25的人:")
    print(older_than_25)
    
    # 添加新列
    df["出生年份"] = 2023 - df["年龄"]
    print(f"\n添加出生年份后:")
    print(df)
    
except ImportError:
    print("pandas库未安装，请使用 'pip install pandas' 安装")
except Exception as e:
    print(f"pandas示例出错: {e}")

print("\n=== 5. 虚拟环境和依赖管理示例 ===")
print("虚拟环境和依赖管理命令示例:")
print("# 创建虚拟环境")
print("python -m venv myenv")
print()
print("# 激活虚拟环境 (Linux/Mac)")
print("source myenv/bin/activate")
print()
print("# 激活虚拟环境 (Windows)")
print("myenv\\Scripts\\activate")
print()
print("# 安装包")
print("pip install requests numpy pandas matplotlib")
print()
print("# 生成依赖列表")
print("pip freeze > requirements.txt")
print()
print("# 从依赖列表安装")
print("pip install -r requirements.txt")
print()
print("# 退出虚拟环境")
print("deactivate")

# 创建示例requirements.txt文件
requirements_content = """requests==2.28.1
numpy==1.24.0
pandas==1.5.2
matplotlib==3.6.2
"""

try:
    with open("requirements_example.txt", "w", encoding="utf-8") as f:
        f.write(requirements_content)
    print("示例requirements.txt文件已创建")
    
    # 读取并显示内容
    with open("requirements_example.txt", "r", encoding="utf-8") as f:
        content = f.read()
    print("requirements_example.txt内容:")
    print(content)
    
    # 清理文件
    import os
    os.remove("requirements_example.txt")
    
except Exception as e:
    print(f"创建requirements示例文件失败: {e}")

print("\n=== 6. Flask Web框架示例 ===")
flask_example = '''
# Flask示例代码 (flask_example.py)
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return '<h1>欢迎来到Flask示例</h1>'

@app.route('/user/<name>')
def user(name):
    return f'<h1>你好, {name}!</h1>'

@app.route('/api/data')
def api_data():
    data = {"message": "Hello from Flask API", "status": "success"}
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
'''

print("Flask示例代码:")
print(flask_example)
print("运行方式: python flask_example.py")
print("访问地址: http://localhost:5000")

print("\n=== 7. 第三方库安装和使用最佳实践 ===")
print("1. 始终在虚拟环境中工作")
print("2. 使用明确的版本号避免兼容性问题")
print("3. 定期更新依赖库以获取安全补丁")
print("4. 阅读官方文档了解正确用法")
print("5. 注意库的许可证是否符合项目要求")
print("6. 避免安装不必要的依赖")