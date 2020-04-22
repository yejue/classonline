from django.urls import path
from .views import docDownload

app_name = 'doc'

urlpatterns = [
    path('', docDownload, name='docDownload'),
]
