from unittest import main, TestCase

from storage.models.device import Device

class DeviceTest(TestCase):

    '''
    Unit tests of device model.

    '''

    def test_device_creation(self):
        '''
        GIVEN we have a set of device parameters.
        WHEN we create a new device instance with this data.
        THEN the instance must be created with the correct parameters.

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
