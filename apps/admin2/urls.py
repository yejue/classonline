from django.urls import path

from .views import \
    IndexView, WaitView, HomeView, MenuListView, MenuAddView, MenuUpdateView, UserListView, UserUpdateView, \
    GroupListView, GroupUpdateView, GroupAddView, NewsAdminView, NewsUpdateView, UploadFileView, NewsAddView

app_name = 'admin'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('home/', HomeView.as_view(), name='home'),
    path('wait/', WaitView.as_view(), name='wait'),
    path('menus/', MenuListView.as_view(), name='menu_list'),
    path('menu/', MenuAddView.as_view(), name='add_menu'),
    path('menu/<int:menu_id>/', MenuUpdateView.as_view(), name='menu_manage'),
    path('users/', UserListView.as_view(), name='user_list'),
    path('user/<int:user_id>/', UserUpdateView.as_view(), name='user_update'),
    path('groups/', GroupListView.as_view(), name='group_list'),
    path('group/<int:group_id>/', GroupUpdateView.as_view(), name='update_group'),
    path('group/', GroupAddView.as_view(), name='add_group'),
    path('newsadmin/', NewsAdminView.as_view(), name='news_list'),
    path('news/<int:news_id>/', NewsUpdateView.as_view(), name='update_news'),
    path('upload/', UploadFileView.as_view(), name='upload'),
    path('news/', NewsAddView.as_view(), name='add_news'),
]