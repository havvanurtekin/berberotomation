from django.contrib.auth.models import AbstractUser
from django.db import models
from salon.models import Salon, Service
from django.core.exceptions import ValidationError

class Person(AbstractUser):
    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    # çalışanlar için
    salon = models.ForeignKey(Salon, on_delete=models.SET_NULL, null=True, blank=True)
    specialties = models.ManyToManyField(Service, blank=True)

    def __str__(self):
        return self.get_full_name()

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
        if not isinstance(self.employee, Employee):
            raise ValidationError("Sadece çalışanlar için uygunluk tanımlanabilir.")