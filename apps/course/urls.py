from django.urls import path
from .views import course

app_name = 'courses'

urlpatterns = [
    path('', course, name='course'),
]
