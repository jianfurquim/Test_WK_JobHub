
from rest_framework import serializers
from .models import Topic

class TopicSerializer(serializers.ModelSerializer):
    created_by_name = serializers.CharField(source='created_by.name', read_only=True)
    is_session_active = serializers.ReadOnlyField()
    
    class Meta:
        model = Topic
        fields = [
            'id', 'title', 'description', 'status', 'created_at', 
            'updated_at', 'session_started_at', 'session_duration',
            'created_by', 'created_by_name', 'is_session_active'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'created_by']
    
    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)

class TopicCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = ['title', 'description', 'session_duration']

class SessionStartSerializer(serializers.Serializer):
    duration = serializers.IntegerField(default=60, min_value=1, max_value=1440)  # Max 24 hours
