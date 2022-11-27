"""test model"""
from core import models
from django.contrib.auth import get_user_model
from django.test import TestCase


def sample_user(email='test@liberty4us.world', password='testpassword'):
    """ Create Sample User """
    return get_user_model().objects.create_user(email=email, password=password)


class ModelTest(TestCase):
    """Test Model Class."""

    def test_create_user_with_email(self):
        """test create user with email success"""
        email = 'test@liberty4us.world'
        password = 'Test1234'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """ Test Email Is Normalized """
        email = 'test@liberty4Us.world'
        user = get_user_model().objects.create_user(email=email, password="asdasdsad")
        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """Test Email ValueError"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(email=None, password="asdasdsad")

    def test_create_superuser(self):
        """ test super user created"""
        email = 'test@liberty4us.world'
        password = 'Test1234'
        user = get_user_model().objects.create_superuser(
            email=email,
            password=password
        )
        self.assertTrue(user.is_staff)

    def test_tag_str(self):
        """Test The Tag String representation"""
        tag = models.Tag.objects.create(
            user=sample_user(),
            name='vegan'
        )

        self.assertEqual(str(tag), tag.name)
