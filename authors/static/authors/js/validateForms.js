export function validateUsernameLength(username) {
    if(username.length <= 3) {
        // colocar tradução
        return 'Please enter at least 4 characters.';
    }
    
    return true;
    
}


// validade_username_already_exists
// validate_email

// validatePasswordMatch

export class PasswordValidators {
    constructor() {
        this._errors = [];
    }

    validatePasswordLength(password) {
        const passwordLength = password.length;

        if(passwordLength < 8) {
            // colocar tradução
            const msg = `Please lengthen this text to 8 characters or more (you are currently using ${passwordLength} characters).`;
            this._errors.push(msg);

            return msg;
        }

        return true;
    };

    validatePasswordContainsSymbols(password) {        
        // password do not have symbols
        if(/\W/.test(password) === false) {
            // colocar tradução
            const msg = 'The password must contain symbols.';
            this._errors.push(msg);

            return msg;
        }

        return true;
    };

    validatePasswordContainsNumbers(password) {
        // password do not have numbers
        if(/\d/.test(password) === false) {
            // colocar tradução
            const msg = 'Password must contain numbers.';
            this._errors.push(msg);

            return msg;
        }

        return true;
    };

    get errors() {
        return this._errors;
    }
};


function attachPasswordListener(passwordInput, errorSpan) {
    passwordInput.addEventListener('input', () => {
        const passwordValidators = new PasswordValidators();

        passwordValidators.validatePasswordLength(passwordInput.value);
        passwordValidators.validatePasswordContainsSymbols(passwordInput.value);
        passwordValidators.validatePasswordContainsNumbers(passwordInput.value);

        const errors = passwordValidators.errors;

        errorSpan.textContent = '';
        for(let error of errors) {
            errorSpan.textContent += error;
        }
    })
}


function attachUsernameListener(usernameInput, errorSpan) {
    usernameInput.addEventListener('input', () => {
        const validation = validateUsernameLength(usernameInput.value);

        if(validation !== true) {
            errorSpan.textContent = validation;
        } else {
            errorSpan.textContent = '';
        }
    }) 
}


function getElements() {
    const form = document.querySelector('.author-form');
    const usernameInput = form.querySelector('#id_username');
    const passwordInput = form.querySelector('#id_password1');

    return {form, usernameInput, passwordInput};
}


function createErrorSpan(form) {
    const errorSpan = document.createElement('span');
    errorSpan.classList.add('error-span');

    form.appendChild(errorSpan);

    return errorSpan;
}


export function main() {
    const {form, usernameInput, passwordInput} = getElements();
    const errorSpan = createErrorSpan(form);

    attachUsernameListener(usernameInput, errorSpan);
    attachPasswordListener(passwordInput, errorSpan);
}
