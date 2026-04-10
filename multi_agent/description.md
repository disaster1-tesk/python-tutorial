# 多 Agent 协作

---

## 学习目标

完成本章节学习后，你将能够：

| 目标 | 描述 | 重要性 |
|------|------|--------|
| 理解多Agent概念 | 掌握多Agent系统的基本原理 | ⭐⭐⭐ 必备 |
| Agent通信 | 实现Agent之间的消息传递 | ⭐⭐⭐ 必备 |
| 协作模式 | 掌握多Agent协作模式 | ⭐⭐ 重要 |
| 任务分配 | 实现任务的智能分配 | ⭐⭐ 重要 |

---

## 章节概览

```
┌─────────────────────────────────────────────────────────┐
│                     多 Agent 协作                          │
├─────────────────────────────────────────────────────────┤
│  1. 多Agent概述 │ 多Agent系统基础                        │
│  2. Agent架构   │ 单个Agent的结构                        │
│  3. 通信机制    │ Agent间消息传递                        │
│  4. 协作模式    │ 多Agent协同工作                        │
│  5. 任务分配    │ 智能任务分配策略                        │
└─────────────────────────────────────────────────────────┘
```

---

## 1. 多Agent概述

### 知识点解析

**多Agent系统（MAS）**：

多Agent系统是由多个自主Agent组成的分布式智能系统，Agent之间通过协作解决复杂问题。

**核心特征**：

1. **自主性**：每个Agent独立运行和决策
2. **社会能力**：Agent之间可以通信协作
3. **反应能力**：能够感知环境并作出反应
4. **预动能力**：能够主动规划和行动

**应用场景**：

| 场景 | 说明 |
|------|------|
| 分布式计算 | 多个Agent协同完成计算任务 |
| 智能客服 | 不同Agent处理不同类型问题 |
| 自动化工作流 | Agent流水线协作完成任务 |

---

## 2. Agent架构

### 知识点解析

**单Agent结构**：

```
┌─────────────────────────────────────┐
│              Agent                  │
├─────────────────────────────────────┤
│  感知层    │  接收外部信息           │
├─────────────────────────────────────┤
│  认知层    │  分析和决策            │
├─────────────────────────────────────┤
│  行动层    │  执行动作              │
└─────────────────────────────────────┘
```

**Agent实现**：

```python
class Agent:
    """基础Agent"""
    
    def __init__(self, agent_id: str, name: str):
        self.agent_id = agent_id
        self.name = name
        self.state = {}
    
    def perceive(self, environment):
        """感知环境"""
        pass
    
    def reason(self):
        """推理决策"""
        pass
    
    def act(self):
        """执行动作"""
        pass
    
    def run(self):
        """运行循环"""
        while True:
            self.perceive()
            self.reason()
            self.act()
```

---

## 3. 通信机制

### 知识点解析

**通信模式**：

1. **点对点通信**：Agent之间直接通信
2. **广播通信**：向所有Agent发送消息
3. **中介通信**：通过中央协调器转发

**消息格式**：

```python
class Message:
    """Agent消息"""
    
    def __init__(self, sender: str, receiver: str, content: dict):
        self.sender = sender
        self.receiver = receiver
        self.content = content
        self.timestamp = time.time()
    
    def to_dict(self) -> dict:
        return {
            "sender": self.sender,
            "receiver": self.receiver,
            "content": self.content,
            "timestamp": self.timestamp
        }
```

**消息处理**：

```python
class MessageHandler:
    """消息处理器"""
    
    def __init__(self):
        self.message_queue = []
    
    def send_message(self, message: Message):
        """发送消息"""
        self.message_queue.append(message)
    
    def receive_message(self, agent_id: str) -> list:
        """接收消息"""
        messages = [m for m in self.message_queue 
                   if m.receiver == agent_id]
        
        # 清除已接收的消息
        self.message_queue = [m for m in self.message_queue 
                            if m.receiver != agent_id]
        
        return messages
```

---

## 4. 协作模式

### 知识点解析

**协作模式类型**：

1. **任务分担**：将任务分解给不同Agent
2. **结果共享**：多个Agent共享中间结果
3. **协商机制**：Agent之间协商决策
4. **竞争模式**：Agent竞争资源

**任务分担模式**：

```python
class TaskDivision:
    """任务分担"""
    
    def __init__(self):
        self.agents = []
        self.task_queue = []
    
    def register_agent(self, agent):
        """注册Agent"""
        self.agents.append(agent)
    
    def assign_task(self, task: dict):
        """分配任务"""
        # 简单的轮询分配
        agent = self.agents[len(self.task_queue) % len(self.agents)]
        self.task_queue.append((task, agent))
        print(f"✓ 任务分配给: {agent.name}")
    
    def execute_tasks(self):
        """执行任务"""
        for task, agent in self.task_queue:
            agent.execute(task)
```

---

## 5. 任务分配

### 知识点解析

**分配策略**：

1. **轮询分配**：循环分配给每个Agent
2. **能力匹配**：根据能力分配任务
3. **负载均衡**：分配给负载最低的Agent
4. **随机分配**：随机选择Agent

**智能分配**：

```python
class SmartScheduler:
    """智能调度器"""
    
    def __init__(self):
        self.agents = {}
        self.task_history = []
    
    def register_agent(self, agent_id: str, capabilities: list):
        """注册Agent及其能力"""
        self.agents[agent_id] = {
            "capabilities": capabilities,
            "current_load": 0,
            "completed_tasks": 0
        }
    
    def select_agent(self, task_requirements: list) -> str:
        """选择最合适的Agent"""
        candidates = []
        
        for agent_id, agent_info in self.agents.items():
            # 检查能力匹配
            matches = sum(1 for req in task_requirements 
                         if req in agent_info["capabilities"])
            
            if matches > 0:
                candidates.append({
                    "agent_id": agent_id,
                    "matches": matches,
                    "load": agent_info["current_load"]
                })
        
        if not candidates:
            return None
        
        # 选择匹配最多、负载最低的Agent
        candidates.sort(key=lambda x: (-x["matches"], x["load"]))
        
        return candidates[0]["agent_id"]
```

---

## 实战案例

### 案例1：完整的多Agent系统

```python
"""
多Agent协作系统示例
"""

import time
from typing import Any


class Agent:
    """Agent实现"""
    
    def __init__(self, agent_id: str, name: str, role: str = "general"):
        self.agent_id = agent_id
        self.name = name
        self.role = role
        self.inbox = []
        self.outbox = []
        self.state = {"tasks_completed": 0}
    
    def receive_message(self, message: dict):
        """接收消息"""
        self.inbox.append(message)
        print(f"📥 {self.name} 收到消息: {message.get('type')}")
    
    def process_messages(self):
        """处理消息"""
        while self.inbox:
            message = self.inbox.pop(0)
            self._handle_message(message)
    
    def _handle_message(self, message: dict):
        """处理单个消息"""
        msg_type = message.get("type")
        
        if msg_type == "task":
            self._execute_task(message)
        elif msg_type == "query":
            self._respond_to_query(message)
        elif msg_type == "result":
            self._receive_result(message)
    
    def _execute_task(self, message: dict):
        """执行任务"""
        task = message.get("task")
        print(f"🔧 {self.name} 执行任务: {task}")
        
        # 模拟任务执行
        time.sleep(0.1)
        
        # 发送结果
        result = {
            "type": "result",
            "task_id": message.get("task_id"),
            "result": f"{self.name} 完成 {task}",
            "agent": self.name
        }
        self.send_message(result, message.get("sender"))
        
        self.state["tasks_completed"] += 1
    
    def _respond_to_query(self, message: dict):
        """响应查询"""
        response = {
            "type": "response",
            "query": message.get("query"),
            "answer": f"{self.name} 的状态: {self.state}",
            "sender": self.name
        }
        self.send_message(response, message.get("sender"))
    
    def _receive_result(self, message: dict):
        """接收结果"""
        print(f"📤 {self.name} 收到结果: {message.get('result')}")
    
    def send_message(self, message: dict, receiver: str):
        """发送消息"""
        message["sender"] = self.name
        message["receiver"] = receiver
        self.outbox.append(message)


class MultiAgentSystem:
    """多Agent系统"""
    
    def __init__(self):
        self.agents = {}
        self.message_bus = []
    
    def register_agent(self, agent: Agent):
        """注册Agent"""
        self.agents[agent.agent_id] = agent
        print(f"✓ 注册Agent: {agent.name} (role: {agent.role})")
    
    def send_message(self, sender: str, receiver: str, message: dict):
        """发送消息"""
        sender_agent = self.agents.get(sender)
        if sender_agent:
            sender_agent.send_message(message, receiver)
    
    def broadcast_message(self, sender: str, message: dict):
        """广播消息"""
        for agent_id, agent in self.agents.items():
            if agent_id != sender:
                agent.receive_message(message.copy())
    
    def process_all(self):
        """处理所有消息"""
        for agent in self.agents.values():
            agent.process_messages()
        
        # 传递消息
        for agent in self.agents.values():
            while agent.outbox:
                message = agent.outbox.pop(0)
                receiver = message.get("receiver")
                
                if receiver in self.agents:
                    self.agents[receiver].receive_message(message)
                else:
                    print(f"⚠️ 未知接收者: {receiver}")
    
    def get_system_status(self) -> dict:
        """获取系统状态"""
        return {
            "total_agents": len(self.agents),
            "agents": {
                agent_id: agent.state
                for agent_id, agent in self.agents.items()
            }
        }


def test_multi_agent():
    """测试多Agent系统"""
    print("\n" + "=" * 50)
    print("多Agent协作系统测试")
    print("=" * 50)
    
    # 创建系统
    system = MultiAgentSystem()
    
    # 创建Agent
    researcher = Agent("agent1", "研究员", "researcher")
    coder = Agent("agent2", "程序员", "coder")
    tester = Agent("agent3", "测试员", "tester")
    
    # 注册Agent
    system.register_agent(researcher)
    system.register_agent(coder)
    system.register_agent(tester)
    
    # 分配任务
    print("\n分配任务:")
    system.send_message("agent1", "agent2", {
        "type": "task",
        "task_id": "task1",
        "task": "实现用户认证功能",
        "sender": "manager"
    })
    
    system.send_message("agent2", "agent3", {
        "type": "task",
        "task_id": "task2",
        "task": "测试用户认证功能",
        "sender": "manager"
    })
    
    # 处理消息
    print("\n处理消息:")
    system.process_all()
    
    # 查询状态
    print("\n系统状态:")
    status = system.get_system_status()
    print(f"  总Agent数: {status['total_agents']}")
    for agent_id, state in status['agents'].items():
        print(f"  {agent_id}: 完成任务 {state['tasks_completed']}")


if __name__ == "__main__":
    test_multi_agent()
```

---

## 本章小结

本章我们学习了多Agent协作：

1. **多Agent概述**：理解了多Agent系统的概念和应用场景
2. **Agent架构**：掌握了Agent的基本结构
3. **通信机制**：学会了Agent间消息传递
4. **协作模式**：掌握了任务分担和结果共享模式
5. **任务分配**：学会了智能任务分配策略

这些内容将帮助你构建多Agent协作系统，实现复杂的AI应用。
