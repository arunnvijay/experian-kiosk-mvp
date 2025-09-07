// Authentication JavaScript for Experian Kiosk MVP
// File: frontend/assets/js/auth.js

class AuthManager {
    constructor() {
        this.apiBaseUrl = 'http://127.0.0.1:8000'; // Your backend URL
        this.initializeAuth();
    }

    initializeAuth() {
        // Check if user is already logged in
        if (this.isLoggedIn()) {
            this.redirectToDashboard();
        }

        // Add form submission handler
        this.setupFormHandler();
    }

    setupFormHandler() {
        const loginForm = document.querySelector('form');
        if (loginForm) {
            loginForm.addEventListener('submit', (e) => this.handleLogin(e));
        }
    }

    async handleLogin(event) {
        event.preventDefault();
        
        const username = document.getElementById('username').value.trim();
        const password = document.getElementById('password').value.trim();

        // Basic validation
        if (!username || !password) {
            this.showError('Please enter both username and password');
            return;
        }

        // Show loading state
        this.setLoadingState(true);

        try {
            // For MVP: Check hardcoded credentials
            if (await this.authenticateUser(username, password)) {
                this.handleSuccessfulLogin(username);
            } else {
                this.showError('Invalid username or password');
            }
        } catch (error) {
            console.error('Login error:', error);
            this.showError('Login failed. Please try again.');
        } finally {
            this.setLoadingState(false);
        }
    }

    async authenticateUser(username, password) {
        try {
            // MVP Version: Hardcoded authentication
            const response = await fetch(`${this.apiBaseUrl}/api/auth/login`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ username, password })
            });

            if (response.ok) {
                const data = await response.json();
                return data.success;
            }
            
            return false;
        } catch (error) {
            // Fallback for MVP: Check hardcoded credentials locally
            console.log('API not available, using local auth');
            return this.checkHardcodedCredentials(username, password);
        }
    }

    checkHardcodedCredentials(username, password) {
        // MVP hardcoded credentials
        return username === 'admin' && password === 'admin';
    }

    handleSuccessfulLogin(username) {
        // Store session information
        sessionStorage.setItem('isLoggedIn', 'true');
        sessionStorage.setItem('username', username);
        sessionStorage.setItem('loginTime', new Date().toISOString());

        // Show success message briefly
        this.showSuccess('Login successful! Redirecting...');

        // Redirect to dashboard after short delay
        setTimeout(() => {
            this.redirectToDashboard();
        }, 1000);
    }

    redirectToDashboard() {
        window.location.href = 'dashboard.html';
    }

    isLoggedIn() {
        return sessionStorage.getItem('isLoggedIn') === 'true';
    }

    logout() {
        sessionStorage.clear();
        window.location.href = 'index.html';
    }

    setLoadingState(isLoading) {
        const loginButton = document.querySelector('button[type="submit"]');
        const usernameInput = document.getElementById('username');
        const passwordInput = document.getElementById('password');

        if (isLoading) {
            loginButton.disabled = true;
            loginButton.innerHTML = `
                <svg class="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                    <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                    <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                Logging in...
            `;
            usernameInput.disabled = true;
            passwordInput.disabled = true;
        } else {
            loginButton.disabled = false;
            loginButton.innerHTML = 'Login';
            usernameInput.disabled = false;
            passwordInput.disabled = false;
        }
    }

    showError(message) {
        this.removeExistingMessages();
        const errorDiv = this.createMessageDiv(message, 'error');
        this.insertMessageDiv(errorDiv);
    }

    showSuccess(message) {
        this.removeExistingMessages();
        const successDiv = this.createMessageDiv(message, 'success');
        this.insertMessageDiv(successDiv);
    }

    createMessageDiv(message, type) {
        const div = document.createElement('div');
        div.className = `mt-4 p-4 rounded-lg text-center font-medium ${
            type === 'error' 
                ? 'bg-red-50 text-red-800 border border-red-200' 
                : 'bg-green-50 text-green-800 border border-green-200'
        }`;
        div.textContent = message;
        div.setAttribute('data-message', 'true');
        return div;
    }

    insertMessageDiv(messageDiv) {
        const form = document.querySelector('form');
        form.appendChild(messageDiv);
    }

    removeExistingMessages() {
        const existingMessages = document.querySelectorAll('[data-message="true"]');
        existingMessages.forEach(msg => msg.remove());
    }
}

// Utility functions for other pages to use
window.AuthUtils = {
    isLoggedIn: () => sessionStorage.getItem('isLoggedIn') === 'true',
    getUsername: () => sessionStorage.getItem('username'),
    logout: () => {
        sessionStorage.clear();
        window.location.href = 'index.html';
    },
    requireAuth: () => {
        if (!window.AuthUtils.isLoggedIn()) {
            window.location.href = 'index.html';
        }
    }
};

// Initialize authentication when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new AuthManager();
});

// Keyboard shortcuts for development/testing
document.addEventListener('keydown', (e) => {
    // Ctrl+Shift+D for quick login (development only)
    if (e.ctrlKey && e.shiftKey && e.key === 'D') {
        if (confirm('Quick login as admin? (Development only)')) {
            document.getElementById('username').value = 'admin';
            document.getElementById('password').value = 'admin';
        }
    }
});