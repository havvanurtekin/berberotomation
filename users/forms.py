from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Person
from django.contrib.auth.forms import AuthenticationForm

class SignUpForm(UserCreationForm):
    class Meta:
        model = Person
        fields = [
            "username", "email", "first_name", "last_name",
            "password1", "password2",
            "phone_number", "address", "salon"
        ]
        widgets = {
            "salon": forms.Select(attrs={"class": "form-select"}),
            "phone_number": forms.TextInput(attrs={"class": "form-control"}),
            "address": forms.Textarea(attrs={"class": "form-control", "rows": 2}),
        }

    def __init__(self, *args, **kwargs):
        role = kwargs.pop("role", None)
        super().__init__(*args, **kwargs)

        # Tüm alanlara Bootstrap class ekle
        for field_name, field in self.fields.items():
            if not isinstance(field.widget, forms.Select):
                field.widget.attrs.update({"class": "form-control"})
            else:
                field.widget.attrs.update({"class": "form-select"})

        # Eğer müşteri ise salon alanını gizle
        if role == "customer":
            self.fields.pop("salon")
        # Eğer çalışan ise salon zorunlu olsun
        elif role == "employee":
            self.fields["salon"].required = True

class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({"class": "form-control"})