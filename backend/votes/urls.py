from django.urls import path
from . import views

urlpatterns = [
    path("topics/<int:topic_id>/vote", views.vote_view, name="vote"),
    path("topics/<int:topic_id>/result", views.topic_result_view, name="topic-result"),
]
