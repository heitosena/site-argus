from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.from django.http import HttpResponse

def index(request):
    return render(request, "home/index.html")

def sobre(request):
    return render(request, "home/sobre.html")

def contato(request):
    return render(request, "home/contato.html")