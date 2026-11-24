
from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.from django.http import HttpResponse

def index(request):
    base_template = (
        "base/base.html"
        if request.session.get("usuario_id")
        else "base-inicio.html"
    )

    return render(request, "home/index.html", {
        "base_template": base_template
    })


def sobre(request):
    return render(request, "home/sobre.html")


def contato(request):
    base_template = (
        "base/base.html"
        if request.session.get("usuario_id")
        else "base-inicio.html"
    )

    return render(request, "home/contato.html", {
        "base_template": base_template
    })
