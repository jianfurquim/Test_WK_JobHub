
from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()

class Topic(models.Model):
    STATUS_CHOICES = [
        ('WAITING', 'Aguardando Abertura'),
        ('OPEN', 'Sessão Aberta'),
        ('CLOSED', 'Votação Encerrada'),
    ]
    
    title = models.CharField(max_length=200, verbose_name='Título')
    description = models.TextField(verbose_name='Descrição')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Criado por')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='WAITING')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Session management
    session_started_at = models.DateTimeField(null=True, blank=True)
    session_duration = models.IntegerField(default=60, help_text='Duração em minutos')
    
    class Meta:
        verbose_name = 'Pauta'
        verbose_name_plural = 'Pautas'
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title
    
    @property
    def is_session_active(self):
        if self.status != 'OPEN' or not self.session_started_at:
            return False
        
        session_end = self.session_started_at + timezone.timedelta(minutes=self.session_duration)
        return timezone.now() < session_end
    
    def close_session_if_expired(self):
        if self.status == 'OPEN' and not self.is_session_active:
            self.status = 'CLOSED'
            self.save()
