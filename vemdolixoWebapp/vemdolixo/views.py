from django.shortcuts import render
from vemdolixo.models import generic_register
from django.http import HttpResponse

# Create your views here.

def index(request):
    context = {}
    return render(request, 'index.html', context)

def generic_register_create(request):
	first_name_lower = request.POST['first_name']
	first_name_lower =first_name_lower.lower()
	last_name_lower = request.POST['last_name']
	last_name_lower = last_name_lower.lower()
	contact_email_lower = request.POST['contact_email']
	contact_email_lower = contact_email_lower.lower()
	new_reg = generic_register(first_name = first_name_lower, last_name = last_name_lower, email = contact_email_lower)
	new_reg.save()
	context = {}
	return render(request, 'thanks-for-register.html', context)