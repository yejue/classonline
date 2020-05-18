from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
# Create your models here.


class UserManager2(UserManager):
    """
    # 修改创建账户时必须输入的信息条件
    """
    def create_superuser(self, username, password, email=None, **extra_fields):
        # 复写父类传入值，其余不变
        super(UserManager2, self).create_superuser(username, password, email, **extra_fields)


class User(AbstractUser):
    """
    自定义User抽象模型，添加 email， email_active 字段
    AbstractUser原本已包含提示: username, first_name, last_name, email, is_active
    """
    mobile = models.CharField(verbose_name='手机号', max_length=11, unique=True, help_text='手机号',
                              error_messages={'unique': '此手机号已被注册'})
    # 邮箱状态
    email_active = models.BooleanField(verbose_name='邮箱状态', default=False)

    class Meta:
        db_table = 'cls_user'                    # 指定迁移时的表名
        verbose_name = '用户'                    # 在admin站点中的显示名称
        verbose_name_plural = verbose_name      # 复数

    def __str__(self):
        return self.username, self.mobile

    # 通过 createsuperuser 命令创建超级账户的条件设置
    REQUIRED_FIELDS = ['mobile']

    # 修改创建账户时必须输入的信息条件,并执行实例
    objects = UserManager2()

