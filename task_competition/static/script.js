// Daily Task Competition - JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips and popovers if using Bootstrap
    initializeBootstrapComponents();
    
    // Add any custom functionality here
    setupFormValidation();
});

/**
 * Initialize Bootstrap components like tooltips and popovers
 */
function initializeBootstrapComponents() {
    // Tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Popovers
    const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });
}

/**
 * Setup client-side form validation
 */
function setupFormValidation() {
    const forms = document.querySelectorAll('form');
    
    forms.forEach(function(form) {
        form.addEventListener('submit', function(event) {
            if (form.checkValidity() === false) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        }, false);
    });
}

/**
 * Show confirmation dialog for important actions
 */
function confirmAction(message = 'Are you sure?') {
    return confirm(message);
}

/**
 * Format currency or points display
 */
function formatPoints(points) {
    if (points >= 0) {
        return '+' + points;
    }
    return points.toString();
}

/**
 * Update points display dynamically
 */
function updatePointsDisplay(elementId, points) {
    const element = document.getElementById(elementId);
    if (element) {
        element.textContent = formatPoints(points);
        element.classList.toggle('text-success', points >= 0);
        element.classList.toggle('text-danger', points < 0);
    }
}

/**
 * Copy text to clipboard
 */
function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(function() {
        // Show success message
        showNotification('Copied to clipboard!', 'success');
    }).catch(function() {
        showNotification('Failed to copy', 'error');
    });
}

/**
 * Show temporary notification
 */
function showNotification(message, type = 'info') {
    const alertClass = `alert-${type}`;
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert ${alertClass} alert-dismissible fade show`;
    alertDiv.setAttribute('role', 'alert');
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    const container = document.querySelector('main .container-fluid');
    if (container) {
        container.insertBefore(alertDiv, container.firstChild);
        
        // Auto-dismiss after 3 seconds
        setTimeout(function() {
            alertDiv.remove();
        }, 3000);
    }
}

/**
 * Format date for display
 */
function formatDate(dateString) {
    const options = { year: 'numeric', month: 'long', day: 'numeric', hour: '2-digit', minute: '2-digit' };
    return new Date(dateString).toLocaleDateString('en-US', options);
}

/**
 * Handle task completion animation
 */
function animateTaskCompletion(element) {
    element.classList.add('fade-out');
    setTimeout(function() {
        element.classList.remove('fade-out');
    }, 500);
}

// Export functions for use in HTML
window.confirmAction = confirmAction;
window.copyToClipboard = copyToClipboard;
window.formatPoints = formatPoints;
window.showNotification = showNotification;
window.formatDate = formatDate;
