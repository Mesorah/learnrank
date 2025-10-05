import { attachEmailListener } from './validateEmail.js';
import { attachPasswordListener } from './validatePassword.js';
import { attachUsernameListener } from './validateUsername.js';


export function sendErrors(validators, errorSpan) {
    const errors = validators.errors;

    errorSpan.textContent = '';
    for(let error of errors) {
        errorSpan.textContent += error;
    }
};


export function getElements() {
    const form = document.querySelector('.author-form');
    const usernameInput = form.querySelector('#id_username');
    const emailInput = form.querySelector('#id_email');
    const password1Input = form.querySelector('#id_password1');
    const password2Input = form.querySelector('#id_password2');

    return {form, usernameInput, emailInput, password1Input, password2Input};
};


export function createErrorSpan(form) {
    const errorSpan = document.createElement('span');
    errorSpan.classList.add('error-span');

    form.appendChild(errorSpan);

    return errorSpan;
};


export function inicializeListener() {
    const {form, usernameInput, emailInput, password1Input, password2Input} = getElements();
    const errorSpan = createErrorSpan(form);

    attachUsernameListener(usernameInput, errorSpan);
    attachPasswordListener(password1Input, password2Input, errorSpan);
    attachEmailListener(emailInput, errorSpan);
};
