from unittest import main, TestCase

from app.storage.models.device import Device

class DeviceTest(TestCase):

    '''
    TODO
    '''

    def test_device_creation(self):
        '''
        TODO
        '''
        dev = Device(
            id='fake-id',
            serial='fake-serial',
            model='fake-model',
            desc='fake-desc'
        )

        self.assertEqual(dev.id, 'fake-id')
        self.assertEqual(dev.serial, 'fake-serial')
        self.assertEqual(dev.model, 'fake-model')
        self.assertEqual(dev.desc, 'fake-desc')

if __name__ == "__main__":
    main()
