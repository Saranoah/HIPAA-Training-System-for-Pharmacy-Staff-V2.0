// static/js/app.js
document.addEventListener('DOMContentLoaded', () => {
    // Fetch CSRF token
    async function loadCsrfToken() {
        const response = await fetch('/api/csrf_token', {
            headers: { 'X-CSRF-Token': document.querySelector('meta[name="csrf-token"]').content }
        });
        const data = await response.json();
        document.querySelector('meta[name="csrf-token"]').content = data.csrf_token;
    }
    
    // Session timeout handling
    const timeoutWarning = document.getElementById('session-timeout-warning');
    const countdownElement = document.getElementById('countdown');
    let timeoutId;
    
    function startSessionTimeout() {
        const sessionDuration = 15 * 60 * 1000; // 15 minutes
        const warningDuration = 60 * 1000; // 1 minute warning
        timeoutId = setTimeout(() => {
            let timeLeft = 60;
            timeoutWarning.style.display = 'flex';
            countdownElement.textContent = timeLeft;
            
            const countdownInterval = setInterval(() => {
                timeLeft--;
                countdownElement.textContent = timeLeft;
                if (timeLeft <= 0) {
                    clearInterval(countdownInterval);
                    window.location.href = '/logout';
                }
            }, 1000);
        }, sessionDuration - warningDuration);
    }
    
    async function extendSession() {
        const response = await fetch('/api/extend_session', {
            method: 'POST',
            headers: { 'X-CSRF-Token': document.querySelector('meta[name="csrf-token"]').content }
        });
        if (response.ok) {
            timeoutWarning.style.display = 'none';
            clearTimeout(timeoutId);
            startSessionTimeout();
        }
    }
    
    // Initialize
    loadCsrfToken();
    startSessionTimeout();
    
    // Expose extendSession globally for button onclick
    window.extendSession = extendSession;
});
