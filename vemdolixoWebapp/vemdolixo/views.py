from django.shortcuts import render
from django.conf import settings
from vemdolixo.models import generic_register, company, residue, receptivity, member, search_history
from django.http import HttpResponse
import json
import googlemaps
from datetime import datetime
import re
import decimal

# Create your procedures here.

def calculate_distance(lat1, lon1, lat2, lon2):
	lat1 = float(lat1)
	lat2 = float(lat2)
	lon1 = float(lon1)
	lon2 = float(lon2)
	distance_lat = (lat1 - lat2) ** 2
	distance_lon = (lon1 - lon2) ** 2
	distance = (distance_lat + distance_lon) ** (0.5)
	return distance

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
	cep = re.sub('[^0-9]','', user_cep)
	gmaps = googlemaps.Client(key=settings.GOOGLE_API_KEY)
	geocode_result = gmaps.geocode(cep)
	lat_user = geocode_result[0]['geometry']['location']['lat']
	lon_user = geocode_result[0]['geometry']['location']['lng']

	companies = company.objects.all()
	distance_array = {}
	for company_item in companies:
		distance = calculate_distance(lat_user, lon_user, company_item.latitude, company_item.longitude)
		distance_array[distance] = company_item

	try:
		residues = residue.objects.get(residue_name = request.POST['residue_type'])
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
		index = index + 1

	name1 = result[1].organization_name
	name2 = result[2].organization_name
	name3 = result[3].organization_name

	email1 = result[1].email
	email2 = result[2].email
	email3 = result[3].email

	tel1 = result[1].phone
	tel2 = result[2].phone
	tel3 = result[3].phone

	address1 = result[1].address
	address2 = result[2].address
	address3 = result[3].address

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
