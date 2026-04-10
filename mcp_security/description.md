# MCP 安全与认证

---

## 学习目标

完成本章节学习后，你将能够：

| 目标 | 描述 | 重要性 |
|------|------|--------|
| 理解安全需求 | 掌握MCP安全的基本概念 | ⭐⭐⭐ 必备 |
| 认证机制 | 实现MCP服务认证 | ⭐⭐⭐ 必备 |
| 权限控制 | 实现细粒度权限控制 | ⭐⭐⭐ 必备 |
| 审计日志 | 记录和审查操作日志 | ⭐⭐ 重要 |
| 数据加密 | 敏感数据加密处理 | ⭐⭐ 重要 |

---

## 章节概览

```
┌─────────────────────────────────────────────────────────┐
│                   MCP 安全与认证                          │
├─────────────────────────────────────────────────────────┤
│  1. 安全概述     │ MCP安全的基本概念和需求                │
│  2. 认证机制     │ 实现身份认证                          │
│  3. 权限控制     │ 实现访问权限控制                       │
│  4. 审计日志     │ 操作记录与审计                         │
│  5. 数据加密     │ 敏感数据保护                          │
└─────────────────────────────────────────────────────────┘
```

---

## 1. 安全概述

### 知识点解析

**MCP安全的重要性**：

MCP作为AI与外部系统交互的桥梁，涉及：
- 文件系统访问
- 数据库操作
- API调用
- 敏感数据处理

**安全威胁**：

1. **未授权访问**：未经授权使用工具
2. **数据泄露**：敏感信息泄露
3. **工具滥用**：恶意使用工具能力
4. **会话劫持**：会话被攻击者控制

---

## 2. 认证机制

### 知识点解析

**认证方式**：

| 方式 | 适用场景 | 安全性 |
|------|----------|--------|
| API密钥 | 简单场景 | 中等 |
| OAuth 2.0 | 企业应用 | 高 |
| JWT | 跨服务调用 | 高 |

**API密钥认证**：

```python
import os
import hmac
import hashlib


class AuthManager:
    """认证管理器"""
    
    def __init__(self):
        self.api_keys = {}
    
    def generate_key(self, user_id: str) -> str:
        """生成API密钥"""
        key = f"mcp_{user_id}_{os.urandom(16).hex()}"
        self.api_keys[key] = user_id
        return key
    
    def verify_key(self, key: str) -> bool:
        """验证API密钥"""
        return key in self.api_keys
    
    def revoke_key(self, key: str):
        """撤销API密钥"""
        if key in self.api_keys:
            del self.api_keys[key]
```

---

## 3. 权限控制

### 知识点解析

**权限模型**：

```python
class Permission:
    """权限定义"""
    
    def __init__(self, resource: str, action: str):
        self.resource = resource
        self.action = action
    
    def __str__(self):
        return f"{self.resource}:{self.action}"


class Role:
    """角色"""
    
    def __init__(self, name: str):
        self.name = name
        self.permissions = []
    
    def add_permission(self, permission: Permission):
        self.permissions.append(permission)


class User:
    """用户"""
    
    def __init__(self, user_id: str, roles: list):
        self.user_id = user_id
        self.roles = roles
    
    def has_permission(self, resource: str, action: str) -> bool:
        for role in self.roles:
            for perm in role.permissions:
                if perm.resource == resource and perm.action == action:
                    return True
        return False
```

---

## 4. 审计日志

### 知识点解析

**审计内容**：

1. 用户身份
2. 操作时间
3. 使用的工具
4. 请求参数
5. 操作结果

**日志格式**：

```python
import json
import time


class AuditLogger:
    """审计日志"""
    
    def __init__(self, log_file: str = "audit.log"):
        self.log_file = log_file
    
    def log(self, user_id: str, action: str, details: dict):
        """记录日志"""
        entry = {
            "timestamp": time.time(),
            "user_id": user_id,
            "action": action,
            "details": details
        }
        
        with open(self.log_file, "a") as f:
            f.write(json.dumps(entry) + "\n")
```

---

## 5. 数据加密

### 知识点解析

**加密策略**：

1. **传输加密**：使用TLS/SSL
2. **存储加密**：敏感数据加密存储
3. **密钥管理**：安全的密钥管理

**示例**：

```python
from cryptography.fernet import Fernet


class EncryptionManager:
    """加密管理器"""
    
    def __init__(self, key: bytes = None):
        if key:
            self.cipher = Fernet(key)
        else:
            self.cipher = Fernet(Fernet.generate_key())
    
    def encrypt(self, data: str) -> str:
        """加密数据"""
        return self.cipher.encrypt(data.encode()).decode()
    
    def decrypt(self, encrypted_data: str) -> str:
        """解密数据"""
        return self.cipher.decrypt(encrypted_data.encode()).decode()
```

---

## 实战案例

### 案例1：完整的安全实现

```python
"""
MCP安全与认证完整示例
"""

import json
import time
import hashlib
from typing import Any


class SecurityManager:
    """安全管理器"""
    
    def __init__(self):
        self.users = {}
        self.sessions = {}
        self.audit_log = []
    
    # 用户管理
    def create_user(self, user_id: str, password: str, role: str = "user"):
        """创建用户"""
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        self.users[user_id] = {
            "password_hash": password_hash,
            "role": role,
            "created_at": time.time()
        }
        print(f"✓ 创建用户: {user_id} (role: {role})")
    
    def verify_password(self, user_id: str, password: str) -> bool:
        """验证密码"""
        if user_id not in self.users:
            return False
        
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        return self.users[user_id]["password_hash"] == password_hash
    
    # 会话管理
    def create_session(self, user_id: str) -> str:
        """创建会话"""
        session_id = hashlib.sha256(
            f"{user_id}{time.time()}".encode()
        ).hexdigest()
        
        self.sessions[session_id] = {
            "user_id": user_id,
            "created_at": time.time()
        }
        
        return session_id
    
    def verify_session(self, session_id: str) -> str:
        """验证会话"""
        if session_id not in self.sessions:
            return None
        
        session = self.sessions[session_id]
        
        # 检查会话是否过期 (1小时)
        if time.time() - session["created_at"] > 3600:
            del self.sessions[session_id]
            return None
        
        return session["user_id"]
    
    # 权限检查
    def check_permission(self, user_id: str, tool_name: str) -> bool:
        """检查权限"""
        if user_id not in self.users:
            return False
        
        role = self.users[user_id]["role"]
        
        # 角色权限定义
        permissions = {
            "admin": ["*"],  # 所有权限
            "user": ["read_file", "write_file", "calculate"],
            "guest": ["read_file"]
        }
        
        user_permissions = permissions.get(role, [])
        
        return "*" in user_permissions or tool_name in user_permissions
    
    # 审计日志
    def audit(self, user_id: str, action: str, details: dict):
        """记录审计日志"""
        entry = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "user_id": user_id,
            "action": action,
            "details": details
        }
        self.audit_log.append(entry)
        print(f"📝 审计: {user_id} - {action}")
    
    def get_audit_log(self, limit: int = 10) -> list:
        """获取审计日志"""
        return self.audit_log[-limit:]


def test_security():
    """测试安全功能"""
    print("\n" + "=" * 50)
    print("MCP安全与认证测试")
    print("=" * 50)
    
    # 创建安全管理器
    security = SecurityManager()
    
    # 创建用户
    print("\n创建用户:")
    security.create_user("admin", "admin123", "admin")
    security.create_user("user1", "pass123", "user")
    security.create_user("guest1", "guest", "guest")
    
    # 登录
    print("\n用户登录:")
    session = security.create_session("user1")
    print(f"会话: {session[:16]}...")
    
    # 验证会话
    user = security.verify_session(session)
    print(f"验证会话用户: {user}")
    
    # 权限检查
    print("\n权限检查:")
    for user_id, tool in [("admin", "write_file"), ("user1", "write_file"), ("guest1", "write_file")]:
        has_perm = security.check_permission(user_id, tool)
        print(f"  {user_id} -> {tool}: {'✓' if has_perm else '✗'}")
    
    # 审计日志
    print("\n记录审计:")
    security.audit("user1", "tool_call", {"tool": "write_file", "path": "/test.txt"})
    security.audit("admin", "user_create", {"new_user": "user2"})
    
    print("\n审计日志:")
    for entry in security.get_audit_log():
        print(f"  [{entry['timestamp']}] {entry['user_id']}: {entry['action']}")


if __name__ == "__main__":
    test_security()
```

---

## 本章小结

本章我们学习了MCP安全与认证：

1. **安全概述**：理解了MCP安全的重要性
2. **认证机制**：掌握了API密钥和会话认证
3. **权限控制**：学会了角色和权限管理
4. **审计日志**：掌握了审计日志记录
5. **数据加密**：学会了数据加密处理

这些内容将帮助你在MCP服务中实现企业级安全保护。
