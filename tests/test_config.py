from unittest import main, TestCase

from storage.models.config import Config

class ConfigTest(TestCase):

    '''
    Unit tests of config model.

    '''

    def test_config_creation(self):
        '''
        GIVEN we have a set of configuration parameters.
        WHEN we create a new config instance with this data.
        THEN the instance must be created with the correct parameters.

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
