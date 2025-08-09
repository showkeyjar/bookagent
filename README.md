# 智能技术图书自动生成系统

## 系统概述

智能技术图书自动生成系统是一个基于大语言模型的智能写作助手，能够根据用户需求自动生成结构完整、内容专业的技术类图书。系统支持Word模板定制、多轮交互式编辑、自动图表生成等功能，帮助用户高效完成技术文档创作。

## 功能特性

### 🎯 专注思想传递的界面设计
- **简洁直观**：去除干扰元素，让用户专注于内容创作
- **智能引导**：分步骤的创作流程，从想法到成书
- **实时预览**：所见即所得的编辑体验

### 🤖 AI 驱动的智能创作
- **思想启发**：AI 助手帮助激发创作灵感
- **内容生成**：基于大语言模型自动生成高质量技术内容
- **智能优化**：自动优化文字表达和内容结构

### 📚 结构化的图书管理
- **模板系统**：提供多种图书模板，快速开始创作
- **章节管理**：可视化的章节结构，支持拖拽重组
- **进度跟踪**：实时显示创作进度和字数统计

### 🎨 现代化的用户体验
- **响应式设计**：完美适配桌面和移动设备
- **流畅动画**：精心设计的交互动效
- **深色模式**：护眼的深色主题（即将推出）

### 🔧 强大的编辑功能
- **Markdown 支持**：支持 Markdown 语法，专业排版
- **实时协作**：多人同时编辑和评论（开发中）
- **版本控制**：完整的版本历史记录，支持版本对比和回滚
- **导出功能**：支持多种格式导出（PDF、Word、HTML）

## 技术栈

- **后端**：Python 3.9+, FastAPI, SQLAlchemy, PostgreSQL, Redis
- **AI**：OpenAI GPT-4, 支持自定义模型
- **存储**：MinIO (S3兼容对象存储)
- **前端**：React, TypeScript, Ant Design (待实现)
- **部署**：Docker, Nginx

## 快速开始

### 环境要求

**后端**：
- Python 3.9+
- PostgreSQL 13+ (可选，开发阶段可跳过)
- Redis 6+ (可选，开发阶段可跳过)

**前端**：
- Node.js 16+
- npm 或 yarn

### 方式一：快速体验（推荐）

#### 1. 启动前端界面

```bash
# Windows 用户
start-frontend.bat

# macOS/Linux 用户
chmod +x start-frontend.sh
./start-frontend.sh
```

前端将在 http://localhost:3000 启动，你可以立即体验完整的用户界面。

#### 2. 启动后端 API（可选）

```bash
# 安装基础依赖
pip install fastapi uvicorn python-dotenv

# 启动简化版 API
python simple_main.py
```

后端将在 http://localhost:8000 启动。

### 方式二：完整开发环境

#### 1. 克隆代码库

```bash
git clone https://github.com/yourusername/bookagent.git
cd bookagent
```

#### 2. 后端设置

```bash
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Windows
.\venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 配置环境变量
cp .env.example .env
# 编辑 .env 文件设置配置

# 启动后端
uvicorn bookagent.main:app --reload
```

#### 3. 前端设置

```bash
# 进入前端目录
cd frontend

# 安装依赖
npm install

# 启动前端
npm run dev
```

### 访问应用

- **前端界面**: http://localhost:3000
- **后端 API**: http://localhost:8000
- **API 文档**: http://localhost:8000/api/docs

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
