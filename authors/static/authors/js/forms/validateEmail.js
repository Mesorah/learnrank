import { ERRORS } from "../constants.js";
import { fetchCheckEmail } from "../getCheckEmailAPI.js";
import { sendErrors } from "./main.js";

// validate email has @ .
export async function validateEmailAlreadyRegistred(email) {
    const result = await fetchCheckEmail(email);
    const emailAlreadyRegistred = result['email_already_registred'];

    if(emailAlreadyRegistred) {
        return ERRORS.EMAIL_ALREADY_TAKEN_ERROR;
    }

    return true;
};


export function attachEmailListener(emailInput, errorSpan) {
    emailInput.addEventListener('input', async () => {
        const msg = await validateEmailAlreadyRegistred(emailInput.value);

        sendErrors(msg, errorSpan);
    })
}
