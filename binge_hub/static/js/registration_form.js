function validateForm() {
    var username = document.getElementById('id_username').value.trim();
    var email = document.getElementById('id_email').value.trim();
    var password1 = document.getElementById('id_password1').value.trim();
    var password2 = document.getElementById('id_password2').value.trim();
    var valid = true;

    // Reset all previous error messages
    resetErrorMessages();

    // Validate username length
    if (username.length < 3 || username.length > 50) {
        document.getElementById('id_username_helptext').innerText = 'Username must be between 3 and 50 characters.';
        valid = false;
    }

    // Validate email format
    var emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email)) {
        document.getElementById('id_email_helptext').innerText = 'Invalid email format.';
        valid = false;
    }

    // Validate password length and complexity
    var passwordRegex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[-_\w@$!%*?&]{8,30}$/;
    if (!passwordRegex.test(password1)) {
        document.getElementById('id_password1_helptext').innerText = 'Password must be 8-30 characters long and include at least one lowercase letter, one uppercase letter, one number, and one special character (@$!%*?&).';
        valid = false;
    }

    // Validate password confirmation
    if (password1 !== password2) {
        document.getElementById('id_password2_helptext').innerText = 'Passwords do not match.';
        valid = false;
    }

    // If all fields are valid, submit the form
    return valid;
}

function resetErrorMessages() {
    document.getElementById('id_username_helptext').innerText = '';
    document.getElementById('id_email_helptext').innerText = '';
    document.getElementById('id_password1_helptext').innerText = '';
    document.getElementById('id_password2_helptext').innerText = '';
}
