from unittest import main, TestCase
from unittest.mock import patch

from flask_jwt_extended import create_access_token

from app.storage.models.device import Device
from run import create_app

class DeviceEndpointTest(TestCase):

    # TODO: remove mocks

    @patch('flask_jwt_extended.view_decorators.verify_jwt_in_request')
    @patch('app.storage.devices.Devices.get_all')
    def test_get_devices_with_empty_db(self, get_all_mock, jwt_required_mock):
        app = create_app()

        with app.test_client() as cli:
            get_all_mock.return_value = []

            ret = cli.get('/devices/')

            self.assertEqual(ret.json, [])
            self.assertEqual(ret.status_code, 200)

            jwt_required_mock.assert_called_once()
            get_all_mock.assert_called_once()

    @patch('flask_jwt_extended.view_decorators.verify_jwt_in_request')
    @patch('app.storage.devices.Devices.get_all')
    def test_get_devices_with_not_empty_db(self, get_all_mock, \
                                           jwt_required_mock):
        '''
        TODO
        '''
        app = create_app()

        with app.test_client() as cli:
            devices = [
                {
                  "desc": "foo-desc",
                  "id": "foo-id",
                  "serial": "foo-serial"
                },
                {
                  "desc": "bar-desc",
                  "id": "bar-id",
                  "serial": "bar-serial"
                }
            ]

            get_all_mock.return_value = devices

            ret = cli.get('/devices/')

            self.assertEqual(ret.json, devices)
            self.assertEqual(ret.status_code, 200)

            jwt_required_mock.assert_called_once()
            get_all_mock.assert_called_once()

    @patch('flask_jwt_extended.view_decorators.verify_jwt_in_request')
    @patch('app.storage.devices.Devices.get')
    def test_get_device_with_not_existent_device(self, get_mock, \
                                                 jwt_required_mock):
        '''
        TODO
        '''
        app = create_app()

        with app.test_client() as cli:
            dev_id = 'fakeid'
            expected_error = {
                "msg": "The device isn't registered on database"
            }

            get_mock.return_value = {}

            ret = cli.get('/devices/' + dev_id)

            self.assertEqual(ret.json, expected_error)
            self.assertEqual(ret.status_code, 404)

            jwt_required_mock.assert_called_once()
            get_mock.assert_called_once_with(dev_id)

    @patch('flask_jwt_extended.view_decorators.verify_jwt_in_request')
    @patch('app.storage.devices.Devices.get')
    def test_get_device_with_existent_device(self, get_mock, jwt_required_mock):
        '''
        TODO
        '''
        app = create_app()

        with app.test_client() as cli:
            dev_id = 'fakeid'
            device_data = {
                "desc": "fake-desc",
                "id": "fake-id",
                "serial": "fake-serial"
            }

            get_mock.return_value = device_data

            ret = cli.get('/devices/' + dev_id)

            self.assertEqual(ret.json, device_data)
            self.assertEqual(ret.status_code, 200)

            jwt_required_mock.assert_called_once()
            get_mock.assert_called_once_with(dev_id)

    @patch('flask_jwt_extended.view_decorators.verify_jwt_in_request')
    @patch('app.storage.devices.Devices.get')
    @patch('app.storage.devices.Devices.rm')
    def test_del_device_with_existent_device(self, rm_mock, get_mock, \
                                             jwt_required_mock):
        '''
        TODO
        '''
        app = create_app()

        with app.test_client() as cli:
            dev_id = 'fakeid'
            expected_msg = { 'msg': 'Device unregistered from database' }

            get_mock.return_value = {
                "desc": "fake-desc",
                "id": "fake-id",
                "serial": "fake-serial"
            }

            ret = cli.delete('/devices/' + dev_id)

            self.assertEqual(ret.json, expected_msg)
            self.assertEqual(ret.status_code, 200)

            jwt_required_mock.assert_called_once()
            get_mock.assert_called_once_with(dev_id)
            rm_mock.assert_called_once_with(dev_id)

    @patch('flask_jwt_extended.view_decorators.verify_jwt_in_request')
    @patch('app.storage.devices.Devices.get')
    @patch('app.storage.devices.Devices.rm')
    def test_del_device_with_not_existent_device(self, rm_mock, get_mock, \
                                                 jwt_required_mock):
        '''
        TODO
        '''
        app = create_app()

        with app.test_client() as cli:
            dev_id = 'fakeid'
            expected_msg = {
                "msg": "The device isn't registered on database"
            }

            get_mock.return_value = {}

            ret = cli.delete('/devices/' + dev_id)

            self.assertEqual(ret.json, expected_msg)
            self.assertEqual(ret.status_code, 404)

            jwt_required_mock.assert_called_once()
            get_mock.assert_called_once_with(dev_id)
            rm_mock.assert_not_called()

    @patch('random.sample')
    @patch('flask_jwt_extended.view_decorators.verify_jwt_in_request')
    @patch('app.storage.devices.Devices.add')
    def test_register_device(self, add_mock, jwt_required_mock, sample_mock):
        app = create_app()

        with app.test_client() as cli:
            device_id = 'fakeid'
            body = {
                "serial-number": "fake-serial",
                "model": "fake-model",
                "description": "fake desc"
            }
            expected_msg = {
                'msg': 'Device registered with success',
                'id': device_id
            }
            fake_device = Device(
                id=device_id,
                serial=body['serial-number'],
                model=body['model'],
                desc=body['description']
            )

            sample_mock.return_value = device_id

            ret = cli.post('/devices/', json=body)

            self.assertEqual(ret.json, expected_msg)
            self.assertEqual(ret.status_code, 201)

            jwt_required_mock.assert_called_once()
            sample_mock.assert_called_once()
            add_mock.assert_called_once_with(fake_device)

    @patch('flask_jwt_extended.view_decorators.verify_jwt_in_request')
    @patch('app.storage.devices.Devices.add')
    def test_register_device_with_missing_model(self, add_mock, \
                                                jwt_required_mock):
        app = create_app()

        with app.test_client() as cli:
            body = {
                "serial-number": "fake-serial",
                "description": "fake-desc",
            }
            expected_msg = { 'msg': 'Missing required data' }

            ret = cli.post('/devices/', json=body)

            self.assertEqual(ret.json, expected_msg)
            self.assertEqual(ret.status_code, 400)

            jwt_required_mock.assert_called_once()
            add_mock.assert_not_called()

    @patch('flask_jwt_extended.view_decorators.verify_jwt_in_request')
    @patch('app.storage.devices.Devices.add')
    def test_register_device_with_blank_model(self, add_mock, \
                                              jwt_required_mock):
        app = create_app()

        with app.test_client() as cli:
            body = {
                "serial-number": "fake-serial",
                "model": "",
                "description": "fake-desc",
            }
            expected_msg = { 'msg': 'Bad request' }

            ret = cli.post('/devices/', json=body)

            self.assertEqual(ret.json, expected_msg)
            self.assertEqual(ret.status_code, 400)

            jwt_required_mock.assert_called_once()
            add_mock.assert_not_called()

    @patch('flask_jwt_extended.view_decorators.verify_jwt_in_request')
    @patch('app.storage.devices.Devices.add')
    def test_register_device_with_missing_serial(self, add_mock, \
                                                 jwt_required_mock):
        app = create_app()

        with app.test_client() as cli:
            body = {
                "description": "fake desc",
                "model": "fakemodel",
            }
            expected_msg = { 'msg': 'Missing required data' }

            ret = cli.post('/devices/', json=body)

            self.assertEqual(ret.json, expected_msg)
            self.assertEqual(ret.status_code, 400)

            jwt_required_mock.assert_called_once()
            add_mock.assert_not_called()

    @patch('flask_jwt_extended.view_decorators.verify_jwt_in_request')
    @patch('app.storage.devices.Devices.add')
    def test_register_device_with_blank_serial(self, add_mock, \
                                               jwt_required_mock):
        app = create_app()

        with app.test_client() as cli:
            body = {
                "serial-number": "",
                "model": "fakemodel",
                "description": "fake desc"
            }
            expected_msg = { 'msg': 'Bad request' }

            ret = cli.post('/devices/', json=body)

            self.assertEqual(ret.json, expected_msg)
            self.assertEqual(ret.status_code, 400)

            jwt_required_mock.assert_called_once()
            add_mock.assert_not_called()

    @patch('random.sample')
    @patch('flask_jwt_extended.view_decorators.verify_jwt_in_request')
    @patch('app.storage.devices.Devices.add')
    def test_register_device_with_missing_desc(self, add_mock, \
                                               jwt_required_mock, sample_mock):
        app = create_app()

        with app.test_client() as cli:
            device_id = 'fakeid'
            body = {
                "model": "fakemodel",
                "serial-number": "fake-serial",
                "description": "",
            }
            expected_msg = {
                'msg': 'Device registered with success',
                'id': device_id
            }
            fake_device = Device(
                id=device_id,
                serial=body['serial-number'],
                model=body['model'],
                desc=body['description']
            )

            sample_mock.return_value = device_id

            ret = cli.post('/devices/', json=body)

            self.assertEqual(ret.json, expected_msg)
            self.assertEqual(ret.status_code, 201)

            jwt_required_mock.assert_called_once()
            sample_mock.assert_called_once()
            add_mock.assert_called_once()

    @patch('random.sample')
    @patch('flask_jwt_extended.view_decorators.verify_jwt_in_request')
    @patch('app.storage.devices.Devices.add')
    def test_register_device_with_blank_desc(self, add_mock, \
                                             jwt_required_mock, sample_mock):
        app = create_app()

        with app.test_client() as cli:
            device_id = 'fakeid'
            body = {
                "model": "fakemodel",
                "serial-number": "fake-serial",
                "description": "",
            }
            expected_msg = {
                'msg': 'Device registered with success',
                'id': device_id
            }
            fake_device = Device(
                id=device_id,
                serial=body['serial-number'],
                model=body['model'],
                desc=body['description']
            )

            sample_mock.return_value = device_id

            ret = cli.post('/devices/', json=body)

            self.assertEqual(ret.json, expected_msg)
            self.assertEqual(ret.status_code, 201)

            jwt_required_mock.assert_called_once()
            sample_mock.assert_called_once()
            add_mock.assert_called_once()

    @patch('flask_jwt_extended.view_decorators.verify_jwt_in_request')
    @patch('app.storage.devices.Devices.add')
    def test_register_device_with_no_parameters(self, add_mock, \
                                                jwt_required_mock):
        app = create_app()

        with app.test_client() as cli:
            expected_msg = { 'msg': 'Bad request' }

            ret = cli.post('/devices/', json={})

            self.assertEqual(ret.json, expected_msg)
            self.assertEqual(ret.status_code, 400)

            jwt_required_mock.assert_called_once()
            add_mock.assert_not_called()

    @patch('flask_jwt_extended.view_decorators.verify_jwt_in_request')
    @patch('app.storage.devices.Devices.get')
    @patch('app.storage.devices.Devices.update')
    def test_update_not_existent_device(self, update_mock, get_mock, \
                                        jwt_required_mock):
        '''
        TODO
        '''
        app = create_app()

        with app.test_client() as cli:
            dev_id = 'fakeid'
            expected_msg = {
                "msg": "The device isn't registered on database"
            }
            data = { 'param': 'foo-param', 'value': 'foo-value' }

            get_mock.return_value = {}

            ret = cli.put('/devices/' + dev_id, json=data)

            self.assertEqual(ret.json, expected_msg)
            self.assertEqual(ret.status_code, 404)

            jwt_required_mock.assert_called_once()
            get_mock.assert_called_once_with(dev_id)
            update_mock.assert_not_called()

    @patch('flask_jwt_extended.view_decorators.verify_jwt_in_request')
    @patch('app.storage.devices.Devices.get')
    @patch('app.storage.devices.Devices.update')
    def test_update_existent_device(self, update_mock, get_mock, \
                                    jwt_required_mock):
         '''
         TODO
         '''
         app = create_app()

         with app.test_client() as cli:
             dev_id = 'fakeid'
             data = { 'param': 'foo-param', 'value': 'foo-value' }
             expected_msg = { "msg": "Device updated in database" }

             get_mock.return_value = {
                 "device-id": "fake-id",
                 "serial-number": "fake-serial",
                 "description": "fake-desc",
             }

             ret = cli.put('/devices/' + dev_id, json=data)

             self.assertEqual(ret.json, expected_msg)
             self.assertEqual(ret.status_code, 200)

             jwt_required_mock.assert_called_once()
             get_mock.assert_called_once_with(dev_id)
             update_mock.assert_called_once_with(
                 dev_id,
                 data['param'],
                 data['value']
             )

    @patch('app.storage.devices.Devices.get_all')
    def test_get_devices_without_token(self, get_all_mock):
        app = create_app()

        with app.test_client() as cli:
            expected_msg = { 'msg': 'Missing Authorization Header' }
            ret = cli.get('/devices/')

            self.assertEqual(ret.json, expected_msg)
            self.assertEqual(ret.status_code, 401)

            get_all_mock.assert_not_called()

    @patch('app.storage.devices.Devices.get')
    def test_get_device_without_token(self, get_mock):
        app = create_app()

        with app.test_client() as cli:
            dev_id = 'fake_id'
            expected_msg = { 'msg': 'Missing Authorization Header' }

            ret = cli.get('/devices/' + dev_id)

            self.assertEqual(ret.json, expected_msg)
            self.assertEqual(ret.status_code, 401)

            get_mock.assert_not_called()

    @patch('app.storage.devices.Devices.get')
    @patch('app.storage.devices.Devices.rm')
    def test_del_device_without_token(self, rm_mock, get_mock):
        app = create_app()

        with app.test_client() as cli:
            dev_id = 'fake_id'
            expected_msg = { 'msg': 'Missing Authorization Header' }

            ret = cli.delete('/devices/' + dev_id)

            self.assertEqual(ret.json, expected_msg)
            self.assertEqual(ret.status_code, 401)

            get_mock.assert_not_called()
            rm_mock.assert_not_called()

    @patch('app.storage.devices.Devices.add')
    def test_register_device_without_token(self, add_mock):
        app = create_app()

        with app.test_client() as cli:
            body = {
                "model": "fake-model",
                "serial-number": "fake-serial",
                "description": "fake-desc",
            }
            expected_msg = { 'msg': 'Missing Authorization Header' }

            ret = cli.post('/devices/', json=body)

            self.assertEqual(ret.json, expected_msg)
            self.assertEqual(ret.status_code, 401)

            add_mock.assert_not_called()

    @patch('app.storage.devices.Devices.get')
    @patch('app.storage.devices.Devices.update')
    def test_update_device_without_token(self, update_mock, get_mock):
        app = create_app()

        with app.test_client() as cli:
            dev_id = 'fake_id'
            DATA = { 'param': 'foo-param', 'value': 'foo-value' }
            expected_msg = { 'msg': 'Missing Authorization Header' }

            ret = cli.put('/devices/' + dev_id, json=DATA)

            self.assertEqual(ret.json, expected_msg)
            self.assertEqual(ret.status_code, 401)

            get_mock.assert_not_called()
            update_mock.assert_not_called()

if __name__ == "__main__":
    main()
