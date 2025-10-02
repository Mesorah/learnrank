/**
 * @jest-environment jsdom
 */

import { validatePasswordHasSymbols, validateUsernameLength } from '@js/validateForms';


describe('Test Username form validations', () => {
    test('username length validator message success', () => {
        expect(validateUsernameLength('abcd')).toBe(true);
    });

    test('username length validator message error', () => {
        expect(validateUsernameLength('abc')).toBe(
            'Please enter at least 4 characters.'
        );
    });
});


describe('Test Password form validations', () => {
    test('password symbols validator message success', () => {
        expect(validatePasswordHasSymbols('ab12!')).toBe(true);
    });

    test('password symbols validator message error', () => {
        expect(validatePasswordHasSymbols('ab12')).toBe(
            'The password must contain symbols.'
        );
    });
})
