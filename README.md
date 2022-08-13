# password_reset_token

Simple and easy to use Python 3 module to generate password reset tokens, based on JWT ([PyJWT](https://github.com/jpadilla/pyjwt)).

# Usage

```py
# Secret key for tokens, store it somewhere safe, for example environment variable.
SECRET_KEY = 'super-secret-string'

# Setup generator
token_generator = PasswordResetTokenGenerator(SECRET_KEY)

# Generate PasswordResetToken instance with custom payload.
token = token_generator.generate_new_token({
    "sub": "vremes"
})

# >> PasswordResetToken(json_web_token='eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ2cmVtZXMiLCJleHAiOjE2NjAzOTY3MjR9.F8bHjTCnw46SoCU9LzqCIpmW9tv4Uhtp5NAZUKIotIM', secret='super-secret-string', algorithm='HS256')
print(token)

# Spit out the payload 
token_payload = token.get_payload()

# >> {'sub': 'vremes', 'exp': 1660396750}
print(token_payload)

# Who does this token belong to?
token_subject = token_payload.get('sub')

# >> vremes
print(token_subject)

# Is this token expired?
token_is_expired = token.is_expired()

# >> False
print(token_is_expired)
```

You can view the JWT at [jwt.io](https://jwt.io/#debugger-io?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ2cmVtZXMiLCJleHAiOjE2NjAzOTY3MjR9.F8bHjTCnw46SoCU9LzqCIpmW9tv4Uhtp5NAZUKIotIM) debugger.
