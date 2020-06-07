from django.urls import path
from .views import course_list, CourseDetailView

app_name = 'course'

urlpatterns = [
    path('', course_list, name='index'),
    path('<int:course_id>/', CourseDetailView.as_view(), name='course_detail'),

]
