# -*- coding: utf-8 -*-
# @Time    : 2024/5/2
# @Author  : 南宫乘风
# @Email   : 1794748404@qq.com
# @File    : result.py
# @Software: PyCharm
"""
统一响应结果模块
提供标准化的 API 响应格式
"""
from typing import Any, Optional, Generic, TypeVar
from pydantic import BaseModel, Field

# 定义泛型类型
T = TypeVar("T")


class Result(BaseModel, Generic[T]):
    """统一响应结果类"""
    code: int = Field(..., description="响应状态码，0 表示成功，非 0 表示失败")
    message: str = Field(..., description="响应消息")
    data: Optional[T] = Field(None, description="响应数据")

    @classmethod
    def success(cls, data: Optional[Any] = None, message: str = "操作成功") -> "Result[Any]":
        """
        成功响应
        :param data: 响应数据
        :param message: 响应消息
        :return: Result 对象
        """
        return cls(code=0, message=message, data=data)

    @classmethod
    def failed(cls, code: int = 501, message: str = "操作失败") -> "Result[Any]":
        """
        失败响应
        :param code: 错误状态码
        :param message: 错误消息
        :return: Result 对象
        """
        return cls(code=code, message=message, data=None)
