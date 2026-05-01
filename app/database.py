# -*- coding: utf-8 -*-
# @Time    : 2024/5/1
# @Author  : 南宫乘风
# @Email   : 1794748404@qq.com
# @File    : database.py
# @Software: PyCharm
"""
数据库配置模块
使用 SQLAlchemy 2.0 声明式语法
"""
from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session, DeclarativeBase

from app.config import get_settings

settings = get_settings()

# 同步引擎（用于 Alembic 和同步操作）
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=3600,
    echo=settings.APP_DEBUG,
)

# 同步会话工厂
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# 声明式基类
class Base(DeclarativeBase):
    """SQLAlchemy 声明式基类"""
    pass


# 数据库会话依赖注入
def get_db() -> Generator[Session, None, None]:
    """
    获取数据库会话
    用于 FastAPI Depends 依赖注入
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
