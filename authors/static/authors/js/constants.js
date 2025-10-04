export const ERRORS = {
    USERNAME_MIN_LENGTH_ERROR: (usernameLength) => gettext('Please enter at least 4 characters (you are currently using %(usernameLength)s characters).').replace('%(usernameLength)s', usernameLength),
    PASSWORD1_MIN_LENGTH_ERROR: (passwordLength) => gettext('Please lengthen this text to 8 characters or more (you are currently using %(passwordLength)s characters).').replace('%(passwordLength)s', passwordLength),
    PASSWORD_MUST_CONTAIN_SYMBOLS_ERROR: gettext('The password must contain symbols.'),
    PASSWORD_MUST_CONTAIN_NUMBERS_ERROR: gettext('Password must contain numbers.'),
    PASSWORDS_DO_NOT_MATCH_ERROR: gettext('Passwords do not match.'),
    USERNAME_TAKEN_ALREADY_ERROR: gettext('Username is already taken.'),
};
