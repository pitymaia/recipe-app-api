from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status


CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')
PAYLOAD = {
    'email': 'pitymaia@mailinator.com',
    'password': 'test123',
    'name': 'John Doe'
}


def create_user(**params):
    return get_user_model().objects.create_user(**params)


class PublicUserApiTests(TestCase):
    """Test users API"""

    def setUp(self):
        self.client = APIClient()

    def test_create_valid_user_success(self):
        """Test if creating user with valid payload is successful"""
        response = self.client.post(CREATE_USER_URL, PAYLOAD)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**response.data)
        self.assertTrue(user.check_password(PAYLOAD['password']))
        self.assertNotIn('password', response.data)

    def test_user_exists(self):
        """Test if user already exists"""
        create_user(**PAYLOAD)
        self.client.post(CREATE_USER_URL, PAYLOAD)

    def test_password_too_shot(self):
        """Test thath the password have more than 5 chars"""
        payload = {
            'email': 'pitymaia@mailinator.com',
            'password': '123',
            'name': 'John Doe'
        }
        response = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(user_exists)

    def test_create_token_for_user(self):
        """Test that a token is created for user"""
        create_user(**PAYLOAD)
        response = self.client.post(TOKEN_URL, PAYLOAD)

        self.assertIn('token', response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_token_invalid(self):
        """Test the token is not created if invalid credentials are given"""
        create_user(email='pitymaia@mailinator.com', password='test123')
        payload = {'email': 'pitymaia@mailinator.com', 'password': '123'}
        response = self.client.post(TOKEN_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_no_user(self):
        """Test that token is not created if user doesn't exist"""
        payload = {'email': 'pitymaia@mailinator.com', 'password': '123'}
        response = self.client.post(TOKEN_URL, payload)
        self.assertNotIn('token', response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_missing_field(self):
        """Test that email and password are required"""
        payload = {'email': '', 'password': ''}
        response = self.client.post(TOKEN_URL, payload)
        self.assertNotIn('token', response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
