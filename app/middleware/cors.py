"""
CORS 中间件配置
处理跨域资源共享问题
"""
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI


def add_cors_middleware(app: FastAPI):
    """
    为 FastAPI 应用添加 CORS 中间件
    :param app: FastAPI 应用实例
    """
    # 允许的源地址
    origins = [
        "*",  # 允许所有源（生产环境建议配置具体地址）
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],  # 允许所有 HTTP 方法
        allow_headers=["*"],  # 允许所有 HTTP 头部
    )
