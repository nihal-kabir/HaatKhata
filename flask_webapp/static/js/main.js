// Main JavaScript for Task Manager

document.addEventListener('DOMContentLoaded', function() {
    // Set dynamic category colors
    const categoryBadges = document.querySelectorAll('.category-badge[data-color]');
    categoryBadges.forEach(badge => {
        const color = badge.getAttribute('data-color');
        if (color) {
            badge.style.backgroundColor = color;
            badge.style.color = 'white';
        }
    });

    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Add fade-in animation to cards
    const cards = document.querySelectorAll('.card');
    cards.forEach((card, index) => {
        setTimeout(() => {
            card.classList.add('fade-in');
        }, index * 100);
    });

    // Task card hover effects
    const taskCards = document.querySelectorAll('.task-card');
    taskCards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-5px)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
        });
    });

    // Auto-hide flash messages after 5 seconds
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });

    // Form validation
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        });
    });

    // Search functionality
    const searchInput = document.querySelector('input[name="search"]');
    if (searchInput) {
        searchInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                this.closest('form').submit();
            }
        });
    }

    // Priority color indicators
    const prioritySelects = document.querySelectorAll('select[name="priority"]');
    prioritySelects.forEach(select => {
        updatePriorityColor(select);
        select.addEventListener('change', function() {
            updatePriorityColor(this);
        });
    });

    function updatePriorityColor(select) {
        const value = select.value;
        select.className = select.className.replace(/\bbg-\w+/g, '');
        
        switch(value) {
            case 'high':
                select.classList.add('bg-danger', 'text-white');
                break;
            case 'medium':
                select.classList.add('bg-warning');
                break;
            case 'low':
                select.classList.add('bg-success', 'text-white');
                break;
        }
    }

    // Status update functionality
    const statusSelects = document.querySelectorAll('select[name="status"]');
    statusSelects.forEach(select => {
        updateStatusColor(select);
        select.addEventListener('change', function() {
            updateStatusColor(this);
        });
    });

    function updateStatusColor(select) {
        const value = select.value;
        select.className = select.className.replace(/\bbg-\w+/g, '');
        
        switch(value) {
            case 'completed':
                select.classList.add('bg-success', 'text-white');
                break;
            case 'in_progress':
                select.classList.add('bg-info', 'text-white');
                break;
            case 'pending':
                select.classList.add('bg-warning');
                break;
        }
    }

    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth'
                });
            }
        });
    });

    // Dynamic progress bar animation
    const progressBars = document.querySelectorAll('.progress-bar');
    progressBars.forEach(bar => {
        const width = bar.style.width;
        bar.style.width = '0%';
        setTimeout(() => {
            bar.style.width = width;
        }, 500);
    });
});

// Utility functions
function showToast(message, type = 'info') {
    const toastContainer = document.getElementById('toast-container') || createToastContainer();
    
    const toast = document.createElement('div');
    toast.className = `toast align-items-center text-white bg-${type} border-0`;
    toast.setAttribute('role', 'alert');
    
    toast.innerHTML = `
        <div class="d-flex">
            <div class="toast-body">${message}</div>
            <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
        </div>
    `;
    
    toastContainer.appendChild(toast);
    
    const bsToast = new bootstrap.Toast(toast);
    bsToast.show();
    
    // Remove toast element after it's hidden
    toast.addEventListener('hidden.bs.toast', () => {
        toast.remove();
    });
}

function createToastContainer() {
    const container = document.createElement('div');
    container.id = 'toast-container';
    container.className = 'toast-container position-fixed bottom-0 end-0 p-3';
    document.body.appendChild(container);
    return container;
}

// Confirmation dialogs
function confirmDelete(message = 'Are you sure you want to delete this item?') {
    return confirm(message);
}

// Loading states
function showLoading(element) {
    element.disabled = true;
    const originalText = element.innerHTML;
    element.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Loading...';
    
    return function hideLoading() {
        element.disabled = false;
        element.innerHTML = originalText;
    };
}
