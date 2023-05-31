const loginBtn = document.getElementById('login-btn');

function updateLoginBtn(isAuthenticated, id) {
    if (isAuthenticated) {
        loginBtn.innerHTML = 'Profile';
        loginBtn.href = '/dashboard/user/' + id;
    } else {
        loginBtn.innerHTML = 'Login';
        loginBtn.href = '/';
    }
}