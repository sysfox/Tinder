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
Tinder/
├── .github/                          # GitHub 配置目录
│   └── workflows/                    # GitHub Actions 工作流
│       ├── codeql.yml                # CodeQL 代码安全扫描工作流
│       ├── docker-build.yml          # Docker 镜像构建工作流
│       └── test.yml                  # 自动化测试工作流
├── core/                             # 核心功能模块
│   ├── database/                     # 数据库相关
│   │   ├── connection/               # 数据库连接管理
│   │   │   ├── db.py                 # SQLAlchemy 引擎与会话工厂（ORM 基类 Base）
│   │   │   └── redis.py              # Redis 连接管理
│   │   ├── dao/                      # 数据访问对象（Data Access Object）
│   │   │   ├── base.py               # BaseDAO 基类，提供通用 CRUD 操作
│   │   │   ├── comments.py           # 评论表 ORM 模型与 DAO
│   │   │   ├── favourites.py         # 收藏表 ORM 模型与 DAO
│   │   │   ├── illegal_requests.py   # 违规请求表 ORM 模型与 DAO
│   │   │   ├── personal_logs.py      # 个人日志表 ORM 模型与 DAO
│   │   │   ├── relations.py          # 用户关系表 ORM 模型与 DAO
│   │   │   ├── request_logs.py       # 请求日志表 ORM 模型与 DAO
│   │   │   ├── song_arrangements.py  # 歌曲编排表 ORM 模型与 DAO
│   │   │   ├── songs.py              # 歌曲表 ORM 模型与 DAO
│   │   │   ├── stores_and_restaurants.py # 商店与餐厅表 ORM 模型与 DAO
│   │   │   ├── system_logs.py        # 系统日志表 ORM 模型与 DAO
│   │   │   ├── system_reports.py     # 系统报告表 ORM 模型与 DAO
│   │   │   ├── tags.py               # 标签表 ORM 模型与 DAO
│   │   │   ├── tasks.py              # 任务表 ORM 模型与 DAO
│   │   │   ├── tokens.py             # 令牌表 ORM 模型与 DAO
│   │   │   ├── users.py              # 用户表 ORM 模型与 DAO
│   │   │   ├── vote.py               # 投票表 ORM 模型与 DAO
│   │   │   ├── wall_looking_for.py   # 寻找墙贴表 ORM 模型与 DAO
│   │   │   └── wall_sayings.py       # 说说墙贴表 ORM 模型与 DAO
│   │   └── migrations/               # 数据库迁移管理
│   │       ├── SQL/                  # SQL 迁移脚本目录
│   │       │   ├── alter_users_add_password.sql      # 用户表新增密码字段
│   │       │   ├── initial_comments.sql              # 评论表初始化
│   │       │   ├── initial_favourites.sql            # 收藏表初始化
│   │       │   ├── initial_illegal_requests.sql      # 违规请求表初始化
│   │       │   ├── initial_migration_user.sql        # 用户表初始化
│   │       │   ├── initial_personal_logs.sql         # 个人日志表初始化
│   │       │   ├── initial_relations.sql             # 用户关系表初始化
│   │       │   ├── initial_request_logs.sql          # 请求日志表初始化
│   │       │   ├── initial_song_arrangements.sql     # 歌曲编排表初始化
│   │       │   ├── initial_songs.sql                 # 歌曲表初始化
│   │       │   ├── initial_stores_and_restaurants.sql # 商店与餐厅表初始化
│   │       │   ├── initial_system_logs.sql           # 系统日志表初始化
│   │       │   ├── initial_system_reports.sql        # 系统报告表初始化
│   │       │   ├── initial_tags.sql                  # 标签表初始化
│   │       │   ├── initial_tasks.sql                 # 任务表初始化
│   │       │   ├── initial_tokens.sql                # 令牌表初始化
│   │       │   ├── initial_vote.sql                  # 投票表初始化
│   │       │   ├── initial_wall_looking_for.sql      # 寻找墙贴表初始化
│   │       │   └── initial_wall_sayings.sql          # 说说墙贴表初始化
│   │       └── migration_history.py  # 迁移脚本执行顺序列表
│   ├── helper/                       # 通用辅助工具
│   │   └── ContainerCustomLog/       # 自定义日志模块
│   │       └── index.py              # 带颜色与时间戳的控制台日志工具
│   └── middleware/                   # 中间件
│       └── firewall/                 # 防火墙/访问控制中间件
│           ├── config.py             # 防火墙规则配置
│           ├── helpers.py            # 防火墙辅助函数
│           ├── index.py              # 对外暴露 FirewallMiddleware
│           └── middleware.py         # 防火墙中间件实现（IP 封禁、限流等）
├── docs/                             # 项目文档
│   └── database/                     # 数据库相关文档
│       ├── db-migration.excalidraw   # 数据库迁移流程图（Excalidraw 格式）
│       └── readme.md                 # 数据库说明文档
├── modules/                          # 业务功能模块
│   └── index/                        # 根路由模块
│       └── index.py                  # 根路由（GET /），返回系统信息
├── tests/                            # 测试目录
│   ├── integration/                  # 集成测试
│   │   ├── conftest.py               # pytest 集成测试夹具配置
│   │   ├── test_api.py               # API 接口集成测试
│   │   └── test_firewall.py          # 防火墙中间件集成测试
│   └── unit/                         # 单元测试
│       ├── test_custom_log.py        # 自定义日志模块单元测试
│       ├── test_firewall_helpers.py  # 防火墙辅助函数单元测试
│       └── test_index_router.py      # 根路由单元测试
├── .env.example                      # 环境变量示例文件（数据库/Redis 配置模板）
├── .gitignore                        # Git 忽略规则
├── Dockerfile                        # Docker 镜像构建文件
├── LICENSE                           # 开源许可证
├── README.md                         # 项目说明文档（本文件）
├── db_migrate.py                     # 数据库迁移入口脚本（使用 psycopg2 执行 SQL）
├── docker-entrypoint.sh              # Docker 容器启动脚本
├── pytest.ini                        # pytest 配置文件
├── requirements.txt                  # Python 依赖列表
└── server.py                         # FastAPI 应用入口，配置中间件与路由
```

## API 文档

启动服务后访问 `http://localhost:1912/docs` 查看Swagger文档
