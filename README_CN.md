# AI CodeHub

AI CodeHub 是一个用于管理和共享 AI 相关代码和项目的结构化平台。

## 功能特点

- 用户认证和授权
  - 用户注册和登录
  - JWT token 认证
  - 角色权限管理（普通用户/超级用户）

- 项目管理
  - 创建和管理项目
  - 项目描述和元数据
  - 项目访问控制

- 模型管理
  - 模型上传和版本控制
  - 模型元数据管理
  - 支持多种模型类型（分类/回归/生成式）
  - 模型状态跟踪（草稿/训练中/就绪/错误）

- GPU 支持
  - CUDA 设备检测
  - GPU 内存管理
  - 模型 GPU 加速

- 测试和报告
  - 环境测试
  - GPU 检测测试
  - HTML 和 JSON 格式的测试报告
  - 自动化测试框架

## 快速开始

1. 克隆仓库：
```bash
git clone https://github.com/yourusername/ai_codehub.git
cd ai_codehub
```

2. 安装依赖：
```bash
pip install -r requirements.txt
```

3. 初始化数据库：
```bash
python -m src.database.init_db
```

4. 启动服务器：
```bash
uvicorn src.main:app --reload
```

5. 访问应用：
- 打开浏览器访问 http://localhost:8000
- 默认超级用户账号：
  - 用户名：admin
  - 密码：admin123

## API 文档

启动服务器后，访问以下地址查看 API 文档：
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

主要 API 端点：
- `/api/auth/*` - 认证相关
- `/api/v1/models/*` - 模型管理
- `/api/projects/*` - 项目管理

## 系统要求

- Python 3.8 或更高版本
- SQLite 3
- CUDA 工具包（可选，用于 GPU 支持）
- 其他依赖见 requirements.txt

## 测试

运行测试：
```bash
python -m pytest tests/ -v
```

测试报告位于 `reports/` 目录：
- `reports/environment/` - 环境测试报告
- `reports/gpu/` - GPU 测试报告
- `reports/summary.html` - 测试总结报告

## 目录结构

```
ai_codehub/
├── src/
│   ├── api/            - API 路由和处理器
│   ├── core/           - 核心功能和配置
│   ├── database/       - 数据库模型和配置
│   ├── models/         - 模型管理相关代码
│   └── static/         - 静态文件
├── tests/              - 测试代码
├── reports/            - 测试报告
├── requirements.txt    - 项目依赖
└── README.md          - 项目文档
```

## 许可证

本项目采用 MIT 许可证。详见 [LICENSE](LICENSE) 文件。

## 项目结构

```
ai_codehub/
├── src/                    # 源代码
│   ├── api/               # API 接口
│   ├── core/              # 核心功能
│   ├── database/          # 数据库模型和操作
│   ├── models/            # AI 模型实现
│   └── utils/             # 工具函数
├── tests/                 # 测试用例
├── scripts/               # 工具脚本
├── config/                # 配置文件
├── docs/                  # 文档
└── static/                # 静态文件 (HTML, CSS, JS)
```

## 数据库模型

项目使用 SQLAlchemy ORM，包含以下主要模型：

### 用户模型 (User)
- **id**: 整数 (主键)
- **username**: 字符串 (唯一)
- **email**: 字符串 (唯一)
- **hashed_password**: 字符串
- **is_active**: 布尔值
- **is_superuser**: 布尔值
- **created_at**: 日期时间
- **updated_at**: 日期时间
- **projects**: 与项目模型的关系

### 项目模型 (Project)
- **id**: 整数 (主键)
- **name**: 字符串
- **description**: 文本
- **owner_id**: 整数 (外键关联用户)
- **created_at**: 日期时间
- **updated_at**: 日期时间
- **owner**: 与用户模型的关系
- **models**: 与模型模型的关系

### 模型模型 (Model)
- **id**: 整数 (主键)
- **name**: 字符串
- **description**: 文本
- **project_id**: 整数 (外键关联项目)
- **model_type**: 字符串
- **model_path**: 字符串
- **created_at**: 日期时间
- **updated_at**: 日期时间
- **project**: 与项目模型的关系 