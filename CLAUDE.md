# FastAPI 项目开发规范

## 技术栈

| 技术              | 版本要求 |
| ----------------- | -------- |
| Python            | 3.8+     |
| FastAPI           | 0.104+   |
| Uvicorn           | 0.24+    |
| Pydantic          | 2.5+     |
| Pydantic Settings | 2.1+     |
| SQLAlchemy        | 2.0+     |
| PyMySQL           | 1.1+     |
| Alembic           | 1.13+    |
| Python-JOSE       | 3.3+     |
| uv                | -        |

## 目录结构

```
project/
├── app/
│   ├── __init__.py              # 包初始化
│   ├── config.py                # 配置管理
│   ├── database.py              # 数据库配置
│   ├── main.py                  # 应用入口
│   ├── api/
│   │   ├── controller/          # 控制器层
│   │   ├── service/             # 服务层
│   │   ├── dao/                 # 数据访问层
│   │   ├── models/              # 数据模型
│   │   └── schemas/             # 数据验证模型
│   ├── middleware/              # 中间件（auth, cors）
│   └── common/                  # 公共模块（result, util）
├── logs/                        # 日志目录
├── scripts/                     # 脚本目录
├── tests/                       # 测试目录
├── pyproject.toml               # uv 项目配置
├── requirements.txt             # Python 依赖
├── .env.example                 # 环境变量示例
├── run.py                       # 启动脚本
└── README.md                    # 项目说明文档
```

## 核心原则

1. **分层清晰**：Controller → Service → DAO → Model
2. **中文注释**：所有代码必须包含中文注释
3. **接口文档**：所有接口必须写 docstring
4. **代码限制**：函数≤50行，文件≤500行
5. **统一响应**：所有 API 返回 Result 格式

## 命名规范

| 类型      | 规范         | 示例                      |
| --------- | ------------ | ------------------------- |
| 文件      | 小写加下划线 | `user_controller.py`      |
| 类        | 大驼峰       | `UserController`          |
| 函数/变量 | 小写加下划线 | `get_user()`, `user_name` |
| 常量      | 全大写下划线 | `SECRET_KEY`              |

## 分层架构

### Controller 层

```python
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.common.result import Result
from app.api.schemas.user import UserCreate
from app.api.service.user_service import UserService
from app.database import get_db

router = APIRouter(prefix="/users", tags=["用户管理"])

@router.get("/{user_id}", summary="获取用户详情")
def get_user(user_id: int, db: Session = Depends(get_db)):
    """根据用户 ID 获取用户详情"""
    user = UserService.get_user_by_id(db, user_id)
    return Result.success(data=user)
```

### Service 层

```python
from typing import Optional
from sqlalchemy.orm import Session
from app.api.dao.user_dao import UserDAO

class UserService:
    """用户服务类"""

    @staticmethod
    def get_user_by_id(db: Session, user_id: int) -> Optional[User]:
        """根据 ID 获取用户"""
        return UserDAO.get_user_by_id(db, user_id)

    @staticmethod
    def create_user(db: Session, user_data: UserCreate) -> User:
        """创建用户"""
        return UserDAO.create_user(db, user_data.model_dump())
```

### DAO 层

```python
from typing import Optional, List
from sqlalchemy.orm import Session
from app.api.models.user import User

class UserDAO:
    """用户数据访问对象"""

    @staticmethod
    def get_user_by_id(db: Session, user_id: int) -> Optional[User]:
        """根据 ID 获取用户"""
        return db.query(User).filter(User.id == user_id).first()

    @staticmethod
    def create_user(db: Session, user_data: dict) -> User:
        """创建用户"""
        user = User(**user_data)
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
```

### Model 层

```python
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from app.database import Base

class User(Base):
    """用户模型"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, comment="主键 ID")
    username = Column(String(50), unique=True, index=True, nullable=False, comment="用户名")
    email = Column(String(100), unique=True, index=True, nullable=False, comment="邮箱")
    is_active = Column(Boolean, default=True, nullable=False, comment="是否激活")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="创建时间")
```

### Schema 层

```python
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, EmailStr

class UserBase(BaseModel):
    """用户基础模型"""
    username: str = Field(..., min_length=3, max_length=50, description="用户名")
    email: EmailStr = Field(..., description="邮箱")

class UserCreate(UserBase):
    """创建用户请求模型"""
    password: str = Field(..., min_length=6, description="密码")

class UserResponse(UserBase):
    """用户响应模型"""
    id: int
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True
```

## 配置管理

### config.py

```python
from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """应用配置类"""
    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True)

    APP_NAME: str = "FastAPI-Backend"
    APP_ENV: str = "development"
    APP_DEBUG: bool = True
    APP_HOST: str = "0.0.0.0"
    APP_PORT: int = 8000
    SECRET_KEY: str = "your-secret-key"

    DB_HOST: str = "127.0.0.1"
    DB_PORT: int = 3306
    DB_USER: str = "root"
    DB_PASSWORD: str = "password"
    DB_DATABASE: str = "fastapi_db"

    JWT_SECRET_KEY: str = "your-jwt-secret-key"
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 480

    @property
    def DATABASE_URL(self) -> str:
        return f"mysql+pymysql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_DATABASE}"

@lru_cache()
def get_settings() -> Settings:
    return Settings()
```

## 数据库配置

### database.py

```python
from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session, DeclarativeBase
from app.config import get_settings

settings = get_settings()

engine = create_engine(settings.DATABASE_URL, pool_pre_ping=True, pool_recycle=3600, echo=settings.APP_DEBUG)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Base(DeclarativeBase):
    """SQLAlchemy 声明式基类"""
    pass

def get_db() -> Generator[Session, None, None]:
    """获取数据库会话"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

## 统一响应格式

### Result 类

```python
from typing import Any, Optional, Generic, TypeVar
from pydantic import BaseModel, Field

T = TypeVar("T")

class Result(BaseModel, Generic[T]):
    """统一响应结果类"""
    code: int = Field(..., description="响应状态码，0 表示成功")
    message: str = Field(..., description="响应消息")
    data: Optional[T] = Field(None, description="响应数据")

    @classmethod
    def success(cls, data: Optional[Any] = None, message: str = "操作成功") -> "Result[Any]":
        return cls(code=0, message=message, data=data)

    @classmethod
    def failed(cls, code: int = 501, message: str = "操作失败") -> "Result[Any]":
        return cls(code=code, message=message, data=None)
```

## 应用入口

### main.py

```python
from fastapi import FastAPI
from app.middleware.cors import add_cors_middleware
from app.api.controller.demo import router as demo_router

def create_app() -> FastAPI:
    app = FastAPI(title="FastAPI Backend", docs_url="/apidocs", redoc_url="/redoc")
    add_cors_middleware(app)
    app.include_router(demo_router)

    @app.get("/health")
    async def health_check():
        return {"status": "healthy"}
    return app

app = create_app()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

## 启动脚本

### run.py

```python
import uvicorn
from app.config import get_settings

settings = get_settings()

if __name__ == "__main__":
    if settings.APP_ENV == "production":
        uvicorn.run("app.main:app", host=settings.APP_HOST, port=settings.APP_PORT, workers=4)
    else:
        uvicorn.run("app.main:app", host=settings.APP_HOST, port=settings.APP_PORT, reload=True)
```

## 依赖管理

### requirements.txt

```txt
fastapi>=0.104.1
uvicorn>=0.24.0
pydantic>=2.5.0
pydantic-settings>=2.1.0
sqlalchemy>=2.0.23
pymysql>=1.1.0
alembic>=1.13.1
python-jose[cryptography]>=3.3.0
passlib[bcrypt]>=1.7.4
python-multipart>=0.0.6
apscheduler>=3.10.4
python-dotenv>=1.0.0
```

## Git 规范

### .gitignore

```txt
__pycache__/
*.py[cod]
.venv/
venv/
.env
.env.local
logs/
*.log
.DS_Store
.pytest_cache/
```

### Git 提交规范

```
<type>: <subject>

类型：
- feat: 新功能
- fix: 修复bug
- docs: 文档更新
- style: 代码格式调整
- refactor: 重构
- test: 测试相关
- chore: 构建/工具相关
```

## 代码审查清单

- [ ] 代码符合分层架构规范
- [ ] 所有函数和类都有中文注释
- [ ] 函数≤50行，文件≤500行
- [ ] 使用正确的命名规范
- [ ] API 接口有完整的 docstring
- [ ] 所有 API 返回统一的 Result 格式
- [ ] 使用 Pydantic 进行参数验证
- [ ] 没有直接在 Controller 层写 SQL
- [ ] 配置都使用 settings 管理
- [ ] 数据库操作都通过 DAO 层

## 创建新模块步骤

1. **创建 Schema** - `app/api/schemas/`
2. **创建 Model** - `app/api/models/`
3. **创建 DAO** - `app/api/dao/`
4. **创建 Service** - `app/api/service/`
5. **创建 Controller** - `app/api/controller/`
6. **注册路由** - `app/main.py`
