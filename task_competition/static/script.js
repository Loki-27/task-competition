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

/**
 * Timer Manager Class
 */
class TimerManager {
    constructor(taskId, durationMinutes = 60) {
        this.taskId = taskId;
        this.durationSeconds = durationMinutes * 60;
        this.elapsedSeconds = 0;
        this.isRunning = false;
        this.intervalId = null;
        this.storageKey = `timer_${taskId}`;
        
        // Load saved state from localStorage
        this.loadState();
    }

    /**
     * Load timer state from localStorage
     */
    loadState() {
        const saved = localStorage.getItem(this.storageKey);
        if (saved) {
            const state = JSON.parse(saved);
            this.elapsedSeconds = state.elapsed || 0;
            this.isRunning = false; // Never auto-start, require user action
        }
    }

    /**
     * Save timer state to localStorage
     */
    saveState() {
        const state = {
            elapsed: this.elapsedSeconds,
            timestamp: Date.now()
        };
        localStorage.setItem(this.storageKey, JSON.stringify(state));
    }

    /**
     * Format seconds to HH:MM:SS
     */
    static formatTime(seconds) {
        const hours = Math.floor(seconds / 3600);
        const minutes = Math.floor((seconds % 3600) / 60);
        const secs = seconds % 60;
        
        return `${String(hours).padStart(2, '0')}:${String(minutes).padStart(2, '0')}:${String(secs).padStart(2, '0')}`;
    }

    /**
     * Start or resume timer
     */
    start() {
        if (this.isRunning) return;
        
        this.isRunning = true;
        this.intervalId = setInterval(() => {
            this.elapsedSeconds++;
            this.saveState();
            this.updateDisplay();
            
            // Check for warnings and danger states
            const remaining = this.durationSeconds - this.elapsedSeconds;
            if (remaining === 300) { // 5 minutes left
                showNotification('⏰ 5 minutes remaining', 'warning');
            } else if (remaining === 0) {
                this.stop();
                showNotification('⏱️ Time\'s up!', 'info');
            }
        }, 1000);
    }

    /**
     * Pause timer
     */
    pause() {
        this.isRunning = false;
        if (this.intervalId) {
            clearInterval(this.intervalId);
            this.intervalId = null;
        }
        this.saveState();
        this.updateDisplay();
    }

    /**
     * Reset timer
     */
    reset() {
        this.isRunning = false;
        if (this.intervalId) {
            clearInterval(this.intervalId);
            this.intervalId = null;
        }
        this.elapsedSeconds = 0;
        localStorage.removeItem(this.storageKey);
        this.updateDisplay();
    }

    /**
     * Stop and save completion
     */
    async stop() {
        this.pause();
        
        try {
            const response = await fetch(`/tasks/${this.taskId}/timer/stop`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    elapsed_seconds: this.elapsedSeconds
                })
            });
            
            if (response.ok) {
                const data = await response.json();
                showNotification(`✓ Task completed! +${data.points} points`, 'success');
                localStorage.removeItem(this.storageKey);
                setTimeout(() => location.reload(), 1500);
            } else {
                showNotification('Error saving task completion', 'error');
            }
        } catch (error) {
            console.error('Error:', error);
            showNotification('Error saving task completion', 'error');
        }
    }

    /**
     * Update timer display
     */
    updateDisplay() {
        const display = document.getElementById(`timer-display-${this.taskId}`);
        if (display) {
            display.textContent = TimerManager.formatTime(this.elapsedSeconds);
            
            // Update progress bar
            const progressFill = document.getElementById(`timer-progress-${this.taskId}`);
            if (progressFill) {
                const percent = (this.elapsedSeconds / this.durationSeconds) * 100;
                progressFill.style.width = Math.min(percent, 100) + '%';
            }
            
            // Update remaining time
            const remaining = this.durationSeconds - this.elapsedSeconds;
            const warningEl = document.getElementById(`timer-warning-${this.taskId}`);
            if (warningEl) {
                warningEl.textContent = `${TimerManager.formatTime(remaining)} remaining`;
                
                // Add visual warnings
                if (remaining <= 0) {
                    display.classList.add('danger');
                    display.classList.remove('warning');
                } else if (remaining <= 300) { // 5 minutes
                    display.classList.add('warning');
                    display.classList.remove('danger');
                } else {
                    display.classList.remove('warning', 'danger');
                }
            }
            
            // Update button states
            this.updateButtonStates();
        }
    }

    /**
     * Update button states based on timer state
     */
    updateButtonStates() {
        const startBtn = document.getElementById(`timer-start-${this.taskId}`);
        const pauseBtn = document.getElementById(`timer-pause-${this.taskId}`);
        const stopBtn = document.getElementById(`timer-stop-${this.taskId}`);
        
        if (startBtn) {
            startBtn.disabled = this.isRunning;
            startBtn.textContent = this.elapsedSeconds > 0 ? '▶ Resume' : '▶ Start';
        }
        if (pauseBtn) {
            pauseBtn.disabled = !this.isRunning;
        }
        if (stopBtn) {
            stopBtn.disabled = this.elapsedSeconds === 0;
        }
    }
}

// Initialize timers on the page
window.TimerManager = TimerManager;

// Export for global use
window.initializeTimer = function(taskId, durationMinutes) {
    return new TimerManager(taskId, durationMinutes);
};