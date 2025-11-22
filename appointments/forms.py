from django import forms
from .models import Appointment
from users.models import Person
from salon.models import Service, Salon
import datetime

class AppointmentForm(forms.ModelForm):
    salon = forms.ModelChoiceField(queryset=Salon.objects.all(), required=True)

    class Meta:
        model = Appointment
        fields = ['salon', 'employee', 'service', 'date', 'start_time', 'end_time']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['employee'].queryset = Person.objects.filter(is_employee=True)
        self.fields['service'].queryset = Service.objects.none()

        if 'salon' in self.data:
            try:
                salon_id = int(self.data.get('salon'))
                self.fields['employee'].queryset = Person.objects.filter(is_employee=True, salon_id=salon_id)
                self.fields['service'].queryset = Service.objects.filter(salon_id=salon_id)
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['employee'].queryset = Person.objects.filter(is_employee=True, salon=self.instance.salon)
            self.fields['service'].queryset = Service.objects.filter(salon=self.instance.salon)

    def clean(self):
        cleaned_data = super().clean()
        employee = cleaned_data.get("employee")
        date = cleaned_data.get("date")
        start_time = cleaned_data.get("start_time")
        service = cleaned_data.get("service")

        if employee and date and start_time and service:
            dt_start = datetime.datetime.combine(date, start_time)
            dt_end = dt_start + datetime.timedelta(minutes=service.duration)
            end_time = dt_end.time()

            overlapping = Appointment.objects.filter(
                employee=employee,
                date=date,
                start_time__lt=end_time,
                end_time__gt=start_time
            ).exclude(pk=self.instance.pk)

            if overlapping.exists():
                raise forms.ValidationError("Bu zaman diliminde çalışan zaten dolu.")

            cleaned_data['end_time'] = end_time

        return cleaned_data
