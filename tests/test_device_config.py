from unittest import main, TestCase
from unittest.mock import patch

from run import create_app

class DeviceConfigEndpointTest(TestCase):

    '''
    TODO
    '''

    @patch('flask_jwt_extended.view_decorators.verify_jwt_in_request')
    @patch('app.storage.configs.Configs.get_all')
    def test_get_configs_with_empty_db(self, get_all_mock, jwt_required_mock):
        '''
        TODO
        '''
        app = create_app()

        with app.test_client() as cli:
            get_all_mock.return_value = []

            ret = cli.get('/devices/config/')

            self.assertEqual(ret.json, [])
            self.assertEqual(ret.status_code, 200)

            jwt_required_mock.assert_called_once()
            get_all_mock.assert_called_once()

    @patch('flask_jwt_extended.view_decorators.verify_jwt_in_request')
    @patch('app.storage.configs.Configs.get_all')
    def test_get_devices_with_not_empty_db(self, get_all_mock, \
                                           jwt_required_mock):
        '''
        TODO
        '''
        app = create_app()

        with app.test_client() as cli:
            configs = [
                {
                  "id": "fakeid",
                  "group": "fake-group",
                  "interval": "10"
                },
                {
                  "id": "fakeid",
                  "group": "fake-group",
                  "interval": "20"
                }
            ]

            get_all_mock.return_value = configs

            ret = cli.get('/devices/config/')

            self.assertEqual(ret.json, configs)
            self.assertEqual(ret.status_code, 200)

            jwt_required_mock.assert_called_once()
            get_all_mock.assert_called_once()

    @patch('flask_jwt_extended.view_decorators.verify_jwt_in_request')
    @patch('app.storage.configs.Configs.get')
    def test_get_config_with_not_existent_config(self, get_mock, \
                                                 jwt_required_mock):
        '''
        TODO
        '''
        app = create_app()

        with app.test_client() as cli:
            dev_id = 'fakeid'
            expected_error = {
                "msg": "The config isn't registered on database"
            }

            get_mock.return_value = {}

            ret = cli.get(f'/devices/{dev_id}/config/')

            self.assertEqual(ret.json, expected_error)
            self.assertEqual(ret.status_code, 404)

            jwt_required_mock.assert_called_once()
            get_mock.assert_called_once_with(dev_id)

    @patch('flask_jwt_extended.view_decorators.verify_jwt_in_request')
    @patch('app.storage.configs.Configs.get')
    def test_get_config_with_existent_config(self, get_mock, jwt_required_mock):
        '''
        TODO
        '''
        app = create_app()

        with app.test_client() as cli:
            dev_id = 'fakeid'
            cfg_data = {
                "id": dev_id,
                "group": "fake-group",
                "interval": "10"
            }

            get_mock.return_value = cfg_data

            ret = cli.get(f'/devices/{dev_id}/config/')

            self.assertEqual(ret.json, cfg_data)
            self.assertEqual(ret.status_code, 200)

            jwt_required_mock.assert_called_once()
            get_mock.assert_called_once_with(dev_id)

    @patch('flask_jwt_extended.view_decorators.verify_jwt_in_request')
    @patch('app.storage.configs.Configs.get')
    @patch('app.storage.configs.Configs.rm')
    def test_del_config_with_existent_config(self, rm_mock, get_mock, \
                                             jwt_required_mock):
        '''
        TODO
        '''
        app = create_app()

        with app.test_client() as cli:
            dev_id = 'fakeid'
            cfg_data = {
                "id": dev_id,
                "group": "fake-group",
                "interval": "10"
            }
            expected_msg = { 'msg': 'Config deleted from database' }

            get_mock.return_value = cfg_data

            ret = cli.delete(f'/devices/{dev_id}/config/')

            self.assertEqual(ret.json, expected_msg)
            self.assertEqual(ret.status_code, 200)

            jwt_required_mock.assert_called_once()
            get_mock.assert_called_once_with(dev_id)
            rm_mock.assert_called_once_with(dev_id)

    @patch('flask_jwt_extended.view_decorators.verify_jwt_in_request')
    @patch('app.storage.configs.Configs.get')
    @patch('app.storage.configs.Configs.rm')
    def test_del_config_with_not_existent_config(self, rm_mock, get_mock, \
                                                 jwt_required_mock):
        '''
        TODO
        '''
        app = create_app()

        with app.test_client() as cli:
            dev_id = 'fakeid'
            expected_msg = {
                "msg": "There's no config for the specific device"
            }

            get_mock.return_value = {}

            ret = cli.delete(f'/devices/{dev_id}/config/')

            self.assertEqual(ret.json, expected_msg)
            self.assertEqual(ret.status_code, 404)

            jwt_required_mock.assert_called_once()
            get_mock.assert_called_once_with(dev_id)
            rm_mock.assert_not_called()

#   @patch('random.sample')
#   @patch('flask_jwt_extended.view_decorators.verify_jwt_in_request')
#   @patch('app.storage.devices.Devices.add')
#   def test_register_device(self, add_mock, jwt_required_mock, sample_mock):
#       '''
#       TODO
#       '''
#       app = create_app()

#       with app.test_client() as cli:
#           device_id = 'fakeid'
#           body = {
#               "serial-number": "fake-serial",
#               "model": "fake-model",
#               "description": "fake desc"
#           }
#           expected_msg = {
#               'msg': 'Device registered with success',
#               'id': device_id
#           }
#           fake_device = Device(
#               id=device_id,
#               serial=body['serial-number'],
#               model=body['model'],
#               desc=body['description']
#           )

#           sample_mock.return_value = device_id

#           ret = cli.post('/devices/', json=body)

#           self.assertEqual(ret.json, expected_msg)
#           self.assertEqual(ret.status_code, 201)

#           jwt_required_mock.assert_called_once()
#           sample_mock.assert_called_once()
#           add_mock.assert_called_once_with(fake_device)

#   @patch('flask_jwt_extended.view_decorators.verify_jwt_in_request')
#   @patch('app.storage.devices.Devices.add')
#   def test_register_device_with_missing_model(self, add_mock, \
#                                               jwt_required_mock):
#       '''
#       TODO
#       '''
#       app = create_app()

#       with app.test_client() as cli:
#           body = {
#               "serial-number": "fake-serial",
#               "description": "fake-desc",
#           }
#           expected_msg = { 'msg': 'Missing required data' }

#           ret = cli.post('/devices/', json=body)

#           self.assertEqual(ret.json, expected_msg)
#           self.assertEqual(ret.status_code, 400)

#           jwt_required_mock.assert_called_once()
#           add_mock.assert_not_called()

#   @patch('flask_jwt_extended.view_decorators.verify_jwt_in_request')
#   @patch('app.storage.devices.Devices.add')
#   def test_register_device_with_blank_model(self, add_mock, \
#                                             jwt_required_mock):
#       '''
#       TODO
#       '''
#       app = create_app()

#       with app.test_client() as cli:
#           body = {
#               "serial-number": "fake-serial",
#               "model": "",
#               "description": "fake-desc",
#           }
#           expected_msg = { 'msg': 'Bad request' }

#           ret = cli.post('/devices/', json=body)

#           self.assertEqual(ret.json, expected_msg)
#           self.assertEqual(ret.status_code, 400)

#           jwt_required_mock.assert_called_once()
#           add_mock.assert_not_called()

#   @patch('flask_jwt_extended.view_decorators.verify_jwt_in_request')
#   @patch('app.storage.devices.Devices.add')
#   def test_register_device_with_missing_serial(self, add_mock, \
#                                                jwt_required_mock):
#       '''
#       TODO
#       '''
#       app = create_app()

#       with app.test_client() as cli:
#           body = {
#               "description": "fake desc",
#               "model": "fakemodel",
#           }
#           expected_msg = { 'msg': 'Missing required data' }

#           ret = cli.post('/devices/', json=body)

#           self.assertEqual(ret.json, expected_msg)
#           self.assertEqual(ret.status_code, 400)

#           jwt_required_mock.assert_called_once()
#           add_mock.assert_not_called()

#   @patch('flask_jwt_extended.view_decorators.verify_jwt_in_request')
#   @patch('app.storage.devices.Devices.add')
#   def test_register_device_with_blank_serial(self, add_mock, \
#                                              jwt_required_mock):
#       '''
#       TODO
#       '''
#       app = create_app()

#       with app.test_client() as cli:
#           body = {
#               "serial-number": "",
#               "model": "fakemodel",
#               "description": "fake desc"
#           }
#           expected_msg = { 'msg': 'Bad request' }

#           ret = cli.post('/devices/', json=body)

#           self.assertEqual(ret.json, expected_msg)
#           self.assertEqual(ret.status_code, 400)

#           jwt_required_mock.assert_called_once()
#           add_mock.assert_not_called()

#   @patch('random.sample')
#   @patch('flask_jwt_extended.view_decorators.verify_jwt_in_request')
#   @patch('app.storage.devices.Devices.add')
#   def test_register_device_with_missing_desc(self, add_mock, \
#                                              jwt_required_mock, sample_mock):
#       '''
#       TODO
#       '''
#       app = create_app()

#       with app.test_client() as cli:
#           device_id = 'fakeid'
#           body = {
#               "model": "fakemodel",
#               "serial-number": "fake-serial",
#               "description": "",
#           }
#           expected_msg = {
#               'msg': 'Device registered with success',
#               'id': device_id
#           }
#           fake_device = Device(
#               id=device_id,
#               serial=body['serial-number'],
#               model=body['model'],
#               desc=body['description']
#           )

#           sample_mock.return_value = device_id

#           ret = cli.post('/devices/', json=body)

#           self.assertEqual(ret.json, expected_msg)
#           self.assertEqual(ret.status_code, 201)

#           jwt_required_mock.assert_called_once()
#           sample_mock.assert_called_once()
#           add_mock.assert_called_once()

#   @patch('random.sample')
#   @patch('flask_jwt_extended.view_decorators.verify_jwt_in_request')
#   @patch('app.storage.devices.Devices.add')
#   def test_register_device_with_blank_desc(self, add_mock, \
#                                            jwt_required_mock, sample_mock):
#       '''
#       TODO
#       '''
#       app = create_app()

#       with app.test_client() as cli:
#           device_id = 'fakeid'
#           body = {
#               "model": "fakemodel",
#               "serial-number": "fake-serial",
#               "description": "",
#           }
#           expected_msg = {
#               'msg': 'Device registered with success',
#               'id': device_id
#           }
#           fake_device = Device(
#               id=device_id,
#               serial=body['serial-number'],
#               model=body['model'],
#               desc=body['description']
#           )

#           sample_mock.return_value = device_id

#           ret = cli.post('/devices/', json=body)

#           self.assertEqual(ret.json, expected_msg)
#           self.assertEqual(ret.status_code, 201)

#           jwt_required_mock.assert_called_once()
#           sample_mock.assert_called_once()
#           add_mock.assert_called_once()

#   @patch('flask_jwt_extended.view_decorators.verify_jwt_in_request')
#   @patch('app.storage.devices.Devices.add')
#   def test_register_device_with_no_parameters(self, add_mock, \
#                                               jwt_required_mock):
#       '''
#       TODO
#       '''
#       app = create_app()

#       with app.test_client() as cli:
#           expected_msg = { 'msg': 'Bad request' }

#           ret = cli.post('/devices/', json={})

#           self.assertEqual(ret.json, expected_msg)
#           self.assertEqual(ret.status_code, 400)

#           jwt_required_mock.assert_called_once()
#           add_mock.assert_not_called()

#   @patch('flask_jwt_extended.view_decorators.verify_jwt_in_request')
#   @patch('app.storage.devices.Devices.get')
#   @patch('app.storage.devices.Devices.update')
#   def test_update_not_existent_device(self, update_mock, get_mock, \
#                                       jwt_required_mock):
#       '''
#       TODO
#       '''
#       app = create_app()

#       with app.test_client() as cli:
#           dev_id = 'fakeid'
#           expected_msg = {
#               "msg": "The device isn't registered on database"
#           }
#           data = { 'param': 'foo-param', 'value': 'foo-value' }

#           get_mock.return_value = {}

#           ret = cli.put('/devices/' + dev_id, json=data)

#           self.assertEqual(ret.json, expected_msg)
#           self.assertEqual(ret.status_code, 404)

#           jwt_required_mock.assert_called_once()
#           get_mock.assert_called_once_with(dev_id)
#           update_mock.assert_not_called()

#   @patch('flask_jwt_extended.view_decorators.verify_jwt_in_request')
#   @patch('app.storage.devices.Devices.get')
#   @patch('app.storage.devices.Devices.update')
#   def test_update_existent_device(self, update_mock, get_mock, \
#                                   jwt_required_mock):
#        '''
#        TODO
#        '''
#        app = create_app()

#        with app.test_client() as cli:
#            dev_id = 'fakeid'
#            data = { 'param': 'foo-param', 'value': 'foo-value' }
#            expected_msg = { "msg": "Device updated in database" }

#            get_mock.return_value = {
#                "device-id": "fake-id",
#                "serial-number": "fake-serial",
#                "description": "fake-desc",
#            }

#            ret = cli.put('/devices/' + dev_id, json=data)

#            self.assertEqual(ret.json, expected_msg)
#            self.assertEqual(ret.status_code, 200)

#            jwt_required_mock.assert_called_once()
#            get_mock.assert_called_once_with(dev_id)
#            update_mock.assert_called_once_with(
#                dev_id,
#                data['param'],
#                data['value']
#            )

    @patch('app.storage.configs.Configs.get_all')
    def test_get_config_without_token(self, get_all_mock):
        '''
        TODO
        '''
        app = create_app()

        with app.test_client() as cli:
            dev_id = 'fakeid'
            expected_msg = { 'msg': 'Missing Authorization Header' }

            ret = cli.get(f'/devices/{dev_id}/config/')

            self.assertEqual(ret.json, expected_msg)
            self.assertEqual(ret.status_code, 401)

            get_all_mock.assert_not_called()

    @patch('app.storage.configs.Configs.get')
    def test_get_config_without_token(self, get_mock):
        '''
        TODO
        '''
        app = create_app()

        with app.test_client() as cli:
            dev_id = 'fakeid'
            expected_msg = { 'msg': 'Missing Authorization Header' }

            ret = cli.get(f'/devices/{dev_id}/config/')

            self.assertEqual(ret.json, expected_msg)
            self.assertEqual(ret.status_code, 401)

            get_mock.assert_not_called()

    @patch('app.storage.configs.Configs.get')
    @patch('app.storage.configs.Configs.rm')
    def test_del_config_without_token(self, rm_mock, get_mock):
        '''
        TODO
        '''
        app = create_app()

        with app.test_client() as cli:
            dev_id = 'fakeid'
            expected_msg = { 'msg': 'Missing Authorization Header' }

            ret = cli.delete(f'/devices/{dev_id}/config/')

            self.assertEqual(ret.json, expected_msg)
            self.assertEqual(ret.status_code, 401)

            get_mock.assert_not_called()
            rm_mock.assert_not_called()

    @patch('app.storage.configs.Configs.add')
    def test_register_config_without_token(self, add_mock):
        '''
        TODO
        '''
        app = create_app()

        with app.test_client() as cli:
            dev_id = 'fakeid'
            body = {
                "group": "fake-group",
                "interval": "20"
            }
            expected_msg = { 'msg': 'Missing Authorization Header' }

            ret = cli.post(f'/devices/{dev_id}/config/', json=body)

            self.assertEqual(ret.json, expected_msg)
            self.assertEqual(ret.status_code, 401)

            add_mock.assert_not_called()

    @patch('app.storage.configs.Configs.get')
    @patch('app.storage.configs.Configs.update')
    def test_update_config_without_token(self, update_mock, get_mock):
        '''
        TODO
        '''
        app = create_app()

        with app.test_client() as cli:
            dev_id = 'fake_id'
            data = { 'param': 'interval', 'value': '10' }
            expected_msg = { 'msg': 'Missing Authorization Header' }

            ret = cli.put(f'/devices/{dev_id}/config/', json=data)

            self.assertEqual(ret.json, expected_msg)
            self.assertEqual(ret.status_code, 401)

            get_mock.assert_not_called()
            update_mock.assert_not_called()

if __name__ == "__main__":
    main()
