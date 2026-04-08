"""
Python Web 开发完整示例
演示内容：
1. Flask：REST API、蓝图、中间件、模板
2. FastAPI：Pydantic模型、依赖注入、自动文档
3. Django：ORM查询、类视图
4. Web全栈：WSGI/ASGI、JWT认证、WebSocket、部署
"""

print("=" * 60)
print("Python Web 开发完整示例")
print("=" * 60)

# ============================================================
# 1. Flask 基础：模拟 REST API（不依赖Flask安装也能运行）
# ============================================================
print("\n【1. Flask 风格的请求路由模拟】")


class FlaskLikeRouter:
    """简化版 Flask 路由器——演示路由匹配原理"""

    def __init__(self):
        self.routes = {}

    def route(self, path, methods=None):
        """装饰器：注册路由"""
        if methods is None:
            methods = ['GET']

        def decorator(func):
            self.routes[(path, tuple(methods))] = func
            return func
        return decorator

    def handle_request(self, path, method='GET'):
        """模拟处理请求"""
        key = (path, tuple(method.split(',')))
        handler = self.routes.get(key)
        if handler:
            return {"status": 200, "data": handler()}
        return {"status": 404, "error": f"路由不存在: {method} {path}"}


app = FlaskLikeRouter()

# 模拟数据
books = [
    {"id": 1, "title": "Python编程", "author": "张三", "price": 79.9},
    {"id": 2, "title": "Web开发实战", "author": "李四", "price": 89.9},
]


@app.route('/api/books', 'GET')
def list_books():
    return books


@app.route('/api/books/2', 'GET')
def get_book():
    return books[1]


# 测试路由
print(f"  GET /api/books -> {app.handle_request('/api/books', 'GET')}")
print(f"  GET /api/books/2 -> {app.handle_request('/api/books/2', 'GET')}")
print(f"  DELETE /api/books/2 -> {app.handle_request('/api/books/2', 'DELETE')}")

# ============================================================
# 2. Pydantic 模型（数据验证核心）
# ============================================================
print("\n【2. Pydantic 风格的数据验证】")


class BookSchema:
    """模拟 Pydantic 的数据验证"""

    def __init__(self, title: str, author: str, price: float = 0.0):
        errors = []
        if not title or len(title) > 200:
            errors.append(f"title无效: 长度需在1-200之间")
        if not author or len(author) > 100:
            errors.append(f"author无效: 长度需在1-100之间")
        if price < 0:
            errors.append(f"price无效: 不能为负数")

        if errors:
            raise ValueError(f"数据验证失败: {errors}")

        self.title = title
        self.author = author
        self.price = price

    def to_dict(self):
        return {"title": self.title, "author": self.author, "price": self.price}


# 验证成功
book1 = BookSchema(title="深度学习", author="王五", price=99.9)
print(f"  验证通过: {book1.to_dict()}")

# 验证失败
try:
    BookSchema(title="", author="测试", price=-10)
except ValueError as e:
    print(f"  验证失败: {e}")

# ============================================================
# 3. Django ORM 风格查询（模拟）
# ============================================================
print("\n【3. Django ORM 风格查询模拟】")


class QuerySet:
    """模拟 Django QuerySet 的链式查询"""

    def __init__(self, data):
        self._data = list(data)

    def filter(self, **kwargs):
        """条件过滤"""
        result = self._data
        for key, value in kwargs.items():
            if key.endswith('__gte'):
                field = key[:-5]
                result = [item for item in result if item.get(field, 0) >= value]
            elif key.endswith('__lte'):
                field = key[:-5]
                result = [item for item in result if item.get(field, 0) <= value]
            elif key.endswith('__contains'):
                field = key[:-10]
                result = [item for item in result if value in str(item.get(field, ''))]
            else:
                result = [item for item in result if item.get(key) == value]
        return QuerySet(result)

    def order_by(self, field):
        """排序，-前缀表示降序"""
        reverse = field.startswith('-')
        key = field.lstrip('-')
        return QuerySet(sorted(self._data, key=lambda x: x.get(key, 0), reverse=reverse))

    def limit(self, n):
        return QuerySet(self._data[:n])

    def count(self):
        return len(self._data)

    def first(self):
        return self._data[0] if self._data else None

    def all(self):
        return self._data

    def values(self, *fields):
        if fields:
            return [{k: item[k] for k in fields if k in item} for item in self._data]
        return self._data


# 模拟文章数据
articles = [
    {"id": 1, "title": "Python入门", "author": "张三", "status": "published", "views": 1500},
    {"id": 2, "title": "Python高级", "author": "李四", "status": "published", "views": 2300},
    {"id": 3, "title": "Web开发", "author": "张三", "status": "draft", "views": 500},
    {"id": 4, "title": "数据分析", "author": "王五", "status": "published", "views": 3200},
    {"id": 5, "title": "机器学习", "author": "李四", "status": "archived", "views": 800},
]

qs = QuerySet(articles)

# 链式查询
result = qs.filter(status='published').order_by('-views').limit(2).all()
print(f"  已发布+按浏览量降序+前2条:")
for r in result:
    print(f"    {r['title']} (views={r['views']})")

# 关键词搜索
result2 = qs.filter(title__contains='Python').all()
print(f"  标题含Python: {[r['title'] for r in result2]}")

# 统计
count = qs.filter(status='published').count()
print(f"  已发布文章数: {count}")

# ============================================================
# 4. JWT Token（简化实现）
# ============================================================
print("\n【4. JWT Token 简化实现】")


import hashlib
import hmac
import json
import base64
import time


def base64url_encode(data: bytes) -> str:
    """Base64URL 编码"""
    return base64.urlsafe_b64encode(data).rstrip(b'=').decode('utf-8')


def create_jwt(payload: dict, secret: str) -> str:
    """创建简化版 JWT Token"""
    header = {"alg": "HS256", "typ": "JWT"}

    header_b64 = base64url_encode(json.dumps(header).encode())
    payload_b64 = base64url_encode(json.dumps(payload).encode())

    message = f"{header_b64}.{payload_b64}"
    signature = hmac.new(
        secret.encode(), message.encode(), hashlib.sha256
    ).digest()
    signature_b64 = base64url_encode(signature)

    return f"{message}.{signature_b64}"


def verify_jwt(token: str, secret: str) -> dict:
    """验证 JWT Token"""
    parts = token.split('.')
    if len(parts) != 3:
        raise ValueError("Token格式错误")

    header_b64, payload_b64, signature_b64 = parts
    message = f"{header_b64}.{payload_b64}"

    expected_sig = hmac.new(
        secret.encode(), message.encode(), hashlib.sha256
    ).digest()
    actual_sig = base64.urlsafe_b64decode(signature_b64 + '==')

    if not hmac.compare_digest(expected_sig, actual_sig):
        raise ValueError("签名验证失败")

    payload = json.loads(base64.urlsafe_b64decode(payload_b64 + '=='))

    if payload.get('exp', 0) < time.time():
        raise ValueError("Token已过期")

    return payload


# 创建 Token
SECRET = "my-super-secret-key-2024"
token = create_jwt(
    {"sub": "user123", "username": "张三", "exp": int(time.time()) + 3600},
    SECRET
)
print(f"  Token: {token[:50]}...")

# 验证 Token
payload = verify_jwt(token, SECRET)
print(f"  验证成功: username={payload['username']}")

# 篡改 Token
try:
    tampered = token[:-5] + "XXXXX"
    verify_jwt(tampered, SECRET)
except ValueError as e:
    print(f"  篡改检测: {e}")

# ============================================================
# 5. WebSocket 聊天室（模拟）
# ============================================================
print("\n【5. WebSocket 连接管理模拟】")


from collections import defaultdict


class ChatRoom:
    """模拟 WebSocket 聊天室"""

    def __init__(self):
        self.rooms: dict[str, list[str]] = defaultdict(list)  # room -> [usernames]
        self.message_history: list[dict] = []

    def join(self, room: str, username: str):
        if username not in self.rooms[room]:
            self.rooms[room].append(username)
            self.message_history.append({
                "type": "system",
                "room": room,
                "message": f"{username} 加入了 {room}"
            })
            print(f"  [{room}] {username} 加入 (当前 {len(self.rooms[room])} 人)")

    def leave(self, room: str, username: str):
        if username in self.rooms[room]:
            self.rooms[room].remove(username)
            self.message_history.append({
                "type": "system",
                "room": room,
                "message": f"{username} 离开了 {room}"
            })
            print(f"  [{room}] {username} 离开 (当前 {len(self.rooms[room])} 人)")

    def send_message(self, room: str, username: str, message: str):
        msg = {"type": "chat", "room": room, "from": username, "message": message}
        self.message_history.append(msg)
        for user in self.rooms[room]:
            if user != username:
                print(f"    → {room}/{user}: [{username}] {message}")
        return msg

    def get_history(self, room: str, limit: int = 10):
        return [
            m for m in self.message_history
            if m.get('room') == room
        ][-limit:]


chat = ChatRoom()
chat.join("Python", "Alice")
chat.join("Python", "Bob")
chat.join("Python", "Charlie")

chat.send_message("Python", "Alice", "大家好！")
chat.send_message("Python", "Bob", "欢迎 Alice！")

chat.leave("Python", "Charlie")

print(f"\n  消息历史:")
for msg in chat.get_history("Python"):
    print(f"    {msg}")

# ============================================================
# 6. 中间件管道
# ============================================================
print("\n【6. 中间件管道模式】")


class MiddlewarePipeline:
    """模拟 Web 框架的中间件处理管道"""

    def __init__(self):
        self.middlewares = []

    def use(self, middleware):
        """注册中间件"""
        self.middlewares.append(middleware)
        return self

    def process(self, request: dict) -> dict:
        """按顺序执行中间件链"""
        print(f"  → 收到请求: {request['method']} {request['path']}")

        for mw in self.middlewares:
            request = mw(request)
            if request.get('blocked'):
                print(f"  ✗ 请求被拦截: {request.get('error')}")
                return request

        print(f"  ✓ 请求通过所有中间件")
        return request


# 定义中间件
def logging_middleware(request):
    request.setdefault('log', []).append(f"{request['method']} {request['path']}")
    print(f"    [日志] 记录请求: {request['path']}")
    return request


def auth_middleware(request):
    token = request.get('headers', {}).get('Authorization', '')
    if not token:
        request['blocked'] = True
        request['error'] = '未提供认证Token'
    else:
        print(f"    [认证] Token验证通过")
    return request


def rate_limit_middleware(request):
    print(f"    [限流] 检查请求频率...")
    return request


def cors_middleware(request):
    request.setdefault('headers', {})['Access-Control-Allow-Origin'] = '*'
    print(f"    [CORS] 添加跨域头")
    return request


# 构建管道
pipeline = MiddlewarePipeline()
pipeline.use(cors_middleware)
pipeline.use(logging_middleware)
pipeline.use(rate_limit_middleware)
pipeline.use(auth_middleware)

# 带Token的请求
req1 = {"method": "GET", "path": "/api/users", "headers": {"Authorization": "Bearer abc123"}}
pipeline.process(req1)

# 不带Token的请求
req2 = {"method": "POST", "path": "/api/articles"}
pipeline.process(req2)

# ============================================================
# 7. REST API 设计规范检查
# ============================================================
print("\n【7. REST API 设计规范检查】")


api_rules = {
    "GET /api/users": "✓ 获取用户列表（名词 + GET）",
    "GET /api/users/123": "✓ 获取单个用户（名词 + ID）",
    "POST /api/users": "✓ 创建用户（名词 + POST）",
    "PUT /api/users/123": "✓ 更新用户（名词 + PUT）",
    "DELETE /api/users/123": "✓ 删除用户（名词 + DELETE）",
    "GET /api/getUsers": "✗ 不规范（URL中不应有动词）",
    "POST /api/users/create": "✗ 不规范（POST已表示创建）",
    "GET /api/user-list": "✗ 不规范（用连字符而非驼峰）",
}

for endpoint, rule in api_rules.items():
    status = "合规" if rule.startswith("✓") else "不合规"
    print(f"  {endpoint:25s} {rule}")

print("\n" + "=" * 60)
print("Web 开发示例运行完毕！")
print("=" * 60)
