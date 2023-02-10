from unittest import main, TestCase
from unittest.mock import patch

from sg_server import create_app

class DeviceEndpointTest(TestCase):

    # TODO: remove mocks

    @patch('app.storage.devices.Devices.get_all')
    def test_get_devices_with_empty_db(self, get_all_mock):
        app = create_app()

        with app.test_client() as cli:
            get_all_mock.return_value = ''

            ret = cli.get('/devices/')

            self.assertEqual(ret.json, '')
            self.assertEqual(ret.status_code, 200)

            get_all_mock.assert_called_once()

    @patch('app.storage.devices.Devices.get_all')
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

    @patch('app.storage.devices.Devices.get')
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

    @patch('app.storage.devices.Devices.get')
    def test_get_device_with_existent_device(self, get_mock):
        app = create_app()

        with app.test_client() as cli:
            DEV_ID = 'foo_id'
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

    @patch('app.storage.devices.Devices.get')
    @patch('app.storage.devices.Devices.rm')
    def test_del_device_with_existent_device(self, rm_mock, get_mock):
        app = create_app()

        with app.test_client() as cli:
            DEV_ID = 'foo_id'
            DEVICE_DATA = {
                "desc": "fake-desc",
                "group": "fake-group",
                "id": "fake-id",
                "serial": "fake-serial"
            }
            EXPECTED_MSG = {
                'message': 'device unregistered from database!'
            }

            get_mock.return_value = DEVICE_DATA

            ret = cli.delete('/devices/' + DEV_ID)

            self.assertEqual(ret.json, EXPECTED_MSG)
            self.assertEqual(ret.status_code, 200)

            get_mock.assert_called_once_with(DEV_ID)
            rm_mock.assert_called_once()

    @patch('app.storage.devices.Devices.get')
    @patch('app.storage.devices.Devices.rm')
    def test_del_device_with_not_existent_device(self, rm_mock, get_mock):
        app = create_app()

        with app.test_client() as cli:
            DEV_ID = 'foo_id'
            EXPECTED_MSG = {
                "message": "the device isn't registered on database!"
            }

            rm_mock.return_value = {}
            get_mock.return_value = None

            ret = cli.delete('/devices/' + DEV_ID)

            self.assertEqual(ret.json, EXPECTED_MSG)
            self.assertEqual(ret.status_code, 404)

            get_mock.assert_called_once_with(DEV_ID)
            rm_mock.assert_not_called()

    #@patch('app.storage.devices.Devices.get')
    #def test_get_device_with_no_device_id(self, get_mock):
    #    app = create_app()

    #    get_mock.return_value = {}

    #    with app.test_client() as cli:
    #        EXPECTED_ERROR = {
    #            "message": "bad request!"
    #        }

    #        ret = cli.get('/devices/')

    #        self.assertEqual(ret.json, EXPECTED_ERROR)
    #        self.assertEqual(ret.status_code, 400)

    #        get_mock.assert_called_once()

if __name__ == "__main__":
    main()
