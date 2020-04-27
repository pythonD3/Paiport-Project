from django.shortcuts import render
from .models import *
from django.shortcuts import redirect
from django.http import HttpResponseRedirect, Http404, JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import json, string
import traceback
from django.core.mail import EmailMessage
import requests
from Pairport_Dev.settings import EMAIL_HOST_USER
from datetime import date, datetime
import ast
import base64
import random
import math
from django.core.mail import send_mail
import sched, time
import threading
import os
from twilio.rest import Client
# from .Checksum import generate_checksum, verify_checksum,__id_generator__
# import Checksum 
import requests
from bs4 import BeautifulSoup

def store_airport_details(request):
	try:
		print("url")
		URL  = "https://airports-list.com/largest-countries-by-airports/"
		# URL  = "https://airports-list.com/"
		page = requests.get(URL)
		soup = BeautifulSoup(page.content, 'html.parser')
		tables = soup.findAll('span', attrs = {'class':'views-field views-field-name'}) 
		country_name=""
		data = []
		for i in tables:
				for country in i.findAll('span', attrs = {'class':['field-content']}): 
					for an in country.findAll('a'):
							country_name = str(an.text)
							string=country_name.replace(" ", "-")
							string=string.replace(" ", "-")
							print("country_name----------------------->",string)
							sec=string.lower()
							
							# if sec == "-of":
								# string=sec.replace("-of", "" )
								# print("sec------>",string)
							# else:
								# string=sec.replace("d&#039;", "")
								# string=sec.replace("-the", "")
								# string1=sec.replace("(","")
								# string=sec.replace(")","")

							obj = Country_Master.objects.create(country_name=country_name)
							obj.save()
							print("country_name  new_string----------------------->",sec)
						
							# break
							if sec:
								stringone=sec.replace("-of", "" )
								stringone=stringone.replace("&#039;", "")
								print("mmmm",stringone)
								stringone=stringone.replace("(","")
								stringone=stringone.replace(")","")
								stringone=stringone.replace("-the", "")
								stringone=stringone.replace(".", "")
								print("22",stringone)
								if stringone:
									print("stringone",stringone)
									URL = "https://airports-list.com/country/"+stringone
									r = requests.get(URL)
									soup = BeautifulSoup(r.content, 'html.parser')
									### tb = soup.find('table', class_='views-table cols-5 display')
									tb = soup.find('table',attrs={'id':'datatable-1'})
									table_body = tb.find('tbody')

									rows = table_body.find_all('tr')
								
									for row in rows:
										cols = row.find_all('td')
										cols = [ele.text.strip() for ele in cols]
										counter = cols[0]
										city_name = cols[1]
										airport_name = cols[2]
										
										print("Sr No --->",counter)
										print("city_name--->",city_name)
										print("airport_name----->",airport_name)
										
										air_ob=Airport_Details(fk_country=Country_Master.objects.get(country_name=country_name),city_name=city_name,airport_name=airport_name) 
										air_ob.save()
					break
					
	except:
		print(str(traceback.format_exc()))
		send_data = {'status':"0", 'msg':"Something Went Wrong", 'error':str(traceback.format_exc())}
		
	return JsonResponse(send_data)




######################################## Store Dial Code 

@csrf_exempt
def store_dial_code(request):
	try:
		URL  = "https://www.science.co.il/international/Country-codes.php"
		r = requests.get(URL)
		soup = BeautifulSoup(r.content, 'html.parser')
		tb = soup.find('table',attrs={'class':'sortable'})
		table_body = tb.findAll('tr')
		data=[]
		for row in table_body:
			col = row.find_all('td')
			cols = [ele.text.strip() for ele in col]
			if cols:
				country_name = str(cols[0])
				capital_name =str(cols[1])
				internet_name = str(cols[2])
				dail_name = str(cols[3])
				code_no=dail_name.replace("-", "")
				dialcode = "+"+code_no
				print("country --->",country_name)
				print("capital_name--->",capital_name)
				print("internet_name----->",internet_name)
				print("dail_name",dialcode)
				obj  =  Country_Code_Master(country_name=country_name,capital_name=capital_name,short_name=internet_name,dial_code=dialcode)
				obj.save()
				send_data={'msg':"Save Successfully"}
	except:
		print(str(traceback.format_exc()))
		send_data = {'status':"0", 'msg':"Something Went Wrong", 'error':str(traceback.format_exc())}
		
	return JsonResponse(send_data)




#################Upload Image Function
@csrf_exempt
def upload_image(img, img_path, img_name):
	current = str(datetime.now().strftime('%Y-%m-%d'))
	path = settings.BASE_DIR + "/media/"
	random_number = '{:04}'.format(random.randrange(1, 10**4))
	imgN= img_path+img_name+random_number+"_"+current+'.jpg'
	destination = open(path+imgN, 'wb')
	destination.write(base64.b64decode(img))
	destination.close()
	return imgN

	
###############Signup API
	
@csrf_exempt
def user_signup_web(request):
	try:
		data = json.loads(request.body.decode('utf-8'))
		dialcode_id = data['dialcode_id']
		phone_no = data['phone_no']
		name = data['name']
		emal_id = data['email_id']
		emal_id = emal_id.lower()
		profile_image = data['profile_image']
		if User_Details.objects.filter(fk_dialcode__id= dialcode_id,phone_no=phone_no).exists():
			send_data ={'msg':"Mobile Number Already Exists",'status':"0"}
		else:
			user_obj = User_Details(name=name,emal_id = emal_id,fk_dialcode_id = dialcode_id,phone_no=phone_no)
			user_obj.save()
			if profile_image:
				profile_name = upload_image(profile_image,"Profile_Image/","Profile_")
				user_obj.user_profile = profile_name
				user_obj.save()
			else:
				pass
			
			send_data = {'msg':"Sign up successful",'status':"1","user_id": str(user_obj.id)}
	except:
		send_data = {'msg':"Something went wrong", 'error':str(traceback.format_exc())}
		print(send_data)
	return JsonResponse(send_data)
	
##########################login API
@csrf_exempt
def login_api_web(request):
	try:
		data = json.loads(request.body.decode('utf-8'))
		dialcode_id = data['dialcode_id']
		phone_no = data['phone_no']
		
		if User_Details.objects.filter(fk_dialcode__id = dialcode_id,phone_no=phone_no).exists():
			user_obj = User_Details.objects.get(fk_dialcode__id = dialcode_id,phone_no=phone_no) 
			
			send_data = {'msg':"Login Sucessfully",'status':"1","user_id": str(user_obj.id)}
		else:	
			send_data = {'msg':"Invalid Credentials", 'status':"0"}
			
	except:
		send_data = {'msg':"Something went wrong", 'error':str(traceback.format_exc())}
		print(send_data)
	return JsonResponse(send_data)
		
		############################ Get Profile Api
		
@csrf_exempt
def get_profile_web(request):
	try:
		data = json.loads(request.body.decode('utf-8'))
		user_id = data['user_id']
		obj = User_Details.objects.get(id = user_id)
		dict = {}
		
		dict['user_id'] = str(obj.id)
		if obj.name:
			dict['name'] = str(obj.name)
		else:
			dict['name'] = ""
		if obj.fk_dialcode:
			dict['dial_code'] = str(obj.fk_dialcode.dial_code)
		else:
			dict['dial_code'] = ""
		
		if obj.phone_no:
			dict['phone_no'] = str(obj.phone_no)
		else:
			dict['phone_no'] = ""
		if obj.profile_image:
			dict['profile_image'] = str(obj.profile_image)
		else:
			dict['profile_image'] = ""
			
		if obj.image_one:
			dict['image_one'] = str(obj.image_one)
		else:
			dict['image_one'] = ""		
		if obj.image_two:
			dict['image_two'] = str(obj.image_two)
		else:
			dict['image_two'] = ""		
		if obj.image_three:
			dict['image_three'] = str(obj.image_three)
		else:
			dict['image_three'] = ""		
		if obj.image_four:
			dict['image_four'] = str(obj.image_four)
		else:
			dict['image_four'] = ""		
		if obj.image_five:
			dict['image_five'] = str(obj.image_five)
		else:
			dict['image_five'] = ""
		if obj.moto:
			dict['moto'] =str(obj.moto)
		else:
			dict['moto'] = ""
		if obj.job:
			dict['job'] = str(obj.job)
		else:
			dict['job'] = ""
			
		# if obj.travel_country:
			# dict['travel_country'] = str(obj.travel_country)
		# else:
			# dict['travel_country'] =  ""
			
		if obj.insta_link:
			dict['insta_link'] = str(obj.insta_link)
		else:
			dict['insta_link'] =  ""
			
		if obj.fk_country:
			dict['residence_country'] = str(obj.fk_country.country_name)
		else:
			dict['residence_country'] = ""
			
		if obj.selected_country_list:
			ls=[]
			li=[]
			list=[]
			new_list = json.loads(json.dumps(obj.selected_country_list))
			new_list = ast.literal_eval(new_list)
			for j in new_list:
				print("jjj",j)
				object=Country_Code_Master.objects.filter(id=j)
				for m in object:
					if m.country_name in list:
						pass
					else:
						print('name...1')
					list.append(m.country_name)
					
					print("service Name", )
				dict['selected_service_list'] =list	
	
		else:
			dict['selected_countries_list'] = ""
		send_data = {'status':"1", 'msg':" User Profile", 'profile':dict}
	except:
		send_data = {'msg':"Something went wrong", 'error':str(traceback.format_exc())}
		print(send_data)
	return JsonResponse(send_data)

	####################################update profile Web
@csrf_exempt
def update_profile_web(request):
	try:
		data = json.loads(request.body.decode('utf-8'))
		user_id = data['user_id']
		name = data['name']
		moto = data['moto']
		job = data['job']
		residence_country_id = data['residence_country_id']
		profile_image = data['profile_image']
		image_one = data['image_one']
		image_two = data['image_two']
		image_three = data['image_three']
		image_four = data['image_four']
		image_five = data['image_five']
		insta_link = data['insta_link']
		selected_countries_list = data['selected_countries_list']
		print("selected_countries_list...............",selected_countries_list)
		# for i in selected_countries_list:
			# print("i.................",i)
		if  User_Details.objects.filter(id=user_id).exists():
			user_obj = User_Details.objects.get(id=user_id)
			user_obj.moto=moto
			user_obj.name=name
			user_obj.job=job
			# user_obj.travel_country=travel_country
			user_obj.insta_link=insta_link
			user_obj.selected_country_list=selected_countries_list
			user_obj.fk_country= Country_Code_Master.objects.get(id =residence_country_id)
			
			
			
			if profile_image:
				profile_name = upload_image(profile_image,"Profile_Image/","Profile_")
				user_obj.profile_image = profile_name
				
			else:
				pass
				
			if image_one:
				image_one_name = upload_image(image_one,"Profile_Image/","Profile_Image_")
				user_obj.image_one = image_one_name
			else:
				pass
				
			if image_two:
				image_two_name = upload_image(image_two,"Profile_Image/","Profile_Image_")
				user_obj.image_two = image_two_name
			else:
				pass
				
			if image_three:
				image_three_name = upload_image(image_three,"Profile_Image/","Profile_Image_")
				user_obj.image_three = image_three_name
			else:
				pass
				
			if image_four:
				image_four_name = upload_image(image_four,"Profile_Image/","Profile_Image_")
				user_obj.image_four = image_four_name
			else:
				pass
						
			if image_five:
				image_five_name = upload_image(image_five,"Profile_Image/","Profile_Image_")
				user_obj.image_five = image_five_name
			else:
				pass
				
			user_obj.save()
			send_data = {'status':"1", 'msg':"Profile updated successfully!"}
		else:
			send_data = {'status':"0", 'msg':"User Not Found"}
	except:
		send_data = {'msg':"Something went wrong", 'error':str(traceback.format_exc())}
		print(send_data)
	return JsonResponse(send_data)
		
	


##################### Twilio OTP Function #####################
@csrf_exempt
def send_otp(send_to,body):
	try:
		account_sid = 'AC87f23320f2d83e8d660986c361dc6d91' 
		auth_token = '2e8213e65c52c4ef65b33e8b388dfb01'
		client = Client(account_sid, auth_token)
		message = client.messages.create(from_= '+19893734917', body = body, to = send_to) 
		print(message.sid)
		return message.sid
	except Exception as e:
		print(str(e))
		return str(e)

		
	#####################verify Number

@csrf_exempt
def user_request_otp_signup_web(request):
	try:
		data = json.loads(request.body.decode('utf-8'))
		dialcode_id = data['dialcode_id']
		phone_no = data['phone_no']
		print("dialcode_id..............",dialcode_id)
		print("contact_no..............",phone_no)
		if User_Details.objects.filter(fk_dialcode__id = dialcode_id, phone_no = phone_no).exists():
			send_data = {'status':"0", 'msg':"Contact No. Already Exists"}	
		else:
			send_to = str(Country_Code_Master.objects.get(id = dialcode_id).dial_code)+str(phone_no)
			otp = '{:04}'.format(random.randrange(1, 10**4))
			print(otp)
			otp_message = otp + " is your verification code for Pairport App."
			print(otp_message)
			res = send_otp(send_to,otp_message)
			print(res)
			send_data = {'status':"1", 'msg':"OTP Sent Successfully", 'otp':str(otp)}
		
	except Exception as e:
		print(str(traceback.format_exc()))
		send_data = {'status':"0", 'msg':"Something went wrong, please try after sometime.", 'error':str(traceback.format_exc())}
		
	return JsonResponse(send_data)

	#################################################### Dial Code List
@csrf_exempt
def country_code_list_web(request):
	try:
		obj = Country_Code_Master.objects.all()
		list =[]
		dict = {}
		for i in obj:
			dict['id'] = str(i.id)
			dict['country_name'] = str(i.country_name)
			dict['short_name'] = str(i.short_name)
			dict['dial_code'] = str(i.dial_code)
			list.append(dict)
			dict={}
		send_data = {'msg':"Country dial code list", 'status':"1","dial_code":list}
	except:
		send_data = {'msg':"Something went wrong", 'error':str(traceback.format_exc())}
		print(send_data)
	return JsonResponse(send_data)
		
	
#############################	# Airport List
def airport_list_web(request):
	try:
		obj = Airport_Details.objects.all()
		list =[]
		dict ={}
		for i in obj:
			dict['id'] = str(i.id)
			dict['country_name'] = str(i.fk_country.country_name)
			dict['city_name'] = str(i.city_name)
			dict['airport_name'] = str(i.airport_name)
			list.append(dict)
			dict ={}
		send_data = {'msg':"Airport list", 'status':"1","airport_list":list}
	except:
		send_data = {'msg':"Something went wrong", 'error':str(traceback.format_exc())}
		print(send_data)
	return JsonResponse(send_data)
		
		
		
########################################################## Add trip
@csrf_exempt
def add_trip_web(request):
	try:
		data = json.loads(request.body.decode('utf-8'))
		user_id = data['user_id']
		airport_id =data['airport_id']
		date_layover =data['date_layover']
		arrival_time =data['arrival_time']
		layover_time =data['layover_time']
		
		if User_Details.objects.filter(id= user_id).exists():
			tri_obj = Trip_Details(fk_user_id = user_id,fk_airport=Airport_Details.objects.get(id=airport_id),date_layover=date_layover,arival_time=arrival_time,layover_time=layover_time)
			tri_obj.save()
			send_data = {'status':"1",'msg':"Trip Added Successfully"}
		else:
			send_data = {'status':"0", 'msg':"User Not Found"}
	except:
		send_data = {'msg':"Something went wrong", 'error':str(traceback.format_exc())}
		print(send_data)
	return JsonResponse(send_data)
		
		
		
#####################################################Trip List

@csrf_exempt
def trip_list_by_user_id_web(request):
	try:
		data = json.loads(request.body.decode('utf-8'))
		print("gdfg")
		user_id = data['user_id']
		if User_Details.objects.filter(id= user_id).exists():
			if Trip_Details.objects.filter(fk_user_id=user_id).exists():
				obj = Trip_Details.objects.filter(fk_user_id=user_id).order_by('date_layover')
				list = []
				dict = {}
				for i in obj:
					dict['trip_id'] = str(i.id)
					if i.fk_airport:
						dict['airport_name'] = str(i.fk_airport.airport_name)
					else:
						dict['airport_name'] = ""
					if i.fk_airport:
						dict['city_name'] = str(i.fk_airport.city_name)
					else:
						dict['city_name'] = ""
					if i.fk_airport:
						dict['country_name'] = str(i.fk_airport.fk_country.country_name)
					else:
						dict['country_name'] = ""
					if i.date_layover:
						dict['date_layover'] = str(i.date_layover)
					else:
						dict['date_layover'] = ""
					if i.arival_time:
						dict['arival_time'] = str(i.arival_time)
					else:
						dict['arival_time'] = ""
					if i.layover_time:
						dict['layover_time'] = str(i.layover_time)
					else:
						dict['layover_time'] = ""
					list.append(dict)
					dict = {}
					
				send_data = {'msg':"Trip List",'status':"1",'trip_list':list}
			else:
				send_data = {'status':"0", 'msg':"Trip Not Found"}
		else:
			send_data = {'status':"0", 'msg':"User Not Found"}
	except:
		send_data = {'msg':"Something went wrong", 'error':str(traceback.format_exc())}
		print(send_data)
	return JsonResponse(send_data)
		
		
		###############################  Search Traveller
@csrf_exempt
def  search_traveller_web(request):
	try:
		data = json.loads(request.body.decode('utf-8'))
		user_id = data['user_id']
		trip_id = data['trip_id']
		
		if User_Details.objects.filter(id= user_id).exists():
			if Trip_Details.objects.filter(id=trip_id).exists():
				trip_obj = Trip_Details.objects.get(id= trip_id)
				trip_airport_id = trip_obj.fk_airport.id
				trip_date = trip_obj.date_layover
				trip_time = trip_obj.arival_time
				trip_layover_time = trip_obj.layover_time
				print("trip_airport_name",trip_airport_id)
				print("trip_date",trip_date)
				print("trip_time",trip_time)
				print("trip_layover_time",trip_layover_time)
				if Trip_Details.objects.filter(fk_airport__id =trip_airport_id,date_layover=trip_date,arival_time=trip_time).exists():
					all_trip_data = Trip_Details.objects.filter(fk_airport__id =trip_airport_id,date_layover=trip_date,arival_time=trip_time).exclude(fk_user_id=user_id).order_by('-date_layover')
					list = []
					dict = {}
					for i in all_trip_data:
						dict['trip_id'] = str(i.id)
						if i.fk_user:
							dict['user_name'] = str(i.fk_user.name)
						else:
							dict['user_name'] = ""
						if i.fk_user:
							dict['profile_image'] = str(i.fk_user.profile_image)
						else:
							dict['profile_image'] = ""
							
						if i.fk_airport:
							dict['airport_name'] = str(i.fk_airport.airport_name)
						else:
							dict['airport_name'] = ""
						if i.date_layover:
							dict['date_layover'] = str(i.date_layover)
						else:
							dict['date_layover'] = ""
						if i.arival_time:
							dict['arival_time'] = str(i.arival_time)
						else:
							dict['arival_time'] = ""
							
						list.append(dict)
						dict = {}
					send_data = {'status':"1", 'msg':"Trip  Found",'trip':list}
				else:
					send_data = {'status':"0", 'msg':"Trip on this  date not Found"}
			else:
				send_data = {'status':"0", 'msg':"Trip Not Found"}
		else:
			send_data = {'status':"0", 'msg':"User Not Found"}
	except:
		send_data = {'msg':"Something went wrong", 'error':str(traceback.format_exc())}
		print(send_data)
	return JsonResponse(send_data)
		
###############save Chat Meassge Api

@csrf_exempt
def save_chatting_message_web(request):
	try:
		data = json.loads(request.body.decode('utf-8'))
		trip_id = data['trip_id']
		user1_id = data['user1_id']
		user2_id = data['user2_id']
		message = data['message']
		message_from = data['message_from']
		date = data['date']
		time = data['time']
		
		data_message = {}
		user1_obj = User_Details.objects.get(id = user1_id)
		if user1_obj.name:
			name1 = user1_obj.name
		else:
			name1 = ""
		if user1_obj.profile_image:
			profile_image1 = str(user1_obj.profile_image)
		else:
			profile_image1 = ""
			
		user2_obj = User_Details.objects.get(id = user2_id)
		if user2_obj.name:
			name2 = user2_obj.name
		else:
			name2 = ""
		if user2_obj.profile_image:
			profile_image2 = str(user2_obj.profile_image)
		else:
			profile_image2 = ""
			
			
		if ChatMaster.objects.filter(fk_trip_id = trip_id,user1_id = user1_id , user2_id = user2_id).exists():
			chat_obj = ChatMaster.objects.get(fk_trip_id = trip_id,user1_id = user1_id , user2_id = user2_id)
			
			ChatChild.objects.create(fk_chat_master_id = chat_obj.id,message = message , date = date , time = time,user_id = message_from)
			
		elif ChatMaster.objects.filter(fk_trip_id = trip_id,user1_id = user2_id , user2_id = user1_id).exists():
			chat_obj =  ChatMaster.objects.get(fk_trip_id = trip_id,user1_id = user2_id , user2_id = user1_id)
			ChatChild.objects.create(fk_chat_master_id = chat_obj.id ,message=message,date=date,time=time,user_id=message_from)
			
		else:
			chat_obj = ChatMaster.objects.create(fk_trip_id = trip_id,user1_id = user1_id , user2_id = user2_id)
			ChatChild.objects.create(fk_chat_master_id = chat_obj.id,message = message , date = date , time = time,user_id = message_from)
		
		message_to = user1_id if message_from == user2_id else user2_id
		android_user_token = User_Details.objects.get(id = message_to).token
		name = User_Details.objects.get(id = message_from).name
		data_message = {}
		message_title = "Pairport App"
		message_body = name+" sent you message"
		data_message = {
		'title':"Pairport App",
		# 'body':name+" sent you message",
		'body':"New Message",
		'trip_id' : trip_id, 
		'user1_id' : user1_id,
		'user2_id' : user2_id,
		'user1_name' : name1,
		'user2_name' : name2,
		'user1_profile' : profile_image1,
		'user2_profile' : profile_image2,
		'notification_type':"chat"
		}
		
		print("data_message",data_message)
		
		# print("android_user_token",android_user_token)
		# if android_user_token:
			# res = send_chatting_notification(android_user_token ,"New Message", message, data_message)
			# print(res)
		# else:
			# pass
		
		send_data = {"status":"1","msg":"message sent successfully"}
		
	except:
		send_data = {'msg':"Something went wrong", 'error':str(traceback.format_exc())}
		print(send_data)
	return JsonResponse(send_data)
	
	
	############################# Get Chat list API 
@csrf_exempt
def get_chatting_message_web(request):
	try:
		data = json.loads(request.body.decode('utf-8'))
		trip_id = data['trip_id']
		user1_id = data['user1_id']
		user2_id = data['user2_id']
		
		if ChatMaster.objects.filter(fk_trip_id =trip_id,user1_id=user1_id, user2_id=user2_id).exists():
			chat_obj = ChatMaster.objects.get(fk_trip_id =trip_id , user1_id = user1_id , user2_id = user2_id)
			chat_child_obj = ChatChild.objects.filter(fk_chat_master_id = chat_obj.id).order_by('date', 'time')
			chat_list = []
			chat_dict = {}
			for i in chat_child_obj:
				chat_dict['message'] = i.message
				chat_dict['date'] = i.date
				chat_dict['time'] = i.time.strftime('%H:%M')
				
				user_name = User_Details.objects.get(id = i.user_id).name
				user2 =i.user_id
				print(" i.user_id", user2)

				if user2_id ==user2:
					chat_dict['user_name'] = ""
				else:
					chat_dict['user_name'] = user_name
				chat_dict['user_id'] = i.user_id
				chat_list.append(chat_dict)
				chat_dict = {}

			send_data = {"status":"1","msg":"chat found","chat_data":chat_list}
		elif  ChatMaster.objects.filter(fk_trip_id =trip_id, user1_id = user2_id , user2_id = user1_id).exists():
				chat_obj = ChatMaster.objects.get(fk_trip_id =trip_id, user1_id = user2_id , user2_id = user1_id)
				chat_child_obj = ChatChild.objects.filter(fk_chat_master_id = chat_obj.id).order_by('date', 'time')
				chat_list = []
				chat_dict = {}
				for i in chat_child_obj:
					chat_dict['message'] = i.message
					chat_dict['date'] = i.date

					chat_dict['time'] = i.time.strftime('%H:%M')
					
					# t = datetime.strptime(str(i.time), "%H:%M:%S")
					# time = t.strftime("%I:%M:%S %p")
					# chat_dict['time'] = time

					user_name = User_Details.objects.get(id = i.user_id).name
					user2 =i.user_id
					print(" i.user_id", user2)

					if user2_id ==user2:
						chat_dict['user_name'] = ""
					else:
						chat_dict['user_name'] = user_name
						
					chat_dict['user_id'] = i.user_id
					chat_list.append(chat_dict)
					chat_dict = {}
				send_data = {"status":"1","msg":"chat found","chat_data":chat_list}
		else:
			send_data = {"status":"0","msg":"no chat found"}
		
	except:
		send_data = {'msg':"Something went wrong", 'error':str(traceback.format_exc())}
		print(send_data)
	return JsonResponse(send_data)
		################################################## Forget Password API
@csrf_exempt
def forget_password_web(request):
	try:
		data = json.loads(request.body.decode('utf-8'))
		emal_id = data['email_id']
		emal_id = emal_id.lower()
		if User_Details.objects.filter(emal_id=emal_id).exists():
			user_obj = User_Details.objects.get(emal_id = emal_id)
			user_email = user_obj.emal_id
			rstr = "\n\nThanks,"+"\nPairport Team"
			subject = "Request For Password Recovery";
			message = "Hi "+user_obj.name+", \nYou have recently requested password for Pairport user account.\n\nYour current password is "+user_obj.password+"\n\nIf you did not request a password, please ignore this email or reply to let us know."+rstr
			print("message---------->",message)
			from_mail = settings.EMAIL_HOST_USER
			print("from_mail------->",from_mail)
			email_msg =EmailMessage(subject, message, to=[emal_id], from_email= from_mail )
			
			print("email_msg   ---------->",email_msg)
			
			email_msg.send()
			print("message..........*",email_msg)
			send_data = {'msg' : "Password has been sent to your registered email id" , 'status': "1"}
		
		else:
			send_data = {'msg':"Email Does not Exist", 'status':"0"}
	except:
		send_data = {'msg':"Something went wrong", 'error':str(traceback.format_exc())}
		print(send_data)
	return JsonResponse(send_data)
		