from django.shortcuts import render,redirect,reverse


def index(request):
    return render(request,"index.html")

def test(request):
    return render(request,"uc_base.html")