from django.shortcuts import render
from django.views import View
from django.http import JsonResponse

from .models import User
from utils.genCheckJson import genCheckJson


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


def check_username_view(request, username):
    """
    查询用户名是否存在
    url: /user/check=(?P<username>\w{5,20})
    :param request:
    :param username:
    :return:
    """
    data = {
            "username": username,   # 查询用户名
            "count": User.objects.filter(username=username).count()     # 查询用户数量
        }

    return JsonResponse(genCheckJson(data=data), charset='utf8')


def check_mobile_view(request, mobile):
    """
    查询手机号是否存在
    url:  /user/mobile=(?P\<mobile>1[3456789]\d{9}/
    :param request:
    :param mobile:
    :return:
    """

    data = {
        'mobile': '18666996101',
        'count': User.objects.filter(mobile=mobile).count()
    }
    return JsonResponse(genCheckJson(data=data), charset='utf8')
