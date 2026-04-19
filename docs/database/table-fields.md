# 数据库字段详细说明

> 数据来源：`core/database/migrations/SQL/*.sql`（含 `users` 的 `ALTER` 迁移）。
>
> 说明：
> - “可能的值”优先写明数据库层已明确的默认值、约束或布尔取值。
> - 若数据库未限制枚举，则标注为“任意文本/自由值（由业务约定）”。

---

## users（用户信息）

| 字段 | 类型 | 作用 | 可能的值 / 约束 |
|---|---|---|---|
| id | SERIAL | 自增主键 | 主键，自增整数 |
| uuid | TEXT | 用户唯一标识 | 非空、唯一，通常为 UUID 字符串 |
| avatar_url | TEXT | 头像地址 | 任意文本（通常为 URL） |
| nickname | TEXT | 昵称 | 任意文本 |
| real_name | TEXT | 真实姓名 | 任意文本 |
| class | TEXT | 班级信息 | 任意文本 |
| class_type | TEXT | 班级类型/类别 | 任意文本 |
| joined_at | TIMESTAMP | 注册/加入时间 | 默认 `CURRENT_TIMESTAMP` |
| current_status | TEXT | 当前状态 | 任意文本（如 online/offline 等，业务约定） |
| last_login_at | TIMESTAMP | 最近登录时间 | 时间戳或 `NULL` |
| last_login_ip | TEXT | 最近登录 IP | 任意文本（通常为 IPv4/IPv6） |
| score | INTEGER | 积分 | 默认 `0` |
| user_role | TEXT | 用户角色 | 任意文本（如 admin/user，业务约定） |
| title | TEXT | 用户头衔 | 任意文本 |
| invited_by | TEXT | 邀请人标识 | 任意文本 |
| views | INTEGER | 被浏览次数 | 默认 `0` |
| other_info | JSONB | 扩展信息 | JSON 对象 |
| is_verified | BOOLEAN | 是否认证 | `true` / `false` / `NULL` |
| username | TEXT | 用户名（登录） | 唯一，可 `NULL` |
| email | TEXT | 邮箱（登录） | 唯一，可 `NULL` |
| password | TEXT | 登录密码（哈希后） | 任意文本（建议仅存哈希） |

---

## tokens（认证令牌）

| 字段 | 类型 | 作用 | 可能的值 / 约束 |
|---|---|---|---|
| id | SERIAL | 自增主键 | 主键，自增整数 |
| uuid | TEXT | 令牌记录唯一标识 | 非空、唯一 |
| belong_to | TEXT | 令牌所属用户标识 | 非空，已建索引 `idx_tokens_belong_to` |
| permission | TEXT | 令牌权限范围 | 非空，任意文本（业务约定） |
| assigner | TEXT | 发放者标识 | 任意文本 |
| created_at | TIMESTAMP | 创建时间 | 默认 `CURRENT_TIMESTAMP` |
| expired_at | TIMESTAMP | 过期时间 | 时间戳或 `NULL`，已建索引 `idx_tokens_expired_at` |
| current_status | TEXT | 当前状态 | 任意文本（如 active/revoked，业务约定） |

---

## tags（标签）

| 字段 | 类型 | 作用 | 可能的值 / 约束 |
|---|---|---|---|
| id | SERIAL | 自增主键 | 主键，自增整数 |
| uuid | TEXT | 标签唯一标识 | 非空、唯一 |
| created_at | TIMESTAMP | 创建时间 | 默认 `CURRENT_TIMESTAMP` |
| tag_name | TEXT | 标签名称 | 非空，任意文本 |
| created_by | TEXT | 创建者标识 | 任意文本 |
| current_status | TEXT | 标签状态 | 任意文本（业务约定） |

---

## relations（标签关系）

| 字段 | 类型 | 作用 | 可能的值 / 约束 |
|---|---|---|---|
| id | SERIAL | 自增主键 | 主键，自增整数 |
| tags_uuid | TEXT | 标签标识 | 非空 |
| related_uuid | TEXT | 被关联对象标识 | 非空 |
| relation_type | TEXT | 关系类型 | 非空，任意文本（业务约定） |
| created_at | TIMESTAMP | 创建时间 | 默认 `CURRENT_TIMESTAMP` |

---

## comments（评论）

| 字段 | 类型 | 作用 | 可能的值 / 约束 |
|---|---|---|---|
| id | SERIAL | 自增主键 | 主键，自增整数 |
| uuid | TEXT | 评论唯一标识 | 非空、唯一 |
| status | TEXT | 评论状态 | 任意文本（业务约定） |
| comment_place | TEXT | 评论位置/模块 | 任意文本 |
| author | TEXT | 评论作者标识 | 任意文本 |
| relations | TEXT | 关联信息 | 任意文本 |
| comment_place_uuid | TEXT | 评论目标对象标识 | 任意文本 |
| ip_address | TEXT | 评论来源 IP | 任意文本 |
| user_agent | TEXT | 客户端 UA | 任意文本 |
| location | TEXT | 地理位置描述 | 任意文本 |
| content | TEXT | 评论内容 | 任意文本 |
| created_at | TIMESTAMP | 评论创建时间 | 默认 `CURRENT_TIMESTAMP` |

---

## favourites（收藏）

| 字段 | 类型 | 作用 | 可能的值 / 约束 |
|---|---|---|---|
| id | SERIAL | 自增主键 | 主键，自增整数 |
| uuid | TEXT | 收藏记录唯一标识 | 非空、唯一 |
| user_uuid | TEXT | 收藏所属用户标识 | 非空 |
| types | TEXT | 收藏类型 | 任意文本（业务约定） |
| created_at | TIMESTAMP | 收藏时间 | 默认 `CURRENT_TIMESTAMP` |

---

## wall_sayings（表白墙）

| 字段 | 类型 | 作用 | 可能的值 / 约束 |
|---|---|---|---|
| id | SERIAL | 自增主键 | 主键，自增整数 |
| uuid | TEXT | 留言唯一标识 | 非空、唯一 |
| author_uuid | TEXT | 作者用户标识 | 非空 |
| content | TEXT | 留言内容 | 任意文本 |
| saying_status | TEXT | 留言状态 | 任意文本（业务约定） |
| saying_type | TEXT | 留言类型 | 任意文本（业务约定） |
| sent_at | TIMESTAMP | 发送时间 | 默认 `CURRENT_TIMESTAMP` |
| updated_at | TIMESTAMP | 更新时间 | 时间戳或 `NULL` |
| other_info | JSONB | 额外信息 | JSON 对象 |
| likes | INTEGER | 点赞数 | 默认 `0` |
| share_count | INTEGER | 分享次数 | 默认 `0` |
| views | INTEGER | 浏览次数 | 默认 `0` |

---

## wall_looking_for（寻人/寻物墙）

| 字段 | 类型 | 作用 | 可能的值 / 约束 |
|---|---|---|---|
| id | SERIAL | 自增主键 | 主键，自增整数 |
| uuid | TEXT | 记录唯一标识 | 非空、唯一 |
| current_status | TEXT | 当前状态 | 任意文本（业务约定） |
| real_status | TEXT | 真实状态 | 任意文本（业务约定） |
| seeker | TEXT | 发起人/寻找者标识 | 任意文本 |
| created_at | TIMESTAMP | 创建时间 | 默认 `CURRENT_TIMESTAMP` |
| looking_for_type | TEXT | 寻找类型 | 任意文本（如 寻人/寻物，业务约定） |
| last_seen_at | TIMESTAMP | 最后出现时间 | 时间戳或 `NULL` |
| helper | TEXT | 协助者信息 | 任意文本 |
| clues | TEXT | 线索 | 任意文本 |

---

## songs（歌曲推荐）

| 字段 | 类型 | 作用 | 可能的值 / 约束 |
|---|---|---|---|
| id | SERIAL | 自增主键 | 主键，自增整数 |
| uuid | TEXT | 歌曲记录唯一标识 | 非空、唯一 |
| name | TEXT | 歌曲名 | 非空 |
| singer | TEXT | 歌手 | 任意文本 |
| platform | TEXT | 音乐平台 | 任意文本 |
| committed_at | TIMESTAMP | 提交时间 | 默认 `CURRENT_TIMESTAMP` |
| status | TEXT | 状态 | 任意文本（业务约定） |
| vote | INTEGER | 票数 | 默认 `0` |
| recommend_by | TEXT | 推荐人标识 | 任意文本 |
| recommend_words | TEXT | 推荐语 | 任意文本 |
| reason | TEXT | 推荐原因 | 任意文本 |

---

## song_arrangements（歌曲编排）

| 字段 | 类型 | 作用 | 可能的值 / 约束 |
|---|---|---|---|
| id | SERIAL | 自增主键 | 主键，自增整数 |
| uuid | TEXT | 编排记录唯一标识 | 非空、唯一 |
| week_number | INTEGER | 周次 | 非空整数 |
| content | TEXT | 编排内容 | 任意文本 |
| created_by | TEXT | 创建者标识 | 任意文本 |
| likes | INTEGER | 点赞数 | 默认 `0` |
| created_at | TIMESTAMP | 创建时间 | 默认 `CURRENT_TIMESTAMP` |

---

## vote（投票）

| 字段 | 类型 | 作用 | 可能的值 / 约束 |
|---|---|---|---|
| id | SERIAL | 自增主键 | 主键，自增整数 |
| uuid | TEXT | 投票记录唯一标识 | 非空、唯一 |
| vote_type | TEXT | 投票类型 | 任意文本（业务约定） |
| voted_at | TIMESTAMP | 投票时间 | 默认 `CURRENT_TIMESTAMP` |
| committed_by | TEXT | 投票人标识 | 任意文本 |
| content | TEXT | 投票内容 | 任意文本 |

---

## stores_and_restaurants（商铺与餐厅）

| 字段 | 类型 | 作用 | 可能的值 / 约束 |
|---|---|---|---|
| id | SERIAL | 自增主键 | 主键，自增整数 |
| uuid | TEXT | 店铺记录唯一标识 | 非空、唯一 |
| name | TEXT | 店名 | 非空 |
| location | TEXT | 位置描述 | 任意文本 |
| likes | INTEGER | 点赞数 | 默认 `0` |
| start_date | TIMESTAMP | 开始时间 | 时间戳或 `NULL` |
| end_date | TIMESTAMP | 结束时间 | 时间戳或 `NULL` |
| ratings | DECIMAL(4,2) | 评分 | `0 ~ 5`（含边界），可 `NULL` |
| status | TEXT | 状态 | 任意文本（业务约定） |

---

## tasks（任务）

| 字段 | 类型 | 作用 | 可能的值 / 约束 |
|---|---|---|---|
| id | SERIAL | 自增主键 | 主键，自增整数 |
| uuid | TEXT | 任务唯一标识 | 非空、唯一 |
| content | TEXT | 任务内容 | 任意文本 |
| parts | TEXT | 任务分段/部分 | 任意文本 |
| assigner | TEXT | 指派人标识 | 任意文本 |
| status | TEXT | 任务状态 | 任意文本（业务约定） |
| created_at | TIMESTAMP | 创建时间 | 默认 `CURRENT_TIMESTAMP` |

---

## personal_logs（个人日志）

| 字段 | 类型 | 作用 | 可能的值 / 约束 |
|---|---|---|---|
| id | SERIAL | 自增主键 | 主键，自增整数 |
| uuid | TEXT | 日志唯一标识 | 非空、唯一 |
| user_uuid | TEXT | 对应用户标识 | 非空 |
| log_level | TEXT | 日志级别 | 任意文本（如 INFO/WARNING/ERROR，业务约定） |
| log_type | TEXT | 日志类型 | 任意文本 |
| content | TEXT | 日志内容 | 任意文本 |
| created_at | TIMESTAMP | 记录时间 | 默认 `CURRENT_TIMESTAMP` |

---

## request_logs（请求统计）

| 字段 | 类型 | 作用 | 可能的值 / 约束 |
|---|---|---|---|
| id | SERIAL | 自增主键 | 主键，自增整数 |
| request_path | TEXT | 请求路径 | 非空、唯一（`UNIQUE(request_path)`） |
| frequency | INTEGER | 请求累计次数 | 默认 `0` |
| created_at | TIMESTAMP | 首次记录时间 | 默认 `CURRENT_TIMESTAMP` |

---

## system_logs（系统日志）

| 字段 | 类型 | 作用 | 可能的值 / 约束 |
|---|---|---|---|
| id | SERIAL | 自增主键 | 主键，自增整数 |
| uuid | TEXT | 系统日志唯一标识 | 非空、唯一 |
| log_level | TEXT | 日志级别 | 任意文本（如 SUCCESS/WARNING/ERROR，业务约定） |
| log_type | TEXT | 日志类型 | 任意文本 |
| created_at | TIMESTAMP | 创建时间 | 默认 `CURRENT_TIMESTAMP` |
| being_flagged | BOOLEAN | 是否被标记 | 默认 `false`，可取 `true/false` |
| content | TEXT | 日志内容 | 任意文本 |
| system_version | TEXT | 系统版本 | 任意文本 |

---

## system_reports（系统报告）

| 字段 | 类型 | 作用 | 可能的值 / 约束 |
|---|---|---|---|
| id | SERIAL | 自增主键 | 主键，自增整数 |
| uuid | TEXT | 报告唯一标识 | 非空、唯一 |
| content | TEXT | 报告内容 | 任意文本 |
| frequency | INTEGER | 统计次数 | 默认 `0` |
| created_at | TIMESTAMP | 创建时间 | 默认 `CURRENT_TIMESTAMP` |

---

## illegal_requests（违规请求）

| 字段 | 类型 | 作用 | 可能的值 / 约束 |
|---|---|---|---|
| id | SERIAL | 自增主键 | 主键，自增整数 |
| uuid | TEXT | 违规记录唯一标识 | 非空、唯一 |
| user | TEXT | 触发用户标识 | 非空，默认 `'unknown'` |
| happened_at | TIMESTAMP | 发生时间 | 默认 `CURRENT_TIMESTAMP`，已建索引 `idx_illegal_requests_happened_at` |
| type | TEXT | 违规类型 | 非空，任意文本（如 xss/sql_injection 等，业务约定） |
| path | TEXT | 请求路径 | 非空 |
| ip | TEXT | 来源 IP | 非空，已建索引 `idx_illegal_requests_ip` |
| ua | TEXT | 客户端 UA | 任意文本 |

