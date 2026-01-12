# CrossPilot - 跨平台智能内容适配器

> 一次创作，全域共鸣

CrossPilot 是一个智能内容适配平台，帮助自媒体创作者将内容快速适配到多个社交媒体平台。

## 功能特性

- **智能内容解析**：自动提取关键信息、分析情感基调、识别风格特征
- **多平台适配**：支持抖音、小红书、B站、微博等8大主流平台
- **一键转换**：自动调整格式、改写文案、生成标题和标签
- **数据追踪**：跨平台数据分析、效果对比、智能优化建议

## 支持平台

| 平台 | 格式 | 特点 |
|------|------|------|
| 抖音 | 竖屏视频 | 快节奏、强冲击、音乐驱动 |
| 快手 | 竖屏视频 | 接地气、真实、生活化 |
| 小红书 | 图文/短视频 | 精致、实用、获得感 |
| 微博 | 短文+九宫格 | 热点驱动、简洁有力 |
| B站 | 中长视频 | 有梗、有深度、社区互动 |
| 视频号 | 横屏视频 | 深度、专业、共鸣 |
| 公众号 | 长文章 | 深度、专业、图文并茂 |
| 知乎 | 问答/长文 | 理性、深度、数据支撑 |

## 技术栈

### 后端
- Python 3.11+
- FastAPI
- SQLAlchemy (AsyncIO)
- PostgreSQL
- Redis
- OpenAI / Claude API

### 前端
- React 18
- TypeScript
- Vite
- Ant Design
- TailwindCSS
- Zustand

## 快速开始

### 后端

```bash
cd backend

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或 venv\Scripts\activate  # Windows

# 安装依赖
pip install -r requirements.txt

# 配置环境变量
cp .env.example .env
# 编辑 .env 文件配置数据库等

# 运行服务
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 前端

```bash
cd frontend

# 安装依赖
npm install

# 运行开发服务器
npm run dev
```

## API 文档

启动后端服务后访问：
- Swagger UI: http://localhost:8000/api/docs
- ReDoc: http://localhost:8000/api/redoc

## 项目结构

```
CrossPilot/
├── backend/                 # 后端服务
│   ├── app/
│   │   ├── api/            # API 路由
│   │   ├── core/           # 核心配置
│   │   ├── models/         # 数据模型
│   │   ├── schemas/        # Pydantic schemas
│   │   ├── services/       # 业务逻辑
│   │   └── utils/          # 工具函数
│   └── requirements.txt
│
├── frontend/                # 前端应用
│   ├── src/
│   │   ├── components/     # 组件
│   │   ├── hooks/          # Hooks & Store
│   │   ├── pages/          # 页面
│   │   ├── router/         # 路由
│   │   ├── services/       # API 服务
│   │   ├── styles/         # 样式
│   │   └── types/          # 类型定义
│   └── package.json
│
└── README.md
```

## 许可证

MIT License
