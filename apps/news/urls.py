from django.urls import path
from .views import index, search, NewsListView

app_name = 'news'

urlpatterns = [
    path('', index, name='index'),
    path('search/', search, name='search'),
    path('news/', NewsListView.as_view(), name='news_list'),
]
