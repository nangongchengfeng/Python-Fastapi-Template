"""
生产环境启动脚本
使用 Uvicorn 启动 FastAPI 应用
"""
import os
import sys
import uvicorn

# 获取当前文件的绝对路径
current_file = os.path.abspath(__file__)
base_dir = os.path.dirname(current_file)

# 将项目目录添加到 sys.path
if base_dir not in sys.path:
    sys.path.append(base_dir)

# 获取运行环境（开发/测试/生产）
env = os.getenv("APP_ENV", "development")

# 配置信息
config = {
    "development": {
        "host": "0.0.0.0",
        "port": 8000,
        "reload": True,
        "log_level": "debug"
    },
    "testing": {
        "host": "0.0.0.0",
        "port": 8000,
        "reload": False,
        "log_level": "info"
    },
    "production": {
        "host": "0.0.0.0",
        "port": 8000,
        "reload": False,
        "log_level": "warning",
        "workers": 4  # 生产环境使用 4 个工作进程
    }
}

# 获取当前环境的配置
current_config = config.get(env, config["development"])

print(f"🚀 启动 FastAPI 服务...")
print(f"🌍 运行环境: {env}")
print(f"📡 监听地址: http://{current_config['host']}:{current_config['port']}")
print(f"📚 API 文档: http://{current_config['host']}:{current_config['port']}/apidocs")
print(f"🔧 Redoc 文档: http://{current_config['host']}:{current_config['port']}/redoc")

# 启动应用
uvicorn.run(
    "app.main:app",
    host=current_config["host"],
    port=current_config["port"],
    reload=current_config["reload"],
    log_level=current_config["log_level"],
    workers=current_config.get("workers", 1)
)
