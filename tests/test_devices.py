from unittest import main, TestCase
from unittest.mock import patch

from flask_jwt_extended import create_access_token

from models.entities.device import Device
from run import create_app


class DeviceEndpointTest(TestCase):

    '''
    Unit tests of /devices/<id> endpoint.

    '''

    @patch('flask_jwt_extended.view_decorators.verify_jwt_in_request')
    @patch('models.device_handler.DeviceHandler.get_all')
    @patch('models.database_mgr.DatabaseMgr.init_db')
    def test_get_devices_with_empty_db(self, init_db_mock, get_all_mock, \
                                       jwt_required_mock):
        '''
        TODO
        '''
        app = create_app()

        with app.test_client() as cli:
            get_all_mock.return_value = []

            ret = cli.get('/devices/')

            self.assertEqual(ret.json, [])
            self.assertEqual(ret.status_code, 200)

            jwt_required_mock.assert_called_once()
            get_all_mock.assert_called_once()

    @patch('flask_jwt_extended.view_decorators.verify_jwt_in_request')
    @patch('models.device_handler.DeviceHandler.get_all')
    @patch('models.database_mgr.DatabaseMgr.init_db')
    def test_get_devices_with_not_empty_db(self, init_db_mock, get_all_mock, \
                                           jwt_required_mock):
        '''
        TODO
        '''
        app = create_app()

        with app.test_client() as cli:
            devices = [
                Device(id='foo-id', serial='foo-serial', model='foo-model',
                       desc='foo-desc'),
                Device(id='bar-id', serial='bar-serial', model='bar-model',
                       desc='bar-desc')
            ]

            get_all_mock.return_value = devices

            ret = cli.get('/devices/')

            self.assertEqual(ret.json, [dev.__dict__ for dev in devices])
            self.assertEqual(ret.status_code, 200)

            jwt_required_mock.assert_called_once()
            get_all_mock.assert_called_once()

    @patch('flask_jwt_extended.view_decorators.verify_jwt_in_request')
    @patch('models.device_handler.DeviceHandler.get')
    @patch('models.database_mgr.DatabaseMgr.init_db')
    def test_get_device_with_not_existent_device(self, init_db_mock, get_mock, \
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

            get_mock.return_value = None

            ret = cli.get('/devices/' + dev_id)

            self.assertEqual(ret.json, expected_error)
            self.assertEqual(ret.status_code, 404)

            jwt_required_mock.assert_called_once()
            get_mock.assert_called_once_with(dev_id)

    @patch('flask_jwt_extended.view_decorators.verify_jwt_in_request')
    @patch('models.device_handler.DeviceHandler.get')
    @patch('models.database_mgr.DatabaseMgr.init_db')
    def test_get_device_with_existent_device(self, init_db_mock, get_mock, \
                                             jwt_required_mock):
        '''
        TODO
        '''
        app = create_app()

        with app.test_client() as cli:
            dev_id = 'fakeid'
            dev = Device(id='fake-id', serial='fake-serial', model='fake-model',
                         desc='fake-desc')

            get_mock.return_value = dev

            ret = cli.get('/devices/' + dev_id)

            self.assertEqual(ret.json, dev.__dict__)
            self.assertEqual(ret.status_code, 200)

            jwt_required_mock.assert_called_once()
            get_mock.assert_called_once_with(dev_id)

    @patch('flask_jwt_extended.view_decorators.verify_jwt_in_request')
    @patch('models.device_handler.DeviceHandler.entry_exists')
    @patch('models.device_handler.DeviceHandler.delete')
    @patch('models.database_mgr.DatabaseMgr.init_db')
    def test_del_device_with_existent_device(self, init_db_mock, delete_mock, \
                                             exists_mock, jwt_required_mock):
        '''
        TODO
        '''
        app = create_app()

        with app.test_client() as cli:
            dev_id = 'fakeid'
            expected_msg = { 'msg': 'Device unregistered from database' }
            dev = Device(id=dev_id, serial='fake-serial', model='fake-model',
                         desc='fake-desc')

            exists_mock.return_value = dev

            ret = cli.delete('/devices/' + dev_id)

            self.assertEqual(ret.json, expected_msg)
            self.assertEqual(ret.status_code, 200)

            jwt_required_mock.assert_called_once()
            exists_mock.assert_called_once_with(dev_id)
            delete_mock.assert_called_once_with(dev_id)

    @patch('flask_jwt_extended.view_decorators.verify_jwt_in_request')
    @patch('models.device_handler.DeviceHandler.entry_exists')
    @patch('models.device_handler.DeviceHandler.delete')
    @patch('models.database_mgr.DatabaseMgr.init_db')
    def test_del_device_with_not_existent_device(self, init_db_mock, \
                                                 delete_mock, exists_mock, \
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

            exists_mock.return_value = False

            ret = cli.delete('/devices/' + dev_id)

            self.assertEqual(ret.json, expected_msg)
            self.assertEqual(ret.status_code, 404)

            jwt_required_mock.assert_called_once()
            exists_mock.assert_called_once_with(dev_id)
            delete_mock.assert_not_called()

    @patch('flask_jwt_extended.view_decorators.verify_jwt_in_request')
    @patch('models.device_handler.DeviceHandler.insert')
    @patch('models.database_mgr.DatabaseMgr.init_db')
    def test_register_device(self, init_db_mock, insert_mock, \
                             jwt_required_mock):
        '''
        TODO
        '''
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
                id='',
                serial=body['serial-number'],
                model=body['model'],
                desc=body['description']
            )

            insert_mock.return_value = device_id

            ret = cli.post('/devices/', json=body)

            self.assertEqual(ret.json, expected_msg)
            self.assertEqual(ret.status_code, 201)

            jwt_required_mock.assert_called_once()
            insert_mock.assert_called_once_with(fake_device)

    @patch('flask_jwt_extended.view_decorators.verify_jwt_in_request')
    @patch('models.device_handler.DeviceHandler.insert')
    @patch('models.database_mgr.DatabaseMgr.init_db')
    def test_register_device_with_missing_model(self, init_db_mock, \
                                                insert_mock, \
                                                jwt_required_mock):
        '''
        TODO
        '''
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
            insert_mock.assert_not_called()

    @patch('flask_jwt_extended.view_decorators.verify_jwt_in_request')
    @patch('models.device_handler.DeviceHandler.insert')
    @patch('models.database_mgr.DatabaseMgr.init_db')
    def test_register_device_with_blank_model(self, init_db_mock, insert_mock, \
                                              jwt_required_mock):
        '''
        TODO
        '''
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
            insert_mock.assert_not_called()

    @patch('flask_jwt_extended.view_decorators.verify_jwt_in_request')
    @patch('models.device_handler.DeviceHandler.insert')
    @patch('models.database_mgr.DatabaseMgr.init_db')
    def test_register_device_with_missing_serial(self, init_db_mock, \
                                                 insert_mock, \
                                                 jwt_required_mock):
        '''
        TODO
        '''
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
            insert_mock.assert_not_called()

    @patch('flask_jwt_extended.view_decorators.verify_jwt_in_request')
    @patch('models.device_handler.DeviceHandler.insert')
    @patch('models.database_mgr.DatabaseMgr.init_db')
    def test_register_device_with_blank_serial(self, init_db_mock, \
                                               insert_mock, jwt_required_mock):
        '''
        TODO
        '''
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
            insert_mock.assert_not_called()

    @patch('flask_jwt_extended.view_decorators.verify_jwt_in_request')
    @patch('models.device_handler.DeviceHandler.insert')
    @patch('models.database_mgr.DatabaseMgr.init_db')
    def test_register_device_with_missing_desc(self, init_db_mock, \
                                               insert_mock, \
                                               jwt_required_mock):
        '''
        TODO
        '''
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
                id='',
                serial=body['serial-number'],
                model=body['model'],
                desc=body['description']
            )

            insert_mock.return_value = device_id

            ret = cli.post('/devices/', json=body)

            self.assertEqual(ret.json, expected_msg)
            self.assertEqual(ret.status_code, 201)

            jwt_required_mock.assert_called_once()
            insert_mock.assert_called_once_with(fake_device)

    @patch('flask_jwt_extended.view_decorators.verify_jwt_in_request')
    @patch('models.device_handler.DeviceHandler.insert')
    @patch('models.database_mgr.DatabaseMgr.init_db')
    def test_register_device_with_blank_desc(self, init_db_mock, insert_mock, \
                                             jwt_required_mock):
        '''
        TODO
        '''
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
                id='',
                serial=body['serial-number'],
                model=body['model'],
                desc=body['description']
            )

            insert_mock.return_value = device_id

            ret = cli.post('/devices/', json=body)

            self.assertEqual(ret.json, expected_msg)
            self.assertEqual(ret.status_code, 201)

            jwt_required_mock.assert_called_once()
            insert_mock.assert_called_once_with(fake_device)

    @patch('flask_jwt_extended.view_decorators.verify_jwt_in_request')
    @patch('models.device_handler.DeviceHandler.insert')
    @patch('models.database_mgr.DatabaseMgr.init_db')
    def test_register_device_with_no_parameters(self, init_db_mock, \
                                                insert_mock, \
                                                jwt_required_mock):
        '''
        TODO
        '''
        app = create_app()

        with app.test_client() as cli:
            expected_msg = { 'msg': 'Bad request' }

            ret = cli.post('/devices/', json={})

            self.assertEqual(ret.json, expected_msg)
            self.assertEqual(ret.status_code, 400)

            jwt_required_mock.assert_called_once()
            insert_mock.assert_not_called()

    @patch('flask_jwt_extended.view_decorators.verify_jwt_in_request')
    @patch('models.device_handler.DeviceHandler.entry_exists')
    @patch('models.device_handler.DeviceHandler.update')
    @patch('models.database_mgr.DatabaseMgr.init_db')
    def test_update_not_existent_device(self, init_db_mock, update_mock, \
                                        exists_mock, jwt_required_mock):
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

            exists_mock.return_value = {}

            ret = cli.put('/devices/' + dev_id, json=data)

            self.assertEqual(ret.json, expected_msg)
            self.assertEqual(ret.status_code, 404)

            jwt_required_mock.assert_called_once()
            exists_mock.assert_called_once_with(dev_id)
            update_mock.assert_not_called()

    @patch('flask_jwt_extended.view_decorators.verify_jwt_in_request')
    @patch('models.device_handler.DeviceHandler.entry_exists')
    @patch('models.device_handler.DeviceHandler.update')
    @patch('models.database_mgr.DatabaseMgr.init_db')
    def test_update_existent_device(self, init_db_mock, update_mock, \
                                    exists_mock, jwt_required_mock):
         '''
         TODO
         '''
         app = create_app()

         with app.test_client() as cli:
             dev_id = 'fakeid'
             data = { 'param': 'foo-param', 'value': 'foo-value' }
             expected_msg = { "msg": "Device updated in database" }

             exists_mock.return_value = True

             ret = cli.put('/devices/' + dev_id, json=data)

             self.assertEqual(ret.json, expected_msg)
             self.assertEqual(ret.status_code, 200)

             jwt_required_mock.assert_called_once()
             exists_mock.assert_called_once_with(dev_id)
             update_mock.assert_called_once_with(dev_id, data['param'],
                                                 data['value'])

    @patch('models.device_handler.DeviceHandler.get_all')
    @patch('models.database_mgr.DatabaseMgr.init_db')
    def test_get_devices_without_token(self, init_db_mock, get_all_mock):
        '''
        TODO
        '''
        app = create_app()

        with app.test_client() as cli:
            expected_msg = { 'msg': 'Missing Authorization Header' }
            ret = cli.get('/devices/')

            self.assertEqual(ret.json, expected_msg)
            self.assertEqual(ret.status_code, 401)

            get_all_mock.assert_not_called()

    @patch('models.device_handler.DeviceHandler.get')
    @patch('models.database_mgr.DatabaseMgr.init_db')
    def test_get_device_without_token(self, init_db_mock, get_mock):
        '''
        TODO
        '''
        app = create_app()

        with app.test_client() as cli:
            dev_id = 'fake_id'
            expected_msg = { 'msg': 'Missing Authorization Header' }

            ret = cli.get('/devices/' + dev_id)

            self.assertEqual(ret.json, expected_msg)
            self.assertEqual(ret.status_code, 401)

            get_mock.assert_not_called()

    @patch('models.device_handler.DeviceHandler.entry_exists')
    @patch('models.device_handler.DeviceHandler.delete')
    @patch('models.database_mgr.DatabaseMgr.init_db')
    def test_del_device_without_token(self, init_db_mock, delete_mock, \
                                      exists_mock):
        '''
        TODO
        '''
        app = create_app()

        with app.test_client() as cli:
            dev_id = 'fake_id'
            expected_msg = { 'msg': 'Missing Authorization Header' }

            ret = cli.delete('/devices/' + dev_id)

            self.assertEqual(ret.json, expected_msg)
            self.assertEqual(ret.status_code, 401)

            exists_mock.assert_not_called()
            delete_mock.assert_not_called()

    @patch('models.device_handler.DeviceHandler.insert')
    @patch('models.database_mgr.DatabaseMgr.init_db')
    def test_register_device_without_token(self, init_db_mock, insert_mock):
        '''
        TODO
        '''
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

            insert_mock.assert_not_called()

    @patch('models.device_handler.DeviceHandler.entry_exists')
    @patch('models.device_handler.DeviceHandler.update')
    @patch('models.database_mgr.DatabaseMgr.init_db')
    def test_update_device_without_token(self, init_db_mock, update_mock, \
                                         exists_mock):
        '''
        TODO
        '''
        app = create_app()

        with app.test_client() as cli:
            dev_id = 'fake_id'
            data = { 'param': 'foo-param', 'value': 'foo-value' }
            expected_msg = { 'msg': 'Missing Authorization Header' }

            ret = cli.put('/devices/' + dev_id, json=data)

            self.assertEqual(ret.json, expected_msg)
            self.assertEqual(ret.status_code, 401)

            exists_mock.assert_not_called()
            update_mock.assert_not_called()


if __name__ == "__main__":
    main()
