from django.urls import path, re_path
from .views import Login, Register, LogoutView

app_name = 'user'


urlpatterns = [
    path('login/', Login.as_view(), name='login'),
    path('register/', Register.as_view(), name='register'),
    path('logout/', LogoutView.as_view(), name='logout'),

]
