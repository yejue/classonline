from django import forms
from django.core.validators import RegexValidator
from django_redis import get_redis_connection

from user.models import User

# 手机号码校验
mobile_validator = RegexValidator('^1[3-9]\d{9}$', 1)


class CheckImageForm(forms.Form):
    """
    - 校验手机号码
    - 校验图形验证码
    - 校验是否在60s内有发送记录
    """
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super(CheckImageForm, self).__init__(*args, **kwargs)

    mobile = forms.CharField(max_length=11, min_length=11, validators=[mobile_validator, ], error_messages={
        'max_length': '手机号长度错误',
        'min_length': '手机号长度错误',
        'required': '手机号不能为空',
    })
    captcha = forms.CharField(max_length=4, min_length=4, error_messages={
        'max_length': '图形验证码长度错误',
        'min_length': '图形验证码长度错误',
        'required': '图形验证码不能为空',
    })

    def clean(self):
        clean_data = super(CheckImageForm, self).clean()
        mobile = clean_data.get('mobile')
        captcha = clean_data.get('captcha')
        if mobile and captcha:
            # 校验图形验证码
            # 获取session中的验证进行比对
            image_code = self.request.session.get('image_code')
            if not image_code:
                raise forms.ValidationError('图形验证码失效')
            if image_code.upper() != captcha.upper():
                raise forms.ValidationError('图形验证码输入错误')

            # 是否在60s 以内发送过短信
            # 查询redis，存在则是60s内发送过
            redis_conn = get_redis_connection(alias='verify_code')
            if redis_conn.get('sms_flag_{}'.format(mobile)):
                raise forms.ValidationError('短信验证码获取过于频繁')

            # 校验手机号码是否被注册
            if User.objects.filter(mobile=mobile).exists():
                raise forms.ValidationError('手机号已被注册，请重新输入')

            return clean_data
