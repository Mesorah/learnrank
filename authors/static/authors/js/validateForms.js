import { ERRORS } from "./constants.js";
import { fetchCheckUsername } from "./getCheckUsernameAPI.js";


export class UsernameValidators {
    constructor() {
        this._errors = [];
    }

    validateUsernameLength(username) {
        const usernameLength = username.length;

        if(usernameLength < 4) {
            const string = ERRORS.USERNAME_MIN_LENGTH_ERROR(usernameLength);
            
            const msg = interpolate(string, {usernameLength}, true);

            this._errors.push(msg);

            return msg;
        }
        
        return true;
    };

    async validateUsernameAlreadyRegistred(username) {
        const result = await fetchCheckUsername(username);
        const usernameAlreadyRegistred = result['username_already_registred'];

        if(usernameAlreadyRegistred) {
            const msg = ERRORS.USERNAME_TAKEN_ALREADY_ERROR;
            this._errors.push(msg);

            return msg;
        }

        return true;
    };

    get errors() {
        return this._errors;
    }
};


// validate_email


export class PasswordValidators {
    constructor() {
        this._errors = [];
    }

    validatePasswordLength(password) {
        const passwordLength = password.length;

        if(passwordLength < 8) {
            const string = ERRORS.PASSWORD1_MIN_LENGTH_ERROR(passwordLength);

            const msg = interpolate(string, {passwordLength}, true);

            this._errors.push(msg);

            return msg;
        }

        return true;
    };

    validatePasswordContainsSymbols(password) {        
        // password do not have symbols
        if(/\W/.test(password) === false) {
            const msg = ERRORS.PASSWORD_MUST_CONTAIN_SYMBOLS_ERROR;
            this._errors.push(msg);

            return msg;
        }

        return true;
    };

    validatePasswordContainsNumbers(password) {
        // password do not have numbers
        if(/\d/.test(password) === false) {
            const msg = ERRORS.PASSWORD_MUST_CONTAIN_NUMBERS_ERROR;
            this._errors.push(msg);

            return msg;
        }

        return true;
    };

    validatePasswordsMatch(password1, password2) {
        // password.length start validate if passwords.length is > 0
        if(password1.length === 0 || password2.length === 0) return;

        if(password1 !== password2) {
            const msg = ERRORS.PASSWORDS_DO_NOT_MATCH_ERROR;
            this._errors.push(msg);

            return msg;
        }

        return true;
    };

    get errors() {
        return this._errors;
    }
};

function sendErrors(passwordValidators, errorSpan) {
    const errors = passwordValidators.errors;

    errorSpan.textContent = '';
    for(let error of errors) {
        errorSpan.textContent += error;
    }
};

function attachUsernameListener(usernameInput, errorSpan) {
    usernameInput.addEventListener('input', async () => {
        const usernameValidators = new UsernameValidators();

        usernameValidators.validateUsernameLength(usernameInput.value);
        const msg = await usernameValidators.validateUsernameAlreadyRegistred(usernameInput.value);

        const errors = usernameValidators.errors;

        errorSpan.textContent = '';
        for(let error of errors) {
            errorSpan.textContent += error;
        }
    }) 
};

function validatePassword(password1Input, password2Input, errorSpan) {
    const passwordValidators = new PasswordValidators();

    passwordValidators.validatePasswordLength(password1Input.value);
    passwordValidators.validatePasswordContainsSymbols(password1Input.value);
    passwordValidators.validatePasswordContainsNumbers(password1Input.value);
    passwordValidators.validatePasswordsMatch(password1Input.value, password2Input.value);

    sendErrors(passwordValidators, errorSpan);
}


function attachPasswordListener(password1Input, password2Input, errorSpan) {
    password1Input.addEventListener('input', () => {
        validatePassword(password1Input, password2Input, errorSpan);
    })

    password2Input.addEventListener('input', () => {
        validatePassword(password1Input, password2Input, errorSpan);
    })
};


function getElements() {
    const form = document.querySelector('.author-form');
    const usernameInput = form.querySelector('#id_username');
    const password1Input = form.querySelector('#id_password1');
    const password2Input = form.querySelector('#id_password2');

    return {form, usernameInput, password1Input, password2Input};
};


function createErrorSpan(form) {
    const errorSpan = document.createElement('span');
    errorSpan.classList.add('error-span');

    form.appendChild(errorSpan);

    return errorSpan;
};


export function main() {
    const {form, usernameInput, password1Input, password2Input} = getElements();
    const errorSpan = createErrorSpan(form);

    attachUsernameListener(usernameInput, errorSpan);
    attachPasswordListener(password1Input, password2Input, errorSpan);
};
