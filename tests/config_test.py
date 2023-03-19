from unittest import main, TestCase

from app.storage.models.config import Config

class ConfigTest(TestCase):

    '''
    TODO
    '''

    def test_config_creation(self):
        '''
        TODO
        '''
        cfg = Config(
            id='fake-id',
            group='fake-group',
            interval=10
        )

        self.assertEqual(cfg.id, 'fake-id')
        self.assertEqual(cfg.group, 'fake-group')
        self.assertEqual(cfg.interval, 10)

if __name__ == "__main__":
    main()
