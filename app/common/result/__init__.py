"""统一响应格式处理模块"""

from .result import Result
from .code import codes, get_message

__all__ = ["Result", "codes", "get_message"]
