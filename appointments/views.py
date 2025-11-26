from datetime import datetime, timedelta
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .forms import AppointmentForm
from .models import Appointment, AppointmentStatus
from salon.models import Salon, Service
from users.models import Employee


def generate_available_slots(employee, salon, date, service):
    """
    Çalışanın seçilen tarihteki uygun slotlarını üretir.
    - Salonun açılış/kapanış saatleri baz alınır
    - Çalışanın mevcut randevuları dolu kabul edilir
    - Slot süresi seçilen hizmetin duration değerine göre belirlenir
    """

    # Salonun mesai saatlerini al
    start = datetime.combine(date, salon.opening_time)
    end = datetime.combine(date, salon.closing_time)

    # Çalışanın o günkü randevularını al
    existing = Appointment.objects.filter(employee=employee, date=date)
    busy_ranges = [
        (datetime.combine(date, a.start_time), datetime.combine(date, a.end_time))
        for a in existing
    ]

    # Hizmet süresi
    duration = service.duration if service else 15

    slots = []
    while start + timedelta(minutes=duration) <= end:
        slot_start = start
        slot_end = start + timedelta(minutes=duration)

        # Çakışma kontrolü
        overlaps = any(
            slot_start < busy_end and slot_end > busy_start
            for busy_start, busy_end in busy_ranges
        )

        slots.append({
            "start": slot_start.time().strftime("%H:%M"),
            "end": slot_end.time().strftime("%H:%M"),
            "status": "busy" if overlaps else "free"
        })

        # Sonraki slot
        start += timedelta(minutes=duration)
    print(slots)
    return slots


@login_required
def create_appointment(request):
    salon_id = request.GET.get("salon") or request.POST.get("salon")
    print(salon_id)
    if request.method == "POST":
        form = AppointmentForm(request.POST, salon_id=salon_id)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.customer = request.user

            if appointment.service_id:
                appointment.price_snapshot = appointment.service.price
                appointment.duration_snapshot = appointment.service.duration

                # Bitiş saatini hesapla
                dt_start = datetime.combine(appointment.date, appointment.start_time)
                dt_end = dt_start + timedelta(minutes=appointment.duration_snapshot)
                appointment.end_time = dt_end.time()

            appointment.save()

            if request.headers.get("x-requested-with") == "XMLHttpRequest":
                return JsonResponse({"message": "Randevu başarıyla oluşturuldu"})
            return redirect("appointment_list")

        if request.headers.get("x-requested-with") == "XMLHttpRequest":
            return JsonResponse({"errors": form.errors}, status=400)
    else:
        form = AppointmentForm(request.GET or None, salon_id=salon_id)

    busy_slots = [
        {
            "employee": a.employee,
            "date": a.date,
            "start": a.start_time,
            "end": a.end_time,
        }
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

    return render(request, "appointments/create.html", {
        "form": form,
        "busy_slots": busy_slots,
        "available_slots": available_slots,
    })



@login_required
def calculate_end_time(request):
    service_id = request.GET.get("service_id")
    start_time = request.GET.get("start_time")
    date = request.GET.get("date")

    try:
        service = Service.objects.get(pk=service_id)
        dt_start = datetime.strptime(f"{date} {start_time}", "%Y-%m-%d %H:%M")
        dt_end = dt_start + timedelta(minutes=service.duration)
        return JsonResponse({"end_time": dt_end.strftime("%H:%M")})
    except Exception:
        return JsonResponse({"error": "Hesaplama yapılamadı"}, status=400)

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
    return redirect("appointment_calendar")


@login_required
def reject_appointment(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    if request.user.is_employee and request.user == appointment.employee and request.method == "POST":
        note = request.POST.get("rejection_note", "")
        appointment.status = AppointmentStatus.REJECTED
        appointment.rejection_note = note
        appointment.save()
    return redirect("appointment_calendar")
