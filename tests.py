import unittest
from dataclasses import FrozenInstanceError

from password_reset_token import PasswordResetTokenGenerator, PasswordResetToken

SECRET_KEY_FOR_TESTS = 'test'

class TestPasswordResetToken(unittest.TestCase):

    def test_password_reset_token_generator(self):
        generator = PasswordResetTokenGenerator(SECRET_KEY_FOR_TESTS)

        token = generator.generate_new_token({
            "hello": "world"
        })

        self.assertIsInstance(token, PasswordResetToken)

    def test_token_immutability(self):
        generator = PasswordResetTokenGenerator(SECRET_KEY_FOR_TESTS)

        token = generator.generate_new_token({
            "hello": "world"
        })

        with self.assertRaises(FrozenInstanceError):
            token.json_web_token = 'test'

    def test_expired_token(self):
        expired_token = PasswordResetToken('eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJoZWxsbyI6IndvcmxkIiwiZXhwIjoxNjYwMzg5MzQ0fQ.nVskhnaRfMsbZVwJ5O5R6PQoiv9O2QZlZrSRpNQb75s', SECRET_KEY_FOR_TESTS)
        self.assertTrue(expired_token.is_expired())

    def test_fresh_token(self):
        generator = PasswordResetTokenGenerator(SECRET_KEY_FOR_TESTS)

        token = generator.generate_new_token({
            "hello": "world"
        })

        self.assertFalse(token.is_expired())

    def test_token_payload(self):
        generator = PasswordResetTokenGenerator(SECRET_KEY_FOR_TESTS)

        token = generator.generate_new_token({
            "hello": "world"
        })

        token_payload = token.get_payload()

        self.assertIsInstance(token_payload, dict)

        token_payload_hello = token_payload.get('hello')

        self.assertIsNotNone(token_payload_hello)

        self.assertTrue(token_payload_hello == 'world')

        token_missing_key = token_payload.get('does-not-exist')

        self.assertIsNone(token_missing_key)

    def test_malformed_token(self):
        malformed_token = PasswordResetToken('eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJoZWxsbyI6IndvcmxkIiwiZXhwIjoxNjYw', SECRET_KEY_FOR_TESTS)

        payload_is_empty = not malformed_token.get_payload()

        self.assertTrue(payload_is_empty)
        
        token_expired = malformed_token.is_expired()

        self.assertTrue(token_expired)

    def test_token_with_random_string(self):
        token = PasswordResetToken('this-is-not-a-jwt', SECRET_KEY_FOR_TESTS)

        payload_is_empty = not token.get_payload()

        self.assertTrue(payload_is_empty)
        
        token_expired = token.is_expired()

        self.assertTrue(token_expired)

if __name__ == '__main__':
    unittest.main()
