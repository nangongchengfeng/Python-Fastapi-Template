# -*- coding: utf-8 -*-
# @Time    : 2024/5/1
# @Author  : 南宫乘风
# @Email   : 1794748404@qq.com
# @File    : auth.py
# @Software: PyCharm
"""
JWT 认证中间件
使用 FastAPI 的依赖注入系统实现 JWT 令牌验证
"""
import jwt
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel

from app.config import get_settings

settings = get_settings()


class TokenData(BaseModel):
    """令牌数据模型"""
    username: str


# 安全机制
security = HTTPBearer()


def create_access_token(data: dict, expires_delta: timedelta = None):
    """
    生成 JWT 访问令牌
    :param data: 要加密到令牌中的数据
    :param expires_delta: 过期时间
    :return: JWT 令牌字符串
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    return encoded_jwt


def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """
    验证 JWT 令牌的依赖注入函数
    :param credentials: HTTP 授权凭证
    :return: 解密后的令牌数据
    """
    try:
        token = credentials.credentials
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="无法验证凭证",
                headers={"WWW-Authenticate": "Bearer"},
            )
        token_data = TokenData(username=username)
        return token_data
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="令牌已过期",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="无效的令牌",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"认证异常: {str(e)}",
            headers={"WWW-Authenticate": "Bearer"},
        )


# 认证依赖别名，方便使用
get_current_user = verify_token
