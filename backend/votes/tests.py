from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from topics.models import Topic
from .models import Vote
from django.utils import timezone

User = get_user_model()


class VoteModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            cpf="12345678901",
            name="Test User",
            email="test@example.com",
            password="testpass123",
        )
        self.topic = Topic.objects.create(
            title="Pauta",
            description="desc",
            created_by=self.user,
            status="OPEN",
            session_started_at=timezone.now(),
        )

    def test_create_vote_valid(self):
        vote = Vote.objects.create(topic=self.topic, user=self.user, vote="YES")
        self.assertEqual(vote.vote, "YES")
        self.assertEqual(vote.topic, self.topic)
        self.assertEqual(vote.user, self.user)

    def test_vote_unique_per_user_per_topic(self):
        Vote.objects.create(topic=self.topic, user=self.user, vote="YES")
        with self.assertRaises(Exception):
            Vote.objects.create(topic=self.topic, user=self.user, vote="NO")

    def test_vote_requires_fields(self):
        with self.assertRaises(Exception):
            Vote.objects.create(user=self.user, vote="YES")
        with self.assertRaises(Exception):
            Vote.objects.create(topic=self.topic, vote="YES")
        with self.assertRaises(Exception):
            Vote.objects.create(topic=self.topic, user=self.user)


class VoteAPITest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            cpf="12345678901",
            name="Test User",
            email="test@example.com",
            password="testpass123",
        )
        self.other_user = User.objects.create_user(
            cpf="98765432100",
            name="Other User",
            email="other@example.com",
            password="otherpass123",
        )
        self.topic = Topic.objects.create(
            title="Pauta",
            description="desc",
            created_by=self.user,
            status="OPEN",
            session_started_at=timezone.now(),
        )
        self.client = APIClient()
        self.vote_url = f"/topics/{self.topic.id}/vote"
        self.result_url = f"/topics/{self.topic.id}/result"

    def test_vote_authenticated(self):
        self.client.force_authenticate(user=self.other_user)
        response = self.client.post(self.vote_url, {"vote": "YES"})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("vote", response.data)

    def test_vote_unauthenticated(self):
        response = self.client.post(self.vote_url, {"vote": "YES"})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_vote_twice_same_topic(self):
        self.client.force_authenticate(user=self.other_user)
        self.client.post(self.vote_url, {"vote": "YES"})
        response = self.client.post(self.vote_url, {"vote": "NO"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)

    def test_vote_when_session_closed(self):
        self.topic.status = "CLOSED"
        self.topic.save()
        self.client.force_authenticate(user=self.other_user)
        response = self.client.post(self.vote_url, {"vote": "YES"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)

    def test_vote_invalid_choice(self):
        self.client.force_authenticate(user=self.other_user)
        response = self.client.post(self.vote_url, {"vote": "MAYBE"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("vote", response.data)

    def test_result_public(self):
        # Votar YES e NO
        Vote.objects.create(topic=self.topic, user=self.user, vote="YES")
        Vote.objects.create(topic=self.topic, user=self.other_user, vote="NO")
        response = self.client.get(self.result_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["total_votes"], 2)
        self.assertEqual(response.data["yes_votes"], 1)
        self.assertEqual(response.data["no_votes"], 1)
