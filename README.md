# Python Tutorial

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.11+--blue?style=for-the-badge&logo=python" alt="Python Version">
  <img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" alt="License">
  <img src="https://img.shields.io/badge/Contributions-Welcome-orange?style=for-the-badge" alt="Contributions">
  <img src="https://img.shields.io/github/stars/user/python-tutorial?style=for-the-badge" alt="Stars">
</p>

> 一个系统性的 Python 编程教程，涵盖从基础到高级的各类知识点。

## ✨ 特性

- **24+ 知识模块** - 从基础语法到深度学习，全面覆盖
- **交互式学习** - Web 端在线浏览和运行代码
- **实践导向** - 每个知识点配有详细的示例代码
- **Docker 支持** - 一键部署，快速启动
- **多平台运行** - 支持 Windows、Linux、macOS

## 🚀 快速开始

### 本地运行

```bash
# 1. 克隆项目
git clone https://github.com/yourusername/python-tutorial.git
cd python-tutorial

# 2. 运行设置脚本 (Linux/Mac)
./scripts/setup.sh

# 或 Windows
scripts\setup.bat

# 3. 启动 Web 应用
# Flask (端口 5000)
./scripts/run_web.sh flask

# 或 Streamlit (端口 8502)
./scripts/run_web.sh streamlit
```

### Docker 运行

```bash
# 构建并启动
./scripts/run_docker.sh up

# 或 Windows
scripts\run_docker.bat up
```

访问 http://localhost:5000 (Flask) 或 http://localhost:8502 (Streamlit)

## 📚 知识模块

### 基础阶段

| 模块 | 描述 |
|------|------|
| [base_syntax](base_syntax/) | 基础语法 - 变量、注释、输入输出、命名规范 |
| [data_types](data_types/) | 数据类型 - 数字、布尔、序列、映射、集合 |
| [control_flow](control_flow/) | 控制流 - 条件语句、循环、循环控制 |
| [functions](functions/) | 函数 - 参数、作用域、递归、装饰器 |
| [classes_objects](classes_objects/) | 类与对象 - 继承、多态、特殊方法 |
| [exception_handling](exception_handling/) | 异常处理 - 捕获、抛出、上下文管理器 |
| [file_operations](file_operations/) | 文件操作 - 读写、路径处理、二进制文件 |

### 进阶阶段

| 模块 | 描述 |
|------|------|
| [modules_packages](modules_packages/) | 模块与包 - 导入、__name__、包创建 |
| [advanced_features](advanced_features/) | 高级特性 - 推导式、生成器、装饰器 |
| [type_hints](type_hints/) | 类型注解 - typing、dataclasses、静态检查 |
| [concurrency](concurrency/) | 并发编程 - 多线程、多进程、异步IO |
| [standard_library](standard_library/) | 标准库 - os、datetime、collections、itertools |
| [third_party_libraries](third_party_libraries/) | 第三方库 - requests、numpy、pandas |

### 实战阶段

| 模块 | 描述 |
|------|------|
| [database](database/) | 数据库操作 - sqlite3、SQLAlchemy ORM |
| [design_patterns](design_patterns/) | 设计模式 - 创建型、结构型、行为型 |
| [networking](networking/) | 网络编程 - socket、requests、REST API、FastAPI |
| [data_processing](data_processing/) | 数据处理 - pandas、matplotlib、seaborn |
| [web_development](web_development/) | Web 开发 - Flask、FastAPI、Django |
| [unit_testing](unit_testing/) | 单元测试 - unittest、pytest |
| [debugging](debugging/) | 调试技巧 - pdb、logging、性能分析 |

### AI/ML 方向

| 模块 | 描述 |
|------|------|
| [ai_ml_basics](ai_ml_basics/) | AI/ML 基础 - NumPy、Pandas、Scikit-learn |
| [deep_learning](deep_learning/) | 深度学习 - PyTorch、CNN、RNN、Transformer |
| [nlp_and_llm](nlp_and_llm/) | NLP 与大语言模型 - HuggingFace、RAG、LangChain |
| [cv_computer_vision](cv_computer_vision/) | 计算机视觉 - OpenCV、目标检测、图像分割 |

## 🛠 技术栈

```
Python 3.11+          Web 框架
├── Flask             Web 后端
├── Streamlit         交互式 Web
├── SQLAlchemy        ORM
└── pytest            测试框架

数据科学
├── NumPy             数值计算
├── Pandas            数据分析
├── Matplotlib        可视化
└── Scikit-learn      机器学习

深度学习
├── PyTorch           深度学习框架
├── Transformers      NLP/Transformer
└── OpenCV            计算机视觉

DevOps
├── Docker             容器化
└── docker-compose    编排
```

## 📁 项目结构

```
python-tutorial/
├── base_syntax/           # 知识点模块
├── data_types/
├── control_flow/
├── ...
├── web/                   # Web 应用
│   ├── app.py
│   ├── config.py
│   ├── components/
│   └── templates/
├── scripts/               # 运行脚本
│   ├── setup.sh
│   ├── run_docker.sh
│   └── run_web.sh
├── Dockerfile             # Docker 配置
├── docker-compose.yml     # 容器编排
└── README.md
```

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

1. Fork 本项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

## 📄 许可证

本项目基于 MIT 许可证开源。

## 📧 联系方式

- Twitter: https://x.com/DisasterWang
- GitHub: https://github.com/disaster1-tesk/python-tutorial