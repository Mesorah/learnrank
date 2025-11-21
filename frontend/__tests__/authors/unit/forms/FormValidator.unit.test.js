import { ERRORS } from '@js/constants.js';
import { PasswordValidators } from '@js/forms/validatePassword.js';
import { UsernameValidators } from '@js/forms/validateUsername.js';


describe('Test Username form validations', () => {
    let usernameValidators;

    beforeEach(() => {
        usernameValidators = new UsernameValidators();
    })

    test('username length validator message success', () => {
        expect(usernameValidators.validateUsernameLength('abcd')).toBe(true);
    });

    test('username length validator message error', () => {
        expect(usernameValidators.validateUsernameLength('abc')).toBe(
            ERRORS.USERNAME_MIN_LENGTH_ERROR(3)
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
                ERRORS.PASSWORD1_MIN_LENGTH_ERROR(7)
            );
        });

        test('should show valiidator error message different length of characters', () => {
            expect(
                passwordValidators.validatePasswordLength(
                'abc12@'
            )).toBe(
                ERRORS.PASSWORD1_MIN_LENGTH_ERROR(6)
            );
        });
    });

    describe('password contains letters', () => {
            test('should show validator success', () => {
                expect(
                    passwordValidators.validatePasswordContainsLetters('ab12!')
                ).toBe(true);
        });

        test('should show validator error message', () => {
            expect(
                passwordValidators.validatePasswordContainsLetters('1212!')
            ).toBe(
                ERRORS.PASSWORD_MUST_CONTAIN_LETTERS_ERROR
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
                ERRORS.PASSWORD_MUST_CONTAIN_SYMBOLS_ERROR
            );
        });
    });

    describe('password contains numbers', () => {
        test('should show validator success', () => {
            expect(passwordValidators.validatePasswordContainsNumbers('ab12!')).toBe(true);
        });

        test('should snow validator error message', () => {
            expect(passwordValidators.validatePasswordContainsNumbers('abc!')).toBe(
                ERRORS.PASSWORD_MUST_CONTAIN_NUMBERS_ERROR
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
            )).toBe(ERRORS.PASSWORDS_DO_NOT_MATCH_ERROR);
        });

        test('should not show symbols, number and length errors', () => {
            expect(passwordValidators.validatePasswordsMatch(
                'abcde1234!@', 'abc'
            )).toBe(ERRORS.PASSWORDS_DO_NOT_MATCH_ERROR);
        });
    });
});
