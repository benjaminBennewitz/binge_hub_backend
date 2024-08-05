document.addEventListener('DOMContentLoaded', (event) => {

      /**
     * helper function for clearing the inputs after submit
     */
      function clearInputs(){
        userNameInput.value = '';
        emailInput.value = '';
        pass1Input.value = '';
        pass2Input.value = '';
    }

    // span elements/error messages id´s
    let usernameErr = document.getElementById('id_username_helptext');
    let emailErr = document.getElementById('id_email_helptext');
    let pass1Err = document.getElementById('id_password1_helptext');
    let pass2Err = document.getElementById('id_password2_helptext');
    let ulElements = document.getElementsByTagName('ul');

    // label id´s
    let labelUsername = document.querySelector('label[for="id_username"]');
    let labelEmail = document.querySelector('label[for="id_email"]');
    let labelPass1 = document.querySelector('label[for="id_password1"]');
    let labelPass2 = document.querySelector('label[for="id_password2"]');

    // input id´s
    let userNameInput = document.querySelector('input[id="id_username"]');
    let emailInput = document.querySelector('input[id="id_email"]');
    let pass1Input = document.querySelector('input[id="id_password1"]');
    let pass2Input = document.querySelector('input[id="id_password2"]');

    // change label default texts
    labelUsername.style.display = 'none';
    labelEmail.style.display = 'none';
    labelPass1.style.display = 'none';
    labelPass2.style.display = 'none';

    // bools for collecting the validate status
    let submitButton = document.querySelector('form button[type="submit"]');
    let un = false;
    let em = false;
    let p1 = false;
    let p2 = false;

    if (userNameInput) {
        userNameInput.placeholder = "Username*";
    }
    
    if (emailInput) {
        emailInput.placeholder = "Email*";
    }
    
    if (pass1Input) {
        pass1Input.placeholder = "Password*";
    }
    
    if (pass2Input) {
        pass2Input.placeholder = "Password confirm*";
    }

    // hide password explain texts by initializing and disable submit
    for (let ul of ulElements) {
        if (ul.querySelector('li')) {
            ul.style.display = 'none';
        }
    }

    submitButton.disabled = true;

    // Event-Handler for USERNAME
    userNameInput.addEventListener('input', function () {
        if (userNameInput.value.length >= 3 && userNameInput.value.length <= 150) {
            usernameErr.style.display = 'none';
            un = true; // Set boolean true, not string "true"
            submitBtn();
        } else {
            usernameErr.style.display = 'block';
            un = false; // Set boolean false, not string "false"
            submitBtn();
        }
    });

    // Event-Handler for EMAIL
    if (!emailErr) {
        let emailInput = document.getElementById('id_email');
        if (emailInput) {
            emailErr = document.createElement('span');
            emailErr.id = 'id_email_helptext';
            emailErr.className = 'helptext';
            emailErr.textContent = 'Please enter a valid email address (must contain @ and .)';
            emailInput.parentNode.appendChild(emailErr);
        }
    }
    emailInput.addEventListener('input', function () {
        let email = emailInput.value.trim();
        if (isValidEmail(email)) {
            emailErr.style.display = 'none';
            em = true; // Set boolean true, not string "true"
            submitBtn();
        } else {
            emailErr.style.display = 'block';
            em = false; // Set boolean false, not string "false"
            submitBtn();
        }
    });


    // Event-Handler for PASSWORD
    pass1Input.addEventListener('input', function () {
        let pass = pass1Input.value.trim();
        if (isValidPass(pass, userNameInput.value, emailInput.value)) {
            for (let ul of ulElements) {
                if (ul.querySelector('li')) {
                    ul.style.display = 'none';
                    p1 = true; // Set boolean true, not string "true"
                    submitBtn();
                }
            }
        } else {
            for (let ul of ulElements) {
                if (ul.querySelector('li')) {
                    ul.style.display = 'block';
                    p1 = false; // Set boolean false, not string "false"
                    submitBtn();
                }
            }
        }
    });

    // Event-Handler for PASSWORD CONFIRM validation
    pass2Input.addEventListener('input', function () {
        if (pass1Input.value === pass2Input.value) {
            pass2Err.style.display = 'none';
            p2 = true; // Set boolean true, not string "true"
            submitBtn();
        } else {
            pass2Err.style.display = 'block';
            p2 = false; // Set boolean false, not string "false"
            submitBtn();
        }
    });

    function submitBtn() {
        if (un && em && p1 && p2) {
            submitButton.disabled = false;
        } else {
            submitButton.disabled = true;
        }
    }

    /**
    * helper function for email validation
    * @param {*} email 
    * @returns 
    */
    function isValidEmail(email) {
        return /\S+@\S+\.\S+/.test(email);
    }

    /**
     * helper function for password validation
     * @param {string} pass
     * @param {string} username
     * @param {string} email
     * @returns {boolean}
     */
    function isValidPass(pass, username, email) {
        if (pass.includes(username) || pass.includes(email)) {
            return false;
        }

        if (pass.length < 8) {
            return false;
        }

        let commonPasswords = ['password', '123456', 'qwerty', 'test'];
        if (commonPasswords.includes(pass.toLowerCase())) {
            return false;
        }

        if (!isNaN(pass)) {
            return false;
        }
        return true;
    }
});