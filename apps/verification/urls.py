from django.urls import path, re_path
from .views import image_code_view
from .views import check_username_view, check_mobile_view, SmsCodeView


app_name = 'verification'


urlpatterns = [
    path('image_code/', image_code_view, name='image_code'),
    re_path('check=(?P<username>\w{5,20})/', check_username_view, name='check_username'),
    re_path('mobile=(?P<mobile>1[3456789]\d{9})/', check_mobile_view, name='check_mobile'),
    path('sms_code/', SmsCodeView.as_view(), name='sms_code_view')
]
