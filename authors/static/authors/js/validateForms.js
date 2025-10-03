export function validateUsernameLength(username) {
    if(username.length < 4) {
        // deixar a msg tipo a do length da password
        return gettext('Please enter at least 4 characters.');
    }
    
    return true;
    
}


// validade_username_already_exists
// validate_email

// validatePasswordMatch

// | Função         | Uso                                        |
// | -------------- | ------------------------------------------ |
// | `gettext`      | Tradução simples                           |
// | `ngettext`     | Tradução plural                            |
// | `interpolate`  | Substituição de variáveis dentro da string |
// | `get_format`   | Pega formato de datas, números etc.        |
// | `gettext_noop` | Marca string para tradução posterior       |
// | `pgettext`     | Tradução com contexto                      |
// | `npgettext`    | Plural + contexto                          |
// | `pluralidx`    | Define índice do plural (interno)          |


export class PasswordValidators {
    constructor() {
        this._errors = [];
    }

    validatePasswordLength(password) {
        const passwordLength = password.length;

        if(passwordLength < 8) {
            const string = gettext(
                'Please lengthen this text to 8 characters or more (you are currently using %(passwordLength)s characters).'
            );

            const msg = interpolate(string, {passwordLength}, true);

            this._errors.push(msg);

            return msg;
        }

        return true;
    };

    validatePasswordContainsSymbols(password) {        
        // password do not have symbols
        if(/\W/.test(password) === false) {
            const msg = gettext('The password must contain symbols.');
            this._errors.push(msg);

            return msg;
        }

        return true;
    };

    validatePasswordContainsNumbers(password) {
        // password do not have numbers
        if(/\d/.test(password) === false) {
            // colocar tradução
            const msg = gettext('Password must contain numbers.');
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
