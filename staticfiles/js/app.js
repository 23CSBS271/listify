// Listify Task Management App - JavaScript Functions

document.addEventListener('DOMContentLoaded', function() {
    // Initialize Bootstrap tooltips
    initializeTooltips();
    
    // Initialize notification system
    initializeNotifications();
    
    // Initialize reminder system
    initializeReminders();
    
    // Auto-hide alerts
    autoHideAlerts();
    
    // Initialize datetime inputs
    initializeDateTimeInputs();
    
    // Initialize form enhancements
    initializeFormEnhancements();
});

// Initialize Bootstrap tooltips
function initializeTooltips() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

// Auto-hide alert messages
function autoHideAlerts() {
    const alerts = document.querySelectorAll('.alert:not(.alert-danger)');
    alerts.forEach(function(alert) {
        if (!alert.classList.contains('alert-danger')) {
            setTimeout(function() {
                const alertInstance = bootstrap.Alert.getOrCreateInstance(alert);
                alertInstance.close();
            }, 5000);
        }
    });
}

// Initialize datetime inputs
function initializeDateTimeInputs() {
    const datetimeInputs = document.querySelectorAll('input[type="datetime-local"]');
    
    datetimeInputs.forEach(function(input) {
        // Set minimum date to current time
        const now = new Date();
        const year = now.getFullYear();
        const month = String(now.getMonth() + 1).padStart(2, '0');
        const day = String(now.getDate()).padStart(2, '0');
        const hours = String(now.getHours()).padStart(2, '0');
        const minutes = String(now.getMinutes()).padStart(2, '0');
        const minDateTime = `${year}-${month}-${day}T${hours}:${minutes}`;
        
        if (!input.value) {
            input.min = minDateTime;
        }
        
        // Add validation feedback
        input.addEventListener('change', function() {
            const selectedDate = new Date(this.value);
            const currentDate = new Date();
            
            if (selectedDate < currentDate) {
                this.classList.add('is-invalid');
                showToast('Warning', 'Selected deadline is in the past', 'warning');
            } else {
                this.classList.remove('is-invalid');
            }
        });
    });
}

// Initialize notification system
function initializeNotifications() {
    // Check for notification support
    if ('Notification' in window) {
        // Request permission if not already granted
        if (Notification.permission === 'default') {
            Notification.requestPermission();
        }
    }
    
    // Start checking for notifications every 5 minutes
    setInterval(checkNotifications, 300000); // 5 minutes
    
    // Initial check
    checkNotifications();
}

// Check for notifications
function checkNotifications() {
    if (!document.getElementById('notification-count')) return;
    
    fetch('/api/notifications')
        .then(response => response.json())
        .then(data => {
            updateNotificationBadge(data.notifications);
            
            // Show browser notifications for urgent tasks
            data.notifications.forEach(notification => {
                if (notification.type === 'urgent' && Notification.permission === 'granted') {
                    showBrowserNotification(notification);
                }
            });
        })
        .catch(error => {
            console.error('Error fetching notifications:', error);
        });
}

// Update notification badge
function updateNotificationBadge(notifications) {
    const badge = document.getElementById('notification-count');
    const notificationList = document.getElementById('notification-list');
    
    if (notifications.length > 0) {
        badge.textContent = notifications.length;
        badge.style.display = 'inline-block';
        
        // Update notification list
        notificationList.innerHTML = '';
        notifications.forEach(notification => {
            const listItem = document.createElement('li');
            listItem.innerHTML = `
                <div class="dropdown-item-text">
                    <div class="d-flex justify-content-between align-items-start">
                        <div>
                            <strong class="text-${notification.type === 'urgent' ? 'warning' : 'danger'}">
                                ${notification.title}
                            </strong>
                            <div class="small text-muted">${notification.message}</div>
                        </div>
                        <span class="badge bg-${notification.type === 'urgent' ? 'warning' : 'danger'} ms-2">
                            ${notification.priority}
                        </span>
                    </div>
                </div>
            `;
            notificationList.appendChild(listItem);
        });
        
        // Add divider and view all link
        const divider = document.createElement('li');
        divider.innerHTML = '<hr class="dropdown-divider">';
        notificationList.appendChild(divider);
        
        const viewAllLink = document.createElement('li');
        viewAllLink.innerHTML = `
            <a class="dropdown-item text-center" href="/dashboard">
                <i class="fas fa-eye me-1"></i>View All Tasks
            </a>
        `;
        notificationList.appendChild(viewAllLink);
    } else {
        badge.style.display = 'none';
        notificationList.innerHTML = '<li><span class="dropdown-item-text text-muted">No notifications</span></li>';
    }
}

// Show browser notification
function showBrowserNotification(notification) {
    if (Notification.permission === 'granted') {
        const browserNotification = new Notification(notification.title, {
            body: notification.message,
            icon: '/static/favicon.ico',
            tag: `task-${notification.task_id}`,
            requireInteraction: true
        });
        
        browserNotification.onclick = function() {
            window.focus();
            window.location.href = '/dashboard';
            browserNotification.close();
        };
        
        // Auto-close after 10 seconds
        setTimeout(() => {
            browserNotification.close();
        }, 10000);
    }
}

// Initialize reminder system
function initializeReminders() {
    // Check for reminders every hour
    setInterval(checkReminders, 3600000); // 1 hour
    
    // Initial check
    checkReminders();
}

// Check for reminders
function checkReminders() {
    fetch('/api/reminders')
        .then(response => response.json())
        .then(data => {
            if (data.upcoming.length > 0 || data.overdue.length > 0) {
                showReminderModal(data);
            }
        })
        .catch(error => {
            console.error('Error fetching reminders:', error);
        });
}

// Show reminder modal
function showReminderModal(reminders) {
    // Create modal if it doesn't exist
    let modal = document.getElementById('reminderModal');
    if (!modal) {
        modal = createReminderModal();
        document.body.appendChild(modal);
    }
    
    // Update modal content
    const modalBody = modal.querySelector('.modal-body');
    let content = '';
    
    if (reminders.upcoming.length > 0) {
        content += '<h6 class="text-warning"><i class="fas fa-clock me-2"></i>Due Soon</h6>';
        content += '<ul class="list-unstyled mb-3">';
        reminders.upcoming.forEach(task => {
            content += `
                <li class="mb-2">
                    <div class="d-flex justify-content-between align-items-center">
                        <div>
                            <strong>${task.title}</strong>
                            <div class="small text-muted">${task.category}</div>
                        </div>
                        <span class="badge bg-warning">${task.hours_left}h left</span>
                    </div>
                </li>
            `;
        });
        content += '</ul>';
    }
    
    if (reminders.overdue.length > 0) {
        content += '<h6 class="text-danger"><i class="fas fa-exclamation-triangle me-2"></i>Overdue</h6>';
        content += '<ul class="list-unstyled">';
        reminders.overdue.forEach(task => {
            content += `
                <li class="mb-2">
                    <div class="d-flex justify-content-between align-items-center">
                        <div>
                            <strong>${task.title}</strong>
                            <div class="small text-muted">${task.category}</div>
                        </div>
                        <span class="badge bg-danger">${task.hours_overdue}h overdue</span>
                    </div>
                </li>
            `;
        });
        content += '</ul>';
    }
    
    modalBody.innerHTML = content;
    
    // Show modal
    const bsModal = new bootstrap.Modal(modal);
    bsModal.show();
}

// Create reminder modal
function createReminderModal() {
    const modal = document.createElement('div');
    modal.className = 'modal fade';
    modal.id = 'reminderModal';
    modal.setAttribute('tabindex', '-1');
    modal.innerHTML = `
        <div class="modal-dialog">
            <div class="modal-content bg-secondary">
                <div class="modal-header bg-primary text-white">
                    <h5 class="modal-title">
                        <i class="fas fa-bell me-2"></i>Task Reminders
                    </h5>
                    <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal"></button>
                </div>
                <div class="modal-body">
                    <!-- Content will be populated dynamically -->
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                    <a href="/dashboard" class="btn btn-primary">View Tasks</a>
                </div>
            </div>
        </div>
    `;
    return modal;
}

// Initialize form enhancements
function initializeFormEnhancements() {
    // Add loading states to forms
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function() {
            const submitBtn = form.querySelector('button[type="submit"]');
            if (submitBtn) {
                submitBtn.disabled = true;
                submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Processing...';
            }
        });
    });
    
    // Add confirmation to delete buttons
    const deleteButtons = document.querySelectorAll('form[action*="delete"]');
    deleteButtons.forEach(form => {
        form.addEventListener('submit', function(e) {
            if (!confirm('Are you sure you want to delete this item?')) {
                e.preventDefault();
            }
        });
    });
}

// Utility function to show toast notifications
function showToast(title, message, type = 'info') {
    // Create toast container if it doesn't exist
    let toastContainer = document.getElementById('toast-container');
    if (!toastContainer) {
        toastContainer = document.createElement('div');
        toastContainer.id = 'toast-container';
        toastContainer.className = 'toast-container position-fixed top-0 end-0 p-3';
        toastContainer.style.zIndex = '1055';
        document.body.appendChild(toastContainer);
    }
    
    // Create toast
    const toast = document.createElement('div');
    toast.className = `toast align-items-center text-white bg-${type} border-0`;
    toast.setAttribute('role', 'alert');
    toast.innerHTML = `
        <div class="d-flex">
            <div class="toast-body">
                <strong>${title}</strong><br>${message}
            </div>
            <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
        </div>
    `;
    
    toastContainer.appendChild(toast);
    
    // Show toast
    const bsToast = new bootstrap.Toast(toast, { delay: 5000 });
    bsToast.show();
    
    // Remove toast element after it's hidden
    toast.addEventListener('hidden.bs.toast', function() {
        toast.remove();
    });
}

// Export functions for global use
window.ListifyApp = {
    showToast,
    checkNotifications,
    checkReminders,
    initializeTooltips
};
