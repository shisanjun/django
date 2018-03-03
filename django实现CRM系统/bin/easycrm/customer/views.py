from django.shortcuts import render,HttpResponse

# Create your views here.

def customer(request):
    return HttpResponse("OK")

def tags(request):
    return HttpResponse("OK")