document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("signupForm");
    const email = document.getElementById("email");
    const username = document.getElementById("username");
    const useEmail = document.getElementById("useEmail");
    const password = document.getElementById("password");
    const confirmPassword = document.getElementById("confirmPassword");
    const msg = document.getElementById("formMessage");

    // Use email prefix as username
    useEmail.addEventListener("change", () => {
        if (useEmail.checked && email.value.includes("@")) {
            username.value = email.value.split("@")[0];
            username.disabled = true;
        } else {
            username.disabled = false;
            username.value = "";
        }
    });

    email.addEventListener("input", () => {
        if (useEmail.checked && email.value.includes("@")) {
            username.value = email.value.split("@")[0];
        }
    });

    form.addEventListener("submit", (e) => {
        e.preventDefault();
        msg.textContent = "";
        msg.className = "";

        if (!email.value.endsWith("@gmail.com")) {
            showError("Email must end with @gmail.com");
            return;
        }

        if (!password.value || !confirmPassword.value) {
            showError("Password fields cannot be empty");
            return;
        }

        if (password.value !== confirmPassword.value) {
            showError("Password and Confirm Password must match");
            return;
        }

        // ✅ NO ALERT
        // ✅ DIRECT REDIRECT
        window.location.href = "/login.html";
    });

    function showError(text) {
        msg.textContent = text;
        msg.className = "error";
    }
});