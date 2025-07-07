
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.utils import timezone
from .models import Topic
from .serializers import TopicSerializer, TopicCreateSerializer, SessionStartSerializer

@api_view(['GET', 'POST'])
def topics_view(request):
    if request.method == 'GET':
        # Public endpoint - no authentication required
        topics = Topic.objects.all()
        # Update expired sessions
        for topic in topics:
            topic.close_session_if_expired()
        
        serializer = TopicSerializer(topics, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        # Creating topics requires authentication
        if not request.user.is_authenticated:
            return Response({'error': 'Autenticação necessária'}, status=status.HTTP_401_UNAUTHORIZED)
        
        serializer = TopicCreateSerializer(data=request.data)
        if serializer.is_valid():
            topic = serializer.save(created_by=request.user)
            response_serializer = TopicSerializer(topic)
            return Response({
                'message': 'Pauta criada com sucesso!',
                'topic': response_serializer.data
            }, status=status.HTTP_201_CREATED)
        
        return Response({
            'error': 'Erro ao criar pauta',
            'details': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def start_session_view(request, topic_id):
    topic = get_object_or_404(Topic, id=topic_id)
    
    if topic.status != 'WAITING':
        return Response({
            'error': 'Sessão não pode ser iniciada. Status atual: ' + topic.get_status_display()
        }, status=status.HTTP_400_BAD_REQUEST)
    
    serializer = SessionStartSerializer(data=request.data)
    if serializer.is_valid():
        duration = serializer.validated_data.get('duration', 60)
        
        topic.status = 'OPEN'
        topic.session_started_at = timezone.now()
        topic.session_duration = duration
        topic.save()
        
        response_serializer = TopicSerializer(topic)
        return Response({
            'message': f'Sessão iniciada! Duração: {duration} minutos',
            'topic': response_serializer.data
        })
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([AllowAny])
def topic_detail_view(request, topic_id):
    topic = get_object_or_404(Topic, id=topic_id)
    topic.close_session_if_expired()  # Update status if needed
    
    serializer = TopicSerializer(topic)
    return Response(serializer.data)
