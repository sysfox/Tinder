import platform
from datetime import datetime
from typing import Dict, Any
from fastapi import APIRouter

# 获取系统信息
def get_system_info() -> Dict[str, Any]:
    """获取应用的系统信息"""
    return {
        "name": "Tinder",
        "system_time": datetime.now(),
        "system_version": platform.platform()
    }

# 根路由
app = APIRouter()
@app.get("/")
async def root():
    """返回应用的系统信息"""
    return get_system_info()