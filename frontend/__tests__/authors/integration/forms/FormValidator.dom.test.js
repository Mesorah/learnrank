/**
 * @jest-environment jsdom
*/

import { ERRORS } from '@js/constants.js';
import { inicializeListener } from '@js/forms/main.js';
import { UsernameValidators } from '@js/forms/validateUsername.js';


const FORM_CLASS = 'author-form';
const USERNAME_INPUT_ID = 'id_username';
const PASSWORD1_INPUT_ID = 'id_password1';
const PASSWORD2_INPUT_ID = 'id_password2';
const ERROR_SPAN_CLASS = 'error-span';


function setupFormTest() {
    document.body.innerHTML = `
        <form class="author-form">
            <input type="text" id="${USERNAME_INPUT_ID}" placeholder="Ex: Gabriel Rodrigues">
            <input type="email" id="id_email" placeholder="Ex: gabrielrodrigues@example.com">
            <input type="password" id="id_password1" placeholder="Ex 23#$1fsgKDL!">
            <input type="password" id="id_password2" placeholder="Repeat your password">
            <button type="submit">Submit</button>
        </form>
    `;

    const form = document.querySelector(`.${FORM_CLASS}`);
    const usernameInput = form.querySelector(`#${USERNAME_INPUT_ID}`);
    const password1Input = form.querySelector(`#${PASSWORD1_INPUT_ID}`);
    const password2Input = form.querySelector(`#${PASSWORD2_INPUT_ID}`);

    inicializeListener();

    return {
        usernameInput, password1Input, password2Input
    };
}


function getErrorSpan() {
    return document.querySelector(`.${ERROR_SPAN_CLASS}`);
}


describe('Test Username input form validations', () => {
    let usernameInput;

    beforeEach(() => {
        ({ usernameInput } = setupFormTest());

        // doing this to nullify the function
        UsernameValidators.prototype.validateUsernameAlreadyRegistred = () => false;
    });

    test('displays error message when username is too short', async() => {
        usernameInput.value = 'abc';
        usernameInput.dispatchEvent(new Event('input'));

        const errorSpan = getErrorSpan();

        await new Promise(process.nextTick);

        expect(errorSpan).not.toBeNull();
        expect(errorSpan.textContent).toBe(ERRORS.USERNAME_MIN_LENGTH_ERROR(3));
    })

    test('not displays error message', () => {
        usernameInput.value = 'abcd';
        usernameInput.dispatchEvent(new Event('input'));

        const errorSpan = getErrorSpan();
        expect(errorSpan).not.toBeNull();
        expect(errorSpan.textContent).toBe('');
    })
});


describe('Test Password input form validations', () => {
    let password1Input;
    let password2Input;

    beforeEach(() => {
        ({ password1Input, password2Input } = setupFormTest());

        // doing this to nullify the function
        UsernameValidators.prototype.validateUsernameAlreadyRegistred = () => false;
    });

    describe('password length validor', () => {
        test('should show valiidator error message', () => {
            password1Input.value = 'abc12!@';
            password1Input.dispatchEvent(new Event('input'));

            const errorSpan = getErrorSpan();
            expect(errorSpan).not.toBeNull();
            expect(errorSpan.textContent).toBe(ERRORS.PASSWORD1_MIN_LENGTH_ERROR(7));
        });

        test('should show valiidator success message', () => {
            password1Input.value = 'abcd12!@';
            password1Input.dispatchEvent(new Event('input'));

            const errorSpan = getErrorSpan();
            expect(errorSpan).not.toBeNull();
            expect(errorSpan.textContent).toBe('');
        });
    });

    describe('password contains symbols', () => {
        test('should show validator error message', () => {
            password1Input.value = '123456ab';
            password1Input.dispatchEvent(new Event('input'));

            const errorSpan = getErrorSpan();
            expect(errorSpan).not.toBeNull();
            expect(errorSpan.textContent).toBe(ERRORS.PASSWORD_MUST_CONTAIN_SYMBOLS_ERROR);
        });

        test('should show validator success message', () => {
            password1Input.value = '123456a!';
            password1Input.dispatchEvent(new Event('input'));

            const errorSpan = getErrorSpan();
            expect(errorSpan).not.toBeNull();
            expect(errorSpan.textContent).toBe('');
        });
    });

    describe('password contains numbers', () => {
        test('should show validator error message', () => {
            password1Input.value = 'abcde!@#';
            password1Input.dispatchEvent(new Event('input'));

            const errorSpan = getErrorSpan();
            expect(errorSpan).not.toBeNull();
            expect(errorSpan.textContent).toBe(ERRORS.PASSWORD_MUST_CONTAIN_NUMBERS_ERROR);
        });

        test('should show validator sucess message', () => {
            password1Input.value = 'abcd1234!';
            password1Input.dispatchEvent(new Event('input'));

            const errorSpan = getErrorSpan();
            expect(errorSpan).not.toBeNull();
            expect(errorSpan.textContent).toBe('');
        });
    });

    describe('password match', () => {
        test('should show validator success', () => {
            password1Input.value = 'abcde1234!@';
            password2Input.value = 'abcde1234!@';

            password1Input.dispatchEvent(new Event('input'));

            const errorSpan = getErrorSpan();
            expect(errorSpan).not.toBeNull();
            expect(errorSpan.textContent).toBe('');
        });

        test('should show validator error message', () => {
            password1Input.value = 'abcde1234!@';
            password2Input.value = 'abcde123!@';

            password1Input.dispatchEvent(new Event('input'));

            const errorSpan = getErrorSpan();
            expect(errorSpan).not.toBeNull();
            expect(errorSpan.textContent).toBe(ERRORS.PASSWORDS_DO_NOT_MATCH_ERROR);
        });

        test('should not show symbols, number and length errors', () => {
            password1Input.value = 'abcde1234!@';
            password2Input.value = 'abc';

            password2Input.dispatchEvent(new Event('input'));

            const errorSpan = getErrorSpan();
            expect(errorSpan).not.toBeNull();
            expect(errorSpan.textContent).toBe(ERRORS.PASSWORDS_DO_NOT_MATCH_ERROR);
        });
    });
})
