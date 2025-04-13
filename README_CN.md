# AI CodeHub

AI 代码管理与共享平台

## 功能特点

- 模型管理
  - 上传和管理 AI 模型
  - 模型版本控制
  - 模型元数据管理
  - GPU 支持模型操作

- 用户认证
  - 用户注册和登录
  - 基于令牌的身份验证
  - 用户资料管理
  - 基于角色的访问控制

- 现代化 Web 界面
  - 响应式设计
  - 用户友好的表单
  - 实时反馈
  - 清晰现代的 UI

## 项目结构

```
ai_codehub/
├── config/             # 配置文件
├── docs/              # 文档
├── examples/          # 示例代码和用法
├── reports/           # 测试和环境报告
├── scripts/           # 实用脚本
├── src/               # 源代码
│   ├── api/           # API 端点
│   ├── core/          # 核心功能
│   ├── database/      # 数据库模型和架构
│   └── models/        # 模型管理
├── static/            # 前端资源
│   ├── css/          # 样式表
│   ├── js/           # JavaScript 文件
│   └── index.html    # 主 HTML 页面
├── tests/             # 测试文件
└── requirements.txt   # Python 依赖
```

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

3. 启动服务器：
```bash
python -m uvicorn src.main:app --reload
```

4. 打开浏览器访问：
```
http://localhost:8000
```

## 身份认证

平台使用 JWT（JSON Web Tokens）进行身份认证。使用 API：

1. 注册新用户：
```bash
curl -X POST "http://localhost:8000/api/auth/register" \
     -H "Content-Type: application/json" \
     -d '{"username": "user", "email": "user@example.com", "password": "password"}'
```

2. 登录获取访问令牌：
```bash
curl -X POST "http://localhost:8000/api/auth/token" \
     -H "Content-Type: application/x-www-form-urlencoded" \
     -d "username=user&password=password"
```

3. 在后续请求中使用令牌：
```bash
curl -X GET "http://localhost:8000/api/auth/me" \
     -H "Authorization: Bearer your_access_token"
```

## GPU 支持

平台自动检测并利用可用的 GPU 资源进行模型操作。检查 GPU 状态：

1. 运行环境测试：
```bash
python -m pytest tests/test_environment.py -v
```

2. 在 `reports/` 目录中查看生成的报告

## 测试

运行测试套件：
```bash
python -m pytest tests/ -v
```

测试报告将生成在 `reports/` 目录中，包括：
- 环境测试结果
- GPU 检测结果
- 测试覆盖率报告

## 系统要求

- Python 3.8 或更高版本
- FastAPI
- SQLAlchemy
- PyTorch（用于 GPU 支持）
- 现代网络浏览器

## 许可证

本项目采用 MIT 许可证 - 详见 LICENSE 文件 