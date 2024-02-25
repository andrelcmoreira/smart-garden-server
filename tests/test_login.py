from unittest import main, TestCase
from unittest.mock import patch

from run import create_app


class LoginEndpointTest(TestCase):

    '''
    Unit tests of /login endpoint.

    '''

    @patch('models.database_mgr.DatabaseMgr.init_db')
    @patch('flask_jwt_extended.create_access_token')
    def test_login_with_valid_credentials(self, create_token_mock, _):
        '''
        GIVEN we have valid credentials
        WHEN  we try to authenticate within the server
        THEN  a token must be generated and returned
        '''
        app = create_app()

        with app.test_client() as cli:
            request = { 'user': 'fake_user', 'password': 'fake_pass' }
            token = 'fake-token'
            expected_msg = { 'token': token }

            create_token_mock.return_value = token

            ret = cli.post('/login/', json=request)

            self.assertEqual(ret.json, expected_msg)
            self.assertEqual(ret.status_code, 200)

            create_token_mock.assert_called_once_with(
                identity=(request['user'], request['password']))

    @patch('models.database_mgr.DatabaseMgr.init_db')
    @patch('flask_jwt_extended.create_access_token')
    def test_login_with_no_user(self, create_token_mock, _):
        '''
        GIVEN we have no valid user
        WHEN  we try to authenticate within the server
        THEN  the suitable error must be returned
        '''
        app = create_app()

        with app.test_client() as cli:
            request = { 'password': 'fake_admin' }
            expected_msg = { 'msg': 'Missing required data' }

            ret = cli.post('/login/', json=request)

            self.assertEqual(ret.json, expected_msg)
            self.assertEqual(ret.status_code, 400)

            create_token_mock.assert_not_called()

    @patch('models.database_mgr.DatabaseMgr.init_db')
    @patch('flask_jwt_extended.create_access_token')
    def test_login_with_no_password(self, create_token_mock, _):
        '''
        GIVEN we have no valid password
        WHEN  we try to authenticate within the server
        THEN  the suitable error must be returned
        '''
        app = create_app()

        with app.test_client() as cli:
            request = { 'user': 'fake_admin' }
            expected_msg = { 'msg': 'Missing required data' }

            ret = cli.post('/login/', json=request)

            self.assertEqual(ret.json, expected_msg)
            self.assertEqual(ret.status_code, 400)

            create_token_mock.assert_not_called()


if __name__ == '__main__':
    main()
