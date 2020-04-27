from django.db import models

# Create your models here.


class Admin(models.Model):
	username = models.CharField(max_length = 100,null=True, blank=True)
	password = models.CharField(max_length = 50,null=True, blank=True)

	class Meta:
		verbose_name="Admin"
		verbose_name_plural = "Admin"
		

		
		
class Country_Code_Master(models.Model):
	country_name = models.CharField(max_length = 50,null=True, blank=True)
	capital_name = models.CharField(max_length = 50,null=True, blank=True)
	short_name = models.CharField(max_length = 50,null=True, blank=True)
	dial_code = models.CharField(max_length = 10,null=True, blank=True)
	
	# def __str__(self):
		# return self.country_name
		
		
class Country_Master(models.Model):
	country_name = models.CharField(max_length=200,null=True,blank=True)
	
	def __str__(self):
		return self.country_name
		
	class Meta:
		verbose_name="Country_Master"
		verbose_name_plural = "Country_Master"
		
	
class City_Master(models.Model):
	fk_country = models.ForeignKey(Country_Master,on_delete=models.CASCADE,null=True,blank=True)
	city_name = models.CharField(max_length=200,null=True,blank=True)
	
	def __str__(self):
		return self.city_name
		
	class Meta:
		verbose_name="City_Master"
		verbose_name_plural = "City_Master"
		
class Airport_Details(models.Model):
	fk_country = models.ForeignKey(Country_Master,on_delete=models.CASCADE,null=True,blank=True)
	city_name = models.CharField(max_length=191,null=True,blank=True)
	airport_name  = models.CharField(max_length=200,null=True,blank=True)
	
	def __str__(self):
		return self.airport_name
		
	class Meta:
		verbose_name="Airport_Details"
		verbose_name_plural = "Airport_Details"

class User_Details(models.Model):
	fk_dialcode = models.ForeignKey(Country_Code_Master ,on_delete = models.CASCADE , null=True , blank = True)
	name =  models.CharField(max_length=200,null=True,blank=True)
	username =  models.CharField(max_length=200,null=True,blank=True)
	password =  models.CharField(max_length=200,null=True,blank=True)
	emal_id =  models.CharField(max_length=200,null=True,blank=True)
	phone_no =  models.CharField(max_length=100,null=True,blank=True)
	token =  models.CharField(max_length=200,null=True,blank=True)
	profile_image = models.ImageField(null = True, blank = True, upload_to = "Profile_Image/")
	fk_country = models.ForeignKey(Country_Code_Master , related_name='country_name_p',on_delete = models.CASCADE , null=True , blank = True)
	image_one = models.ImageField(null = True, blank = True, upload_to = "Profile_Image/")
	image_two = models.ImageField(null = True, blank = True, upload_to = "Profile_Image/")
	image_three = models.ImageField(null = True, blank = True, upload_to = "Profile_Image/")
	image_four = models.ImageField(null = True, blank = True, upload_to = "Profile_Image/")
	image_five = models.ImageField(null = True, blank = True, upload_to = "Profile_Image/")
	moto =  models.CharField(max_length=200,null=True,blank=True)
	job =  models.CharField(max_length=200,null=True,blank=True)
	travel_country =  models.CharField(max_length=200,null=True,blank=True)
	insta_link = models.CharField(max_length=200,null=True,blank=True)
	selected_country_list = models.TextField(null=True , blank = True)
	
	def __str__(self):
		return self.name
		
	class Meta:
		verbose_name="User_Details"
		verbose_name_plural = "User_Details"

		
		
		
class Trip_Details(models.Model):
	fk_user = models.ForeignKey(User_Details , on_delete = models.CASCADE , null=True , blank = True)
	fk_airport =  models.ForeignKey(Airport_Details , on_delete = models.CASCADE , null=True , blank = True)
	date_layover = models.DateField(null=True, blank=True)
	arival_time = models.TimeField(null=True,blank=True)
	layover_time = models.CharField(max_length=100,null=True,blank=True)
	
	class Meta:
		verbose_name="Trip_Details"
		verbose_name_plural = "Trip_Details"
		
		
class ChatMaster(models.Model):
	fk_trip =  models.ForeignKey(Trip_Details,on_delete=models.CASCADE,null=True,blank=True)
	user1_id = models.CharField(max_length = 10,null=True,blank=True)
	user2_id = models.CharField(max_length = 10,null=True,blank=True)
	
	class Meta:
		verbose_name="ChatMaster"
		verbose_name_plural = "ChatMaster"

class ChatChild(models.Model):
	fk_chat_master = models.ForeignKey(ChatMaster,null = True, db_column='fk_chat_master',on_delete=models.CASCADE)
	message = models.TextField(null = True , blank = True)
	date = models.DateField(null = True , blank = True)
	time = models.TimeField(null = True , blank = True)
	user_id = models.CharField(max_length = 10,null=True,blank=True)

	class Meta:
		verbose_name="ChatChild"
		verbose_name_plural = "ChatChild"