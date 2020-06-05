from django.urls import path
from .views import doc_index, DocDownload

app_name = 'doc'

urlpatterns = [
    path('', doc_index, name='docIndex'),
    path('<int:doc_id>/', DocDownload.as_view(), name='docDownload'),
]
