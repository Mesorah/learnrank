import { attachEmailListener } from './validateEmail.js';
import { attachPasswordListener } from './validatePassword.js';
import { attachUsernameListener } from './validateUsername.js';


export function sendErrors(validators, form_p) {
    const errorSpan = createErrorSpan(form_p);

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


export function createErrorSpan(form_p) {
    const error_span = form_p.querySelector('.error-span');

    if(error_span) return error_span;

    const errorSpan = document.createElement('span');
    errorSpan.classList.add('error-span');

    form_p.appendChild(errorSpan);

    return errorSpan;
};


export function inicializeListener() {
    const {form, usernameInput, emailInput, password1Input, password2Input} = getElements();
    // const errorSpan = createErrorSpan(form);

    attachUsernameListener(usernameInput);
    attachPasswordListener(password1Input, password2Input);
    attachEmailListener(emailInput);
};
