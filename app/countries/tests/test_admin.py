"""Test Admin Panel For countries"""
from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse


class TestCountriesAdmin(TestCase):
    """Test Countries In Admin Panel"""

    def setUp(self) -> None:
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email="test@liberty4us.com",
            password="testpassword",
            name="superAdmin"
        )
        self.client.force_login(self.admin_user)
        self.user = get_user_model().objects.create_user(
            email="test@simpleuser.com",
            password="testpassword",
            name="Test User"
        )

    def test_list(self):
        """test data in admin list"""
