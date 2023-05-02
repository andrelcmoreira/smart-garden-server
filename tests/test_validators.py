from unittest import main, TestCase

from app.validators import validate_field

class ValidatorsTest(TestCase):

    '''
    Validators unit tests.

    '''

    def test_validate_field_with_valid_id(self):
        '''
        TODO
        '''
        value = '1234efgh'

        self.assertTrue(validate_field('id', value))

    def test_validate_field_with_invalid_id(self):
        '''
        TODO
        '''
        value = 'ABCDE123@!_'

        self.assertFalse(validate_field('id', value))

    def test_validate_field_with_blank_id(self):
        '''
        TODO
        '''
        self.assertFalse(validate_field('id', ''))


    def test_validate_field_with_valid_user(self):
        '''
        TODO
        '''
        user_name = 'admin'

        self.assertTrue(validate_field('user', user_name))

    def test_validate_field_with_blank_user(self):
        '''
        TODO
        '''
        self.assertFalse(validate_field('user', ''))

    def test_validate_field_with_invalid_user(self):
        '''
        TODO
        '''
        user_name = '@dm1n_1234!'

        self.assertFalse(validate_field('user', user_name))

    def test_validate_field_with_valid_pass(self):
        '''
        TODO
        '''
        password = '_P@$$sw0rd!'

        self.assertTrue(validate_field('password', password))

    def test_validate_field_with_blank_pass(self):
        '''
        TODO
        '''
        self.assertFalse(validate_field('password', ''))

    def test_validate_field_with_invalid_pass(self):
        '''
        TODO
        '''
        password = '   _p@$$_'

        self.assertFalse(validate_field('password', password))

    def test_validate_field_with_valid_serial(self):
        '''
        TODO
        '''
        serial = 'ABCDE-12345'

        self.assertTrue(validate_field('serial-number', serial))

    def test_validate_field_with_blank_serial(self):
        '''
        TODO
        '''
        self.assertFalse(validate_field('serial-number', ''))

    def test_validate_field_with_invalid_serial(self):
        '''
        TODO
        '''
        serial = '@bcd_!2345'

        self.assertFalse(validate_field('serial-number', serial))

    def test_validate_field_with_valid_model(self):
        '''
        TODO
        '''
        model = 'VALID_MODEL'

        self.assertTrue(validate_field('model', model))

    def test_validate_field_with_blank_model(self):
        '''
        TODO
        '''
        self.assertFalse(validate_field('model', ''))

    def test_validate_field_with_invalid_model(self):
        '''
        TODO
        '''
        model = '@#$MODEL'

        self.assertFalse(validate_field('model', model))

# TODO: validate_request tests

if __name__ == "__main__":
    main()
