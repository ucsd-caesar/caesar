const loginBtn = document.getElementById('login-btn');

function updateLoginBtn(isAuthenticated, id) {
    if (isAuthenticated) {
        loginBtn.innerHTML = 'Profile';
        loginBtn.addEventListener('click', () => {
            window.location.href = '/dashboard/user/' + id;
        });
    } else {
        loginBtn.innerHTML = 'Login';
        loginBtn.addEventListener('click', () => {
            window.location.href = '/dashboard/login';
        });
    }
}