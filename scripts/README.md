# AI CodeHub Scripts

This directory contains utility scripts for managing the AI CodeHub project.

## Git Version Management Script

The `git_manager.py` script provides a convenient way to manage Git operations with best practices.

### Installation

1. Make the script executable:
```bash
chmod +x scripts/git_manager.py
```

2. Add the script to your PATH (optional):
```bash
# For Linux/Mac
ln -s $(pwd)/scripts/git_manager.py /usr/local/bin/git-manager

# For Windows (PowerShell)
$env:Path += ";$(pwd)\scripts"
```

### Usage

The script provides the following commands:

#### Create a new branch
```bash
python scripts/git_manager.py create-branch feature/new-feature --base main
```

#### Commit changes
```bash
python scripts/git_manager.py commit "Add new feature"
```

#### Push changes
```bash
python scripts/git_manager.py push --branch feature/new-feature
```

#### Pull latest changes
```bash
python scripts/git_manager.py pull
```

#### Merge branches
```bash
python scripts/git_manager.py merge feature/new-feature --target main
```

#### Delete a branch
```bash
python scripts/git_manager.py delete-branch feature/new-feature
# Force delete
python scripts/git_manager.py delete-branch feature/new-feature --force
```

#### Create and push a tag
```bash
python scripts/git_manager.py tag v1.0.0 "Release version 1.0.0"
```

### Features

- Automatic branch creation from latest main
- Safe merge operations with pull before merge
- Tag creation and pushing
- Error handling and informative messages
- Support for different repository paths
- Type hints for better code maintainability

### Best Practices

1. Always create feature branches from the latest main branch
2. Use meaningful commit messages
3. Pull latest changes before merging
4. Use tags for version releases
5. Delete merged branches to keep the repository clean

### Error Handling

The script includes comprehensive error handling:
- Repository validation
- Command execution errors
- Branch existence checks
- Merge conflicts detection

### Examples

#### Complete feature workflow
```bash
# Create a new feature branch
python scripts/git_manager.py create-branch feature/user-authentication

# Make changes and commit them
python scripts/git_manager.py commit "Add user authentication"

# Push changes
python scripts/git_manager.py push

# After review, merge to main
python scripts/git_manager.py merge feature/user-authentication

# Delete the feature branch
python scripts/git_manager.py delete-branch feature/user-authentication
```

#### Release workflow
```bash
# Create and push a release tag
python scripts/git_manager.py tag v1.0.0 "Release version 1.0.0"
``` 