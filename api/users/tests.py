from django.test import TestCase
from users.models import User

# Create your tests here.


class UserTestCase(TestCase):
    """Dummy test case for user"""

    def test_user_was_saved(self):
        """Dummy"""
        user = User.objects.create(name="Brian", nick_name="Ogutu",
                                   email="codingbrian58@gmail.com",
                                   password="Henkdebruin58")
        self.assertEqual(user.name, "Brian")
        self.assertEqual(user.email, "codingbrian58@gmail.com")


class YourTestClass(TestCase):

    def test_one_plus_one_equals_two(self):
        print("Method: test_one_plus_one_equals_two.")
        self.assertEqual(1 + 1, 2)
