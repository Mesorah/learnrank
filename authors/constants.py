from django.utils.translation import gettext_lazy as _lazy

# Errors
DELETE_ACCOUNT_ERROR = _lazy('Incorrect confirmation. Please type "DELETE" to delete your account.')
USERNAME_MIN_LENGTH_ERROR = _lazy('Please enter at least 4 characters.')
PASSWORD1_MIN_LENGTH_ERROR = _lazy('Please enter at least 8 characters.')
PASSWORD2_MIN_LENGTH_ERROR = _lazy('Please enter at least 8 characters.')
USERNAME_TAKEN_ALREADY_ERROR = _lazy('Username is already taken.')
EMAIL_ALREADY_REGISTERED_ERROR = _lazy('Email is already registered.')
PASSWORDS_DO_NOT_MATCH_ERROR = _lazy('Passwords do not match.')
PASSWORD_MUST_CONTAIN_SYMBOLS_ERROR = _lazy('The password must contain symbols.')
PASSWORD_MUST_CONTAIN_NUMBERS_ERROR = _lazy('Password must contain numbers.')
PASSWORD_MUST_CONTAIN_LETTERS_ERROR = _lazy('Password must contain letters.')

CANNOT_ACCESS_LOGGED_ERROR = _lazy('You cannot access this while logged in.')
FORM_INVALID_ERROR = _lazy('Form invalid.')
CANNOT_ACCESS_NOT_LOGGED_ERROR = _lazy('You cannot access this while not logged in.')


# Placeholders
DELETE_ACCOUNT_PLACEHOLDER = _lazy('Type "DELETE" to permanently delete your account.')
NEW_PASSWORD1_PLACEHOLDER = _lazy('Write your new password.')
NEW_PASSWORD2_PLACEHOLDER = _lazy('Confirm your new password.')
EMAIL_PLACEHOLDER = _lazy('Write your email here.')
PASSWORD_PLACEHOLDER = _lazy('Write your password here.')
USERNAME_PLACEHOLDER = _lazy('Write your username here.')
SIGNUP_USERNAME_PLACEHOLDER = _lazy('Ex: Gabriel Rodrigues')
SIGNUP_EMAIL_PLACEHOLDER = _lazy('Ex: gabrielrodrigues@example.com')
SIGNUP_PASSWORD1_PLACEHOLDER = _lazy('Ex 23#$1fsgKDL!')
SIGNUP_PASSWORD2_PLACEHOLDER = _lazy('Repeat your password')
NEW_USERNAME_PLACEHOLDER = _lazy('Write your new username.')


# Labels
DELETE_CONFIRMATION_LABEL = _lazy('Delete confirmation')
USERNAME_LABEL = _lazy('Username')
EMAIL_LABEL = _lazy('Email')
PASSWORD1_LABEL = _lazy('Password')
PASSWORD2_LABEL = _lazy('Repeat password')
ACTUAL_USERNAME_LABEL = _lazy('Your actual username')
NEW_USERNAME_LABEL = _lazy('New username')


# SUCCESS MESSAGES
ACCOUNT_CREATED_SUCCESS = _lazy('Account created!')
ACCOUNT_LOGGED_SUCCESS = _lazy('Account logged!')
ACCOUNT_DELETED_SUCCESS = _lazy('Your account has been successfully deleted!')
PASSWORD_CHANGED_SUCCESS = _lazy('Password changed successfully!')
ACCOUNT_LOGOUT_SUCCESS = _lazy('Success, you have logged out!')


# TITLES
TITLE_SIGN_UP = _lazy('Sign Up')
TITLE_LOGIN = _lazy('Login')
TITLE_DELETE_ACCOUNT = _lazy('Delete your account')
