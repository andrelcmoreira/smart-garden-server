from unittest import main, TestCase
from unittest.mock import patch

from models.entities.user import User
from run import create_app


class LoginEndpointTest(TestCase):

    '''
    Unit tests of /login endpoint.

    '''

    @patch('models.database_mgr.DatabaseMgr.init_db')
    @patch('models.user_handler.UserHandler.get')
    @patch('flask_jwt_extended.create_access_token')
    def test_login_with_valid_credentials(self, create_token_mock, \
                                          get_user_mock, _):
        '''
        GIVEN we have valid credentials
        WHEN  we try to authenticate within the server
        THEN  a token must be generated and returned
        '''
        app = create_app()

        with app.test_client() as cli:
            request = { 'user': 'fake_user', 'password': 'fake_pass' }
            expected_msg = { 'token': 'fake-token' }

            create_token_mock.return_value = expected_msg['token']
            get_user_mock.return_value = User(
                username='fake_user',
                passwd='3991295cc205927003bcea7af76cf72d72cf73860b4dbcaf96' +
                    '66b6885207c2e7'
            )

            ret = cli.post('/login/', json=request)

            self.assertEqual(ret.json, expected_msg)
            self.assertEqual(ret.status_code, 200)

            get_user_mock.assert_called_once_with('fake_user')
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

    @patch('models.database_mgr.DatabaseMgr.init_db')
    @patch('models.user_handler.UserHandler.get')
    @patch('flask_jwt_extended.create_access_token')
    def test_login_with_invalid_user(self, create_token_mock, get_user_mock, _):
        '''
        GIVEN we have an invalid user
        WHEN  we try to authenticate within the server
        THEN  we must to receive the suitable error
        '''
        app = create_app()

        with app.test_client() as cli:
            request = { 'user': 'fake_user', 'password': 'fake_pass' }
            expected_msg = { 'msg': 'Bad credentials!' }

            get_user_mock.return_value = None
            ret = cli.post('/login/', json=request)

            self.assertEqual(ret.json, expected_msg)
            self.assertEqual(ret.status_code, 401)

            get_user_mock.assert_called_once_with('fake_user')
            create_token_mock.assert_not_called()

    @patch('models.database_mgr.DatabaseMgr.init_db')
    @patch('models.user_handler.UserHandler.get')
    @patch('flask_jwt_extended.create_access_token')
    def test_login_with_invalid_passwd(self, create_token_mock, get_user_mock, \
                                       _):
        '''
        GIVEN we have an invalid password
        WHEN  we try to authenticate within the server
        THEN  we must to receive the suitable error
        '''
        app = create_app()

        with app.test_client() as cli:
            request = { 'user': 'fake_user', 'password': 'fake_pass' }
            expected_msg = { 'msg': 'Bad credentials!' }

            get_user_mock.return_value = User(
                username='fake_user',
                passwd='3991300cc205927003bcea7af76cf72d72cf73860b4dbcaf96' +
                    '66b6885207c2e7'
            )
            ret = cli.post('/login/', json=request)

            self.assertEqual(ret.json, expected_msg)
            self.assertEqual(ret.status_code, 401)

            get_user_mock.assert_called_once_with('fake_user')
            create_token_mock.assert_not_called()

if __name__ == '__main__':
    main()
