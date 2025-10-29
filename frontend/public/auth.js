// Login functionality

const loginForm = document.getElementById('loginForm');
const errorMessage = document.getElementById('errorMessage');

loginForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    
    try {
        const response = await fetch(`${API_BASE_URL}/auth/login`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ username, password })
        });
        
        const data = await response.json();
        
        if (data.success) {
            // Save token and user info
            localStorage.setItem('token', data.token);
            localStorage.setItem('user', JSON.stringify(data.user));
            
            // Redirect to dashboard
            window.location.href = 'index.html';
        } else {
            errorMessage.textContent = data.message;
            errorMessage.classList.add('show');
        }
    } catch (error) {
        console.error('Login error:', error);
        errorMessage.textContent = 'Terjadi kesalahan saat login. Silakan coba lagi.';
        errorMessage.classList.add('show');
    }
});