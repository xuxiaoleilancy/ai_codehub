const translations = {
    en: {
        // Navigation
        home: 'Home',
        documentation: 'Documentation',
        examples: 'Examples',
        login: 'Log in',
        signup: 'Sign up',
        // Language
        language: 'Language',
        // User
        profile: 'Profile',
        settings: 'Settings',
        logout: 'Log out',
        // Messages
        welcome: 'Welcome to AI CodeHub',
        // Add more translations as needed
    },
    cn: {
        // Navigation
        home: '首页',
        documentation: '文档',
        examples: '示例',
        login: '登录',
        signup: '注册',
        // Language
        language: '语言',
        // User
        profile: '个人资料',
        settings: '设置',
        logout: '退出登录',
        // Messages
        welcome: '欢迎使用 AI CodeHub',
        // Add more translations as needed
    }
};

// 获取当前语言
function getCurrentLanguage() {
    return localStorage.getItem('language') || 'en';
}

// 设置语言
function setLanguage(lang) {
    localStorage.setItem('language', lang);
    updatePageLanguage();
    // 刷新页面以应用语言更改
    window.location.reload();
}

// 更新页面语言
function updatePageLanguage() {
    const lang = getCurrentLanguage();
    const elements = document.querySelectorAll('[data-translate]');
    
    elements.forEach(element => {
        const key = element.getAttribute('data-translate');
        if (translations[lang] && translations[lang][key]) {
            if (element.tagName === 'INPUT' && element.type === 'placeholder') {
                element.placeholder = translations[lang][key];
            } else {
                element.textContent = translations[lang][key];
            }
        }
    });
}

// 初始化语言
document.addEventListener('DOMContentLoaded', () => {
    updatePageLanguage();
    
    // 更新语言切换按钮状态
    const langEn = document.getElementById('lang-en');
    const langCn = document.getElementById('lang-cn');
    const currentLang = getCurrentLanguage();
    
    if (langEn && langCn) {
        if (currentLang === 'en') {
            langEn.classList.add('active');
            langCn.classList.remove('active');
        } else {
            langEn.classList.remove('active');
            langCn.classList.add('active');
        }
    }
}); 