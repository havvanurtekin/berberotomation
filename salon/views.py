from django.shortcuts import render

def salon_list(request):
    return render(request, "salon/list.html")
