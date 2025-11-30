from django import forms
from datetime import datetime
from .models import Appointment
from salon.models import Salon, Service
from users.models import Employee

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ["salon", "employee", "service", "date", "start_time", "end_time"]
        widgets = {
            "salon": forms.Select(attrs={"class": "form-select", "id": "id_salon"}),
            "employee": forms.Select(attrs={"class": "form-select", "id": "id_employee"}),
            "service": forms.Select(attrs={"class": "form-select", "id": "id_service"}),
            "date": forms.DateInput(attrs={"class": "form-control", "type": "date", "id": "id_date"}),
            "start_time": forms.HiddenInput(),   # gizli input
            "end_time": forms.HiddenInput(),     # gizli input
        }

    def __init__(self, *args, **kwargs):
        available_slots = kwargs.pop("available_slots", None)
        super().__init__(*args, **kwargs)

        self.fields["salon"].queryset = Salon.objects.all()
        self.fields["employee"].queryset = Employee.objects.none()
        self.fields["service"].queryset = Service.objects.none()

        salon_id = self.data.get("salon") or self.initial.get("salon")
        if salon_id:
            self.fields["employee"].queryset = Employee.objects.filter(salon_id=salon_id)

        employee_id = self.data.get("employee") or self.initial.get("employee")
        if employee_id:
            try:
                employee = Employee.objects.get(pk=employee_id)
                self.fields["service"].queryset = employee.services.all()
            except Employee.DoesNotExist:
                self.fields["service"].queryset = Service.objects.none()
