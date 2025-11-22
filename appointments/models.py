from django.db import models
from users.models import Person
from salon.models import Service, Salon
import datetime

class AppointmentStatus(models.TextChoices):
    PENDING = "pending", "Beklemede"
    CONFIRMED = "confirmed", "Onaylandı"
    REJECTED = "rejected", "Reddedildi"
    CANCELLED = "cancelled", "İptal"
    NO_SHOW = "no_show", "Gelmedi"

class Appointment(models.Model):
    customer = models.ForeignKey(
        Person,
        on_delete=models.CASCADE,
        limit_choices_to={"is_customer": True},
        related_name="appointments_as_customer"
    )
    employee = models.ForeignKey(
        Person,
        on_delete=models.CASCADE,
        limit_choices_to={"is_employee": True},
        related_name="appointments_as_employee"
    )
    salon = models.ForeignKey(Salon, on_delete=models.PROTECT)
    service = models.ForeignKey(Service, on_delete=models.PROTECT)

    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()

    status = models.CharField(
        max_length=20,
        choices=AppointmentStatus.choices,
        default=AppointmentStatus.PENDING
    )
    rejection_note = models.TextField(blank=True, null=True)

    price_snapshot = models.DecimalField(max_digits=10, decimal_places=2)
    duration_snapshot = models.PositiveIntegerField()

    class Meta:
        ordering = ["-date", "-start_time"]

    def __str__(self):
        return f"{self.customer} - {self.service.name} - {self.date} {self.start_time}"

    def clean(self):
        if not self.duration_snapshot and self.service:
            self.duration_snapshot = self.service.duration
        if not self.price_snapshot and self.service:
            self.price_snapshot = self.service.price

        if not self.end_time and self.start_time and self.duration_snapshot:
            dt_start = datetime.datetime.combine(self.date, self.start_time)
            dt_end = dt_start + datetime.timedelta(minutes=self.duration_snapshot)
            self.end_time = dt_end.time()

        if self.start_time and self.end_time and self.start_time >= self.end_time:
            raise ValueError("Başlangıç saati bitişten önce olmalı.")
