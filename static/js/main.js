// Toast Notifications
class ToastNotification {
    constructor() {
        this.container = document.createElement('div');
        this.container.className = 'notifications';
        document.body.appendChild(this.container);
    }

    show(message, type = 'info', duration = 3000) {
        const toast = document.createElement('div');
        toast.className = `toast toast--${type}`;
        
        const icon = document.createElement('i');
        icon.className = this.getIconClass(type);
        
        const text = document.createElement('span');
        text.textContent = message;
        
        toast.appendChild(icon);
        toast.appendChild(text);
        this.container.appendChild(toast);

        setTimeout(() => {
            toast.style.opacity = '0';
            setTimeout(() => toast.remove(), 300);
        }, duration);
    }

    getIconClass(type) {
        const icons = {
            success: 'fas fa-check-circle',
            error: 'fas fa-times-circle',
            warning: 'fas fa-exclamation-circle',
            info: 'fas fa-info-circle'
        };
        return icons[type] || icons.info;
    }
}

// Form Validation
class FormValidator {
    constructor(form) {
        this.form = form;
        this.setupValidation();
    }

    setupValidation() {
        const inputs = this.form.querySelectorAll('input, select, textarea');
        
        inputs.forEach(input => {
            input.addEventListener('blur', () => this.validateField(input));
            input.addEventListener('input', () => this.validateField(input));
        });

        this.form.addEventListener('submit', (e) => {
            let isValid = true;
            inputs.forEach(input => {
                if (!this.validateField(input)) {
                    isValid = false;
                }
            });

            if (!isValid) {
                e.preventDefault();
            }
        });
    }

    validateField(input) {
        const value = input.value.trim();
        let isValid = true;
        let message = '';

        // Required field
        if (input.hasAttribute('required') && !value) {
            isValid = false;
            message = 'Este campo é obrigatório';
        }

        // Email validation
        if (input.type === 'email' && value) {
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (!emailRegex.test(value)) {
                isValid = false;
                message = 'Email inválido';
            }
        }

        // Phone validation
        if (input.id === 'phone' && value) {
            const phoneRegex = /^\(\d{2}\) \d{4,5}-\d{4}$/;
            if (!phoneRegex.test(value)) {
                isValid = false;
                message = 'Telefone inválido';
            }
        }

        this.updateFieldStatus(input, isValid, message);
        return isValid;
    }

    updateFieldStatus(input, isValid, message) {
        const feedback = input.nextElementSibling?.classList.contains('form-feedback')
            ? input.nextElementSibling
            : document.createElement('div');

        if (!input.nextElementSibling?.classList.contains('form-feedback')) {
            feedback.className = 'form-feedback';
            input.parentNode.insertBefore(feedback, input.nextSibling);
        }

        input.className = `form-control ${isValid ? 'is-valid' : 'is-invalid'}`;
        feedback.className = `form-feedback ${isValid ? 'is-valid' : 'is-invalid'}`;
        feedback.textContent = message;
    }
}

// Input Masks
class InputMask {
    static phone(input) {
        input.addEventListener('input', (e) => {
            let value = e.target.value.replace(/\D/g, '');
            if (value.length <= 11) {
                value = value.replace(/^(\d{2})(\d)/g, '($1) $2');
                value = value.replace(/(\d)(\d{4})$/, '$1-$2');
                e.target.value = value;
            }
        });
    }
}

// Modal
class Modal {
    constructor(content, options = {}) {
        this.options = {
            closeOnBackdrop: true,
            ...options
        };
        this.createModal(content);
    }

    createModal(content) {
        this.modal = document.createElement('div');
        this.modal.className = 'modal';
        
        const modalContent = document.createElement('div');
        modalContent.className = 'modal__content';
        modalContent.innerHTML = content;

        const closeBtn = document.createElement('button');
        closeBtn.className = 'modal__close btn btn-icon';
        closeBtn.innerHTML = '<i class="fas fa-times"></i>';
        closeBtn.addEventListener('click', () => this.close());

        modalContent.insertBefore(closeBtn, modalContent.firstChild);
        this.modal.appendChild(modalContent);

        if (this.options.closeOnBackdrop) {
            this.modal.addEventListener('click', (e) => {
                if (e.target === this.modal) this.close();
            });
        }

        document.body.appendChild(this.modal);
    }

    open() {
        setTimeout(() => this.modal.classList.add('show'), 10);
    }

    close() {
        this.modal.classList.remove('show');
        setTimeout(() => this.modal.remove(), 300);
    }
}

// Breadcrumbs
class Breadcrumbs {
    constructor(container) {
        this.container = container;
        this.items = [];
    }

    addItem(label, url = null) {
        this.items.push({ label, url });
        this.render();
    }

    render() {
        this.container.innerHTML = this.items
            .map((item, index) => {
                const isLast = index === this.items.length - 1;
                const content = item.url
                    ? `<a href="${item.url}">${item.label}</a>`
                    : item.label;
                
                return `
                    <div class="breadcrumbs__item">
                        ${content}
                        ${!isLast ? '<i class="fas fa-chevron-right breadcrumbs__separator"></i>' : ''}
                    </div>
                `;
            })
            .join('');
    }
}

// Initialize components
document.addEventListener('DOMContentLoaded', () => {
    // Initialize toast notifications
    window.toast = new ToastNotification();

    // Initialize form validation
    document.querySelectorAll('form').forEach(form => {
        new FormValidator(form);
    });

    // Initialize phone masks
    document.querySelectorAll('input[type="tel"], input#phone').forEach(input => {
        InputMask.phone(input);
    });

    // Initialize breadcrumbs
    const breadcrumbsContainer = document.querySelector('.breadcrumbs');
    if (breadcrumbsContainer) {
        window.breadcrumbs = new Breadcrumbs(breadcrumbsContainer);
    }
});

// Skeleton Loading
function createSkeleton(type, count = 1) {
    const skeletons = [];
    for (let i = 0; i < count; i++) {
        const skeleton = document.createElement('div');
        skeleton.className = `skeleton skeleton--${type}`;
        skeletons.push(skeleton);
    }
    return skeletons;
}

// Search functionality
function setupSearch(input, items) {
    input.addEventListener('input', (e) => {
        const value = e.target.value.toLowerCase();
        items.forEach(item => {
            const text = item.textContent.toLowerCase();
            item.style.display = text.includes(value) ? '' : 'none';
        });
    });
}
