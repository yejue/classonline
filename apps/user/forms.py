from django import forms
from django.core.validators import RegexValidator
from django_redis import get_redis_connection

from .constants import *
from .models import User
from verification.forms import mobile_validator

# 用户名限制 5~20个字母或数字
username_validators = RegexValidator('^\w{5,20}$', 1)


class RegisterForm(forms.Form):
    
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super(RegisterForm, self).__init__(*args, **kwargs)

    username = forms.CharField(label='用户名', max_length=MAX_USERNAME_LENGTH, min_length=MIN_USERNAME_LENGTH,
                               validators=[username_validators],
                               error_messages={
                                   'max_length': '用户名长度错误',
                                   'min_length': '用户名长度错误',
                                   'validators': '用户名格式为5~20个字母或数字',
                                   'required': '用户名不能为空',
                               })
    password = forms.CharField(label='密码', max_length=MAX_PASSWORD_LENGTH, min_length=MIN_PASSWORD_LENGTH,
                               error_messages={
                                   'max_length': '密码长度错误',
                                   'min_length': '密码长度错误',
                                   'required': '密码不能为空',
                               })
    password_repeat = forms.CharField(label='重复密码', max_length=MAX_PASSWORD_LENGTH, min_length=MIN_PASSWORD_LENGTH,
                                      error_messages={
                                          'max_length': '密码最大长度为{}'.format(MAX_PASSWORD_LENGTH),
                                          'min_length': '密码长度至少为{}'.format(MIN_PASSWORD_LENGTH),
                                          'required': '密码不能为空',
                                      })

    mobile = forms.CharField(label='手机号',
                             max_length=11, min_length=11, validators=[mobile_validator, ],
                             error_messages={
                                 'max_length': '手机号长度错误',
                                 'min_length': '手机号长度错误',
                                 'required': '手机号不能为空',
                             })
    sms_code = forms.CharField(label='短信验证码', error_messages={'required': '短信验证码不能为空'})

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('用户名已存在')
        return username

    def clean_mobile(self):
        mobile = self.cleaned_data.get('mobile')
        if User.objects.filter(username=mobile).exists():
            raise forms.ValidationError('手机号已被注册')
        return mobile

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        mobile = cleaned_data.get('mobile')
        password = cleaned_data.get('password')
        password_repeat = cleaned_data.get('password_repeat')
        sms_code = cleaned_data.get('sms_code')

        # 校验两次输入的密码是否一致
        if password != password_repeat:
            raise forms.ValidationError('两次输入的密码不一致')

        # 校验短信验证码是否正确
        # 连接redis
        redis_conn = get_redis_connection(alias='verify_code')
        real_sms_code = redis_conn.get('sms_text_{}'.format(mobile))
        if not real_sms_code and sms_code != real_sms_code:
            raise forms.ValidationError('短信验证码错误')

        return cleaned_data