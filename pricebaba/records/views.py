from django.shortcuts import render
from django.http import *
import datetime
from django.shortcuts import render,redirect
from django.template import RequestContext
from records.models import *
from django.views.decorators.csrf import csrf_exempt
import urllib2
import urllib
import json
ACCESS_TOKEN = 'AIzaSyAwY_UfZQijFtDk6dhtMkCIczaN0PLql3M'
# Create your views here.
def home(request):
	
	users = User.objects.all()
	context = {}
	context['users'] = users
	print users
	if 'message' in request.GET:
		context['message'] = request.GET['message']
	elif 'message_error' in request.GET:
		context['message_error'] = request.GET['message_error']


	return render(request,'home.html',context)

@csrf_exempt
def add_user(request):
	context = {}
	if request.method == 'GET':
		if 'message' in request.GET:
			context['message'] = request.GET['message']
		elif 'message_error' in request.GET:
			context['message_error'] = request.GET['message_error']
		try:

			user_id = request.GET['id']
			user = User.objects.get(id = user_id)
			context['user'] = user
			return render(request,'add_user.html',context)
		except:
			return render(request,'add_user.html',context)
	elif request.method == 'POST':
		try:
			first_name = request.POST['first_name']
			last_name = request.POST['last_name']
			email = request.POST['email']
			age = request.POST['age']
			mobile = request.POST['mobile']
			date_of_birth = request.POST['date_of_birth']
			location = get_location(str(request.POST['location']))
			print "POST:"
			print request.POST
			if 'user_id' in request.POST:
				user_id = request.POST['user_id']
				user_object = User.objects.get(id = user_id)
				#user_object = User(id =user_id, first_name = first_name,last_name = last_name,email = email,age = age,mobile = mobile,date_of_birth = date_of_birth,location = location)
				user_object.first_name = first_name
				user_object.last_name = last_name
				user_object.email = email
				user_object.age = age
				user_object.mobile = mobile
				user_object.date_of_birth = date_of_birth
				user_object.location = location
				user_object.save()
			else:

				user_object = User(first_name = first_name,last_name = last_name,email = email,age = age,mobile = mobile,date_of_birth = date_of_birth,location = location)
				user_object.save()
			return redirect('/?message=User added')
		except:
			return redirect('/add_user/?message_error=User not added')


def build_URL(search_text='',types_text=''):
    base_url = 'https://maps.googleapis.com/maps/api/place/textsearch/json'     # Can change json to xml to change output type
    key_string = '?key='+ACCESS_TOKEN                                           # First think after the base_url starts with ? instead of &
    query_string = '&query='+urllib.quote(search_text)
    sensor_string = '&sensor=false'                                             # Presumably you are not getting location from device GPS
    type_string = ''
    if types_text!='':
        type_string = '&types='+urllib.quote(types_text)                        # More on types: https://developers.google.com/places/documentation/supported_types
    url = base_url+key_string+query_string+sensor_string+type_string
    return url


def get_location(search_txt=None):
	resp = urllib2.urlopen(build_URL(search_text=search_txt))

	r=json.load(resp)
	for i in r['results']:
		result = i['formatted_address']
	return result