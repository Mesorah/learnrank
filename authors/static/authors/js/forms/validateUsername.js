import { ERRORS } from "../constants.js";
import { fetchCheckUsername } from "../getCheckUsernameAPI.js";
import { sendErrors } from "./main.js";


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
            const msg = ERRORS.USERNAME_ALREADY_TAKEN_ERROR;
            this._errors.push(msg);

            return msg;
        }

        return true;
    };

    get errors() {
        return this._errors;
    }
};

export function attachUsernameListener(usernameInput, errorSpan) {
    usernameInput.addEventListener('input', async () => {
        const usernameValidators = new UsernameValidators();

        usernameValidators.validateUsernameLength(usernameInput.value);
        await usernameValidators.validateUsernameAlreadyRegistred(usernameInput.value);

        sendErrors(usernameValidators, errorSpan);
    }) 
};
