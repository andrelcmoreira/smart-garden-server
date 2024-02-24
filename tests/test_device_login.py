from unittest import main, TestCase
from unittest.mock import patch

from run import create_app

from models.entities.config import Config
from models.entities.device import Device


class DeviceLoginEndpointTest(TestCase):

    '''
    Unit tests of /devices/<id>/login endpoint.

    '''

    @patch('flask_jwt_extended.create_access_token')
    @patch('models.device_handler.DeviceHandler.get')
    @patch('models.config_handler.ConfigHandler.get')
    @patch('models.database_mgr.DatabaseMgr.init_db')
    def test_device_login_with_valid_data(self, init_db_mock, get_config_mock, \
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
            cfg = Config(id=dev_id, interval="10", group="fake-group")
            dev = Device(serial=serial, model="fake-model", id=dev_id,
                         desc='fake-desc')
            expected_msg = {
                'config': cfg.__dict__,
                'msg': 'Device authenticated with success',
                'token': token
            }

            get_device_mock.return_value = dev
            get_config_mock.return_value = cfg
            create_token_mock.return_value = token

            ret = cli.post('/devices/login/', json=body)

            self.assertEqual(ret.json, expected_msg)
            self.assertEqual(ret.status_code, 200)

            get_device_mock.assert_called_once_with(dev_id)
            get_config_mock.assert_called_once_with(dev_id)
            create_token_mock.assert_called_once_with(identity=(dev_id, serial))

    @patch('flask_jwt_extended.create_access_token')
    @patch('models.device_handler.DeviceHandler.get')
    @patch('models.config_handler.ConfigHandler.get')
    @patch('models.database_mgr.DatabaseMgr.init_db')
    def test_device_login_with_invalid_id(self, init_db_mock, get_config_mock, \
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
    @patch('models.device_handler.DeviceHandler.get')
    @patch('models.config_handler.ConfigHandler.get')
    @patch('models.database_mgr.DatabaseMgr.init_db')
    def test_device_login_with_invalid_serial(self, init_db_mock, \
                                              get_config_mock, \
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

#    @patch('flask_jwt_extended.create_access_token')
#    @patch('storage.devices.Devices.get')
#    @patch('storage.configs.Configs.get')
#    def test_device_login_with_missing_id(self, get_config_mock, \
#                                          get_device_mock, create_token_mock):
#        '''
#        TODO
#        '''
#        app = create_app()
#
#        with app.test_client() as cli:
#            serial = 'fake-serial'
#            body = { "serial-number": serial }
#            expected_msg = { 'msg': 'Missing required data' }
#
#            ret = cli.post('/devices/login/', json=body)
#
#            self.assertEqual(ret.json, expected_msg)
#            self.assertEqual(ret.status_code, 400)
#
#            get_device_mock.assert_not_called()
#            get_config_mock.assert_not_called()
#            create_token_mock.assert_not_called()
#
#    @patch('flask_jwt_extended.create_access_token')
#    @patch('storage.devices.Devices.get')
#    @patch('storage.configs.Configs.get')
#    def test_device_login_with_missing_serial(self, get_config_mock, \
#                                              get_device_mock, \
#                                              create_token_mock):
#        '''
#        TODO
#        '''
#        app = create_app()
#
#        with app.test_client() as cli:
#            dev_id = 'fakeid'
#            body = { 'id': dev_id }
#            expected_msg = { 'msg': 'Missing required data' }
#
#            ret = cli.post('/devices/login/', json=body)
#
#            self.assertEqual(ret.json, expected_msg)
#            self.assertEqual(ret.status_code, 400)
#
#            get_device_mock.assert_not_called()
#            get_config_mock.assert_not_called()
#            create_token_mock.assert_not_called()
#
#    @patch('flask_jwt_extended.create_access_token')
#    @patch('storage.devices.Devices.get')
#    @patch('storage.configs.Configs.get')
#    def test_device_login_with_not_existent_device(self, get_config_mock, \
#                                                   get_device_mock, \
#                                                   create_token_mock):
#        '''
#        TODO
#        '''
#        app = create_app()
#
#        with app.test_client() as cli:
#            dev_id = '2i74qzhd'
#            serial = 'fakeserial'
#            body = { "id": dev_id, "serial-number": serial }
#            expected_msg = { 'msg': 'Device not registered on database' }
#
#            get_device_mock.return_value = {}
#
#            ret = cli.post('/devices/login/', json=body)
#
#            self.assertEqual(ret.json, expected_msg)
#            self.assertEqual(ret.status_code, 404)
#
#            get_device_mock.assert_called_once_with(dev_id)
#            get_config_mock.assert_not_called()
#            create_token_mock.assert_not_called()
#
#    @patch('flask_jwt_extended.create_access_token')
#    @patch('storage.devices.Devices.get')
#    @patch('storage.configs.Configs.get')
#    def test_device_login_with_wrong_serial(self, get_config_mock, \
#                                            get_device_mock, create_token_mock):
#        '''
#        TODO
#        '''
#        app = create_app()
#
#        with app.test_client() as cli:
#            dev_id = '2i74qzhd'
#            serial = 'fakeserial'
#            body = { "id": dev_id, "serial-number": serial }
#            dev = {
#                "desc": "fake-desc",
#                "id": dev_id,
#                "model": "fake-model",
#                "serial": "wrong-serial"
#            }
#            expected_msg = { 'msg': 'Authentication failed' }
#
#            get_device_mock.return_value = dev
#
#            ret = cli.post('/devices/login/', json=body)
#
#            self.assertEqual(ret.json, expected_msg)
#            self.assertEqual(ret.status_code, 401)
#
#            get_device_mock.assert_called_once_with(dev_id)
#            get_config_mock.assert_not_called()
#            create_token_mock.assert_not_called()
#
#    @patch('flask_jwt_extended.create_access_token')
#    @patch('storage.devices.Devices.get')
#    @patch('storage.configs.Configs.get')
#    def test_device_login_with_not_existent_config(self, get_config_mock, \
#                                                   get_device_mock, \
#                                                   create_token_mock):
#        '''
#        TODO
#        '''
#        app = create_app()
#
#        with app.test_client() as cli:
#            dev_id = '2i74qzhd'
#            serial = 'fakeserial'
#            body = { "id": dev_id, "serial-number": serial }
#            dev = {
#                "desc": "fake-desc",
#                "id": dev_id,
#                "model": "fake-model",
#                "serial": serial
#            }
#            expected_msg = {
#                'msg': "There's no config for the specified device"
#            }
#
#            get_config_mock.return_value = {}
#            get_device_mock.return_value = dev
#
#            ret = cli.post('/devices/login/', json=body)
#
#            self.assertEqual(ret.json, expected_msg)
#            self.assertEqual(ret.status_code, 404)
#
#            get_device_mock.assert_called_once_with(dev_id)
#            get_config_mock.assert_called_once_with(dev_id)
#            create_token_mock.assert_not_called()

if __name__ == "__main__":
    main()
