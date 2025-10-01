/**
 * @jest-environment jsdom
 */

import { main, validatePasswordHasSymbols, validateUsernameLength } from '@js/validateForms';


const FORM_CLASS = 'author-form';
const USERNAME_INPUT_ID = 'id_username';
const PASSWORD1_INPUT_ID = 'id_password1';
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

    main();

    return {
        usernameInput, password1Input
    };
}

function getErrorSpan() {
    return document.querySelector(`.${ERROR_SPAN_CLASS}`);
}


describe('Test Username input form validations', () => {
    let usernameInput;

    beforeEach(() => {
        ({ usernameInput } = setupFormTest());
    });

    test('username length validator message success', () => {
        expect(validateUsernameLength('abcd')).toBe(true);
    });

    test('username length validator message error', () => {
        expect(validateUsernameLength('abc')).toBe(
            'Please enter at least 4 characters.'
        );
    });

    test('displays error message when username is too short', () => {
        usernameInput.value = 'abc';
        usernameInput.dispatchEvent(new Event('input'));

        const errorSpan = getErrorSpan();
        expect(errorSpan).not.toBeNull();
        expect(errorSpan.textContent).toBe('Please enter at least 4 characters.');
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

    beforeEach(() => {
        ({ password1Input } = setupFormTest());
    });

    test('password symbols validator message success', () => {
        expect(validatePasswordHasSymbols('ab12!')).toBe(true);
    });

    test('password symbols validator message error', () => {
        expect(validatePasswordHasSymbols('ab12')).toBe(
            'The password must contain symbols.'
        );
    });

    test('password no has symbols show error', () => {
        password1Input.value = '123456ab';
        password1Input.dispatchEvent(new Event('input'));

        const errorSpan = getErrorSpan();
        expect(errorSpan).not.toBeNull();
        expect(errorSpan.textContent).toBe('The password must contain symbols.');
    });

    test('password has symbols do not show error', () => {
        password1Input.value = '123456a!';
        password1Input.dispatchEvent(new Event('input'));

        const errorSpan = getErrorSpan();
        expect(errorSpan).not.toBeNull();
        expect(errorSpan.textContent).toBe('');
    });
})