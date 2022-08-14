# password_reset_token

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

# Demo application 
I wrote a demo application for this module using Flask, check the [repository](https://github.com/vremes/password_reset_token_demo).
