from django.contrib import admin
from .models import Appointment

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = (
        "customer",
        "employee",
        "salon",
        "service",
        "date",
        "start_time",
        "end_time",
        "status",
    )
    list_filter = ("status", "salon", "date", "employee")
    search_fields = ("customer__username", "employee__username", "service__name")
    ordering = ("-date", "-start_time")

    # readonly alanlar (snapshot değerleri geçmişi korumak için)
    readonly_fields = ("price_snapshot", "duration_snapshot")

    fieldsets = (
        (None, {
            "fields": (
                "customer",
                "employee",
                "salon",
                "service",
                "date",
                "start_time",
                "end_time",
                "status",
                "rejection_note",
            )
        }),
        ("Snapshot Bilgileri", {
            "fields": ("price_snapshot", "duration_snapshot"),
            "classes": ("collapse",),
        }),
    )
