import unittest
from uuid import uuid4
from dataclasses import FrozenInstanceError

from password_reset_token import PasswordResetTokenGenerator, PasswordResetToken

SECRET_KEY_FOR_TESTS = 'test'
GENERATOR = PasswordResetTokenGenerator(SECRET_KEY_FOR_TESTS)
USER_IDENTIFIER = str(uuid4())

class TestPasswordResetToken(unittest.TestCase):

    def test_password_reset_token_generator(self):
        token = GENERATOR.generate_new_token(USER_IDENTIFIER)

        self.assertIsInstance(token, PasswordResetToken)

    def test_token_immutability(self):
        token = GENERATOR.generate_new_token(USER_IDENTIFIER)

        with self.assertRaises(FrozenInstanceError):
            token.json_web_token = 'test'

    def test_expired_token(self):
        expired_token = PasswordResetToken('eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiI0ZTcxMDUyYS04YjNjLTQ4NmMtYTNhYi0yZmRlMTBiOTFlMGUiLCJleHAiOjE2NjA0ODYxNDJ9.lnSV4bzW4u0J0fiZIAEAi0V6NEAEKubzQImm3UvLB5Y', SECRET_KEY_FOR_TESTS)
        self.assertTrue(expired_token.is_expired())

    def test_fresh_token(self):
        token = GENERATOR.generate_new_token(USER_IDENTIFIER)

        self.assertFalse(token.is_expired())

    def test_token_payload(self):
        token = GENERATOR.generate_new_token(USER_IDENTIFIER)

        token_payload = token.get_payload()

        self.assertIsInstance(token_payload, dict)

        token_user_identifier = token.get_user_identifier()

        self.assertTrue(token_user_identifier == USER_IDENTIFIER)

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

    def test_token_additional_claims(self):
        token = GENERATOR.generate_new_token(USER_IDENTIFIER, {
            "my-custom-claim": "custom-claim-value",
            "sub": "conflicting-sub"
        })

        token_payload = token.get_payload()

        self.assertTrue(token_payload.get('sub') == USER_IDENTIFIER)
        self.assertTrue(token_payload.get('my-custom-claim') == 'custom-claim-value')

    def test_multiple_tokens(self):
        for uid in range(0, 10):
            token = GENERATOR.generate_new_token(uid)
            self.assertTrue(token.get_user_identifier() == uid)

if __name__ == '__main__':
    unittest.main()
