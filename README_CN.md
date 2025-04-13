# AI CodeHub

AI CodeHub 是一个用于管理、共享和协作AI相关代码和项目的综合平台。该框架为AI开发、实验和部署提供了结构化的环境。

## 项目结构

```
ai_codehub/
├── src/                    # 源代码目录
│   ├── core/              # 核心功能
│   ├── models/            # AI模型实现
│   ├── utils/             # 工具函数
│   └── api/               # API接口
├── tests/                 # 测试文件
│   ├── conftest.py        # 测试配置
│   ├── test_model_manager.py  # 模型管理器测试
│   ├── test_environment.py    # 环境测试
│   └── test_gpu_environment.py # GPU环境测试
├── docs/                  # 文档
├── examples/              # 示例实现
├── requirements.txt       # Python依赖
└── config/               # 配置文件
```

## 功能特点

- 模型管理：组织和版本控制AI模型
- 实验跟踪：记录和监控实验
- 代码共享：共享和协作AI项目
- API集成：轻松集成各种AI服务
- 文档：全面的文档和示例
- GPU支持：自动GPU检测和利用
- 测试：使用pytest的全面测试套件

## 快速开始

1. 克隆仓库
2. 安装依赖：`pip install -r requirements.txt`
3. 运行开发服务器：`python src/main.py`

## GPU支持

框架提供全面的GPU支持和环境检测：

### GPU要求
- 支持CUDA的NVIDIA GPU
- 已安装NVIDIA驱动
- 已安装CUDA工具包
- 已安装cuDNN
- 支持CUDA的PyTorch

### GPU环境检测
框架自动检测和测试：
- GPU可用性和数量
- GPU内存和计算能力
- CUDA版本兼容性
- 驱动版本
- 性能基准测试

## 测试

项目使用pytest进行测试。运行测试：

```bash
# 安装测试依赖
pip install pytest pytest-cov pytest-xdist

# 运行所有测试
pytest tests/

# 运行测试并生成覆盖率报告
pytest --cov=src tests/

# 运行特定测试文件
pytest tests/test_model_manager.py

# 运行GPU环境测试
pytest tests/test_gpu_environment.py -v

# 并行运行测试
pytest -n auto tests/
```

### 测试覆盖范围

#### 环境测试
- Python版本兼容性
- 包依赖
- 系统资源
- 文件系统权限
- 环境变量

#### GPU测试
- GPU可用性和数量
- GPU内存信息
- 计算能力
- CUDA工具包版本
- 性能基准测试
- 基本操作
- 内存管理

#### 模型测试
- 模型保存和加载
- 元数据管理
- 错误处理
- 模型列表

## 测试报告生成

框架自动生成全面的测试报告，支持 JSON 和 HTML 格式。报告存储在 `reports` 目录中，结构如下：

```
reports/
├── environment/          # 环境测试报告
├── gpu/                 # GPU测试报告
└── test_summary_*.html  # HTML汇总报告
```

### 报告类型

1. **环境报告** (`reports/environment/`)
   - 系统信息
   - Python版本
   - 包依赖
   - 系统资源
   - 环境变量
   - 测试结果

2. **GPU报告** (`reports/gpu/`)
   - GPU可用性
   - CUDA版本
   - GPU数量和内存
   - 计算能力
   - 性能基准测试
   - 测试结果

3. **HTML汇总报告** (`reports/test_summary_*.html`)
   - 所有测试结果的综合视图
   - 系统和GPU信息
   - 性能指标
   - 详细JSON报告的链接
   - 支持中英文版本

### 生成报告

运行测试时会自动生成报告。也可以手动生成报告：

```bash
# 生成所有报告
python -m pytest tests/ -v

# 生成特定测试文件的报告
python -m pytest tests/test_environment.py -v
python -m pytest tests/test_gpu_environment.py -v
```

### 报告特性

- **时间戳**：每个报告都包含生成时间戳
- **双语支持**：提供中英文版本报告
- **详细信息**：全面的系统和测试数据
- **性能指标**：GPU性能基准测试
- **易于导航**：HTML报告包含详细JSON数据的链接
- **绝对路径**：所有报告链接使用绝对路径，方便访问

## 系统要求

- Python 3.8+
- requirements.txt中列出的依赖
- CUDA支持（可选，用于GPU加速）
  - 支持CUDA的NVIDIA GPU
  - NVIDIA驱动
  - CUDA工具包
  - cuDNN

## 许可证

MIT许可证 