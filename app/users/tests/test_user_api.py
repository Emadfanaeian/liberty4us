"""Test User Apis"""

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

CREATE_USER_URL = reverse('users:create')
TOKEN_URL = reverse('users:token')
ME_URL = reverse('users:me')


def create_user(**params):
    """ Create Simple Usee """
    return get_user_model().objects.create_user(**params)


class PublicUsersApiTests(TestCase):
    """Test Public Users API"""

    def setUp(self) -> None:
        self.client = APIClient()

    def test_create_valid_user_success(self):
        """Test User With Valid Payload is Success"""
        payload = {
            'email': 'test@liberty4us.world',
            'password': 'testpassword',
            'name': 'test name'
        }

        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**res.data)
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)

    def test_user_duplicate(self):
        """Test that user already exists"""
        payload = {'email': 'foo@liberty4us.worl', 'password': 'testpassword'}
        create_user(**payload)
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_short(self):
        """test strong password"""
        payload = {'email': 'test@liberty4us.world', 'password':  'test'}
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(user_exists)

    def test_create_token_for_user(self):
        """ Test Token Creation For User """
        payload = {
            'email': 'test@liberty4u.world',
            'password': 'testpassword'
        }
        create_user(**payload)
        res = self.client.post(TOKEN_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_invalid_credentials(self):
        """ bad payload """
        payload = {
            'email': 'test@liberty4u.world',
            'password': 'testpassword'
        }
        create_user(**payload)
        res = self.client.post(TOKEN_URL, **{
            'email': 'test@liberty4u.world',
            'password': 'testpasswordaaa'
        })
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_user_no_user(self):
        """test user not exists"""
        res = self.client.post(TOKEN_URL, **{
            'email': 'test@liberty4u.world',
            'password': 'testpasswordaaa'
        })
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_token_missing_field(self):
        """test user not exists"""
        res = self.client.post(TOKEN_URL, **{
            'email': 'test@liberty4u.world',
            'password': ''
        })
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_user_unauthorized(self):
        """Test That auth is requiired for users"""
        res = self.client.get(ME_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateUserApiTest(TestCase):
    """Test pprivate User Apis"""

    def setUp(self):
        self.user = create_user(
            email='test@liberty4u.world',
            password='testpassword',
            name='name'
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retrieve_profile(self):
        """retrieve profile for logged in user"""
        res = self.client.get(ME_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, {
            'name': self.user.name,
            'email': self.user.email,
        })

    def test_post_profile_not_allowed(self):
        """ Test That post method is not allowed on me url """
        res = self.client.post(ME_URL, {})
        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_user_profile(self):
        """Test Updating Profile For Authorized User"""
        payload = {'name': 'new name', 'password': 'newpassword'}
        res = self.client.patch(ME_URL, payload)
        self.user.refresh_from_db()
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(self.user.name, payload['name'])
        self.assertTrue(self.user.check_password(payload['password']))
