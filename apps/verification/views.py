import random
import logging

from django.shortcuts import render
from django.http import HttpResponse

from utils.captcha import captcha
from . import constants

# Create your views here.


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
    request.session['img_code'] = text
    request.session.set_expiry(constants.IMG_CODE_EXPIRES)
    # 3记录日志
    logger = logging.getLogger('django')
    logger.info('生成了图片{}'.format(text))
    # 4返回验证码图片
    return HttpResponse(img_code, content_type='img', charset='utf8')

