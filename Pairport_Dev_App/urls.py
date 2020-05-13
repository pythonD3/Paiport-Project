from django.conf.urls import url, include
from .views import *
from .views_web import *

urlpatterns = [
	url(r'^admin_panel/$',admin_panel, name='admin_panel'),
	url(r'^admin_login/$',admin_login, name='admin_login'),
	url(r'^dashboard_page/$',dashboard_page, name='dashboard_page'),
	url(r'^user_page/$',user_page, name='user_page'),
	url(r'^airport_page/$',airport_page, name='airport_page'),
	url(r'^save_airport_details/$',save_airport_details, name='save_airport_details'),
	url(r'^delete_airport/$',delete_airport, name='delete_airport'),
	url(r'^logout/$',logout, name='logout'),
	
	
	
	#############################################URL API
	url(r'^store_airport_details/$',store_airport_details, name='store_airport_details'),
	url(r'^store_dial_code/$',store_dial_code, name='store_dial_code'),
	
	##################################################WEB API
	url(r'^user_signup_web/$',user_signup_web, name='user_signup_web'),
	url(r'^login_api_web/$',login_api_web, name='login_api_web'),
	url(r'^update_profile_web/$',update_profile_web, name='update_profile_web'),
	url(r'^country_code_list_web/$',country_code_list_web, name='country_code_list_web'),
	url(r'^user_request_otp_signup_web/$',user_request_otp_signup_web, name='user_request_otp_signup_web'),
	url(r'^send_otp/$',send_otp, name='send_otp'),
	url(r'^get_profile_web/$',get_profile_web, name='get_profile_web'),
	url(r'^airport_list_web/$',airport_list_web, name='airport_list_web'),
	url(r'^add_trip_web/$',add_trip_web, name='add_trip_web'),
	url(r'^trip_list_by_user_id_web/$',trip_list_by_user_id_web, name='trip_list_by_user_id_web'),
	url(r'^search_traveller_web/$',search_traveller_web, name='search_traveller_web'),
	url(r'^save_chatting_message_web/$',save_chatting_message_web, name='save_chatting_message_web'),
	url(r'^get_chatting_message_web/$',get_chatting_message_web, name='get_chatting_message_web'),
	url(r'^save_flag_web_api/$',save_flag_web_api, name='save_flag_web_api'),
	url(r'^flag_list_web/$',flag_list_web, name='flag_list_web'),
	
	url(r'^forget_password_web/$',forget_password_web, name='forget_password_web'),
]