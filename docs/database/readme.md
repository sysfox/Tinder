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

连接管理器位于 `core/helper/database/connection/`。应用启动时自动连接，停止时自动断开；若连接中途断开，后台线程将以指数退避策略（初始 2 秒，最大 60 秒）持续尝试重连。

### PostgreSQL

```python
from core.helper.database.connection.pgsql import pgsql

# 获取原生 psycopg2 连接对象
conn = pgsql.get_connection()
```

| 方法 | 说明 |
|------|------|
| `pgsql.start()` | 建立连接并启动后台监控线程（由应用 lifespan 自动调用） |
| `pgsql.stop()` | 停止监控并关闭连接（由应用 lifespan 自动调用） |
| `pgsql.get_connection()` | 返回当前活跃的 `psycopg2` 连接，未连接时返回 `None` |

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

所有 DAO 位于 `core/dao/`，继承自 `core/dao/base.py` 的 `BaseDAO`。

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

## 表结构一览

| DAO 文件 | 表名 | 说明 |
|----------|------|------|
| `users.py` | `users` | 用户信息 |
| `tokens.py` | `tokens` | 认证令牌 |
| `tags.py` | `tags` | 标签 |
| `relations.py` | `relations` | 标签关联关系 |
| `songs.py` | `songs` | 歌曲 |
| `song_arrangements.py` | `song_arrangements` | 歌曲编排 |
| `vote.py` | `vote` | 投票 |
| `comments.py` | `comments` | 评论 |
| `favourites.py` | `favourites` | 收藏 |
| `wall_sayings.py` | `wall_sayings` | 表白墙留言 |
| `wall_looking_for.py` | `wall_looking_for` | 寻人/寻物墙 |
| `stores_and_restaurants.py` | `stores_and_restaurants` | 商铺与餐厅 |
| `tasks.py` | `tasks` | 任务 |
| `personal_logs.py` | `personal_logs` | 用户操作日志 |
| `request_logs.py` | `request_logs` | 接口请求统计 |
| `system_logs.py` | `system_logs` | 系统日志 |
| `system_reports.py` | `system_reports` | 系统报告 |

---

## ER 图

- `database-schema.excalidraw` – 数据库表结构 ER 图（可在 [excalidraw.com](https://excalidraw.com) 打开）
- `../db-migration.excalidraw` – 数据库迁移流程图
