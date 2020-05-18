from django.urls import path, re_path
from .views import login, Register

app_name = 'user'


urlpatterns = [
    path('login/', login, name='login'),
    path('register/', Register.as_view(), name='register'),

]
