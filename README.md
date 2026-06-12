# news-fastapi

头条新闻类项目接口，基于 Python FastAPI 框架开发的异步 RESTful API 学习项目，涵盖新闻浏览、用户管理、收藏与浏览历史等核心功能。

## 技术栈

| 依赖 | 版本 | 说明 |
|------|------|------|
| FastAPI | 0.136.3 | 高性能异步 Web 框架 |
| SQLAlchemy | 2.0.50 | 异步 ORM，使用 `async_engine` + `AsyncSession` |
| aiomysql | 0.3.2 | MySQL 异步驱动 |
| Pydantic | v2 | 数据校验与序列化 |
| pydantic-settings | 2.14.1 | 环境变量配置管理 |
| PyJWT | 2.13.0 | JWT Token 签发与验证 |
| pwdlib[argon2] | 0.3.0 | Argon2 密码加密 |
| redis | 8.0.0 | 异步 Redis 客户端 |
| python-multipart | 0.0.32 | 表单数据解析 |
| uvicorn | 0.49.0 | ASGI 服务器 |

## 项目结构

```
app/
├── api/          # 路由层（category、news、users、favorite、history）
├── config/       # 配置管理（pydantic-settings 读取 .env）
├── core/         # 核心模块（db、jwt、redis、异常处理、统一响应、依赖注入）
├── crud/         # 数据库操作层
├── models/       # SQLAlchemy 数据模型（含抽象基类 BaseModel）
├── schems/       # Pydantic 请求/响应模型
├── services/     # 业务逻辑层（含 Redis 缓存策略）
└── utils/        # 工具类（RedisUtil、安全工具、日志）
```

## 数据模型

所有模型继承自 `BaseModel`，自动包含 `created_at`、`updated_at` 字段。

| 表名 | 模型 | 字段 |
|------|------|------|
| new_category | CategoryModel | id, name, sort_order |
| news | NewsModel | id, title, description, author, content, image, category_id(FK), views, publish_time |
| users | User | id, username, password, nickname, avatar, gender, bio, phone |
| favorite | FavoriteModel | id, user_id(FK), news_id(FK) |
| history | HistoryModel | id, user_id(FK), news_id(FK), view_time |

> - `favorite` 表设置了 `(user_id, news_id)` 唯一约束，防止重复收藏
> - `history` 表设置了 `(user_id, news_id)` 唯一约束，同一用户同一篇新闻只保留一条记录，重复浏览更新 `view_time`

## 接口列表

### 分类接口 /api/category

| 方法 | 路径 | 鉴权 | 说明 |
|------|------|------|------|
| GET | /api/category | 否 | 获取分类列表（Redis 永久缓存，增删改自动失效） |
| POST | /api/category | 是 | 创建分类 |
| PUT | /api/category/{id} | 是 | 更新分类 |
| DELETE | /api/category/{id} | 是 | 删除分类 |

### 新闻接口 /api/news

| 方法 | 路径 | 鉴权 | 说明 |
|------|------|------|------|
| GET | /api/news | 否 | 按分类查新闻列表（分页，支持 page/size 参数） |
| GET | /api/news/{id} | 否 | 获取新闻详情（含同分类相关新闻，Redis 永久缓存） |

### 用户接口 /api/user

| 方法 | 路径 | 鉴权 | 说明 |
|------|------|------|------|
| POST | /api/user | 否 | 注册用户 |
| POST | /api/user/login | 否 | JSON 登录，返回 `access_token` + `refresh_token` |
| POST | /api/user/login/form | 否 | OAuth2 表单登录（兼容 Swagger UI） |
| POST | /api/user/refresh | 否 | 用 `refresh_token` 换取新的 `access_token` |
| GET | /api/user/info | 是 | 获取当前登录用户信息 |
| PUT | /api/user/{id} | 是 | 更新用户信息（仅可修改自己） |
| PUT | /api/user/{id}/password | 是 | 修改密码（仅可修改自己） |

### 收藏接口 /api/favorite

| 方法 | 路径 | 鉴权 | 说明 |
|------|------|------|------|
| GET | /api/favorite/{id} | 是 | 根据新闻 ID 查询当前用户是否已收藏 |
| GET | /api/favorite | 是 | 获取我的收藏列表（分页） |
| POST | /api/favorite | 是 | 收藏新闻 |
| DELETE | /api/favorite/{id} | 是 | 取消收藏（仅可删除自己的） |

### 历史记录接口 /api/history

| 方法 | 路径 | 鉴权 | 说明 |
|------|------|------|------|
| GET | /api/history | 是 | 获取我的浏览历史（分页，按 view_time 倒序） |
| POST | /api/history | 是 | 记录浏览历史（同一篇新闻重复浏览更新时间） |
| DELETE | /api/history/{id} | 是 | 删除指定历史记录（仅可删除自己的） |

## 鉴权机制

- 采用 **JWT Bearer Token** 认证
- 登录成功返回 `access_token`（有效期由 `ACCESS_TOKEN_EXPIRE_MINUTES` 控制）和 `refresh_token`
- 需要鉴权的接口请求头携带：`Authorization: Bearer <token>`
- 通过 `/api/user/refresh` 接口用 `refresh_token` 换取新的 `access_token`

## 缓存策略

- 分类列表：永久缓存（`category:all`），增删改操作后自动删除缓存
- 新闻详情：永久缓存（`news:detail:{id}`），不自动过期
- 其他查询：默认 300 秒过期

## 快速开始

**1. 安装依赖**

```bash
pip install -r requirements.txt
```

**2. 配置环境变量**，新建 `.env` 文件并填写以下配置：

```env
# 项目
ENV=dev
PROJECT_NAME=FastAPI
API_PREFIX=/api

# MySQL
DB_HOST=127.0.0.1
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=news_app

# Redis
REDIS_HOST=127.0.0.1
REDIS_PORT=6379
REDIS_DB=0
REDIS_PASSWORD=

# JWT
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=10080
```

**3. 启动服务**

```bash
uvicorn main:app --reload
```

**4. 访问接口文档**：http://127.0.0.1:8000/docs
