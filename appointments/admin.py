from django.contrib import admin
from .models import Appointment

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('customer', 'employee', 'service', 'date', 'start_time', 'end_time', 'is_confirmed')
    list_filter = ('is_confirmed', 'date', 'employee')
    actions = ['confirm_appointments']

    def confirm_appointments(self, request, queryset):
        queryset.update(is_confirmed=True)
        self.message_user(request, "Seçili randevular onaylandı.")
    confirm_appointments.short_description = "Seçili randevuları onayla"
