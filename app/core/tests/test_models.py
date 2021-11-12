from django.test import TestCase
from django.contrib.auth import get_user_model


EMAIL = 'pitymaia@mailinator.com'
PASSWORD = 'testPassword123'

class ModelTests(TestCase):

	def test_create_user_with_email(self):
		"""Test creating a new user with email"""
		user = get_user_model().objects.create_user(
			email=EMAIL,
			password=PASSWORD
		)

		self.assertEqual(user.email, EMAIL)
		self.assertTrue(user.check_password(PASSWORD))

	def test_new_user_email_normalized(self):
		"""Test if the user email is normalized"""
		email = 'pitymaia@MAILINATOR.COM'
		user = get_user_model().objects.create_user(email, PASSWORD)

		self.assertEqual(user.email, email.lower())
		self.assertEqual(user.email, EMAIL)

	def test_new_user_invalid_email(self):
		"""Test creating user with no email raises error"""
		with self.assertRaises(ValueError):
			get_user_model().objects.create_user(None, PASSWORD)

	def test_create_superuser(self):
		"""Test create new superuser"""
		user = get_user_model().objects.create_superuser(
			EMAIL,
			PASSWORD
		)

		self.assertTrue(user.is_superuser)
		self.assertTrue(user.is_staff)