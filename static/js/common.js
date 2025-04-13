// 加载导航栏
async function loadNavbar() {
    try {
        const response = await fetch('/components/navbar.html');
        if (!response.ok) {
            throw new Error('Failed to load navbar');
        }
        const html = await response.text();
        const navbarContainer = document.getElementById('navbar-container');
        navbarContainer.innerHTML = html;
        
        // 初始化语言
        const currentLang = localStorage.getItem('language') || 'cn';
        updateTranslations(currentLang);
        
        // 检查登录状态
        checkLoginStatus();
        
        // 添加登出按钮事件监听
        setupLogoutButton();
    } catch (error) {
        console.error('Error loading navbar:', error);
    }
}

// 设置退出登录按钮事件监听
function setupLogoutButton() {
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
                checkLoginStatus();
                
                // 延迟跳转到首页，确保导航栏已更新
                setTimeout(() => {
                    window.location.href = '/';
                }, 100);
            }
        });
    }
}

// 检查登录状态
function checkLoginStatus() {
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
function updateNavbarLoginState() {
    checkLoginStatus();
}

// 检查认证状态
function checkAuth() {
    const token = localStorage.getItem('token');
    if (!token) {
        window.location.href = '/login';
        return false;
    }
    return true;
}

// 初始化页面
document.addEventListener('DOMContentLoaded', async () => {
    await loadNavbar();
    setupLogoutButton();
}); 