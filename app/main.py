"""
FastAPI 应用入口文件
包含应用创建、中间件配置、路由注册等
"""
from fastapi import FastAPI, Depends
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from app.middleware.cors import add_cors_middleware
from app.middleware.auth import get_current_user, TokenData
from app.api.controller.demo import router as demo_router

__author__ = '南宫乘风'
__version__ = '1.0.0'


def create_app() -> FastAPI:
    """
    创建并配置 FastAPI 应用
    :return: 配置好的 FastAPI 应用实例
    """
    # 创建 FastAPI 应用实例
    app = FastAPI(
        title="Python FastAPI Template",
        description="基于 FastAPI 的 Python 后端服务模板",
        version="1.0.0",
        docs_url="/apidocs",
        redoc_url="/redoc",
        openapi_url="/openapi.json"
    )

    # 配置 CORS 中间件
    add_cors_middleware(app)

    # 注册路由
    app.include_router(demo_router)

    # 健康检查接口
    @app.get("/health")
    async def health_check():
        """健康检查接口"""
        return {"status": "healthy", "version": "1.0.0"}

    # 受保护的示例接口
    @app.get("/protected")
    async def protected_route(current_user: TokenData = Depends(get_current_user)):
        """
        受保护的示例接口
        需要提供有效的 JWT 令牌才能访问
        """
        return {"message": f"欢迎 {current_user.username} 访问受保护的接口"}

    return app


# 创建应用实例
app = create_app()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
