from django.db import models
from django.contrib.auth.models import User
from salon.models import Service
from employees.models import Employee


class Appointment(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="appointments")
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_confirmed = models.BooleanField(default=False)
    rejection_note = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.customer} - {self.service.name} - {self.date}"
