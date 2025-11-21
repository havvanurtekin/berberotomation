from django import forms
from .models import Appointment
from employees.models import Employee
from salon.models import Service
import datetime

class AppointmentForm(forms.ModelForm):
    salon = forms.ModelChoiceField(queryset=None, required=True)

    class Meta:
        model = Appointment
        fields = ['salon', 'employee', 'service', 'date', 'start_time', 'end_time']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from salon.models import Salon
        self.fields['salon'].queryset = Salon.objects.all()
        self.fields['employee'].queryset = Employee.objects.none()
        self.fields['service'].queryset = Service.objects.none()

        if 'salon' in self.data:
            try:
                salon_id = int(self.data.get('salon'))
                self.fields['employee'].queryset = Employee.objects.filter(salon_id=salon_id)
                self.fields['service'].queryset = Service.objects.filter(salon_id=salon_id)
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['employee'].queryset = self.instance.salon.employee_set.all()
            self.fields['service'].queryset = self.instance.salon.services.all()

    def clean(self):
        cleaned_data = super().clean()
        employee = cleaned_data.get("employee")
        date = cleaned_data.get("date")
        start_time = cleaned_data.get("start_time")
        service = cleaned_data.get("service")

        if employee and date and start_time and service:
            end_time = (datetime.datetime.combine(date, start_time) +
                        datetime.timedelta(minutes=service.duration)).time()

            overlapping = Appointment.objects.filter(
                employee=employee,
                date=date,
                start_time__lt=end_time,
                end_time__gt=start_time
            )
            if overlapping.exists():
                raise forms.ValidationError("Bu zaman diliminde çalışan zaten dolu.")

            cleaned_data['end_time'] = end_time

        return cleaned_data
