# CrossPilot 部署测试流程

本文档详细说明 CrossPilot 项目的部署和测试流程。

## 目录

- [环境要求](#环境要求)
- [本地开发环境部署](#本地开发环境部署)
- [生产环境部署](#生产环境部署)
- [测试流程](#测试流程)
- [Docker 部署](#docker-部署)
- [常见问题](#常见问题)

---

## 环境要求

### 系统要求

| 组件 | 版本要求 |
|------|----------|
| Python | 3.11+ |
| Node.js | 18+ |
| PostgreSQL | 14+ |
| Redis | 6+ |

### 依赖服务

- **PostgreSQL**: 主数据库，存储用户、内容、平台账户等数据
- **Redis**: 缓存服务，用于会话管理和任务队列
- **AWS S3**: 媒体文件存储（可选，本地开发可使用本地存储）

---

## 本地开发环境部署

### 1. 克隆项目

```bash
git clone https://github.com/wskyl/CrossPilot.git
cd CrossPilot
```

### 2. 后端部署

#### 2.1 创建虚拟环境

```bash
cd backend

# Linux/Mac
python -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

#### 2.2 安装依赖

```bash
pip install -r requirements.txt
```

#### 2.3 配置环境变量

```bash
cp .env.example .env
```

编辑 `.env` 文件，配置以下关键参数：

```env
# 数据库连接
DATABASE_URL=postgresql+asyncpg://postgres:your_password@localhost:5432/crosspilot

# Redis 连接
REDIS_URL=redis://localhost:6379/0

# JWT 密钥（生产环境请使用强密钥）
SECRET_KEY=your-secret-key-change-in-production

# AI 服务 API（至少配置一个）
OPENAI_API_KEY=your-openai-key
ANTHROPIC_API_KEY=your-anthropic-key
```

#### 2.4 初始化数据库

```bash
# 创建数据库
createdb crosspilot

# 运行数据库迁移
alembic upgrade head
```

#### 2.5 启动后端服务

```bash
# 开发模式（支持热重载）
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# 生产模式
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

#### 2.6 验证后端服务

- API 文档: http://localhost:8000/api/docs
- ReDoc: http://localhost:8000/api/redoc
- 健康检查: http://localhost:8000/health

### 3. 前端部署

#### 3.1 安装依赖

```bash
cd frontend
npm install
```

#### 3.2 配置环境变量

创建 `.env.local` 文件：

```env
VITE_API_BASE_URL=http://localhost:8000/api/v1
```

#### 3.3 启动前端开发服务器

```bash
npm run dev
```

访问 http://localhost:5173 查看前端页面。

#### 3.4 构建生产版本

```bash
npm run build
npm run preview  # 预览构建结果
```

---

## 生产环境部署

### 1. 服务器准备

```bash
# 安装系统依赖
sudo apt update
sudo apt install -y python3.11 python3.11-venv nodejs npm postgresql redis-server nginx

# 安装 pm2 用于进程管理
npm install -g pm2
```

### 2. 后端生产部署

#### 2.1 配置 Gunicorn

创建 `gunicorn.conf.py`:

```python
bind = "0.0.0.0:8000"
workers = 4
worker_class = "uvicorn.workers.UvicornWorker"
accesslog = "/var/log/crosspilot/access.log"
errorlog = "/var/log/crosspilot/error.log"
```

#### 2.2 使用 PM2 管理进程

```bash
# 创建 ecosystem 配置文件
cat > ecosystem.config.js << EOF
module.exports = {
  apps: [{
    name: 'crosspilot-api',
    cmd: 'gunicorn',
    args: 'app.main:app -c gunicorn.conf.py',
    cwd: '/path/to/CrossPilot/backend',
    interpreter: '/path/to/venv/bin/python'
  }]
}
EOF

pm2 start ecosystem.config.js
pm2 save
pm2 startup
```

### 3. 前端生产部署

#### 3.1 构建前端

```bash
cd frontend
npm run build
```

#### 3.2 Nginx 配置

```nginx
server {
    listen 80;
    server_name your-domain.com;

    # 前端静态文件
    location / {
        root /path/to/CrossPilot/frontend/dist;
        try_files $uri $uri/ /index.html;
    }

    # API 代理
    location /api {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

```bash
# 启用配置
sudo ln -s /etc/nginx/sites-available/crosspilot /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

---

## 测试流程

### 1. 后端单元测试

```bash
cd backend

# 运行所有测试
pytest

# 运行带覆盖率的测试
pytest --cov=app --cov-report=html

# 运行特定测试文件
pytest tests/test_auth.py -v

# 运行异步测试
pytest tests/ -v --asyncio-mode=auto
```

### 2. 后端 API 测试

```bash
# 安装 httpie（可选，更友好的命令行 HTTP 客户端）
pip install httpie

# 测试健康检查端点
curl http://localhost:8000/health

# 测试用户注册
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "testpassword123", "username": "testuser"}'

# 测试用户登录
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=test@example.com&password=testpassword123"
```

### 3. 前端测试

```bash
cd frontend

# 运行 ESLint 检查
npm run lint

# 类型检查
npx tsc --noEmit
```

### 4. 集成测试清单

| 测试项 | 测试步骤 | 预期结果 |
|--------|----------|----------|
| 用户注册 | POST /api/v1/auth/register | 返回用户信息和 token |
| 用户登录 | POST /api/v1/auth/login | 返回 access_token |
| 内容上传 | POST /api/v1/content/upload | 返回内容 ID |
| 内容适配 | POST /api/v1/content/{id}/adapt | 返回适配后的内容 |
| 获取内容列表 | GET /api/v1/content | 返回内容列表 |

### 5. E2E 测试流程

```bash
# 1. 确保后端服务运行中
curl http://localhost:8000/health

# 2. 确保前端服务运行中
curl http://localhost:5173

# 3. 完整流程测试
# - 访问首页
# - 注册新用户
# - 登录系统
# - 上传内容
# - 选择目标平台
# - 生成适配内容
# - 预览和导出
```

---

## Docker 部署

### docker-compose.yml 示例

```yaml
version: '3.8'

services:
  postgres:
    image: postgres:14-alpine
    environment:
      POSTGRES_DB: crosspilot
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: your_password
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    environment:
      DATABASE_URL: postgresql+asyncpg://postgres:your_password@postgres:5432/crosspilot
      REDIS_URL: redis://redis:6379/0
    ports:
      - "8000:8000"
    depends_on:
      - postgres
      - redis

  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    ports:
      - "80:80"
    depends_on:
      - backend

volumes:
  postgres_data:
```

### 启动 Docker 服务

```bash
# 构建并启动所有服务
docker-compose up -d --build

# 查看服务状态
docker-compose ps

# 查看日志
docker-compose logs -f backend

# 停止服务
docker-compose down
```

---

## 常见问题

### Q1: 数据库连接失败

```bash
# 检查 PostgreSQL 服务状态
sudo systemctl status postgresql

# 检查连接配置
psql -h localhost -U postgres -d crosspilot
```

### Q2: Redis 连接失败

```bash
# 检查 Redis 服务状态
sudo systemctl status redis

# 测试连接
redis-cli ping
```

### Q3: 前端无法连接后端 API

1. 检查后端服务是否运行: `curl http://localhost:8000/health`
2. 检查 CORS 配置是否正确
3. 确认前端 `.env.local` 中的 API 地址配置正确

### Q4: AI 服务调用失败

1. 检查 API Key 是否正确配置
2. 检查网络是否可以访问 OpenAI/Anthropic API
3. 查看后端日志获取详细错误信息

---

## 部署检查清单

- [ ] PostgreSQL 服务运行正常
- [ ] Redis 服务运行正常
- [ ] 后端环境变量配置完成
- [ ] 数据库迁移已执行
- [ ] 后端服务启动成功
- [ ] API 文档可访问
- [ ] 前端依赖安装完成
- [ ] 前端服务启动成功
- [ ] 前后端通信正常
- [ ] AI 服务 API 配置完成（可选）

---

## 联系支持

如有部署问题，请提交 Issue 至项目仓库：https://github.com/wskyl/CrossPilot/issues
