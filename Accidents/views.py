from django.shortcuts import render
from .models import *
# Create your views here.

def index(request):
	accidents = Accident.objects.all();
	for accident in accidents:
		print type(accident.location)
		print accident.location
		accident.location = accident.location.encode('utf-8').replace("\n","")
	return render(request, "Accidents/index2.djt", {'accidents':accidents})