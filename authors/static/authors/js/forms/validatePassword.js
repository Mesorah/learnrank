import { ERRORS } from "../constants.js";
import { sendErrors } from "./main.js";


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


export function attachPasswordListener(password1Input, password2Input, errorSpan) {
    password1Input.addEventListener('input', () => {
        validatePassword(password1Input, password2Input, errorSpan);
    })

    password2Input.addEventListener('input', () => {
        validatePassword(password1Input, password2Input, errorSpan);
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
