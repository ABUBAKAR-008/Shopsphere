from django.shortcuts import render

def homemain(request):
    return render(request, 'index.html')