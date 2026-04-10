# MCP 安全与认证示例代码

"""
MCP安全与认证示例代码
展示认证、权限、加密和审计实现
"""

import json
import time
import hashlib
import os
from typing import Any, Optional


# ============================================================
# 1. 认证机制
# ============================================================


class AuthManager:
    """认证管理器"""
    
    def __init__(self):
        self.users = {}
        self.sessions = {}
        self.api_keys = {}
        print("🔐 认证管理器已初始化")
    
    def register_user(self, username: str, password: str, role: str = "user") -> bool:
        """注册用户"""
        if username in self.users:
            print(f"✗ 用户已存在: {username}")
            return False
        
        # 密码哈希
        password_hash = self._hash_password(password)
        
        self.users[username] = {
            "password_hash": password_hash,
            "role": role,
            "created_at": time.time()
        }
        
        print(f"✓ 注册用户: {username} (role: {role})")
        return True
    
    def login(self, username: str, password: str) -> Optional[str]:
        """登录"""
        if username not in self.users:
            return None
        
        password_hash = self._hash_password(password)
        
        if self.users[username]["password_hash"] != password_hash:
            return None
        
        # 创建会话
        session_id = self._generate_session_id(username)
        
        self.sessions[session_id] = {
            "username": username,
            "created_at": time.time()
        }
        
        print(f"✓ 用户登录: {username}")
        return session_id
    
    def logout(self, session_id: str):
        """登出"""
        if session_id in self.sessions:
            username = self.sessions[session_id]["username"]
            del self.sessions[session_id]
            print(f"✓ 用户登出: {username}")
    
    def verify_session(self, session_id: str) -> Optional[str]:
        """验证会话"""
        if session_id not in self.sessions:
            return None
        
        session = self.sessions[session_id]
        
        # 会话有效期 1小时
        if time.time() - session["created_at"] > 3600:
            del self.sessions[session_id]
            return None
        
        return session["username"]
    
    def generate_api_key(self, username: str) -> Optional[str]:
        """生成API密钥"""
        if username not in self.users:
            return None
        
        api_key = f"mcp_{username}_{os.urandom(16).hex()}"
        
        self.api_keys[api_key] = {
            "username": username,
            "created_at": time.time()
        }
        
        return api_key
    
    def verify_api_key(self, api_key: str) -> Optional[str]:
        """验证API密钥"""
        if api_key not in self.api_keys:
            return None
        
        return self.api_keys[api_key]["username"]
    
    def _hash_password(self, password: str) -> str:
        """密码哈希"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def _generate_session_id(self, username: str) -> str:
        """生成会话ID"""
        return hashlib.sha256(
            f"{username}{time.time()}{os.urandom(8)}".encode()
        ).hexdigest()


def test_auth():
    """测试认证"""
    print("\n" + "=" * 50)
    print("示例1: 认证机制")
    print("=" * 50)
    
    auth = AuthManager()
    
    # 注册用户
    auth.register_user("admin", "admin123", "admin")
    auth.register_user("user1", "user123", "user")
    
    # 登录
    session = auth.login("user1", "user123")
    print(f"会话ID: {session[:16]}...")
    
    # 验证会话
    username = auth.verify_session(session)
    print(f"验证结果: {username}")
    
    # 生成API密钥
    api_key = auth.generate_api_key("user1")
    print(f"API密钥: {api_key[:20]}...")
    
    # 验证API密钥
    username = auth.verify_api_key(api_key)
    print(f"API验证结果: {username}")


# ============================================================
# 2. 权限控制
# ============================================================


class Permission:
    """权限"""
    
    def __init__(self, resource: str, action: str):
        self.resource = resource
        self.action = action
    
    def __str__(self):
        return f"{self.resource}:{self.action}"
    
    def matches(self, resource: str, action: str) -> bool:
        """检查是否匹配"""
        if self.resource == "*" or self.resource == resource:
            if self.action == "*" or self.action == action:
                return True
        return False


class Role:
    """角色"""
    
    def __init__(self, name: str, permissions: list = None):
        self.name = name
        self.permissions = permissions or []
    
    def add_permission(self, permission: Permission):
        self.permissions.append(permission)
    
    def has_permission(self, resource: str, action: str) -> bool:
        for perm in self.permissions:
            if perm.matches(resource, action):
                return True
        return False


class PermissionManager:
    """权限管理器"""
    
    def __init__(self):
        self.roles = {}
        self.user_roles = {}
        self._init_default_roles()
    
    def _init_default_roles(self):
        """初始化默认角色"""
        # 管理员 - 所有权限
        admin = Role("admin")
        admin.add_permission(Permission("*", "*"))
        
        # 普通用户 - 读写权限
        user = Role("user")
        user.add_permission(Permission("file", "read"))
        user.add_permission(Permission("file", "write"))
        user.add_permission(Permission("tool", "execute"))
        
        # 访客 - 只读权限
        guest = Role("guest")
        guest.add_permission(Permission("file", "read"))
        
        self.roles = {
            "admin": admin,
            "user": user,
            "guest": guest
        }
    
    def assign_role(self, username: str, role_name: str):
        """分配角色"""
        if role_name not in self.roles:
            print(f"✗ 角色不存在: {role_name}")
            return
        
        if username not in self.user_roles:
            self.user_roles[username] = []
        
        if role_name not in self.user_roles[username]:
            self.user_roles[username].append(role_name)
            print(f"✓ 分配角色: {username} -> {role_name}")
    
    def check_permission(self, username: str, resource: str, action: str) -> bool:
        """检查权限"""
        roles = self.user_roles.get(username, ["guest"])
        
        for role_name in roles:
            role = self.roles.get(role_name)
            if role and role.has_permission(resource, action):
                return True
        
        return False


def test_permissions():
    """测试权限"""
    print("\n" + "=" * 50)
    print("示例2: 权限控制")
    print("=" * 50)
    
    pm = PermissionManager()
    
    # 分配角色
    pm.assign_role("admin", "admin")
    pm.assign_role("user1", "user")
    pm.assign_role("guest1", "guest")
    
    # 权限检查
    print("\n权限检查:")
    tests = [
        ("admin", "file", "write"),
        ("admin", "system", "config"),
        ("user1", "file", "write"),
        ("user1", "system", "config"),
        ("guest1", "file", "read"),
        ("guest1", "file", "write")
    ]
    
    for username, resource, action in tests:
        result = pm.check_permission(username, resource, action)
        print(f"  {username} -> {resource}:{action} : {'✓' if result else '✗'}")


# ============================================================
# 3. 审计日志
# ============================================================


class AuditLogger:
    """审计日志"""
    
    def __init__(self, log_file: str = "audit.log"):
        self.log_file = log_file
        self.entries = []
    
    def log(self, username: str, action: str, details: dict):
        """记录日志"""
        entry = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "timestamp_unix": time.time(),
            "username": username,
            "action": action,
            "details": details,
            "ip_address": "127.0.0.1"  # 简化
        }
        
        self.entries.append(entry)
        
        # 写入文件
        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
        
        print(f"📝 审计: {username} - {action}")
    
    def get_logs(self, limit: int = 100) -> list:
        """获取日志"""
        return self.entries[-limit:]
    
    def search_logs(self, username: str = None, action: str = None) -> list:
        """搜索日志"""
        results = []
        
        for entry in self.entries:
            if username and entry.get("username") != username:
                continue
            if action and entry.get("action") != action:
                continue
            results.append(entry)
        
        return results
    
    def get_stats(self) -> dict:
        """获取统计"""
        if not self.entries:
            return {"total": 0}
        
        action_counts = {}
        
        for entry in self.entries:
            action = entry.get("action", "unknown")
            action_counts[action] = action_counts.get(action, 0) + 1
        
        return {
            "total": len(self.entries),
            "by_action": action_counts
        }


def test_audit():
    """测试审计"""
    print("\n" + "=" * 50)
    print("示例3: 审计日志")
    print("=" * 50)
    
    logger = AuditLogger()
    
    # 记录操作
    logger.log("admin", "login", {"method": "password"})
    logger.log("user1", "tool_execute", {"tool": "read_file", "path": "/data.txt"})
    logger.log("user1", "tool_execute", {"tool": "write_file", "path": "/output.txt"})
    logger.log("guest1", "login", {"method": "api_key"})
    
    # 获取统计
    stats = logger.get_stats()
    print(f"\n统计: {stats}")
    
    # 搜索日志
    print("\n用户user1的日志:")
    logs = logger.search_logs(username="user1")
    for log in logs:
        print(f"  [{log['timestamp']}] {log['action']} - {log['details']}")


# ============================================================
# 4. 数据加密
# ============================================================


class SimpleEncryption:
    """简单加密工具（用于演示）"""
    
    def __init__(self, key: str = None):
        # 简化实现 - 使用XOR加密演示
        self.key = key or "default_key"
    
    def encrypt(self, data: str) -> str:
        """加密"""
        key_bytes = self.key.encode()
        data_bytes = data.encode()
        
        result = bytearray()
        for i, byte in enumerate(data_bytes):
            result.append(byte ^ key_bytes[i % len(key_bytes)])
        
        import base64
        return base64.b64encode(bytes(result)).decode()
    
    def decrypt(self, encrypted_data: str) -> str:
        """解密"""
        import base64
        try:
            encrypted_bytes = base64.b64decode(encrypted_data.encode())
        except:
            return ""
        
        key_bytes = self.key.encode()
        
        result = bytearray()
        for i, byte in enumerate(encrypted_bytes):
            result.append(byte ^ key_bytes[i % len(key_bytes)])
        
        return bytes(result).decode()


class SecureMCPServer:
    """安全MCP服务器"""
    
    def __init__(self):
        self.auth = AuthManager()
        self.permissions = PermissionManager()
        self.audit = AuditLogger()
        self.encryption = SimpleEncryption()
    
    def handle_request(self, session_id: str, tool: str, params: dict) -> dict:
        """处理请求"""
        # 验证会话
        username = self.auth.verify_session(session_id)
        if not username:
            return {"error": "未授权", "code": 401}
        
        # 检查权限
        if not self.permissions.check_permission(username, "tool", tool):
            self.audit.log(username, "permission_denied", {"tool": tool})
            return {"error": "权限不足", "code": 403}
        
        # 执行操作
        try:
            result = {"success": True, "tool": tool, "params": params}
            
            # 记录审计
            self.audit.log(username, "tool_execute", {"tool": tool, "params": params})
            
            return result
            
        except Exception as e:
            self.audit.log(username, "tool_error", {"tool": tool, "error": str(e)})
            return {"error": str(e), "code": 500}


def test_encryption():
    """测试加密"""
    print("\n" + "=" * 50)
    print("示例4: 数据加密")
    print("=" * 50)
    
    enc = SimpleEncryption("my_secret_key")
    
    # 加密数据
    data = "敏感信息: 密码123456"
    encrypted = enc.encrypt(data)
    print(f"原文: {data}")
    print(f"加密: {encrypted}")
    
    # 解密数据
    decrypted = enc.decrypt(encrypted)
    print(f"解密: {decrypted}")


def test_secure_server():
    """测试安全服务器"""
    print("\n" + "=" * 50)
    print("示例5: 安全MCP服务器")
    print("=" * 50)
    
    server = SecureMCPServer()
    
    # 创建用户
    server.auth.register_user("admin", "admin123", "admin")
    server.auth.register_user("user1", "user123", "user")
    
    # 分配角色
    server.permissions.assign_role("admin", "admin")
    server.permissions.assign_role("user1", "user")
    
    # 登录
    session = server.auth.login("user1", "user123")
    
    # 模拟请求
    print("\n请求测试:")
    
    # 正常请求
    result = server.handle_request(session, "read_file", {"path": "/data.txt"})
    print(f"read_file: {result}")
    
    # 权限不足
    result = server.handle_request(session, "system_config", {"key": "value"})
    print(f"system_config: {result}")
    
    # 查看审计日志
    print("\n审计日志:")
    logs = server.audit.get_logs()
    for log in logs:
        print(f"  [{log['timestamp']}] {log['username']}: {log['action']}")


# ============================================================
# 主函数
# ============================================================

if __name__ == "__main__":
    print("=" * 60)
    print("MCP 安全与认证示例")
    print("=" * 60)
    
    test_auth()
    test_permissions()
    test_audit()
    test_encryption()
    test_secure_server()
    
    print("\n" + "=" * 60)
    print("所有示例完成!")
    print("=" * 60)
