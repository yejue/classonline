from django.urls import path

from .views import \
    IndexView, WaitView, HomeView, MenuListView, MenuAddView, MenuUpdateView, UserListView, UserUpdateView, \
    GroupListView, GroupUpdateView, GroupAddView, NewsAdminView, NewsUpdateView, UploadFileView, NewsAddView, \
    TagListView, TagUpdateView, TagAddView, HotNewsListView, HotNewsUpdateView, HotNewsAddView, BannerListView, \
    BannerUpdateView, BannerAddView, DocListView, DocUpdateView, DocAddView, CourseListView, CourseUpdateView, CourseAddView

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

    path('tags/', TagListView.as_view(), name='news_tag_list'),
    path('tag/<int:tag_id>/', TagUpdateView.as_view(), name='news_tag_update'),
    path('tag/', TagAddView.as_view(), name='news_tag_add'),

    path('hotnewses/', HotNewsListView.as_view(), name='hotnews_list'),
    path('hotnews/<int:pk>/', HotNewsUpdateView.as_view(), name='hotnews_update'),
    path('hotnews/', HotNewsAddView.as_view(), name='hotnews_add'),

    path('banners/', BannerListView.as_view(), name='banner_list'),
    path('banner/<int:pk>/', BannerUpdateView.as_view(), name='banner_update'),
    path('banner/', BannerAddView.as_view(), name='banner_add'),

    path('docs/', DocListView.as_view(), name='doc_list'),
    path('doc/<int:pk>/', DocUpdateView.as_view(), name='doc_update'),
    path('doc/', DocAddView.as_view(), name='doc_add'),

    path('courses/', CourseListView.as_view(), name='course_list'),
    path('course/<int:pk>/', CourseUpdateView.as_view(), name='course_update'),
    path('course/', CourseAddView.as_view(), name='course_add'),
]