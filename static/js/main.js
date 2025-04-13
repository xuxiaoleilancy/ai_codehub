document.addEventListener('DOMContentLoaded', () => {
    // 获取DOM元素
    const loginForm = document.getElementById('loginForm');
    const registerForm = document.getElementById('registerForm');
    const tabButtons = document.querySelectorAll('.tab-btn');
    const userInfo = document.getElementById('userInfo');
    const usernameSpan = document.getElementById('username');
    const logoutBtn = document.getElementById('logoutBtn');

    // 检查是否已登录
    const token = localStorage.getItem('token');
    if (token) {
        fetchUserInfo();
    }

    // 标签页切换
    tabButtons.forEach(button => {
        button.addEventListener('click', () => {
            const tabId = button.dataset.tab;
            
            // 更新按钮状态
            tabButtons.forEach(btn => btn.classList.remove('active'));
            button.classList.add('active');
            
            // 显示对应的内容
            document.querySelectorAll('.tab-pane').forEach(pane => {
                pane.classList.remove('active');
            });
            document.getElementById(tabId).classList.add('active');
        });
    });

    // 登录表单提交
    loginForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const formData = new FormData(loginForm);
        const data = {
            username: formData.get('username'),
            password: formData.get('password')
        };

        try {
            const response = await fetch('/api/auth/token', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: new URLSearchParams(data)
            });

            if (response.ok) {
                const result = await response.json();
                localStorage.setItem('token', result.access_token);
                showUserInfo(result.username);
                showMessage('Login successful!', 'success');
            } else {
                const error = await response.json();
                showMessage(error.detail || 'Login failed', 'error');
            }
        } catch (error) {
            showMessage('An error occurred', 'error');
        }
    });

    // 注册表单提交
    registerForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const formData = new FormData(registerForm);
        const data = {
            username: formData.get('username'),
            email: formData.get('email'),
            password: formData.get('password')
        };

        try {
            const response = await fetch('/api/auth/register', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data)
            });

            if (response.ok) {
                showMessage('Registration successful! Please login.', 'success');
                // 切换到登录标签
                document.querySelector('[data-tab="login"]').click();
            } else {
                const error = await response.json();
                showMessage(error.detail || 'Registration failed', 'error');
            }
        } catch (error) {
            showMessage('An error occurred', 'error');
        }
    });

    // 登出
    logoutBtn.addEventListener('click', () => {
        localStorage.removeItem('token');
        userInfo.style.display = 'none';
        document.querySelector('.auth-container').style.display = 'block';
    });

    // 获取用户信息
    async function fetchUserInfo() {
        try {
            const response = await fetch('/api/auth/me', {
                headers: {
                    'Authorization': `Bearer ${localStorage.getItem('token')}`
                }
            });

            if (response.ok) {
                const user = await response.json();
                showUserInfo(user.username);
            } else {
                localStorage.removeItem('token');
            }
        } catch (error) {
            localStorage.removeItem('token');
        }
    }

    // 显示用户信息
    function showUserInfo(username) {
        usernameSpan.textContent = username;
        userInfo.style.display = 'block';
        document.querySelector('.auth-container').style.display = 'none';
    }

    // 显示消息
    function showMessage(message, type) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `${type}-message`;
        messageDiv.textContent = message;

        const container = document.querySelector('.auth-container');
        container.insertBefore(messageDiv, container.firstChild);

        setTimeout(() => {
            messageDiv.remove();
        }, 3000);
    }
}); 