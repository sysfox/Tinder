# 数据库使用指南

本目录包含 Tinder 项目的数据库设计文档与 ER 图。

---

## 目录

- [环境配置](#环境配置)
- [数据库连接管理](#数据库连接管理)
  - [PostgreSQL](#postgresql)
  - [Redis](#redis)
- [DAO 层使用](#dao-层使用)
  - [通用 CRUD](#通用-crud)
  - [特殊 DAO 说明](#特殊-dao-说明)
- [ORM 层使用](#orm-层使用)
  - [背景与目标](#背景与目标)
  - [目录结构](#目录结构)
  - [UsersRepository 示例](#usersrepository-示例)
  - [开发规范](#开发规范)
- [表结构一览](#表结构一览)
- [ER 图](#er-图)

---

## 环境配置

在项目根目录复制 `.env.example` 为 `.env`，并按实际环境填写连接字符串：

```env
# PostgreSQL 连接字符串
DATABASE_URL=postgresql://postgres:password@localhost:5432/tinder

# Redis 连接字符串
REDIS_URL=redis://localhost:6379/0
```

---

## 数据库连接管理

PostgreSQL 连接由 SQLAlchemy Engine 统一管理，应用启动时自动验证连接，停止时调用 `dispose_engine()` 关闭连接池。Redis 连接管理器独立运行。

### PostgreSQL（ORM 引擎）

```python
from core.database.orm.session import get_session

with get_session() as session:
    # 在 session 内执行 ORM 操作
    ...
```

| 函数/方法 | 说明 |
|-----------|------|
| `get_session()` | 上下文管理器，提供线程安全的 SQLAlchemy Session |
| `dispose_engine()` | 释放连接池（由应用 lifespan 自动调用） |

### Redis

```python
from core.helper.database.connection.redis import redis_conn

# 获取 redis-py 客户端
client = redis_conn.get_client()
client.set("key", "value")
value = client.get("key")
```

| 方法 | 说明 |
|------|------|
| `redis_conn.start()` | 建立连接并启动后台监控线程（由应用 lifespan 自动调用） |
| `redis_conn.stop()` | 停止监控并关闭连接（由应用 lifespan 自动调用） |
| `redis_conn.get_client()` | 返回当前活跃的 `redis.Redis` 客户端，未连接时返回 `None` |

---

## DAO 层使用

所有 DAO 位于 `core/database/dao/`，继承自 `core/database/dao/base.py` 的 `BaseDAO`，底层使用 **SQLAlchemy 2.x ORM**。

### 通用 CRUD

以 `UsersDAO` 为例：

```python
from core.dao.users import UsersDAO

dao = UsersDAO()

# 查询单条（按 uuid）
user = dao.find_by_uuid("xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx")

# 分页查询
users = dao.find_all(limit=20, offset=0)

# 插入
new_user = dao.create({
    "uuid": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
    "nickname": "张三",
    "user_role": "user",
})

# 更新
updated = dao.update("xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx", {"nickname": "李四"})

# 删除
success = dao.delete("xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx")
```

### 特殊 DAO 说明

#### `RelationsDAO`

`relations` 表没有独立的 `uuid` 字段，请使用以下方法：

| 方法 | 说明 |
|------|------|
| `find_by_id(id)` | 按主键 id 查询 |
| `find_by_tags_uuid(tags_uuid)` | 按 tags_uuid 查询关联记录列表 |
| `update_by_id(id, data)` | 按主键 id 更新 |
| `delete_by_id(id)` | 按主键 id 删除 |

#### `RequestLogsDAO`

`request_logs` 表以 `request_path` 作为唯一键，请使用以下方法：

| 方法 | 说明 |
|------|------|
| `find_by_path(path)` | 按 request_path 查询 |
| `upsert_by_path(path)` | 不存在则插入，存在则 frequency +1 |
| `delete_by_path(path)` | 按 request_path 删除 |

#### `TokensDAO`

在基础 CRUD 之外额外提供：

| 方法 | 说明 |
|------|------|
| `find_by_belong_to(belong_to)` | 查询指定用户的所有 token |
| `find_active_by_belong_to(belong_to)` | 查询指定用户的所有未过期 token |

---

## ORM 层

所有 DAO 已全量迁移至 SQLAlchemy 2.x ORM，原 psycopg2 手写 SQL 层已移除。

### 目录结构

```
core/database/orm/
├── __init__.py
├── base.py        # DeclarativeBase + Engine/Session 工厂
├── session.py     # get_session() 上下文管理器、dispose_engine()
└── models/        # 每个表对应一个 ORM 模型文件
    ├── users.py
    ├── tokens.py
    ├── comments.py
    ├── favourites.py
    ├── illegal_requests.py
    ├── personal_logs.py
    ├── relations.py
    ├── request_logs.py
    ├── song_arrangements.py
    ├── songs.py
    ├── stores_and_restaurants.py
    ├── system_logs.py
    ├── system_reports.py
    ├── tags.py
    ├── tasks.py
    ├── vote.py
    ├── wall_looking_for.py
    └── wall_sayings.py
```

### 开发规范

1. **新表必须先写 ORM 模型**：在 `core/database/orm/models/` 中新增模型文件，字段定义与 SQL 迁移文件保持一致。
2. **新 DAO 继承 BaseDAO**：在 `core/database/dao/` 中新增 DAO 文件，设置 `MODEL` 属性指向对应的 ORM 模型类。
3. **Session 生命周期**：始终通过 `get_session()` 上下文管理器使用 Session，禁止在函数外持有 Session 引用。

---

## 表结构一览

| DAO 文件 | ORM 模型 | 表名 | 说明 |
|----------|----------|------|------|
| `users.py` | `User` | `users` | 用户信息 |
| `tokens.py` | `Token` | `tokens` | 认证令牌 |
| `tags.py` | `Tag` | `tags` | 标签 |
| `relations.py` | `Relation` | `relations` | 标签关联关系 |
| `songs.py` | `Song` | `songs` | 歌曲 |
| `song_arrangements.py` | `SongArrangement` | `song_arrangements` | 歌曲编排 |
| `vote.py` | `Vote` | `vote` | 投票 |
| `comments.py` | `Comment` | `comments` | 评论 |
| `favourites.py` | `Favourite` | `favourites` | 收藏 |
| `wall_sayings.py` | `WallSaying` | `wall_sayings` | 表白墙留言 |
| `wall_looking_for.py` | `WallLookingFor` | `wall_looking_for` | 寻人/寻物墙 |
| `stores_and_restaurants.py` | `StoreOrRestaurant` | `stores_and_restaurants` | 商铺与餐厅 |
| `tasks.py` | `Task` | `tasks` | 任务 |
| `personal_logs.py` | `PersonalLog` | `personal_logs` | 用户操作日志 |
| `request_logs.py` | `RequestLog` | `request_logs` | 接口请求统计 |
| `system_logs.py` | `SystemLog` | `system_logs` | 系统日志 |
| `system_reports.py` | `SystemReport` | `system_reports` | 系统报告 |
| `illegal_requests.py` | `IllegalRequest` | `illegal_requests` | 违规请求记录 |

---

## ER 图

- `database-schema.excalidraw` – 数据库表结构 ER 图（可在 [excalidraw.com](https://excalidraw.com) 打开）
- `../db-migration.excalidraw` – 数据库迁移流程图
