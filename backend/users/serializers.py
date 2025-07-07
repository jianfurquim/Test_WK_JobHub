
from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import User

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)
    
    class Meta:
        model = User
        fields = ('name', 'cpf', 'password', 'email')
        extra_kwargs = {
            'email': {'required': False}
        }
    
    def validate_cpf(self, value):
        # Remove non-numeric characters
        cpf = ''.join(filter(str.isdigit, value))
        
        if len(cpf) != 11:
            raise serializers.ValidationError("CPF deve ter 11 dígitos.")
        
        return cpf
    
    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()
        return user

class UserLoginSerializer(serializers.Serializer):
    cpf = serializers.CharField()
    password = serializers.CharField()
    
    def validate(self, attrs):
        cpf = attrs.get('cpf')
        password = attrs.get('password')
        
        if cpf and password:
            # Clean CPF
            cpf = ''.join(filter(str.isdigit, cpf))
            
            user = authenticate(request=self.context.get('request'),
                             cpf=cpf, password=password)
            
            if not user:
                raise serializers.ValidationError('CPF ou senha incorretos.')
            
            attrs['user'] = user
            return attrs
        else:
            raise serializers.ValidationError('CPF e senha são obrigatórios.')

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'name', 'cpf', 'email', 'date_joined')
        read_only_fields = ('id', 'date_joined')
