# BookAgent Frontend

专注于思想传递的智能图书创作平台前端界面。

## 设计理念

### 1. 思想优先
- 简洁的界面设计，减少认知负担
- 直观的创作流程，让用户专注于内容
- AI 助手无缝集成，提供智能创作支持

### 2. 用户体验
- 响应式设计，适配各种设备
- 流畅的动画效果，提升交互体验
- 清晰的信息层次，便于内容组织

### 3. 功能特性
- **智能创作**：AI 驱动的内容生成和优化
- **结构化编辑**：章节管理和版本控制
- **实时协作**：多人同时编辑和评论
- **可视化导出**：支持多种格式输出

## 技术栈

- **框架**：Next.js 14 (App Router)
- **样式**：Tailwind CSS
- **动画**：Framer Motion
- **图标**：Heroicons
- **状态管理**：Zustand
- **HTTP 客户端**：Axios
- **Markdown**：React Markdown

## 快速开始

### 安装依赖
```bash
npm install
```

### 启动开发服务器
```bash
npm run dev
```

### 构建生产版本
```bash
npm run build
npm start
```

## 项目结构

```
frontend/
├── app/                    # Next.js App Router
│   ├── globals.css        # 全局样式
│   ├── layout.tsx         # 根布局
│   ├── page.tsx           # 首页
│   ├── dashboard/         # 仪表板
│   ├── editor/            # 编辑器
│   └── create/            # 创建图书
├── components/            # 可复用组件
├── lib/                   # 工具函数
├── hooks/                 # 自定义 Hooks
└── types/                 # TypeScript 类型定义
```

## 核心页面

### 1. 首页 (/)
- 产品介绍和特性展示
- 清晰的价值主张
- 引导用户开始创作

### 2. 仪表板 (/dashboard)
- 图书项目管理
- 创作进度跟踪
- 快速操作入口

### 3. 编辑器 (/editor/[id])
- 章节结构导航
- 实时编辑和预览
- AI 助手集成
- 协作功能

### 4. 创建图书 (/create)
- 分步骤创建流程
- 模板选择
- 智能配置

## 设计系统

### 颜色方案
- **主色**：蓝色系 (#0ea5e9)
- **辅助色**：灰色系
- **强调色**：紫色、绿色、黄色

### 字体
- **无衬线**：Inter (界面文字)
- **衬线**：Crimson Text (内容文字)

### 组件规范
- 统一的按钮样式
- 一致的表单控件
- 标准化的卡片布局
- 响应式网格系统

## 开发指南

### 代码规范
- 使用 TypeScript 进行类型检查
- 遵循 ESLint 规则
- 组件采用函数式写法
- 使用 Tailwind CSS 类名

### 性能优化
- 图片懒加载
- 代码分割
- 缓存策略
- 预加载关键资源

### 可访问性
- 语义化 HTML
- 键盘导航支持
- 屏幕阅读器友好
- 颜色对比度符合标准

## 部署

### 环境变量
```bash
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### Docker 部署
```bash
docker build -t bookagent-frontend .
docker run -p 3000:3000 bookagent-frontend
```

## 贡献指南

1. Fork 项目
2. 创建功能分支
3. 提交更改
4. 推送到分支
5. 创建 Pull Request

## 许可证

MIT License