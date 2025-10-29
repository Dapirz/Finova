// Utility functions

function getToken() {
    return localStorage.getItem('token');
}

function checkAuth() {
    const token = getToken();
    if (!token) {
        window.location.href = 'login.html';
        return false;
    }
    return true;
}

function logout() {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    window.location.href = 'login.html';
}

function formatCurrency(amount) {
    return new Intl.NumberFormat('id-ID', {
        style: 'currency',
        currency: 'IDR',
        minimumFractionDigits: 0
    }).format(amount);
}

function showError(message) {
    alert('Error: ' + message);
}

function showSuccess(message) {
    alert('Sukses: ' + message);
}

// Display user name in navbar
function displayUserName() {
    const user = JSON.parse(localStorage.getItem('user'));
    if (user) {
        const userNameElement = document.getElementById('userName');
        if (userNameElement) {
            userNameElement.textContent = user.nama_lengkap;
        }
    }
}

// Call this on page load for authenticated pages
if (window.location.pathname !== '/login.html') {
    window.addEventListener('DOMContentLoaded', displayUserName);
}