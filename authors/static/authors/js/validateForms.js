export function validateUsernameLength(username) {
    if(username.length <= 3) {
        return 'Please enter at least 4 characters.';
    }
    
    return true;
    
}


function attachUsernameListener(usernameInput, form, errorSpan) {
    usernameInput.addEventListener('input', () => {
        const validation = validateUsernameLength(usernameInput.value);

        form.appendChild(errorSpan);

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

    return {form, usernameInput};
}


function createErrorSpan() {
    const errorSpan = document.createElement('span');
    errorSpan.classList.add('error-span');

    return errorSpan;
}


export function main() {
    const {form, usernameInput} = getElements();
    const errorSpan = createErrorSpan();

    attachUsernameListener(usernameInput, form, errorSpan);
}
