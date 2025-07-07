
from django.contrib import admin
from .models import Topic

@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'created_by', 'created_at', 'is_session_active')
    list_filter = ('status', 'created_at')
    search_fields = ('title', 'description')
    readonly_fields = ('created_at', 'updated_at', 'is_session_active')
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('title', 'description', 'created_by')
        }),
        ('Status e Sessão', {
            'fields': ('status', 'session_started_at', 'session_duration', 'is_session_active')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
