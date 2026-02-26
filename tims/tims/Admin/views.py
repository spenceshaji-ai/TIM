from django.shortcuts import render
from django.views import View 

# Create your views here.
class Home3View(View):
    def get(self, request):
        return render(request, "homee.html")