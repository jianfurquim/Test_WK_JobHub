from django.contrib import admin
from .models import Vote


@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ("user", "topic", "vote", "created_at")
    list_filter = ("vote", "created_at", "topic__status")
    search_fields = ("user__name", "user__cpf", "topic__title")
    readonly_fields = ("created_at",)

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("user", "topic")
