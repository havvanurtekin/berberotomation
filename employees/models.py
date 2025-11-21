from django.db import models
from django.contrib.auth.models import User
from salon.models import Salon, Service


class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    salon = models.ForeignKey(Salon, on_delete=models.CASCADE)
    specialties = models.ManyToManyField(Service, blank=True)

    def __str__(self):
        return self.user.get_full_name()


class Availability(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
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
