from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db.models import Count, Q
from topics.models import Topic
from .models import Vote
from .serializers import VoteCreateSerializer, TopicResultSerializer


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def vote_view(request, topic_id):
    topic = get_object_or_404(Topic, id=topic_id)

    # Check if session is active
    topic.close_session_if_expired()
    if not topic.is_session_active:
        return Response(
            {"error": "Sessão de votação não está ativa"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    # Check if user already voted
    if Vote.objects.filter(topic=topic, user=request.user).exists():
        return Response(
            {"error": "Você já votou nesta pauta"}, status=status.HTTP_400_BAD_REQUEST
        )

    serializer = VoteCreateSerializer(data=request.data)
    if serializer.is_valid():
        vote = Vote.objects.create(
            topic=topic, user=request.user, vote=serializer.validated_data["vote"]
        )

        return Response(
            {
                "message": "Voto registrado com sucesso!",
                "vote": {
                    "id": vote.id,
                    "vote": vote.vote,
                    "created_at": vote.created_at,
                },
            },
            status=status.HTTP_201_CREATED,
        )

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@permission_classes([AllowAny])
def topic_result_view(request, topic_id):
    topic = get_object_or_404(Topic, id=topic_id)

    # Get vote counts
    vote_counts = Vote.objects.filter(topic=topic).aggregate(
        total=Count("id"),
        yes_votes=Count("id", filter=Q(vote="YES")),
        no_votes=Count("id", filter=Q(vote="NO")),
    )

    result_data = {
        "topic_id": topic.id,
        "topic_title": topic.title,
        "topic_description": topic.description,
        "topic_status": topic.status,
        "total_votes": vote_counts["total"] or 0,
        "yes_votes": vote_counts["yes_votes"] or 0,
        "no_votes": vote_counts["no_votes"] or 0,
        "results": {
            "YES": vote_counts["yes_votes"] or 0,
            "NO": vote_counts["no_votes"] or 0,
        },
    }

    serializer = TopicResultSerializer(result_data)
    return Response(serializer.data)
