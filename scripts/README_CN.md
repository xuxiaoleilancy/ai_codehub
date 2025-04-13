# AI CodeHub 脚本工具

本目录包含用于管理 AI CodeHub 项目的实用脚本。

## Git 版本管理脚本

`git_manager.py` 脚本提供了一种便捷的方式来管理 Git 操作，并遵循最佳实践。

### 安装

1. 使脚本可执行：
```bash
chmod +x scripts/git_manager.py
```

2. 将脚本添加到 PATH（可选）：
```bash
# Linux/Mac
ln -s $(pwd)/scripts/git_manager.py /usr/local/bin/git-manager

# Windows (PowerShell)
$env:Path += ";$(pwd)\scripts"
```

### 使用方法

脚本提供以下命令：

#### 创建新分支
```bash
python scripts/git_manager.py create-branch feature/new-feature --base main
```

#### 提交更改
```bash
python scripts/git_manager.py commit "添加新功能"
```

#### 推送更改
```bash
python scripts/git_manager.py push --branch feature/new-feature
```

#### 拉取最新更改
```bash
python scripts/git_manager.py pull
```

#### 合并分支
```bash
python scripts/git_manager.py merge feature/new-feature --target main
```

#### 删除分支
```bash
python scripts/git_manager.py delete-branch feature/new-feature
# 强制删除
python scripts/git_manager.py delete-branch feature/new-feature --force
```

#### 创建并推送标签
```bash
python scripts/git_manager.py tag v1.0.0 "发布版本 1.0.0"
```

### 功能特点

- 从最新的主分支自动创建分支
- 合并操作前自动拉取最新更改
- 标签创建和推送
- 错误处理和信息提示
- 支持不同的仓库路径
- 类型提示以提高代码可维护性

### 最佳实践

1. 始终从最新的主分支创建功能分支
2. 使用有意义的提交信息
3. 合并前拉取最新更改
4. 使用标签进行版本发布
5. 删除已合并的分支以保持仓库整洁

### 错误处理

脚本包含全面的错误处理：
- 仓库验证
- 命令执行错误
- 分支存在性检查
- 合并冲突检测

### 示例

#### 完整的功能开发流程
```bash
# 创建新的功能分支
python scripts/git_manager.py create-branch feature/user-authentication

# 进行更改并提交
python scripts/git_manager.py commit "添加用户认证功能"

# 推送更改
python scripts/git_manager.py push

# 审核后合并到主分支
python scripts/git_manager.py merge feature/user-authentication

# 删除功能分支
python scripts/git_manager.py delete-branch feature/user-authentication
```

#### 发布流程
```bash
# 创建并推送发布标签
python scripts/git_manager.py tag v1.0.0 "发布版本 1.0.0"
``` 