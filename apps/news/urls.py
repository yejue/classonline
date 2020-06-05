from django.urls import path
from .views import index, NewsSearchView, NewsListView, NewsBannerView, NewsDetailView, NewsCommentView

app_name = 'news'

urlpatterns = [
    path('', index, name='index'),
    path('search/', NewsSearchView.as_view(), name='search'),
    path('news/', NewsListView.as_view(), name='news_list'),
    path('banners/', NewsBannerView.as_view(), name='banners'),
    path('news/<int:news_id>', NewsDetailView.as_view(), name='news_detail'),
    path('news/<int:news_id>/comment/', NewsCommentView.as_view(), name='news_comment'),
]
