from django.contrib import admin
from .models import Person, Customer, Employee

# Ana kullanıcı modeli
@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ("username", "get_full_name", "is_customer", "is_employee", "salon")
    list_filter = ("is_customer", "is_employee", "salon")
    search_fields = ("username", "first_name", "last_name")

# Customer proxy modeli
@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ("username", "get_full_name")
    search_fields = ("username", "first_name", "last_name")

    def get_queryset(self, request):
        # sadece is_customer=True olanları göster
        qs = super().get_queryset(request)
        return qs.filter(is_customer=True)

# Employee proxy modeli
@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ("username", "get_full_name", "salon")
    list_filter = ("salon",)
    search_fields = ("username", "first_name", "last_name")

    def get_queryset(self, request):
        # sadece is_employee=True olanları göster
        qs = super().get_queryset(request)
        return qs.filter(is_employee=True)
