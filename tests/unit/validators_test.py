from unittest import main, TestCase

from app.validators import *

class ValidatorsTest(TestCase):

    def test_validate_user_with_valid_entry(self):
        user_name = 'admin'

        self.assertTrue(__is_user_valid(user_name))

    def test_validate_user_with_blank_entry(self):
        self.assertFalse(__is_user_valid(''))

    def test_validate_user_with_invalid_entry(self):
        user_name = '@dm1n_1234!'

        self.assertFalse(__is_user_valid(user_name))

    def test_validate_password_with_valid_entry(self):
        password = '_P@$$sw0rd!'

        self.assertTrue(__is_password_valid(password))

    def test_validate_password_with_blank_entry(self):
        self.assertFalse(__is_password_valid(''))

    def test_validate_password_with_invalid_entry(self):
        password = '   _p@$$_'

        self.assertFalse(__is_password_valid(password))

    def test_validate_serial_with_valid_entry(self):
        serial = 'ABCDE-12345'

        self.assertTrue(__is_serial_valid(serial))

    def test_validate_serial_with_blank_entry(self):
        serial = ''

        self.assertFalse(__is_serial_valid(serial))

    def test_validate_serial_with_invalid_entry(self):
        serial = 'abcd_12345'

        self.assertFalse(__is_serial_valid(serial))

    def test_validate_model_with_valid_entry(self):
        model = 'VALID_MODEL'

        self.assertTrue(__is_model_valid(model))

    def test_validate_model_with_blank_entry(self):
        model = ''

        self.assertFalse(__is_model_valid(model))

    def test_validate_model_with_invalid_entry(self):
        model = '@#$MODEL'

        self.assertFalse(__is_model_valid(model))

    def test_validate_id_with_valid_entry(self):
        dev_id = '1234efgh'

        self.assertTrue(__is_id_valid(dev_id))

    def test_validate_id_with_blank_entry(self):
        dev_id = ''

        self.assertFalse(__is_id_valid(dev_id))

    def test_validate_id_with_invalid_entry(self):
        dev_id = '@ABC$EF01234'

        self.assertFalse(__is_id_valid(dev_id))

if __name__ == "__main__":
    main()
