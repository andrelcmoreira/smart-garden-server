from unittest import main, TestCase
from unittest.mock import patch

from models.entities.config import Config
from models.entities.device import Device

from run import create_app


class DeviceLoginEndpointTest(TestCase):

    '''
    Unit tests of /devices/<id>/login endpoint.

    '''

    @patch('flask_jwt_extended.create_access_token')
    @patch('models.device_handler.DeviceHandler.get')
    @patch('models.config_handler.ConfigHandler.get')
    @patch('models.database_mgr.DatabaseMgr.init_db')
    def test_device_login_with_valid_data(self, _, get_config_mock, \
                                          get_device_mock, create_token_mock):
        '''
        TODO
        '''
        app = create_app()

        with app.test_client() as cli:
            cfg = Config(id='id', interval='10', group='group')
            dev = Device(id='id', serial='serial', model='model', desc='desc')
            token = 'fake-token'
            request = { 'id': dev.id, 'serial-number': dev.serial }
            expected_msg = {
                'config': cfg.__dict__,
                'msg': 'Device authenticated with success',
                'token': token
            }

            get_device_mock.return_value = dev
            get_config_mock.return_value = cfg
            create_token_mock.return_value = token

            ret = cli.post('/devices/login/', json=request)

            self.assertEqual(ret.json, expected_msg)
            self.assertEqual(ret.status_code, 200)

            get_device_mock.assert_called_once_with(dev.id)
            get_config_mock.assert_called_once_with(dev.id)
            create_token_mock.assert_called_once_with(
                identity=(dev.id, dev.serial))

    @patch('flask_jwt_extended.create_access_token')
    @patch('models.device_handler.DeviceHandler.get')
    @patch('models.config_handler.ConfigHandler.get')
    @patch('models.database_mgr.DatabaseMgr.init_db')
    def test_device_login_with_invalid_id(self, _, get_config_mock, \
                                          get_device_mock, create_token_mock):
        '''
        TODO
        '''
        app = create_app()

        with app.test_client() as cli:
            request = { 'id': 'bad-id', 'serial-number': 'fakeserial' }
            expected_msg = { 'msg': 'Bad request' }

            ret = cli.post('/devices/login/', json=request)

            self.assertEqual(ret.json, expected_msg)
            self.assertEqual(ret.status_code, 400)

            get_device_mock.assert_not_called()
            get_config_mock.assert_not_called()
            create_token_mock.assert_not_called()

    @patch('flask_jwt_extended.create_access_token')
    @patch('models.device_handler.DeviceHandler.get')
    @patch('models.config_handler.ConfigHandler.get')
    @patch('models.database_mgr.DatabaseMgr.init_db')
    def test_device_login_with_invalid_serial(self, _, get_config_mock, \
                                              get_device_mock, \
                                              create_token_mock):
        '''
        TODO
        '''
        app = create_app()

        with app.test_client() as cli:
            request = { 'id': '2i74qzhd', 'serial-number': '!@#%R' }
            expected_msg = { 'msg': 'Bad request' }

            ret = cli.post('/devices/login/', json=request)

            self.assertEqual(ret.json, expected_msg)
            self.assertEqual(ret.status_code, 400)

            get_device_mock.assert_not_called()
            get_config_mock.assert_not_called()
            create_token_mock.assert_not_called()

    @patch('flask_jwt_extended.create_access_token')
    @patch('models.device_handler.DeviceHandler.get')
    @patch('models.config_handler.ConfigHandler.get')
    @patch('models.database_mgr.DatabaseMgr.init_db')
    def test_device_login_with_missing_id(self, _, get_config_mock, \
                                          get_device_mock, create_token_mock):
        '''
        TODO
        '''
        app = create_app()

        with app.test_client() as cli:
            request = { "serial-number": 'fake-serial' }
            expected_msg = { 'msg': 'Missing required data' }

            ret = cli.post('/devices/login/', json=request)

            self.assertEqual(ret.json, expected_msg)
            self.assertEqual(ret.status_code, 400)

            get_device_mock.assert_not_called()
            get_config_mock.assert_not_called()
            create_token_mock.assert_not_called()

    @patch('flask_jwt_extended.create_access_token')
    @patch('models.device_handler.DeviceHandler.get')
    @patch('models.config_handler.ConfigHandler.get')
    @patch('models.database_mgr.DatabaseMgr.init_db')
    def test_device_login_with_missing_serial(self, _, get_config_mock, \
                                              get_device_mock, \
                                              create_token_mock):
        '''
        TODO
        '''
        app = create_app()

        with app.test_client() as cli:
            request = { 'id': 'fakeid' }
            expected_msg = { 'msg': 'Missing required data' }

            ret = cli.post('/devices/login/', json=request)

            self.assertEqual(ret.json, expected_msg)
            self.assertEqual(ret.status_code, 400)

            get_device_mock.assert_not_called()
            get_config_mock.assert_not_called()
            create_token_mock.assert_not_called()

    @patch('flask_jwt_extended.create_access_token')
    @patch('models.device_handler.DeviceHandler.get')
    @patch('models.config_handler.ConfigHandler.get')
    @patch('models.database_mgr.DatabaseMgr.init_db')
    def test_device_login_with_not_existent_device(self, _, get_config_mock, \
                                                   get_device_mock, \
                                                   create_token_mock):
        '''
        TODO
        '''
        app = create_app()

        with app.test_client() as cli:
            request = { 'id': '2i74qzhd', 'serial-number': 'fakeserial' }
            expected_msg = { 'msg': "The device isn't registered on database" }

            get_device_mock.return_value = None

            ret = cli.post('/devices/login/', json=request)

            self.assertEqual(ret.json, expected_msg)
            self.assertEqual(ret.status_code, 404)

            get_device_mock.assert_called_once_with(request['id'])
            get_config_mock.assert_not_called()
            create_token_mock.assert_not_called()

    @patch('flask_jwt_extended.create_access_token')
    @patch('models.device_handler.DeviceHandler.get')
    @patch('models.config_handler.ConfigHandler.get')
    @patch('models.database_mgr.DatabaseMgr.init_db')
    def test_device_login_with_wrong_serial(self, _, get_config_mock, \
                                            get_device_mock, create_token_mock):
        '''
        TODO
        '''
        app = create_app()

        with app.test_client() as cli:
            dev = Device(serial='wrong-serial', model='fake-model',
                         id='2i74qzhd', desc='fake-desc')
            request = { 'id': dev.id, 'serial-number': 'good-serial' }
            expected_msg = { 'msg': 'Authentication failed' }

            get_device_mock.return_value = dev

            ret = cli.post('/devices/login/', json=request)

            self.assertEqual(ret.json, expected_msg)
            self.assertEqual(ret.status_code, 401)

            get_device_mock.assert_called_once_with(dev.id)
            get_config_mock.assert_not_called()
            create_token_mock.assert_not_called()

    @patch('flask_jwt_extended.create_access_token')
    @patch('models.device_handler.DeviceHandler.get')
    @patch('models.config_handler.ConfigHandler.get')
    @patch('models.database_mgr.DatabaseMgr.init_db')
    def test_device_login_with_not_existent_config(self, _, get_config_mock, \
                                                   get_device_mock, \
                                                   create_token_mock):
        '''
        TODO
        '''
        app = create_app()

        with app.test_client() as cli:
            dev = Device(serial='fakeserial', model="fake-model", id='2i74qzhd',
                         desc='fake-desc')
            request = { "id": dev.id, "serial-number": dev.serial }
            expected_msg = {
                'msg': "There's no config for the specific device"
            }

            get_device_mock.return_value = dev
            get_config_mock.return_value = None

            ret = cli.post('/devices/login/', json=request)

            self.assertEqual(ret.json, expected_msg)
            self.assertEqual(ret.status_code, 404)

            get_device_mock.assert_called_once_with(dev.id)
            get_config_mock.assert_called_once_with(dev.id)
            create_token_mock.assert_not_called()


if __name__ == "__main__":
    main()
