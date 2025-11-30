from django.db import models


class Salon(models.Model):
    name = models.CharField(max_length=150)
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=20, blank=True, null=True)
    opening_time = models.TimeField()
    closing_time = models.TimeField()
    image = models.ImageField(upload_to="salons/", blank=True, null=True)

    def __str__(self):
        return self.name

    @property
    def employees(self):
        return self.person_set.filter(is_staff=True)  # veya Employee proxy üzerinden

    @property
    def services(self):
        return self.service_set.all()

class Service(models.Model):
    salon = models.ForeignKey(Salon, on_delete=models.CASCADE, related_name="service_set")
    name = models.CharField(max_length=150)
    duration = models.IntegerField(help_text="Süre (dakika)")
    price = models.DecimalField(max_digits=6, decimal_places=2)
    employees = models.ManyToManyField("users.Person", related_name="services", blank=True)

    def __str__(self):
        return f"{self.name}"
