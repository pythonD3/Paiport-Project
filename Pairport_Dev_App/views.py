from django.shortcuts import render
from .models import *
from django.shortcuts import redirect
from django.http import HttpResponseRedirect, Http404, JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import csv
from datetime import datetime, timedelta
# Create your views here.
import ast
import json


@csrf_exempt
def admin_panel(request):
	return render(request,'Website/login.html')
	
	
@csrf_exempt
def admin_login(request):
	Email = request.POST.get('email')
	Email = Email.lower()
	Password = request.POST.get('password')
	print(Email)
	print(Password)
	obj =  Admin.objects.filter(username = Email, password = Password)
	if obj:
		print("check")
		id = Admin.objects.get(username = Email, password = Password).id
		request.session['admin_id'] = str(id)
		return HttpResponse('success')
	else:
		return HttpResponse('error')
		
		

	
	
@csrf_exempt
def logout(request):
	try:
		del request.session['admin_id']
		return redirect('/admin_panel/')
	except:
		return redirect('/admin_panel/')
					
								
@csrf_exempt
def dashboard_page(request):
	admin = request.session.get('admin_id')
	if admin:
		admin_obj = Admin.objects.get(id=admin)
		admin_name = admin_obj.username
		return render(request, 'AdminPanel/administration.html',{'admin_name':admin_name})
	else:
		return redirect('/admin_panel/')
	
@csrf_exempt
def user_page(request):
	admin = request.session.get("admin_id")
	if admin:
		admin_obj = Admin.objects.get(id=admin)
		admin_name = admin_obj.username
		user_obj  =  User_Details.objects.all()
		return render(request,'AdminPanel/users_page.html',{'user_obj':user_obj,'admin_name':admin_name})
		# return render(request,'AdminPanel/UserListPage.html',{'user_obj':user_obj,'admin_name':admin_name})
	else:
		return redirect('/admin_panel/')
	
	
	
@csrf_exempt
def airport_page(request):
	admin = request.session.get("admin_id")
	if admin:
		admin_obj = Admin.objects.get(id=admin)
		admin_name = admin_obj.username
		air_obj  =  Airport_Details.objects.all()
		return render(request,'AdminPanel/aeroplane_list.html',{'air_obj':air_obj,'admin_name':admin_name})
	else:
		return redirect('/admin_panel/')
	
	
@csrf_exempt
def save_airport_details(request):
	admin = request.session.get("admin_id")
	if admin:
		country = request.POST.get('country')
		city = request.POST.get('city')
		airport = request.POST.get('airport')
		print("country_id",country)
		print("airport",airport)
		# if Airport_Details.objects.filter(fk_country = Country_Master.objects.get(country_name = country_id),city_name=city,airport_name=airport).exists():
			# return HttpResponse('error')
		# else:
		
		if  Country_Master.objects.filter(country_name = country).exists():
			if Airport_Details.objects.filter(fk_country = Country_Master.objects.get(country_name = country),city_name=city,airport_name=airport).exists():
				return HttpResponse("Exists")
			else:
				obj = Airport_Details(fk_country = Country_Master.objects.get(country_name = country),city_name=city,airport_name=airport)
				obj.save()
				return HttpResponse('success')
		else:
			object_c=Country_Master(country_name = country)
			object_c.save()
			Air_obj = Airport_Details(fk_country = Country_Master.objects.get(country_name = country),city_name=city,airport_name=airport)
			Air_obj.save()
			return HttpResponse('success')
	else:
		return redirect('/admin_panel/')
		
@csrf_exempt
def delete_airport(request):
	admin = request.session.get("admin_id")
	if admin:
		id = request.POST.get('id')
		print("id", id)
		obj = Airport_Details.objects.get(id=id)
		obj.delete()
		return HttpResponse("success")
	else:
		return redirect('/admin_panel/')
