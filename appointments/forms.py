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
        widgets = {
            'salon': forms.Select(attrs={'class': 'form-select'}),
            'employee': forms.Select(attrs={'class': 'form-select'}),
            'service': forms.Select(attrs={'class': 'form-select'}),
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'start_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'end_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['salon'].widget.attrs.update({'class': 'form-select'})

        # Başlangıçta boş
        self.fields['employee'].queryset = Person.objects.none()
        self.fields['service'].queryset = Service.objects.none()

        # Salon seçildiyse filtrele
        data = self.data if self.is_bound else None
        salon_id = None
        if data and data.get('salon'):
            try:
                salon_id = int(data.get('salon'))
            except (TypeError, ValueError):
                salon_id = None

        if salon_id:
            self.fields['employee'].queryset = Person.objects.filter(is_employee=True, salon_id=salon_id)
            self.fields['service'].queryset = Service.objects.filter(salon_id=salon_id)
        elif self.instance and self.instance.salon_id:
            self.fields['employee'].queryset = Person.objects.filter(is_employee=True, salon_id=self.instance.salon_id)
            self.fields['service'].queryset = Service.objects.filter(salon_id=self.instance.salon_id)

    def clean(self):
        cleaned = super().clean()
        salon = cleaned.get("salon")
        employee = cleaned.get("employee")
        service = cleaned.get("service")
        date = cleaned.get("date")
        start = cleaned.get("start_time")
        end = cleaned.get("end_time")

        # Salon seçilmeden personel/hizmet seçilemez
        if not salon and (employee or service):
            raise forms.ValidationError("Lütfen önce salon seçin.")

        # Service varsa end_time otomatik hesapla
        if service and date and start:
            dt_start = datetime.datetime.combine(date, start)
            dt_end = dt_start + datetime.timedelta(minutes=service.duration)
            cleaned['end_time'] = dt_end.time()
            end = cleaned['end_time']

        # Çakışma kontrolü
        if employee and date and start and end:
            overlapping = Appointment.objects.filter(
                employee=employee,
                date=date,
                start_time__lt=end,
                end_time__gt=start
            ).exclude(pk=self.instance.pk)

            if overlapping.exists():
                raise forms.ValidationError("Bu saat aralığında çalışan zaten dolu.")

        # Başlangıç-bitiş kontrolü (15 dk kuralı)
        if start and end:
            dt_start = datetime.datetime.combine(date, start)
            dt_end = datetime.datetime.combine(date, end)
            diff_minutes = (dt_end - dt_start).total_seconds() / 60

            if end <= start:
                raise forms.ValidationError("Bitiş saati başlangıçtan önce olamaz.")
            if diff_minutes < 15:
                raise forms.ValidationError("Bitiş saati başlangıçtan en az 15 dakika sonra olmalı.")

        return cleaned

