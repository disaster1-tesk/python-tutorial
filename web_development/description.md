# Python Web 开发

## 1. Flask 框架

### 知识点解析

**概念定义**：Flask 是一个轻量级的 Python Web 框架，遵循 WSGI 协议。它以简洁著称——核心只有路由和模板引擎，其他功能通过扩展实现（如 Flask-SQLAlchemy、Flask-Login）。

**核心概念**：
- **路由（Routing）**：将 URL 映射到 Python 函数，`@app.route('/path')`
- **请求与响应**：`request` 对象获取请求数据，函数返回值自动包装为 `Response`
- **模板引擎 Jinja2**：在 HTML 中嵌入 Python 变量和逻辑
- **蓝图（Blueprint）**：模块化组织大型应用
- **中间件与钩子**：`before_request`、`after_request`、`errorhandler`

**核心规则**：
1. Flask 应用 = `Flask(__name__)` 创建实例，`app.run()` 启动
2. 路由支持动态参数：`@app.route('/user/<int:id>')`
3. 请求方法通过 `methods=['GET', 'POST']` 指定
4. `render_template()` 渲染模板，`redirect()` 重定向，`jsonify()` 返回 JSON
5. `app.config` 管理配置，支持从环境变量和配置文件加载

**常见易错点**：
1. 忘记设置 `SECRET_KEY` 导致 session 和 CSRF 功能不可用
2. 模板中 `{{ }}` 是变量输出，`{% %}` 是逻辑控制，`{# #}` 是注释——不要混淆
3. 蓝图注册时注意 `url_prefix`，避免路由冲突
4. 表单提交注意 `request.form`（POST）vs `request.args`（GET查询参数）

### 实战案例

#### 案例1：Flask RESTful API
```python
from flask import Flask, jsonify, request
from functools import wraps

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key-2024'

# 模拟数据库
books_db = [
    {"id": 1, "title": "Python编程", "author": "张三", "price": 79.9},
    {"id": 2, "title": "Flask入门", "author": "李四", "price": 59.9},
]
next_id = 3

# ========== 中间件：API 认证 ==========
def require_api_key(f):
    """简单的 API Key 认证装饰器"""
    @wraps(f)
    def decorated(*args, **kwargs):
        api_key = request.headers.get('X-API-Key')
        if api_key != 'my-secret-key':
            return jsonify({"error": "无效的API Key"}), 401
        return f(*args, **kwargs)
    return decorated

# ========== 请求钩子 ==========
@app.before_request
def log_request():
    """每个请求前记录日志"""
    print(f"[请求] {request.method} {request.path}")

@app.after_request
def add_cors_headers(response):
    """每个响应后添加 CORS 头"""
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response

# ========== 错误处理 ==========
@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "资源不存在"}), 404

@app.errorhandler(500)
def server_error(e):
    return jsonify({"error": "服务器内部错误"}), 500

# ========== CRUD 路由 ==========
@app.route('/api/books', methods=['GET'])
def get_books():
    """获取书籍列表，支持分页和搜索"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    search = request.args.get('search', '').strip()

    result = books_db
    if search:
        result = [b for b in result if search.lower() in b['title'].lower()]

    start = (page - 1) * per_page
    end = start + per_page
    return jsonify({
        "data": result[start:end],
        "total": len(result),
        "page": page,
        "per_page": per_page
    })

@app.route('/api/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    """获取单本书籍"""
    book = next((b for b in books_db if b['id'] == book_id), None)
    if not book:
        return jsonify({"error": "书籍不存在"}), 404
    return jsonify(book)

@app.route('/api/books', methods=['POST'])
@require_api_key
def create_book():
    """创建新书籍"""
    data = request.get_json()
    if not data or 'title' not in data or 'author' not in data:
        return jsonify({"error": "title和author字段必填"}), 400

    global next_id
    book = {
        "id": next_id,
        "title": data['title'],
        "author": data['author'],
        "price": data.get('price', 0.0)
    }
    books_db.append(book)
    next_id += 1
    return jsonify(book), 201

@app.route('/api/books/<int:book_id>', methods=['PUT'])
@require_api_key
def update_book(book_id):
    """更新书籍"""
    book = next((b for b in books_db if b['id'] == book_id), None)
    if not book:
        return jsonify({"error": "书籍不存在"}), 404

    data = request.get_json()
    book.update({
        k: v for k, v in data.items()
        if k in ('title', 'author', 'price')
    })
    return jsonify(book)

@app.route('/api/books/<int:book_id>', methods=['DELETE'])
@require_api_key
def delete_book(book_id):
    """删除书籍"""
    global books_db
    books_db = [b for b in books_db if b['id'] != book_id]
    return jsonify({"message": "删除成功"}), 200

# if __name__ == '__main__':
#     app.run(debug=True, port=5000)
```

#### 案例2：Flask 蓝图与模板渲染
```python
from flask import Flask, render_template, Blueprint

app = Flask(__name__, template_folder='templates')

# ====== 创建蓝图 ======
user_bp = Blueprint('user', __name__, url_prefix='/user')
api_bp = Blueprint('api', __name__, url_prefix='/api/v1')

@user_bp.route('/profile/<username>')
def profile(username):
    """用户主页"""
    return render_template('profile.html', username=username)

@user_bp.route('/settings')
def settings():
    """用户设置页"""
    return render_template('settings.html')

@api_bp.route('/status')
def status():
    """API 健康检查"""
    return {"status": "ok", "version": "1.0"}

# 注册蓝图
app.register_blueprint(user_bp)
app.register_blueprint(api_bp)
```

---

## 2. FastAPI 框架

### 知识点解析

**概念定义**：FastAPI 是一个现代、高性能的 Web 框架，基于 Starlette（异步）+ Pydantic（数据验证）+ OpenAPI（自动文档）。它是目前 Python Web 开发中最受欢迎的新框架之一。

**核心概念**：
- **路径操作装饰器**：`@app.get()`、`@app.post()` 等替代 Flask 的 `@app.route(methods=...)`
- **Pydantic 模型**：自动请求体验证和响应序列化
- **依赖注入**：`Depends()` 实现优雅的依赖管理
- **自动文档**：Swagger UI（`/docs`）和 ReDoc（`/redoc`）自动生成
- **异步支持**：原生 async/await，天然支持高并发

**核心规则**：
1. 使用 `BaseModel` 定义请求/响应 schema，自动完成数据校验
2. 路径参数 `<param>` 和查询参数（函数参数默认值）自动区分
3. `status_code` 指定响应状态码，`response_model` 指定响应格式
4. `Depends()` 实现数据库连接、认证等横切关注点
5. `HTTPException` 抛出 HTTP 错误，自定义异常处理器统一错误格式

**常见易错点**：
1. Pydantic V2 与 V1 语法不同：`@validator` → `@field_validator`，`@root_validator` → `@model_validator`
2. 异步路由中不能调用同步阻塞函数，需用 `run_in_threadpool`
3. `Form()` 接收表单数据，`File()` 接收文件，`Body()` 接收 JSON——根据场景选择
4. CORS 需要显式配置 `CORSMiddleware`

### 实战案例

#### 案例1：FastAPI 完整 CRUD
```python
from fastapi import FastAPI, HTTPException, Depends, Query, Path
from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import datetime
import uvicorn

app = FastAPI(
    title="书籍管理API",
    description="基于FastAPI的RESTful CRUD示例",
    version="1.0.0"
)

# ========== Pydantic 模型 ==========
class BookCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200, description="书名")
    author: str = Field(..., min_length=1, max_length=100, description="作者")
    price: float = Field(default=0.0, ge=0, description="价格")
    isbn: Optional[str] = Field(default=None, pattern=r'^\d{13}$', description="ISBN")

    @field_validator('title')
    @classmethod
    def title_must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError('书名不能为空')
        return v.strip()

class BookResponse(BookCreate):
    id: int
    created_at: datetime

    model_config = {"from_attributes": True}

class PaginatedResponse(BaseModel):
    data: list[BookResponse]
    total: int
    page: int
    per_page: int

# ========== 模拟数据库 ==========
books_db: list[dict] = []
next_id_counter = 1

# ========== 依赖注入 ==========
def get_db_session():
    """模拟数据库会话"""
    print("数据库连接已打开")
    try:
        yield {}
    finally:
        print("数据库连接已关闭")

def common_params(
    page: int = Query(1, ge=1, description="页码"),
    per_page: int = Query(10, ge=1, le=100, description="每页数量")
):
    """通用分页参数"""
    return {"page": page, "per_page": per_page}

# ========== CRUD 端点 ==========
@app.post("/api/books", response_model=BookResponse, status_code=201)
async def create_book(book: BookCreate):
    """创建书籍"""
    global next_id_counter
    new_book = {
        **book.model_dump(),
        "id": next_id_counter,
        "created_at": datetime.now()
    }
    books_db.append(new_book)
    next_id_counter += 1
    return new_book

@app.get("/api/books", response_model=PaginatedResponse)
async def get_books(params: dict = Depends(common_params)):
    """分页获取书籍列表"""
    page = params["page"]
    per_page = params["per_page"]
    start = (page - 1) * per_page
    end = start + per_page
    return {
        "data": books_db[start:end],
        "total": len(books_db),
        "page": page,
        "per_page": per_page
    }

@app.get("/api/books/{book_id}", response_model=BookResponse)
async def get_book(
    book_id: int = Path(..., ge=1, description="书籍ID")
):
    """获取单本书籍"""
    book = next((b for b in books_db if b["id"] == book_id), None)
    if not book:
        raise HTTPException(status_code=404, detail="书籍不存在")
    return book

@app.put("/api/books/{book_id}", response_model=BookResponse)
async def update_book(book_id: int, book: BookCreate):
    """更新书籍"""
    idx = next((i for i, b in enumerate(books_db) if b["id"] == book_id), None)
    if idx is None:
        raise HTTPException(status_code=404, detail="书籍不存在")
    books_db[idx].update(book.model_dump())
    return books_db[idx]

@app.delete("/api/books/{book_id}", status_code=204)
async def delete_book(book_id: int):
    """删除书籍"""
    global books_db
    original_len = len(books_db)
    books_db = [b for b in books_db if b["id"] != book_id]
    if len(books_db) == original_len:
        raise HTTPException(status_code=404, detail="书籍不存在")

# if __name__ == '__main__':
#     uvicorn.run(app, host="0.0.0.0", port=8000)
```

---

## 3. Django 框架（核心概念）

### 知识点解析

**概念定义**：Django 是一个"全栈式" Web 框架，提供 ORM、认证、管理后台、模板引擎等开箱即用的功能。遵循" batteries included"（自带电池）哲学。

**核心概念**：
- **MVT 架构**：Model（数据模型）+ View（视图逻辑）+ Template（模板），类似 MVC
- **ORM（对象关系映射）**：用 Python 类定义数据库表，无需写 SQL
- **Admin 后台**：自动生成管理界面，开箱即用
- **中间件（Middleware）**：请求/响应处理的钩子链
- **信号（Signals）**：模型事件的观察者模式

**核心规则**：
1. 项目 = `django-admin startproject`，应用 = `python manage.py startapp`
2. 模型字段类型对应数据库列：`CharField` → VARCHAR，`IntegerField` → INT
3. `QuerySet` 是惰性的——不会立即执行查询，直到真正需要数据
4. 视图可以用函数视图（FBV）或类视图（CBV），CBV 适合 REST 风格
5. `settings.py` 管理所有配置：数据库、中间件、模板、静态文件等

**常见易错点**：
1. 忘记在 `INSTALLED_APPS` 中注册新创建的应用
2. 修改模型后忘记 `python manage.py makemigrations` + `migrate`
3. `QuerySet.select_related()` 用于外键（一对一），`prefetch_related()` 用于多对多——别用反
4. 静态文件在开发模式由 Django 提供，生产环境需要 nginx 等处理

### 实战案例

#### 案例1：Django 模型与 ORM
```python
# models.py
from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    """分类模型"""
    name = models.CharField('分类名', max_length=100, unique=True)
    description = models.TextField('描述', blank=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)

    class Meta:
        verbose_name = '分类'
        verbose_name_plural = '分类'
        ordering = ['name']

    def __str__(self):
        return self.name

class Article(models.Model):
    """文章模型"""
    STATUS_CHOICES = [
        ('draft', '草稿'),
        ('published', '已发布'),
        ('archived', '已归档'),
    ]

    title = models.CharField('标题', max_length=200)
    content = models.TextField('内容')
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name='作者',
        related_name='articles'
    )
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True,
        verbose_name='分类', related_name='articles'
    )
    tags = models.ManyToManyField('Tag', blank=True, verbose_name='标签')
    status = models.CharField('状态', max_length=20, choices=STATUS_CHOICES, default='draft')
    view_count = models.PositiveIntegerField('浏览量', default=0)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        verbose_name = '文章'
        verbose_name_plural = '文章'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['status', '-created_at']),
        ]

    def __str__(self):
        return self.title

# ====== ORM 查询示例 ======
def orm_examples():
    """Django ORM 常用查询"""

    # 1. 基础查询
    all_articles = Article.objects.all()                     # 所有文章
    published = Article.objects.filter(status='published')    # 条件过滤
    article = Article.objects.get(id=1)                      # 获取单个（不存在会抛异常）
    first = Article.objects.first()                          # 第一个（不存在返回None）

    # 2. 链式查询
    result = (Article.objects
              .filter(status='published')
              .filter(category__name='Python')
              .order_by('-created_at')[:10])

    # 3. 字段查找
    titles_with_python = Article.objects.filter(title__icontains='python')
    recent = Article.objects.filter(created_at__gte='2024-01-01')

    # 4. 关联查询
    user_articles = Article.objects.filter(author__username='admin')
    articles_with_tags = Article.objects.filter(tags__name__in=['Python', 'Web'])

    # 5. 聚合与注解
    from django.db.models import Count, Avg, Max
    category_stats = Category.objects.annotate(
        article_count=Count('articles')
    ).values('name', 'article_count')

    avg_views = Article.objects.aggregate(avg=Avg('view_count'))

    # 6. 优化查询——避免 N+1 问题
    # 不好：会产生 N+1 次查询
    articles = Article.objects.all()  # 首次查询
    for a in articles:
        print(a.author.username)  # 每篇文章额外查一次

    # 好：一次 JOIN 查询
    articles = Article.objects.select_related('author', 'category').all()

    # 多对多预加载
    articles = Article.objects.prefetch_related('tags').all()

    # 7. 批量操作
    bulk_articles = [Article(title=f"文章{i}", author_id=1) for i in range(100)]
    Article.objects.bulk_create(bulk_articles)  # 一条INSERT

    Article.objects.filter(status='draft').update(status='archived')  # 批量更新
```

#### 案例2：Django 类视图
```python
# views.py
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import Article
from .forms import ArticleForm

class ArticleListView(ListView):
    """文章列表视图"""
    model = Article
    template_name = 'articles/article_list.html'
    context_object_name = 'articles'
    paginate_by = 10

    def get_queryset(self):
        """只显示已发布文章"""
        return Article.objects.filter(status='published').select_related('author', 'category')

class ArticleDetailView(DetailView):
    """文章详情视图"""
    model = Article
    template_name = 'articles/article_detail.html'

    def get_queryset(self):
        return Article.objects.select_related('author', 'category').prefetch_related('tags')

    def get_object(self):
        """每次访问增加浏览量"""
        obj = super().get_object()
        Article.objects.filter(id=obj.id).update(view_count=obj.view_count + 1)
        return obj

class ArticleCreateView(LoginRequiredMixin, CreateView):
    """创建文章视图"""
    model = Article
    form_class = ArticleForm
    template_name = 'articles/article_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
```

---

## 4. Web 全栈知识

### 4.1 WSGI 与 ASGI

**知识点解析**：

**WSGI（Web Server Gateway Interface）**：
- 同步协议，定义 Web 服务器与 Python 应用之间的接口
- Flask、Django（默认）都是 WSGI 框架
- 生产部署：Gunicorn（推荐）、uWSGI
- `environ` 字典包含请求信息，函数返回可迭代响应体

**ASGI（Asynchronous Server Gateway Interface）**：
- 异步协议，WSGI 的异步继任者
- 支持 WebSocket、HTTP/2、Server-Sent Events
- FastAPI、Starlette、Django 3.0+（可选）是 ASGI 框架
- 生产部署：Uvicorn、Daphne、Hypercorn

```python
# WSGI 应用示例
def simple_wsgi_app(environ, start_response):
    """最简单的 WSGI 应用"""
    path = environ['PATH_INFO']
    status = '200 OK'
    headers = [('Content-Type', 'text/plain; charset=utf-8')]
    start_response(status, headers)
    return [f"你访问了: {path}".encode('utf-8')]

# ASGI 应用示例
async def simple_asgi_app(scope, receive, send):
    """最简单的 ASGI 应用"""
    await send({
        'type': 'http.response.start',
        'status': 200,
        'headers': [(b'content-type', b'text/plain; charset=utf-8')],
    })
    await send({
        'type': 'http.response.body',
        'body': f"ASGI: 你访问了 {scope['path']}".encode('utf-8'),
    })
```

### 4.2 RESTful API 设计规范

**核心规则**：
1. **URL 用名词，表示资源**：`/users`、`/articles/123`
2. **HTTP 方法表示操作**：GET（查询）、POST（创建）、PUT（全量更新）、PATCH（部分更新）、DELETE（删除）
3. **状态码语义化**：200（成功）、201（创建成功）、204（删除成功）、400（请求错误）、401（未认证）、403（无权限）、404（不存在）、500（服务器错误）
4. **分页**：`GET /articles?page=1&per_page=20`
5. **过滤与排序**：`GET /articles?status=published&sort=-created_at`
6. **版本控制**：URL路径 `/api/v1/` 或 Header `Accept: application/vnd.api.v1+json`

### 4.3 认证与授权

```python
# JWT 认证流程（FastAPI 示例）
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
from datetime import datetime, timedelta

SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
security = HTTPBearer()

def create_access_token(data: dict, expires_delta: timedelta = timedelta(hours=24)):
    """生成 JWT Token"""
    to_encode = data.copy()
    to_encode.update({"exp": datetime.utcnow() + expires_delta})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """从 JWT Token 获取当前用户"""
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="无效的Token")
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token已过期")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="无效的Token")
    return {"username": username}

# 使用：在路由中注入依赖
@app.get("/me")
async def get_me(user=Depends(get_current_user)):
    return user
```

### 4.4 数据库迁移与 Alembic

```python
# Alembic 是 SQLAlchemy 的数据库迁移工具
# 常用命令：
# alembic init migrations          # 初始化迁移目录
# alembic revision --autogenerate  # 自动生成迁移脚本
# alembic upgrade head             # 执行迁移到最新版本
# alembic downgrade -1             # 回退一个版本
# alembic history                  # 查看迁移历史
```

### 4.5 部署与生产环境

**核心知识点**：
1. **反向代理**：Nginx 接收请求 → 转发到 Gunicorn/Uvicorn
2. **进程管理**：Systemd / Supervisor / Docker 管理应用进程
3. **环境配置**：`python-dotenv` 加载 `.env` 文件，敏感信息不入代码库
4. **HTTPS**：Let's Encrypt 免费证书，Nginx 配置 SSL
5. **日志**：结构化日志（JSON格式），ELK/Loki 日志收集
6. **健康检查**：`/health` 端点 + 容器健康检查
7. **Docker 部署**：

```dockerfile
# Dockerfile 示例
FROM python:3.12-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
EXPOSE 8000

# FastAPI
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--workers", "4"]

# Flask + Gunicorn
# CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:8000", "--workers", "4"]
```

### 4.6 WebSocket 实时通信

```python
# FastAPI WebSocket 聊天室示例
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from typing import List

app = FastAPI()

class ConnectionManager:
    """WebSocket 连接管理器"""
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()

@app.websocket("/ws/chat")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(f"用户: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast("有用户离开了聊天室")
```

---

## 5. 前端交互基础（Python 开发者视角）

### 知识点解析

**Python Web 开发者需要了解的前端知识**：

1. **HTML 基础**：表单（form）、输入类型、语义化标签
2. **CSS 基础**：Flexbox/Grid 布局、响应式设计（media query）
3. **JavaScript 基础**：fetch API 调用后端接口、DOM 操作、Promise/async-await
4. **模板引擎**：Jinja2 模板继承、条件渲染、循环、过滤器
5. **前后端分离**：后端只提供 API，前端（React/Vue/纯HTML）独立开发

```python
# Jinja2 模板继承示例
"""
# base.html（父模板）
<!DOCTYPE html>
<html>
<head><title>{% block title %}{% endblock %}</title></head>
<body>
    <nav>{% block nav %}{% endblock %}</nav>
    <main>{% block content %}{% endblock %}</main>
    <footer>{% block footer %}{% endblock %}</footer>
</body>
</html>

# article.html（子模板）
{% extends "base.html" %}
{% block title %}{{ article.title }}{% endblock %}
{% block content %}
    <h1>{{ article.title }}</h1>
    <p>{{ article.content|truncatewords:50 }}</p>
    {% if article.tags %}
        <div class="tags">
            {% for tag in article.tags %}
                <span class="tag">{{ tag.name }}</span>
            {% endfor %}
        </div>
    {% endif %}
{% endblock %}
"""
```

## 学习建议

1. **先 Flask 后 FastAPI**：Flask 帮助理解 Web 基本概念，FastAPI 适合现代 API 开发
2. **Django 适合大型项目**：需要快速搭建功能完善的后台管理系统时选择 Django
3. **重视 API 设计**：RESTful 规范不仅影响代码质量，也直接影响前端对接效率
4. **掌握部署**：Docker + Nginx + Gunicorn/Uvicorn 是 Python Web 部署的标准组合
5. **前后端分离趋势**：Flask/FastAPI + Vue/React 是当前主流架构，模板渲染逐渐减少
