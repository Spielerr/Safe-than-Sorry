from django.shortcuts import render

# Create your views here.

def banks(request):
	return render(request, 'interface/banks_i.html')