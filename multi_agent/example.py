# 多 Agent 协作示例代码

"""
多Agent协作系统示例代码
展示Agent通信、协作和任务分配
"""

import time
import queue
from typing import Any, List, Dict


# ============================================================
# 1. 基础Agent实现
# ============================================================


class BaseAgent:
    """基础Agent"""
    
    def __init__(self, agent_id: str, name: str):
        self.agent_id = agent_id
        self.name = name
        self.message_queue = queue.Queue()
        self.inbox = []
    
    def receive(self, message: dict):
        """接收消息"""
        self.inbox.append(message)
        print(f"📥 {self.name} 收到: {message.get('type', 'unknown')}")
    
    def send(self, receiver, message: dict):
        """发送消息"""
        message["from"] = self.agent_id
        message["to"] = receiver.agent_id
        receiver.receive(message)
    
    def process(self):
        """处理消息"""
        pass
    
    def run_step(self):
        """运行一步"""
        self.process()


def test_base_agent():
    """测试基础Agent"""
    print("\n" + "=" * 50)
    print("示例1: 基础Agent")
    print("=" * 50)
    
    agent1 = BaseAgent("agent1", "Agent One")
    agent2 = BaseAgent("agent2", "Agent Two")
    
    # 发送消息
    agent1.send(agent2, {"type": "greeting", "content": "Hello!"})
    
    # 处理
    agent2.process()
    print(f"Agent2 收件箱: {len(agent2.inbox)} 条")


# ============================================================
# 2. Agent通信系统
# ============================================================


class MessageBus:
    """消息总线"""
    
    def __init__(self):
        self.subscribers = {}
        self.message_log = []
    
    def subscribe(self, agent_id: str, agent):
        """订阅"""
        self.subscribers[agent_id] = agent
        print(f"✓ Agent订阅: {agent_id}")
    
    def unsubscribe(self, agent_id: str):
        """取消订阅"""
        if agent_id in self.subscribers:
            del self.subscribers[agent_id]
    
    def publish(self, sender_id: str, message: dict):
        """发布消息"""
        # 记录日志
        self.message_log.append({
            "sender": sender_id,
            "message": message
        })
        
        # 发送给所有订阅者
        for agent_id, agent in self.subscribers.items():
            if agent_id != sender_id:
                agent.receive(message.copy())
    
    def broadcast(self, sender_id: str, message: dict):
        """广播（包含发送者）"""
        self.message_log.append({
            "sender": sender_id,
            "message": message
        })
        
        for agent_id, agent in self.subscribers.items():
            agent.receive(message.copy())


class CommunicatingAgent(BaseAgent):
    """通信Agent"""
    
    def __init__(self, agent_id: str, name: str, bus: MessageBus):
        super().__init__(agent_id, name)
        self.bus = bus
        self.bus.subscribe(agent_id, self)
    
    def broadcast(self, message: dict):
        """广播消息"""
        self.bus.broadcast(self.agent_id, message)
    
    def send_to(self, receiver_id: str, message: dict):
        """发送给特定Agent"""
        self.bus.publish(self.agent_id, message)


def test_communication():
    """测试通信"""
    print("\n" + "=" * 50)
    print("示例2: Agent通信")
    print("=" * 50)
    
    bus = MessageBus()
    
    agent1 = CommunicatingAgent("agent1", "Alice", bus)
    agent2 = CommunicatingAgent("agent2", "Bob", bus)
    agent3 = CommunicatingAgent("agent3", "Charlie", bus)
    
    # 测试广播
    print("\n广播测试:")
    agent1.broadcast({"type": "announcement", "content": "大家好!"})
    
    # 处理消息
    for agent in [agent1, agent2, agent3]:
        agent.process()
    
    print(f"\nAlice 收件箱: {len(agent1.inbox)}")
    print(f"Bob 收件箱: {len(agent2.inbox)}")
    print(f"Charlie 收件箱: {len(agent3.inbox)}")


# ============================================================
# 3. 任务Agent
# ============================================================


class TaskAgent(CommunicatingAgent):
    """任务Agent"""
    
    def __init__(self, agent_id: str, name: str, bus: MessageBus, skills: list = None):
        super().__init__(agent_id, name, bus)
        self.skills = skills or []
        self.tasks = []
        self.completed_tasks = []
        self.current_task = None
    
    def assign_task(self, task: dict):
        """分配任务"""
        task["status"] = "assigned"
        task["assigned_to"] = self.agent_id
        self.tasks.append(task)
        print(f"✓ {self.name} 收到任务: {task.get('name')}")
    
    def execute_task(self, task: dict) -> dict:
        """执行任务"""
        print(f"🔧 {self.name} 执行: {task.get('name')}")
        
        # 模拟执行
        time.sleep(0.1)
        
        result = {
            "task_id": task.get("id"),
            "result": f"{self.name} 完成 {task.get('name')}",
            "status": "completed"
        }
        
        return result
    
    def process(self):
        """处理消息"""
        while self.inbox:
            message = self.inbox.pop(0)
            msg_type = message.get("type")
            
            if msg_type == "task":
                self.assign_task(message.get("task", {}))
            elif msg_type == "query":
                self._handle_query(message)
        
        # 执行任务
        if self.tasks and not self.current_task:
            self.current_task = self.tasks.pop(0)
        
        if self.current_task:
            result = self.execute_task(self.current_task)
            self.completed_tasks.append(result)
            
            # 通知完成
            self.broadcast({
                "type": "task_completed",
                "result": result
            })
            
            self.current_task = None
    
    def _handle_query(self, message: dict):
        """处理查询"""
        print(f"❓ {self.name} 收到查询: {message.get('query')}")
    
    def get_status(self) -> dict:
        """获取状态"""
        return {
            "id": self.agent_id,
            "name": self.name,
            "skills": self.skills,
            "pending_tasks": len(self.tasks),
            "completed_tasks": len(self.completed_tasks)
        }


def test_task_agent():
    """测试任务Agent"""
    print("\n" + "=" * 50)
    print("示例3: 任务Agent")
    print("=" * 50)
    
    bus = MessageBus()
    
    # 创建Agent
    researcher = TaskAgent("agent1", "研究员", bus, ["research", "analysis"])
    coder = TaskAgent("agent2", "程序员", bus, ["coding", "debug"])
    tester = TaskAgent("agent3", "测试员", bus, ["testing", "quality"])
    
    # 分配任务
    print("\n分配任务:")
    researcher.assign_task({"id": "task1", "name": "调研AI技术"})
    coder.assign_task({"id": "task2", "name": "实现AI功能"})
    tester.assign_task({"id": "task3", "name": "测试AI功能"})
    
    # 执行
    print("\n执行任务:")
    for _ in range(5):
        researcher.process()
        coder.process()
        tester.process()
    
    # 状态
    print("\nAgent状态:")
    for agent in [researcher, coder, tester]:
        status = agent.get_status()
        print(f"  {status['name']}: 完成 {status['completed_tasks']} 个任务")


# ============================================================
# 4. 任务分配器
# ============================================================


class TaskScheduler:
    """任务调度器"""
    
    def __init__(self, bus: MessageBus):
        self.bus = bus
        self.agents = {}
        self.task_queue = []
    
    def register_agent(self, agent: TaskAgent):
        """注册Agent"""
        self.agents[agent.agent_id] = agent
        print(f"✓ 注册Agent到调度器: {agent.name}")
    
    def add_task(self, task: dict):
        """添加任务"""
        task["status"] = "pending"
        self.task_queue.append(task)
        print(f"✓ 添加任务: {task.get('name')}")
    
    def schedule(self):
        """调度任务"""
        while self.task_queue:
            task = self.task_queue[0]
            
            # 选择合适的Agent
            agent_id = self._select_agent(task)
            
            if agent_id:
                task["status"] = "scheduled"
                task["assigned_to"] = agent_id
                
                # 分配给Agent
                self.agents[agent_id].assign_task(task)
                
                self.task_queue.pop(0)
            else:
                # 没有可用的Agent
                break
    
    def _select_agent(self, task: dict) -> str:
        """选择Agent"""
        required_skills = task.get("required_skills", [])
        
        if not required_skills:
            # 简单轮询
            return list(self.agents.keys())[0]
        
        # 匹配技能
        candidates = []
        
        for agent_id, agent in self.agents.items():
            matches = sum(1 for skill in required_skills 
                        if skill in agent.skills)
            
            if matches > 0:
                candidates.append({
                    "agent_id": agent_id,
                    "matches": matches,
                    "load": len(agent.tasks)
                })
        
        if not candidates:
            return None
        
        # 选择匹配最多、负载最低的
        candidates.sort(key=lambda x: (-x["matches"], x["load"]))
        
        return candidates[0]["agent_id"]
    
    def get_pending_tasks(self) -> List[dict]:
        """获取待处理任务"""
        return self.task_queue


def test_scheduler():
    """测试调度器"""
    print("\n" + "=" * 50)
    print("示例4: 任务调度器")
    print("=" * 50)
    
    bus = MessageBus()
    scheduler = TaskScheduler(bus)
    
    # 创建Agent
    researcher = TaskAgent("agent1", "研究员", bus, ["research", "analysis"])
    coder = TaskAgent("agent2", "程序员", bus, ["coding", "debug"])
    tester = TaskAgent("agent3", "测试员", bus, ["testing", "quality"])
    
    # 注册到调度器
    scheduler.register_agent(researcher)
    scheduler.register_agent(coder)
    scheduler.register_agent(tester)
    
    # 添加任务
    print("\n添加任务:")
    scheduler.add_task({
        "id": "task1",
        "name": "调研AI技术",
        "required_skills": ["research"]
    })
    scheduler.add_task({
        "id": "task2",
        "name": "编写Web服务",
        "required_skills": ["coding"]
    })
    scheduler.add_task({
        "id": "task3",
        "name": "编写测试用例",
        "required_skills": ["testing"]
    })
    scheduler.add_task({
        "id": "task4",
        "name": "性能分析",
        "required_skills": ["analysis", "testing"]
    })
    
    # 调度
    print("\n调度任务:")
    scheduler.schedule()
    
    # 查看待处理
    pending = scheduler.get_pending_tasks()
    print(f"\n待处理任务: {len(pending)}")


# ============================================================
# 5. 协作工作流
# ============================================================


class Workflow:
    """工作流"""
    
    def __init__(self, name: str):
        self.name = name
        self.steps = []
        self.results = {}
    
    def add_step(self, step: dict):
        """添加步骤"""
        self.steps.append(step)
    
    def execute(self, context: dict) -> dict:
        """执行工作流"""
        print(f"\n🚀 执行工作流: {self.name}")
        
        current_context = context.copy()
        
        for i, step in enumerate(self.steps):
            print(f"\n步骤 {i+1}: {step.get('name')}")
            
            # 获取执行的Agent
            agent_type = step.get("agent")
            action = step.get("action")
            
            # 模拟执行
            if action == "process":
                current_context[f"step_{i}_result"] = f"处理完成"
            
            print(f"  完成: {current_context.get(f'step_{i}_result')}")
        
        self.results = current_context
        return current_context


def test_workflow():
    """测试工作流"""
    print("\n" + "=" * 50)
    print("示例5: 协作工作流")
    print("=" * 50)
    
    # 创建工作流
    workflow = Workflow("AI功能开发")
    
    # 添加步骤
    workflow.add_step({
        "name": "需求分析",
        "agent": "researcher",
        "action": "process"
    })
    workflow.add_step({
        "name": "编码实现",
        "agent": "coder",
        "action": "process"
    })
    workflow.add_step({
        "name": "测试验证",
        "agent": "tester",
        "action": "process"
    })
    workflow.add_step({
        "name": "部署上线",
        "agent": "deployer",
        "action": "process"
    })
    
    # 执行
    result = workflow.execute({
        "project": "AI助手",
        "priority": "high"
    })
    
    print(f"\n最终结果: {result}")


# ============================================================
# 6. 完整的多Agent系统
# ============================================================


class MultiAgentSystem:
    """完整的多Agent系统"""
    
    def __init__(self):
        self.message_bus = MessageBus()
        self.scheduler = TaskScheduler(self.message_bus)
        self.agents = {}
        self.workflows = {}
    
    def create_agent(self, agent_id: str, name: str, role: str, skills: list = None) -> TaskAgent:
        """创建Agent"""
        agent = TaskAgent(agent_id, name, self.message_bus, skills or [])
        self.agents[agent_id] = agent
        self.scheduler.register_agent(agent)
        
        print(f"✓ 创建Agent: {name} ({role})")
        return agent
    
    def create_workflow(self, name: str) -> Workflow:
        """创建工作流"""
        workflow = Workflow(name)
        self.workflows[name] = workflow
        return workflow
    
    def run_workflow(self, workflow_name: str, context: dict) -> dict:
        """运行工作流"""
        workflow = self.workflows.get(workflow_name)
        
        if not workflow:
            return {"error": f"工作流不存在: {workflow_name}"}
        
        # 为工作流创建任务
        for step in workflow.steps:
            task = {
                "id": f"task_{step.get('name')}",
                "name": step.get("name"),
                "required_skills": [step.get("agent")]
            }
            self.scheduler.add_task(task)
        
        # 调度任务
        self.scheduler.schedule()
        
        # 执行多轮
        for _ in range(10):
            for agent in self.agents.values():
                agent.process()
            self.message_bus.publish("system", {"type": "tick"})
        
        return {"status": "completed", "context": workflow.results}
    
    def get_system_status(self) -> dict:
        """获取系统状态"""
        return {
            "agents": len(self.agents),
            "workflows": len(self.workflows),
            "pending_tasks": len(self.scheduler.get_pending_tasks())
        }


def test_complete_system():
    """测试完整系统"""
    print("\n" + "=" * 50)
    print("示例6: 完整多Agent系统")
    print("=" * 50)
    
    # 创建系统
    system = MultiAgentSystem()
    
    # 创建Agent
    system.create_agent("researcher", "研究员", "research", ["research", "analysis"])
    system.create_agent("coder", "程序员", "development", ["coding", "debug"])
    system.create_agent("tester", "测试员", "testing", ["testing", "quality"])
    system.create_agent("writer", "文档工程师", "documentation", ["writing", "review"])
    
    # 创建工作流
    workflow = system.create_workflow("新功能开发")
    workflow.add_step({
        "name": "技术调研",
        "agent": "researcher"
    })
    workflow.add_step({
        "name": "代码实现",
        "agent": "coder"
    })
    workflow.add_step({
        "name": "测试验证",
        "agent": "tester"
    })
    workflow.add_step({
        "name": "文档编写",
        "agent": "writer"
    })
    
    # 运行工作流
    result = system.run_workflow("新功能开发", {
        "feature": "用户认证",
        "priority": "high"
    })
    
    # 系统状态
    status = system.get_system_status()
    print(f"\n系统状态: {status}")


# ============================================================
# 主函数
# ============================================================

if __name__ == "__main__":
    print("=" * 60)
    print("多 Agent 协作系统示例")
    print("=" * 60)
    
    test_base_agent()
    test_communication()
    test_task_agent()
    test_scheduler()
    test_workflow()
    test_complete_system()
    
    print("\n" + "=" * 60)
    print("所有示例完成!")
    print("=" * 60)
