from django.shortcuts import render, get_object_or_404
from .models import Salon

def salon_list(request):
    salons = Salon.objects.all()
    return render(request, "salon/list.html", {"salons": salons})

def salon_detail(request, pk):
    salon = get_object_or_404(Salon, pk=pk)
    return render(request, "salon/detail.html", {"salon": salon})