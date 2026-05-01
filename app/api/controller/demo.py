"""
示例 API 控制器
包含常见的 CRUD 操作示例接口
"""

from fastapi import APIRouter, Query
from app.common.result import Result
from app.api.schemas.demo import DemoRequest
from datetime import datetime


# 创建路由实例
router = APIRouter(prefix="/demo", tags=["示例接口"])


@router.get("/get", tags=["示例接口"], summary="获取数据接口")
def get_example():
    """
    示例 GET 请求接口

    获取示例数据，演示基本的查询操作

    Returns:
        Result: 统一响应格式，包含示例数据
    """
    return Result.success(data={"message": "这是 GET 请求的示例响应"})


@router.post("/post", tags=["示例接口"], summary="创建数据接口")
def post_example(request: DemoRequest):
    """
    示例 POST 请求接口

    处理数据创建操作，演示请求参数验证和处理

    Args:
        request: 包含 name、email 等字段的请求体

    Returns:
        Result: 统一响应格式，包含处理后的数据
    """
    # 处理 POST 请求的业务逻辑
    response_data = {
        "id": 1,
        "name": request.name,
        "email": request.email,
        "age": request.age,
        "phone": request.phone,
        "tags": request.tags,
        "is_active": request.is_active,
        "status": "active",
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat()
    }
    return Result.success(data=response_data, message="数据已成功创建")


@router.put("/put", tags=["示例接口"], summary="更新数据接口")
def put_example(request: DemoRequest):
    """
    示例 PUT 请求接口

    处理数据更新操作，演示请求参数验证和处理

    Args:
        request: 包含 name、email 等字段的请求体

    Returns:
        Result: 统一响应格式，包含处理后的数据
    """
    # 处理 PUT 请求的业务逻辑
    response_data = {
        "id": 1,
        "name": request.name,
        "email": request.email,
        "age": request.age,
        "phone": request.phone,
        "tags": request.tags,
        "is_active": request.is_active,
        "status": "active",
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat()
    }
    return Result.success(data=response_data, message="数据已成功更新")


@router.delete("/delete", tags=["示例接口"], summary="删除数据接口")
def delete_example(id: int = Query(..., description="要删除的数据 ID")):
    """
    示例 DELETE 请求接口

    处理数据删除操作，演示查询参数的使用

    Args:
        id: 要删除的数据 ID

    Returns:
        Result: 统一响应格式，包含处理后的结果
    """
    # 处理 DELETE 请求的业务逻辑
    return Result.success(data={"id": id}, message="数据已成功删除")
