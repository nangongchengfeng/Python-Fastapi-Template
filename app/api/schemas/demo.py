"""
示例 API 数据模型
包含演示用的请求、响应和查询参数模型
"""

from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, field_validator, EmailStr


class DemoQuery(BaseModel):
    """
    查询参数模型
    用于 GET 请求的查询参数验证
    """
    page: int = Field(
        default=1,
        ge=1,
        description="页码，从 1 开始",
        examples=[1]
    )
    page_size: int = Field(
        default=10,
        ge=1,
        le=100,
        description="每页数量，最大 100",
        examples=[10]
    )
    keyword: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=100,
        description="搜索关键词",
        examples=["测试"]
    )
    status: Optional[str] = Field(
        default=None,
        description="状态筛选",
        examples=["active"]
    )
    
    @field_validator("status")
    @classmethod
    def validate_status(cls, v: Optional[str]) -> Optional[str]:
        """验证状态值是否在允许的范围内"""
        if v is None:
            return v
        allowed_statuses = {"active", "inactive", "pending"}
        if v not in allowed_statuses:
            raise ValueError(f"状态必须是以下之一: {', '.join(allowed_statuses)}")
        return v


class DemoRequest(BaseModel):
    """
    请求参数模型
    用于 POST 和 PUT 请求的请求体验证
    """
    name: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="姓名",
        examples=["张三"]
    )
    email: EmailStr = Field(
        ...,
        description="邮箱地址",
        examples=["zhangsan@example.com"]
    )
    age: Optional[int] = Field(
        default=None,
        ge=0,
        le=150,
        description="年龄",
        examples=[30]
    )
    phone: Optional[str] = Field(
        default=None,
        min_length=11,
        max_length=11,
        description="手机号码",
        examples=["13800138000"]
    )
    tags: Optional[List[str]] = Field(
        default=None,
        description="标签列表",
        examples=[["技术", "产品"]]
    )
    is_active: bool = Field(
        default=True,
        description="是否激活",
        examples=[True]
    )

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, v: Optional[str]) -> Optional[str]:
        """验证手机号码格式"""
        if v is None:
            return v
        if not v.isdigit() or len(v) != 11:
            raise ValueError("手机号码必须是 11 位数字")
        if not v.startswith(("13", "14", "15", "16", "17", "18", "19")):
            raise ValueError("手机号码格式不正确")
        return v


class DemoResponse(BaseModel):
    """
    响应数据模型
    用于返回 API 响应结果
    """
    id: int = Field(
        ...,
        description="唯一标识符",
        examples=[1]
    )
    name: str = Field(
        ...,
        description="姓名",
        examples=["张三"]
    )
    email: str = Field(
        ...,
        description="邮箱地址",
        examples=["zhangsan@example.com"]
    )
    age: Optional[int] = Field(
        default=None,
        description="年龄",
        examples=[30]
    )
    phone: Optional[str] = Field(
        default=None,
        description="手机号码",
        examples=["13800138000"]
    )
    tags: Optional[List[str]] = Field(
        default=None,
        description="标签列表",
        examples=[["技术", "产品"]]
    )
    is_active: bool = Field(
        ...,
        description="是否激活",
        examples=[True]
    )
    status: str = Field(
        ...,
        description="状态",
        examples=["active"]
    )
    created_at: datetime = Field(
        ...,
        description="创建时间",
        examples=[datetime(2024, 1, 1, 10, 30)]
    )
    updated_at: datetime = Field(
        ...,
        description="更新时间",
        examples=[datetime(2024, 1, 1, 10, 30)]
    )

    class Config:
        """配置类"""
        from_attributes = True
