# 企业级 MCP 示例代码

"""
企业级MCP方案示例代码
展示高可用、负载均衡和监控配置
"""

import json
import time
from typing import Any


# ============================================================
# 1. 高可用架构
# ============================================================


class MCPInstance:
    """MCP服务器实例"""
    
    def __init__(self, instance_id: str, host: str = "localhost"):
        self.instance_id = instance_id
        self.host = host
        self.status = "starting"
        self.start_time = time.time()
        self.request_count = 0
        self.error_count = 0
    
    def start(self):
        """启动实例"""
        self.status = "running"
        print(f"✓ 实例 {self.instance_id} 已启动")
    
    def stop(self):
        """停止实例"""
        self.status = "stopped"
        print(f"✗ 实例 {self.instance_id} 已停止")
    
    def health_check(self) -> bool:
        """健康检查"""
        if self.status != "running":
            return False
        # 模拟健康检查逻辑
        return self.error_count < 10
    
    def handle_request(self, request: dict) -> dict:
        """处理请求"""
        self.request_count += 1
        
        try:
            # 模拟处理逻辑
            result = {"status": "success", "data": f"处理请求 {self.request_count}"}
            return result
        except Exception as e:
            self.error_count += 1
            return {"status": "error", "message": str(e)}


class HACluster:
    """高可用集群"""
    
    def __init__(self, name: str):
        self.name = name
        self.instances = {}
        self.primary = None
    
    def add_instance(self, instance: MCPInstance):
        """添加实例"""
        self.instances[instance.instance_id] = instance
        if self.primary is None:
            self.primary = instance.instance_id
        print(f"✓ 添加实例: {instance.instance_id}")
    
    def remove_instance(self, instance_id: str):
        """移除实例"""
        if instance_id in self.instances:
            del self.instances[instance_id]
            if self.primary == instance_id:
                self.primary = list(self.instances.keys())[0] if self.instances else None
            print(f"✗ 移除实例: {instance_id}")
    
    def check_health(self) -> dict:
        """检查集群健康状态"""
        healthy = []
        unhealthy = []
        
        for instance_id, instance in self.instances.items():
            if instance.health_check():
                healthy.append(instance_id)
            else:
                unhealthy.append(instance_id)
        
        return {
            "total": len(self.instances),
            "healthy": len(healthy),
            "unhealthy": len(unhealthy),
            "healthy_instances": healthy,
            "unhealthy_instances": unhealthy
        }
    
    def failover(self):
        """故障转移"""
        health = self.check_health()
        
        if not health["healthy_instances"]:
            print("⚠️ 没有健康的实例可用")
            return
        
        # 选择新的主节点
        new_primary = health["healthy_instances"][0]
        
        if new_primary != self.primary:
            print(f"🔄 故障转移: {self.primary} -> {new_primary}")
            self.primary = new_primary


def test_ha_cluster():
    """测试高可用集群"""
    print("\n" + "=" * 50)
    print("示例1: 高可用集群")
    print("=" * 50)
    
    # 创建集群
    cluster = HACluster("mcp-cluster")
    
    # 添加实例
    for i in range(3):
        instance = MCPInstance(f"server-{i+1}")
        instance.start()
        cluster.add_instance(instance)
    
    # 健康检查
    health = cluster.check_health()
    print(f"\n集群健康状态: {health}")
    
    # 模拟故障
    print("\n模拟故障:")
    cluster.instances["server-1"].status = "failed"
    cluster.instances["server-1"].error_count = 20
    
    health = cluster.check_health()
    print(f"故障后健康状态: {health}")
    
    # 触发故障转移
    cluster.failover()


# ============================================================
# 2. 负载均衡
# ============================================================


class LoadBalancer:
    """负载均衡器"""
    
    def __init__(self, strategy: str = "round_robin"):
        self.strategy = strategy
        self.instances = []
        self.current_index = 0
        self.request_counts = {}
    
    def add_instance(self, instance_id: str):
        """添加实例"""
        self.instances.append(instance_id)
        self.request_counts[instance_id] = 0
        print(f"✓ 添加到负载均衡池: {instance_id}")
    
    def remove_instance(self, instance_id: str):
        """移除实例"""
        if instance_id in self.instances:
            self.instances.remove(instance_id)
            del self.request_counts[instance_id]
    
    def select_instance(self) -> str:
        """选择实例"""
        if not self.instances:
            raise Exception("没有可用的实例")
        
        if self.strategy == "round_robin":
            # 轮询策略
            instance = self.instances[self.current_index]
            self.current_index = (self.current_index + 1) % len(self.instances)
        
        elif self.strategy == "least_connections":
            # 最少连接策略
            instance = min(
                self.instances,
                key=lambda x: self.request_counts[x]
            )
        
        elif self.strategy == "ip_hash":
            # IP哈希策略
            # 简化实现
            instance = self.instances[0]
        else:
            instance = self.instances[0]
        
        self.request_counts[instance] += 1
        return instance
    
    def route_request(self, request: dict) -> tuple:
        """路由请求"""
        instance = self.select_instance()
        
        return instance, {
            "request_id": request.get("id"),
            "instance": instance,
            "strategy": self.strategy
        }


def test_load_balancer():
    """测试负载均衡"""
    print("\n" + "=" * 50)
    print("示例2: 负载均衡")
    print("=" * 50)
    
    # 创建负载均衡器
    lb = LoadBalancer("round_robin")
    
    # 添加实例
    for i in range(3):
        lb.add_instance(f"server-{i+1}")
    
    # 测试路由
    print("\n测试请求路由 (轮询策略):")
    for i in range(5):
        instance, info = lb.route_request({"id": i+1})
        print(f"  请求 {i+1} -> {info['instance']}")
    
    # 切换到最少连接策略
    print("\n切换到最少连接策略:")
    lb.strategy = "least_connections"
    lb.request_counts = {"server-1": 100, "server-2": 50, "server-3": 10}
    
    instance, info = lb.route_request({"id": 6})
    print(f"  请求6 -> {info['instance']} (应该选择server-3)")


# ============================================================
# 3. 监控指标
# ============================================================


class MetricsCollector:
    """指标收集器"""
    
    def __init__(self):
        self.metrics = {
            "requests_total": 0,
            "requests_success": 0,
            "requests_error": 0,
            "latency_sum": 0,
            "tool_calls": {}
        }
    
    def record_request(self, tool: str, latency: float, success: bool):
        """记录请求"""
        self.metrics["requests_total"] += 1
        
        if success:
            self.metrics["requests_success"] += 1
        else:
            self.metrics["requests_error"] += 1
        
        self.metrics["latency_sum"] += latency
        
        # 记录工具调用
        if tool not in self.metrics["tool_calls"]:
            self.metrics["tool_calls"][tool] = 0
        self.metrics["tool_calls"][tool] += 1
    
    def get_stats(self) -> dict:
        """获取统计信息"""
        total = self.metrics["requests_total"]
        
        return {
            "total_requests": total,
            "success_rate": f"{self.metrics['requests_success']/total*100:.2f}%" if total > 0 else "0%",
            "error_rate": f"{self.metrics['requests_error']/total*100:.2f}%" if total > 0 else "0%",
            "avg_latency": f"{self.metrics['latency_sum']/total*1000:.2f}ms" if total > 0 else "0ms",
            "tool_calls": self.metrics["tool_calls"]
        }


def test_metrics():
    """测试监控指标"""
    print("\n" + "=" * 50)
    print("示例3: 监控指标")
    print("=" * 50)
    
    collector = MetricsCollector()
    
    # 模拟请求
    tools = ["read_file", "write_file", "query", "calculate"]
    
    for i in range(20):
        tool = tools[i % len(tools)]
        latency = 0.1 + (i * 0.05)
        success = i != 15  # 模拟一次失败
        collector.record_request(tool, latency, success)
    
    # 获取统计
    stats = collector.get_stats()
    
    print("\n统计信息:")
    for key, value in stats.items():
        print(f"  {key}: {value}")


# ============================================================
# 4. 配置管理
# ============================================================


class ConfigManager:
    """配置管理器"""
    
    ENVIRONMENTS = ["development", "testing", "staging", "production"]
    
    def __init__(self):
        self.configs = {}
        self._load_configs()
    
    def _load_configs(self):
        """加载配置"""
        self.configs = {
            "development": {
                "log_level": "DEBUG",
                "max_connections": 10,
                "enable_debug": True,
                "cache_ttl": 60
            },
            "testing": {
                "log_level": "INFO",
                "max_connections": 100,
                "enable_debug": True,
                "cache_ttl": 300
            },
            "staging": {
                "log_level": "WARNING",
                "max_connections": 500,
                "enable_debug": False,
                "cache_ttl": 600
            },
            "production": {
                "log_level": "ERROR",
                "max_connections": 1000,
                "enable_debug": False,
                "cache_ttl": 3600
            }
        }
    
    def get_config(self, env: str = "development") -> dict:
        """获取配置"""
        return self.configs.get(env, self.configs["development"])
    
    def update_config(self, env: str, key: str, value: Any):
        """更新配置"""
        if env in self.configs:
            self.configs[env][key] = value
            print(f"✓ 更新配置 [{env}] {key} = {value}")
    
    def validate_config(self, env: str) -> bool:
        """验证配置"""
        config = self.get_config(env)
        
        required_keys = ["log_level", "max_connections", "enable_debug"]
        
        for key in required_keys:
            if key not in config:
                print(f"✗ 缺少必需配置: {key}")
                return False
        
        return True


def test_config_manager():
    """测试配置管理"""
    print("\n" + "=" * 50)
    print("示例4: 配置管理")
    print("=" * 50)
    
    manager = ConfigManager()
    
    # 获取各环境配置
    for env in ConfigManager.ENVIRONMENTS:
        config = manager.get_config(env)
        valid = manager.validate_config(env)
        print(f"\n{env.upper()} (有效: {valid}):")
        for key, value in config.items():
            print(f"  {key}: {value}")


# ============================================================
# 主函数
# ============================================================

if __name__ == "__main__":
    print("=" * 60)
    print("企业级 MCP 方案示例")
    print("=" * 60)
    
    test_ha_cluster()
    test_load_balancer()
    test_metrics()
    test_config_manager()
    
    print("\n" + "=" * 60)
    print("所有示例完成!")
    print("=" * 60)
