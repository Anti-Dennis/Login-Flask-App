// password-validation.js
function validatePasswordRequirements() {
    const passwordInput = document.getElementById('register-password');
    const strengthBar = document.getElementById('strength-bar');
    const requirements = [
        { regex: /.{8,}/, elementId: 'length' },
        { regex: /\d/, elementId: 'number' },
        { regex: /[a-z]/, elementId: 'lowercase' },
        { regex: /[A-Z]/, elementId: 'uppercase' },
        { regex: /[!@#$%^&*(),.?":{}|<>]/, elementId: 'special' }
    ];
    
    passwordInput.addEventListener('input', () => {
        let strength = 0;
        requirements.forEach(requirement => {
            const requirementElement = document.getElementById(requirement.elementId);
            if (requirement.regex.test(passwordInput.value)) {
                requirementElement.classList.add('valid');
                requirementElement.classList.remove('invalid');
                strength += 1;
            } else {
                requirementElement.classList.add('invalid');
                requirementElement.classList.remove('valid');
            }
        });

        // Update the strength bar based on the number of criteria met
        const strengthPercentage = (strength / requirements.length) * 100;
        strengthBar.style.width = strengthPercentage + '%';

        if (strengthPercentage <= 40) {
            strengthBar.className = 'strength-weak';
        } else if (strengthPercentage <= 80) {
            strengthBar.className = 'strength-medium';
        } else {
            strengthBar.className = 'strength-strong';
        }
    });
}

window.onload = validatePasswordRequirements;
