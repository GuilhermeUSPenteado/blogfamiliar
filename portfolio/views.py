from django.shortcuts import render

def about(request):
    return render(request, 'portfolio/about.html')

def index(request):
    return render(request, 'portfolio/index.html')