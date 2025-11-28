from django.urls import path
from . import views

urlpatterns = [
    path("list/", views.salon_list, name="salon_list"),
    path("<int:pk>/", views.salon_detail, name="salon_detail"),
]
