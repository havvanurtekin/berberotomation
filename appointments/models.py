from django.db import models
from django.core.exceptions import ValidationError
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
        related_name="appointments_as_customer"
    )
    employee = models.ForeignKey(
        Person,
        on_delete=models.CASCADE,
        related_name="appointments_as_employee"
    )
    salon = models.ForeignKey(Salon, on_delete=models.PROTECT)
    service = models.ForeignKey(Service, on_delete=models.PROTECT)

    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField(blank=True, null=True)

    status = models.CharField(
        max_length=20,
        choices=AppointmentStatus.choices,
        default=AppointmentStatus.PENDING
    )
    rejection_note = models.TextField(blank=True, null=True)

    price_snapshot = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    duration_snapshot = models.PositiveIntegerField(blank=True, null=True)

    class Meta:
        ordering = ["-date", "-start_time"]

    def __str__(self):
        service_name = self.service.name if self.service_id else "Hizmet Yok"
        return f"{self.customer} - {service_name} - {self.date} {self.start_time}"

    def clean(self):
        # Hizmet snapshot bilgilerini doldur
        if self.service_id:
            if self.duration_snapshot is None:
                self.duration_snapshot = self.service.duration
            if self.price_snapshot is None:
                self.price_snapshot = self.service.price

        # end_time hesapla
        if self.end_time is None and self.date and self.start_time and self.duration_snapshot:
            dt_start = datetime.datetime.combine(self.date, self.start_time)
            dt_end = dt_start + datetime.timedelta(minutes=self.duration_snapshot)
            self.end_time = dt_end.time()

        # Mantık kontrolü
        if self.start_time and self.end_time and self.start_time >= self.end_time:
            raise ValidationError("Başlangıç saati bitişten önce olmalı.")
