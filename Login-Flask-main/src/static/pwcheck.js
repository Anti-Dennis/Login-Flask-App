let parameters = {
    count: false,
    letters: false,
    numbers: false,
    special: false
};

let strengthBar = document.getElementById("strength-bar");
let msg = document.getElementById("msg");

function strengthChecker() {
    let password = document.getElementById("register-password").value; // Use 'register-password' here

    // Check each requirement
    parameters.letters = /[A-Za-z]+/.test(password);
    parameters.numbers = /\d+/.test(password);
    parameters.special = /[!\"$%&/()=?@~\\.\';:+=^*_-]+/.test(password);
    parameters.count = password.length >= 8;

    // Calculate strength based on fulfilled criteria
    let strength = Object.values(parameters).filter(value => value).length;

    // Update strength bar
    let strengthPercentage = (strength / 4) * 100; // 4 represents the number of conditions (letters, numbers, special, length)
    strengthBar.style.width = strengthPercentage + "%";

    // Set color and message based on strength level
    if (strength <= 1) {
        strengthBar.style.backgroundColor = "#ff3e36"; // Red
        msg.textContent = "Your password is very weak";
    } else if (strength === 2) {
        strengthBar.style.backgroundColor = "#ff691f"; // Orange
        msg.textContent = "Your password is weak";
    } else if (strength === 3) {
        strengthBar.style.backgroundColor = "#ffda36"; // Yellow
        msg.textContent = "Your password is good";
    } else if (strength === 4) {
        strengthBar.style.backgroundColor = "#0be881"; // Green
        msg.textContent = "Your password is strong";
    }
}

document.getElementById("register-password").addEventListener("input", strengthChecker); // Listen for password input
