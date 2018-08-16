from .helper import TestHelper, User
from ..validations import *


class UtilValidation(TestHelper):

    def test_validate_email(self):
        print('validate_email')
        with self.assertRaises(forms.ValidationError):
            validate_email('fakeemail.com')

    def test_validate_password(self):
        print('validate_password')
        with self.assertRaises(forms.ValidationError):
            validate_password(self.password, 'otherpassword')
            validate_password('some', 'some')
            validate_password('', '')
            validate_password('', self.password)
            validate_password(self.password, '')
        self.assertEqual(validate_password(self.password, self.password), self.password)

    def test_validate_email_absence(self):
        print('validate_email_absence')
        User.objects.create_user(**self.data['user'])
        with self.assertRaises(forms.ValidationError):
            validate_email_absence(self.email)
            validate_email_absence('')
        self.delete_user_instance(self.email)
        self.assertEqual(validate_email_absence(self.email), self.email)
