# AI CodeHub

AI CodeHub is a comprehensive platform for AI code generation and project management, built with FastAPI and React.

## Features

- Support for multiple AI models (GPT-4, Claude, Gemini, etc.)
- Code generation and project management
- User authentication and authorization
- Multi-language support (English/Chinese)
- Responsive design with mobile support

## Tech Stack

### Backend
- FastAPI
- SQLAlchemy
- Pydantic
- JWT Authentication
- SQLite Database

### Frontend
- React
- Tailwind CSS
- i18next Internationalization
- Axios HTTP Client

## Installation & Setup

### Prerequisites
- Python 3.8+
- Node.js 16+
- npm or yarn

### Backend Setup
1. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run backend service:
```bash
python -m src.main
```

### Frontend Setup
1. Install dependencies:
```bash
cd static
npm install
```

2. Run development server:
```bash
npm run dev
```

## Testing

The project uses pytest for both unit tests and API tests.

### Running Tests
```bash
pytest
```

### Test Coverage
- User authentication (registration, login, token validation)
- API endpoint access control
- Database operations
- Error handling

### Test Database
Tests use an in-memory SQLite database, which is automatically created and cleaned up before and after each test case.

## API Documentation

After starting the service, access the API documentation at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Project Structure

```
ai_codehub/
├── src/
│   ├── main.py              # Application entry point
│   ├── database/            # Database configuration and models
│   ├── api/                 # API routes
│   ├── core/                # Core configuration and utilities
│   └── services/            # Business logic
├── static/                  # Frontend code
│   ├── components/          # React components
│   ├── js/                  # JavaScript utilities
│   └── css/                 # Style files
├── tests/                   # Test files
├── requirements.txt         # Python dependencies
└── README.md               # Project documentation
```

## Contributing

1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details

---

# AI CodeHub

AI CodeHub 是一个基于 FastAPI 和 React 的 AI 代码生成平台，支持多种 AI 模型，提供代码生成、项目管理等功能。

## 功能特点

- 支持多种 AI 模型（GPT-4, Claude, Gemini 等）
- 代码生成和项目管理
- 用户认证和授权
- 多语言支持（中文/英文）
- 响应式设计，支持移动端访问

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
python -m src.main
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
│   ├── core/                # 核心配置和工具
│   └── services/            # 业务逻辑
├── static/                  # 前端代码
│   ├── components/          # React 组件
│   ├── js/                  # JavaScript 工具
│   └── css/                 # 样式文件
├── tests/                   # 测试文件
├── requirements.txt         # Python 依赖
└── README.md               # 项目文档
```

## 贡献指南

1. Fork 项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建 Pull Request

## 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件
