from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserRegistrationSerializer, UserLoginSerializer, UserSerializer

@api_view(['POST'])
@permission_classes([AllowAny])
def register_view(request):
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        user_data = UserSerializer(user).data
        
        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'message': 'Usuário cadastrado com sucesso!',
            'user': user_data,
            'token': str(refresh.access_token),
            'refresh': str(refresh)
        }, status=status.HTTP_201_CREATED)
    
    return Response({
        'error': 'Erro no cadastro',
        'details': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
@csrf_exempt
def login_view(request):
    print("ENTROU NESSA VIEW")
    serializer = UserLoginSerializer(data=request.data, context={'request': request})
    print(serializer.is_valid())
    if serializer.is_valid():
        user = serializer.validated_data['user']
        user_data = UserSerializer(user).data
        
        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'message': 'Login realizado com sucesso!',
            'user': user_data,
            'token': str(refresh.access_token),
            'refresh': str(refresh)
        })
    
    return Response({
        'error': 'Erro no login',
        'details': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)
