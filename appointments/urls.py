from django.urls import path
from . import views

urlpatterns = [
    path("create/", views.create_appointment, name="appointment_create"),
    path("list/", views.appointment_list, name="appointment_list"),
    path("calendar/", views.appointment_calendar, name="appointment_calendar"),
    path('approve/<int:pk>/', views.approve_appointment, name='approve_appointment'),
    path('reject/<int:pk>/', views.reject_appointment, name='reject_appointment'),
]
