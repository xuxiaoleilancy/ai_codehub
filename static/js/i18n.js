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

// 初始化语言
function initLanguage() {
    const savedLang = localStorage.getItem('language');
    if (!savedLang) {
        localStorage.setItem('language', 'cn');  // 默认设置为中文
    }
    updateTranslations(localStorage.getItem('language') || 'cn');
} 