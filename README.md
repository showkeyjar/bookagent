# 智能技术图书自动生成系统

## 系统概述

智能技术图书自动生成系统是一个基于大语言模型的智能写作助手，能够根据用户需求自动生成结构完整、内容专业的技术类图书。系统支持Word模板定制、多轮交互式编辑、自动图表生成等功能，帮助用户高效完成技术文档创作。

## 功能特性

- **智能内容生成**：基于大语言模型自动生成高质量技术内容
- **模板管理**：支持自定义Word模板，灵活适配不同写作需求
- **交互式编辑**：提供实时协作编辑功能，支持多人同时编辑
- **版本控制**：完整的版本历史记录，支持版本对比和回滚
- **权限管理**：基于角色的访问控制，确保数据安全
- **RESTful API**：标准化的API接口，方便集成其他系统

## 技术栈

- **后端**：Python 3.9+, FastAPI, SQLAlchemy, PostgreSQL, Redis
- **AI**：OpenAI GPT-4, 支持自定义模型
- **存储**：MinIO (S3兼容对象存储)
- **前端**：React, TypeScript, Ant Design (待实现)
- **部署**：Docker, Nginx

## 快速开始

### 环境要求

- Python 3.9+
- PostgreSQL 13+
- Redis 6+
- MinIO (可选，用于文件存储)

### 1. 克隆代码库

```bash
git clone https://github.com/yourusername/bookagent.git
cd bookagent
```

### 2. 创建并激活虚拟环境

```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. 安装依赖

```bash
pip install -r requirements.txt
```

### 4. 配置环境变量

复制示例环境变量文件并修改配置：

```bash
cp .env.example .env
```

编辑 `.env` 文件，设置您的数据库连接和其他配置。

### 5. 初始化数据库

```bash
alembic upgrade head
```

### 6. 运行开发服务器

```bash
uvicorn main:app --reload
```

API文档将在以下地址可用：
- Swagger UI: http://localhost:8000/api/docs
- ReDoc: http://localhost:8000/api/redoc

## API 使用示例

### 1. 用户认证

```bash
# 获取访问令牌
curl -X 'POST' \
  'http://localhost:8000/api/v1/auth/token' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -d 'grant_type=password&username=admin&password=yourpassword'
```

### 2. 创建图书

```bash
# 创建新图书
curl -X 'POST' \
  'http://localhost:8000/api/v1/books/' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer YOUR_ACCESS_TOKEN' \
  -H 'Content-Type: application/json' \
  -d '{
    "title": "Python高级编程",
    "description": "深入理解Python高级特性和最佳实践",
    "status": "draft"
  }'
```

### 3. 生成章节内容

```bash
# 使用AI生成章节内容
curl -X 'POST' \
  'http://localhost:8000/api/v1/ai/generate/chapter' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer YOUR_ACCESS_TOKEN' \
  -H 'Content-Type: application/json' \
  -d '{
    "topic": "Python装饰器详解",
    "style": "technical",
    "language": "zh",
    "length": "medium"
  }'
```

## 项目结构

```
bookagent/
├── alembic/                  # 数据库迁移脚本
├── bookagent/                # 应用主包
│   ├── app/                  # 应用代码
│   │   ├── api/              # API路由
│   │   ├── core/             # 核心功能
│   │   ├── models/           # 数据库模型
│   │   ├── schemas/          # Pydantic模型
│   │   └── services/         # 业务逻辑
│   ├── migrations/           # 数据库迁移
│   └── tests/                # 测试代码
├── .env.example             # 环境变量示例
├── .gitignore
├── alembic.ini              # Alembic配置
├── main.py                  # 应用入口
├── README.md                # 项目说明
└── requirements.txt         # 依赖列表
```

## 开发指南

### 代码规范

- 使用 `black` 进行代码格式化
- 使用 `isort` 进行导入排序
- 使用 `mypy` 进行类型检查

### 测试

运行测试：

```bash
pytest
```

### 代码提交

提交代码前请确保：

1. 所有测试通过
2. 代码已格式化
3. 类型检查通过

## 部署

### 使用 Docker 部署

1. 安装 Docker 和 Docker Compose
2. 复制并配置 `.env` 文件
3. 运行以下命令：

```bash
docker-compose up -d
```

## 贡献指南

欢迎提交 Issue 和 Pull Request。

## 许可证

[MIT License](LICENSE)

## 系统架构

```mermaid
graph TD
    A[用户界面] -->|输入需求| B[智能体控制器]
    B --> C[内容生成模块]
    B --> D[模板管理模块]
    B --> E[交互式编辑模块]
    C --> F[大语言模型]
    D --> G[Word模板库]
    E --> H[版本控制系统]
    F --> C
    G --> D
    H --> E
    A <-->|交互| E
```

## 核心模块详解

### 1. 智能体控制器

#### 1.1 指令解析器
- 自然语言理解：解析用户输入，识别意图和参数
- 任务调度：根据指令类型分发给对应模块
- 状态管理：维护任务执行状态和上下文

#### 1.2 工作流引擎
- 任务编排：定义和执行内容生成流程
- 异常处理：捕获和处理各模块异常
- 性能监控：记录各环节执行时间和资源占用

### 2. 内容生成模块

#### 2.1 文本生成器
- 基于大语言模型生成高质量技术内容
- 支持多轮迭代优化
- 内容风格控制

#### 2.2 图表生成器
- 自动生成技术架构图
- 支持流程图、类图等常用技术图表
- 图表样式自定义

#### 2.3 知识库集成
- 技术文档检索
- 代码示例库
- 最佳实践指南

### 3. 模板管理模块

#### 3.1 模板解析器
- 解析Word文档模板
- 提取占位符和变量
- 支持条件判断和循环结构

#### 3.2 样式管理器
- 维护文档样式规范
- 自动应用样式
- 支持自定义样式

#### 3.3 模板版本控制
- 模板版本管理
- 变更历史记录
- 版本回滚功能

### 4. 交互式编辑模块

#### 4.1 实时协作
- 多用户实时编辑
- 操作冲突解决
- 协同光标显示

#### 4.2 评论与批注
- 添加批注
- @提及协作者
- 讨论线程管理

#### 4.3 版本对比
- 版本差异可视化
- 选择性恢复
- 变更历史浏览

## 技术实现

### 1. 技术栈

#### 后端
- 编程语言：Python 3.9+
- Web框架：FastAPI
- 数据库：PostgreSQL + Redis
- 任务队列：Celery
- 存储：MinIO

#### 前端
- 框架：React + TypeScript
- 富文本编辑器：TinyMCE
- 图表库：Mermaid.js
- 状态管理：Redux Toolkit

### 2. 集成服务

#### 大语言模型
- OpenAI GPT-4 API
- 本地部署的开源模型（可选）
- 模型微调接口

#### 文档处理
- python-docx：Word文档处理
- Pandoc：文档格式转换
- WeasyPrint：PDF生成

## 部署架构

```mermaid
flowchart TB
    subgraph 负载均衡
    LB[NGINX]
    end
    
    subgraph 应用服务器
    A1[FastAPI] --> B1[PostgreSQL]
    A1 --> C1[Redis]
    A1 --> D1[MinIO]
    end
    
    subgraph 工作节点
    W1[Celery Worker]
    W2[Celery Beat]
    end
    
    LB -->|请求| A1
    A1 -->|异步任务| W1
    W2 -->|定时任务| W1
```

## 配置说明

### 环境变量

```env
# 数据库配置
DATABASE_URL=postgresql://user:password@localhost:5432/bookagent
REDIS_URL=redis://localhost:6379/0

# 存储配置
STORAGE_ENDPOINT=localhost:9000
STORAGE_ACCESS_KEY=minioadmin
STORAGE_SECRET_KEY=minioadmin
STORAGE_BUCKET=bookagent

# 大模型配置
OPENAI_API_KEY=your-api-key
MODEL_NAME=gpt-4
TEMPERATURE=0.7
```

## 开发指南

### 环境准备

1. 安装依赖
```bash
pip install -r requirements.txt
```

2. 初始化数据库
```bash
alembic upgrade head
```

3. 启动开发服务器
```bash
uvicorn app.main:app --reload
```

## 使用示例

### 生成新章节

```python
from bookagent import BookAgent

agent = BookAgent()
chapter = agent.generate_chapter(
    topic="微服务架构设计",
    template="standard",
    style="academic"
)
print(chapter.content)
```

### 交互式编辑

```python
# 开始编辑会话
session = agent.start_edit_session(chapter_id=123)

# 获取建议修改
suggestions = session.get_suggestions()

# 应用修改
session.apply_edit(suggestions[0])

# 保存更改
session.save()
```

## 许可证

MIT License
