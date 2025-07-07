
from rest_framework import serializers
from .models import Vote

class VoteSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.name', read_only=True)
    topic_title = serializers.CharField(source='topic.title', read_only=True)
    
    class Meta:
        model = Vote
        fields = ['id', 'topic', 'user', 'vote', 'created_at', 'user_name', 'topic_title']
        read_only_fields = ['id', 'user', 'created_at']

class VoteCreateSerializer(serializers.Serializer):
    vote = serializers.ChoiceField(choices=Vote.VOTE_CHOICES)

class TopicResultSerializer(serializers.Serializer):
    topic_id = serializers.IntegerField()
    topic_title = serializers.CharField()
    topic_description = serializers.CharField()
    topic_status = serializers.CharField()
    total_votes = serializers.IntegerField()
    yes_votes = serializers.IntegerField()  
    no_votes = serializers.IntegerField()
    results = serializers.DictField()
