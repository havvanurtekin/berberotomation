from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm

from .forms import SignUpForm
from .models import Customer, Employee


def signup_view(request, role="customer"):
    """
    Tek bir signup sayfası. Varsayılan rol 'customer'.
    Eğer role parametresi verilmezse müşteri kaydı yapılır.
    """
    if role not in ["customer", "employee"]:
        role = "customer"  # default müşteri

    if request.method == "POST":
        form = SignUpForm(request.POST, role=role)
        if form.is_valid():
            user = form.save(commit=False)

            # Proxy model üzerinden kaydet
            if role == "customer":
                user = Customer.objects.create(**user.__dict__)
            else:
                user = Employee.objects.create(**user.__dict__)

            login(request, user)  # kayıt sonrası otomatik giriş
            return redirect("home")
    else:
        form = SignUpForm(role=role)

    return render(request, "signup.html", {"form": form, "role": role})


@login_required
def logout_view(request):
    logout(request)
    return redirect("home")


def login_view(request):
    """
    Basit login view. Django'nun AuthenticationForm'u kullanılıyor.
    """
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("home")
    else:
        form = AuthenticationForm()

    return render(request, "login.html", {"form": form})
