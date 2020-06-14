import random
import logging

from django.http import HttpResponse
from django.views import View
from django_redis import get_redis_connection

from user.models import User
from utils.res_code import Code, error_map
from utils.captcha import captcha
from utils.genJsonResponse import json_response
from . import constants
from .forms import CheckImageForm
from utils.huyiwuxian.sms3 import huyisms
from utils.yuntongxun.sms import CCP

# Create your views here.


# 日志器
logger = logging.getLogger('django')


def image_code_view(request):
    """
    图形验证码视图
    url: /veri/image_code
    :param request:
    :return:
    """
    # 1生成图形验证码
    text, img_code = captcha.captcha.generate_captcha()
    # 2保存验证码会话
    request.session['image_code'] = text
    request.session.set_expiry(constants.IMG_CODE_EXPIRES)
    # 3记录日志
    # logger = logging.getLogger('django')
    # logger.info('生成了图片{}'.format(text))
    # 4返回验证码图片
    return HttpResponse(img_code, content_type='img', charset='utf8')


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

    return json_response(data=data)


def check_mobile_view(request, mobile):
    """
    查询手机号是否存在
    url:  /veri/mobile=(?P\<mobile>1[3456789]\d{9}/
    :param request:
    :param mobile:
    :return:
    """

    data = {
        'mobile': mobile,
        'count': User.objects.filter(mobile=mobile).count()
    }
    return json_response(data=data)


class SmsCodeView(View):
    """
    发送短信验证码
    url:/sms_code/
    """
    def post(self, request):
        """

        - 发送短信验证码
        - 发送短信
        - 保存短信验证码
        - 保存发送记录
        :param request:
        :return:
        """
        form = CheckImageForm(request.POST, request=request)

        if form.is_valid():
            # 获取手机号
            mobile = form.cleaned_data.get('mobile')
            # 生成短信验证码
            sms_code = ''.join([str(random.choice([i for i in range(10)])) for _ in range(constants.SMS_CODE_LENGTH)])
            # 发送短信验证码
            # ccp = CCP()
            # # 注意： 测试的短信模板编号为1
            # result = None
            # for i in range(3):
            #     result = ccp.send_template_sms('{}'.format(mobile), ['{}'.format(sms_code), 5], "1")
            #     if result == 0:
            #         print('短信验证码发送成功！')
            #         break
            result = huyisms(smscode=sms_code, mobile=mobile)
            logger.info('{}，发送验证码{}成功'.format(mobile, sms_code))
            # 保存验证码 redis
            # 创建发送验证码记录的key
            sms_flag_key = 'sms_flag_{}'.format(mobile)
            sms_text_key = 'sms_text_{}'.format(mobile)
            redis_conn = get_redis_connection(alias='verify_code', )
            # 让管道通知redis
            pl = redis_conn.pipeline()

            try:
                # 设置生存时间与value
                pl.setex(sms_flag_key, constants.SMS_CODE_INTERVAL, 1)
                pl.setex(sms_text_key, constants.SMS_CODE_EXPIRES*60, sms_code)
                # 让管道通知 redis 执行
                pl.execute()
                return json_response(errmsg='短信验证码发送成功')
            except Exception as e:
                logger.error('redis 执行异常{}'.format(e))
                return json_response(errorno=Code.UNKOWNERR, errmsg=error_map[Code.UNKOWNERR])

        else:
            # 将表单错误信息进行拼接
            err_msg_str = '/'.join([item[0] for item in form.errors.values()])

            return json_response(errorno=Code.PARAMERR, errmsg=err_msg_str)





