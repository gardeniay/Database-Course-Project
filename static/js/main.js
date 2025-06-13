document.addEventListener('DOMContentLoaded', function () {
    // 为所有表单添加提交前验证
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function (event) {
            const inputs = form.querySelectorAll('input[type="text"], input[type="int"]');

            // 检查是否有空字段
            for (let input of inputs) {
                if (input.value.trim() === '' && !input.hasAttribute('data-optional')) {
                    event.preventDefault();
                    showAlert('请填写所有必填字段', 'error');
                    input.focus();
                    return;
                }
            }
        });
    });

    // 点赞按钮交互
    const likeBtns = document.querySelectorAll('.like-btn');
    likeBtns.forEach(btn => {
        btn.addEventListener('click', function () {
            // 视觉反馈
            this.classList.add('liked');

            // 更新计数显示（实际操作由表单提交执行）
            const countEl = this.querySelector('.like-count');
            if (countEl) {
                const currentCount = parseInt(countEl.innerText);
                countEl.innerText = currentCount + 1;
            }
        });
    });

    // 添加平滑滚动
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();

            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                window.scrollTo({
                    top: target.offsetTop,
                    behavior: 'smooth'
                });
            }
        });
    });

    // 实现消息提示框
    window.showAlert = function (message, type = 'info') {
        const alertDiv = document.createElement('div');
        alertDiv.className = `alert alert-${type === 'error' ? 'danger' : type}`;
        alertDiv.textContent = message;

        const container = document.querySelector('.container') || document.body;
        container.insertBefore(alertDiv, container.firstChild);

        // 3秒后自动消失
        setTimeout(() => {
            alertDiv.style.opacity = '0';
            alertDiv.style.transition = 'opacity 0.5s';

            setTimeout(() => {
                alertDiv.remove();
            }, 500);
        }, 3000);
    };

    // 实现表单字段验证
    const validateField = function (input) {
        const value = input.value.trim();
        const dataType = input.getAttribute('data-type');

        if (!value && !input.hasAttribute('data-optional')) {
            return { valid: false, message: '此字段不能为空' };
        }

        if (dataType === 'number' && value && !/^\d+$/.test(value)) {
            return { valid: false, message: '请输入有效的数字' };
        }

        return { valid: true };
    };

    // 为输入框添加验证
    document.querySelectorAll('input[type="text"], input[type="int"]').forEach(input => {
        input.addEventListener('blur', function () {
            const result = validateField(this);

            // 移除之前的错误提示
            const nextEl = this.nextElementSibling;
            if (nextEl && nextEl.classList.contains('error-message')) {
                nextEl.remove();
            }

            // 显示新的错误提示
            if (!result.valid) {
                const errorMessage = document.createElement('div');
                errorMessage.className = 'error-message';
                errorMessage.style.color = '#f44336';
                errorMessage.style.fontSize = '0.8rem';
                errorMessage.style.marginTop = '5px';
                errorMessage.textContent = result.message;

                this.parentNode.insertBefore(errorMessage, this.nextSibling);
            }
        });
    });

    // 为删除按钮添加确认功能
    document.querySelectorAll('.btn-danger, button[type="submit"][value="删除"]').forEach(btn => {
        btn.addEventListener('click', function (event) {
            if (!confirm('确定要删除吗？此操作不可撤销')) {
                event.preventDefault();
            }
        });
    });
}); 