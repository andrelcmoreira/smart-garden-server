from unittest import main, TestCase

from app.validators import validate_field


class ValidatorsTest(TestCase):

    '''
    Validators unit tests.

    '''

    def test_validate_field_with_valid_id(self):
        '''
        GIVEN we have a valid ID
        WHEN  we validate it
        THEN  true must be returned
        '''
        value = '1234efgh'

        self.assertTrue(validate_field('id', value))

    def test_validate_field_with_invalid_id(self):
        '''
        GIVEN we have an invalid ID
        WHEN  we validate it
        THEN  false must be returned
        '''
        value = 'ABCDE123@!_'

        self.assertFalse(validate_field('id', value))

    def test_validate_field_with_blank_id(self):
        '''
        GIVEN we have a blank ID
        WHEN  we validate it
        THEN  false must be returned
        '''
        self.assertFalse(validate_field('id', ''))


    def test_validate_field_with_valid_user(self):
        '''
        GIVEN we have a valid user
        WHEN  we validate it
        THEN  true must be returned
        '''
        user_name = 'admin'

        self.assertTrue(validate_field('user', user_name))

    def test_validate_field_with_blank_user(self):
        '''
        GIVEN we have a blank user
        WHEN  we validate it
        THEN  false must be returned
        '''
        self.assertFalse(validate_field('user', ''))

    def test_validate_field_with_invalid_user(self):
        '''
        GIVEN we have an invalid user
        WHEN  we validate it
        THEN  false must be returned
        '''
        user_name = '@dm1n_1234!'

        self.assertFalse(validate_field('user', user_name))

    def test_validate_field_with_valid_pass(self):
        '''
        GIVEN we have a valid pass
        WHEN  we validate it
        THEN  true must be returned
        '''
        password = '_P@$$sw0rd!'

        self.assertTrue(validate_field('password', password))

    def test_validate_field_with_blank_pass(self):
        '''
        GIVEN we have a blank pass
        WHEN  we validate it
        THEN  false must be returned
        '''
        self.assertFalse(validate_field('password', ''))

    def test_validate_field_with_invalid_pass(self):
        '''
        GIVEN we have an invalid pass
        WHEN  we validate it
        THEN  false must be returned
        '''
        password = '   _p@$$_'

        self.assertFalse(validate_field('password', password))

    def test_validate_field_with_valid_serial(self):
        '''
        GIVEN we have a valid serial
        WHEN  we validate it
        THEN  true must be returned
        '''
        serial = 'ABCDE-12345'

        self.assertTrue(validate_field('serial-number', serial))

    def test_validate_field_with_blank_serial(self):
        '''
        GIVEN we have a blank serial
        WHEN  we validate it
        THEN  false must be returned
        '''
        self.assertFalse(validate_field('serial-number', ''))

    def test_validate_field_with_invalid_serial(self):
        '''
        GIVEN we have an invalid serial
        WHEN  we validate it
        THEN  false must be returned
        '''
        serial = '@bcd_!2345'

        self.assertFalse(validate_field('serial-number', serial))

    def test_validate_field_with_valid_model(self):
        '''
        GIVEN we have a valid model
        WHEN  we validate it
        THEN  true must be returned
        '''
        model = 'VALID_MODEL'

        self.assertTrue(validate_field('model', model))

    def test_validate_field_with_blank_model(self):
        '''
        GIVEN we have a blank model
        WHEN  we validate it
        THEN  false must be returned
        '''
        self.assertFalse(validate_field('model', ''))

    def test_validate_field_with_invalid_model(self):
        '''
        GIVEN we have an invalid model
        WHEN  we validate it
        THEN  false must be returned
        '''
        model = '@#$MODEL'

        self.assertFalse(validate_field('model', model))

# TODO: validate_request tests

if __name__ == "__main__":
    main()
