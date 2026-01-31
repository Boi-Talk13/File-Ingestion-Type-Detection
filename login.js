function login() {
    const username = document.getElementById("username").value.trim();
    const password = document.getElementById("password").value.trim();
    const error = document.getElementById("error");

    if (!username || !password) {
        error.textContent = "Please enter username and password";
        return;
    }

    const users = JSON.parse(localStorage.getItem("users")) || {};

    if (!users[username] || users[username] !== password) {
        error.textContent = "Invalid username or password";
        return;
    }

    localStorage.setItem("loggedIn", "true");
    localStorage.setItem("user", username);

    window.location.href = "/";
}