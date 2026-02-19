# 引入依赖
import uvicorn, os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from datetime import datetime
import platform
from typing import Dict, Any
from core.helper.ContainerCustomLog.index import custom_log

# 加载环境变量
load_dotenv()
os.environ['TZ'] = 'Asia/Shanghai' # 设置时区为上海


# 创建FastAPI应用
app = FastAPI()

# 配置CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# 导入模块
from modules.index.index import app as index_router
# 导入路由
app.include_router(index_router)


# 尝试启动服务器
custom_log("SUCCESS", "Tinder服务器启动中...")
custom_log("SUCCESS", f"===================================================")
custom_log("SUCCESS", f"Python版本: {platform.python_version()}")
custom_log("SUCCESS", f"当前APP_ENV: {os.getenv('APP_ENV', 'not set')}")
custom_log("SUCCESS", f"===================================================")

if __name__ == "__main__":
    try:
        # 根据环境变量设置日志级别
        env = os.getenv('APP_ENV', 'development').lower()
        log_level = "info" if env == "development" else "warning"
        
        uvicorn.run(
            app="server:app",
            host='0.0.0.0',
            port=1912,
            reload=True,
            access_log=False,
            log_level=log_level
        )
    except Exception as e:
        custom_log("ERROR", f"Error starting server: {e}")