document.addEventListener('DOMContentLoaded', () => {
    const uploadForm = document.getElementById('uploadForm');
    const modelList = document.getElementById('modelList');
    const searchInput = document.getElementById('searchInput');
    const frameworkFilter = document.getElementById('frameworkFilter');
    const taskFilter = document.getElementById('taskFilter');
    const modal = document.getElementById('modelModal');
    const closeBtn = document.querySelector('.close');
    const updateModelBtn = document.getElementById('updateModelBtn');
    const deleteModelBtn = document.getElementById('deleteModelBtn');
    const logoutBtn = document.getElementById('logoutBtn');

    let currentModels = [];
    let selectedModel = null;

    // 检查认证状态
    const token = localStorage.getItem('token');
    if (!token) {
        window.location.href = '/';
        return;
    }

    // 加载模型列表
    async function loadModels() {
        try {
            const response = await fetch('/api/models/list', {
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            });

            if (response.ok) {
                currentModels = await response.json();
                filterAndDisplayModels();
            } else {
                showMessage('Failed to load models', 'error');
            }
        } catch (error) {
            showMessage('An error occurred while loading models', 'error');
        }
    }

    // 过滤和显示模型
    function filterAndDisplayModels() {
        const searchTerm = searchInput.value.toLowerCase();
        const framework = frameworkFilter.value;
        const task = taskFilter.value;

        const filteredModels = currentModels.filter(model => {
            const matchesSearch = model.name.toLowerCase().includes(searchTerm) ||
                                (model.description && model.description.toLowerCase().includes(searchTerm));
            const matchesFramework = !framework || model.framework === framework;
            const matchesTask = !task || model.task_type === task;
            return matchesSearch && matchesFramework && matchesTask;
        });

        modelList.innerHTML = filteredModels.map(model => `
            <div class="model-card" data-model-name="${model.name}">
                <h3>${model.name}</h3>
                <p>${model.description || 'No description'}</p>
                <div class="model-meta">
                    <span>${model.framework} | ${model.task_type}</span>
                    <span>v${model.version}</span>
                </div>
            </div>
        `).join('');
    }

    // 上传模型
    uploadForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const formData = new FormData(uploadForm);
        
        try {
            const response = await fetch('/api/models/upload', {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${token}`
                },
                body: formData
            });

            if (response.ok) {
                showMessage('Model uploaded successfully', 'success');
                uploadForm.reset();
                loadModels();
            } else {
                const error = await response.json();
                showMessage(error.detail || 'Failed to upload model', 'error');
            }
        } catch (error) {
            showMessage('An error occurred while uploading', 'error');
        }
    });

    // 显示模型详情
    modelList.addEventListener('click', async (e) => {
        const card = e.target.closest('.model-card');
        if (!card) return;

        const modelName = card.dataset.modelName;
        try {
            const response = await fetch(`/api/models/${modelName}`, {
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            });

            if (response.ok) {
                selectedModel = await response.json();
                displayModelDetails(selectedModel);
                modal.style.display = 'block';
            } else {
                showMessage('Failed to load model details', 'error');
            }
        } catch (error) {
            showMessage('An error occurred while loading model details', 'error');
        }
    });

    // 显示模型详情
    function displayModelDetails(model) {
        document.getElementById('modelDetails').innerHTML = `
            <div class="detail-group">
                <label>Name:</label>
                <span>${model.name}</span>
            </div>
            <div class="detail-group">
                <label>Description:</label>
                <span>${model.description || 'No description'}</span>
            </div>
            <div class="detail-group">
                <label>Version:</label>
                <span>${model.version}</span>
            </div>
            <div class="detail-group">
                <label>Framework:</label>
                <span>${model.framework}</span>
            </div>
            <div class="detail-group">
                <label>Task Type:</label>
                <span>${model.task_type}</span>
            </div>
            <div class="detail-group">
                <label>Created By:</label>
                <span>${model.created_by}</span>
            </div>
            <div class="detail-group">
                <label>Created At:</label>
                <span>${new Date(model.created_at).toLocaleString()}</span>
            </div>
            <div class="detail-group">
                <label>File Size:</label>
                <span>${formatFileSize(model.file_size)}</span>
            </div>
        `;
    }

    // 更新模型
    updateModelBtn.addEventListener('click', async () => {
        if (!selectedModel) return;

        const description = prompt('Enter new description:', selectedModel.description);
        const version = prompt('Enter new version:', selectedModel.version);

        if (description === null && version === null) return;

        const formData = new FormData();
        if (description !== null) formData.append('description', description);
        if (version !== null) formData.append('version', version);

        try {
            const response = await fetch(`/api/models/${selectedModel.name}`, {
                method: 'PUT',
                headers: {
                    'Authorization': `Bearer ${token}`
                },
                body: formData
            });

            if (response.ok) {
                showMessage('Model updated successfully', 'success');
                modal.style.display = 'none';
                loadModels();
            } else {
                const error = await response.json();
                showMessage(error.detail || 'Failed to update model', 'error');
            }
        } catch (error) {
            showMessage('An error occurred while updating', 'error');
        }
    });

    // 删除模型
    deleteModelBtn.addEventListener('click', async () => {
        if (!selectedModel || !confirm('Are you sure you want to delete this model?')) return;

        try {
            const response = await fetch(`/api/models/${selectedModel.name}`, {
                method: 'DELETE',
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            });

            if (response.ok) {
                showMessage('Model deleted successfully', 'success');
                modal.style.display = 'none';
                loadModels();
            } else {
                const error = await response.json();
                showMessage(error.detail || 'Failed to delete model', 'error');
            }
        } catch (error) {
            showMessage('An error occurred while deleting', 'error');
        }
    });

    // 事件监听器
    searchInput.addEventListener('input', filterAndDisplayModels);
    frameworkFilter.addEventListener('change', filterAndDisplayModels);
    taskFilter.addEventListener('change', filterAndDisplayModels);
    closeBtn.addEventListener('click', () => modal.style.display = 'none');
    window.addEventListener('click', (e) => {
        if (e.target === modal) modal.style.display = 'none';
    });

    // 登出
    logoutBtn.addEventListener('click', () => {
        localStorage.removeItem('token');
        window.location.href = '/';
    });

    // 辅助函数
    function formatFileSize(bytes) {
        if (bytes === 0) return '0 Bytes';
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    }

    function showMessage(message, type) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `${type}-message`;
        messageDiv.textContent = message;
        document.querySelector('.container').insertBefore(messageDiv, document.querySelector('main'));
        setTimeout(() => messageDiv.remove(), 3000);
    }

    // 初始加载
    loadModels();
}); 