from django.urls import path
from users.views import signup_view

urlpatterns = [
    path("signup/", signup_view, name="signup"),
]
