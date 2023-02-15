from unittest import main, TestCase
from unittest.mock import patch

from app import create_app

class DeviceEndpointTest(TestCase):

    # TODO: remove mocks

    @patch('sg_server.storage.devices.Devices.get_all')
    def test_get_devices_with_empty_db(self, get_all_mock):
        app = create_app()

        with app.test_client() as cli:
            get_all_mock.return_value = ''

            ret = cli.get('/devices/')

            self.assertEqual(ret.json, '')
            self.assertEqual(ret.status_code, 200)

            get_all_mock.assert_called_once()

    @patch('sg_server.storage.devices.Devices.get_all')
    def test_get_devices_with_not_empty_db(self, get_all_mock):
        app = create_app()

        with app.test_client() as cli:
            DEVICES = '''
                [
                    {
                      "desc": "foo-desc",
                      "group": "foo-group",
                      "id": "foo-id",
                      "serial": "foo-serial"
                    },
                    {
                      "desc": "bar-desc",
                      "group": "bar-group",
                      "id": "bar-id",
                      "serial": "bar-serial"
                    },
                ]

            '''

            get_all_mock.return_value = DEVICES

            ret = cli.get('/devices/')

            self.assertEqual(ret.json, DEVICES)
            self.assertEqual(ret.status_code, 200)

            get_all_mock.assert_called_once()

    @patch('sg_server.storage.devices.Devices.get')
    def test_get_device_with_not_existent_device(self, get_mock):
        app = create_app()

        with app.test_client() as cli:
            DEV_ID = 'foo_id'
            EXPECTED_ERROR = {
                "message": "the device isn't registered on database!"
            }

            get_mock.return_value = {}

            ret = cli.get('/devices/' + DEV_ID)

            self.assertEqual(ret.json, EXPECTED_ERROR)
            self.assertEqual(ret.status_code, 404)

            get_mock.assert_called_once_with(DEV_ID)

    @patch('sg_server.storage.devices.Devices.get')
    def test_get_device_with_existent_device(self, get_mock):
        app = create_app()

        with app.test_client() as cli:
            DEV_ID = 'fake_id'
            DEVICE_DATA = {
                "desc": "fake-desc",
                "group": "fake-group",
                "id": "fake-id",
                "serial": "fake-serial"
            }

            get_mock.return_value = DEVICE_DATA

            ret = cli.get('/devices/' + DEV_ID)

            self.assertEqual(ret.json, DEVICE_DATA)
            self.assertEqual(ret.status_code, 200)

            get_mock.assert_called_once_with(DEV_ID)

    @patch('sg_server.storage.devices.Devices.get')
    @patch('sg_server.storage.devices.Devices.rm')
    def test_del_device_with_existent_device(self, rm_mock, get_mock):
        app = create_app()

        with app.test_client() as cli:
            DEV_ID = 'fake_id'
            EXPECTED_MSG = { 'message': 'device unregistered from database!' }

            get_mock.return_value = {
                "desc": "fake-desc",
                "group": "fake-group",
                "id": "fake-id",
                "serial": "fake-serial"
            }

            ret = cli.delete('/devices/' + DEV_ID)

            self.assertEqual(ret.json, EXPECTED_MSG)
            self.assertEqual(ret.status_code, 200)

            get_mock.assert_called_once_with(DEV_ID)
            rm_mock.assert_called_once()

    @patch('sg_server.storage.devices.Devices.get')
    @patch('sg_server.storage.devices.Devices.rm')
    def test_del_device_with_not_existent_device(self, rm_mock, get_mock):
        app = create_app()

        with app.test_client() as cli:
            DEV_ID = 'fake_id'
            EXPECTED_MSG = {
                "message": "the device isn't registered on database!"
            }

            get_mock.return_value = {}

            ret = cli.delete('/devices/' + DEV_ID)

            self.assertEqual(ret.json, EXPECTED_MSG)
            self.assertEqual(ret.status_code, 404)

            get_mock.assert_called_once_with(DEV_ID)
            rm_mock.assert_not_called()

    @patch('sg_server.storage.devices.Devices.add')
    def test_register_device(self, add_mock):
        app = create_app()

        with app.test_client() as cli:
            BODY = {
                "device-id": "fake-id",
                "serial-number": "fake-serial",
                "description": "fake-desc",
                "group": "fake-group"
            }
            EXPECTED_MSG = { 'message': 'device registered with success!' }

            ret = cli.post('/devices/', json=BODY)

            self.assertEqual(ret.json, EXPECTED_MSG)
            self.assertEqual(ret.status_code, 201)

            add_mock.assert_called_once()

    @patch('sg_server.storage.devices.Devices.add')
    def test_register_device_with_missing_id(self, add_mock):
        app = create_app()

        with app.test_client() as cli:
            BODY = {
                "serial-number": "fake-serial",
                "description": "fake-desc",
                "group": "fake-group"
            }
            EXPECTED_MSG = { 'message': 'bad request!' }

            ret = cli.post('/devices/', json=BODY)

            self.assertEqual(ret.json, EXPECTED_MSG)
            self.assertEqual(ret.status_code, 400)

            add_mock.assert_not_called()

    @patch('sg_server.storage.devices.Devices.add')
    def test_register_device_with_blank_id(self, add_mock):
        app = create_app()

        with app.test_client() as cli:
            BODY = {
                "device-id": "",
                "serial-number": "fake-serial",
                "description": "fake-desc",
                "group": "fake-group"
            }
            EXPECTED_MSG = { 'message': 'bad request!' }

            ret = cli.post('/devices/', json=BODY)

            self.assertEqual(ret.json, EXPECTED_MSG)
            self.assertEqual(ret.status_code, 400)

            add_mock.assert_not_called()

    @patch('sg_server.storage.devices.Devices.add')
    def test_register_device_with_missing_serial(self, add_mock):
        app = create_app()

        with app.test_client() as cli:
            BODY = {
                "device-id": "fake-id",
                "description": "fake-desc",
                "group": "fake-group"
            }
            EXPECTED_MSG = { 'message': 'bad request!' }

            ret = cli.post('/devices/', json=BODY)

            self.assertEqual(ret.json, EXPECTED_MSG)
            self.assertEqual(ret.status_code, 400)

            add_mock.assert_not_called()

    @patch('sg_server.storage.devices.Devices.add')
    def test_register_device_with_blank_serial(self, add_mock):
        app = create_app()

        with app.test_client() as cli:
            BODY = {
                "device-id": "fake-id",
                "serial-number": "",
                "description": "fake-desc",
                "group": "fake-group"
            }
            EXPECTED_MSG = { 'message': 'bad request!' }

            ret = cli.post('/devices/', json=BODY)

            self.assertEqual(ret.json, EXPECTED_MSG)
            self.assertEqual(ret.status_code, 400)

            add_mock.assert_not_called()

    @patch('sg_server.storage.devices.Devices.add')
    def test_register_device_with_missing_desc(self, add_mock):
        app = create_app()

        with app.test_client() as cli:
            BODY = {
                "device-id": "fake-id",
                "serial-number": "fake-serial",
                "group": "fake-group"
            }
            EXPECTED_MSG = { 'message': 'device registered with success!' }

            ret = cli.post('/devices/', json=BODY)

            self.assertEqual(ret.json, EXPECTED_MSG)
            self.assertEqual(ret.status_code, 201)

            add_mock.assert_called_once()

    @patch('sg_server.storage.devices.Devices.add')
    def test_register_device_with_blank_desc(self, add_mock):
        app = create_app()

        with app.test_client() as cli:
            BODY = {
                "device-id": "fake-id",
                "serial-number": "fake-serial",
                "description": "",
                "group": "fake-group"
            }
            EXPECTED_MSG = { 'message': 'device registered with success!' }

            ret = cli.post('/devices/', json=BODY)

            self.assertEqual(ret.json, EXPECTED_MSG)
            self.assertEqual(ret.status_code, 201)

            add_mock.assert_called_once()

    @patch('sg_server.storage.devices.Devices.add')
    def test_register_device_with_missing_group(self, add_mock):
        app = create_app()

        with app.test_client() as cli:
            BODY = {
                "device-id": "fake-id",
                "serial-number": "fake-serial",
                "description": "fake-desc",
            }
            EXPECTED_MSG = { 'message': 'bad request!' }

            ret = cli.post('/devices/', json=BODY)

            self.assertEqual(ret.json, EXPECTED_MSG)
            self.assertEqual(ret.status_code, 400)

            add_mock.assert_not_called()

    @patch('sg_server.storage.devices.Devices.add')
    def test_register_device_with_blank_group(self, add_mock):
        app = create_app()

        with app.test_client() as cli:
            BODY = {
                "device-id": "fake-id",
                "serial-number": "fake-serial",
                "description": "fake-desc",
                "group": ""
            }
            EXPECTED_MSG = { 'message': 'bad request!' }

            ret = cli.post('/devices/', json=BODY)

            self.assertEqual(ret.json, EXPECTED_MSG)
            self.assertEqual(ret.status_code, 400)

            add_mock.assert_not_called()

    @patch('sg_server.storage.devices.Devices.add')
    def test_register_device_with_no_parameters(self, add_mock):
        app = create_app()

        with app.test_client() as cli:
            EXPECTED_MSG = { 'message': 'bad request!' }

            ret = cli.post('/devices/', json={})

            self.assertEqual(ret.json, EXPECTED_MSG)
            self.assertEqual(ret.status_code, 400)

            add_mock.assert_not_called()

    @patch('sg_server.storage.devices.Devices.get')
    @patch('sg_server.storage.devices.Devices.update')
    def test_update_not_existent_device(self, update_mock, get_mock):
        app = create_app()

        with app.test_client() as cli:
            DEV_ID = 'fake_id'
            EXPECTED_MSG = {
                "message": "the device isn't registered on database!"
            }

            get_mock.return_value = {}

            ret = cli.put('/devices/' + DEV_ID)

            self.assertEqual(ret.json, EXPECTED_MSG)
            self.assertEqual(ret.status_code, 404)

            get_mock.assert_called_once_with(DEV_ID)
            update_mock.assert_not_called()

    @patch('sg_server.storage.devices.Devices.get')
    @patch('sg_server.storage.devices.Devices.update')
    def test_update_existent_device(self, update_mock, get_mock):
        app = create_app()

        with app.test_client() as cli:
            DEV_ID = 'fake_id'
            DATA = { 'param': 'foo-param', 'value': 'foo-value' }
            EXPECTED_MSG = { "message": "device updated in database!" }

            get_mock.return_value = {
                "device-id": "fake-id",
                "serial-number": "",
                "description": "fake-desc",
                "group": "fake-group"
            }

            ret = cli.put('/devices/' + DEV_ID, json=DATA)

            self.assertEqual(ret.json, EXPECTED_MSG)
            self.assertEqual(ret.status_code, 200)

            get_mock.assert_called_once_with(DEV_ID)
            update_mock.assert_called_once_with(
                DEV_ID,
                DATA['param'],
                DATA['value']
            )

if __name__ == "__main__":
    main()
