from django.db import models
from users.models import Person
from salon.models import Service, Salon
import datetime
from django.core.exceptions import ValidationError

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
    end_time = models.TimeField(blank=True, null=True)

    status = models.CharField(
        max_length=20,
        choices=AppointmentStatus.choices,
        default=AppointmentStatus.PENDING
    )
    rejection_note = models.TextField(blank=True, null=True)

    # Snapshot alanları artık opsiyonel
    price_snapshot = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    duration_snapshot = models.PositiveIntegerField(blank=True, null=True)

    class Meta:
        ordering = ["-date", "-start_time"]

    def __str__(self):
        service_name = self.service.name if self.service_id else "Hizmet Yok"
        return f"{self.customer} - {service_name} - {self.date} {self.start_time}"
    def clean(self):
        # 1) Hizmet erişimini sadece id varsa yap
        if self.service_id:
            # self.service'e erişim artık güvenli
            service = self.service
            if self.duration_snapshot is None:
                self.duration_snapshot = service.duration
            if self.price_snapshot is None:
                self.price_snapshot = service.price

        # 2) end_time yalnızca tüm girdiler doluysa hesapla
        if self.end_time is None and self.date and self.start_time and self.duration_snapshot:
            dt_start = datetime.datetime.combine(self.date, self.start_time)
            dt_end = dt_start + datetime.timedelta(minutes=self.duration_snapshot)
            self.end_time = dt_end.time()

        # 3) Saat mantığı kontrolü (ValidationError kullan)
        if self.start_time and self.end_time and self.start_time >= self.end_time:
            raise ValidationError("Başlangıç saati bitişten önce olmalı.")