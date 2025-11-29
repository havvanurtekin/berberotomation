from django.db import models
from users.models import Person  # user olarak Person kullanılıyor

class Notification(models.Model):
    user = models.ForeignKey(Person, on_delete=models.CASCADE, related_name="notifications")
    message = models.CharField(max_length=255)
    url = models.CharField(max_length=255)  # bildirime tıklanınca gidilecek adres
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} → {self.message}"
