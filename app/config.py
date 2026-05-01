# -*- coding: utf-8 -*-
# @Time    : 2024/5/1
# @Author  : 南宫乘风
# @Email   : 1794748404@qq.com
# @File    : config.py
# @Software: PyCharm
"""
应用配置模块
使用 pydantic-settings 管理环境变量配置
"""
import os
from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """应用配置类"""
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"
    )

    # 应用基本配置
    APP_NAME: str = "FastAPI-Backend"
    APP_ENV: str = "development"
    APP_DEBUG: bool = True
    APP_HOST: str = "0.0.0.0"
    APP_PORT: int = 8000
    SECRET_KEY: str = "your-secret-key-change-this-in-production"

    # 数据库配置
    DB_HOST: str = "127.0.0.1"
    DB_PORT: int = 3306
    DB_USER: str = "root"
    DB_PASSWORD: str = "password"
    DB_DATABASE: str = "fastapi_db"

    # JWT 配置
    JWT_SECRET_KEY: str = "your-jwt-secret-key"
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 480

    # API 配置
    API_V1_PREFIX: str = "/api/v1"

    @property
    def DATABASE_URL(self) -> str:
        """构建数据库连接 URL"""
        return f"mysql+pymysql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_DATABASE}"

    @property
    def IS_DEVELOPMENT(self) -> bool:
        """是否为开发环境"""
        return self.APP_ENV == "development"

    @property
    def IS_PRODUCTION(self) -> bool:
        """是否为生产环境"""
        return self.APP_ENV == "production"


# 基础目录
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# URL 前缀
URL_PATH_PREFIX = "/api"

# 全局配置实例（使用缓存避免重复读取）
@lru_cache()
def get_settings() -> Settings:
    """获取配置单例"""
    return Settings()
