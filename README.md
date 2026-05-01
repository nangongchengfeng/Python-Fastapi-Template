# FastAPI 后端服务模板

## 项目概述

基于 FastAPI 构建的高性能 Python 后端服务模板，采用分层架构设计，提供规范化的项目结构，帮助开发者快速搭建和开发 Web 应用。

## 技术栈

| 技术 | 版本 | 说明 |
|------|------|------|
| Python | 3.8+ | 编程语言 |
| FastAPI | 0.104+ | Web 框架 |
| Uvicorn | 0.24+ | ASGI 服务器 |
| Pydantic | 2.5+ | 数据验证和序列化 |
| Pydantic Settings | 2.1+ | 配置管理 |
| SQLAlchemy | 2.0+ | ORM 框架 |
| PyMySQL | 1.1+ | MySQL 数据库驱动 |
| Alembic | 1.13+ | 数据库迁移工具 |
| Python-JOSE | 3.3+ | JWT 认证 |
| APScheduler | 3.10+ | 任务调度 |
| uv | - | 包管理工具 |

## 项目结构

```
backend/
├── app/
│   ├── __init__.py              # 包初始化文件
│   ├── config.py                # 配置管理模块
│   ├── database.py              # 数据库配置模块
│   ├── main.py                  # FastAPI 应用入口
│   ├── api/
│   │   ├── __init__.py
│   │   ├── controller/          # 控制器层
│   │   │   ├── __init__.py
│   │   │   └── demo.py          # 示例控制器
│   │   ├── service/             # 服务层（业务逻辑）
│   │   │   └── __init__.py
│   │   ├── dao/                 # 数据访问层
│   │   │   └── __init__.py
│   │   ├── models/              # 数据模型层
│   │   │   └── __init__.py
│   │   └── schemas/             # 数据验证模型
│   │       ├── __init__.py
│   │       └── demo.py          # 示例数据模型
│   ├── middleware/              # 中间件
│   │   ├── __init__.py
│   │   ├── auth.py              # JWT 认证中间件
│   │   └── cors.py              # CORS 中间件
│   └── common/                  # 公共模块
│       ├── __init__.py
│       ├── result/              # 统一响应格式
│       │   ├── __init__.py
│       │   ├── code.py          # 状态码定义
│       │   └── result.py        # 响应结果类
│       ├── util/                # 工具函数
│       │   └── LogHandler.py    # 日志处理
│       └── sockets_test/        # Socket 测试（可选）
├── logs/                        # 日志目录
├── scripts/                     # 脚本目录
├── tests/                       # 测试目录
├── pyproject.toml               # uv 项目配置
├── requirements.txt             # Python 依赖
├── .env.example                 # 环境变量示例
├── run.py                       # 启动脚本
└── README.md                    # 项目说明文档
```

### 分层架构说明

- **Controller 层**：处理 HTTP 请求，参数验证，调用 Service 层
- **Service 层**：实现业务逻辑，调用 DAO 层进行数据操作
- **DAO 层**：封装数据库操作，提供数据访问接口
- **Model 层**：定义数据库 ORM 模型
- **Schema 层**：定义请求和响应的数据验证模型

## 快速开始

### 环境要求

- Python 3.8+
- MySQL 5.7+ 或 8.0+

### 使用 uv 安装（推荐）

```bash
# 克隆项目
cd backend

# 创建虚拟环境
uv venv

# 激活虚拟环境
source .venv/bin/activate  # Linux/Mac
# 或
.venv\Scripts\activate  # Windows

# 安装依赖
uv pip install -r requirements.txt

# 复制环境变量配置文件
cp .env.example .env

# 编辑 .env 文件，配置数据库连接等信息
vim .env
```

### 使用 pip 安装

```bash
# 创建虚拟环境
python -m venv .venv

# 激活虚拟环境
source .venv/bin/activate  # Linux/Mac
# 或
.venv\Scripts\activate  # Windows

# 安装依赖
pip install -r requirements.txt
```

### 配置说明

编辑 `.env` 文件，配置以下内容：

```env
# 应用配置
APP_NAME=FastAPI-Backend
APP_ENV=development
APP_DEBUG=true
APP_HOST=0.0.0.0
APP_PORT=8000
SECRET_KEY=your-secret-key-change-this-in-production

# 数据库配置
DB_HOST=127.0.0.1
DB_PORT=3306
DB_USER=root
DB_PASSWORD=password
DB_DATABASE=fastapi_db

# JWT 配置
JWT_SECRET_KEY=your-jwt-secret-key
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=480
```

### 启动服务

#### 开发模式（自动重载）

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### 生产模式

```bash
python run.py
```

或使用 Gunicorn + Uvicorn：

```bash
pip install gunicorn
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000
```

### 访问服务

- **API 文档 (Swagger UI)**: http://127.0.0.1:8000/apidocs
- **API 文档 (Redoc)**: http://127.0.0.1:8000/redoc
- **健康检查**: http://127.0.0.1:8000/health

## API 文档

### 统一响应格式

所有 API 接口返回统一的响应格式：

```json
{
    "code": 0,
    "message": "操作成功",
    "data": {}
}
```

- **code**: 状态码，0 表示成功，非 0 表示失败
- **message**: 响应消息
- **data**: 响应数据

### 状态码说明

| 状态码 | 说明 |
|--------|------|
| 0 | 操作成功 |
| 501 | 操作失败 |
| 401 | 请求头的 auth 为空 |
| 405 | 请求头的 auth 格式错误 |
| 406 | 无效的 Token 或登录过期 |
| 407 | 认证异常 |
| 408 | 用户名不存在 |
| 409 | 验证码不正确 |
| 410 | 密码不正确 |
| 411 | 账号已停用 |
| 412 | 非标准接口 JSON 数据 |

### 示例接口

#### 1. 获取数据 (GET)

```
GET /demo/get
```

#### 2. 创建数据 (POST)

```
POST /demo/post
Content-Type: application/json

{
    "name": "张三",
    "email": "zhangsan@example.com",
    "age": 30,
    "phone": "13800138000",
    "tags": ["技术", "产品"],
    "is_active": true
}
```

#### 3. 更新数据 (PUT)

```
PUT /demo/put
Content-Type: application/json

{
    "name": "张三",
    "email": "zhangsan@example.com",
    "age": 31,
    "phone": "13800138000",
    "tags": ["技术"],
    "is_active": true
}
```

#### 4. 删除数据 (DELETE)

```
DELETE /demo/delete?id=1
```

## 认证说明

### JWT 令牌认证

项目使用 JWT (JSON Web Token) 进行身份验证。

#### 生成令牌

```python
from app.middleware.auth import create_access_token
from datetime import timedelta

token = create_access_token(
    data={"sub": "testuser"},
    expires_delta=timedelta(hours=8)
)
```

#### 使用令牌访问受保护接口

在请求头中添加：

```
Authorization: Bearer <your-jwt-token>
```

#### 受保护的接口示例

```python
from fastapi import Depends
from app.middleware.auth import get_current_user, TokenData

@app.get("/protected")
async def protected_route(current_user: TokenData = Depends(get_current_user)):
    return {"message": f"欢迎 {current_user.username} 访问受保护的接口"}
```

## 数据库配置

### 初始化数据库

项目使用 SQLAlchemy 2.0 作为 ORM，配合 Alembic 进行数据库迁移。

#### 创建数据库模型

在 `app/api/models/` 目录下创建模型文件：

```python
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from app.database import Base

class User(Base):
    """用户模型"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
```

#### 使用 DAO 层

在 `app/api/dao/` 目录下创建数据访问对象：

```python
from sqlalchemy.orm import Session
from app.api.models.user import User

class UserDAO:
    """用户数据访问对象"""

    @staticmethod
    def get_user(db: Session, user_id: int):
        """根据 ID 获取用户"""
        return db.query(User).filter(User.id == user_id).first()

    @staticmethod
    def get_user_by_email(db: Session, email: str):
        """根据邮箱获取用户"""
        return db.query(User).filter(User.email == email).first()

    @staticmethod
    def create_user(db: Session, user_data: dict):
        """创建用户"""
        user = User(**user_data)
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
```

### Alembic 迁移

```bash
# 初始化 Alembic（仅第一次）
alembic init alembic

# 创建迁移脚本
alembic revision --autogenerate -m "initial migration"

# 执行迁移
alembic upgrade head
```

## 配置中间件

### CORS 配置

CORS 中间件已配置在 `app/middleware/cors.py` 中。默认允许所有源，生产环境建议配置具体地址：

```python
origins = [
    "https://example.com",
    "https://app.example.com",
]
```

### 自定义中间件

在 `app/middleware/` 目录下创建中间件文件，然后在 `app/main.py` 的 `create_app()` 函数中添加。

## 日志配置

项目提供了日志处理工具，支持文件日志和控制台输出：

```python
from app.common.util.LogHandler import LogHandler

# 创建日志实例
logger = LogHandler("app", level="INFO")

# 记录日志
logger.info("这是一条信息日志")
logger.warning("这是一条警告日志")
logger.error("这是一条错误日志")
```

日志文件保存在 `logs/` 目录下，按天轮转，保留 15 天。

## 开发规范

### 代码风格

- 遵循 PEP 8 规范
- 使用类型提示
- 所有代码包含中文注释
- 函数长度不超过 50 行，文件长度不超过 500 行

### 命名规范

- 文件/文件夹：小写加下划线（snake_case）
- 类名：大驼峰（PascalCase）
- 函数/变量：小写加下划线（snake_case）
- 常量：全大写下划线分隔（UPPER_SNAKE_CASE）

### 目录结构规范

- 控制器：`xxx_controller.py` 或 `xxx.py`
- 服务：`xxx_service.py`
- 数据访问：`xxx_dao.py`
- 模型：`xxx.py`
- 数据验证：`xxx.py`

### Git 提交规范

使用 Conventional Commits 规范：

```
<type>(<scope>): <subject>

类型：
- feat: 新功能
- fix: 修复bug
- docs: 文档更新
- style: 代码格式调整
- refactor: 重构
- test: 测试相关
- chore: 构建/工具相关
```

## 部署说明

### Docker 部署

创建 `Dockerfile`：

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "run.py"]
```

构建并运行：

```bash
docker build -t fastapi-backend .
docker run -p 8000:8000 --env-file .env fastapi-backend
```

### 使用 Docker Compose

创建 `docker-compose.yml`：

```yaml
version: '3.8'

services:
  app:
    build: .
    ports:
      - "8000:8000"
    env_file:
      - .env
    depends_on:
      - db

  db:
    image: mysql:8.0
    environment:
      MYSQL_ROOT_PASSWORD: password
      MYSQL_DATABASE: fastapi_db
    ports:
      - "3306:3306"
    volumes:
      - mysql_data:/var/lib/mysql

volumes:
  mysql_data:
```

## 测试

### 运行测试

```bash
pytest
```

### 测试覆盖率

```bash
pytest --cov=app tests/
```

## 常见问题

### 1. 如何添加新的 API 接口？

1. 在 `app/api/schemas/` 中创建数据验证模型
2. 在 `app/api/dao/` 中创建数据访问对象
3. 在 `app/api/service/` 中实现业务逻辑
4. 在 `app/api/controller/` 中创建控制器
5. 在 `app/main.py` 中注册路由

### 2. 如何配置数据库连接池？

在 `app/database.py` 中修改 `create_engine` 的参数：

```python
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=3600,
    pool_size=10,
    max_overflow=20,
    echo=settings.APP_DEBUG,
)
```

### 3. 如何修改 JWT 配置？

修改 `.env` 文件中的 JWT 相关配置，或在 `app/config.py` 中修改默认值。

## 许可证

MIT License

## 联系方式

- 作者：南宫乘风
- 邮箱：1794748404@qq.com
