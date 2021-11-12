from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse


EMAIL = 'pitymaia@mailinator.com'
PASSWORD = 'test123'


class AdminTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email='pitymaia@gmail.com',
            password=PASSWORD
        )
        self.client.force_login(self.admin_user)
        self.user = get_user_model().objects.create_superuser(
            email=EMAIL,
            password=PASSWORD,
            name='Test user full name'
        )

    def test_users_listed(self):
        """Test that users are listed on user page"""
        url = reverse('admin:core_user_changelist')
        response = self.client.get(url)

        self.assertContains(response, self.user.name)
        self.assertContains(response, self.user.email)

    def test_user_change_page(self):
        """Test that the user edit page works"""
        url = reverse('admin:core_user_change', args=[self.user.id])
        # /admin/core/user/:id
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

    def test_create_user_page(self):
        """Test thath the create user page works"""
        url = reverse('admin:core_user_add')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
