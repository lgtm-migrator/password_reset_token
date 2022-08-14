# password_reset_token

[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/vremes/password_reset_token.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/vremes/password_reset_token/context:python)
[![Total alerts](https://img.shields.io/lgtm/alerts/g/vremes/password_reset_token.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/vremes/password_reset_token/alerts/)

Simple and easy to use Python 3 module to generate password reset tokens, based on JWT ([PyJWT](https://github.com/jpadilla/pyjwt)).

# Usage

### Generating new tokens
```py
from password_reset_token import PasswordResetTokenGenerator

# Secret key for tokens, store it somewhere safe, for example environment variable.
SECRET_KEY = 'super-secret-string'

# Setup generator
token_generator = PasswordResetTokenGenerator(SECRET_KEY)

# Generate PasswordResetToken instance with custom payload.
token = token_generator.generate_new_token('vremes')

# >> PasswordResetToken(json_web_token='eyJ0eXAiOiJKV1QiLCJhbGci...', secret='super-secret-string', algorithm='HS256')
print(token)

# Spit out the payload 
token_payload = token.get_payload()

# >> {'sub': 'vremes', 'exp': 1660396724}
print(token_payload)

# Who does this token belong to?
user_identifier = token_payload.get_user_identifier()

# >> vremes
print(user_identifier)

# Is this token expired?
token_is_expired = token.is_expired()

# >> False
print(token_is_expired)
```

### Using existing tokens
```py
from password_reset_token import PasswordResetToken

SECRET_KEY = 'super-secret-string'

token = PasswordResetToken('eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ2cmVtZXMiLCJleHAiOjE2NjAzOTY3MjR9.F8bHjTCnw46SoCU9LzqCIpmW9tv4Uhtp5NAZUKIotIM', SECRET_KEY)

# >> PasswordResetToken(json_web_token='eyJ0eXAiOiJKV1QiLCJhbGci...', secret='super-secret-string', algorithm='HS256')
print(token)

# Is this token expired?
token_is_expired = token.is_expired()

# >> True
print(token_is_expired)
```

You can view the JWT at [jwt.io](https://jwt.io/#debugger-io?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ2cmVtZXMiLCJleHAiOjE2NjAzOTY3MjR9.F8bHjTCnw46SoCU9LzqCIpmW9tv4Uhtp5NAZUKIotIM) debugger.

### Additional claims

Generated tokens will expire in **one hour** by default, you can override the default expiration time by passing `exp` to `additional_claims` on `generate_new_token` method.

```py
from time import time
from password_reset_token import PasswordResetTokenGenerator

SECRET_KEY = 'super-secret-string'

token_generator = PasswordResetTokenGenerator(SECRET_KEY)

# This token will expire in 10 minutes
token = token_generator.generate_new_token('vremes', {
    "exp": int(time()) + 600
})
```

### Secret keys

You should refer to Python [secrets](https://docs.python.org/3/library/secrets.html) module for secret keys.

Command to generate a secret key:
```sh
python -c "import secrets;print(secrets.token_urlsafe(64))"
```

You should store that secret key into environment variable in your operating system, for example `PASSWORD_RESET_TOKEN_SECRET`.

Then you can access it in your code using `os.getenv` and pass it to `PasswordResetTokenGenerator` constructor.

```py
from os import getenv
from password_reset_token import PasswordResetTokenGenerator

PASSWORD_RESET_TOKEN_SECRET = getenv('PASSWORD_RESET_TOKEN_SECRET')

token_generator = PasswordResetTokenGenerator(PASSWORD_RESET_TOKEN_SECRET)
```

# Demo application 
I wrote a demo application for this module using Flask, check the [repository](https://github.com/vremes/password_reset_token_demo).
