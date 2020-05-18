from django.shortcuts import render
from django.views import View
from django.http import JsonResponse


from .forms import RegisterForm
from .models import User
from utils.res_code import Code, error_map
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
        # 1.校验数据
        form = RegisterForm(request.POST, request=request)
        if form.is_valid():
            # 新建数据
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            mobile = form.cleaned_data.get('mobile')
            # 新建用户
            User.objects.create_user(username=username, password=password, mobile=mobile)
            return JsonResponse(genCheckJson(errmsg='注册成功'))
        else:
            # 将表单错误信息进行拼接
            err_msg_str = '/'.join([item[0] for item in form.errors.values()])

            return JsonResponse(genCheckJson(errorno=Code.PARAMERR, errmsg=err_msg_str), charset='utf8')


