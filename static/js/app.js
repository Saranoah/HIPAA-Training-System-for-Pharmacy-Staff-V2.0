// Enhanced JavaScript from index.html with API integration
document.addEventListener('DOMContentLoaded', async () => {
    try {
        // Fetch CSRF token
        const csrfResponse = await fetch('/api/csrf_token', {
            method: 'GET',
            credentials: 'same-origin'
        });
        window.csrf_token = (await csrfResponse.json()).csrf_token;

        // Fetch initial progress
        const progressResponse = await fetch('/api/progress', {
            headers: { 'X-CSRF-Token': window.csrf_token }
        });
        const progress = await progressResponse.json();
        updateProgressUI(progress);

        // Set session timestamp
        document.getElementById('sessionTime').textContent = new Date().toLocaleString();

        // Initialize constellation
        initializeConstellation(progress);

        // Session timeout handling
        setTimeout(showTimeoutWarning, 13 * 60 * 1000); // 13 minutes
        setTimeout(handleSessionTimeout, 15 * 60 * 1000); // 15 minutes

    } catch (error) {
        console.error('Initialization error:', error);
    }
});

function updateProgressUI(progress) {
    document.querySelectorAll('.progress-bar').forEach(bar => {
        const module = bar.closest('.module-card');
        if (module) {
            const moduleType = module.querySelector('.module-title').textContent.toLowerCase();
            let width = 0;
            if (moduleType.includes('lessons')) {
                width = (progress.lessons_completed.length / 13) * 100;
                module.querySelector('.module-stats span:first-child').textContent = `${progress.lessons_completed.length}/13 Completed`;
            } else if (moduleType.includes('quiz')) {
                width = progress.quiz_taken ? 100 : 0;
                module.querySelector('.module-stats span:first-child').textContent = progress.quiz_taken ? `Score: ${progress.quiz_score}%` : 'Not Taken';
            } else if (moduleType.includes('checklist')) {
                const completedItems = Object.keys(progress).filter(key => key.startsWith('checklist_') && progress[key]).length;
                width = (completedItems / 15) * 100;
                module.querySelector('.module-stats span:first-child').textContent = `${completedItems}/15 Completed`;
            }
            bar.style.width = `${width}%`;
            bar.setAttribute('aria-valuenow', width);
        }
    });
}

function initializeConstellation(progress) {
    const constellation = document.getElementById('complianceConstellation');
    if (!constellation) return;

    const stars = [
        { name: "Privacy Rule", x: 50, y: 50 },
        // ... Include all stars from index.html ...
    ];

    stars.forEach((star, index) => {
        const starElement = document.createElement('div');
        starElement.className = `star ${progress.lessons_completed.includes(star.name) ? 'completed' : ''}`;
        starElement.style.left = `${star.x}px`;
        starElement.style.top = `${star.y}px`;
        starElement.tabIndex = 0;
        starElement.setAttribute('role', 'button');
        starElement.setAttribute('aria-label', `${star.name} - ${progress.lessons_completed.includes(star.name) ? 'Completed' : 'Not completed'}`);
        starElement.addEventListener('click', () => showLessonDetails(star.name));
        starElement.addEventListener('keypress', (e) => {
            if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault();
                showLessonDetails(star.name);
            }
        });
        constellation.appendChild(starElement);
    });

    for (let i = 0; i < stars.length - 1; i++) {
        const connection = document.createElement('div');
        connection.className = 'connection';
        const start = stars[i];
        const end = stars[i + 1];
        const length = Math.sqrt(Math.pow(end.x - start.x, 2) + Math.pow(end.y - start.y, 2));
        const angle = Math.atan2(end.y - start.y, end.x - start.x) * 180 / Math.PI;
        connection.style.width = `${length}px`;
        connection.style.left = `${start.x}px`;
        connection.style.top = `${start.y}px`;
        connection.style.transform = `rotate(${angle}deg)`;
        connection.setAttribute('aria-hidden', 'true');
        constellation.appendChild(connection);
    }
}

async function completeLesson(lessonName) {
    try {
        const response = await fetch('/api/complete_lesson', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRF-Token': window.csrf_token
            },
            body: JSON.stringify({ lesson_name: lessonName })
        });
        if (response.ok) {
            const progress = await (await fetch('/api/progress', {
                headers: { 'X-CSRF-Token': window.csrf_token }
            })).json();
            updateProgressUI(progress);
            initializeConstellation(progress);
        }
    } catch (error) {
        console.error('Lesson completion error:', error);
        alert('An error occurred while marking the lesson as complete.');
    }
}

function showLessonDetails(lessonName) {
    window.location.href = `/lessons#${lessonName.replace(/\s+/g, '-')}`;
}

function navigateTo(path) {
    window.location.href = path;
}

function handleModuleKeypress(event, pathOrLesson) {
    if (event.key === 'Enter' || event.key === ' ') {
        event.preventDefault();
        if (pathOrLesson.startsWith('/')) {
            navigateTo(pathOrLesson);
        } else {
            completeLesson(pathOrLesson);
        }
    }
}

let lastActivityTime = Date.now();
document.addEventListener('click', updateLastActivity);
document.addEventListener('keypress', updateLastActivity);
document.addEventListener('scroll', updateLastActivity);

function updateLastActivity() {
    lastActivityTime = Date.now();
    document.getElementById('lastActivity').textContent = new Date().toLocaleTimeString();
}

function showTimeoutWarning() {
    const warning = document.getElementById('timeoutWarning');
    if (warning) {
        warning.style.display = 'block';
        warning.setAttribute('aria-live', 'assertive');
    }
}

async function extendSession() {
    try {
        const response = await fetch('/api/extend_session', {
            method: 'POST',
            headers: { 'X-CSRF-Token': window.csrf_token }
        });
        if (response.ok) {
            const warning = document.getElementById('timeoutWarning');
            if (warning) warning.style.display = 'none';
            lastActivityTime = Date.now();
        }
    } catch (error) {
        console.error('Session extension error:', error);
    }
}

function handleSessionTimeout() {
    window.location.href = '/login?reason=timeout';
}
