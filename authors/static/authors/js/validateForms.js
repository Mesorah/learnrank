export function validateUsernameLength(username) {
    if(username.length <= 3) {
        // colocar tradução
        return 'Please enter at least 4 characters.';
    }
    
    return true;
    
}

// validade_username_already_exists
// validate_email

export function validatePasswordHasSymbols(password) {
    if(password.length <= 0) return true;
    
    // password do not have symbols
    if(/\W/.test(password) === false) {
        // colocar tradução
        return 'The password must contain symbols.';
    }

    return true;
}

function attachPasswordListener(passwordInput, form, errorSpan) {
    passwordInput.addEventListener('input', () => {
        const validation = validatePasswordHasSymbols(passwordInput.value);

        if(validation !== true) {
            errorSpan.textContent = validation;
        } else {
            errorSpan.textContent = '';
        }

    })
}

function attachUsernameListener(usernameInput, form, errorSpan) {
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

    attachUsernameListener(usernameInput, form, errorSpan);
    attachPasswordListener(passwordInput, form, errorSpan);
}
