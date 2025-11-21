from django.contrib import admin
from django.urls import path, include
from .views import home

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", home, name="home"),
    path("appointments/", include("appointments.urls")),
    path("salon/", include("salon.urls")),
    path("employees/", include("employees.urls")),
]
