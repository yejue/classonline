from django.shortcuts import render
from django.views import View

# Create your views here.


def login(request):
    return render(request, 'user/login.html')


class Register(View):
    """
    注册视图
    url: /user/register
    """
    def get(self, request):
        return render(request, 'user/register.html')

    def post(self, request):
        pass
