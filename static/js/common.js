// 加载导航栏
window.loadNavbar = async function() {
    try {
        const response = await fetch('/components/navbar.html');
        if (!response.ok) {
            throw new Error('Failed to load navbar');
        }
        const html = await response.text();
        const navbarContainer = document.getElementById('navbar-container');
        navbarContainer.innerHTML = html;
        
        // 检查登录状态
        window.checkLoginStatus();
        
        // 添加登出按钮事件监听
        window.setupLogoutButton();
    } catch (error) {
        console.error('Error loading navbar:', error);
    }
}

// 设置退出登录按钮事件监听
window.setupLogoutButton = function() {
    // 使用事件委托，监听整个导航栏容器
    const navbarContainer = document.getElementById('navbar-container');
    if (navbarContainer) {
        navbarContainer.addEventListener('click', async (e) => {
            // 检查点击的是否是退出登录按钮
            if (e.target.closest('#logout-button')) {
                e.preventDefault();
                
                // 清除本地存储
                localStorage.removeItem('token');
                localStorage.removeItem('username');
                localStorage.removeItem('is_superuser');
                
                // 显示成功消息
                const notification = document.createElement('div');
                notification.className = 'notification is-success';
                notification.innerHTML = `
                    <button class="delete"></button>
                    <p data-i18n="logout_success">登出成功</p>
                `;
                document.body.appendChild(notification);
                
                // 更新导航栏状态
                window.checkLoginStatus();
                
                // 延迟跳转到首页，确保导航栏已更新
                setTimeout(() => {
                    window.location.href = '/';
                }, 100);
            }
        });
    }
}

// 检查登录状态
window.checkLoginStatus = function() {
    const token = localStorage.getItem('token');
    const username = localStorage.getItem('username');
    const guestButtons = document.querySelectorAll('.guest-buttons');
    const userButtons = document.querySelectorAll('.user-buttons');
    const usernameElements = document.querySelectorAll('.username');
    
    if (token && username) {
        // 用户已登录
        guestButtons.forEach(button => button.style.display = 'none');
        userButtons.forEach(button => button.style.display = 'block');
        usernameElements.forEach(element => {
            element.textContent = username;
        });
    } else {
        // 用户未登录
        guestButtons.forEach(button => button.style.display = 'block');
        userButtons.forEach(button => button.style.display = 'none');
        usernameElements.forEach(element => {
            element.textContent = '';
        });
    }
}

// 更新导航栏登录状态
window.updateNavbarLoginState = function() {
    window.checkLoginStatus();
}

// 检查认证状态
window.checkAuth = function() {
    const token = localStorage.getItem('token');
    const tokenExpiry = localStorage.getItem('tokenExpiry');
    
    // 检查 token 是否存在且未过期
    if (!token || !tokenExpiry || new Date(tokenExpiry) < new Date()) {
        // token 不存在或已过期，清除登录状态
        window.clearAuth();
        // 如果不在登录页面，则重定向到登录页面
        if (!window.location.pathname.includes('/login')) {
            window.location.href = '/login';
        }
        return false;
    }
    return true;
}

// 保存认证信息
window.saveAuth = function(token, expiresIn) {
    try {
        // 计算过期时间（当前时间 + 过期时间）
        const expiryDate = new Date();
        expiryDate.setMinutes(expiryDate.getMinutes() + expiresIn);
        
        // 保存 token 和过期时间
        localStorage.setItem('token', token);
        localStorage.setItem('tokenExpiry', expiryDate.toISOString());
    } catch (error) {
        console.error('保存认证信息时出错:', error);
        throw error;
    }
}

// 清除认证信息
window.clearAuth = function() {
    localStorage.removeItem('token');
    localStorage.removeItem('tokenExpiry');
    localStorage.removeItem('username');
    localStorage.removeItem('isSuperuser');
}

// 检查 token 是否即将过期（例如：5分钟内过期）
window.isTokenExpiringSoon = function() {
    const tokenExpiry = localStorage.getItem('tokenExpiry');
    if (!tokenExpiry) return true;
    
    const expiryDate = new Date(tokenExpiry);
    const now = new Date();
    const fiveMinutes = 5 * 60 * 1000; // 5分钟（毫秒）
    
    return (expiryDate - now) < fiveMinutes;
}

// 刷新 token
window.refreshToken = async function() {
    const token = localStorage.getItem('token');
    if (!token) return false;
    
    try {
        const response = await fetch('/api/v1/auth/refresh', {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        
        if (response.ok) {
            const data = await response.json();
            window.saveAuth(data.access_token, data.expires_in);
            return true;
        }
    } catch (error) {
        console.error('刷新 token 失败:', error);
    }
    return false;
}

// 定期检查 token 状态
window.checkTokenStatus = async function() {
    if (window.isTokenExpiringSoon()) {
        const refreshed = await window.refreshToken();
        if (!refreshed) {
            window.clearAuth();
            if (!window.location.pathname.includes('/login')) {
                window.location.href = '/login';
            }
        }
    }
}

// 启动定期检查
setInterval(window.checkTokenStatus, 60000); // 每分钟检查一次

// 初始化页面
// 移除这里的初始化代码，因为现在由各个页面自己处理初始化
// document.addEventListener('DOMContentLoaded', async () => {
//     await loadNavbar();
//     setupLogoutButton();
// }); 