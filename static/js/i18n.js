// Language management utility
const i18n = {
    currentLang: 'en',
    
    init() {
        // Get language from localStorage or browser preference
        const savedLang = localStorage.getItem('language');
        const browserLang = navigator.language.split('-')[0];
        this.currentLang = savedLang || (browserLang === 'zh' ? 'zh' : 'en');
        this.updatePageLanguage();
    },
    
    setLanguage(lang) {
        if (locales[lang]) {
            this.currentLang = lang;
            localStorage.setItem('language', lang);
            this.updatePageLanguage();
        }
    },
    
    getText(key) {
        return locales[this.currentLang][key] || key;
    },
    
    updatePageLanguage() {
        // Update all elements with data-i18n attribute
        document.querySelectorAll('[data-i18n]').forEach(element => {
            const key = element.getAttribute('data-i18n');
            if (element.tagName === 'INPUT' && element.type === 'submit') {
                element.value = this.getText(key);
            } else {
                element.textContent = this.getText(key);
            }
        });
        
        // Update placeholder text
        document.querySelectorAll('[data-i18n-placeholder]').forEach(element => {
            const key = element.getAttribute('data-i18n-placeholder');
            element.placeholder = this.getText(key);
        });
        
        // Update title
        document.querySelectorAll('[data-i18n-title]').forEach(element => {
            const key = element.getAttribute('data-i18n-title');
            element.title = this.getText(key);
        });
    }
}; 

// 更新页面上的翻译
function updateTranslations(lang) {
    const translations = window.translations || {};
    const elements = document.querySelectorAll('[data-i18n]');
    
    elements.forEach(element => {
        const key = element.getAttribute('data-i18n');
        if (translations[lang] && translations[lang][key]) {
            if (element.tagName.toLowerCase() === 'input' && element.type === 'text') {
                element.placeholder = translations[lang][key];
            } else {
                element.textContent = translations[lang][key];
            }
        }
    });

    // 更新页面语言
    document.documentElement.lang = lang;
    localStorage.setItem('language', lang);
}

// 切换语言
function switchLanguage(lang) {
    // 触发语言改变事件
    const event = new CustomEvent('languageChanged', {
        detail: { language: lang }
    });
    document.dispatchEvent(event);
}

// 初始化语言
document.addEventListener('DOMContentLoaded', () => {
    const savedLang = localStorage.getItem('language') || 'zh';
    updateTranslations(savedLang);
}); 