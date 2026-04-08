"""
Python 网络编程完整示例
演示内容：
1. Socket TCP：回声服务器/客户端
2. Socket UDP：无连接通信
3. requests 进阶：Session、超时、重试、JSON
4. Flask REST API：CRUD操作、错误处理
5. API 设计规范与最佳实践
"""

import socket
import threading
import time
import json

print("=" * 60)
print("Python 网络编程完整示例")
print("=" * 60)

# ============================================================
# 1. Socket TCP 编程
# ============================================================
print("\n【1. Socket TCP 回声服务器】")


class EchoServer:
    """TCP回声服务器：收到什么就返回什么"""

    def __init__(self, host: str = "127.0.0.1", port: int = 9999):
        self.host = host
        self.port = port
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((host, port))
        self.server.listen(5)
        self.running = False

    def start(self) -> None:
        """启动服务器"""
        self.running = True
        print(f"TCP服务器启动: {self.host}:{self.port}")
        try:
            while self.running:
                try:
                    self.server.settimeout(1.0)
                    client, addr = self.server.accept()
                    print(f"  客户端连接: {addr}")
                    t = threading.Thread(
                        target=self._handle_client, args=(client, addr), daemon=True
                    )
                    t.start()
                except socket.timeout:
                    continue
        except KeyboardInterrupt:
            pass
        finally:
            self.server.close()
            print("TCP服务器关闭")

    def _handle_client(self, client: socket.socket, addr: tuple) -> None:
        """处理客户端请求"""
        try:
            while True:
                data = client.recv(1024)
                if not data:
                    break
                message = data.decode("utf-8")
                print(f"  [{addr[0]}:{addr[1]}] 收到: {message}")
                response = f"Echo: {message}"
                client.sendall(response.encode("utf-8"))
        except (ConnectionResetError, ConnectionAbortedError):
            pass
        finally:
            client.close()
            print(f"  [{addr[0]}:{addr[1]}] 断开")


class EchoClient:
    """TCP回声客户端"""

    def __init__(self, host: str = "127.0.0.1", port: int = 9999):
        self.host = host
        self.port = port

    def send_messages(self, messages: list[str]) -> list[str]:
        """发送多条消息并收集响应"""
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.settimeout(5.0)
        responses = []
        try:
            client.connect((self.host, self.port))
            for msg in messages:
                client.sendall(msg.encode("utf-8"))
                data = client.recv(1024)
                response = data.decode("utf-8")
                responses.append(response)
                print(f"  发送: {msg:20} <- {response}")
                time.sleep(0.05)
        except socket.timeout:
            print("  连接超时")
        finally:
            client.close()
        return responses


# 演示TCP通信
server = EchoServer(port=19876)
server_thread = threading.Thread(target=server.start, daemon=True)
server_thread.start()
time.sleep(0.3)

client = EchoClient(port=19876)
client.send_messages(["你好，服务器", "Python TCP", "测试完毕"])
print("  TCP通信演示结束")

# ============================================================
# 2. Socket UDP 编程
# ============================================================
print("\n【2. Socket UDP 通信】")


def udp_demo():
    """UDP 服务端 + 客户端演示"""

    class UDPServer:
        def __init__(self, host: str = "127.0.0.1", port: int = 19877):
            self.host = host
            self.port = port

        def run(self, count: int = 3) -> list:
            server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            server.bind((self.host, self.port))
            server.settimeout(3.0)
            messages = []
            for _ in range(count):
                try:
                    data, addr = server.recvfrom(1024)
                    msg = data.decode("utf-8")
                    messages.append(msg)
                    print(f"  服务端收到: {msg}（来自 {addr}）")
                    server.sendto(f"UDP-ACK: {msg}".encode(), addr)
                except socket.timeout:
                    break
            server.close()
            return messages

    # UDP 客户端
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client.settimeout(2.0)

    server = UDPServer()
    server_thread = threading.Thread(target=lambda: server.run(3), daemon=True)
    server_thread.start()
    time.sleep(0.2)

    for msg in ["UDP消息1", "UDP消息2", "UDP消息3"]:
        client.sendto(msg.encode("utf-8"), ("127.0.0.1", 19877))
        try:
            data, _ = client.recvfrom(1024)
            print(f"  客户端收到: {data.decode('utf-8')}")
        except socket.timeout:
            print(f"  客户端: '{msg}' 未收到回复（UDP不保证可靠）")

    client.close()


udp_demo()

# ============================================================
# 3. requests HTTP 客户端进阶
# ============================================================
print("\n【3. requests HTTP 客户端进阶】")

try:
    import requests
    from requests.adapters import HTTPAdapter
    from urllib3.util.retry import Retry

    # 1. 基础 GET 请求
    print("--- 基础GET ---")
    resp = requests.get(
        "https://httpbin.org/get",
        params={"key": "python", "page": 1},
        timeout=5,
    )
    resp.raise_for_status()
    print(f"  状态码: {resp.status_code}")
    print(f"  Content-Type: {resp.headers['content-type']}")
    data = resp.json()
    print(f"  请求参数: {data.get('args')}")

    # 2. Session 保持会话
    print("\n--- Session 会话管理 ---")
    session = requests.Session()

    # 配置重试策略
    retry = Retry(
        total=3,
        backoff_factor=0.5,
        status_forcelist=[500, 502, 503, 504],
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("https://", adapter)
    session.mount("http://", adapter)

    # 设置全局 headers
    session.headers.update({"X-App-Version": "1.0.0"})

    # 设置 cookies
    resp = session.get(
        "https://httpbin.org/cookies/set",
        params={"session_id": "abc123", "user": "zhang"},
        timeout=5,
    )

    # 后续请求自动携带 cookies
    resp = session.get("https://httpbin.org/cookies", timeout=5)
    cookies = resp.json().get("cookies", {})
    print(f"  Session携带的Cookies: {cookies}")

    # 3. POST JSON
    print("\n--- POST JSON ---")
    resp = requests.post(
        "https://httpbin.org/post",
        json={"name": "张三", "scores": [90, 85, 92]},
        headers={"Content-Type": "application/json"},
        timeout=5,
    )
    result = resp.json()
    print(f"  发送的JSON: {result.get('json')}")

    # 4. 错误处理
    print("\n--- 错误处理 ---")
    try:
        resp = requests.get("https://httpbin.org/status/404", timeout=5)
        resp.raise_for_status()  # 404 会抛异常
    except requests.exceptions.HTTPError as e:
        print(f"  HTTP错误: {e.response.status_code} {e.response.reason}")

    try:
        resp = requests.get("https://httpbin.org/delay/10", timeout=2)
    except requests.exceptions.Timeout:
        print(f"  请求超时（2秒内未响应）")

    try:
        resp = requests.get("https://nonexistent-domain-xyz123.com", timeout=3)
    except requests.exceptions.ConnectionError:
        print(f"  连接错误（域名不存在）")

    session.close()

except ImportError:
    print("  提示: pip install requests")

# ============================================================
# 4. Flask REST API
# ============================================================
print("\n【4. Flask REST API】")

try:
    from flask import Flask, jsonify, request as flask_request

    app = Flask(__name__)

    # 内存数据存储
    _todos = {
        1: {"id": 1, "title": "学习Python", "done": True},
        2: {"id": 2, "title": "学习网络编程", "done": False},
        3: {"id": 3, "title": "完成项目", "done": False},
    }
    _next_id = 4

    @app.route("/api/todos", methods=["GET"])
    def list_todos():
        """获取所有待办事项"""
        return jsonify({"todos": list(_todos.values())}), 200

    @app.route("/api/todos/<int:todo_id>", methods=["GET"])
    def get_todo(todo_id: int):
        """获取单个待办"""
        todo = _todos.get(todo_id)
        if not todo:
            return jsonify({"error": f"待办 {todo_id} 不存在"}), 404
        return jsonify(todo), 200

    @app.route("/api/todos", methods=["POST"])
    def create_todo():
        """创建待办"""
        global _next_id
        data = flask_request.get_json()
        if not data or "title" not in data:
            return jsonify({"error": "缺少 title 字段"}), 400
        todo = {
            "id": _next_id,
            "title": data["title"],
            "done": data.get("done", False),
        }
        _todos[_next_id] = todo
        _next_id += 1
        return jsonify(todo), 201

    @app.route("/api/todos/<int:todo_id>", methods=["PUT"])
    def update_todo(todo_id: int):
        """更新待办"""
        if todo_id not in _todos:
            return jsonify({"error": "不存在"}), 404
        data = flask_request.get_json()
        if not data:
            return jsonify({"error": "请求体不能为空"}), 400
        _todos[todo_id].update(data)
        _todos[todo_id]["id"] = todo_id
        return jsonify(_todos[todo_id]), 200

    @app.route("/api/todos/<int:todo_id>", methods=["DELETE"])
    def delete_todo(todo_id: int):
        """删除待办"""
        if todo_id not in _todos:
            return jsonify({"error": "不存在"}), 404
        deleted = _todos.pop(todo_id)
        return jsonify({"message": "已删除", "todo": deleted}), 200

    @app.errorhandler(404)
    def handle_404(e):
        return jsonify({"error": "资源不存在"}), 404

    @app.errorhandler(400)
    def handle_400(e):
        return jsonify({"error": "请求错误"}), 400

    # 用测试客户端演示（不需要启动真实服务器）
    print("--- REST API CRUD 演示 ---")
    with app.test_client() as tc:
        # GET all
        resp = tc.get("/api/todos")
        print(f"  GET /api/todos: {resp.get_json()}")

        # POST
        resp = tc.post("/api/todos", json={"title": "学习并发编程"})
        print(f"  POST 创建: {resp.get_json()} (状态码: {resp.status_code})")

        # GET single
        resp = tc.get("/api/todos/1")
        print(f"  GET /api/todos/1: {resp.get_json()}")

        # PUT
        resp = tc.put("/api/todos/2", json={"done": True})
        print(f"  PUT 更新: {resp.get_json()}")

        # DELETE
        resp = tc.delete("/api/todos/3")
        print(f"  DELETE 删除: {resp.get_json()}")

        # 404
        resp = tc.get("/api/todos/999")
        print(f"  GET /api/todos/999: {resp.status_code} {resp.get_json()}")

        # 错误请求
        resp = tc.post("/api/todos", json={"wrong_field": "value"})
        print(f"  POST 缺少字段: {resp.status_code} {resp.get_json()}")

except ImportError:
    print("  提示: pip install flask")

# ============================================================
# 5. 网络编程最佳实践总结
# ============================================================
print("\n【5. 最佳实践总结】")
tips = [
    "✓ Socket: 始终设置 SO_REUSEADDR，避免端口占用",
    "✓ Socket: 设置 settimeout()，防止永久阻塞",
    "✓ requests: 永远设置 timeout，避免请求挂起",
    "✓ requests: 用 Session 复用连接，减少TCP握手开销",
    "✓ requests: Retry + backoff_factor 实现指数退避重试",
    "✓ REST API: 用 HTTP方法语义化（GET读/POST写/PUT改/DELETE删）",
    "✓ REST API: 返回合适的状态码（200/201/400/404/500）",
    "✓ REST API: 用 JSON 统一响应格式，便于前端解析",
    "✓ 生产环境: HTTPS + 认证 + 限流 + 日志",
]
for tip in tips:
    print(f"  {tip}")
