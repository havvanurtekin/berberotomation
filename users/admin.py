from django.contrib import admin
from .models import Person, Customer, Employee

@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ("username", "get_full_name", "get_roles", "salon")
    list_filter = ("roles", "salon")   # MultiSelectField filtrelenebilir
    search_fields = ("username", "first_name", "last_name")

    def get_roles(self, obj):
        return ", ".join(obj.roles) if obj.roles else "-"
    get_roles.short_description = "Roller"


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ("username", "get_full_name", "salon")
    search_fields = ("username", "first_name", "last_name")

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(roles__contains="customer")


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ("username", "get_full_name", "salon")
    list_filter = ("salon",)
    search_fields = ("username", "first_name", "last_name")

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(roles__contains="employee")
