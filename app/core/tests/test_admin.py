"""Test Admin Panel For Core"""
from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse


class AdminSiteTest(TestCase):
    """Test Admin"""

    def setUp(self):
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

    def test_users_list(self):
        """Test Users List Got Our New Model"""
        url = reverse('admin:core_user_changelist')
        print(self.admin_user.name)
        res = self.client.get(url)
        self.assertContains(res, self.user.name)
        self.assertContains(res, self.user.email)

    def test_user_change_page(self):
        """User Edit Page Works"""
        url = reverse('admin:core_user_change', args=[self.user.id])
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)

    def test_create_user_page(self):
        """test create user page works"""
        url = reverse('admin:core_user_add')
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)