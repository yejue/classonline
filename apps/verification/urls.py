from django.urls import path
from .views import image_code_view


app_name = 'verification'


urlpatterns = [
    path('image_code/', image_code_view, name='image_code')
]
