from django.contrib import admin
from .models import Person, Customer, Employee

# Ana kullanıcı modeli
@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ("username", "get_full_name", "role", "salon")
    list_filter = ("salon",)
    search_fields = ("username", "first_name", "last_name")

    def role(self, obj):
        if isinstance(obj, Customer):
            return "Customer"
        elif isinstance(obj, Employee):
            return "Employee"
        return "Person"
    role.short_description = "Rol"

# Customer proxy modeli
@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ("username", "get_full_name")
    search_fields = ("username", "first_name", "last_name")

    def get_queryset(self, request):
        # Proxy zaten Customer'ları gösterir
        return super().get_queryset(request)

# Employee proxy modeli
@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ("username", "get_full_name", "salon")
    list_filter = ("salon",)
    search_fields = ("username", "first_name", "last_name")

    def get_queryset(self, request):
        # Proxy zaten Employee'leri gösterir
        return super().get_queryset(request)
