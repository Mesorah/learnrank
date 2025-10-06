import { ERRORS } from "../constants.js";
import { fetchCheckInformation } from "../getCheckInformationAPI.js";
import { sendErrors } from "./main.js";


export class EmailValidators {
    constructor() {
        this._errors = [];
    }
    
    // usar o debounce
    async validateEmailAlreadyRegistred(email) {
        const result = await fetchCheckInformation('email', email);
        const emailAlreadyRegistred = result['email_already_registred'];

        if(emailAlreadyRegistred) {
            const msg = ERRORS.EMAIL_ALREADY_TAKEN_ERROR;
            this._errors.push(msg);

            return msg;
        }

        return true;
    };

    get errors() {
        return this._errors;
    };
};


export function attachEmailListener(emailInput, errorSpan) {
    emailInput.addEventListener('input', async () => {
        const emailValidators = new EmailValidators();

        await emailValidators.validateEmailAlreadyRegistred(
            emailInput.value
        );

        sendErrors(emailValidators, errorSpan);
    })
}
