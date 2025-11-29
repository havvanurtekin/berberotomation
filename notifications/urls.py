from django.urls import path
from . import views

urlpatterns = [
    path("read/<int:pk>/", views.mark_notification_read, name="mark_notification_read"),
]
