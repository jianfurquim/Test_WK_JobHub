
from django.db import models
from django.contrib.auth import get_user_model
from topics.models import Topic

User = get_user_model()

class Vote(models.Model):
    VOTE_CHOICES = [
        ('YES', 'Sim'),
        ('NO', 'Não'),
    ]
    
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='votes')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    vote = models.CharField(max_length=3, choices=VOTE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['topic', 'user']  # One vote per user per topic
        verbose_name = 'Voto'
        verbose_name_plural = 'Votos'
    
    def __str__(self):
        return f"{self.user.name} - {self.topic.title} - {self.get_vote_display()}"
