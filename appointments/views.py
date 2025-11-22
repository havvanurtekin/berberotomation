from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .forms import AppointmentForm
from .models import Appointment, AppointmentStatus
from users.models import Person   # Employee proxy yerine Person + filtre

def create_appointment(request):
    if request.method == "POST":
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            # end_time form.clean() içinde hesaplanıyor
            appointment.end_time = form.cleaned_data['end_time']
            appointment.customer = request.user
            # snapshot alanlarını doldur
            appointment.price_snapshot = appointment.service.price
            appointment.duration_snapshot = appointment.service.duration
            appointment.save()

            # AJAX kontrolü
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({"message": "Randevu başarıyla oluşturuldu"})

            return redirect('appointment_list')
        else:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({"errors": form.errors}, status=400)
    else:
        form = AppointmentForm()

    return render(request, "appointments/create.html", {"form": form})


@login_required
def appointment_list(request):
    # sadece müşteri randevularını listele
    appointments = Appointment.objects.filter(customer=request.user)
    return render(request, "appointments/list.html", {"appointments": appointments})


@login_required
def appointment_calendar(request):
    # giriş yapan kullanıcı çalışan mı?
    if request.user.is_employee:
        appointments = Appointment.objects.filter(employee=request.user)
    else:
        appointments = Appointment.objects.none()
    return render(request, "appointments/calendar.html", {"appointments": appointments})


@login_required
def approve_appointment(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    # sadece ilgili çalışan onaylayabilir
    if request.user.is_employee and request.user == appointment.employee:
        appointment.status = AppointmentStatus.CONFIRMED
        appointment.rejection_note = ""
        appointment.save()
    return redirect('appointment_calendar')


@login_required
def reject_appointment(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    if request.user.is_employee and request.user == appointment.employee and request.method == "POST":
        note = request.POST.get("rejection_note", "")
        appointment.status = AppointmentStatus.REJECTED
        appointment.rejection_note = note
        appointment.save()
    return redirect('appointment_calendar')
