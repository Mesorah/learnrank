import { PasswordValidators, validateUsernameLength } from '@js/validateForms';


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
    let passwordValidators;

    beforeEach(() => {
        passwordValidators = new PasswordValidators();
    })
    
    describe('password contains symbols', () => {
            test('should show validator success message', () => {
                expect(
                    passwordValidators.validatePasswordContainsSymbols('ab12!')
                ).toBe(true);
        });

        test('should show validator error message', () => {
            expect(
                passwordValidators.validatePasswordContainsSymbols('ab12')
            ).toBe(
                'The password must contain symbols.'
            );
        });
    });

    describe('password contains numbers', () => {
        test('should show validator success message', () => {
            expect(passwordValidators.validatePasswordContainsNumbers('ab12!')).toBe(true);
        });

        test('should snow validator error message', () => {
            expect(passwordValidators.validatePasswordContainsNumbers('abc!')).toBe(
                'Password must contain numbers.'
            );
        });
    });
});
