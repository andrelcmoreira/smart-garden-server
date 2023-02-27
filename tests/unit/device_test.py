from unittest import main, TestCase

from app.storage.models.device import Device

class DeviceTest(TestCase):

    def test_device_creation(self):
        dev = Device(
            id='fake-id',
            serial='fake-serial',
            group='fake-group',
            desc='fake-desc'
        )

        self.assertEqual(dev.id, 'fake-id')
        self.assertEqual(dev.serial, 'fake-serial')
        self.assertEqual(dev.group, 'fake-group')
        self.assertEqual(dev.desc, 'fake-desc')

if __name__ == "__main__":
    main()
