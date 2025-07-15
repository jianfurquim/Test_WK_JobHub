from django.test import TestCase
from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError

User = get_user_model()


class UserModelTest(TestCase):
    def test_create_user_with_valid_data(self):
        user = User.objects.create_user(
            cpf="12345678901",
            name="Test User",
            email="test@example.com",
            password="testpass123",
        )
        self.assertEqual(user.cpf, "12345678901")
        self.assertEqual(user.name, "Test User")
        self.assertEqual(user.email, "test@example.com")
        self.assertTrue(user.check_password("testpass123"))
        self.assertFalse(user.is_staff)
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_superuser)

    def test_create_superuser(self):
        admin_user = User.objects.create_superuser(
            cpf="10987654321",
            name="Admin User",
            email="admin@example.com",
            password="adminpass123",
        )
        self.assertEqual(admin_user.cpf, "10987654321")
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)
        self.assertTrue(admin_user.is_active)

    def test_cpf_is_required(self):
        with self.assertRaises(ValueError):
            User.objects.create_user(
                cpf=None, name="No CPF", email="no_cpf@example.com", password="nopass"
            )

    def test_cpf_is_unique(self):
        User.objects.create_user(
            cpf="55566677788", name="User1", email="user1@example.com", password="pass1"
        )
        with self.assertRaises(IntegrityError):
            User.objects.create_user(
                cpf="55566677788",
                name="User2",
                email="user2@example.com",
                password="pass2",
            )

    def test_email_is_unique(self):
        User.objects.create_user(
            cpf="88899900011",
            name="User1",
            email="unique@example.com",
            password="pass1",
        )
        with self.assertRaises(IntegrityError):
            User.objects.create_user(
                cpf="11122233344",
                name="User2",
                email="unique@example.com",
                password="pass2",
            )

    def test_name_none_raises_integrity_error(self):
        with self.assertRaises(IntegrityError):
            User.objects.create_user(
                cpf="33344455566",
                name=None,
                email="none_name@example.com",
                password="nopass",
            )

    def test_name_empty_string(self):
        user = User.objects.create_user(
            cpf="44455566677",
            name="",
            email="empty_name@example.com",
            password="nopass",
        )
        self.assertEqual(user.name, "")
