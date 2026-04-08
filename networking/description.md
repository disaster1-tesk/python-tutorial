# Python 网络编程

## 1. Socket 编程基础

### 知识点解析

**概念定义**：Socket（套接字）是网络通信的端点，是操作系统提供的网络编程接口。可以把 Socket 想象成电话——一方拨号（connect），另一方接听（accept），然后双方通过电话线（连接）交换信息。

**核心概念**：
- **TCP（传输控制协议）**：面向连接、可靠传输、有顺序。像打电话——先建立连接，然后通话，最后挂断
- **UDP（用户数据报协议）**：无连接、不保证可靠、无顺序。像发短信——发出去就行，对方收不收到不确定
- **IP地址 + 端口号**：`192.168.1.100:8080`，IP 标识机器，端口标识进程

**核心规则**：
1. 服务端流程：`socket()` → `bind()` → `listen()` → `accept()` → `recv()/send()` → `close()`
2. 客户端流程：`socket()` → `connect()` → `send()/recv()` → `close()`
3. TCP 用 `socket.SOCK_STREAM`，UDP 用 `socket.SOCK_DGRAM`
4. 数据传输必须编码为 `bytes`：`data.encode()` 发送，`data.decode()` 接收
5. `recv(1024)` 中的 1024 是缓冲区大小，不是精确接收字节数

**常见易错点**：
1. 端口被占用：`Address already in use`，用 `SO_REUSEADDR` 选项复用地址
2. `recv()` 不会等待恰好接收指定字节——TCP 是流式协议，数据可能分多次到达
3. 阻塞模式下 `accept()` 和 `recv()` 会一直等待，需要设置超时 `settimeout()`
4. 忘记关闭 Socket 导致端口占用和资源泄漏

### 实战案例

#### 案例1：TCP 回声服务器与客户端
```python
# TCP 回声服务器
import socket
import threading
import time

print("===TCP 回声服务器===")

def start_tcp_server(host: str = "127.0.0.1", port: int = 9999) -> None:
    """启动TCP回声服务器（收到什么就返回什么）"""
    # 创建TCP Socket
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # 复用地址
    server.bind((host, port))
    server.listen(5)  # 最大等待连接数
    print(f"服务器启动: {host}:{port}")
    
    try:
        while True:
            client, addr = server.accept()  # 阻塞等待连接
            print(f"客户端连接: {addr}")
            
            # 每个客户端用独立线程处理
            thread = threading.Thread(target=handle_client, args=(client, addr), daemon=True)
            thread.start()
    except KeyboardInterrupt:
        print("\n服务器关闭")
    finally:
        server.close()

def handle_client(client: socket.socket, addr: tuple) -> None:
    """处理客户端请求"""
    try:
        while True:
            data = client.recv(1024)
            if not data:  # 客户端断开
                break
            message = data.decode("utf-8")
            print(f"[{addr}] 收到: {message}")
            
            # 回声：原样返回
            response = f"Echo: {message}"
            client.sendall(response.encode("utf-8"))
    except ConnectionResetError:
        pass
    finally:
        client.close()
        print(f"[{addr}] 断开连接")

# 简单的TCP客户端
def tcp_client(host: str = "127.0.0.1", port: int = 9999) -> None:
    """TCP客户端"""
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.settimeout(5.0)  # 5秒超时
    
    try:
        client.connect((host, port))
        print(f"已连接服务器: {host}:{port}")
        
        messages = ["你好", "Python网络编程", "再见"]
        for msg in messages:
            client.sendall(msg.encode("utf-8"))
            data = client.recv(1024)
            print(f"收到响应: {data.decode('utf-8')}")
            time.sleep(0.1)
    except socket.timeout:
        print("连接超时")
    finally:
        client.close()

# 注意：实际运行需要先启动服务器再启动客户端（在不同终端或线程中）
# 演示：单线程内先启动服务器再连接（仅供演示）
print("（以下为模拟演示，实际运行需分开服务器和客户端）")

# 线程方式：服务器在后台线程运行
def demo_tcp():
    server_thread = threading.Thread(target=start_tcp_server, daemon=True)
    server_thread.start()
    time.sleep(0.5)  # 等待服务器启动
    
    # 启动客户端
    tcp_client()

demo_tcp()
```

#### 案例2：UDP 通信
```python
# UDP 通信（无连接，不保证可靠）
import socket

print("\n===UDP 通信===")

def udp_server(host: str = "127.0.0.1", port: int = 8888) -> None:
    """UDP服务器"""
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server.bind((host, port))
    print(f"UDP服务器启动: {host}:{port}")
    
    try:
        while True:
            data, addr = server.recvfrom(1024)
            message = data.decode("utf-8")
            print(f"收到来自 {addr} 的数据: {message}")
            response = f"UDP回复: {message}"
            server.sendto(response.encode("utf-8"), addr)
    except KeyboardInterrupt:
        print("\nUDP服务器关闭")
    finally:
        server.close()

def udp_client(host: str = "127.0.0.1", port: int = 8888) -> None:
    """UDP客户端"""
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client.settimeout(3.0)
    
    messages = ["测试消息1", "测试消息2"]
    for msg in messages:
        client.sendto(msg.encode("utf-8"), (host, port))
        try:
            data, _ = client.recvfrom(1024)
            print(f"收到回复: {data.decode('utf-8')}")
        except socket.timeout:
            print(f"超时，'{msg}'可能未送达（UDP不保证可靠）")
    
    client.close()

# UDP 演示
def demo_udp():
    server_thread = threading.Thread(target=udp_server, daemon=True)
    server_thread.start()
    time.sleep(0.3)
    udp_client()

demo_udp()
```

### 代码说明

**案例1代码解释**：
1. `socket.SOCK_STREAM` 是 TCP 协议，`SOCK_DGRAM` 是 UDP 协议
2. `SO_REUSEADDR` 允许服务器在重启后立即绑定上次的端口（否则会报"地址已使用"）
3. `listen(5)` 设置最大等待连接队列长度（不是最大连接数）
4. `accept()` 返回元组 `(client_socket, client_address)`，每个连接用独立线程处理

**案例2代码解释**：
1. UDP 没有连接建立过程：服务器直接 `recvfrom` 等待数据，客户端直接 `sendto` 发送
2. `recvfrom()` 返回 `(data, address)`，address 是发送方地址，可直接用于回复
3. UDP 不保证可靠——发送的消息可能丢失，接收方也可能收不到

---

## 2. requests 库进阶

### 知识点解析

**概念定义**：`requests` 是 Python 最流行的 HTTP 库，比内置的 `urllib` 简洁得多。进阶用法包括 Session 会话管理、认证、超时控制、重试机制等。

**核心规则**：
1. `Session` 对象可以保持连接（连接池），跨请求保持 cookies 和 headers
2. 设置超时 `timeout=(connect_timeout, read_timeout)` 防止请求无限等待
3. 使用 `raise_for_status()` 检查 HTTP 状态码
4. 大文件下载用 `iter_content(chunk_size)` 流式读取
5. 安装：`pip install requests`

**常见易错点**：
1. 不设置超时导致程序永久挂起——**永远要设 timeout**
2. `Session` 忘记 `close()` 或不用 `with` 导致连接泄漏
3. 请求频率过高被限流——需要加延迟或使用重试+退避
4. 忽略 SSL 证书验证（`verify=False`）的安全风险

### 实战案例

#### 案例3：requests 进阶用法
```python
# requests 进阶用法
# 安装: pip install requests
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

print("===requests 进阶===")

# 1. 基础请求
try:
    resp = requests.get("https://httpbin.org/get", params={"key": "value"}, timeout=5)
    resp.raise_for_status()
    print(f"状态码: {resp.status_code}")
    print(f"响应JSON: {resp.json()}")
except requests.RequestException as e:
    print(f"请求失败: {e}")

# 2. Session：保持连接和cookies
print("\n===Session 用法===")
session = requests.Session()

# 设置请求头（所有请求自动携带）
session.headers.update({"User-Agent": "MyApp/1.0", "Accept-Language": "zh-CN"})

# 设置超时（默认值）
session.timeout = 10

# 设置重试策略
retry_strategy = Retry(
    total=3,              # 最大重试次数
    backoff_factor=0.5,   # 退避因子：0.5s, 1s, 2s
    status_forcelist=[500, 502, 503, 504],  # 哪些状态码重试
)
adapter = HTTPAdapter(max_retries=retry_strategy)
session.mount("https://", adapter)
session.mount("http://", adapter)

try:
    # 第一次请求设置cookie
    resp1 = session.get("https://httpbin.org/cookies/set", params={"mycookie": "hello"}, timeout=5)
    # 第二次请求自动携带cookie
    resp2 = session.get("https://httpbin.org/cookies", timeout=5)
    print(f"Cookies: {resp2.json()}")
except requests.RequestException as e:
    print(f"Session请求失败: {e}")
finally:
    session.close()

# 3. POST请求与JSON处理
print("\n===POST与JSON===")
try:
    resp = requests.post(
        "https://httpbin.org/post",
        json={"name": "张三", "age": 25},  # 自动设置 Content-Type 和序列化
        timeout=5,
    )
    result = resp.json()
    print(f"POST数据: {result['json']}")
except requests.RequestException as e:
    print(f"POST失败: {e}")
```

### 代码说明

**案例3代码解释**：
1. `Session` 对象在多次请求之间复用 TCP 连接（连接池），比每次创建新连接快很多
2. `session.headers.update()` 设置的全局 headers 会自动添加到每个请求
3. `Retry(backoff_factor=0.5)` 实现指数退避：第一次等0.5秒，第二次1秒，第三次2秒
4. `json={"key": "value"}` 自动序列化为 JSON 并设置 `Content-Type: application/json`

---

## 3. REST API 构建（Flask）

### 知识点解析

**概念定义**：REST（Representational State Transfer）是一种 API 设计风格。REST API 使用 HTTP 方法（GET/POST/PUT/DELETE）对资源（URL 路径）进行操作。Flask 是 Python 最轻量的 Web 框架。

**REST 设计规范**：
- `GET /users` → 获取用户列表
- `GET /users/1` → 获取ID为1的用户
- `POST /users` → 创建新用户
- `PUT /users/1` → 更新ID为1的用户
- `DELETE /users/1` → 删除ID为1的用户

### 实战案例

#### 案例4：Flask REST API
```python
# Flask REST API
# 安装: pip install flask

from flask import Flask, jsonify, request

print("===Flask REST API===")

app = Flask(__name__)

# 内存数据库（演示用）
users_db = {
    1: {"id": 1, "name": "张三", "email": "zhang@example.com"},
    2: {"id": 2, "name": "李四", "email": "li@example.com"},
}
next_id = 3

@app.route("/api/users", methods=["GET"])
def get_users():
    """GET /api/users - 获取所有用户"""
    return jsonify({"users": list(users_db.values())}), 200

@app.route("/api/users/<int:user_id>", methods=["GET"])
def get_user(user_id: int):
    """GET /api/users/<id> - 获取单个用户"""
    user = users_db.get(user_id)
    if not user:
        return jsonify({"error": "用户不存在"}), 404
    return jsonify(user), 200

@app.route("/api/users", methods=["POST"])
def create_user():
    """POST /api/users - 创建用户"""
    global next_id
    data = request.get_json()
    if not data or "name" not in data or "email" not in data:
        return jsonify({"error": "缺少必要字段: name, email"}), 400
    
    user = {"id": next_id, "name": data["name"], "email": data["email"]}
    users_db[next_id] = user
    next_id += 1
    return jsonify(user), 201

@app.route("/api/users/<int:user_id>", methods=["PUT"])
def update_user(user_id: int):
    """PUT /api/users/<id> - 更新用户"""
    if user_id not in users_db:
        return jsonify({"error": "用户不存在"}), 404
    data = request.get_json()
    if not data:
        return jsonify({"error": "请求体不能为空"}), 400
    
    users_db[user_id].update(data)
    users_db[user_id]["id"] = user_id  # 防止id被覆盖
    return jsonify(users_db[user_id]), 200

@app.route("/api/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id: int):
    """DELETE /api/users/<id> - 删除用户"""
    if user_id not in users_db:
        return jsonify({"error": "用户不存在"}), 404
    deleted = users_db.pop(user_id)
    return jsonify({"message": "已删除", "user": deleted}), 200

# 错误处理
@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "资源不存在"}), 404

@app.errorhandler(500)
def server_error(e):
    return jsonify({"error": "服务器内部错误"}), 500

# 注意：实际运行用 app.run(debug=True)
# 以下用 Flask 测试客户端演示（不需要启动服务器）
print("\n使用Flask测试客户端演示:")
with app.test_client() as client:
    # GET all
    resp = client.get("/api/users")
    print(f"GET /api/users: {resp.get_json()}")
    
    # POST create
    resp = client.post("/api/users", json={"name": "王五", "email": "wang@example.com"})
    print(f"POST /api/users: {resp.get_json()}")
    
    # GET single
    resp = client.get("/api/users/1")
    print(f"GET /api/users/1: {resp.get_json()}")
    
    # PUT update
    resp = client.put("/api/users/1", json={"email": "zhang_new@example.com"})
    print(f"PUT /api/users/1: {resp.get_json()}")
    
    # DELETE
    resp = client.delete("/api/users/2")
    print(f"DELETE /api/users/2: {resp.get_json()}")
    
    # 404
    resp = client.get("/api/users/999")
    print(f"GET /api/users/999: {resp.status_code} {resp.get_json()}")
```

### 代码说明

1. `@app.route("/api/users", methods=["GET"])` 用装饰器将 URL 路径映射到 Python 函数
2. `jsonify()` 自动将 Python 字典转为 JSON 响应并设置 `Content-Type: application/json`
3. `request.get_json()` 从请求体解析 JSON 数据
4. `app.test_client()` 提供无需启动服务器的测试方式，单元测试时很方便
5. REST API 应返回适当的 HTTP 状态码：200成功、201创建、400请求错误、404未找到

---

## 4. 知识点小结

| 技术 | 适用场景 | 复杂度 |
|------|---------|--------|
| socket TCP | 自定义协议、实时通信、聊天室 | 高 |
| socket UDP | 视频流、游戏、广播 | 中 |
| requests | HTTP客户端、调用第三方API、爬虫 | 低 |
| Flask | 小型API、原型开发、微服务 | 低 |
| FastAPI | 高性能API、自动文档、异步支持 | 中 |

**安装命令**：
```bash
pip install requests          # HTTP客户端
pip install flask             # Web框架
pip install fastapi uvicorn   # 异步Web框架 + ASGI服务器
```

**最佳实践**：
1. HTTP请求永远设置 `timeout`，防止无限等待
2. 生产环境不要用 `verify=False` 忽略SSL证书
3. REST API 用名词路径 + HTTP方法，不用动词路径（`/get_user` 是不好的设计）
4. 用 `Session` 管理连接池和 cookies，比每次创建请求更高效
5. API 返回适当的 HTTP 状态码，前端根据状态码处理不同情况
