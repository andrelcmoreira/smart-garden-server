from unittest import main, TestCase
from unittest.mock import patch

from run import create_app

from models.config_handler import ConfigHandler
from models.entities.config import Config


class DeviceConfigEndpointTest(TestCase):

    '''
    Unit tests of /device/<id>/config endpoint.

    '''

    @patch('flask_jwt_extended.view_decorators.verify_jwt_in_request')
    @patch('models.config_handler.ConfigHandler.get_all')
    @patch('models.database_mgr.DatabaseMgr.init_db')
    def test_get_configs_with_empty_db(self, _, get_all_mock, \
                                       jwt_required_mock):
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
    @patch('models.config_handler.ConfigHandler.get_all')
    @patch('models.database_mgr.DatabaseMgr.init_db')
    def test_get_configs_with_not_empty_db(self, _, get_all_mock, \
                                           jwt_required_mock):
        '''
        TODO
        '''
        app = create_app()

        with app.test_client() as cli:
            configs = [
                Config(id='fakeid', group="fake-group", interval="10"),
                Config(id='fakeid', group='fake-group', interval='20')
            ]

            get_all_mock.return_value = configs

            ret = cli.get('/devices/config/')

            self.assertEqual(ret.json, [cfg.__dict__ for cfg in configs])
            self.assertEqual(ret.status_code, 200)

            jwt_required_mock.assert_called_once()
            get_all_mock.assert_called_once()

    @patch('flask_jwt_extended.view_decorators.verify_jwt_in_request')
    @patch('models.config_handler.ConfigHandler.get')
    @patch('models.database_mgr.DatabaseMgr.init_db')
    def test_get_config_with_not_existent_config(self, _, get_mock, \
                                                 jwt_required_mock):
        '''
        TODO
        '''
        app = create_app()

        with app.test_client() as cli:
            dev_id = 'fakeid'
            expected_error = {
                "msg": "The device has no configuration"
            }

            get_mock.return_value = None

            ret = cli.get(f'/devices/{dev_id}/config/')

            self.assertEqual(ret.json, expected_error)
            self.assertEqual(ret.status_code, 404)

            jwt_required_mock.assert_called_once()
            get_mock.assert_called_once_with(dev_id)

    @patch('flask_jwt_extended.view_decorators.verify_jwt_in_request')
    @patch('models.config_handler.ConfigHandler.get')
    @patch('models.database_mgr.DatabaseMgr.init_db')
    def test_get_config_with_existent_config(self, _, get_mock, \
                                             jwt_required_mock):
        '''
        TODO
        '''
        app = create_app()

        with app.test_client() as cli:
            cfg = Config(id='fakeid', interval="10", group="fake-group")

            get_mock.return_value = cfg

            ret = cli.get(f'/devices/{cfg.id}/config/')

            self.assertEqual(ret.json, cfg.__dict__)
            self.assertEqual(ret.status_code, 200)

            jwt_required_mock.assert_called_once()
            get_mock.assert_called_once_with(cfg.id)

    @patch('flask_jwt_extended.view_decorators.verify_jwt_in_request')
    @patch('models.config_handler.ConfigHandler.entry_exists')
    @patch('models.config_handler.ConfigHandler.delete')
    @patch('models.database_mgr.DatabaseMgr.init_db')
    def test_del_config_with_existent_config(self, _, delete_mock, \
                                             exists_mock, jwt_required_mock):
        '''
        TODO
        '''
        app = create_app()

        with app.test_client() as cli:
            dev_id = 'fakeid'
            expected_msg = { 'msg': 'Config deleted from database' }

            exists_mock.return_value = True

            ret = cli.delete(f'/devices/{dev_id}/config/')

            self.assertEqual(ret.json, expected_msg)
            self.assertEqual(ret.status_code, 200)

            jwt_required_mock.assert_called_once()
            exists_mock.assert_called_once_with(dev_id)
            delete_mock.assert_called_once_with(dev_id)

    @patch('flask_jwt_extended.view_decorators.verify_jwt_in_request')
    @patch('models.config_handler.ConfigHandler.entry_exists')
    @patch('models.config_handler.ConfigHandler.delete')
    @patch('models.database_mgr.DatabaseMgr.init_db')
    def test_del_config_with_not_existent_config(self, _, delete_mock, \
                                                 exists_mock, \
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

            exists_mock.return_value = False

            ret = cli.delete(f'/devices/{dev_id}/config/')

            self.assertEqual(ret.json, expected_msg)
            self.assertEqual(ret.status_code, 404)

            jwt_required_mock.assert_called_once()
            exists_mock.assert_called_once_with(dev_id)
            delete_mock.assert_not_called()

    @patch('flask_jwt_extended.view_decorators.verify_jwt_in_request')
    @patch('models.device_handler.DeviceHandler.entry_exists')
    @patch('models.config_handler.ConfigHandler.insert')
    @patch('models.database_mgr.DatabaseMgr.init_db')
    def test_register_config(self, _, insert_mock, entry_exists_mock, \
                             jwt_required_mock):
        '''
        TODO
        '''
        app = create_app()

        with app.test_client() as cli:
            cfg = Config(id='fakeid', group='fakegroup', interval='10')
            request = { 'group': cfg.group, 'interval': cfg.interval }
            expected_msg = { 'msg': 'Configuration registered with success' }

            entry_exists_mock.return_value = True

            ret = cli.post(f'/devices/{cfg.id}/config/', json=request)

            self.assertEqual(ret.json, expected_msg)
            self.assertEqual(ret.status_code, 201)

            jwt_required_mock.assert_called_once()
            entry_exists_mock.assert_called_once_with(cfg.id)
            insert_mock.assert_called_once_with(cfg)

    @patch('flask_jwt_extended.view_decorators.verify_jwt_in_request')
    @patch('models.device_handler.DeviceHandler.entry_exists')
    @patch('models.config_handler.ConfigHandler.insert')
    @patch('models.database_mgr.DatabaseMgr.init_db')
    def test_register_cfg_with_missing_interval(self, _, insert_mock, \
                                                exists_mock, \
                                                jwt_required_mock):
        '''
        TODO
        '''
        app = create_app()

        with app.test_client() as cli:
            dev_id = 'fakeid'
            request = { 'group': 'fakegroup' }
            expected_msg = { 'msg': 'Missing required data' }

            ret = cli.post(f'/devices/{dev_id}/config/', json=request)

            self.assertEqual(ret.json, expected_msg)
            self.assertEqual(ret.status_code, 400)

            jwt_required_mock.assert_called_once()
            exists_mock.assert_not_called()
            insert_mock.assert_not_called()

    @patch('flask_jwt_extended.view_decorators.verify_jwt_in_request')
    @patch('models.device_handler.DeviceHandler.entry_exists')
    @patch('models.config_handler.ConfigHandler.insert')
    @patch('models.database_mgr.DatabaseMgr.init_db')
    def test_register_device_with_missing_group(self, _, insert_mock, \
                                                exists_mock, \
                                                jwt_required_mock):
        '''
        TODO
        '''
        app = create_app()

        with app.test_client() as cli:
            cfg = Config(id='fakeid', group=None, interval='10')
            request = { "interval": cfg.interval }
            expected_msg = { 'msg': 'Configuration registered with success' }

            exists_mock.return_value = True

            ret = cli.post(f'/devices/{cfg.id}/config/', json=request)

            self.assertEqual(ret.json, expected_msg)
            self.assertEqual(ret.status_code, 201)

            jwt_required_mock.assert_called_once()
            exists_mock.assert_called_once_with(cfg.id)
            insert_mock.assert_called_once_with(cfg)

    @patch('flask_jwt_extended.view_decorators.verify_jwt_in_request')
    @patch('models.config_handler.ConfigHandler.insert')
    @patch('models.database_mgr.DatabaseMgr.init_db')
    def test_register_config_with_no_parameters(self, _, insert_mock, \
                                                jwt_required_mock):
        '''
        TODO
        '''
        app = create_app()

        with app.test_client() as cli:
            dev_id = 'fakeid'
            expected_msg = { 'msg': 'Bad request' }

            ret = cli.post(f'/devices/{dev_id}/config/', json={})

            self.assertEqual(ret.json, expected_msg)
            self.assertEqual(ret.status_code, 400)

            jwt_required_mock.assert_called_once()
            insert_mock.assert_not_called()

    @patch('flask_jwt_extended.view_decorators.verify_jwt_in_request')
    @patch('models.config_handler.ConfigHandler.entry_exists')
    @patch('models.config_handler.ConfigHandler.update')
    @patch('models.database_mgr.DatabaseMgr.init_db')
    def test_update_not_existent_config(self, _, update_mock, \
                                        exists_mock, jwt_required_mock):
        '''
        TODO
        '''
        app = create_app()

        with app.test_client() as cli:
            dev_id = 'fakeid'
            expected_msg = {
                "msg": "There's no config for the specific device"
            }
            request = { 'param': 'foo-param', 'value': 'foo-value' }

            exists_mock.return_value = False

            ret = cli.put(f'/devices/{dev_id}/config/', json=request)

            self.assertEqual(ret.json, expected_msg)
            self.assertEqual(ret.status_code, 404)

            jwt_required_mock.assert_called_once()
            exists_mock.assert_called_once_with(dev_id)
            update_mock.assert_not_called()

    @patch('flask_jwt_extended.view_decorators.verify_jwt_in_request')
    @patch('models.config_handler.ConfigHandler.entry_exists')
    @patch('models.config_handler.ConfigHandler.update')
    @patch('models.database_mgr.DatabaseMgr.init_db')
    def test_update_existent_config(self, _, update_mock, exists_mock, \
                                    jwt_required_mock):
         '''
         TODO
         '''
         app = create_app()

         with app.test_client() as cli:
             dev_id = 'fakeid'
             request = { 'param': 'foo-param', 'value': 'foo-value' }
             expected_msg = { "msg": "Config updated in database" }

             exists_mock.return_value = True

             ret = cli.put(f'/devices/{dev_id}/config/', json=request)

             self.assertEqual(ret.json, expected_msg)
             self.assertEqual(ret.status_code, 200)

             jwt_required_mock.assert_called_once()
             exists_mock.assert_called_once_with(dev_id)
             update_mock.assert_called_once_with(dev_id, request['param'],
                                                 request['value'])

    @patch('models.config_handler.ConfigHandler.get_all')
    @patch('models.database_mgr.DatabaseMgr.init_db')
    def test_get_config_without_token(self, _, get_all_mock):
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

    @patch('models.config_handler.ConfigHandler.get')
    @patch('models.database_mgr.DatabaseMgr.init_db')
    def test_get_config_without_token(self, _, get_mock):
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

    @patch('models.config_handler.ConfigHandler.get')
    @patch('models.config_handler.ConfigHandler.delete')
    @patch('models.database_mgr.DatabaseMgr.init_db')
    def test_del_config_without_token(self, _, delete_mock, get_mock):
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
            delete_mock.assert_not_called()

    @patch('models.config_handler.ConfigHandler.insert')
    @patch('models.database_mgr.DatabaseMgr.init_db')
    def test_register_config_without_token(self, _, insert_mock):
        '''
        TODO
        '''
        app = create_app()

        with app.test_client() as cli:
            dev_id = 'fakeid'
            request = {
                "group": "fake-group",
                "interval": "20"
            }
            expected_msg = { 'msg': 'Missing Authorization Header' }

            ret = cli.post(f'/devices/{dev_id}/config/', json=request)

            self.assertEqual(ret.json, expected_msg)
            self.assertEqual(ret.status_code, 401)

            insert_mock.assert_not_called()

    @patch('models.config_handler.ConfigHandler.get')
    @patch('models.config_handler.ConfigHandler.update')
    @patch('models.database_mgr.DatabaseMgr.init_db')
    def test_update_config_without_token(self, _, update_mock, get_mock):
        '''
        TODO
        '''
        app = create_app()

        with app.test_client() as cli:
            dev_id = 'fake_id'
            request = { 'param': 'interval', 'value': '10' }
            expected_msg = { 'msg': 'Missing Authorization Header' }

            ret = cli.put(f'/devices/{dev_id}/config/', json=request)

            self.assertEqual(ret.json, expected_msg)
            self.assertEqual(ret.status_code, 401)

            get_mock.assert_not_called()
            update_mock.assert_not_called()


if __name__ == "__main__":
    main()
