# Tinder

航海家计划后端API服务

## 技术栈

- **框架**: FastAPI
- **数据库**: PostgreSQL
- **缓存**: Redis
- **部署**: Docker

## 快速开始

### 环境要求

- Python 3.8+
- PostgreSQL
- Redis

### 本地开发

1. 安装依赖
```bash
pip install -r requirements.txt
```

2. 配置环境变量
```bash
cp .env.example .env
# 编辑.env文件设置数据库和Redis连接信息
```

3. 数据库迁移
```bash
python db_migrate.py
```

4. 运行服务
```bash
python server.py
```

服务将在 `http://localhost:1912` 启动

### Docker 部署

```bash
docker build -t tinder .
docker run -p 1912:1912 tinder
```

## 项目结构

```
├── modules/          # 功能模块（用户、索引等）
├── core/            # 核心功能（数据库迁移）
├── docs/            # 文档
├── server.py        # 主应用入口
├── db_migrate.py    # 数据库迁移管理
└── requirements.txt # 项目依赖
```

## ORM 支持

项目从 psycopg2 + 手写 SQL 逐步迁移到 **SQLAlchemy 2.x ORM**，详情见 [数据库文档](docs/database/readme.md#orm-层使用)。

- ORM 基础设施位于 `core/database/orm/`，包含声明式基类、Session 管理和示例模型。
- 新表 / 新功能应优先使用 ORM，旧 DAO 暂时保留，不影响现有行为。

## API 文档

启动服务后访问 `http://localhost:1912/docs` 查看Swagger文档
