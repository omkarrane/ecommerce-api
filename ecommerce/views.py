from django.shortcuts import render, HttpResponse

# Create your views here.
def register_view(request):
    print("route called")
    return render(request, 'test.html')