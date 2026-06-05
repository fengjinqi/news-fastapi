# news-fastapi

头条新闻类项目接口，基于 Python FastAPI 框架开发的异步 RESTful API 学习项目。

## 技术栈

- **FastAPI** - 高性能异步 Web 框架
- **SQLAlchemy 2.0** - 异步 ORM，使用 `async_engine` + `AsyncSession`
- **aiomysql** - MySQL 异步驱动
- **Pydantic v2** - 数据校验与序列化
- **pydantic-settings** - 环境变量配置管理

## 项目结构

```
app/
├── api/          # 路由层（category、news）
├── config/       # 配置管理（读取 .env）
├── core/         # 核心模块（db、异常处理、统一响应）
├── crud/         # 数据库操作层
├── models/       # SQLAlchemy 数据模型
├── schems/       # Pydantic 请求/响应模型
├── services/     # 业务逻辑层
└── utils/        # 工具函数
```

## 数据模型

- **new_category** - 新闻分类表（id、name、sort_order、created_at、updated_at）
- **news** - 新闻表（id、title、description、author、content、image、category_id、views、publish_time、created_at、updated_at）

## 接口列表

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | /api/category | 获取分类列表 |
| POST | /api/category | 创建分类 |
| PUT | /api/category/{id} | 更新分类 |
| DELETE | /api/category/{id} | 删除分类 |
| GET | /api/news | 获取新闻列表 |

## 快速开始

1. 安装依赖

```bash
pip install -r requirements.txt
```

2. 配置环境变量，复制 `.env` 并填写数据库信息

```env
DB_HOST=127.0.0.1
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=news_app
```

3. 启动服务

```bash
uvicorn main:app --reload
```

4. 访问文档：http://127.0.0.1:8000/docs
