from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from .views import home
from users.views import signup_view
urlpatterns = [
    path('admin/', admin.site.urls),
    path("", home, name="home"),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path("signup/", signup_view, name="signup"),
    path("appointments/", include("appointments.urls")),
    path("salon/", include("salon.urls")),
    path("accounts/", include("users.urls")),
]
