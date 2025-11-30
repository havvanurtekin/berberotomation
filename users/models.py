from django.contrib.auth.models import AbstractUser
from django.db import models
from salon.models import Salon
from django.core.exceptions import ValidationError
from multiselectfield import MultiSelectField
class Person(AbstractUser):
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    ROLE_CHOICES = [
        ("customer", "Customer"),
        ("employee", "Employee"),
    ]
    roles = MultiSelectField(max_length=20, choices=ROLE_CHOICES, default="customer")
    # Çalışanlar için
    salon = models.ForeignKey(Salon, on_delete=models.SET_NULL, null=True, blank=True)
    def __str__(self):
        return self.get_full_name() or self.username

    @property
    def is_employee(self):
        # Proxy üzerinden kontrol
        return Employee.objects.filter(pk=self.pk).exists()

    @property
    def is_customer(self):
        return Customer.objects.filter(pk=self.pk).exists()


class Customer(Person):
    class Meta:
        proxy = True


class Employee(Person):
    class Meta:
        proxy = True


class Availability(models.Model):
    employee = models.ForeignKey(Person, on_delete=models.CASCADE)
    day = models.CharField(
        max_length=10,
        choices=[
            ("Mon", "Monday"), ("Tue", "Tuesday"), ("Wed", "Wednesday"),
            ("Thu", "Thursday"), ("Fri", "Friday"), ("Sat", "Saturday"), ("Sun", "Sunday")
        ]
    )
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f"{self.employee} - {self.day} {self.start_time}-{self.end_time}"

    def clean(self):
        # Proxy üzerinden kontrol
        if not Employee.objects.filter(pk=self.employee.pk).exists():
            raise ValidationError("Sadece çalışanlar için uygunluk tanımlanabilir.")

class Role(models.Model):
    name = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.name
