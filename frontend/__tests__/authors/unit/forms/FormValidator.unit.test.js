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

    describe('password length validor', () => {
        test('should show valiidator success message', () => {
            expect(
                passwordValidators.validatePasswordLength('abcd12!@')
            ).toBe(true);
        });

        test('should show valiidator error message', () => {
            expect(
                passwordValidators.validatePasswordLength(
                    'abc12!@'
                )).toBe(
                'Please lengthen this text to 8 characters or more (you are currently using 7 characters).'
            );
        });

        test('should show valiidator error message different length of characters', () => {
            expect(
                passwordValidators.validatePasswordLength(
                'abc12@'
            )).toBe(
                'Please lengthen this text to 8 characters or more (you are currently using 6 characters).'
            );
        });
    });
    
    describe('password contains symbols', () => {
            test('should show validator success', () => {
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
        test('should show validator success', () => {
            expect(passwordValidators.validatePasswordContainsNumbers('ab12!')).toBe(true);
        });

        test('should snow validator error message', () => {
            expect(passwordValidators.validatePasswordContainsNumbers('abc!')).toBe(
                'Password must contain numbers.'
            );
        });
    });

    describe('password match', () => {
        test('should show validator success', () => {
            expect(passwordValidators.validatePasswordsMatch(
                'abcde1234!@', 'abcde1234!@'
            )).toBe(true);
        });

        test('should show validator error message', () => {
            expect(passwordValidators.validatePasswordsMatch(
                'abcde1234!@', 'abcde123!@'
            )).toBe('Passwords do not match.');
        });

        test('should not show symbols, number and length errors', () => {
            expect(passwordValidators.validatePasswordsMatch(
                'abcde1234!@', 'abc'
            )).toBe('Passwords do not match.');
        });
    });
});
