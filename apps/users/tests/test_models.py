from django.contrib.auth import get_user_model
from django.test import TestCase


class UserModelTest(TestCase):
    def test_create_user(self) -> None:
        User = get_user_model()
        user = User.objects.create_user(
            email="test@example.com",
            username="testuser",
            password="testpass123",  # nosec B106
        )
        self.assertEqual(user.email, "test@example.com")
        self.assertEqual(user.username, "testuser")
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_superuser(self) -> None:
        User = get_user_model()
        admin_user = User.objects.create_superuser(
            email="admin@example.com",
            username="admin",
            password="testpass123",  # nosec B106
        )
        self.assertEqual(admin_user.email, "admin@example.com")
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)
