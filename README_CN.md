# AI CodeHub

AI CodeHub 是一个基于 FastAPI 和 React 的 AI 代码生成平台，支持多种 AI 模型，提供代码生成、项目管理等功能。

## 功能特点

- 支持多种 AI 模型（GPT-4, Claude, Gemini 等）
- 代码生成和项目管理
- 用户认证和授权
- 多语言支持（中文/英文）
- 响应式设计，支持移动端访问
- 实时导航栏状态管理
- 安全退出功能

## 技术栈

### 后端
- FastAPI
- SQLAlchemy
- Pydantic
- JWT 认证
- SQLite 数据库

### 前端
- React
- Tailwind CSS
- i18next 国际化
- Axios HTTP 客户端
- 事件委托用于动态元素
- 本地存储用于状态管理

## 安装与运行

### 环境要求
- Python 3.8+
- Node.js 16+
- npm 或 yarn

### 后端设置
1. 创建虚拟环境：
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

2. 安装依赖：
```bash
pip install -r requirements.txt
```

3. 运行后端服务：
```bash
uvicorn src.main:app --reload
```

### 前端设置
1. 安装依赖：
```bash
cd static
npm install
```

2. 运行开发服务器：
```bash
npm run dev
```

## 测试

项目使用 pytest 进行测试，包括单元测试和 API 测试。

### 运行测试
```bash
pytest
```

### 测试覆盖
- 用户认证（注册、登录、token 验证）
- API 端点访问控制
- 数据库操作
- 错误处理
- 导航栏状态管理
- 退出功能

### 测试数据库
测试使用 SQLite 内存数据库，每个测试用例运行前后会自动创建和清理数据库。

## API 文档

启动服务后，访问以下地址查看 API 文档：
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 项目结构

```
ai_codehub/
├── src/
│   ├── main.py              # 应用入口
│   ├── database/            # 数据库配置和模型
│   ├── api/                 # API 路由
│   │   ├── routers/        # API 路由处理器
│   │   │   ├── auth.py     # 认证路由
│   │   │   ├── model_router.py  # 模型管理路由
│   │   │   └── project_router.py # 项目管理路由
│   ├── core/                # 核心配置和工具
│   └── services/            # 业务逻辑
├── static/                  # 前端代码
│   ├── components/          # React 组件
│   │   └── navbar.html     # 导航栏组件
│   ├── js/                 # JavaScript 文件
│   │   ├── common.js       # 通用工具
│   │   ├── locales.js      # 国际化
│   │   └── i18n.js         # i18n 配置
│   ├── index.html          # 主页
│   ├── login.html          # 登录页
│   ├── register.html       # 注册页
│   ├── models.html         # 模型页
│   ├── projects.html       # 项目页
│   └── profile.html        # 用户配置页
├── tests/                  # 测试文件
├── requirements.txt        # Python 依赖
└── README.md              # 项目文档
```

## 最近更新

### v0.1.0
- 添加安全退出功能
- 改进导航栏状态管理
- 增强用户认证流程
- 修复 API 端点验证
- 添加配置文件
- 改进错误处理
- 增强国际化支持

## 贡献指南

1. Fork 项目
2. 创建特性分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'Add some amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 创建 Pull Request

## 许可证

本项目采用 MIT 许可证 - 详见 LICENSE 文件 