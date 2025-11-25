from django.shortcuts import render, redirect
from .forms import SignUpForm
from .models import Customer, Employee
from django.contrib.auth import authenticate, login, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm

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
            # Rolü belirle
            if role == "customer":
                user.__class__ = Customer
            else:
                user.__class__ = Employee
            user.save()
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
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("home")  # giriş sonrası ana sayfaya yönlendir
    else:
        form = AuthenticationForm()
    return render(request, "login.html", {"form": form})