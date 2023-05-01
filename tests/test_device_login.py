from unittest import main, TestCase
from unittest.mock import patch

from run import create_app

class DeviceLoginEndpointTest(TestCase):

    '''
    TODO
    '''

    @patch('flask_jwt_extended.create_access_token')
    @patch('app.storage.devices.Devices.get')
    @patch('app.storage.configs.Configs.get')
    def test_device_login_with_valid_data(self, get_config_mock, \
                                          get_device_mock, create_token_mock):
        '''
        TODO
        '''
        app = create_app()

        with app.test_client() as cli:
            dev_id = '2i74qzhd'
            serial = 'fakeserial'
            body = { "id": dev_id, "serial-number": serial }
            token = 'fake-token'
            cfg = { "group": "fake-group", "id": dev_id, "interval": "10" }
            dev = {
                "desc": "fake-desc",
                "id": dev_id,
                "model": "fake-model",
                "serial": serial
            }
            expected_msg = {
                'msg': 'Device authenticated with success',
                'token': token,
                'config': cfg
            }

            get_config_mock.return_value = cfg
            get_device_mock.return_value = dev
            create_token_mock.return_value = token

            ret = cli.post('/devices/login/', json=body)

            self.assertEqual(ret.json, expected_msg)
            self.assertEqual(ret.status_code, 200)

            get_device_mock.assert_called_once_with(dev_id)
            get_config_mock.assert_called_once_with(dev_id)
            create_token_mock.assert_called_once_with(identity=(dev_id, serial))

    @patch('flask_jwt_extended.create_access_token')
    @patch('app.storage.devices.Devices.get')
    @patch('app.storage.configs.Configs.get')
    def test_device_login_with_invalid_id(self, get_config_mock, \
                                          get_device_mock, create_token_mock):
        '''
        TODO
        '''
        app = create_app()

        with app.test_client() as cli:
            dev_id = 'bad-id'
            serial = 'fakeserial'
            body = { "id": dev_id, "serial-number": serial }
            expected_msg = { 'msg': 'Bad request' }

            ret = cli.post('/devices/login/', json=body)

            self.assertEqual(ret.json, expected_msg)
            self.assertEqual(ret.status_code, 400)

            get_device_mock.assert_not_called()
            get_config_mock.assert_not_called()
            create_token_mock.assert_not_called()

    @patch('flask_jwt_extended.create_access_token')
    @patch('app.storage.devices.Devices.get')
    @patch('app.storage.configs.Configs.get')
    def test_device_login_with_invalid_serial(self, get_config_mock, \
                                              get_device_mock, \
                                              create_token_mock):
        '''
        TODO
        '''
        app = create_app()

        with app.test_client() as cli:
            dev_id = '2i74qzhd'
            serial = '!@#%R'
            body = { "id": dev_id, "serial-number": serial }
            expected_msg = { 'msg': 'Bad request' }

            ret = cli.post('/devices/login/', json=body)

            self.assertEqual(ret.json, expected_msg)
            self.assertEqual(ret.status_code, 400)

            get_device_mock.assert_not_called()
            get_config_mock.assert_not_called()
            create_token_mock.assert_not_called()

    @patch('flask_jwt_extended.create_access_token')
    @patch('app.storage.devices.Devices.get')
    @patch('app.storage.configs.Configs.get')
    def test_device_login_with_missing_id(self, get_config_mock, \
                                          get_device_mock, create_token_mock):
        '''
        TODO
        '''
        app = create_app()

        with app.test_client() as cli:
            serial = 'fake-serial'
            body = { "serial-number": serial }
            expected_msg = { 'msg': 'Missing required data' }

            ret = cli.post('/devices/login/', json=body)

            self.assertEqual(ret.json, expected_msg)
            self.assertEqual(ret.status_code, 400)

            get_device_mock.assert_not_called()
            get_config_mock.assert_not_called()
            create_token_mock.assert_not_called()

    @patch('flask_jwt_extended.create_access_token')
    @patch('app.storage.devices.Devices.get')
    @patch('app.storage.configs.Configs.get')
    def test_device_login_with_missing_serial(self, get_config_mock, \
                                              get_device_mock, \
                                              create_token_mock):
        '''
        TODO
        '''
        app = create_app()

        with app.test_client() as cli:
            dev_id = 'fakeid'
            body = { 'id': dev_id }
            expected_msg = { 'msg': 'Missing required data' }

            ret = cli.post('/devices/login/', json=body)

            self.assertEqual(ret.json, expected_msg)
            self.assertEqual(ret.status_code, 400)

            get_device_mock.assert_not_called()
            get_config_mock.assert_not_called()
            create_token_mock.assert_not_called()

    @patch('flask_jwt_extended.create_access_token')
    @patch('app.storage.devices.Devices.get')
    @patch('app.storage.configs.Configs.get')
    def test_device_login_with_not_existent_device(self, get_config_mock, \
                                                   get_device_mock, \
                                                   create_token_mock):
        '''
        TODO
        '''
        app = create_app()

        with app.test_client() as cli:
            dev_id = '2i74qzhd'
            serial = 'fakeserial'
            body = { "id": dev_id, "serial-number": serial }
            expected_msg = { 'msg': 'Device not registered on database' }

            get_device_mock.return_value = {}

            ret = cli.post('/devices/login/', json=body)

            self.assertEqual(ret.json, expected_msg)
            self.assertEqual(ret.status_code, 404)

            get_device_mock.assert_called_once_with(dev_id)
            get_config_mock.assert_not_called()
            create_token_mock.assert_not_called()

    @patch('flask_jwt_extended.create_access_token')
    @patch('app.storage.devices.Devices.get')
    @patch('app.storage.configs.Configs.get')
    def test_device_login_with_wrong_serial(self, get_config_mock, \
                                            get_device_mock, create_token_mock):
        '''
        TODO
        '''
        app = create_app()

        with app.test_client() as cli:
            dev_id = '2i74qzhd'
            serial = 'fakeserial'
            body = { "id": dev_id, "serial-number": serial }
            dev = {
                "desc": "fake-desc",
                "id": dev_id,
                "model": "fake-model",
                "serial": "wrong-serial"
            }
            expected_msg = { 'msg': 'Authentication failed' }

            get_device_mock.return_value = dev

            ret = cli.post('/devices/login/', json=body)

            self.assertEqual(ret.json, expected_msg)
            self.assertEqual(ret.status_code, 401)

            get_device_mock.assert_called_once_with(dev_id)
            get_config_mock.assert_not_called()
            create_token_mock.assert_not_called()

    @patch('flask_jwt_extended.create_access_token')
    @patch('app.storage.devices.Devices.get')
    @patch('app.storage.configs.Configs.get')
    def test_device_login_with_not_existent_config(self, get_config_mock, \
                                                   get_device_mock, \
                                                   create_token_mock):
        '''
        TODO
        '''
        app = create_app()

        with app.test_client() as cli:
            dev_id = '2i74qzhd'
            serial = 'fakeserial'
            body = { "id": dev_id, "serial-number": serial }
            dev = {
                "desc": "fake-desc",
                "id": dev_id,
                "model": "fake-model",
                "serial": serial
            }
            expected_msg = {
                'msg': "There's no config for the specified device"
            }

            get_config_mock.return_value = {}
            get_device_mock.return_value = dev

            ret = cli.post('/devices/login/', json=body)

            self.assertEqual(ret.json, expected_msg)
            self.assertEqual(ret.status_code, 404)

            get_device_mock.assert_called_once_with(dev_id)
            get_config_mock.assert_called_once_with(dev_id)
            create_token_mock.assert_not_called()

if __name__ == "__main__":
    main()
