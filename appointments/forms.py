from django import forms
from .models import Appointment
from salon.models import Service, Salon
from users.models import Employee

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ["salon", "employee", "service", "date", "start_time"]
        widgets = {
            "salon": forms.Select(attrs={"class": "form-select", "id": "id_salon"}),
            "employee": forms.Select(attrs={"class": "form-select", "id": "id_employee"}),
            "service": forms.Select(attrs={"class": "form-select", "id": "id_service"}),
            "date": forms.DateInput(attrs={"class": "form-control", "type": "date", "id": "id_date"}),
            "start_time": forms.TimeInput(attrs={"class": "form-control", "type": "time", "id": "id_start_time"}),
        }

    def __init__(self, *args, **kwargs):
        salon_id = kwargs.pop("salon_id", None)
        super().__init__(*args, **kwargs)

        # Başlangıçta boş queryset
        self.fields["employee"].queryset = Employee.objects.none()
        self.fields["service"].queryset = Service.objects.none()

        # Eğer salon seçildiyse filtre uygula
        if salon_id:
            self.fields["employee"].queryset = Employee.objects.filter(salon_id=salon_id)
            self.fields["service"].queryset = Service.objects.filter(salon_id=salon_id)


