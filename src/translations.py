from typing import Dict, Any

translations: Dict[str, Dict[str, str]] = {
    "en": {
        # Authentication
        "invalid_credentials": "Invalid username or password",
        "username_required": "Username is required",
        "password_required": "Password is required",
        "email_required": "Email is required",
        "username_taken": "Username is already taken",
        "email_taken": "Email is already registered",
        "registration_success": "Registration successful",
        "login_success": "Login successful",
        "logout_success": "Logout successful",
        "unauthorized": "Unauthorized access",
        "token_expired": "Token has expired",
        "token_invalid": "Invalid token",
        
        # Models
        "model_not_found": "Model not found",
        "model_upload_success": "Model uploaded successfully",
        "model_upload_failed": "Failed to upload model",
        "model_delete_success": "Model deleted successfully",
        "model_delete_failed": "Failed to delete model",
        "model_update_success": "Model updated successfully",
        "model_update_failed": "Failed to update model",
        
        # Projects
        "project_not_found": "Project not found",
        "project_create_success": "Project created successfully",
        "project_create_failed": "Failed to create project",
        "project_delete_success": "Project deleted successfully",
        "project_delete_failed": "Failed to delete project",
        "project_update_success": "Project updated successfully",
        "project_update_failed": "Failed to update project",
        
        # General
        "server_error": "Internal server error",
        "validation_error": "Validation error",
        "not_found": "Resource not found",
        "forbidden": "Access forbidden",
        "bad_request": "Bad request",
    },
    "zh": {
        # Authentication
        "invalid_credentials": "用户名或密码错误",
        "username_required": "用户名不能为空",
        "password_required": "密码不能为空",
        "email_required": "邮箱不能为空",
        "username_taken": "用户名已被使用",
        "email_taken": "邮箱已被注册",
        "registration_success": "注册成功",
        "login_success": "登录成功",
        "logout_success": "退出成功",
        "unauthorized": "未授权访问",
        "token_expired": "令牌已过期",
        "token_invalid": "无效的令牌",
        
        # Models
        "model_not_found": "模型不存在",
        "model_upload_success": "模型上传成功",
        "model_upload_failed": "模型上传失败",
        "model_delete_success": "模型删除成功",
        "model_delete_failed": "模型删除失败",
        "model_update_success": "模型更新成功",
        "model_update_failed": "模型更新失败",
        
        # Projects
        "project_not_found": "项目不存在",
        "project_create_success": "项目创建成功",
        "project_create_failed": "项目创建失败",
        "project_delete_success": "项目删除成功",
        "project_delete_failed": "项目删除失败",
        "project_update_success": "项目更新成功",
        "project_update_failed": "项目更新失败",
        
        # General
        "server_error": "服务器内部错误",
        "validation_error": "数据验证错误",
        "not_found": "资源不存在",
        "forbidden": "禁止访问",
        "bad_request": "请求错误",
    }
}

def get_translation(key: str, lang: str = "zh") -> str:
    """获取指定语言的翻译文本"""
    return translations.get(lang, {}).get(key, key)

def get_error_response(key: str, lang: str = "zh", status_code: int = 400, **kwargs) -> Dict[str, Any]:
    """获取错误响应"""
    return {
        "error": get_translation(key, lang),
        "status_code": status_code,
        **kwargs
    } 