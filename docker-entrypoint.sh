#!/bin/bash
set -e

# 运行数据库迁移脚本
echo "Migrate database..."
python3 db_migrate.py

echo "Starting Tinder Server..."

# 启动server.py
python3 server.py
