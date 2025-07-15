from django.urls import path
from . import views

urlpatterns = [
    path("topics", views.topics_view, name="topics"),
    path("topics/<int:topic_id>", views.topic_detail_view, name="topic-detail"),
    path(
        "topics/<int:topic_id>/session", views.start_session_view, name="start-session"
    ),
]
