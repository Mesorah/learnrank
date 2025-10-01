/**
 * @jest-environment jsdom
 */

import { main, validateUsernameLength } from '@js/validateForms';

describe('Test input form validations', () => {
    const formClass = 'author-form';
    const usernameInputID = 'id_username';
    const errorSpanClass = 'error-span';

    let form;
    let usernameInput;

    beforeEach(() => {
        document.body.innerHTML = `
        <form class="author-form">
            <input type="text" id="${usernameInputID}" placeholder="Ex: Gabriel Rodrigues">
            <input type="email" id="id_email" placeholder="Ex: gabrielrodrigues@example.com">
            <input type="password" id="id_password1" placeholder="Ex 23#$1fsgKDL!">
            <input type="password" id="id_password2" placeholder="Repeat your password">
            <button type="submit">Submit</button>
        </form>
        `;

        form = document.querySelector(`.${formClass}`);
        usernameInput = form.querySelector(`#${usernameInputID}`);

        main();
    });

    test('username length validator message', () => {
        expect(validateUsernameLength('abc')).toBe(
            'Please enter at least 4 characters.'
        );
        expect(validateUsernameLength('abcd')).toBe(true);
    });

    test('displays error message when username is too short', () => {
        usernameInput.value = 'abc';
        usernameInput.dispatchEvent(new Event('input'));

        const errorSpan = document.querySelector(`.${errorSpanClass}`);
        expect(errorSpan).not.toBeNull();
        expect(errorSpan.textContent).toBe('Please enter at least 4 characters.');
    })

    test('not displays error message', () => {
        usernameInput.value = 'abcd';
        usernameInput.dispatchEvent(new Event('input'));

        const errorSpan = document.querySelector(`.${errorSpanClass}`);
        expect(errorSpan).not.toBeNull();
        expect(errorSpan.textContent).toBe('');
    })
});