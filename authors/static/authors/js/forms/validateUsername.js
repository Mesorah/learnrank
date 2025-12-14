import { ERRORS } from "../constants.js";
import { fetchCheckInformation } from "../getCheckInformationAPI.js";
import { sendErrors } from "./main.js";


export class UsernameValidators {
    constructor() {
        this._errors = [];
    }

    validateUsernameLength(username) {
        const usernameLength = username.length;

        if(usernameLength <= 3) {
            const string = ERRORS.USERNAME_MIN_LENGTH_ERROR(usernameLength);
            const msg = interpolate(string, {usernameLength}, true);

            this._errors.push(msg);

            return msg;
        }
        
        return true;
    };

    // usar o debounce
    async validateUsernameAlreadyRegistred(username) {
        const result = await fetchCheckInformation('username', username);
        const usernameAlreadyRegistred = result['username_already_registred'];

        if(usernameAlreadyRegistred) {
            const msg = ERRORS.USERNAME_ALREADY_TAKEN_ERROR;
            this._errors.push(msg);

            return msg;
        }

        return true;
    };

    get errors() {
        return this._errors;
    };
};

export function attachUsernameListener(usernameInput) {
    usernameInput.addEventListener('input', async () => {
        const usernameValidators = new UsernameValidators();

        usernameValidators.validateUsernameLength(usernameInput.value);
        await usernameValidators.validateUsernameAlreadyRegistred(usernameInput.value);

        sendErrors(usernameValidators, usernameInput.parentElement);
    }) 
};
