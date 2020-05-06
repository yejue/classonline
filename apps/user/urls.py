from django.urls import path, re_path
from .views import login, Register, check_username_view, check_mobile_view


app_name = 'user'


urlpatterns = [
    path('login/', login, name='login'),
    path('register/', Register.as_view(), name='register'),
    re_path('check=(?P<username>\w{5,20})/', check_username_view, name='check_username'),
    re_path('mobile=(?P<mobile>1[3456789]\d{9})/', check_mobile_view, name='check_mobile'),
]
