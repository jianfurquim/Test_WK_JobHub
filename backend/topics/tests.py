from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from .models import Topic
from django.urls import reverse
from django.utils import timezone

User = get_user_model()


class TopicModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            cpf="12345678901",
            name="Test User",
            email="test@example.com",
            password="testpass123",
        )

    def test_create_topic_with_valid_data(self):
        topic = Topic.objects.create(
            title="Pauta 1", description="Descrição da pauta", created_by=self.user
        )
        self.assertEqual(topic.title, "Pauta 1")
        self.assertEqual(topic.status, "WAITING")
        self.assertEqual(topic.created_by, self.user)

    def test_topic_requires_created_by(self):
        with self.assertRaises(Exception):
            Topic.objects.create(title="Pauta", description="desc")

    def test_is_session_active_property(self):
        topic = Topic.objects.create(
            title="Sessão", description="desc", created_by=self.user
        )
        self.assertFalse(topic.is_session_active)
        topic.status = "OPEN"
        topic.session_started_at = timezone.now() - timezone.timedelta(minutes=30)
        topic.session_duration = 60
        topic.save()
        self.assertTrue(topic.is_session_active)
        topic.session_started_at = timezone.now() - timezone.timedelta(minutes=61)
        topic.save()
        self.assertFalse(topic.is_session_active)

    def test_close_session_if_expired(self):
        topic = Topic.objects.create(
            title="Sessão",
            description="desc",
            created_by=self.user,
            status="OPEN",
            session_started_at=timezone.now() - timezone.timedelta(minutes=61),
            session_duration=60,
        )
        topic.close_session_if_expired()
        topic.refresh_from_db()
        self.assertEqual(topic.status, "CLOSED")


class TopicAPITest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            cpf="12345678901",
            name="Test User",
            email="test@example.com",
            password="testpass123",
        )
        self.client = APIClient()
        self.topics_url = "/topics"

    def test_list_topics_public(self):
        Topic.objects.create(title="Pauta 1", description="desc", created_by=self.user)
        response = self.client.get(self.topics_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) >= 1)

    def test_create_topic_unauthenticated(self):
        data = {"title": "Nova Pauta", "description": "Desc"}
        response = self.client.post(self.topics_url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_topic_authenticated(self):
        self.client.force_authenticate(user=self.user)
        data = {"title": "Nova Pauta", "description": "Desc"}
        response = self.client.post(self.topics_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("topic", response.data)

    def test_topic_detail(self):
        topic = Topic.objects.create(
            title="Detalhe", description="desc", created_by=self.user
        )
        url = f"/topics/{topic.id}"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Detalhe")

    def test_start_session_unauthenticated(self):
        topic = Topic.objects.create(
            title="Sessão", description="desc", created_by=self.user
        )
        url = f"/topics/{topic.id}/session"
        response = self.client.post(url, {"duration": 30})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_start_session_authenticated(self):
        topic = Topic.objects.create(
            title="Sessão", description="desc", created_by=self.user
        )
        self.client.force_authenticate(user=self.user)
        url = f"/topics/{topic.id}/session"
        response = self.client.post(url, {"duration": 30})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("message", response.data)
