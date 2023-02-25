from unittest import main, TestCase
from unittest.mock import patch

from app import create_app

class LoginEndpointTest(TestCase):

    @patch('flask_jwt_extended.create_access_token')
    def test_login_with_valid_credentials(self, create_token_mock):
        app = create_app()

        with app.test_client() as cli:
            BODY = {
                "user": "fake-user",
                "password": "fake-pass"
            }
            TOKEN = 'fake-token'
            EXPECTED_MSG = { 'token': TOKEN }

            create_token_mock.return_value = TOKEN

            ret = cli.post('/login/', json=BODY)

            self.assertEqual(ret.json, EXPECTED_MSG)
            self.assertEqual(ret.status_code, 200)

            create_token_mock.assert_called_once_with(
                identity=(BODY['user'], BODY['password'])
            )

    @patch('flask_jwt_extended.create_access_token')
    def test_login_with_no_user(self, create_token_mock):
        app = create_app()

        with app.test_client() as cli:
            BODY = {
                "password": "fake-admin"
            }
            EXPECTED_MSG = { 'msg': 'invalid user credentials!' }

            ret = cli.post('/login/', json=BODY)

            self.assertEqual(ret.json, EXPECTED_MSG)
            self.assertEqual(ret.status_code, 400)

            create_token_mock.assert_not_called()

    @patch('flask_jwt_extended.create_access_token')
    def test_login_with_no_password(self, create_token_mock):
        app = create_app()

        with app.test_client() as cli:
            BODY = {
                "user": "fake-admin"
            }
            EXPECTED_MSG = { 'msg': 'invalid user credentials!' }

            ret = cli.post('/login/', json=BODY)

            self.assertEqual(ret.json, EXPECTED_MSG)
            self.assertEqual(ret.status_code, 400)

            create_token_mock.assert_not_called()

if __name__ == "__main__":
    main()
