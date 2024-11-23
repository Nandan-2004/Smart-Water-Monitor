function showNotification(message, type, duration = 3000, position = 'bottom') {
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    notification.textContent = message;

    // Set ARIA attributes for accessibility
    notification.setAttribute('role', 'alert');
    notification.setAttribute('aria-live', 'assertive');

    // Append to body or a specific container
    document.body.appendChild(notification);

    // Positioning logic
    notification.style.position = 'fixed';
    if (position === 'top') {
        notification.style.top = '20px';
    } else if (position === 'bottom') {
        notification.style.bottom = '20px';
    }
    notification.style.left = '50%';
    notification.style.transform = 'translateX(-50%)';

    // Show the notification with animation
    setTimeout(() => {
        notification.classList.add('show');
    }, 10);  // Adding delay to ensure that CSS transition works

    // Hide and remove the notification after the specified duration
    setTimeout(() => {
        // Remove the 'show' class after the duration
        notification.classList.remove('show');

        // Remove the notification completely after fade-out animation (300ms delay for fade effect)
        setTimeout(() => {
            notification.remove();
        }, 300);  // This delay should match the CSS transition time
    }, duration);  // This duration controls how long the notification stays visible
}

// Example Usage
showNotification("High water usage alert!", "error", 5000, "top");
showNotification("Reward earned for low usage!", "success", 3000, "bottom");
