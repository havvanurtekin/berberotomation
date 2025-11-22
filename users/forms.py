from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Person  # Custom user model

class SignUpForm(UserCreationForm):
    class Meta:
        model = Person
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "password1",
            "password2",
            "is_customer",
            "is_employee",
            "salon",
            "phone_number",  # eğer Person modelinde varsa
            "address",  # varsa
        )