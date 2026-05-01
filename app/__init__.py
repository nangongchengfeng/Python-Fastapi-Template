# -*- coding: utf-8 -*-
# @Time    : 2024/5/1
# @Author  : 南宫乘风
# @Email   : 1794748404@qq.com
# @File    : __init__.py
# @Software: PyCharm
"""
FastAPI 应用包初始化模块
"""
__version__ = "1.0.0"
__author__ = "南宫乘风"
__email__ = "1794748404@qq.com"

# 导出配置和数据库相关对象，方便其他模块导入
from app.config import get_settings, Settings
from app.database import get_db, engine, Base

__all__ = [
    # 版本信息
    "__version__",
    "__author__",
    "__email__",
    # 配置相关
    "get_settings",
    "Settings",
    # 数据库相关
    "get_db",
    "engine",
    "Base",
]
