from unittest.mock import patch

from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models

EMAIL = 'pitymaia@mailinator.com'
PASSWORD = 'testPassword123'


def sample_user(email='test@mailinator.com', password='test123'):
    """Create a sample user"""
    return get_user_model().objects.create_user(email, password)


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

    def test_tag_str(self):
        """Test the tag string representation"""
        tag = models.Tag.objects.create(
            user=sample_user(),
            name='Vegan'
        )

        self.assertEqual(str(tag), tag.name)

    def test_ingredient_str(self):
        """Test ingredient string representation"""
        ingredient = models.Ingredient.objects.create(
            user=sample_user(),
            name="cucumber"
        )
        self.assertEqual(str(ingredient), ingredient.name)

    def test_recipe_str(self):
        """Test recipe string representation"""
        recipe = models.Recipe.objects.create(
            user=sample_user(),
            title='Stake and mushroom sauce',
            time_minutes=5,
            price=5.00
        )

        self.assertEqual(str(recipe), recipe.title)

    @patch('uuid.uuid4')
    def test_recipe_file_name_uuid(self, mock_uuid):
        """Test that image is saved in the correct location"""
        uuid = 'test-uuid'
        mock_uuid.return_value = uuid
        file_path = models.recipe_image_file_path(None, 'myimage.jpg')

        exp_path = f'uploads/recipe/{uuid}.jpg'
        self.assertEqual(file_path, exp_path)
