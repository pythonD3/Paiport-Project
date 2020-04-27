from django.contrib import admin
from .models import*
# Register your models here.

class Country_Master_class(admin.ModelAdmin):
	list_display = ('id','country_name')
admin.site.register(Country_Master , Country_Master_class)

class Airport_Details_class(admin.ModelAdmin):
	list_display = ('id','fk_country','city_name','airport_name')
admin.site.register(Airport_Details , Airport_Details_class)


class Admin_class(admin.ModelAdmin):
	list_display = ('id','username')
admin.site.register(Admin , Admin_class)

class Country_Code_Master_class(admin.ModelAdmin):
	list_display = ('id','country_name','dial_code')
admin.site.register(Country_Code_Master , Country_Code_Master_class)

class User_Details_class(admin.ModelAdmin):
	list_display = ('id','name','phone_no',)
admin.site.register(User_Details , User_Details_class)

class ChatMaster_class(admin.ModelAdmin):
	list_display = ('id','fk_trip','user1_id','user2_id')
admin.site.register(ChatMaster ,ChatMaster_class)

class ChatChild_class(admin.ModelAdmin):
	list_display = ('id','fk_chat_master','date','time')
admin.site.register(ChatChild , ChatChild_class)
