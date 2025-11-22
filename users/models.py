from django.contrib.auth.models import AbstractUser
from django.db import models
from salon.models import Salon, Service

class Person(AbstractUser):
    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    is_customer = models.BooleanField(default=False)
    is_employee = models.BooleanField(default=False)
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

    def save(self, *args, **kwargs):
        self.is_customer = True
        super().save(*args, **kwargs)


class Employee(Person):
    class Meta:
        proxy = True

    def save(self, *args, **kwargs):
        self.is_employee = True
        super().save(*args, **kwargs)

class Availability(models.Model):
    employee = models.ForeignKey(Person, on_delete=models.CASCADE, limit_choices_to={"is_employee": True})
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
