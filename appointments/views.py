from django.shortcuts import render, redirect
from .forms import AppointmentForm
from .models import Appointment
from django.http import JsonResponse
from employees.models import Employee
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required


def create_appointment(request):
    if request.method == "POST":
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.end_time = form.cleaned_data['end_time']
            appointment.customer = request.user
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


def appointment_list(request):
    appointments = Appointment.objects.filter(customer=request.user)
    return render(request, "appointments/list.html", {"appointments": appointments})

def appointment_calendar(request):
    try:
        employee = Employee.objects.get(user=request.user)
    except Employee.DoesNotExist:
        employee = None

    if employee:
        appointments = Appointment.objects.filter(employee=employee)
    else:
        appointments = Appointment.objects.none()  # veya uygun başka fallback

    return render(request, "appointments/calendar.html", {"appointments": appointments})

@login_required
def approve_appointment(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    if request.user.employee == appointment.employee:
        appointment.is_confirmed = True
        appointment.rejection_note = ""
        appointment.save()
    return redirect('appointment_calendar')


@login_required
def reject_appointment(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    if request.user.employee == appointment.employee and request.method == "POST":
        note = request.POST.get("rejection_note", "")
        appointment.is_confirmed = False
        appointment.rejection_note = note
        appointment.save()
    return redirect('appointment_calendar')

