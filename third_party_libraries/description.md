# Python第三方库使用知识点

## 1. 第三方库概述和包管理

### 知识点解析

**概念定义**：第三方库就像别人已经做好的工具箱，我们可以直接拿过来使用，而不需要自己从头制作。比如别人做好的计算器、画图工具、网络请求工具等，我们只需要安装就能使用，大大提高了编程效率。

**核心规则**：
1. 使用pip工具安装和管理第三方库
2. 通过虚拟环境隔离不同项目的依赖
3. 使用requirements.txt文件记录项目依赖
4. 定期更新和维护第三方库

**常见易错点**：
1. 忘记激活虚拟环境导致全局环境混乱
2. 不固定依赖版本导致项目在不同环境中行为不一致
3. 安装不兼容的库版本导致程序出错
4. 忽略库的安全更新导致安全风险

### 实战案例

#### 案例1：项目依赖管理器
```python
# 项目依赖管理器
print("===项目依赖管理器===")

import subprocess
import sys
import os
from pathlib import Path

class DependencyManager:
    """项目依赖管理器"""
    
    def __init__(self, project_name="my_project"):
        """
        初始化依赖管理器
        
        参数:
            project_name (str): 项目名称
        """
        self.project_name = project_name
        self.venv_name = f"{project_name}_env"
        print(f"项目依赖管理器已启动，项目: {project_name}")
    
    def create_virtual_environment(self):
        """创建虚拟环境"""
        try:
            print(f"正在创建虚拟环境: {self.venv_name}")
            result = subprocess.run([
                sys.executable, "-m", "venv", self.venv_name
            ], check=True, capture_output=True, text=True)
            
            print(f"虚拟环境创建成功: {self.venv_name}")
            return True
        except subprocess.CalledProcessError as e:
            print(f"创建虚拟环境失败: {e}")
            return False
        except Exception as e:
            print(f"创建虚拟环境时发生未知错误: {e}")
            return False
    
    def activate_virtual_environment(self):
        """激活虚拟环境说明"""
        print(f"\n=== 激活虚拟环境 ===")
        if os.name == 'nt':  # Windows
            activate_script = f"{self.venv_name}\\Scripts\\activate"
            print(f"Windows系统请运行:")
            print(f"  {activate_script}")
        else:  # Unix/Linux/Mac
            activate_script = f"{self.venv_name}/bin/activate"
            print(f"Unix/Linux/Mac系统请运行:")
            print(f"  source {activate_script}")
    
    def install_package(self, package_name, version=None):
        """
        安装包
        
        参数:
            package_name (str): 包名
            version (str): 版本号，None表示安装最新版本
        """
        try:
            # 构建安装命令
            if version:
                package_spec = f"{package_name}=={version}"
            else:
                package_spec = package_name
            
            print(f"正在安装包: {package_spec}")
            
            # 在虚拟环境中安装包
            pip_path = os.path.join(self.venv_name, "Scripts" if os.name == 'nt' else "bin", "pip")
            result = subprocess.run([
                pip_path, "install", package_spec
            ], check=True, capture_output=True, text=True)
            
            print(f"包安装成功: {package_spec}")
            return True
        except subprocess.CalledProcessError as e:
            print(f"安装包失败: {e}")
            return False
        except Exception as e:
            print(f"安装包时发生未知错误: {e}")
            return False
    
    def create_requirements_file(self, packages):
        """
        创建requirements.txt文件
        
        参数:
            packages (dict): 包名和版本号的字典
        """
        try:
            requirements_content = ""
            for package, version in packages.items():
                if version:
                    requirements_content += f"{package}=={version}\n"
                else:
                    requirements_content += f"{package}\n"
            
            requirements_file = f"{self.project_name}_requirements.txt"
            with open(requirements_file, "w", encoding="utf-8") as f:
                f.write(requirements_content)
            
            print(f"requirements.txt文件已创建: {requirements_file}")
            print("文件内容:")
            print(requirements_content)
            return requirements_file
        except Exception as e:
            print(f"创建requirements.txt文件失败: {e}")
            return None
    
    def install_from_requirements(self, requirements_file):
        """
        从requirements.txt安装包
        
        参数:
            requirements_file (str): requirements文件路径
        """
        try:
            if not os.path.exists(requirements_file):
                print(f"requirements文件不存在: {requirements_file}")
                return False
            
            print(f"正在从 {requirements_file} 安装包")
            
            pip_path = os.path.join(self.venv_name, "Scripts" if os.name == 'nt' else "bin", "pip")
            result = subprocess.run([
                pip_path, "install", "-r", requirements_file
            ], check=True, capture_output=True, text=True)
            
            print("包安装成功")
            return True
        except subprocess.CalledProcessError as e:
            print(f"从requirements安装包失败: {e}")
            return False
        except Exception as e:
            print(f"从requirements安装包时发生未知错误: {e}")
            return False
    
    def list_installed_packages(self):
        """列出已安装的包"""
        try:
            print("已安装的包:")
            
            pip_path = os.path.join(self.venv_name, "Scripts" if os.name == 'nt' else "bin", "pip")
            result = subprocess.run([
                pip_path, "list"
            ], check=True, capture_output=True, text=True)
            
            print(result.stdout)
            return True
        except subprocess.CalledProcessError as e:
            print(f"列出已安装包失败: {e}")
            return False
        except Exception as e:
            print(f"列出已安装包时发生未知错误: {e}")
            return False

# 使用依赖管理器
print("创建依赖管理器:")
manager = DependencyManager("web_project")

# 创建虚拟环境
manager.create_virtual_environment()

# 激活虚拟环境说明
manager.activate_virtual_environment()

# 创建requirements.txt文件
packages = {
    "flask": "2.2.2",
    "requests": "2.28.1",
    "numpy": "1.24.0",
    "pandas": "1.5.2"
}

requirements_file = manager.create_requirements_file(packages)

# 演示依赖管理概念（实际安装会因为缺少真实环境而失败）
print("\n=== 依赖管理概念演示 ===")
print("在实际项目中，您需要:")
print("1. 激活虚拟环境")
print("2. 运行: pip install -r requirements.txt")
print("3. 开始开发项目")

# 清理文件
if requirements_file and os.path.exists(requirements_file):
    os.remove(requirements_file)
```

#### 案例2：Web应用开发环境
```python
# Web应用开发环境
print("\n===Web应用开发环境===")

import json
import os

class WebDevEnvironment:
    """Web应用开发环境"""
    
    def __init__(self):
        """初始化Web开发环境"""
        print("Web应用开发环境已启动")
    
    def create_project_structure(self):
        """创建项目结构"""
        print("\n=== 创建项目结构 ===")
        
        # 项目目录结构
        structure = {
            "web_app": {
                "README.md": "# Web应用\n这是一个Web应用程序",
                "requirements.txt": "flask==2.2.2\nrequests==2.28.1\n",
                "app.py": self._get_app_py_content(),
                "config.py": self._get_config_py_content(),
                "models": {
                    "__init__.py": "",
                    "user.py": self._get_user_py_content()
                },
                "api": {
                    "__init__.py": "",
                    "routes": {
                        "__init__.py": "",
                        "auth.py": self._get_auth_py_content(),
                        "users.py": self._get_users_py_content()
                    }
                },
                "utils": {
                    "__init__.py": "",
                    "helpers.py": self._get_helpers_py_content()
                },
                "templates": {
                    "base.html": self._get_base_html_content(),
                    "index.html": self._get_index_html_content(),
                    "login.html": self._get_login_html_content()
                },
                "static": {
                    "css": {
                        "style.css": self._get_style_css_content()
                    },
                    "js": {
                        "app.js": self._get_app_js_content()
                    }
                },
                "tests": {
                    "__init__.py": "",
                    "test_app.py": self._get_test_app_py_content()
                }
            }
        }
        
        self._create_structure(structure)
        print("项目结构创建完成")
    
    def _create_structure(self, structure, base_path="."):
        """递归创建目录结构"""
        for name, content in structure.items():
            path = os.path.join(base_path, name)
            if isinstance(content, dict):
                # 创建目录
                os.makedirs(path, exist_ok=True)
                # 递归创建子结构
                self._create_structure(content, path)
            else:
                # 创建文件
                with open(path, "w", encoding="utf-8") as f:
                    f.write(content)
    
    def _get_app_py_content(self):
        """获取app.py内容"""
        return '''"""
Web应用主文件
"""

from flask import Flask
from config import Config

def create_app():
    """创建Flask应用"""
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # 注册蓝图
    from api.routes import auth, users
    app.register_blueprint(auth.bp)
    app.register_blueprint(users.bp)
    
    @app.route("/")
    def index():
        return "<h1>欢迎来到Web应用</h1>"
    
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
'''
    
    def _get_config_py_content(self):
        """获取config.py内容"""
        return '''"""
应用配置
"""

import os

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "dev-secret-key"
    DEBUG = os.environ.get("DEBUG", "False").lower() == "true"

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False

config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig
}
'''
    
    def _get_user_py_content(self):
        """获取user.py内容"""
        return '''"""
用户模型
"""

class User:
    def __init__(self, username, email):
        self.username = username
        self.email = email
        self.id = None
    
    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email
        }
'''
    
    def _get_auth_py_content(self):
        """获取auth.py内容"""
        return '''"""
认证路由
"""

from flask import Blueprint, request, jsonify

bp = Blueprint("auth", __name__, url_prefix="/auth")

@bp.route("/login", methods=["POST"])
def login():
    """用户登录"""
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    
    # 这里应该是实际的认证逻辑
    if username and password:
        return jsonify({
            "success": True,
            "message": "登录成功",
            "user": {"username": username}
        })
    else:
        return jsonify({
            "success": False,
            "message": "用户名或密码错误"
        }), 401

@bp.route("/register", methods=["POST"])
def register():
    """用户注册"""
    data = request.get_json()
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")
    
    # 这里应该是实际的注册逻辑
    if username and email and password:
        return jsonify({
            "success": True,
            "message": "注册成功",
            "user": {"username": username, "email": email}
        })
    else:
        return jsonify({
            "success": False,
            "message": "请提供完整的注册信息"
        }), 400
'''
    
    def _get_users_py_content(self):
        """获取users.py内容"""
        return '''"""
用户路由
"""

from flask import Blueprint, jsonify

bp = Blueprint("users", __name__, url_prefix="/api/users")

@bp.route("/", methods=["GET"])
def get_users():
    """获取用户列表"""
    # 这里应该是从数据库获取用户列表
    users = [
        {"id": 1, "username": "张三", "email": "zhangsan@example.com"},
        {"id": 2, "username": "李四", "email": "lisi@example.com"}
    ]
    
    return jsonify({
        "success": True,
        "data": users
    })

@bp.route("/<int:user_id>", methods=["GET"])
def get_user(user_id):
    """获取单个用户"""
    # 这里应该是从数据库获取指定用户
    user = {"id": user_id, "username": "用户", "email": "user@example.com"}
    
    return jsonify({
        "success": True,
        "data": user
    })
'''
    
    def _get_helpers_py_content(self):
        """获取helpers.py内容"""
        return '''"""
工具函数
"""

def validate_email(email):
    """验证邮箱格式"""
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def generate_token():
    """生成访问令牌"""
    import secrets
    return secrets.token_urlsafe(32)
'''
    
    def _get_base_html_content(self):
        """获取base.html内容"""
        return '''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Web应用{% endblock %}</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
</head>
<body>
    <nav>
        <ul>
            <li><a href="{{ url_for('index') }}">首页</a></li>
            <li><a href="{{ url_for('auth.login') }}">登录</a></li>
        </ul>
    </nav>
    
    <main>
        {% block content %}{% endblock %}
    </main>
    
    <script src="{{ url_for('static', filename='js/app.js') }}"></script>
</body>
</html>
'''
    
    def _get_index_html_content(self):
        """获取index.html内容"""
        return '''{% extends "base.html" %}

{% block title %}首页 - Web应用{% endblock %}

{% block content %}
<h1>欢迎来到Web应用</h1>
<p>这是一个使用Flask构建的Web应用程序示例。</p>

<div class="features">
    <h2>功能特性</h2>
    <ul>
        <li>用户认证</li>
        <li>REST API</li>
        <li>响应式设计</li>
        <li>现代化前端</li>
    </ul>
</div>
{% endblock %}
'''
    
    def _get_login_html_content(self):
        """获取login.html内容"""
        return '''{% extends "base.html" %}

{% block title %}登录 - Web应用{% endblock %}

{% block content %}
<h1>用户登录</h1>

<form id="loginForm">
    <div class="form-group">
        <label for="username">用户名:</label>
        <input type="text" id="username" name="username" required>
    </div>
    
    <div class="form-group">
        <label for="password">密码:</label>
        <input type="password" id="password" name="password" required>
    </div>
    
    <button type="submit">登录</button>
</form>

<script>
document.getElementById('loginForm').addEventListener('submit', function(e) {
    e.preventDefault();
    // 这里应该是实际的登录逻辑
    alert('登录功能演示');
});
</script>
{% endblock %}
'''
    
    def _get_style_css_content(self):
        """获取style.css内容"""
        return '''/* 样式表 */
body {
    font-family: Arial, sans-serif;
    line-height: 1.6;
    margin: 0;
    padding: 0;
}

nav {
    background-color: #333;
    padding: 1rem;
}

nav ul {
    list-style-type: none;
    margin: 0;
    padding: 0;
}

nav ul li {
    display: inline;
    margin-right: 1rem;
}

nav ul li a {
    color: white;
    text-decoration: none;
}

main {
    padding: 2rem;
}

.form-group {
    margin-bottom: 1rem;
}

.form-group label {
    display: block;
    margin-bottom: 0.5rem;
}

.form-group input {
    width: 100%;
    padding: 0.5rem;
    border: 1px solid #ddd;
    border-radius: 4px;
}

button {
    background-color: #007bff;
    color: white;
    padding: 0.5rem 1rem;
    border: none;
    border-radius: 4px;
    cursor: pointer;
}

button:hover {
    background-color: #0056b3;
}
'''
    
    def _get_app_js_content(self):
        """获取app.js内容"""
        return '''// 前端JavaScript
console.log('Web应用前端脚本已加载');

// 可以在这里添加交互功能
document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM已加载完成');
});
'''
    
    def _get_test_app_py_content(self):
        """获取test_app.py内容"""
        return '''"""
应用测试
"""

import unittest
from app import create_app

class AppTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
    
    def test_index(self):
        """测试首页"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('欢迎来到Web应用', response.get_data(as_text=True))
    
    def test_auth_login(self):
        """测试登录接口"""
        response = self.client.post('/auth/login', 
                                  json={'username': 'test', 'password': 'test'})
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
'''
    
    def show_project_structure(self):
        """显示项目结构"""
        print("\n=== 项目结构 ===")
        structure = """
web_app/
├── README.md
├── requirements.txt
├── app.py
├── config.py
├── models/
│   ├── __init__.py
│   └── user.py
├── api/
│   ├── __init__.py
│   └── routes/
│       ├── __init__.py
│       ├── auth.py
│       └── users.py
├── utils/
│   ├── __init__.py
│   └── helpers.py
├── templates/
│   ├── base.html
│   ├── index.html
│   └── login.html
├── static/
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── app.js
└── tests/
    ├── __init__.py
    └── test_app.py
        """
        print(structure)
    
    def cleanup_project(self):
        """清理项目文件"""
        print("\n=== 清理项目文件 ===")
        import shutil
        try:
            if os.path.exists("web_app"):
                shutil.rmtree("web_app")
                print("项目文件已清理")
            else:
                print("项目目录不存在")
        except Exception as e:
            print(f"清理项目文件时出错: {e}")

# 使用Web开发环境
print("创建Web开发环境:")
web_env = WebDevEnvironment()

# 显示项目结构
web_env.show_project_structure()

# 创建项目结构
web_env.create_project_structure()

# 清理项目文件
web_env.cleanup_project()
```

### 代码说明

**案例1代码解释**：
1. `subprocess.run([sys.executable, "-m", "venv", self.venv_name], check=True)`：使用subprocess模块创建虚拟环境
2. `os.path.join(self.venv_name, "Scripts" if os.name == 'nt' else "bin", "pip")`：根据操作系统构建pip路径
3. `with open(requirements_file, "w", encoding="utf-8") as f:`：创建并写入requirements.txt文件
4. `subprocess.CalledProcessError`：捕获命令执行失败的异常

如果虚拟环境不存在就直接运行pip命令，会使用全局Python环境而不是项目的隔离环境。

**案例2代码解释**：
1. `os.makedirs(path, exist_ok=True)`：创建目录，如果目录已存在不会报错
2. `with open(path, "w", encoding="utf-8") as f:`：创建并写入文件内容
3. `request.get_json()`：获取POST请求中的JSON数据
4. `jsonify({...})`：将Python字典转换为JSON响应

如果在Flask路由中忘记return语句，会导致请求没有响应，客户端会一直等待。

## 2. requests库 - 网络请求

### 知识点解析

**概念定义**：requests库就像Python的"网络浏览器"，可以帮我们发送各种网络请求，比如获取网页内容、提交表单、上传文件等，而不需要打开真正的浏览器。

**核心规则**：
1. 使用requests.get()发送GET请求获取数据
2. 使用requests.post()发送POST请求提交数据
3. 处理响应状态码和内容
4. 设置请求头、认证信息和超时时间

**常见易错点**：
1. 忘记处理网络异常导致程序崩溃
2. 不检查响应状态码导致处理错误数据
3. 发送敏感信息时不使用HTTPS
4. 不设置超时时间导致程序长时间等待

### 实战案例

#### 案例1：API客户端
```python
# API客户端
print("===API客户端===")

import json
import time

class APIClient:
    """API客户端"""
    
    def __init__(self, base_url="https://jsonplaceholder.typicode.com"):
        """
        初始化API客户端
        
        参数:
            base_url (str): API基础URL
        """
        self.base_url = base_url
        print(f"API客户端已初始化，基础URL: {base_url}")
    
    def get_posts(self, user_id=None):
        """
        获取文章列表
        
        参数:
            user_id (int): 用户ID，None表示获取所有文章
            
        返回:
            list: 文章列表
        """
        try:
            import requests
            
            # 构建URL
            url = f"{self.base_url}/posts"
            params = {}
            if user_id:
                params["userId"] = user_id
            
            print(f"正在获取文章列表...")
            response = requests.get(url, params=params, timeout=10)
            
            # 检查响应状态
            if response.status_code == 200:
                posts = response.json()
                print(f"成功获取 {len(posts)} 篇文章")
                return posts
            else:
                print(f"获取文章失败，状态码: {response.status_code}")
                return []
                
        except ImportError:
            print("错误: 未安装requests库，请运行 'pip install requests'")
            return []
        except requests.exceptions.Timeout:
            print("错误: 请求超时")
            return []
        except requests.exceptions.RequestException as e:
            print(f"网络请求错误: {e}")
            return []
        except json.JSONDecodeError:
            print("错误: 响应不是有效的JSON格式")
            return []
        except Exception as e:
            print(f"获取文章时发生未知错误: {e}")
            return []
    
    def get_post(self, post_id):
        """
        获取单篇文章
        
        参数:
            post_id (int): 文章ID
            
        返回:
            dict: 文章信息
        """
        try:
            import requests
            
            url = f"{self.base_url}/posts/{post_id}"
            print(f"正在获取文章 {post_id}...")
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                post = response.json()
                print(f"成功获取文章: {post['title']}")
                return post
            else:
                print(f"获取文章失败，状态码: {response.status_code}")
                return None
                
        except ImportError:
            print("错误: 未安装requests库，请运行 'pip install requests'")
            return None
        except requests.exceptions.RequestException as e:
            print(f"网络请求错误: {e}")
            return None
        except Exception as e:
            print(f"获取文章时发生未知错误: {e}")
            return None
    
    def create_post(self, title, body, user_id):
        """
        创建新文章
        
        参数:
            title (str): 文章标题
            body (str): 文章内容
            user_id (int): 用户ID
            
        返回:
            dict: 创建的文章信息
        """
        try:
            import requests
            
            url = f"{self.base_url}/posts"
            data = {
                "title": title,
                "body": body,
                "userId": user_id
            }
            
            print(f"正在创建文章: {title}")
            response = requests.post(url, json=data, timeout=10)
            
            if response.status_code == 201:
                post = response.json()
                print(f"文章创建成功，ID: {post['id']}")
                return post
            else:
                print(f"创建文章失败，状态码: {response.status_code}")
                return None
                
        except ImportError:
            print("错误: 未安装requests库，请运行 'pip install requests'")
            return None
        except requests.exceptions.RequestException as e:
            print(f"网络请求错误: {e}")
            return None
        except Exception as e:
            print(f"创建文章时发生未知错误: {e}")
            return None
    
    def update_post(self, post_id, title=None, body=None):
        """
        更新文章
        
        参数:
            post_id (int): 文章ID
            title (str): 新标题，None表示不更新
            body (str): 新内容，None表示不更新
            
        返回:
            dict: 更新后的文章信息
        """
        try:
            import requests
            
            # 首先获取原文内容
            original_post = self.get_post(post_id)
            if not original_post:
                print("无法获取原文内容")
                return None
            
            # 构建更新数据
            update_data = {}
            if title is not None:
                update_data["title"] = title
            else:
                update_data["title"] = original_post["title"]
                
            if body is not None:
                update_data["body"] = body
            else:
                update_data["body"] = original_post["body"]
                
            update_data["userId"] = original_post["userId"]
            update_data["id"] = post_id
            
            url = f"{self.base_url}/posts/{post_id}"
            print(f"正在更新文章 {post_id}...")
            response = requests.put(url, json=update_data, timeout=10)
            
            if response.status_code == 200:
                updated_post = response.json()
                print(f"文章更新成功")
                return updated_post
            else:
                print(f"更新文章失败，状态码: {response.status_code}")
                return None
                
        except ImportError:
            print("错误: 未安装requests库，请运行 'pip install requests'")
            return None
        except requests.exceptions.RequestException as e:
            print(f"网络请求错误: {e}")
            return None
        except Exception as e:
            print(f"更新文章时发生未知错误: {e}")
            return None
    
    def delete_post(self, post_id):
        """
        删除文章
        
        参数:
            post_id (int): 文章ID
            
        返回:
            bool: 是否删除成功
        """
        try:
            import requests
            
            url = f"{self.base_url}/posts/{post_id}"
            print(f"正在删除文章 {post_id}...")
            response = requests.delete(url, timeout=10)
            
            if response.status_code == 200:
                print(f"文章删除成功")
                return True
            else:
                print(f"删除文章失败，状态码: {response.status_code}")
                return False
                
        except ImportError:
            print("错误: 未安装requests库，请运行 'pip install requests'")
            return False
        except requests.exceptions.RequestException as e:
            print(f"网络请求错误: {e}")
            return False
        except Exception as e:
            print(f"删除文章时发生未知错误: {e}")
            return False

# 使用API客户端
print("创建API客户端:")
client = APIClient()

# 获取文章列表
print("\n获取文章列表:")
posts = client.get_posts()
if posts:
    print(f"获取到 {len(posts)} 篇文章")
    # 显示前3篇文章
    for post in posts[:3]:
        print(f"  - {post['id']}: {post['title']}")

# 获取单篇文章
print("\n获取单篇文章:")
post = client.get_post(1)
if post:
    print(f"文章标题: {post['title']}")
    print(f"文章内容: {post['body'][:50]}...")

# 创建新文章
print("\n创建新文章:")
new_post = client.create_post(
    title="我的新文章",
    body="这是文章的内容，包含一些示例文本。",
    user_id=1
)

# 更新文章
if new_post:
    print("\n更新文章:")
    updated_post = client.update_post(
        post_id=new_post["id"],
        title="更新后的文章标题"
    )

# 删除文章
if new_post:
    print("\n删除文章:")
    success = client.delete_post(new_post["id"])
    if success:
        print("文章删除成功")

print("\n=== 网络请求最佳实践 ===")
print("1. 始终处理网络异常")
print("2. 设置合理的超时时间")
print("3. 检查响应状态码")
print("4. 使用会话对象复用连接")
print("5. 设置适当的请求头")
```

#### 案例2：网页数据抓取器
```python
# 网页数据抓取器
print("\n===网页数据抓取器===")

import time
import json
from urllib.parse import urljoin, urlparse

class WebScraper:
    """网页数据抓取器"""
    
    def __init__(self):
        """初始化网页抓取器"""
        print("网页数据抓取器已启动")
    
    def fetch_webpage(self, url, headers=None):
        """
        获取网页内容
        
        参数:
            url (str): 网页URL
            headers (dict): 请求头
            
        返回:
            str: 网页内容
        """
        try:
            import requests
            
            # 默认请求头
            default_headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            
            if headers:
                default_headers.update(headers)
            
            print(f"正在获取网页: {url}")
            response = requests.get(url, headers=default_headers, timeout=10)
            
            if response.status_code == 200:
                print(f"网页获取成功，内容长度: {len(response.text)} 字符")
                return response.text
            else:
                print(f"获取网页失败，状态码: {response.status_code}")
                return None
                
        except ImportError:
            print("错误: 未安装requests库，请运行 'pip install requests'")
            return None
        except requests.exceptions.Timeout:
            print("错误: 请求超时")
            return None
        except requests.exceptions.RequestException as e:
            print(f"网络请求错误: {e}")
            return None
        except Exception as e:
            print(f"获取网页时发生未知错误: {e}")
            return None
    
    def fetch_json_data(self, url, params=None):
        """
        获取JSON数据
        
        参数:
            url (str): API URL
            params (dict): 查询参数
            
        返回:
            dict: JSON数据
        """
        try:
            import requests
            
            print(f"正在获取JSON数据: {url}")
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                print(f"JSON数据获取成功，包含 {len(str(data))} 个字符")
                return data
            else:
                print(f"获取JSON数据失败，状态码: {response.status_code}")
                return None
                
        except ImportError:
            print("错误: 未安装requests库，请运行 'pip install requests'")
            return None
        except requests.exceptions.RequestException as e:
            print(f"网络请求错误: {e}")
            return None
        except json.JSONDecodeError:
            print("错误: 响应不是有效的JSON格式")
            return None
        except Exception as e:
            print(f"获取JSON数据时发生未知错误: {e}")
            return None
    
    def download_file(self, url, filename):
        """
        下载文件
        
        参数:
            url (str): 文件URL
            filename (str): 保存文件名
            
        返回:
            bool: 是否下载成功
        """
        try:
            import requests
            
            print(f"正在下载文件: {url}")
            response = requests.get(url, timeout=30, stream=True)
            
            if response.status_code == 200:
                with open(filename, 'wb') as f:
                    # 分块下载大文件
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
                
                print(f"文件下载成功: {filename}")
                return True
            else:
                print(f"下载文件失败，状态码: {response.status_code}")
                return False
                
        except ImportError:
            print("错误: 未安装requests库，请运行 'pip install requests'")
            return False
        except requests.exceptions.RequestException as e:
            print(f"网络请求错误: {e}")
            return False
        except Exception as e:
            print(f"下载文件时发生未知错误: {e}")
            return False
    
    def check_website_status(self, urls):
        """
        检查网站状态
        
        参数:
            urls (list): URL列表
            
        返回:
            dict: 状态检查结果
        """
        try:
            import requests
            
            results = {}
            
            for url in urls:
                try:
                    print(f"检查网站状态: {url}")
                    response = requests.head(url, timeout=10)
                    results[url] = {
                        'status_code': response.status_code,
                        'status_text': '可用' if response.status_code == 200 else '不可用',
                        'response_time': response.elapsed.total_seconds()
                    }
                except requests.exceptions.RequestException as e:
                    results[url] = {
                        'status_code': None,
                        'status_text': f'错误: {str(e)}',
                        'response_time': None
                    }
                
                # 避免请求过于频繁
                time.sleep(0.1)
            
            return results
            
        except ImportError:
            print("错误: 未安装requests库，请运行 'pip install requests'")
            return {}
        except Exception as e:
            print(f"检查网站状态时发生未知错误: {e}")
            return {}
    
    def simulate_user_session(self, base_url):
        """
        模拟用户会话
        
        参数:
            base_url (str): 基础URL
        """
        try:
            import requests
            
            print(f"模拟用户会话: {base_url}")
            
            # 创建会话对象
            session = requests.Session()
            
            # 设置会话级别的请求头
            session.headers.update({
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            })
            
            # 访问首页
            print("访问首页...")
            response = session.get(base_url, timeout=10)
            print(f"首页状态: {response.status_code}")
            
            # 模拟用户操作
            print("模拟用户操作...")
            time.sleep(1)
            
            # 访问其他页面
            # 注意：这里只是演示，实际使用时需要根据具体网站调整
            print("会话模拟完成")
            
            # 关闭会话
            session.close()
            
        except ImportError:
            print("错误: 未安装requests库，请运行 'pip install requests'")
        except requests.exceptions.RequestException as e:
            print(f"网络请求错误: {e}")
        except Exception as e:
            print(f"模拟用户会话时发生未知错误: {e}")

# 使用网页抓取器
print("创建网页抓取器:")
scraper = WebScraper()

# 获取网页内容（演示，实际运行时需要有效的URL）
print("\n获取网页内容:")
content = scraper.fetch_webpage("https://httpbin.org/html")
if content:
    print(f"网页标题示例: {content[:100]}...")

# 获取JSON数据
print("\n获取JSON数据:")
json_data = scraper.fetch_json_data("https://httpbin.org/json")
if json_data:
    print(f"获取到JSON数据: {type(json_data)}")

# 检查网站状态
print("\n检查网站状态:")
urls = [
    "https://httpbin.org/status/200",
    "https://httpbin.org/status/404",
    "https://httpbin.org/delay/1"
]

status_results = scraper.check_website_status(urls)
for url, result in status_results.items():
    print(f"  {url}: {result['status_text']} (状态码: {result['status_code']})")

# 模拟用户会话
print("\n模拟用户会话:")
scraper.simulate_user_session("https://httpbin.org")

print("\n=== 网页抓取最佳实践 ===")
print("1. 设置合适的User-Agent")
print("2. 控制请求频率，避免给服务器造成压力")
print("3. 处理各种网络异常")
print("4. 使用会话对象复用连接")
print("5. 对于大文件使用流式下载")
print("6. 遵守网站的robots.txt规则")
```

### 代码说明

**案例1代码解释**：
1. `requests.get(url, params=params, timeout=10)`：发送带参数和超时的GET请求
2. `response.json()`：将JSON响应解析为Python对象
3. `requests.post(url, json=data, timeout=10)`：发送JSON数据的POST请求
4. `response.status_code == 201`：检查POST请求是否成功创建资源

如果API需要认证，需要在请求中添加认证头或使用requests.auth模块。

**案例2代码解释**：
1. `response.iter_content(chunk_size=8192)`：分块下载大文件
2. `requests.Session()`：创建会话对象复用连接和Cookie
3. `requests.head(url, timeout=10)`：只获取响应头，不下载完整内容
4. `session.headers.update({...})`：设置会话级别的请求头

如果网站有反爬虫机制，可能需要使用代理、更换User-Agent或添加更多请求头。

## 3. numpy和pandas库 - 数据处理

### 知识点解析

**概念定义**：numpy就像Python的"超级计算器"，可以高效处理大量数值数据；pandas则像"数据管理专家"，专门处理表格数据，比如Excel表格或数据库表格。

**核心规则**：
1. numpy用于数值计算和多维数组操作
2. pandas用于数据处理和分析
3. 使用向量化操作提高计算效率
4. 合理使用索引和切片操作数据

**常见易错点**：
1. 混淆numpy数组和Python列表的操作方法
2. 忘记处理缺失数据导致计算错误
3. 不理解数组广播机制导致意外结果
4. 内存使用不当导致程序崩溃

### 实战案例

#### 案例1：学生成绩分析系统
```python
# 学生成绩分析系统
print("===学生成绩分析系统===")

class StudentGradeAnalyzer:
    """学生成绩分析系统"""
    
    def __init__(self):
        """初始化成绩分析系统"""
        print("学生成绩分析系统已启动")
    
    def create_sample_data(self):
        """创建示例成绩数据"""
        try:
            import numpy as np
            
            # 创建示例学生成绩数据
            np.random.seed(42)  # 设置随机种子以获得可重现的结果
            
            # 生成50个学生的成绩数据
            student_ids = np.arange(1, 51)  # 学号1-50
            math_scores = np.random.normal(75, 10, 50)  # 数学成绩，均值75，标准差10
            english_scores = np.random.normal(80, 8, 50)   # 英语成绩，均值80，标准差8
            science_scores = np.random.normal(78, 12, 50)  # 科学成绩，均值78，标准差12
            
            # 确保成绩在合理范围内(0-100)
            math_scores = np.clip(math_scores, 0, 100)
            english_scores = np.clip(english_scores, 0, 100)
            science_scores = np.clip(science_scores, 0, 100)
            
            # 创建结构化数组存储学生成绩
            dtype = [('id', 'i4'), ('math', 'f4'), ('english', 'f4'), ('science', 'f4')]
            grades = np.zeros(50, dtype=dtype)
            grades['id'] = student_ids
            grades['math'] = math_scores
            grades['english'] = english_scores
            grades['science'] = science_scores
            
            print(f"示例成绩数据创建完成，共{len(grades)}个学生")
            return grades
            
        except ImportError:
            print("错误: 未安装numpy库，请运行 'pip install numpy'")
            return None
        except Exception as e:
            print(f"创建示例数据时发生错误: {e}")
            return None
    
    def analyze_grades(self, grades):
        """
        分析成绩数据
        
        参数:
            grades: 成绩数据
        """
        try:
            import numpy as np
            
            if grades is None:
                print("没有成绩数据可分析")
                return
            
            print("\n=== 成绩统计分析 ===")
            
            # 各科成绩统计
            subjects = ['math', 'english', 'science']
            subject_names = ['数学', '英语', '科学']
            
            for i, subject in enumerate(subjects):
                scores = grades[subject]
                print(f"\n{subject_names[i]}成绩:")
                print(f"  平均分: {np.mean(scores):.2f}")
                print(f"  最高分: {np.max(scores):.2f}")
                print(f"  最低分: {np.min(scores):.2f}")
                print(f"  标准差: {np.std(scores):.2f}")
                print(f"  中位数: {np.median(scores):.2f}")
            
            # 总分和平均分
            total_scores = grades['math'] + grades['english'] + grades['science']
            average_scores = total_scores / 3
            
            print(f"\n总成绩:")
            print(f"  平均总分: {np.mean(total_scores):.2f}")
            print(f"  最高总分: {np.max(total_scores):.2f}")
            print(f"  最低总分: {np.min(total_scores):.2f}")
            
            print(f"\n平均成绩:")
            print(f"  平均分: {np.mean(average_scores):.2f}")
            print(f"  最高分: {np.max(average_scores):.2f}")
            print(f"  最低分: {np.min(average_scores):.2f}")
            
            # 成绩分布
            print(f"\n成绩分布:")
            grade_ranges = [(90, 100, '优秀'), (80, 89, '良好'), (70, 79, '中等'), (60, 69, '及格'), (0, 59, '不及格')]
            
            for min_score, max_score, grade_name in grade_ranges:
                count = np.sum((average_scores >= min_score) & (average_scores <= max_score))
                percentage = count / len(average_scores) * 100
                print(f"  {grade_name} ({min_score}-{max_score}分): {count}人 ({percentage:.1f}%)")
            
            # 找出各科前5名
            print(f"\n各科前5名:")
            for i, subject in enumerate(subjects):
                sorted_indices = np.argsort(grades[subject])[::-1][:5]  # 降序排列，取前5名
                print(f"\n{subject_names[i]}前5名:")
                for j, idx in enumerate(sorted_indices):
                    student_id = grades[idx]['id']
                    score = grades[idx][subject]
                    print(f"  第{j+1}名: 学号{student_id}, {score:.1f}分")
            
            return {
                'total_scores': total_scores,
                'average_scores': average_scores
            }
            
        except ImportError:
            print("错误: 未安装numpy库，请运行 'pip install numpy'")
            return None
        except Exception as e:
            print(f"分析成绩数据时发生错误: {e}")
            return None
    
    def create_grade_dataframe(self, grades):
        """
        创建成绩DataFrame
        
        参数:
            grades: 成绩数据
            
        返回:
            DataFrame: 成绩DataFrame
        """
        try:
            import pandas as pd
            import numpy as np
            
            if grades is None:
                print("没有成绩数据可转换")
                return None
            
            # 将numpy数组转换为DataFrame
            df = pd.DataFrame({
                '学号': grades['id'],
                '数学': grades['math'],
                '英语': grades['english'],
                '科学': grades['science']
            })
            
            # 计算总分和平均分
            df['总分'] = df['数学'] + df['英语'] + df['科学']
            df['平均分'] = df['总分'] / 3
            
            # 计算等级
            def get_grade(average_score):
                if average_score >= 90:
                    return '优秀'
                elif average_score >= 80:
                    return '良好'
                elif average_score >= 70:
                    return '中等'
                elif average_score >= 60:
                    return '及格'
                else:
                    return '不及格'
            
            df['等级'] = df['平均分'].apply(get_grade)
            
            print(f"成绩DataFrame创建完成，{len(df)}行 {len(df.columns)}列")
            return df
            
        except ImportError:
            print("错误: 未安装pandas库，请运行 'pip install pandas'")
            return None
        except Exception as e:
            print(f"创建成绩DataFrame时发生错误: {e}")
            return None
    
    def analyze_with_pandas(self, df):
        """
        使用pandas分析成绩
        
        参数:
            df (DataFrame): 成绩DataFrame
        """
        try:
            import pandas as pd
            
            if df is None:
                print("没有数据可分析")
                return
            
            print("\n=== 使用pandas分析成绩 ===")
            
            # 基本信息
            print(f"数据形状: {df.shape}")
            print(f"列名: {list(df.columns)}")
            
            # 描述性统计
            print("\n描述性统计:")
            print(df.describe())
            
            # 按等级统计
            print("\n等级分布:")
            grade_counts = df['等级'].value_counts()
            print(grade_counts)
            
            # 各科成绩相关性
            print("\n各科成绩相关性:")
            correlation = df[['数学', '英语', '科学']].corr()
            print(correlation)
            
            # 找出总分前10名
            print("\n总分前10名:")
            top_students = df.nlargest(10, '总分')[['学号', '总分', '平均分', '等级']]
            print(top_students.to_string(index=False))
            
            # 各科平均分
            print("\n各科平均分:")
            subject_averages = df[['数学', '英语', '科学']].mean()
            for subject, avg in subject_averages.items():
                print(f"  {subject}: {avg:.2f}分")
            
        except ImportError:
            print("错误: 未安装pandas库，请运行 'pip install pandas'")
        except Exception as e:
            print(f"使用pandas分析成绩时发生错误: {e}")

# 使用成绩分析系统
print("创建成绩分析系统:")
analyzer = StudentGradeAnalyzer()

# 创建示例数据
grades = analyzer.create_sample_data()

# 分析成绩
analysis_result = analyzer.analyze_grades(grades)

# 创建DataFrame
df = analyzer.create_grade_dataframe(grades)

# 使用pandas分析
analyzer.analyze_with_pandas(df)

print("\n=== 数据处理最佳实践 ===")
print("1. 使用numpy进行数值计算")
print("2. 使用pandas处理结构化数据")
print("3. 注意处理缺失值和异常值")
print("4. 合理使用向量化操作提高性能")
print("5. 使用适当的数据类型节省内存")
```

#### 案例2：销售数据分析系统
```python
# 销售数据分析系统
print("\n===销售数据分析系统===")

import json
from datetime import datetime, timedelta

class SalesAnalyzer:
    """销售数据分析系统"""
    
    def __init__(self):
        """初始化销售分析系统"""
        print("销售数据分析系统已启动")
    
    def create_sample_sales_data(self):
        """创建示例销售数据"""
        try:
            import pandas as pd
            import numpy as np
            
            # 设置随机种子
            np.random.seed(42)
            
            # 生成示例销售数据
            dates = pd.date_range('2023-01-01', '2023-12-31', freq='D')
            n_days = len(dates)
            
            # 产品信息
            products = [
                {'id': 1, 'name': '笔记本电脑', 'category': '电子产品', 'price': 5999},
                {'id': 2, 'name': '智能手机', 'category': '电子产品', 'price': 3999},
                {'id': 3, 'name': '平板电脑', 'category': '电子产品', 'price': 2999},
                {'id': 4, 'name': '蓝牙耳机', 'category': '电子产品', 'price': 299},
                {'id': 5, 'name': '智能手表', 'category': '电子产品', 'price': 1999}
            ]
            
            # 生成销售记录
            sales_data = []
            for date in dates:
                # 每天随机生成10-50笔销售记录
                n_sales = np.random.randint(10, 51)
                
                for _ in range(n_sales):
                    product = np.random.choice(products)
                    quantity = np.random.randint(1, 6)  # 1-5件
                    amount = product['price'] * quantity
                    
                    # 随机折扣(0-20%)
                    discount = np.random.random() * 0.2
                    final_amount = amount * (1 - discount)
                    
                    sales_record = {
                        'date': date,
                        'product_id': product['id'],
                        'product_name': product['name'],
                        'category': product['category'],
                        'price': product['price'],
                        'quantity': quantity,
                        'amount': amount,
                        'discount': discount,
                        'final_amount': final_amount
                    }
                    sales_data.append(sales_record)
            
            # 创建DataFrame
            df = pd.DataFrame(sales_data)
            
            print(f"示例销售数据创建完成，共{len(df)}条记录")
            return df
            
        except ImportError as e:
            print(f"错误: 缺少必要的库，请安装 pandas 和 numpy")
            return None
        except Exception as e:
            print(f"创建示例销售数据时发生错误: {e}")
            return None
    
    def load_sales_data(self, filename):
        """
        从文件加载销售数据
        
        参数:
            filename (str): 文件名
            
        返回:
            DataFrame: 销售数据
        """
        try:
            import pandas as pd
            
            if filename.endswith('.csv'):
                df = pd.read_csv(filename)
                print(f"从CSV文件加载数据: {filename}")
            elif filename.endswith('.json'):
                df = pd.read_json(filename)
                print(f"从JSON文件加载数据: {filename}")
            else:
                print("不支持的文件格式")
                return None
            
            print(f"数据加载完成，共{len(df)}条记录")
            return df
            
        except ImportError:
            print("错误: 未安装pandas库，请运行 'pip install pandas'")
            return None
        except Exception as e:
            print(f"加载销售数据时发生错误: {e}")
            return None
    
    def save_sales_data(self, df, filename):
        """
        保存销售数据到文件
        
        参数:
            df (DataFrame): 销售数据
            filename (str): 文件名
        """
        try:
            if filename.endswith('.csv'):
                df.to_csv(filename, index=False)
                print(f"数据已保存到CSV文件: {filename}")
            elif filename.endswith('.json'):
                df.to_json(filename, orient='records', date_format='iso')
                print(f"数据已保存到JSON文件: {filename}")
            else:
                print("不支持的文件格式")
                
        except Exception as e:
            print(f"保存销售数据时发生错误: {e}")
    
    def analyze_sales_trends(self, df):
        """
        分析销售趋势
        
        参数:
            df (DataFrame): 销售数据
        """
        try:
            import pandas as pd
            import numpy as np
            
            if df is None or df.empty:
                print("没有数据可分析")
                return
            
            print("\n=== 销售趋势分析 ===")
            
            # 转换日期列
            df['date'] = pd.to_datetime(df['date'])
            
            # 按日期统计销售额
            daily_sales = df.groupby('date')['final_amount'].sum().reset_index()
            
            # 计算日销售额统计
            print(f"日销售额统计:")
            print(f"  总销售额: ¥{daily_sales['final_amount'].sum():,.2f}")
            print(f"  平均日销售额: ¥{daily_sales['final_amount'].mean():,.2f}")
            print(f"  最高日销售额: ¥{daily_sales['final_amount'].max():,.2f}")
            print(f"  最低日销售额: ¥{daily_sales['final_amount'].min():,.2f}")
            
            # 按月统计销售额
            df['month'] = df['date'].dt.to_period('M')
            monthly_sales = df.groupby('month')['final_amount'].sum()
            
            print(f"\n月度销售额:")
            for month, sales in monthly_sales.items():
                print(f"  {month}: ¥{sales:,.2f}")
            
            # 按产品类别统计
            category_sales = df.groupby('category')['final_amount'].sum().sort_values(ascending=False)
            
            print(f"\n按产品类别统计:")
            for category, sales in category_sales.items():
                percentage = sales / df['final_amount'].sum() * 100
                print(f"  {category}: ¥{sales:,.2f} ({percentage:.1f}%)")
            
            # 按产品统计
            product_sales = df.groupby('product_name')['final_amount'].sum().sort_values(ascending=False)
            
            print(f"\n畅销产品前5名:")
            for i, (product, sales) in enumerate(product_sales.head().items(), 1):
                print(f"  {i}. {product}: ¥{sales:,.2f}")
            
            # 销售数量统计
            print(f"\n销售数量统计:")
            total_quantity = df['quantity'].sum()
            avg_quantity = df['quantity'].mean()
            print(f"  总销售数量: {total_quantity:,} 件")
            print(f"  平均每单数量: {avg_quantity:.2f} 件")
            
            # 折扣分析
            print(f"\n折扣分析:")
            avg_discount = df['discount'].mean() * 100
            total_discount = (df['amount'] - df['final_amount']).sum()
            print(f"  平均折扣率: {avg_discount:.1f}%")
            print(f"  总折扣金额: ¥{total_discount:,.2f}")
            
        except ImportError:
            print("错误: 未安装pandas库，请运行 'pip install pandas'")
        except Exception as e:
            print(f"分析销售趋势时发生错误: {e}")
    
    def create_sales_report(self, df, period='monthly'):
        """
        创建销售报告
        
        参数:
            df (DataFrame): 销售数据
            period (str): 报告周期 ('daily', 'weekly', 'monthly')
        """
        try:
            import pandas as pd
            
            if df is None or df.empty:
                print("没有数据可生成报告")
                return
            
            print(f"\n=== {period.capitalize()} 销售报告 ===")
            
            # 转换日期列
            df['date'] = pd.to_datetime(df['date'])
            
            # 根据周期分组
            if period == 'daily':
                df['period'] = df['date'].dt.date
            elif period == 'weekly':
                df['period'] = df['date'].dt.to_period('W')
            elif period == 'monthly':
                df['period'] = df['date'].dt.to_period('M')
            else:
                print("不支持的报告周期")
                return
            
            # 按周期统计
            period_stats = df.groupby('period').agg({
                'final_amount': ['sum', 'mean', 'count'],
                'quantity': 'sum'
            }).round(2)
            
            # 重命名列
            period_stats.columns = ['总销售额', '平均销售额', '订单数', '总销售量']
            
            print(period_stats.to_string())
            
        except ImportError:
            print("错误: 未安装pandas库，请运行 'pip install pandas'")
        except Exception as e:
            print(f"创建销售报告时发生错误: {e}")

# 使用销售分析系统
print("创建销售分析系统:")
sales_analyzer = SalesAnalyzer()

# 创建示例数据
print("\n创建示例销售数据:")
sales_df = sales_analyzer.create_sample_sales_data()

# 分析销售趋势
if sales_df is not None:
    sales_analyzer.analyze_sales_trends(sales_df)
    
    # 创建月度报告
    sales_analyzer.create_sales_report(sales_df, 'monthly')
    
    # 保存数据示例
    print("\n保存数据示例:")
    sales_analyzer.save_sales_data(sales_df.head(100), 'sample_sales.csv')
    sales_analyzer.save_sales_data(sales_df.head(100), 'sample_sales.json')

print("\n=== 数据分析最佳实践 ===")
print("1. 使用pandas处理结构化数据")
print("2. 使用numpy进行数值计算")
print("3. 合理处理缺失值和异常值")
print("4. 使用适当的数据类型节省内存")
print("5. 利用向量化操作提高性能")
print("6. 使用分组和聚合功能进行统计分析")
```

### 代码说明

**案例1代码解释**：
1. `np.random.normal(75, 10, 50)`：生成正态分布的随机数
2. `np.clip(scores, 0, 100)`：将数值限制在0-100范围内
3. `np.argsort(grades[subject])[::-1][:5]`：获取成绩排序后的索引，取前5名
4. `df[['数学', '英语', '科学']].corr()`：计算各科成绩的相关性

如果数据量很大，应该考虑使用pandas的chunksize参数分块读取数据。

**案例2代码解释**：
1. `pd.date_range('2023-01-01', '2023-12-31', freq='D')`：生成日期范围
2. `df.groupby('date')['final_amount'].sum()`：按日期分组汇总销售额
3. `df['date'].dt.to_period('M')`：将日期转换为月份周期
4. `df.groupby('period').agg({...})`：按周期进行多列聚合统计

如果处理非常大的数据集，应该考虑使用dask等分布式计算库。

## 4. matplotlib库 - 数据可视化

### 知识点解析

**概念定义**：matplotlib就像Python的"画笔和画布"，可以绘制各种图表，如折线图、柱状图、饼图等，让数据变得更加直观易懂。

**核心规则**：
1. 使用pyplot接口创建和定制图表
2. 合理设置图表标题、坐标轴标签和图例
3. 选择合适的图表类型展示数据
4. 控制图表样式和颜色

**常见易错点**：
1. 忘记调用plt.show()导致图表不显示
2. 图表元素重叠导致难以阅读
3. 颜色选择不当导致视觉效果差
4. 不保存图表导致工作丢失

### 实战案例

#### 案例1：学生成绩可视化系统
```python
# 学生成绩可视化系统
print("===学生成绩可视化系统===")

import numpy as np
import math

class GradeVisualizer:
    """学生成绩可视化系统"""
    
    def __init__(self):
        """初始化成绩可视化系统"""
        print("学生成绩可视化系统已启动")
    
    def create_sample_grade_data(self):
        """创建示例成绩数据"""
        try:
            # 生成示例成绩数据
            np.random.seed(42)
            
            # 生成3个班级的成绩数据
            classes = ['一班', '二班', '三班']
            subjects = ['数学', '英语', '科学']
            
            # 每个班级40个学生
            data = {}
            for class_name in classes:
                class_data = {}
                for subject in subjects:
                    # 生成正态分布的成绩数据
                    mean_score = np.random.uniform(70, 85)  # 随机均值
                    scores = np.random.normal(mean_score, 8, 40)  # 生成40个成绩
                    scores = np.clip(scores, 0, 100)  # 限制在0-100之间
                    class_data[subject] = scores
                data[class_name] = class_data
            
            print("示例成绩数据创建完成")
            return data, classes, subjects
            
        except Exception as e:
            print(f"创建示例成绩数据时发生错误: {e}")
            return None, None, None
    
    def plot_grade_distribution(self, data, classes, subjects):
        """
        绘制成绩分布图
        
        参数:
            data (dict): 成绩数据
            classes (list): 班级列表
            subjects (list): 科目列表
        """
        try:
            import matplotlib.pyplot as plt
            
            # 创建图表
            fig, axes = plt.subplots(2, 2, figsize=(15, 12))
            fig.suptitle('学生成绩分布分析', fontsize=16, fontweight='bold')
            
            # 1. 各科成绩箱线图
            axes[0, 0].set_title('各科成绩箱线图')
            all_scores = []
            labels = []
            
            for subject in subjects:
                for class_name in classes:
                    all_scores.append(data[class_name][subject])
                    labels.append(f'{class_name}\n{subject}')
            
            box_plot = axes[0, 0].boxplot(all_scores, labels=labels, patch_artist=True)
            
            # 设置箱线图颜色
            colors = ['lightblue', 'lightgreen', 'lightcoral']
            for i, patch in enumerate(box_plot['boxes']):
                patch.set_facecolor(colors[i % 3])
            
            axes[0, 0].tick_params(axis='x', rotation=45)
            axes[0, 0].set_ylabel('成绩')
            axes[0, 0].grid(True, alpha=0.3)
            
            # 2. 班级平均分对比
            axes[0, 1].set_title('各班级平均分对比')
            class_averages = []
            
            for class_name in classes:
                class_avg = np.mean([np.mean(data[class_name][subject]) for subject in subjects])
                class_averages.append(class_avg)
            
            bars = axes[0, 1].bar(classes, class_averages, color=['skyblue', 'lightgreen', 'salmon'])
            axes[0, 1].set_ylabel('平均分')
            axes[0, 1].set_ylim(0, 100)
            
            # 在柱状图上显示数值
            for bar, avg in zip(bars, class_averages):
                height = bar.get_height()
                axes[0, 1].text(bar.get_x() + bar.get_width()/2., height,
                               f'{avg:.1f}', ha='center', va='bottom')
            
            axes[0, 1].grid(True, alpha=0.3)
            
            # 3. 成绩分布直方图
            axes[1, 0].set_title('成绩分布直方图（所有学生）')
            all_students_scores = []
            for class_name in classes:
                for subject in subjects:
                    all_students_scores.extend(data[class_name][subject])
            
            axes[1, 0].hist(all_students_scores, bins=20, color='gold', alpha=0.7, edgecolor='black')
            axes[1, 0].set_xlabel('成绩')
            axes[1, 0].set_ylabel('学生人数')
            axes[1, 0].set_xlim(0, 100)
            axes[1, 0].grid(True, alpha=0.3)
            
            # 4. 各科成绩雷达图
            axes[1, 1].set_title('各科成绩雷达图')
            angles = np.linspace(0, 2 * np.pi, len(subjects), endpoint=False).tolist()
            angles += angles[:1]  # 闭合图形
            
            ax_radar = plt.subplot(2, 2, 4, projection='polar')
            
            for i, class_name in enumerate(classes):
                values = [np.mean(data[class_name][subject]) for subject in subjects]
                values += values[:1]  # 闭合图形
                
                colors_radar = ['blue', 'green', 'red']
                ax_radar.plot(angles, values, 'o-', linewidth=2, label=class_name, color=colors_radar[i])
                ax_radar.fill(angles, values, alpha=0.25, color=colors_radar[i])
            
            ax_radar.set_xticks(angles[:-1])
            ax_radar.set_xticklabels(subjects)
            ax_radar.set_ylim(0, 100)
            ax_radar.legend(loc='upper right', bbox_to_anchor=(1.3, 1.0))
            
            plt.tight_layout()
            plt.savefig('grade_analysis.png', dpi=300, bbox_inches='tight')
            print("成绩分布图已保存为 grade_analysis.png")
            
            # 为了在教学环境中正常运行，我们不显示图表
            plt.close()
            
        except ImportError:
            print("错误: 未安装matplotlib库，请运行 'pip install matplotlib'")
        except Exception as e:
            print(f"绘制成绩分布图时发生错误: {e}")
    
    def plot_subject_trends(self, data, classes, subjects):
        """
        绘制科目趋势图
        
        参数:
            data (dict): 成绩数据
            classes (list): 班级列表
            subjects (list): 科目列表
        """
        try:
            import matplotlib.pyplot as plt
            
            # 创建图表
            plt.figure(figsize=(12, 8))
            
            # 计算每个科目各班级的平均分
            x = np.arange(len(subjects))
            width = 0.25
            
            for i, class_name in enumerate(classes):
                averages = [np.mean(data[class_name][subject]) for subject in subjects]
                plt.bar(x + i * width, averages, width, label=class_name)
            
            plt.xlabel('科目')
            plt.ylabel('平均分')
            plt.title('各班级科目成绩对比')
            plt.xticks(x + width, subjects)
            plt.legend()
            plt.ylim(0, 100)
            plt.grid(True, alpha=0.3)
            
            # 添加数值标签
            for i, class_name in enumerate(classes):
                averages = [np.mean(data[class_name][subject]) for subject in subjects]
                for j, avg in enumerate(averages):
                    plt.text(j + i * width, avg + 1, f'{avg:.1f}', 
                            ha='center', va='bottom', fontsize=9)
            
            plt.tight_layout()
            plt.savefig('subject_trends.png', dpi=300, bbox_inches='tight')
            print("科目趋势图已保存为 subject_trends.png")
            
            # 为了在教学环境中正常运行，我们不显示图表
            plt.close()
            
        except ImportError:
            print("错误: 未安装matplotlib库，请运行 'pip install matplotlib'")
        except Exception as e:
            print(f"绘制科目趋势图时发生错误: {e}")
    
    def plot_grade_statistics(self, data, classes, subjects):
        """
        绘制成绩统计图
        
        参数:
            data (dict): 成绩数据
            classes (list): 班级列表
            subjects (list): 科目列表
        """
        try:
            import matplotlib.pyplot as plt
            
            # 创建饼图显示各等级人数
            plt.figure(figsize=(15, 5))
            
            # 计算各等级人数
            grade_labels = ['优秀(90-100)', '良好(80-89)', '中等(70-79)', '及格(60-69)', '不及格(0-59)']
            
            for i, class_name in enumerate(classes):
                plt.subplot(1, 3, i+1)
                
                # 合并所有科目的成绩
                all_scores = []
                for subject in subjects:
                    all_scores.extend(data[class_name][subject])
                
                # 统计各等级人数
                grades_count = [0, 0, 0, 0, 0]
                for score in all_scores:
                    if score >= 90:
                        grades_count[0] += 1
                    elif score >= 80:
                        grades_count[1] += 1
                    elif score >= 70:
                        grades_count[2] += 1
                    elif score >= 60:
                        grades_count[3] += 1
                    else:
                        grades_count[4] += 1
                
                # 绘制饼图
                colors = ['gold', 'yellowgreen', 'lightcoral', 'lightskyblue', 'lightpink']
                plt.pie(grades_count, labels=grade_labels, autopct='%1.1f%%', colors=colors)
                plt.title(f'{class_name}成绩等级分布')
            
            plt.tight_layout()
            plt.savefig('grade_statistics.png', dpi=300, bbox_inches='tight')
            print("成绩统计图已保存为 grade_statistics.png")
            
            # 为了在教学环境中正常运行，我们不显示图表
            plt.close()
            
        except ImportError:
            print("错误: 未安装matplotlib库，请运行 'pip install matplotlib'")
        except Exception as e:
            print(f"绘制成绩统计图时发生错误: {e}")

# 使用成绩可视化系统
print("创建成绩可视化系统:")
visualizer = GradeVisualizer()

# 创建示例数据
data, classes, subjects = visualizer.create_sample_grade_data()

# 绘制各种图表
if data is not None:
    print("\n绘制成绩分布图:")
    visualizer.plot_grade_distribution(data, classes, subjects)
    
    print("\n绘制科目趋势图:")
    visualizer.plot_subject_trends(data, classes, subjects)
    
    print("\n绘制成绩统计图:")
    visualizer.plot_grade_statistics(data, classes, subjects)

print("\n=== 数据可视化最佳实践 ===")
print("1. 选择合适的图表类型")
print("2. 合理设置颜色和样式")
print("3. 添加必要的标题和标签")
print("4. 保持图表简洁清晰")
print("5. 保存重要图表以备使用")
```

#### 案例2：销售数据可视化系统
```python
# 销售数据可视化系统
print("\n===销售数据可视化系统===")

class SalesVisualizer:
    """销售数据可视化系统"""
    
    def __init__(self):
        """初始化销售可视化系统"""
        print("销售数据可视化系统已启动")
    
    def create_sample_sales_data(self):
        """创建示例销售数据"""
        try:
            # 生成示例销售数据
            months = ['1月', '2月', '3月', '4月', '5月', '6月',
                     '7月', '8月', '9月', '10月', '11月', '12月']
            
            # 不同产品的月销售额（单位：万元）
            products = {
                '笔记本电脑': [120, 135, 142, 158, 165, 178, 185, 192, 175, 168, 182, 210],
                '智能手机': [200, 220, 240, 260, 280, 300, 290, 280, 260, 240, 250, 270],
                '平板电脑': [80, 85, 90, 95, 100, 110, 105, 100, 95, 90, 95, 105],
                '配件产品': [50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100, 110]
            }
            
            # 各地区销售额
            regions = {
                '华北': [450, 480, 510, 540, 570, 600, 580, 560, 540, 520, 530, 550],
                '华东': [600, 650, 700, 750, 800, 850, 820, 800, 780, 760, 770, 800],
                '华南': [350, 380, 410, 440, 470, 500, 480, 460, 440, 420, 430, 450]
            }
            
            print("示例销售数据创建完成")
            return months, products, regions
            
        except Exception as e:
            print(f"创建示例销售数据时发生错误: {e}")
            return None, None, None
    
    def plot_sales_trends(self, months, products):
        """
        绘制销售趋势图
        
        参数:
            months (list): 月份列表
            products (dict): 产品销售数据
        """
        try:
            import matplotlib.pyplot as plt
            
            # 创建折线图
            plt.figure(figsize=(14, 8))
            
            # 为不同产品设置不同颜色和线型
            colors = ['blue', 'red', 'green', 'orange']
            linestyles = ['-', '--', '-.', ':']
            
            for i, (product, sales) in enumerate(products.items()):
                plt.plot(months, sales, 
                        color=colors[i % len(colors)],
                        linestyle=linestyles[i % len(linestyles)],
                        marker='o',
                        linewidth=2,
                        markersize=6,
                        label=product)
                
                # 添加数据标签
                for j, (month, sale) in enumerate(zip(months, sales)):
                    plt.annotate(f'{sale}', 
                               (month, sale),
                               textcoords="offset points",
                               xytext=(0,10),
                               ha='center',
                               fontsize=8)
            
            plt.title('2023年各产品月销售额趋势', fontsize=16, fontweight='bold')
            plt.xlabel('月份')
            plt.ylabel('销售额 (万元)')
            plt.legend()
            plt.grid(True, alpha=0.3)
            
            # 旋转x轴标签以避免重叠
            plt.xticks(rotation=45)
            
            plt.tight_layout()
            plt.savefig('sales_trends.png', dpi=300, bbox_inches='tight')
            print("销售趋势图已保存为 sales_trends.png")
            
            # 为了在教学环境中正常运行，我们不显示图表
            plt.close()
            
        except ImportError:
            print("错误: 未安装matplotlib库，请运行 'pip install matplotlib'")
        except Exception as e:
            print(f"绘制销售趋势图时发生错误: {e}")
    
    def plot_sales_composition(self, products):
        """
        绘制销售构成图
        
        参数:
            products (dict): 产品销售数据
        """
        try:
            import matplotlib.pyplot as plt
            
            # 创建子图
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
            
            # 1. 年度总销售额饼图
            total_sales = {product: sum(sales) for product, sales in products.items()}
            labels = list(total_sales.keys())
            sizes = list(total_sales.values())
            colors = ['gold', 'lightcoral', 'lightskyblue', 'lightgreen']
            
            ax1.pie(sizes, labels=labels, autopct='%1.1f%%', colors=colors, startangle=90)
            ax1.axis('equal')  # 确保饼图是圆形
            ax1.set_title('年度总销售额构成', fontsize=14, fontweight='bold')
            
            # 2. 年度总销售额柱状图
            bars = ax2.bar(labels, sizes, color=colors)
            ax2.set_title('年度总销售额对比', fontsize=14, fontweight='bold')
            ax2.set_ylabel('销售额 (万元)')
            ax2.grid(True, alpha=0.3)
            
            # 在柱状图上添加数值标签
            for bar, size in zip(bars, sizes):
                height = bar.get_height()
                ax2.text(bar.get_x() + bar.get_width()/2., height,
                        f'{size}万', ha='center', va='bottom')
            
            plt.tight_layout()
            plt.savefig('sales_composition.png', dpi=300, bbox_inches='tight')
            print("销售构成图已保存为 sales_composition.png")
            
            # 为了在教学环境中正常运行，我们不显示图表
            plt.close()
            
        except ImportError:
            print("错误: 未安装matplotlib库，请运行 'pip install matplotlib'")
        except Exception as e:
            print(f"绘制销售构成图时发生错误: {e}")
    
    def plot_regional_sales(self, months, regions):
        """
        绘制地区销售图
        
        参数:
            months (list): 月份列表
            regions (dict): 地区销售数据
        """
        try:
            import matplotlib.pyplot as plt
            
            # 创建堆叠柱状图
            plt.figure(figsize=(14, 8))
            
            # 准备数据
            x = np.arange(len(months))
            width = 0.6
            
            # 计算堆叠数据
            bottom = np.zeros(len(months))
            colors = ['skyblue', 'lightcoral', 'lightgreen']
            
            for i, (region, sales) in enumerate(regions.items()):
                plt.bar(x, sales, width, label=region, bottom=bottom, color=colors[i])
                bottom += np.array(sales)
            
            plt.xlabel('月份')
            plt.ylabel('销售额 (万元)')
            plt.title('各地区月销售额堆叠图', fontsize=16, fontweight='bold')
            plt.xticks(x, months, rotation=45)
            plt.legend()
            plt.grid(True, alpha=0.3)
            
            # 添加总销售额线
            total_sales = np.sum(list(regions.values()), axis=0)
            plt.plot(x, total_sales, color='black', marker='o', linewidth=2, label='总计')
            
            plt.tight_layout()
            plt.savefig('regional_sales.png', dpi=300, bbox_inches='tight')
            print("地区销售图已保存为 regional_sales.png")
            
            # 为了在教学环境中正常运行，我们不显示图表
            plt.close()
            
        except ImportError:
            print("错误: 未安装matplotlib库，请运行 'pip install matplotlib'")
        except Exception as e:
            print(f"绘制地区销售图时发生错误: {e}")
    
    def plot_sales_heatmap(self, months, products):
        """
        绘制销售热力图
        
        参数:
            months (list): 月份列表
            products (dict): 产品销售数据
        """
        try:
            import matplotlib.pyplot as plt
            
            # 创建热力图数据
            data = []
            product_names = list(products.keys())
            
            for product in product_names:
                data.append(products[product])
            
            # 创建热力图
            plt.figure(figsize=(12, 6))
            
            # 使用imshow创建热力图
            im = plt.imshow(data, cmap='YlOrRd', aspect='auto')
            
            # 设置坐标轴
            plt.xticks(np.arange(len(months)), months, rotation=45)
            plt.yticks(np.arange(len(product_names)), product_names)
            
            # 添加颜色条
            plt.colorbar(im, label='销售额 (万元)')
            
            # 在每个格子中添加数值
            for i in range(len(product_names)):
                for j in range(len(months)):
                    plt.text(j, i, f'{data[i][j]}',
                            ha="center", va="center", color="black", fontsize=8)
            
            plt.title('产品月销售额热力图', fontsize=16, fontweight='bold')
            plt.xlabel('月份')
            plt.ylabel('产品')
            
            plt.tight_layout()
            plt.savefig('sales_heatmap.png', dpi=300, bbox_inches='tight')
            print("销售热力图已保存为 sales_heatmap.png")
            
            # 为了在教学环境中正常运行，我们不显示图表
            plt.close()
            
        except ImportError:
            print("错误: 未安装matplotlib库，请运行 'pip install matplotlib'")
        except Exception as e:
            print(f"绘制销售热力图时发生错误: {e}")

# 使用销售可视化系统
print("创建销售可视化系统:")
sales_visualizer = SalesVisualizer()

# 创建示例数据
months, products, regions = sales_visualizer.create_sample_sales_data()

# 绘制各种销售图表
if months is not None and products is not None and regions is not None:
    print("\n绘制销售趋势图:")
    sales_visualizer.plot_sales_trends(months, products)
    
    print("\n绘制销售构成图:")
    sales_visualizer.plot_sales_composition(products)
    
    print("\n绘制地区销售图:")
    sales_visualizer.plot_regional_sales(months, regions)
    
    print("\n绘制销售热力图:")
    sales_visualizer.plot_sales_heatmap(months, products)

print("\n=== 数据可视化最佳实践 ===")
print("1. 选择合适的图表类型展示数据")
print("2. 合理使用颜色和样式")
print("3. 添加必要的标题、标签和图例")
print("4. 保持图表清晰易读")
print("5. 保存重要图表供后续使用")
```

### 代码说明

**案例1代码解释**：
1. `plt.subplots(2, 2, figsize=(15, 12))`：创建2x2的子图布局
2. `axes[0, 0].boxplot(all_scores, labels=labels)`：绘制箱线图
3. `axes[0, 1].bar(classes, class_averages, color=['skyblue', 'lightgreen', 'salmon'])`：绘制柱状图
4. `plt.subplot(2, 2, 4, projection='polar')`：创建极坐标子图用于雷达图

如果数据量很大，应该考虑使用seaborn等高级可视化库，或者对数据进行采样。

**案例2代码解释**：
1. `plt.plot(months, sales, marker='o', linewidth=2)`：绘制带标记的折线图
2. `ax1.pie(sizes, labels=labels, autopct='%1.1f%%')`：绘制饼图并显示百分比
3. `plt.bar(x, sales, width, label=region, bottom=bottom)`：绘制堆叠柱状图
4. `plt.imshow(data, cmap='YlOrRd', aspect='auto')`：创建热力图

如果需要交互式图表，可以考虑使用plotly等库替代matplotlib。

这些实战案例展示了Python第三方库在实际项目中的应用，包括依赖管理、网络请求、数据处理和可视化等方面。通过这些例子，可以更好地理解如何在实际开发中使用这些强大的工具来解决具体问题。