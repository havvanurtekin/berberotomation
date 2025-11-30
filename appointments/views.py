from datetime import datetime, timedelta
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .forms import AppointmentForm
from .models import Appointment, AppointmentStatus
from salon.models import Salon, Service
from users.models import Employee
from notifications.models import Notification


def generate_available_slots(employee, salon, date, service):
    start = datetime.combine(date, salon.opening_time)
    end = datetime.combine(date, salon.closing_time)

    existing = Appointment.objects.filter(employee=employee, date=date)
    duration = service.duration if service else 15

    slots = []
    while start + timedelta(minutes=duration) <= end:
        slot_start = start
        slot_end = start + timedelta(minutes=duration)

        # Bu slotta var olan randevu var mı?
        appointment = next(
            (a for a in existing
             if slot_start.time() == a.start_time and slot_end.time() == a.end_time),
            None
        )

        if appointment:
            if appointment.status == AppointmentStatus.PENDING:
                status = "pending"   # turuncu
            elif appointment.status == AppointmentStatus.CONFIRMED:
                status = "confirmed" # kırmızı
            elif appointment.status == AppointmentStatus.REJECTED:
                status = "free"      # yeşil (tekrar kullanılabilir)
            else:
                status = "busy"
        else:
            status = "free"

        slots.append({
            "start": slot_start.time().strftime("%H:%M"),
            "end": slot_end.time().strftime("%H:%M"),
            "status": status
        })

        # Sonraki slot
        start += timedelta(minutes=duration)

    return slots


@login_required
def create_appointment(request):
    if request.method == "POST":
        form = AppointmentForm(request.POST, available_slots=[])
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.customer = request.user
            appointment.save()

            Notification.objects.create(
                user=appointment.employee,
                message=f"{appointment.customer} yeni randevu talep etti.",
                url="/appointments/calendar/"
            )

            if request.headers.get("x-requested-with") == "XMLHttpRequest":
                return JsonResponse({"message": "Randevu başarıyla oluşturuldu"})
            return redirect("appointment_list")

        if request.headers.get("x-requested-with") == "XMLHttpRequest":
            return JsonResponse({"errors": form.errors}, status=400)
    else:
        form = AppointmentForm(request.GET or None, available_slots=[])

    busy_slots = [
        {"employee": a.employee, "date": a.date, "start": a.start_time, "end": a.end_time}
        for a in Appointment.objects.all()
    ]

    available_slots = []
    salon = form.data.get("salon")
    employee = form.data.get("employee")
    service = form.data.get("service")
    date_str = form.data.get("date")

    if salon and employee and service and date_str:
        try:
            salon_obj = Salon.objects.get(pk=salon)
            employee_obj = Employee.objects.get(pk=employee)
            service_obj = Service.objects.get(pk=service)
            date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
            available_slots = generate_available_slots(employee_obj, salon_obj, date_obj, service_obj)
        except Exception as e:
            print("Slot error:", e)

    form = AppointmentForm(request.POST or None, available_slots=available_slots, initial={
        "salon": salon,
        "employee": employee,
        "service": service,
        "date": date_str,
    })

    return render(request, "appointments/create.html", {
        "form": form,
        "busy_slots": busy_slots,
        "available_slots": available_slots,
    })




@login_required
def appointment_list(request):
    # sadece giriş yapan müşterinin randevuları
    appointments = Appointment.objects.filter(customer=request.user)
    return render(request, "appointments/list.html", {"appointments": appointments})


@login_required
def appointment_calendar(request):
    # sadece çalışan kendi takvimini görebilir
    if request.user.is_employee:
        appointments = Appointment.objects.filter(employee=request.user)
    else:
        appointments = Appointment.objects.none()
    return render(request, "appointments/calendar.html", {"appointments": appointments})


@login_required
def approve_appointment(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    if request.user.is_employee and request.user == appointment.employee:
        appointment.status = AppointmentStatus.CONFIRMED
        appointment.rejection_note = ""
        appointment.save()

        Notification.objects.create(
            user=appointment.customer,
            message=f"Randevu talebiniz {appointment.get_status_display()} oldu.",
            url="/appointments/list/"
        )

    return redirect("appointment_calendar")


@login_required
def reject_appointment(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    if request.user.is_employee and request.user == appointment.employee and request.method == "POST":
        note = request.POST.get("rejection_note", "")
        appointment.status = AppointmentStatus.REJECTED
        appointment.rejection_note = note
        appointment.save()

        Notification.objects.create(
            user=appointment.customer,
            message=f"Randevu talebiniz {appointment.get_status_display()} oldu.",
            url="/appointments/list/"
        )

    return redirect("appointment_calendar")
