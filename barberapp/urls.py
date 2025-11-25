from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from .views import home
from users.forms import LoginForm

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", home, name="home"),
    path("login/", auth_views.LoginView.as_view(
        template_name="login.html",
        authentication_form=LoginForm
    ), name="login"),
    path("users/", include("users.urls")),
    path("appointments/", include("appointments.urls")),
    path("salon/", include("salon.urls")),
    path("accounts/", include("users.urls")),
]
