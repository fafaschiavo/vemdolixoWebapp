# -*- coding: utf-8 -*-
import sys
from django.shortcuts import render
from django.conf import settings
from vemdolixo.models import generic_register, company, residue, receptivity, members, search_history, residue_association
from django.http import HttpResponse
from difflib import SequenceMatcher
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import EmailMultiAlternatives
from django.core.mail import EmailMessage
import json
import googlemaps
from datetime import datetime
import re
import decimal

# Create your procedures here.

def mandrill_form_request(name, email, message):
	msg = EmailMessage(subject="Form Request", from_email="VemDoLixo <atendimento@vemdolixo.com.br>", to=["atendimento@vemdolixo.com.br"])
	msg.template_name = "form-request"
	msg.global_merge_vars = {'NAME': name, 'EMAIL': email, 'MESSAGE': message}
	msg.send()
	return None

def mandrill_generic_request(email, text):
	msg = EmailMultiAlternatives("Requisição Formulário", "text body", "atendimento@vemdolixo.com.br", [email])
	email_text = "<html>" + text + "</html>"
	msg.attach_alternative(email_text, "text/html")
	msg.send()
	return None

msg = EmailMultiAlternatives("Subject", "text body",
                             "from@example.com", ["to@example.com"])
msg.attach_alternative("<html>html body</html>", "text/html")

def convert_characters(string_to_convert):
	reload(sys)
	sys.setdefaultencoding('UTF8')
	converted_string = string_to_convert
	converted_string = converted_string.replace("Ã§", "ç")
	converted_string = converted_string.replace("Ã£", "ã")
	converted_string = converted_string.replace("Ã¡", "á")
	converted_string = converted_string.replace("Ã©", "é")
	converted_string = converted_string.replace("Ãº", "ú")
	converted_string = converted_string.replace("Ã³", "ó")
	converted_string = converted_string.replace("Ã´", "ô")
	converted_string = converted_string.replace("Ã", "í")
	return converted_string

def calculate_distance(lat1, lon1, lat2, lon2):
	lat1 = float(lat1)
	lat2 = float(lat2)
	lon1 = float(lon1)
	lon2 = float(lon2)
	distance_lat = (lat1 - lat2) ** 2
	distance_lon = (lon1 - lon2) ** 2
	distance = (distance_lat + distance_lon) ** (0.5)
	return distance

def verify_http_url(url):
	new_url = url
	if "http://" not in url: 
		new_url = "http://" + url
	return new_url

def rank_string_similarity_with_residues_type(string_to_test):
	residues = residue_association.objects.all()
	match_array = {}
	for residue_type in residues:
		result = SequenceMatcher(None, string_to_test, residue_type.term).ratio()
		original_residue = residue.objects.filter(id = residue_type.residue_id)
		match_array[result] = original_residue

	score_array = sorted(match_array, reverse=True)

	result_array = {}
	index = 0
	for score in score_array:
		result_array[index] = match_array[score][0]
		index = index + 1

	return result_array

def best_match_with_residues_type(string_to_test):
	residues = residue_association.objects.all()
	match_array = {}
	for residue_type in residues:
		result = SequenceMatcher(None, string_to_test, residue_type.term).ratio()
		original_residue = residue.objects.filter(id = residue_type.residue_id)
		match_array[result] = original_residue

	score_array = sorted(match_array, reverse=True)
	
	result_array = {}
	index = 0
	for score in score_array:
		result_array[index] = match_array[score]
		index = index + 1

	return result_array[0]

# Create your views here.

def index(request):
	residues = residue.objects.all()
	autocomplete_residue = ''
	for residue_type in residues:
		autocomplete_residue = autocomplete_residue + "'" + convert_characters(residue_type.residue_name) + "',"

	context = {
		'autocomplete_residue': autocomplete_residue,
	}
	return render(request, 'index.html', context)

def about(request):
	context = {}
	return render(request, 'about.html', context)

def simple_register_create(request):
	first_name_lower = ''
	last_name_lower = ''
	contact_email_lower = request.POST['contact_email']
	contact_email_lower = contact_email_lower.lower()
	try:
		new_reg = generic_register(first_name = first_name_lower, last_name = last_name_lower, email = contact_email_lower)
		new_reg.save()
		return HttpResponse(200)
	except:
		return HttpResponse(400)

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

def footer_form(request):
	fullname = request.POST['fullname']
	email = request.POST['email']
	message = request.POST['message']

	first_name = fullname.split(' ', 1)[0]
	first_name_lower = first_name.lower()
	last_name = fullname.rsplit(' ', 1)[1]
	last_name_lower = last_name.lower()
	contact_email_lower = email.lower()
	new_reg = generic_register(first_name = first_name_lower, last_name = last_name_lower, email = contact_email_lower)
	new_reg.save()

	mandrill_form_request(fullname, email, message)
	context = {}
	return render(request, 'thanks-for-register.html', context)

@csrf_exempt
def new_search(request):
	name1 = ''
	name2 = ''
	name3 = ''

	email1 = ''
	email2 = ''
	email3 = ''

	tel1 = ''
	tel2 = ''
	tel3 = ''

	address1 = ''
	address2 = ''
	address3 = ''

	site1 = ''
	site2 = ''
	site3 = ''

	user_cep = request.POST['user_cep']
	gmaps = googlemaps.Client(key=settings.GOOGLE_API_KEY)
	geocode_result = gmaps.geocode(user_cep)


	if len(geocode_result) >= 1:
		lat_user = geocode_result[0]['geometry']['location']['lat']
		lon_user = geocode_result[0]['geometry']['location']['lng']
	elif len(user_cep) == 8:
		formated_cep = user_cep[:5] + '-' + user_cep[5:]
		geocode_result = gmaps.geocode(formated_cep)
		if len(geocode_result) >= 1:
			lat_user = geocode_result[0]['geometry']['location']['lat']
			lon_user = geocode_result[0]['geometry']['location']['lng']
		else:
			context = {}
			return render(request, 'location-not-found.html', context)
	else:
		context = {}
		return render(request, 'location-not-found.html', context)

	is_brazil = False
	for information_set in geocode_result[0]['address_components']:
		if information_set['long_name'] == 'Brazil':
			is_brazil = True
	if is_brazil == False:
		context = {}
		return render(request, 'location-not-found.html', context)

	companies = company.objects.filter(is_active = 1)
	distance_array = {}
	for company_item in companies:
		distance = calculate_distance(lat_user, lon_user, company_item.latitude, company_item.longitude)
		distance_array[distance] = company_item

	residue_best_match = best_match_with_residues_type(request.POST['residue_type'])

	try:
		residues = residue.objects.get(residue_name = residue_best_match.residue_name)
		receptivities = receptivity.objects.filter(residue_id = residues.id)
		for distance in sorted(distance_array):
			flag = 0
			for match in receptivities:
				if match.company_id == distance_array[distance].id:
					flag = 1
			if flag == 0:
				distance_array.pop(distance)
	except:
		pass

	index = 1;
	result = {}
	for distance in sorted(distance_array):
		result[index] = distance_array[distance]
		if len(result[index].website) < 5:
			result[index].website = "www.vemdolixo.com"
		index = index + 1

	add_history = search_history(text = request.POST['residue_type'], latitude = lat_user, longitude = lon_user)
	add_history.save()

	name1 = convert_characters(result[1].organization_name)
	name2 = convert_characters(result[2].organization_name)
	name3 = convert_characters(result[3].organization_name)

	email1 = result[1].email
	email2 = result[2].email
	email3 = result[3].email

	tel1 = result[1].phone
	tel2 = result[2].phone
	tel3 = result[3].phone

	address1 = convert_characters(result[1].address)
	address2 = convert_characters(result[2].address)
	address3 = convert_characters(result[3].address)

	site1_url = verify_http_url(result[1].website)
	site2_url = verify_http_url(result[2].website)
	site3_url = verify_http_url(result[3].website)

	site1 = result[1].website
	site2 = result[2].website
	site3 = result[3].website

	lat_original = lat_user
	lat1 = result[1].latitude
	lat2 = result[2].latitude
	lat3 = result[3].latitude

	lon_original = lon_user
	lon1 = result[1].longitude
	lon2 = result[2].longitude
	lon3 = result[3].longitude

	context = {
		'name1': name1,
		'name2': name2,
		'name3': name3,
		'email1': email1,
		'email2': email2,
		'email3': email3,
		'tel1': tel1,
		'tel2': tel2,
		'tel3': tel3,
		'address1': address1,
		'address2': address2,
		'address3': address3,
		'site1': site1,
		'site2': site2,
		'site3': site3,
		'site1_url': site1_url,
		'site2_url': site2_url,
		'site3_url': site3_url,
		'lat_original': lat_original,
		'lat1': lat1,
		'lat2': lat2,
		'lat3': lat3,
		'lon_original': lon_original,
		'lon1': lon1,
		'lon2': lon2,
		'lon3': lon3,
	}
	return render(request, 'result-page.html', context)

def great_amounts(request):
	# fullname = request.POST['fullname']

	context = {}
	return render(request, 'great-amounts.html', context)

def great_amounts_send_email(request):
	fullname = request.POST['full_name']
	email = request.POST['contact_email']
	residue_type = request.POST['residue_type']
	other = request.POST.get('other', ' - ')
	amount = request.POST['amount']
	amount = request.POST.get('amount', '0')
	amount_type = request.POST.get('amount_type', ' - ')

	reload(sys)
	sys.setdefaultencoding('UTF8')
	request_text = 'Nome completo - ' + fullname + '\n'
	request_text = request_text + 'email - ' + email + '\n'
	request_text = request_text + 'Tipo de resíduo - ' + residue_type + '\n'
	request_text = request_text + 'Outro (campo opcional) - ' + other + '\n'
	request_text = request_text + 'Quantidade - ' + amount + ' ' + amount_type + '\n'

	mandrill_generic_request("fabricio@vemdolixo.com", request_text)
	mandrill_generic_request("fabricio@vemdolixo.com.br", request_text)
	mandrill_generic_request("augusto@vemdolixo.com", request_text)
	mandrill_generic_request("augusto@vemdolixo.com.br", request_text)
	mandrill_generic_request("renato@vemdolixo.com", request_text)
	mandrill_generic_request("renato@vemdolixo.com.br", request_text)
	mandrill_generic_request("atendimento@vemdolixo.com.br", request_text)

	try:
		first_name = fullname.split(' ', 1)[0]
		first_name_lower = first_name.lower()
		last_name = fullname.rsplit(' ', 1)[1]
		last_name_lower = last_name.lower()
		contact_email_lower = email.lower()
		new_reg = generic_register(first_name = first_name_lower, last_name = last_name_lower, email = contact_email_lower)
		new_reg.save()
	except:
		try:
			fullname_lower = fullname.lower()
			contact_email_lower = email.lower()
			new_reg = generic_register(first_name = fullname_lower, last_name = '', email = contact_email_lower)
			new_reg.save()
		except:
			pass

	context = {}
	return render(request, 'thanks-for-register.html', context)

def deactivate_all(request):
	companies = company.objects.all()
	for company_item in companies:
		print company_item.created_at
		company_item.is_active = 0
		company_item.save()
	return HttpResponse(200)



